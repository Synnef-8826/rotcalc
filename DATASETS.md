This file is a brief overview on the datasets format for storing heist information RotCalc can work with.

An example dataset (`data/datasets/Cheesecake.json`) is provided in the repo.

# JSON structure
- `rotationData`:

  - `name`: dataset name
  
  - `description`: optional as it's currently unused, describes what the dataset is for
  
  - `players`: number of players from the run the dataset is derived from. Used for calculating extra XP from the Crew Alive bonus and Team Boosts equipped on weapons
      - WARNING: 2 Team Boosts per player is assumed, if your needs are different (like the need for Concealment boosts) let me know!

  - `initialHeist`: the rotation's initial heist, must be the `id` of an entry in `heists`
        
- `heists`: array of every heist in the dataset. Each heist is composed of:

   - `id`: heist name used internally. Only requirement is being a valid key in Python dictionaries, avoid spaces and anything that isn't a-z, A-Z, 0-9, `-` and `_`.
   
   - `prettyName`: heist name used in output

   - `difficulty`: the difficulty of the heist represented as a number from 0-6, 0 being Normal and 6 being Death Sentence
   
   - `xp`: final base XP reward from the heist, including all objectives and secured bags
   
   - `stealthBonus`: stealth bonus given by the heist that will carry over to the next mission
   
     - Must be `multiplier-1`, for example, a 5% SB is represented as `1.05 - 1 = 0.05`
     
   - `avgTime`: average time taken to complete the heist while meeting the previous criteria. Measured in seconds
   
   - `bestTime`: lowest time ever obtained for the heist. Used for displaying average and best possible times in generated rotations. Measured in seconds
   
   - `gagePacks`: each Gage package adds +0.5% to the cumulative XP bonuses (read [Reputation](https://payday.fandom.com/wiki/Reputation_(Payday_2)#Factors_affecting_earned_XP) page on the game's wiki), this option is available to account for that but can be safely set to `0` in the majority of cases.
