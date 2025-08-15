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
    for fl in args:
        if not os.path.isfile(fl):
            print(f"Error: File '{fl}' does not exist.")
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


def update_logs(result, command, log_dir):
    curr_datetime = datetime.now()
    curr_time = curr_datetime.strftime("%H:%M:%S")
    curr_date = curr_datetime.strftime("%Y-%m-%d")

    try:
        # args = parse_args()
        result_file = os.path.join(log_dir, "results.log")
        error_file = os.path.join(log_dir, "errors.log")

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


def execute_command(command, work_dir):
    return subprocess.run(
        command,
        capture_output=True,
        cwd=work_dir,
        shell=True,
        text=True,
    )


def run_task():
    try:
        args = parse_args()

        with open(args.tasks, "r") as f:
            data = json.load(f)

        for task in data["tasks"]:
            command = task["command"]

            if not command:
                print("No command found in task, skipping...")
                continue

            if task["schedule"]["type"] == "daily":
                schedule.every().day.at(str(task["schedule"]["time"])).do(
                    lambda cmd=command: update_logs(
                        execute_command(cmd, args.work_dir), cmd, args.log_dir
                    )
                )
            elif "minutes" in task["schedule"]:
                schedule.every(task["schedule"]["minutes"]).minutes.do(
                    lambda cmd=command: update_logs(
                        execute_command(cmd, args.work_dir), cmd, args.log_dir
                    )
                )
            elif "seconds" in task["schedule"]:
                schedule.every(task["schedule"]["seconds"]).seconds.do(
                    lambda cmd=command: update_logs(
                        execute_command(cmd, args.work_dir), cmd, args.log_dir
                    )
                )
            else:
                print(f"Unknown schedule type for task: {task}, skipping...")
    except Exception as e:
        print(f"Error while running command: {e}")


def main():
    run_task()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
