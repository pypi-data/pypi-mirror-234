from rest.decorators import periodic
from datetime import datetime, timedelta
from .models import Member
from sessionlog.models import SessionLog


@periodic(minute=15)
def run_cleanup_tokens(force=False, verbose=False, now=None):
    # we want to nuke invite tokens every 15 minutes
    # we do not want to do this if using invite
    stale = datetime.now() - timedelta(hours=24)
    qset = Member.objects.filter(auth_token__isnull=False).filter(modified__lte=stale)
    qset.update(auth_token=None)

    # lets prune old non active sessions
    SessionLog.Clean(limit=10000)

