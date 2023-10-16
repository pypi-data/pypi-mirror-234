def manage_retries(partial_function, handled_exceptions, propagate_exceptions, retries, backoff=True):
    from logging import getLogger
    from time import sleep
    success = False
    attempts = 0
    results = None
    delay = 1
    logger = getLogger()
    while attempts < retries and not success:
        try:
            results = partial_function()
        except handled_exceptions as e:
            attempts += 1
            if retries == attempts and propagate_exceptions:
                raise e
            else:
                logger.warning(e)
                if backoff:
                    sleep(delay)
                    delay *= 2
        else:
            success = True
    return results
