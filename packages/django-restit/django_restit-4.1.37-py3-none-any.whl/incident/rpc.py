from rest import decorators as rd
from rest import views as rv
from rest import helpers as rh
from rest import settings
from . import models as am
from .parsers import ossec
from taskqueue.models import Task


@rd.urlPOST(r'^ossec/alert$')
def ossec_alert_creat_from_request(request):
    payload = request.DATA.get("payload")
    if payload:
        try:
            # TODO make this a task (background it)
            od = ossec.parseAlert(request, payload)
            # lets now create a local event
            if od is not None:
                level = 10
                if od.level > 10:
                    level = 1
                elif od.level > 7:
                    level = 2
                elif od.level == 6:
                    level = 3
                elif od.level == 5:
                    level = 4
                elif od.level == 4:
                    level = 6
                elif od.level <= 3:
                    level = 8
                metadata = od.toDict(graph="default")
                if od.geoip:
                    metadata["country"] = od.geoip.country
                    metadata["city"] = od.geoip.city
                    metadata["province"] = od.geoip.state
                    metadata["isp"] = od.geoip.isp
                am.Event.createFromDict(None, {
                    "hostname": od.hostname,
                    "description": od.title,
                    "details": od.text,
                    "level": level,
                    "category": "ossec",
                    "component": "incident.ServerOssecAlert",
                    "component_id": od.id,
                    "metadata": metadata
                })
        except Exception:
            rh.log_exception("during ossec alert", payload)
    return rv.restStatus(request, False, error="no alert data")


@rd.urlGET(r'^ossec$')
@rd.urlGET(r'^ossec/(?P<pk>\d+)$')
@rd.login_required
def on_ossec(request, pk=None):
    return am.ServerOssecAlert.on_rest_request(request, pk)


@rd.urlPOST(r'^event$')
def rest_on_create_event(request, pk=None):
    # TODO check for key?
    resp = am.Event.on_rest_request(request)
    return rv.restStatus(request, True)


@rd.urlGET(r'^event$')
@rd.urlGET(r'^event/(?P<pk>\d+)$')
@rd.login_required
def rest_on_event(request, pk=None):
    return am.Event.on_rest_request(request, pk)


@rd.url(r'^incident$')
@rd.url(r'^incident/(?P<pk>\d+)$')
@rd.login_required
def rest_on_incident(request, pk=None):
    return am.Incident.on_rest_request(request, pk)


@rd.url(r'^incident/history$')
@rd.url(r'^incident/history/(?P<pk>\d+)$')
@rd.login_required
def rest_on_incident_history(request, pk=None):
    return am.IncidentHistory.on_rest_request(request, pk)


@rd.url(r'^rule$')
@rd.url(r'^rule/(?P<pk>\d+)$')
@rd.login_required
def rest_on_rule(request, pk=None):
    return am.Rule.on_rest_request(request, pk)


@rd.url(r'^rule/check$')
@rd.url(r'^rule/check/(?P<pk>\d+)$')
@rd.login_required
def rest_on_rule_check(request, pk=None):
    return am.RuleCheck.on_rest_request(request, pk)


# BEGIN FIREWALL
@rd.urlPOST(r'^ossec/firewall$')
def ossec_firewall_event(request):
    data = request.DATA.toObject()
    # rh.debug("firewall event", data)
    gip = ossec.GeoIP.lookup(data.ip)
    if gip:
        data.country = gip.country
        data.province = gip.state
        data.city = gip.city
        data.isp = gip.isp
        data.ip_hostname = gip.hostname
    if data.action == "add":
        data.action = "blocked"
    else:
        data.action = "unblocked"
    title = f"FIREWALL: {data.ip} {data.action} on {data.hostname}"
    am.Event.createFromDict(None, dict(
        hostname=data.hostname,
        reporter_ip=data.ip,
        description=title,
        details=title,
        category="firewall",
        level=6,
        metadata=data
    ))
    # now block the ip globally
    if settings.FIREWALL_GLOBAL_BLOCK:
        Task.Publish("incident", "firewall_block", dict(ip=data.ip), channel="tq_broadcast")
    return rv.restStatus(request, True)


@rd.urlGET(r'^firewall$')
# @rd.superuser_required
def rest_firewall_blocked(request, pk=None):
    return rv.restReturn(request, dict(data=dict(blocked=rh.getBlockedHosts())))


@rd.urlPOST(r'^firewall$')
@rd.superuser_required
@rd.requires_params(["ip", "action"])
def rest_firewall_block(request):
    # block the ip globally
    ip = request.DATA.get("ip")
    action = request.DATA.get("action")
    if action not in ["block", "unblock"]:
        return rv.restPermissionDenied(request)
    Task.Publish("incident", f"firewall_{action}", dict(ip=ip), channel="tq_broadcast")
    return rv.restStatus(request, True)
