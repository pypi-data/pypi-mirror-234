from django.db import models
from rest import settings

from rest import models as rm
from rest import helpers as rh
from taskqueue.models import Task
from account.models import Member
from objict import objict
from datetime import datetime, timedelta
from rest import log
from ws4redis import client as ws4redis
import time

logger = log.getLogger("incident", filename="incident.log")

INCIDENT_STATE_NEW = 0
INCIDENT_STATE_OPENED = 1
INCIDENT_STATE_PAUSED = 2
INCIDENT_STATE_IGNORE = 3
INCIDENT_STATE_RESOLVED = 4

INCIDENT_STATES = [
    (INCIDENT_STATE_NEW, "new"),
    (INCIDENT_STATE_OPENED, "opened"),
    (INCIDENT_STATE_PAUSED, "paused"),
    (INCIDENT_STATE_IGNORE, "ignored"),
    (INCIDENT_STATE_RESOLVED, "resolved"),
]


class Incident(models.Model, rm.RestModel, rm.MetaDataModel):
    class RestMeta:
        POST_SAVE_FIELDS = ["level", "catagory"]
        SEARCH_FIELDS = ["description", "hostname"]
        # VIEW_PERMS = ["example_permission"]
        GRAPHS = {
            "default": {
                "extra": ["metadata", ("get_state_display", "state_display")],
                "graphs": {
                    "group": "basic",
                    "rule": "basic",
                    "assigned_to": "basic"
                },
            }
        }

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=200)
    component = models.CharField(max_length=200, null=True, default=None, db_index=True)
    hostname = models.CharField(max_length=200, null=True, default=None, db_index=True)
    reporter_ip = models.CharField(max_length=16, blank=True, null=True, default=None, db_index=True)

    group = models.ForeignKey("account.Group", on_delete=models.SET_NULL, null=True, default=None)
    assigned_to = models.ForeignKey("account.Member", on_delete=models.SET_NULL, null=True, default=None)
    
    priority = models.IntegerField(default=0)  # 1-10, 1 being the highest
    state = models.IntegerField(default=0, choices=INCIDENT_STATES)  # 0=new, 1=opened, 2=paused, 3=ignore, 4=resolved
    action_sent = models.DateTimeField(default=None, null=True)

    rule = models.ForeignKey("incident.Rule", on_delete=models.SET_NULL, null=True, default=None)

    @property
    def first_event(self):
        return self.events.first()
    
    def triggerAction(self, force=False):
        if self.rule is None:
            if self.action_sent is None:
                self.triggerAsyncNotify()
                self.triggerNotify()
            return
        if self.action_sent is not None and not force:
            return

        # if self.rule.bundle == 0:
        #     return
        # only do query if not 0
        logger.info("triggerAction", self.rule.action)
        if force or self.rule.action_after == 0 or self.rule.action_after < self.events.all().count():
            logger.info(f"triggering incident action: {self.rule.action}")
            self.triggerAsyncNotify()
            if self.rule.action is None or self.rule.action == "notify":
                self.triggerNotify()
            elif self.rule.action.startswith("email:") or self.rule.action.startswith("notify:"):
                self.triggerEmail()
            elif self.rule.action.startswith("sms:"):
                self.triggerSMS()
            elif self.rule.action.startswith("task:"):
                self.triggerTask()

    def triggerAsyncNotify(self):
        msg = dict(
            created=time.mktime(self.created.timetuple()),
            description=self.description,
            component=self.component,
            hostname=self.hostname)
        if self.rule is not None:
            msg["rule"] = self.rule.name
        event = self.first_event
        if event is not None:
            msg["catagory"] = event.category
            msg["details"] = event.getProperty("details")
            msg["hostname"] = event.hostname
            msg["username"] = event.getProperty("username")
            msg["server"] = event.getProperty("server")
            msg["ip"] = event.getProperty("ip")
            msg["method"] = event.getProperty("method")
        try:
            ws4redis.sendMessageToPK("incident", "all", msg)
        except Exception:
            rh.log_exception("triggerAsyncNotify")

    def triggerTask(self):
        # task:APP_NAME:FNAME:CHANNEL
        fields = self.rule.action.split(':')
        if len(fields) < 4:
            rh.log_error("triggerTask failed, invalid field count")
            return
        self.action_sent = datetime.now()
        self.save()
        Task.Publish(fields[1], fields[2], channel=fields[3])

    def triggerEmail(self):
        # email:NOTIFY_SETTING or email:bob@example.com
        action, perm = self.rule.action.split(":")
        self.action_sent = datetime.now()
        self.save()
        # notify with perm
        self.notifyWith(perm)

    def triggerSMS(self):
        # sms:NOTIFY_SETTING
        self.action_sent = datetime.now()
        self.save()
        action, perm = self.rule.action.split(":")
        members = Member.GetWithNotification(perm)
        msg = f"{settings.SITE_LABEL}\nNew Incident: {self.description}"
        for m in members:
            m.sendSMS(msg)  

    def notifyWith(self, perm):
        logger.info("notifyWith", perm)
        Member.notifyWith(
            perm,
            subject=F"New Incident Priority: {self.priority} - {self.component} - {self.hostname}",
            template=settings.get("INCIDENT_TEMPLATE", "email/incident_plain.html"),
            context=dict(incident=self, portal_url=settings.INCIDENT_PORTAL_URL),
            email_only=True)

    def triggerNotify(self):
        self.action_sent = datetime.now()
        self.save()
        if self.group is not None:
            # all member of the group are notified because it is an incident group
            self.group.notifyMembers(
                subject=F"New Incident Priority: {self.priority} - {self.component} - {self.hostname}",
                template=settings.get("INCIDENT_TEMPLATE", "email/incident_plain.html"),
                context=dict(incident=self, portal_url=settings.INCIDENT_PORTAL_URL),
                email_only=True)
        else:
            self.notifyWith("unknown_incidents")

    def on_rest_saved(self, request, is_new=False):
        if not is_new:
            self.logHistory(request=request)
            if request != None and len(request.FILES):
                for name, value in request.FILES.items():
                    self.logHistory(kind="media", media=value, request=request)
            if request != None and "DATA" in request and "note" in request.DATA:
                self.logHistory(kind="note", note=request.DATA.get("note"), request=request)

    def logHistory(self, kind="history", note=None, media=None, request=None):
        if request is None:
            request = self.getActiveRequest()

        h = IncidentHistory(
            parent=self,
            to=self.assigned_to,
            note=note,
            kind=kind,
            priority=self.priority,
            state=self.state)
        if request is not None:
            h.by = request.member
        if media is not None:
            h.saveMediaFile(media, "media", media.name)
        h.save()
        self.notifyWatchers(subject=F"Incident:{self.id} Change - {self.description}", history=h)

    def notifyWatchers(self, subject, history=None):
        # this should notify all users in our incident group of the change
        if self.group is not None:
            # all member of the group are notified because it is an incident group
            self.group.notifyMembers(
                subject=subject,
                template="email/incident_change.html",
                context=None,
                email_only=True)

    @classmethod
    def getBundled(cls, rule, event):
        # calculate our bundle start time
        when = datetime.now() - timedelta(minutes=rule.bundle)
        q = objict(rule=rule, created__gte=when)
        if rule.bundle_by == 1:
            q.hostname = event.hostname
        elif rule.bundle_by == 2:
            q.component = event.category
        elif rule.bundle_by == 3:
            q.hostname = event.hostname
            q.component = event.category
        elif rule.bundle_by == 4:
            q.reporter_ip = event.reporter_ip
        elif rule.bundle_by == 5:
            q.reporter_ip = event.reporter_ip
            q.component = event.category
        return Incident.objects.filter(**q).last()

    @classmethod
    def canPublishTo(cls, credentials, msg):
        if credentials:
            return True
        return False


