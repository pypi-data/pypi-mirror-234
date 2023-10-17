from liveramp_automation.utils.log import Logger


def test_logInfo():
    Logger.info("AAA")


def test_logError():
    Logger.error("Error")


def test_logDebug():
    Logger.debug("Debug")


def test_logWarning():
    Logger.warning("warning")
