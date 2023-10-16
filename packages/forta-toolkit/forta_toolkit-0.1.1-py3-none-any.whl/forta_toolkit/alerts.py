"""Statistics on the bot alert rate."""

import collections
import functools

# INIT ########################################################################

def init_alert_history(size: int) -> collections.deque:
    """Creates a FIFO of fixed size N to store the alerts for the latest N transactions."""
    return collections.deque(size * [()], size)

# UPDATE ######################################################################

def update_alert_history(fifo: collections.deque, alerts: tuple) -> None:
    """Push the alert ids for the latest block into the history."""
    fifo.append(alerts)

# PROCESS #####################################################################

def calculate_alert_rate(fifo: collections.deque, alert: str) -> float:
    """Calculate the alert rate for a given id over the last N transactions."""
    return min(sum([__t.count(alert) for __t in fifo]) / len(fifo), 1.)

# WRAPPER #####################################################################

def alert_history(size: int) -> callable:
    """Creates a decorator for handle_transaction to add an alert history."""
    __history = init_alert_history(size=size)

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and handles the alert history."""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            __findings = func(*args, **kwargs)
            update_alert_history(fifo=__history, alerts=tuple(__f.alert_id for __f in __findings))
            for __f in __findings:
                __f.metadata['anomaly_score'] = calculate_alert_rate(fifo=__history, alert=__f.alert_id)
            return __findings

        return __wrapper

    return __decorator
