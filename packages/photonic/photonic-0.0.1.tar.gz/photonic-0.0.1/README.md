# Photonic Utilities Library
## Description
Photonic is the library where I upload all my neat tools!

### _logging
This package is designed to make logging easier and customizable.  

**Quick start:**  
1) You need to configure your logger before using it, here is an example:


    logger_name = "my_logger"

    console_config(logger_name)  # This makes the logger log to the console (with colors)!
    json_file_config(logger_name)  # This makes the logger log to a json file (more detailed too).

2) Now, we are all set! To use the logger all you need to do is:


    logger = getLogger("my_logger")

    logger.debug(f"Test Message from logger.debug")
    logger.info(f"Test Message from logger.info")
    logger.warning(f"Test Message from logger.warning")
    logger.error(f"Test Message from logger.error")
    logger.critical(f"Test Message from logger.critical")

This code will log the messages to both the console and the json file.

You can use custom formats for the message or the provided formats in the logging.formatters.Format enum.

### utils
Utils are a group of functions that are nice to have ready for you.
Note: the functions currently in the package are meant to be used as a decorator.
Example:

    @threaded
    def treaded_function():
        # some code

Now, `threaded_function` will start in a new thread whenever called.

### enums
This package is a place where I put enums that I might use in the future.
Currently, it has one enum called `AnsiColor` which contains some of the colors used in the console.
Example:

    print(AnsiColor.red.value + "Example Error Text." + AnsiColor.reset.value)

## Contact Me!
If you have any suggestions to add to the library you can [email me](mailto:asem.sh2004@gmail.com). 
I am open to any constructive criticism!