import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

import schedule


def validate_dir(*args):
    for dir in args:
        if not os.path.isdir(dir):
            print(f"Error: Directory '{dir}' does not exist.")
            sys.exit(1)


def validate_file(*args):
    for file in args:
        if not os.path.isfile(file):
            print(f"Error: File '{file}' does not exist.")
            sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run tasks based on a schedule",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--work-dir",
        type=str,
        required=True,
        help="Directory to run tool in",
    )

    parser.add_argument(
        "-t", "--tasks", type=str, required=True, help="Tasks to schedule"
    )

    parser.add_argument(
        "-l",
        "--log-dir",
        type=str,
        required=True,
        help="Log directory",
    )

    args = parser.parse_args()

    # validate paths
    validate_dir(args.work_dir, args.log_dir)
    validate_file(args.tasks)

    return args


def verify_log_dir():
    try:
        os.makedirs("./logs", exist_ok=True)
    except OSError as e:
        print(f"Error while creating log directory: {e}")


def update_logs(res, command):
    curr_datetime = datetime.now()
    curr_time = curr_datetime.strftime("%H:%M:%S")
    curr_date = curr_datetime.strftime("%Y-%m-%d")

    try:
        if res.returncode != 0:
            with open("./logs/errors.log", "a") as err_log:
                err_log.write(
                    f"Got err: {res.stderr} for {command.strip()} at {curr_time} on {curr_date}\n"
                )

        with open("./logs/command.log", "a") as log:
            log.write(
                f"Ran {command.strip()} at {curr_time.hour}:{curr_time.minute}:{curr_time.second} on {curr_date}\n"
            )
    except IOError as e:
        print(f"Error while logging: {e}")


def schedule_process():
    try:
        res = subprocess.run(["ls", "-l"], capture_output=True, text=True)
        command = " ".join(res.args)
        update_logs(res, command)
    except Exception as e:
        print(f"Error while running command: {e}")


def main():
    verify_log_dir()
    schedule.every(5).seconds.do(schedule_process)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
