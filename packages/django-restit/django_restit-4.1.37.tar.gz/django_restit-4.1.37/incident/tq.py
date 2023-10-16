"""
This is where you can put handlers for running async background tasks

Task.Publish("myapp", "on_tq_test")
"""
# from datetime import datetime, timedelta
# from auditlog.models import PersistentLog
# from django.conf import settings
from incident.models import Event
from rest import helpers
from rest import settings


def new_event(task):
    data = task.data
    if "hostname" in data.metadata:
        data.hostname = data.metadata.hostname
    if "details" in data.metadata:
        data.details = data.metadata.details
    if "component" in data.metadata:
        data.component = data.metadata.component
    if "component_id" in data.metadata:
        data.component_id = data.metadata.component_id
    if "ip" in data.metadata:
        data.reporter_ip = data.metadata.ip
    Event.createFromDict(None, task.data)
    task.completed()


def firewall_block(task):
    # Task.Publish("incident", "firewall_block", {ip:"x.x.x.x"}, channel="tq_broadcast")
    helpers.blockIP(task.data.ip)
    task.log(f"{settings.HOSTNAME} - {task.data.ip} BLOCKED")
    task.completed()


def firewall_unblock(task):
    # Task.Publish("incident", "firewall_unblock", {ip:"x.x.x.x"}, channel="tq_broadcast")
    helpers.unblockIP(task.data.ip)
    task.log(f"{settings.HOSTNAME} - {task.data.ip} UNBLOCKED")
    task.completed()