class IncidentMetaData(rm.MetaDataBase):
    parent = models.ForeignKey(Incident, related_name="properties", on_delete=models.CASCADE)


class IncidentHistory(models.Model, rm.RestModel):
    class Meta:
        ordering = ['-created']

    class RestMeta:
        SEARCH_FIELDS = ["to__username", "note"]
        GRAPHS = {
            "default": {
                "extra":[
                    ("get_state_display", "state_display"),
                    ("get_priority_display", "priority_display"),
                ],
                "graphs":{
                    "by":"basic",
                    "to":"basic",
                    "media": "basic"
                }
            },
        }
    parent = models.ForeignKey(Incident, related_name="history", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    group = models.ForeignKey("account.Group", blank=True, null=True, default=None, related_name="+", on_delete=models.CASCADE)

    kind = models.CharField(max_length=80, blank=True, null=True, default=None, db_index=True)

    to = models.ForeignKey("account.Member", blank=True, null=True, default=None, related_name="+", on_delete=models.CASCADE)
    by = models.ForeignKey("account.Member", blank=True, null=True, default=None, related_name="+", on_delete=models.CASCADE)

    state = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)

    note = models.TextField(blank=True, null=True, default=None)
    media = models.ForeignKey("medialib.MediaItem", related_name="+", null=True, default=None, on_delete=models.CASCADE)

