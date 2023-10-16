from datetime import datetime
from rest import decorators as rd
from rest import views as rv
from rest import settings
from rest import helpers as rh
from rest import net
from rest import ssl_check
from location.models import GeoIP
from . import client as metrics
from . import models as mm
from . import models as em
from .providers import aws
from objict import objict
import time

"""
Capture simple analytics counters.
"""
LOCATION_METRICS = settings.LOCATION_METRICS


@rd.urlPOST('metric')
def rest_on_new_metric(request):
    # slug, num=1, category=None, expire=None, date=None
    data = request.DATA.toObject()
    if data.slug is None:
        return rv.restStatus(request, False)
    if data.value is None:
        data.value = 1
    metrics.metric(data.slug, data.value, category=data.category, expire=data.expire)
    if request.DATA.get("geolocate", False, field_type=bool):
        if request.location is None:
            request.location = GeoIP.get(request.ip)
        if request.location and request.location.country:
            country = request.location.country.lower().replace(" ", "_")
            state = request.location.state.lower().replace(" ", "_")
            metrics.metric(f"geo_country__{country}__{data.slug}", category="geo_country")
            metrics.metric(f"geo_state__{state}__{data.slug}", category="geo_state")
            
    return rv.restStatus(request, True)


@rd.urlGET('metric')
@rd.login_required
def rest_on_get_metric(request):
    # slug, num=1, category=None, expire=None, date=None
    data = request.DATA.toObject()
    if data.slug is None:
        return rv.restStatus(request, False)
    result = metrics.get_metric(data.slug)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.urlGET('metrics')
@rd.login_required
def rest_on_get_metrics(request, pk=None):
    # slug, since, granularity
    since = request.DATA.get("since", field_type=datetime)
    granularity = request.DATA.get(["granularity", "period"], default="daily")
    category = request.DATA.get("category")
    if category:
        result = metrics.get_category_metrics(category, since, granularity)
        return rv.restReturn(request, dict(data=result))
    slugs = request.DATA.getlist(["slugs", "slug"])
    if slugs is None:
        return rv.restStatus(request, False)

    result = metrics.get_metrics(slugs, since, granularity)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.urlGET('slugs')
@rd.login_required
def rest_on_get_metrics_slugs(request, pk=None):
    category = request.DATA.get("category", None)
    slugs = metrics.get_slugs(category)
    prefix = request.DATA.get("prefix")
    if prefix:
        slugs = [s for s in slugs if s.startswith(prefix)]
    return rv.restReturn(request, dict(data=slugs))


@rd.urlPOST('guage')
def rest_on_guage(request, pk=None):
    data = request.DATA.toObject()
    if data.slug is None or data.value is None:
        return rv.restStatus(request, False)
    metrics.guage(data.slug, data.value)
    return rv.restStatus(request, True)


@rd.urlGET('guage')
@rd.login_required
def rest_on_get_guage(request):
    # slug, num=1, category=None, expire=None, date=None
    data = request.DATA.toObject()
    if data.slug is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, metrics.get_guage(data.slug))


@rd.urlGET('guages')
@rd.login_required
def rest_on_get_guages(request, pk=None):
    # slug, num=1, category=None, expire=None, date=None
    data = request.DATA.toObject()
    if data.slugs is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, metrics.get_guages(data.slugs))


@rd.url('db/metrics/objects')
@rd.url('db/metrics/objects/<int:pk>')
@rd.login_required
def rest_on_db_metrics_objects(request, pk=None):
    return mm.Metrics.on_rest_request(request, pk)


@rd.urlGET('db/metrics')
@rd.login_required
def rest_on_get_model_metrics(request, pk=None):
    # slug, since, granularity
    since = request.DATA.get("since", field_type=datetime)
    granularity = request.DATA.get(["granularity", "period"], default="daily")
    category = request.DATA.get("category")
    if category:
        result = mm.get_category_metrics(category, since, granularity, group=request.group)
        return rv.restReturn(request, dict(data=result))
    slugs = request.DATA.get(["slug", "slugs"])
    if slugs is None:
        return rv.restStatus(request, False)

    status, reason, code = rh.requestHasPerms(request, ["view_metrics", "reporting", "admin", "manage_groups"], group=request.group)
    if not status:
        return rv.restPermissionDenied(request, reason, code)

    result = mm.get_metrics(slugs, granularity, since, group=request.group)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.urlGET('db/metric')
