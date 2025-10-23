import csv, json, os

# TODO: make crew alive bonus dependent on the number of players to allow datasets for solo/duo/trio rotations
def getHeistXp(heistData, rotationData, stealthBoost):
    return ((heistData["xp"] + (heistData["bagsCollected"] * heistData["xpPerBag"])) * (1 + 0.45 + 2.05 + (0.03 * (2*rotationData["players"])) + (0.1*(rotationData["players"]-1)) + (0.005 * heistData["gagePacks"]))) * (stealthBoost+1) * 15

def getCsvData(file):
    parsedCsv = []
    for row in csv.reader(open(file, encoding="utf-8")): 
        if len(row) > 1: parsedCsv.append(row) # skips comment lines
    return parsedCsv

def getSettings(): return json.loads(open("data/settings.json", "r").read())

def setSettings(newSettings):
    open("data/settings.json", "w").write(json.dumps(newSettings))

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
        ["dataset", os.listdir("data/datasets")[0].replace(".csv","")],
        ["amount", 100000],
        ["heistCount", 10],
        ["allowPenalties", False],
        ["goal", "xp"],
        ["loadTime", 0]
        ]:
        changeSetting(setting[0], setting[1])
    input("[WARNING] A default configuration has been loaded due to empty or incomplete settings. Please revise the rotcalc settings")

def printSettingUpdate(key, old, new): print(f"Changed {key} {old}->{new}")
