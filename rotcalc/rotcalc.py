import argparse, sys, json, os, lib

# Initial setup
if "settings.json" not in os.listdir("data"): lib.loadDefaults()

argList = [ # short,long,desc,type,options?
        ["-r", "--run", "run rotcalc with the current settings", "store_true"],
        ["-o", "--output", "send all output to file OUTPUT", "store"],
        ["-s", "--settings", "print current settings", "store_true"],

        ["-d", "--dataset", "change the active dataset (must be a filename in ./data/datasets, e.g 'Cheesecake.json')", "store"],
        ["-a", "--amount", "set amount of rotations to generate", "store"],
        ["-c", "--count", "set length of generated rotations, 9/10 recommended for infamy", "store"],
        ["-p", "--penalty", "toggles generating rotations that don't prevent heat penalties'", "store_true"],
        ["-g", "--goal", "change criteria for selecting best rotations", "store", ["xp", "time"]],
        ["-l", "--load", "specify a load time that will be added between every heist, use for approximating RTA timing", "store"],
]

# Add arguments defined by argList
parser = argparse.ArgumentParser(description="Tool for generating PAYDAY 2 heist rotations")
for arg in argList:
        match len(arg):
                case 4: parser.add_argument(arg[0], arg[1], help=arg[2], action=arg[3])
                case 5: parser.add_argument(arg[0], arg[1], help=arg[2], action=arg[3], choices=arg[4])

# Exit and print help if no arguments are provided
if len(sys.argv) == 1:
        parser.print_help()
        exit()

args = parser.parse_args()

# --- Settings arguments ---
if args.dataset:
        if args.dataset not in os.listdir("data/datasets"):
                raise Exception(f"Could not find dataset {args.dataset} in datasets folder")
        lib.changeSetting("dataset", args.dataset)

if args.amount:
        lib.printSettingUpdate("amount", lib.getSettings()["amount"], args.amount)
        lib.changeSetting("amount", int(args.amount))

if args.goal:
        lib.printSettingUpdate("goal", lib.getSettings()["goal"], args.goal)
        lib.changeSetting("goal", args.goal)

if args.penalty:
        lib.changeSetting("allowPenalties", not lib.getSettings()["allowPenalties"])
        print(f"Penalties are now {"allowed" if lib.getSettings()["allowPenalties"] else "prohibited"}")

if args.count:
        lib.printSettingUpdate("heistCount", lib.getSettings()["heistCount"], args.count)
        lib.changeSetting("heistCount", int(args.count))

if args.load:
        lib.printSettingUpdate("loadTime", lib.getSettings()["loadTime"], args.count)
        lib.changeSetting("loadTime", int(args.load))

# --- Info arguments ---
if args.settings:
        for setting in lib.getSettings(): print(f"{setting}: {lib.getSettings()[setting]}")

# --- Run arguments ---
if args.run:
        from calculator import generateRotations, plotRotation
        generateRotations(lib.getSettings()["amount"], lib.getSettings()["heistCount"], not lib.getSettings()["allowPenalties"], lib.getSettings()["loadTime"], lib.getSettings()["goal"], args.output)
