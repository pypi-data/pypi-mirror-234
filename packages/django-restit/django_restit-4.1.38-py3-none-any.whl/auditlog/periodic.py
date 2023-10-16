from rest.decorators import periodic
from taskqueue.models import Task


@periodic(hour=12, minute=30)
def run_log_cleanup(force=False, verbose=False, now=None):
    # schedule pruning
    Task.Publish("auditlog", "on_cleanup", channel="tq_app_handler_cleanup")


