import requests

def data(url, token, _id=None, nid=None, date_from=None, date_to=None, group_id=None, verify=True, timeout=60):
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'token': token
    }

    # only for administrators
    if group_id is not None:
        header['grpid'] = group_id

    uri = url + "/api/v1.0/data"

    params = {}
    
    if nid is not None:
        params['nid'] = nid
    elif _id is not None:
        params['_id'] = _id
        
    if date_from is not None:
        params['from'] = date_from

    if date_to is not None:
        params['to'] = date_to

    result = None
    
    try:
        r = requests.delete(uri, json=params, headers=header, verify=verify, timeout=timeout)
    except Exception as e:
        print(e)
        return None
    
    if r.status_code == 200:
        return r.json()
    else:
        return None
