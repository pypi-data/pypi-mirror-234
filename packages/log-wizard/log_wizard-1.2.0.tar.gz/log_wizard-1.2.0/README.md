# log_wizard

## Installation
To get started with Log Wizard, you can easily install it using pip
```bash
pip install log-wizard
```

## usage
```python
from log_wizard import DefaultConfig, log
# initilize DefaultConfig if need
# You can do it onece, before first call of log
# Also look at params for DefaultConfig
# info_file_postfix takes all log msgs except .debug
# debug_file_postfixh takes all log msgs

DefaultConfig(info_file_postfix = 'info', debug_file_postfixh = 'debug')
# I can add a handler for your own function
# DefaultConfig().set_ui_log_func(print)


# now in any module of your project you can use this log
log = log()

# write log info
log.info("info") # 20.09.2023 06:10:35 - INFO - info
log.error("error") # 20.09.2023 06:10:35 - ERROR - error
log,critical("critical") # 20.09.2023 06:10:35 - CTITICAL - critical
proc_id = '12345'
with log.insert_proc_id(proc_id):
    #20.09.2023 06:10:35 - INFO - 12345 - here should be proc id
    log.info("here should be proc id")
    with log.insert_func_name():
        log.info("here also should be proc id and a func name, where log was called")
```

## Configuration
You can configure Log Wizard by modifying the DefaultConfig class.

## Features
Insert process IDs into log messages
Insert function names into log messages
Supports different log levels (info, error, debug, critical, etc.)

## License
This project is licensed under the Apache License, Version 2.0 - see the LICENSE file for details.

## Contact
For any questions or feedback, feel free to contact me at ruslan.izhakovskij@gmail.com.
