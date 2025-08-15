# CLI Task Scheduler - Automate the boring stuff

A lightweight, Python-based task scheduler that runs commands on a defined schedule, logs results, and handles both success and error outputs.  
Perfect for automating recurring tasks, backups, or data processing scripts on Linux systems.

---

## Features

-   **JSON-configurable tasks** — Define multiple tasks with commands and schedules in a single file.
-   **Multiple schedule types** — Support for daily, minute-based, and second-based intervals.
-   **Logging system** — Separate logs for successes (`results.log`) and errors (`errors.log`).
-   **Command execution in specific directory** — Run all tasks from a specified working directory.
-   **Command-line interface** — Flexible arguments for directories and task files.
-   **Continuous execution** — Uses a background loop to run pending jobs automatically.

---

## Example `tasks.json`

```json
{
    "tasks": [
        {
            "command": "echo 'Hello World'",
            "schedule": {
                "type": "daily",
                "time": "14:00"
            }
        },
        {
            "command": "ls -al",
            "schedule": {
                "minutes": 5
            }
        },
        {
            "command": "python3 script.py",
            "schedule": {
                "seconds": 30
            }
        }
    ]
}
```

# Usage

## Prepare directories

Make sure you have:

-   A **working directory** (`--work-dir`) — where commands will run.
-   A **log directory** (`--log-dir`) — where logs will be stored.
-   A **tasks JSON file** (`--tasks`) — list of commands and schedules.

---

## Run the Job Runner

```bash
python3 runner.py \
  --work-dir /path/to/workdir
  --tasks /path/to/tasks.json
  --log-dir /path/to/logdir
```

## Logs

-   `results.log` — Stores successful command outputs with timestamps.
-   `errors.log` — Stores failed command errors with timestamps.

# Requirements

-   Python 3.8+
-   Install dependencies:

```bash
pip install schedule
```

# Future Improvements

-   Concurrency so multiple tasks can run in parallel.

-   Retry mechanism for failed tasks.
