import argparse
import json
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


def update_logs(result, command):
    curr_datetime = datetime.now()
    curr_time = curr_datetime.strftime("%H:%M:%S")
    curr_date = curr_datetime.strftime("%Y-%m-%d")

    try:
        args = parse_args()
        result_file = os.path.join(args.log_dir, "results.log")
        error_file = os.path.join(args.log_dir, "errors.log")

        if result.returncode != 0:
            with open(error_file, "a") as err_log:
                err_log.write(
                    f"Got err: {result.stderr} for {command} at {curr_time} on {curr_date}\n"
                )

        with open(result_file, "a") as res_log:
            res_log.write(
                f"Got output: {result.stdout} for {command} at {curr_time} on {curr_date}\n"
            )
    except IOError as e:
        print(f"Error while logging: {e}")


def run_command():
    try:
        args = parse_args()

        with open(args.tasks, "r") as f:
            data = json.load(f)

        for task in data.get("tasks", []):
            command = task.get("command")

            if not command:
                print("No command found in task, skipping...")
                continue

            result = subprocess.run(
                command, capture_output=True, cwd=args.work_dir, shell=True, text=True
            )

            update_logs(result, command)
    except Exception as e:
        print(f"Error while running command: {e}")


def schedule_task():
    # todo: schedule each task to run based on the type, time, minute, second provided in the tasks.json
    pass


def main():
    # todo: update main to run schedule task after implementation of the func
    schedule.every(5).seconds.do(run_command)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
