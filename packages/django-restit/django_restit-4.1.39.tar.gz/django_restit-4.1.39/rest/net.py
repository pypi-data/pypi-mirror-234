import requests
from objict import objict


def getURL(host, path):
    if host.endswith("/"):
        host = host[:-1]
    if path.startswith("/"):
        path = path[1:]
    if host.startswith("http"):
        return "{host}/{path}"
    return f"https://{host}/{path}" 


def REQUEST(method, host, path, data=None, params=None, headers=None, files=None, session=None, post_json=False):
    url = getURL(host, path)
    if headers is None:
        headers = objict()

    fields = dict(url=url, params=params, files=files)
    if isinstance(data, dict):
        fields["data"] = objict.fromdict(data).toJSON()
    elif data is not None:
        fields["data"] = data

    # headers["Accept"] = 'application/json'
    if post_json:
        headers['Content-type'] = 'application/json'
    fields["headers"] = headers
    if session is None:
        session = requests
    try:
        res = getattr(session, method.lower())(**fields)
    except Exception as err:
        return objict(status=False, status_code=500, error=str(err))
    return processResponse(res, url)


def processResponse(res, url):
    data = res.text
    try:
        data = objict.fromdict(res.json())
    except Exception as err:
        return objict(status=False, status_code=res.status_code, data=res.text, error=str(err))

    if res.status_code not in [200, 201]:
        if isinstance(data, dict) and data.error:
            data.status = False
            data.status_code = res.status_code
            return data
        return objict(status=False, status_code=res.status_code, error=res.text)
    if data.data:
        data = data.data
    return objict(status=True, status_code=res.status_code, data=data)
