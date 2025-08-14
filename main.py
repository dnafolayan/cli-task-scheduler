import subprocess
from datetime import datetime

curr_datetime = datetime.now()

curr_time = curr_datetime.time()
curr_date = curr_datetime.date()

res = subprocess.run(["ls", "-l"], capture_output=True, text=True)

command = ""
for arg in res.args:
    command = command + arg + " "

if res.returncode != 0:
    with open("./logs/errors.log", "a") as err_log:
        err_log.write(
            f"Got err: {res.stderr} for {command.strip()} at {curr_time.hour}:{curr_time.minute}:{curr_time.second} on {curr_date}\n"
        )
    print(res.stderr)


# update logs
with open("./logs/command.log", "a") as log:
    log.write(
        f"Ran {command.strip()} at {curr_time.hour}:{curr_time.minute}:{curr_time.second} on {curr_date}\n"
    )
