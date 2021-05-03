import os
from subprocess import run, PIPE
from msvcrt import getch
import threading
from datetime import datetime, timedelta
from time import sleep
import re

APP_NAME_ASCII_ARTWORK = r"""
  _______ _                     _               _                    _     _              _          __   ___  
 |__   __(_)                   | |             | |     /\           (_)   | |            | |        /_ | / _ \ 
    | |   _ _ __ ___   ___  ___| |__   ___  ___| |_   /  \   ___ ___ _ ___| |_ __ _ _ __ | |_  __   _| || | | |
    | |  | | '_ ` _ \ / _ \/ __| '_ \ / _ \/ _ \ __| / /\ \ / __/ __| / __| __/ _` | '_ \| __| \ \ / / || | | |
    | |  | | | | | | |  __/\__ \ | | |  __/  __/ |_ / ____ \\__ \__ \ \__ \ || (_| | | | | |_   \ V /| || |_| |
    |_|  |_|_| |_| |_|\___||___/_| |_|\___|\___|\__/_/    \_\___/___/_|___/\__\__,_|_| |_|\__|   \_/ |_(_)___/ """

session_active_artwork = """
                                      ╔═╗╔═╗╔═╗╔═╗╦╔═╗╔╗╔  ╔═╗╔═╗╔╦╗╦╦  ╦╔═╗
                                      ╚═╗║╣ ╚═╗╚═╗║║ ║║║║  ╠═╣║   ║ ║╚╗╔╝║╣ 
                                      ╚═╝╚═╝╚═╝╚═╝╩╚═╝╝╚╝  ╩ ╩╚═╝ ╩ ╩ ╚╝ ╚═╝"""


def cmd(command):
    cmd_out = run(command.split(" "), shell=True, stdout=PIPE, stderr=PIPE, timeout=2)

    return {"return_code": cmd_out.returncode,
            "stdout": cmd_out.stdout.decode('utf-8'),
            "stderr": cmd_out.stderr.decode('utf-8')}


def terminate():
    print("\n" + "=" * 115)
    print("\nThank You for using TimesheetAssistant v1.0 !")
    print("If you fou this code useful, please share the GitHub Repository :D")
    print("\n" + "=" * 115)
    input("\nPress ENTER to Exit...")
    exit(0)


def key_wait():
    global session_active
    while ord(getch()) != 145:
        pass
    session_active = False


print(APP_NAME_ASCII_ARTWORK, end='\n\n')
print("{:^115s}".format("By Sagar Dev Achar (https://www.github.com/SagarDevAchar/)"))
print("{:^115s}".format("Artworks generated by https://www.textkool.com/"))

print("\n" + "=" * 115, end='\n\n')

TIMESHEET_HEAD = "\nDate,Session Start,Session End,Work Duration,Summary"

folder_name = os.path.realpath(__file__).split("\\")[-2]

if 'timesheet_meta.bin' not in os.listdir():
    input("No Timesheet maintained! Press ENTER to Initialize...")

    project_name = folder_name
    if input("\nDo you want to use the Folder Name as the Project Name [Y / N] : ").strip().upper()[0] == 'N':
        project_name = input("Enter the Project Name : ").strip()
    print("\nInitializing TimesheetAssistant for Project \"%s\"..." % project_name)

    git_support = input("Do you want Git Support [Y / N] : ").strip().upper()[0] == 'Y'
    if git_support:
        git_check = cmd("git --version")
        if git_check['return_code'] == 0:
            print(git_check['stdout'].replace("\n", " found"))
            git_support = True
            TIMESHEET_HEAD += ",Git Commit SHA\n"

            git_init = cmd("git init")
            if git_init['return_code'] == 0:
                print(git_init['stdout'].replace("\n", ""))
                open(".gitignore", 'a').close()
                print("Please consider setting up Git for this project now...")
        else:
            print("git was not found on this PC! Please make sure git is installed and setup properly (with PATH)")
            terminate()
    else:
        TIMESHEET_HEAD += "\n"

    with open('timesheet_meta.bin', 'w') as TIMESHEET_META:
        TIMESHEET_META.write("folder_name={:s}|project_name={:s}|git_support={:s}|work_time={:d}d {:d}h {:d}m"
                             .format(folder_name,
                                     project_name,
                                     "Enabled" if git_support else "Disabled",
                                     0, 0, 0))

    with open('timesheet.csv', 'a') as TIMESHEET:
        TIMESHEET.write(TIMESHEET_HEAD)

    print("\n" + "=" * 115, end='\n\n')

TIMESHEET_META_DATA = {}
with open('timesheet_meta.bin', 'r') as TIMESHEET_META:
    for data in TIMESHEET_META.read().split("|"):
        prop = data.split("=")
        TIMESHEET_META_DATA[prop[0]] = prop[1]

print("Project : " + TIMESHEET_META_DATA['project_name'])
print("Git Support : " + TIMESHEET_META_DATA['git_support'])
print("Current Work Time : " + TIMESHEET_META_DATA['work_time'])

