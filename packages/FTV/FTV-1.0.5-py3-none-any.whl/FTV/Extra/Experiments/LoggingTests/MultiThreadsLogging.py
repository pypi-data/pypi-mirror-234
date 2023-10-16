import logging
import logging.handlers


ETT="TVAR 1"
objectname="TVAR 2"
URLFORLOG="TVAR 3"

def setup_custom_logger(name):
    fileLogName='visualreclogfile.log'
    #formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

    handlerCH = logging.StreamHandler()
    handlerCH.setFormatter(formatter)

    handlerFILE = logging.handlers.RotatingFileHandler(fileLogName, maxBytes=(1048576*5), backupCount=7)
    handlerFILE.setFormatter(formatter)


    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logger.addHandler(handlerCH)
    logger.addHandler(handlerFILE)

    return logger

def LoggingFileForELK(MessageToBeLogged):
    logger = setup_custom_logger('root')
    logger.info(MessageToBeLogged)


def mainFunction():
    Messages=("*** CONTENT LOGGING *** OBJECT UUID : %s WITH NAME KEY : %s HAS URL : %s ") %(ETT,objectname,URLFORLOG)
    MessageToBeLogged=str(Messages)
    LoggingFileForELK(MessageToBeLogged)




for i in range(5):
    mainFunction()