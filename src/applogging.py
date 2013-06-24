import logging
import logging.handlers
import os

def set_up():
    # Loggers
    rootLogger = logging.getLogger('')

    if len(rootLogger.handlers) == 0:
        # Formatters
        simple_formatter   = logging.Formatter("%(levelname)s - %(message)s")
        extended_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Handlers
        logFile       = os.path.dirname(__file__)+os.path.sep+'logs/error.log'
        fileHandler   = logging.handlers.RotatingFileHandler(
            logFile, maxBytes=10485760, backupCount=10
        )
        fileHandler.setFormatter(extended_formatter)

        # Loggers setup
        rootLogger.addHandler(fileHandler)
        rootLogger.level = logging.DEBUG

        # stdout logging during the development
        console = logging.StreamHandler()
        console.setFormatter(extended_formatter)
        console.setLevel(logging.DEBUG)
        rootLogger.addHandler(console)

set_up();
