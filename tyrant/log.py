
_log_enabled = False

def set_logging(log):
    import tyrant.log
    tyrant.log._log_enabled = log

def log_enabled():
    return _log_enabled

def log(message):
    print message