if 'timesheet.csv' not in os.listdir():
    print("\nLooks like the Timesheet has been deleted!")
    print("Creating a new Timesheet...")
    with open('timesheet.csv', 'a') as TIMESHEET:
        TIMESHEET.write(TIMESHEET_HEAD)
        if TIMESHEET_META_DATA['git_support'] == "Enabled":
            TIMESHEET.write(",Git Commit SHA")
        TIMESHEET.write("\n")

while True:
    print("\n" + "=" * 115)

    while True:
        command = input("\nEnter \'Start\' to start timing your work session or \'Quit\' to exit : ").strip()
        if command == "Start":
            break
        elif command == "Quit":
            terminate()
        else:
            print("Wrong Confirmation Command! Input is CASE SENSITIVE")

    START_TIME = datetime.now()

    print(session_active_artwork)
    print("{:^115s}".format("[ Press <Ctrl> + <Alt> + <Q> to stop the session ]"), end='\n\n')

    session_active = True
    key_thread = threading.Thread(target=key_wait, daemon=True)
    key_thread.start()

    while session_active:
        delta = str(datetime.now() - START_TIME).split(".")[0].split(":")
    
        print("\r{:^115s}".format("{:s} hours {:s} minutes {:s} seconds".format(delta[0], delta[1], delta[2])), end="")
        sleep(1)

    END_TIME = datetime.now()
    print("\n\nSession Completed!\n")

    current_session_info = {}

    if TIMESHEET_META_DATA['git_support'] == "Enabled":
        if input("Do you want to link a Git Commit to your session [Y / N] : ").strip().upper()[0] == 'Y':
            sha_input = input("Please enter the SHA1 Hash of the commit [use -r for recent] : ").strip().lower().replace("-r", "")
            if sha_input != "":
                sha_input = " " + sha_input
            commit_info = cmd(r'git log --pretty=format:"%H::%B" -n 1' + sha_input)['stdout'].replace("\"", "").replace("\n", "").split("::")
            if len(commit_info) == 2:
                current_session_info["sha1"] = commit_info[0]
                current_session_info["message"] = commit_info[1]
                print("Linked COMMIT %s to current session!" % current_session_info["sha1"].upper(), end='\n\n')
            else:
                current_session_info["sha1"] = None
                current_session_info["message"] = ""
                print("Failed to get commit info!", end='\n\n')
        else:
            current_session_info["sha1"] = None
            current_session_info["message"] = ""
    else:
        current_session_info["sha1"] = None
        current_session_info["message"] = ""

    if current_session_info['message'] == "":
        if input("Do you want to add a message to your session [Y / N] : ").strip().upper()[0] == 'Y':
            current_session_info["message"] = input("MESSAGE : ").strip()
            print("Added message to current session!")
        print("")

    current_work_time_seconds = (END_TIME - START_TIME).total_seconds()

    previous_time_data = list(map(int, re.findall(r"\d", TIMESHEET_META_DATA['work_time'])))
    total_work_time_minutes = int(previous_time_data[0] * 1440 + previous_time_data[1] * 60 + previous_time_data[2] +
                                  current_work_time_seconds // 60)

    current_work_time = [0, 0]
    current_work_time[0] = current_work_time_seconds // 3600
    current_work_time_seconds -= current_work_time[0] * 3600
    current_work_time[1] = current_work_time_seconds // 60

    total_work_time = [0, 0, 0]
    total_work_time[0] = total_work_time_minutes // 1440
    total_work_time_minutes -= total_work_time[0] * 1440
    total_work_time[1] = total_work_time_minutes // 60
    total_work_time_minutes -= total_work_time[1] * 60
    total_work_time[2] = total_work_time_minutes

    while True:
        try:
            with open('timesheet.csv', 'a') as TIMESHEET:
                TIMESHEET.write(START_TIME.strftime("%d/%m/%Y,%H:%M:%S,"))
                TIMESHEET.write(END_TIME.strftime("%H:%M:%S,"))
                TIMESHEET.write("%dh %dm," % (current_work_time[0], current_work_time[1]))
                TIMESHEET.write("\"%s\"" % current_session_info['message'])
                if current_session_info['sha1']:
                    TIMESHEET.write("," + current_session_info['sha1'])
                TIMESHEET.write("\n")
            print("Current Session Logged in Timesheet!")
            break
        except Exception:
            input("Looks like the Timesheet is open! Please close it and press ENTER to proceed...")

    while True:
        try:
            with open('timesheet_meta.bin', 'w') as TIMESHEET_META:
                TIMESHEET_META.write("folder_name={:s}|project_name={:s}|git_support={:s}|work_time={:d}d {:d}h {:d}m"
                                     .format(TIMESHEET_META_DATA['folder_name'],
                                             TIMESHEET_META_DATA['project_name'],
                                             TIMESHEET_META_DATA['git_support'],
                                             total_work_time[0], total_work_time[1], total_work_time[2]))

            print("Refreshed the Metadata BIN!")
            break
        except Exception:
            input("Looks like the Metadata File is open! Please close it and press ENTER to proceed...")

terminate()
