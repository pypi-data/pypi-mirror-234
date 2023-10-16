import importlib
import logging
import traceback

from tornado.options import options


def sentry_monitor():
    sentry_config = options.sentry_config
    enable = sentry_config.pop("enable", False)
    if enable:
        try:
            sentry_sdk = importlib.import_module("sentry_sdk")
            sentry_sdk_tornado = importlib.import_module("sentry_sdk.integrations.tornado")
        except ImportError:
            raise Exception(f"sentry-sdk is not exist,run:pip install sentry-sdk==1.22.2")
        integrations = sentry_config.pop("integrations", [])
        if "before_send_transaction" not in sentry_config:
            sentry_config["before_send_transaction"] = lambda transaction, hint: \
                before_send_transaction(transaction, hint)
        if "before_send" not in sentry_config:
            sentry_config["before_send"] = lambda event, hint: before_send(event, hint)
        try:
            sentry_sdk.init(
                integrations=[
                    sentry_sdk_tornado.TornadoIntegration(),
                ] if not integrations else integrations,
                **sentry_config
            )
        except Exception:
            logging.error(traceback.format_exc())


def before_send(event, hint):
    try:
        if isinstance(event, dict):
            event_level = event.get("level")
            event_exception = event.get("exception")
            if isinstance(event_exception, dict):
                event_values = event_exception.get("values", [])
                event_types = []
                if event_values:
                    event_types = [event_value.get("type") for event_value in event_values if
                                   isinstance(event_value, dict)
                                   if
                                   event_value.get("type") == 'BusinessException']
                if event_level == "error":
                    if 'BusinessException' in event_types:
                        return None
                    else:
                        return event
                else:
                    return None
            else:
                return event
        else:
            return event
    except Exception as e:
        return event


def before_send_transaction(transaction, hint):
    return None
