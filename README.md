# NOTICE
There are some individuals that have repeatedly attempted to claim PAYDAY 2's speedrunning community's achievements and innovations as theirs for their own community's benefit. **While this project's license allows for private use of the licensed software, be aware that anyone claiming it as theirs without providing credit to THIS repository nor performing any changes to the original project is being dishonest.**

Thank you for reading and your understanding. If the people this notice is referring to are reading this, which I know you are, this is a project for the entire community, so we appreciate that you spread the voice so we all benefit from it.

Making this notice is my decision and my decision alone.

# RotCalc
A simple python script to generate [PAYDAY 2](https://www.paydaythegame.com/payday2/) heist rotations. Made for streamlining [speedrun.com](https://www.speedrun.com/pd2ce)'s Infamy Solo and Co-op run development.

![ezgif com-optimize](https://github.com/user-attachments/assets/6b126f08-c37e-4304-93b1-2b97bfdd9b33)

## Features
- Generate heist rotations based on data from past runs
- Make rotations of different heist lengths
- Aim for minimum time from level 0 -> 100 or for maximum XP gain
- Attempts to prevent [heat XP penalties](https://payday.fandom.com/wiki/Reputation_(Payday_2)#Heat_System), conformant with Infamy Solo/Co-op Restricted rules
- Add artificial loading times to simulate RTA runs
- *Blazingly fast!* 🚀 <sub>~god i hated typing that~</sub>

## Prerequisites
- Python (3.13.7 was used, exact minimum version is TBD)
- [tqdm](https://github.com/tqdm/tqdm?tab=readme-ov-file#installation)
- A Windows, MacOS, Linux or Android device <sub>_or, alternatively, [AIX, HP-UX, IBM i, iOS, iPadOS, RISC OS, Solaris, the UEFI shell enviroment or z/OS](https://www.python.org/download/other/), apparently_</sub>

## Setup and usage
- Download the repo and make a [Python virtual environment](https://docs.python.org/3/library/venv.html) in it
- `pip install tqdm`
- Activate the venv when using. If the demand is there I'll make and package a separate version without any external dependencies.

## [Heist dataset formatting](https://github.com/Synnef-8826/rotcalc/blob/main/DATASETS.md)
