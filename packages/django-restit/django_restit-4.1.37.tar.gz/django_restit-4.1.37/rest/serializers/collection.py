from . import model as ms
from django.db.models.query import QuerySet
from rest import settings
# from . import profiler


def serialize(qset, graph, sort=None, size=25, start=0):
    if isinstance(graph, str):
        model = getattr(qset, "model", None)
        if model:
            graph = model.getGraph(graph)
    return to_list_from_graph(qset, graph, sort, size, start)


def to_list_from_graph(qset, graph, sort=None, size=25, start=0):
    fields = graph.get("fields", [])
    extra = graph.get("extra", [])
    exclude = graph.get("exclude", [])
    recurse_into = graph.get("recurse_into", [])
    return to_list(qset, sort, size, fields=fields, extra=extra, exclude=exclude, recurse_into=recurse_into)


def to_list(qset, sort=None, size=25, start=0, fields=[], extra=[], exclude=[], recurse_into=[], cache=None):
    if cache is None:
        cache = dict()
    output = {"size": size, "start": start}
    if sort and isinstance(qset, QuerySet):
        sort_args = get_sort_args(qset, sort)
        try:
            qset = qset.order_by(*sort_args)
            output["sort"] = sort_args
        except Exception:
            pass

    qset = qset[start:start+size+1]
    if not fields:
        fields = ms.get_fields(qset)
    if settings.REST_SELECT_RELATED:
        # this should improve speed greatly for lookups
        foreign_fields = ms.get_select_related_fields(qset.model, fields)
        if foreign_fields:
            qset = qset.select_related(*foreign_fields)
    data = []
    output["data"] = data
    for obj in qset:
        data.append(ms.to_dict(obj, fields, extra, exclude, recurse_into, cache=cache))
    return output


def get_sort_args(qset, sort):
    if not isinstance(sort, str) or "metadata" in sort:
        return None
    if sort.endswith("_display"):
        # fix for django _display kinds being sorted
        sort = sort[:sort.find("_display")]

    sort_args = []
    for s in sort.split(","):
        sort_args.append(s.replace('.', '__'))
    return sort_args

