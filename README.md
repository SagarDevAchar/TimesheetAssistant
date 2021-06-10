# TimesheetAssistant
A CLI Application with Git Support to manage a Work Timesheet on your project

Click [here](https://github.com/SagarDevAchar/TimesheetAssistant/releases) to download the **latest release**

## Release Notes

- **v1.1**: Bugfixed the Regex which was causing Total Time computational errors for the Metadata BIN File

## Requirements and Dependencies
- **Operating System:** Windows
- Properly set-up **Git** added to the system's **PATH** variable (if Git Support required, *TimesheetAssistant* works without Git Support too..)

Here are a few Git links that would be useful:
- Download [Git for Windows](https://git-scm.com/download/win)
- Git [Documentation](https://git-scm.com/docs)
- Git [Cheatsheet](https://training.github.com/)

## Files in Repository
- **LICENSE** : MIT License for *TimesheetAssistant*
- **README.md** : Here you are!
- **TimesheetAssistant.py** : The Source Code for the latest version of *TimesheetAssistant*
- **exe_gen.bat** : The batch file with the pyinstaller command to generate the EXE
- **TimesheetAssistant.ico** : The icon for the EXE

## How it works
To use *TimesheetAssistant* in a project, just **copy the EXE** to that folder and run it to start Timetracking your work

1. On initializing the *TimesheetAssistant*, **2 files** are created in your project directory
   - **timesheet.csv** : The Actual Timesheet in CSV format. Why CSV you ask? It is simple to write and data can be read and parsed easily directly or with Pandas
   - **timesheet_meta.bin** : A Metadata Binary File which holds the info about the current project's timesheet. Deleting this will reinitialize the timesheet
2. Type in **"Start"** to start timing your session. The timer keeps running until you stop the session or terminate the program
3. Press the Hotkey Combination **`Ctrl`+`Alt`+`Q`** to **stop** the current session
4. Please make sure both the *TimesheetAssistant* files are **closed** to allow proper updation of data
5. If you want to exit *TimesheetAssistant*, just type in **"Quit"** before the start of a new session

Compressed to EXE using PyInstaller (check out the PyInstaller command in the **exe_gen.bat** script)

## That's it I guess...

Please share this repository if you find *TimesheetAssistant* useful
