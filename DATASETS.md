This file is a brief overview on the datasets format for storing heist information RotCalc can work with.

An example dataset (`data/datasets/Cheesecake.json`) is provided in the repo.

# JSON structure
- `rotationData`:

  - `name`: dataset name
  
  - `description`: optional as it's currently unused, describes what the dataset is for
  
  - `players`: number of players from the run the dataset is derived from. Used for calculating extra XP from the Crew Alive bonus and Team Boosts equipped on weapons
      - WARNING: 2 Team Boosts per player is assumed, if your needs are different (like the need for Concealment boosts) let me know!
        
- `heists`: array of every heist in the dataset. Each heist is composed of:

   - `id`: heist name used internally. Only requirement is being a valid key in Python dictionaries, avoid spaces and anything that isn't a-z, A-Z, 0-9, `-` and `_`.
   
   - `prettyName`: heist name used in output
   
   - `xp`: base XP reward from the heist, including all objectives and excluding all bag pickups
   
   - `xpPerBag`: XP per collected bag. For heists with multiple loot types that each give different XP the average value per bag must be used
   
   - `bagsCollected`: amount of secured bags
   
   - `stealthBonus`: stealth bonus given by the heist that will carry over to the next mission
   
     - Must be `1-multiplier`, for example, a 5% SB is represented as `0.05`
     
   - `avgTime`: average time taken to complete the heist while meeting the previous criteria
   
   - `bestTime`: lowest time ever obtained for the heist. Used for displaying average and best possible times in generated rotations
   
   - `gagePacks`: each Gage package adds +0.5% to the cumulative XP bonuses (read [Reputation](https://payday.fandom.com/wiki/Reputation_(Payday_2)#Factors_affecting_earned_XP) page on the game's wiki), this option is available to account for that but can be safely set to `0` in the majority of cases.
