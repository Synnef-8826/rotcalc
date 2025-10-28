from lib import getHeistXp, getSettings
import copy, time, tqdm, math, random, sys, json
from datetime import datetime, timedelta
from tqdm import tqdm

heists = json.loads(open(f"./data/datasets/{getSettings()["dataset"]}", "r").read())["heists"]
rotation = json.loads(open(f"./data/datasets/{getSettings()["dataset"]}", "r").read())["rotationData"]
startTime = time.time()

# Precalculate heist XP gain without stealth bonuses for faster rot generation
heistXpTable = {}
for heist in heists:
    heistXpTable[heist["id"]] = getHeistXp(heist, rotation, 0)

# Associates each heist's data with its ID, used for finding heist data faster when plotting rotations
heistsTable = {}
for heist in heists:
    heistsTable[heist["id"]] = heist

# Determine if dataset enforces an initial heist
if "initialHeist" in rotation: initialHeist = rotation["initialHeist"]

# Prints summary to stdout or a given file after operations have completed
def printResults(scannedRotations, xp, timesAvg, timesBest, goal, loadTime, dumpFile):
    if dumpFile != None:
        print(f"Saved output to {dumpFile}")
        sys.stdout = open(dumpFile, "w")
        print("Generated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

    # Prints different information based on goal
    match goal:
        case "time":
            print(f"\nFastest run found:\n- IGT: {timedelta(seconds=timesAvg[timesAvg.index(min(timesAvg))])} avg / {timedelta(seconds=timesBest[timesAvg.index(min(timesAvg))])} best\n- RTA: {timedelta(seconds=((timesAvg[timesAvg.index(min(timesAvg))]) + ((loadTime * len(scannedRotations[0])))))} avg / {timedelta(seconds=((timesBest[timesAvg.index(min(timesAvg))]) + ((loadTime * len(scannedRotations[0])))))} best\n- {math.trunc(xp[timesAvg.index(min(timesAvg))])} XP ({math.trunc(xp[timesAvg.index(min(timesAvg))]) - 23336413} overflow)\n\n---HEIST LIST---\n{scannedRotations[timesAvg.index(min(timesAvg))]}\n")

            print("\n---ROTATION DETAILS---")
            plotRotation(scannedRotations[timesAvg.index(min(timesAvg))], True)

            print(f"Speed avg (for benchmarking): {getSettings()["amount"] / ((time.time() - startTime))} rots/s")

        case "xp":
            print(f"Most lucrative run found:\n- Average: {round(timesAvg[xp.index(max(xp))]/60, 3)} minutes\n- Best:    {round(timesBest[xp.index(max(xp))]/60, 3)} minutes\n- {math.trunc(xp[xp.index(max(xp))])} XP\n\n---HEIST LIST:---\n{scannedRotations[xp.index(max(xp))]}\n---END OF HEIST LIST---")

            print("\n---ROTATION DETAILS---\n")
            plotRotation(scannedRotations[xp.index(max(xp))], True)

# Simpler function to get total rotation XP that improves performance
def getRotationXp(heistList):
    xp = 0
    stealthBoost = 0
    for heist in heistList:
        heistData = heistsTable[heist]
        xp += heistXpTable[heistData["id"]] * (stealthBoost+1)
        stealthBoost = heistData["stealthBonus"]
    return xp

# Returns information about the passed rotation and optionally prints it
def plotRotation(heistList, printDetails):
    xp = 0
    timeAvg = 0
    timeBest = 0
    stealthBoost = 0

    i = 0
    for heist in heistList:
        heistData = heistsTable[heist]

        xp += heistXpTable[heistData["id"]] * (stealthBoost+1)
        if printDetails: print(f"Heist {i+1}: {heistData["prettyName"]}\n- Takes {heistData["avgTime"]} seconds\n- Earns {math.trunc(heistXpTable[heistData["id"]] * (stealthBoost+1))} XP {f"(x{stealthBoost+1} SB)" if i > 0 and stealthBoost > 0 else ""}\n")

        stealthBoost = heistData["stealthBonus"]
        timeAvg += heistData["avgTime"]
        timeBest += heistData["bestTime"]

        i += 1

    return {"xp": xp, "timeAvg": timeAvg, "timeBest": timeBest}

# Randomly generates the given amount of rotations
def generateRotations(amount, heistCount, preventPenalties, loadTime, goal, dumpFile):
    if "initialHeist" in rotation: heistCount -= 1
    maxRepeats = 2 if preventPenalties else 999

    # Lowers cooldowns for every heist provided by the dataset. Combines all Diamond Store variations so it works properly
    def lowerCooldowns(cd):
        for h in heists:
            heist = h["id"]
            if "ds" in heist: heist = "ds"

            if cd[heist] > 0: cd[heist] -= 1
        return cd

    # Returns how many instances of a given heist are already in the rotation. Combines all Diamond Store variations. Used to meet Restricted speedrun.com rules
    def getRepeats(heist):
        if not preventPenalties: return 0 # makes this function faster when allowing penalties

        if "ds" in heist: return repeats["ds"]
        else: return repeats[heist]

    ## Adds 1 to heist count
    def addRepeat(heist):
        if "ds" in heist: repeats["ds"] += 1
        else: repeats[heist] += 1

    # These will hold information about every generated rotation and its respective information
    scannedRotations = []
    timesAvg = []
    timesBest = []
    xp = []

    # Prepares heistList and heistCooldowns based on the provided dataset. Combines all Diamond Store variations
    heistList = []
    heistCooldowns = {}
    repeats = {}
    for heist in heists:
        heistList.append(heist["id"])

        if "ds" in heist["id"]:
            heistCooldowns["ds"] = 0
            repeats["ds"] = 0
        else:
            heistCooldowns[heist["id"]] = 0
            repeats[heist["id"]] = 0

    # Main rotation generation loop
    for i in tqdm(range(amount), total = amount, unit = " rots", desc=f"Working..."):
        rot = [initialHeist] if "initialHeist" in rotation else []

        # Reset repeats dict
        repeats = {}
        for heist in heists:
            if "ds" in heist["id"]: repeats["ds"] = 0
            else: repeats[heist["id"]] = 0

        # Randomly generates a rotation
        for i in range(heistCount):
            heistCooldowns = lowerCooldowns(heistCooldowns) # Refresh cooldowns

            while True:
                randomHeist = random.choice(heistList) # Pick a heist
                if "ds0" in randomHeist: continue # Makes sure DS0 cannot appear more than once

                # Gets current cooldown for random heist
                if "ds" in randomHeist: currentCd = heistCooldowns["ds"]
                else: currentCd = heistCooldowns[randomHeist]

                if currentCd == 0:

                    # Applies cooldown if penalties are being prevented
                    if preventPenalties:
                        if getRepeats(randomHeist) >= maxRepeats: continue # prevents choosing heists that have been played the max number of times allowed

                        addRepeat(randomHeist)
                        if "ds" in randomHeist: heistCooldowns["ds"] = 3
                        else: heistCooldowns[randomHeist] = 3
                    break

            rot.append(randomHeist) # Add heist to rotation

        # Plot the generated rotation and add its information to times/xp lists
        if getRotationXp(rot) >= 23336413:
            summary = plotRotation(rot, False)
            scannedRotations.append(rot)
            timesAvg.append(summary["timeAvg"])
            timesBest.append(summary["timeBest"])
            xp.append(summary["xp"])

    printResults(scannedRotations, xp, timesAvg, timesBest, goal, loadTime, dumpFile) # Print the best found rotation based on goal argument
