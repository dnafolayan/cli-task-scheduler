import subprocess
from datetime import datetime

curr_datetime = datetime.now()

curr_time = curr_datetime.time()
curr_date = curr_datetime.date()

res = subprocess.run(["ls", "-l"], capture_output=True, text=True)

if res.returncode != 0:
    print(res.stderr)

command = ""
for arg in res.args:
    command = command + arg + " "

# update logs
with open("./logs/command.log", "a") as log:
    log.write(
        f"Ran {command.strip()} at {curr_time.hour}:{curr_time.minute}:{curr_time.second} on {curr_date}"
    )
