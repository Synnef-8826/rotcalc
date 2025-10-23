from lib import getHeistXp, getSettings
import copy, time, tqdm, math, random, sys, json
from datetime import datetime
from tqdm import tqdm

heists = json.loads(open(f"./data/datasets/{getSettings()["dataset"]}.json", "r").read())["heists"]
rotation = json.loads(open(f"./data/datasets/{getSettings()["dataset"]}.json", "r").read())["rotationData"]

# Prints summary to stdout or a given file after operations have completed
def printResults(scannedRotations, xp, timesAvg, timesBest, goal, loadTime, dumpFile):
    if dumpFile != None:
        print(f"Saved output to {dumpFile}")
        sys.stdout = open(dumpFile, "w")
        print("Generated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

    # Prints different information based on goal
    match goal:
        case "time":
            print(f"\nFastest run found:\n- Average: {round(timesAvg[timesAvg.index(min(timesAvg))]/60, 3)} minutes\n- Best:    {round(timesBest[timesAvg.index(min(timesAvg))]/60, 3)} minutes\n- Average (RTA): {round((timesAvg[timesAvg.index(min(timesAvg))]/60) + ((loadTime * len(scannedRotations[0]))/60), 3)} minutes\n- Best    (RTA): {round((timesBest[timesAvg.index(min(timesAvg))]/60) + ((loadTime * len(scannedRotations[0]))/60), 3)} minutes \n- {math.trunc(xp[timesAvg.index(min(timesAvg))])} XP ({math.trunc(xp[timesAvg.index(min(timesAvg))]) - 23336413} overflow)\n\n---HEIST LIST:---\n{scannedRotations[timesAvg.index(min(timesAvg))]}\n---END OF HEIST LIST---")

            print("\n---ROTATION DETAILS---")
            plotRotation(scannedRotations[timesAvg.index(min(timesAvg))], True)
            print("---END OF ROTATION DETAILS---")

        case "xp":
            print(f"Most lucrative run found:\n- Average: {round(timesAvg[xp.index(max(xp))]/60, 3)} minutes\n- Best:    {round(timesBest[xp.index(max(xp))]/60, 3)} minutes\n- {math.trunc(xp[xp.index(max(xp))])} XP\n\n---HEIST LIST:---\n{scannedRotations[xp.index(max(xp))]}\n---END OF HEIST LIST---")

            print("\n---ROTATION DETAILS---\n")
            plotRotation(scannedRotations[xp.index(max(xp))], True)
            print("---END OF ROTATION DETAILS---")

# Returns information about the passed rotation and optionally prints it
def plotRotation(heistList, printDetails):
    xp = 0
    timeAvg = 0
    timeBest = 0
    stealthBoost = 0

    i = 0
    for heist in heistList:
        for h in heists:
            if h["id"] == heist: heistData = h

        xp += getHeistXp(heistData, rotation, stealthBoost)
        if printDetails: print(f"Heist {i+1}: {heistData["prettyName"]}\n- Takes {heistData["avgTime"]} seconds\n- Earns {getHeistXp(heistData, rotation, stealthBoost)} XP {f"(x{stealthBoost+1} SB)" if i > 0 and stealthBoost > 0 else ""}\n")

        stealthBoost = heistData["stealthBonus"]
        timeAvg += heistData["avgTime"]
        timeBest += heistData["bestTime"]

        i += 1

    return {"xp": xp, "timeAvg": timeAvg, "timeBest": timeBest}

# Randomly generates the given amount of rotations
def generateRotations(amount, heistCount, preventPenalties, loadTime, goal, dumpFile):
    maxRepeats = 2 if preventPenalties else 999

    # Lowers cooldowns for every heist provided by the dataset. Combines all Diamond Store variations so it works properly
    def lowerCooldowns(cd):
        for h in heists:
            heist = h["id"]
            if "ds" in heist: heist = "ds"

            if cd[heist] > 0: cd[heist] -= 1
        return cd

    # Returns how many instances of a given heist are already in the rotation. Combines all Diamond Store variations. Used to meet Restricted speedrun.com rules
    def findRepeats(rot, heist):
        repeats = 0
        if not ("ds" in heist): return rot.count(heist)
        else:
            for i in rot:
                if heist in i or ("ds" in heist and "ds" in i): repeats += 1
        return repeats

    # These will hold information about every generated rotation and its respective information
    scannedRotations = []
    timesAvg = []
    timesBest = []
    xp = []

    # Prepares heistList and heistCooldowns based on the provided dataset. Combines all Diamond Store variations
    heistList = []
    heistCooldowns = {}
    for heist in heists:
        heistList.append(heist["id"])

        if "ds" in heist["id"]: heistCooldowns["ds"] = 0
        else: heistCooldowns[heist["id"]] = 0

    # Main rotation generation loop
    for i in tqdm(range(amount), total = amount, unit = " rots", desc=f"Generating random {heistCount}-heist rotations"):
        rot = ["ds0_14"] # Rotations always start with DS0 because it's the most consistent heist at LV0 and gives room for enough skills to meet the rest of heist times

        # Randomly generates a rotation
        for i in range(heistCount-1):
            heistCooldowns = lowerCooldowns(heistCooldowns) # Refresh cooldowns

            while True:
                randomHeist = random.choice(heistList) # Pick a heist

                # Gets current cooldown for random heist
                if "ds" in randomHeist: currentCd = heistCooldowns["ds"]
                else: currentCd = heistCooldowns[randomHeist]

                # If cooldown is ready, picked heist is not DS0 and we haven't gone over the repeat limit, add heist to the rotation
                if "ds0" not in randomHeist and currentCd == 0 and findRepeats(rot, randomHeist) < maxRepeats:

                    # Applies cooldown if penalties are being prevented
                    if preventPenalties:
                        if "ds" in randomHeist: heistCooldowns["ds"] = 3
                        else: heistCooldowns[randomHeist] = 3
                    break

            rot.append(randomHeist) # Add heist to rotation

        # Plot the generated rotation and add its information to times/xp lists
        summary = plotRotation(rot, False)
        if summary["xp"] >= 23336413:
            scannedRotations.append(rot)
            timesAvg.append(summary["timeAvg"])
            timesBest.append(summary["timeBest"])
            xp.append(summary["xp"])

    printResults(scannedRotations, xp, timesAvg, timesBest, goal, loadTime, dumpFile) # Print the best found rotation based on goal argument
