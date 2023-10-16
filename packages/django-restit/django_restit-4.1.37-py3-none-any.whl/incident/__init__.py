from objict import objict

META_KEYS = ["SERVER_PROTOCOL", "REQUEST_METHOD", "QUERY_STRING", "HTTP_USER_AGENT"]


def event(category, description, level=10, request=None, **kwargs):
    from taskqueue.models import Task
    data = objict(category=category, description=description, level=level)
    data.metadata = objict.fromdict(kwargs)
    Task.Publish("incident", "new_event", channel="tq_app_handler", data=data)


def event_now(category, description, level=10, request=None, **kwargs):
    from .models.event import Event
    data = objict(category=category, description=description, level=level)
    data.metadata = objict.fromdict(kwargs)
    if request is not None:
        data.metadata.ip = request.ip
        if "path" not in data.metadata:
            data.metadata.path = request.path
        for key in META_KEYS:
            value = request.META.get(key, None)
            if value is not None and isinstance(value, str) and "." not in key:
                data.metadata[key.lower()] = str(value)
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
    Event.createFromDict(None, data)
