---
id: scripts
title: Scripts
sidebar_label: Scripts
---

There are two categories of scripts one can write when developing a SOIL application: scripts that run when something happens for example when new data arrives and scripts that run on a schedule.

The entry points for these scripts are defined in the `soil.yml` file on the top of the project.

An example syntax of the file is the following:

```yml

setup: # Scripts to run when setting up the app for the first time.
    - on_setup:
        path: PATH

data:            # Defines pipeline to execute on new data arrival
    - first_script:
        path: PATH      # Path to script to execute
        params:
            param1: value1
            param2: value2
            ...
    - second_script:
        ...
    ...
    - last_script:        # Last script to be executed

schedules:              # Defines scripts that will be executed on a schedule
    - retrain:
        path: PATH
        schedule: 0 0 * * *         # Every day at 00:00
        params:
            param1: value1
            param2: value2
            ...
    - delete_last_year:
        path: PATH2
        schedule: 0 0 1 1 *         # 1st Jan at 00:00
    - saturday_night_predictions:
        path: PATH3
        schedule: 30 23 * * 6       # Saturdays at 23:30
    - update_every_5m:
        path: PATH4
        schedule: */5 * * * *       # Every 5 minutes
```
## Running scripts

To run script with soil you can do:
```sh
soil run [group] [script]
```

Where *group* is one of: *setup*, *data* or *schedules* and *script* is the name of a script inside that group.

Example:

```sh
soil run schedules retrain
```

It is possible to override params:

```sh
soil run schedules retrain --param1 new_value
```

## Synchronization issues
It is responsibility of the programmer to ensure there are no race conditions and to implement, if necessary, the required data locks to avoid syncronization issues.
