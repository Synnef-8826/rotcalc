import csv, json, os, math

difficultyMultipliers = [
        1,
        3,
        6,
        11,
        12.5,
        14,
        15,
    ]

# Gets player's current level from their current XP by referencing expTable.csv
def getCurrentLevel(totalXp):
    level = 0

    for lv in getCsvData("data/expTable.csv"):
        if totalXp >= int(lv[1]): level += 1
        else: break

    return {"current": level, "nextRemaining": round(totalXp / int(getCsvData("data/expTable.csv")[level][1]), 4) if level < 100 else 1, "skillPoints": level + (2*(math.trunc(level/10)))}


# Gets a heist's XP payout for the current parameters
def getHeistXp(heistData, rotationData, stealthBoost):
    return (heistData["xp"] * (1 + 0.45 + 2.05 + (0.03 * (2*rotationData["players"])) + (0.1*(rotationData["players"]-1)) + (0.005 * heistData["gagePacks"]))) * (stealthBoost+1) * difficultyMultipliers[heistData["difficulty"]]


# Reads CSV files
def getCsvData(file):
    parsedCsv = []
    for row in csv.reader(open(file, encoding="utf-8")): 
        if len(row) > 1: parsedCsv.append(row) # skips comment lines
    return parsedCsv


def getSettings(): return json.loads(open("data/settings.json", "r").read())


def setSettings(newSettings): open("data/settings.json", "w").write(json.dumps(newSettings))


def changeSetting(setting, value):
    settings = getSettings()
    settings[setting] = value
    setSettings(settings)


# Loads a default configuration and warns the user about it
def loadDefaults():
    # Raise error if there are no datasets in data/datasets
    if len(os.listdir("data/datasets")) == 0:
        print("No datasets found in ./data/datasets")
        exit(1)

    # Create settings file
    with open("data/settings.json", "x") as file:
        file.write("{}")

    for setting in [
        ["dataset", os.listdir("data/datasets")[0]],
        ["amount", 100000],
        ["heistCount", 10],
        ["allowPenalties", False],
        ["goal", "time"],
        ["loadTime", 0]
        ]:
        changeSetting(setting[0], setting[1])
    input("[WARNING] A default configuration has been loaded due to empty or incomplete settings. Please revise the rotcalc settings")


def printSettingUpdate(key, old, new): print(f"Changed {key} {old}->{new}")
