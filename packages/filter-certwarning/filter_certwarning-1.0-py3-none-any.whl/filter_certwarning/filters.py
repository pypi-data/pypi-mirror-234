import logging
import urllib3

from warnings import catch_warnings, simplefilter

mlog = logging.getLogger(__name__)


def _filter(action='once'):
    """Decorator to filter InsecureRequetWarnings when certificate verification is turned off
    """
    def decorator(function, *args, **kwargs):
        mlog.debug("warning filter action=" + action)

        def filtered(*fargs, **fkwargs):
            with catch_warnings():
                simplefilter(action, urllib3.connectionpool.InsecureRequestWarning)
                return function(*fargs, **fkwargs)

        return filtered

    return decorator


def warnonce(function):
    decorator = _filter('once')
    return decorator(function)


def silent(function):
    decorator = _filter('ignore')
    return decorator(function)