@rd.login_required
def rest_on_get_model_metric(request, pk=None):
    # slug, since, granularity
    since = request.DATA.get("since", field_type=datetime)
    granularity = request.DATA.get(["granularity", "period"], default="daily")
    slugs = request.DATA.get(["slug", "slugs"])
    if slugs is None:
        return rv.restStatus(request, False)

    status, reason, code = rh.requestHasPerms(request, ["view_metrics", "reporting", "admin", "manage_groups"], group=request.group)
    if not status:
        return rv.restPermissionDenied(request, reason, code)

    result = mm.get_metric(slugs, granularity, since, group=request.group)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.urlGET('db/slugs')
@rd.login_required
def rest_on_get_model_metrics_slugs(request, pk=None):
    return rv.restGet(request, dict(data=list(mm.Metrics.objects.all().distinct().values_list("slug", flat=True))))


# BEGIN EOD METRICS
@rd.urlGET('db/eod/metric')
@rd.login_required
def rest_on_get_model_eod_metrics(request, pk=None):
    # slug, since, granularity
    dr_end = request.DATA.get("dr_end", field_type=datetime)
    slug = request.DATA.get("slug")
    status, reason, code = rh.requestHasPerms(request, ["view_metrics", "reporting", "admin", "manage_groups"], group=request.group)
    if not status:
        return rv.restPermissionDenied(request, reason, code)

    result = em.get_metric(slug, dr_end, group=request.group)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.urlGET('db/eod/metrics')
@rd.login_required
def rest_on_get_model_eod_metrics(request, pk=None):
    # slug, since, granularity
    dr_end = request.DATA.get("dr_end", field_type=datetime)
    slug = request.DATA.get("slug")
    count = request.DATA.get("count", 7)
    status, reason, code = rh.requestHasPerms(request, ["view_metrics", "reporting", "admin", "manage_groups"], group=request.group)
    if not status:
        return rv.restPermissionDenied(request, reason, code)

    result = em.get_metrics(slug, count, dr_end, group=request.group)
    if result is None:
        return rv.restStatus(request, False)
    return rv.restReturn(request, dict(data=result))


@rd.url('db/eod/metrics/objects')
@rd.url('db/eod/metrics/objects/<int:pk>')
@rd.login_required
def rest_on_db_eod_metrics_objects(request, pk=None):
    return em.EODMetrics.on_rest_request(request, pk)


@rd.urlGET('db/eod/slugs')
@rd.login_required
def rest_on_get_model_eod_metrics_slugs(request, pk=None):
    return rv.restGet(request, dict(data=list(em.EODMetrics.objects.all().distinct().values_list("slug", flat=True))))


# BEGIN CLOUDWATCH

def getPeriods(period, duration):
    count = int(duration/period)
    periods = []
    utc_time = int(time.strftime('%s', time.gmtime()))
    for i in range(0, count-1):
        periods.append(utc_time - (i * period))
    periods.reverse()
    return periods


@rd.urlGET('restit/domains')
@rd.login_required
def rest_on_ec2_domains(request, pk=None):
    if not settings.DOMAIN_WATCH:
        return rv.restPermissionDenied(request)

    output = []
    result = ssl_check.check(*settings.DOMAIN_WATCH)
    for key, value in result.items():
        output.append(dict(domain=key, expires=value, id=key))
    return rv.restList(request, output)


@rd.urlGET('restit/servers')
@rd.login_required
def rest_on_ec2_restit_stats(request, pk=None):
    hostname = settings.SERVER_ROOT
    if hostname is None:
        hostname = settings.SERVER_NAME
    if hostname.count(".") == 2:
        hostname = hostname[hostname.find(".")]
    instances = aws.getAllEC2()
    hosts = [inst.name for inst in instances]
    data = []
    for name in hosts:
        if settings.SERVER_NAME_MAP and name in settings.SERVER_NAME_MAP:
            host = settings.SERVER_NAME_MAP[name]
            if "." not in host:
                host = f"{name}.{hostname}"
        else:
            host = f"{name}.{hostname}"
        resp = net.REQUEST("GET", host, "/rpc/versions", params=dict(detailed=1))
        if resp.status:
            resp.data.id = host
            resp.data.hostname = host
            data.append(resp.data)
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/ec2/list/details')
@rd.login_required
def rest_on_ec2_list(request, pk=None):
    return rv.restReturn(request, dict(data=aws.getAllEC2()))


@rd.urlGET('aws/ec2/list/ids')
@rd.login_required
def rest_on_ec2_list_ids(request, pk=None):
    return rv.restReturn(request, dict(data=aws.getAllEC2(True)))


