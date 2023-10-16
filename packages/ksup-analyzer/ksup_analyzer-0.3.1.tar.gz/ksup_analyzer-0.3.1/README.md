# KSUP Analyzer

This is based on the csup_analyzer.

## What
Reads replay files (the .header files) from the game [Karting Superstars](https://store.steampowered.com/app/2503220/Karting_Superstars/) and offers tools to analyze the extracted data. 

This

The replay files hold information about (for quali and race respectively):
- lap times
- fastest lap times
- time penalties per lap (no slow down penalties)
- metres driven
- number of laps driven
- number of laps led
- total race time
- track name and layout
- driver car
- driver/car color codes
- if driver is an AI
- driver name
- driver platform

Besides reading them out of the files in a well-structured way and serving them via a pandas DataFrame (very popular in python data analysis) it also calculates more variables out of those provided:
- time until starting line (basically the time until you start lap 1)
- race start position
- race finish position
- race positions by lap

## Who
This is a community project kicked-off by Dremet but everyone is welcome to contribute and use the code, see Licence at the bottom.

## When
This project was launched at the beginning of September 2023 when Karting Superstars was released. Previously, the csup_anazlyer was launched at the end of June 2023 when the version 1.5.0 of the game was released because the .header replay files did not hold that much valuable information before.

## Why
The purpose of this libary is to analyze race data. There is currently no API you can request race data/statistics from and also there is no in-game race history/statistics functionality.

Another reason for this project is that the initial author, Dremet, is administrating the community website https://www.csup.app/ which offers league administration, standings calculations, an elo list, driver statistics etc. Until the 1.5.0 patch there was no way to automatically enter race results into the database behind the website. Extracting data from the .header files is the first step to (semi-) automize result entry. The plan is to launch a CSUP.APP discord bot that offers a `/enter_results {race_id} {header_files}` command for organizers to enter results easily. That bot would use this library to extract the data from the replay files.

## How
After each race you can find a .header file for each session (e.g. one for qualification and one for the race) in a folder. Assuming your main drive is named **"C:"** as well you only need to replace "WINDOWS_USER" and "SOME_USER_ID" in the follow folder path to find the replay files on your computer:

`C:\Users\WINDOWS_USER\AppData\LocalLow\Original Fire Games\Karting Superstars\SOME_USER_ID\race-recordings`

If you just want to use the library, simply install it like any other library with `pip install ksup_analyzer` or `pdm add ksup_analyzer`. 

If you want to develop/contribute and you use pdm for your python environments you should be able to easily set up the environment with the pyproject.toml file (`pdm install`). Otherwise a `requirements.txt` file is provided. 

Afterwards you can adapt the file paths in `run.py` to test it and have fun with the modified pandas DataFrame accessible via `event.result_df`. 


## Contribute

You are very welcome to work on this project and create pull requests! Feel free to contact me (Dremet) on Discord. You'll find me on (almost) all CSUP/OFG (Original Fire Games) discord servers.

If you want to add calculations please have a look at `ksup_analyzer/event/Result.py`.

If you want to add visualization support please go to `ksup_analyzer/plots/Plots.py`.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

