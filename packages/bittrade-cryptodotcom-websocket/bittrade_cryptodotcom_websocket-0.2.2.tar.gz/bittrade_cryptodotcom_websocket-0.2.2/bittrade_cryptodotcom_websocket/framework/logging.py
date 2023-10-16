from logging import LogRecord
from functools import partial


def does_not_contain_filter(reject_text: str, record: LogRecord) -> bool:
    return reject_text not in record.msg


no_open_orders = lambda: partial(
    does_not_contain_filter, '"method":"private/get-open-orders","code":0'
)
no_heartbeat = lambda: partial(does_not_contain_filter, '"method":"public/heartbeat"')
no_heartbeat_response = lambda: partial(
    does_not_contain_filter, '"method":"public/respond-heartbeat"'
)


def _set_direction(record: LogRecord):
    if "sent" in record.name:
        record.msg = f"<<< {record.msg}"
    elif "received" in record.name:
        record.msg = f">>> {record.msg}"
    return True


set_direction = lambda: _set_direction