@rd.urlGET('aws/ec2/cpu')
@rd.requires_params(["ids"])
def rest_on_ec2_metrics_cpu(request, pk=None):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    get_rds = False
    instances = aws.getAllEC2()
    if "all" in ids:
        get_rds = True
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric="cpu",
        namespace="ec2",
        stat="max")
    # convert ids to names
    output = dict()
    for i in instances:
        if i.id in data:
            output[i.name] = data[i.id]
            output[i.name].reverse()
    # if get_rds:
    #     ids = aws.getAllRDS(True)
    #     rds_cpu = (aws.getMetrics(
    #         ids,
    #         period=period,
    #         duration_seconds=duration,
    #         metric="cpu",
    #         namespace="rds",
    #         stat="max"))
    #     for k, v in rds_cpu.items():
    #         v.reverse()
    #     output.update(rds_cpu)

    data = dict(data=output, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/ec2/network/in')
@rd.requires_params(["ids"])
def rest_on_ec2_metrics_netin(request, pk=None):
    data = aws.getMetrics(
        request.DATA.getlist("ids"),
        period=request.DATA.get("period", 300, field_type=int),
        duration_seconds=request.DATA.get("duration", 900, field_type=int),
        metric="NetworkIn",
        namespace="ec2",
        stat="max")
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/ec2/network/out')
@rd.requires_params(["ids"])
def rest_on_ec2_metrics_netout(request, pk=None):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    get_rds = False
    instances = aws.getAllEC2()
    if "all" in ids:
        get_rds = True
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric="NetworkOut",
        namespace="ec2",
        stat="max")
    # convert ids to names
    output = dict()
    for i in instances:
        if i.id in data:
            output[i.name] = data[i.id]
            output[i.name].reverse()
    data = dict(data=output, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/rds/cpu')
@rd.requires_params(["ids"])
def rest_on_ec2_metrics_cpu(request, pk=None):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    instances = aws.getAllRDS()
    if "all" in ids:
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric="cpu",
        namespace="rds",
        stat="max")
    data = dict(data=data, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/rds/memory')
@rd.requires_params(["ids"])
def rest_on_rds_metrics_memory(request, pk=None):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    instances = aws.getAllRDS()
    if "all" in ids:
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric="memory",
        namespace="rds",
        stat="max")
    data = dict(data=data, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/rds/cons')
@rd.requires_params(["ids"])
def rest_on_rds_metrics_cons(request, pk=None):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    instances = aws.getAllRDS()
    if "all" in ids:
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric="cons",
        namespace="rds",
        stat="max")
    data = dict(data=data, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


@rd.urlGET('aws/redis/cpu')
@rd.requires_params(["ids"])
def rest_on_redis_metrics_cpu(request, pk=None):
    return get_redis_metrics(request, "cpu")


@rd.urlGET('aws/redis/cons')
@rd.requires_params(["ids"])
def rest_on_redis_metrics_cons(request, pk=None):
    return get_redis_metrics(request, "cache_cons")


@rd.urlGET('aws/redis/memory')
@rd.requires_params(["ids"])
def rest_on_redis_metrics_mem(request, pk=None):
    return get_redis_metrics(request, "cache_usage")


def get_redis_metrics(request, metric):
    ids = request.DATA.getlist("ids")
    period = request.DATA.get("period", 300, field_type=int)
    duration = request.DATA.get("duration", period*8, field_type=int)
    instances = aws.getAllRedis()
    if "all" in ids:
        ids = [inst.id for inst in instances]
    data = aws.getMetrics(
        ids,
        period=period,
        duration_seconds=duration,
        metric=metric,
        namespace="redis",
        stat="max")
    data = dict(data=data, periods=getPeriods(period, duration))
    return rv.restReturn(request, dict(data=data))


# @rd.urlGET('aws/ec2/metrics/list')
# @rd.login_required
# def rest_on_ec2_list_ids(request, pk=None):
#     ['DiskWriteOps', 'CPUCreditUsage', 'DiskReadOps', 
#     'NetworkOut', 'CPUSurplusCreditBalance', 
#     'CPUUtilization', 'CPUCreditBalance', 
#     'NetworkPacketsOut', 'StatusCheckFailed', 
#     'NetworkIn', 'StatusCheckFailed_System', 
#     'StatusCheckFailed_Instance', 'DiskWriteBytes', 
#     'NetworkPacketsIn', 'CPUSurplusCreditsCharged', 
#     'DiskReadBytes', 'MetadataNoToken']
#     return rv.restReturn(request, data=aws.getMetricsList(request.DATA.get("id", None)))


@rd.urlGET('aws/rds/list/details')
@rd.login_required
def rest_on_rds_list(request, pk=None):
    return rv.restReturn(request, dict(data=aws.getAllRDS()))


@rd.urlGET('aws/rds/list/ids')
@rd.login_required
def rest_on_rds_list_ids(request, pk=None):
    return rv.restReturn(request, dict(data=aws.getAllRDS(True)))


