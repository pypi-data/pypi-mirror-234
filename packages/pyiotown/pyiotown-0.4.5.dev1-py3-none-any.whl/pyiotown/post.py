import sys
import requests
import json
import ssl

def uploadImage(url, token, payload, group_id=None, verify=True, timeout=60):
    '''
    url : IoT.own Server Address
    token : IoT.own API Token
    payload : Image + Annotation Json Data (check format in README.md)
    '''
    apiaddr = url + "/api/v1.0/nn/image"
    header = {'Content-Type': 'application/json', 'Token': token}
    if group_id is not None:
        header['grpid'] = group_id
    try:
        r = requests.post(apiaddr, data=payload, headers=header, verify=verify, timeout=timeout)
        if r.status_code == 200:
            return True
        else:
            print(r.content)
            return False
    except Exception as e:
        print(e)
        return False

def data(url, token, nid, data, upload="", group_id=None, verify=True, timeout=60):
    '''
    url : IoT.own Server Address
    token : IoT.own API Token
    type: Message Type
    nid: Node ID
    data: data to send (JSON object)
    '''
    typenum = "2" # 2 static 
    apiaddr = url + "/api/v1.0/data"
    if upload == "":
        header = {'Accept':'application/json', 'token':token }
        if group_id is not None:
            header['grpid'] = group_id
        payload = { "type" : typenum, "nid" : nid, "data": data }
        try:
            r = requests.post(apiaddr, json=payload, headers=header, verify=verify, timeout=timeout)
            if r.status_code == 200:
                return True
            else:
                print(r.content)
                return False
        except Exception as e:
            print(e)
            return False
    else:
        header = {'Accept':'application/json', 'token':token }
        if group_id is not None:
            header['grpid'] = group_id
        payload = { "type" : typenum, "nid" : nid, "meta": json.dumps(data) }
        try:
            r = requests.post(apiaddr, data=payload, headers=header, verify=verify, timeout=timeout, files=upload)
            if r.status_code == 200:
                return True
            else:
                print(r.content)
                return False
        except Exception as e:
            print(e)
            return False

def command(url, token, nid, command, lorawan=None, group_id=None, verify=True, timeout=60):
    uri = url + "/api/v1.0/command"
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'token': token
    }

    if group_id is not None:
        header['grpid'] = group_id

    payload = {
        'nid': nid,
    }

    if type(command) is str:
        payload['type'] = 'string'
        payload['command'] = command
    elif type(command) is bytes:
        payload['type'] = 'hex'
        payload['command'] = command.hex()
    else:
        raise Exception("The type of 'command' must be either str or bytes.")

    if lorawan is not None:
        payload['lorawan'] = lorawan
    
    try:
        r = requests.post(uri, json=payload, headers=header, verify=verify, timeout=timeout)
        if r.status_code == 200:
            return True
        else:
            print(r.content)
            return False
    except Exception as e:
        print(e)
        return False

def post_files(result, url, token, group_id=None, verify=True, timeout=60):
    if 'data' not in result.keys():
        return result
    
    for key in result['data'].keys():
        if type(result['data'][key]) is dict:
            resultkey = result['data'][key].keys()
            if ('raw' in resultkey) and ( 'file_type' in resultkey) :
                header = {'Accept':'application/json', 'token':token }
                if group_id is not None:
                    header['grpid'] = group_id
                upload = { key: result['data'][key]['raw'] }
                try:
                    r = requests.post( url + "/api/v1.0/file", headers=header, verify=verify, timeout=timeout, files=upload )
                    if r.status_code == 200:
                        del result['data'][key]['raw']
                        result['data'][key]['file_id'] = r.json()["files"][0]["file_id"]
                        result['data'][key]['file_size'] = r.json()["files"][0]["file_size"]
                    else:
                        print("[ Error ] while send Files to IoT.own. check file format [raw, file_type]")
                        print(r.content)
                except Exception as e:
                    print(e)
            # post post process apply.
    return result

def postprocess(url, name, func, username, pw, port=8883, verify=True):
    raise Exception('post.postprocess is deprecated. Instead of it, use post_process.connect()', file=sys.stderr)

def postprocess_common(url, topic, func, username, pw, port=8883):
    raise Exception('post.postprocess_common is deprecated. Instead of it, use post_process.connect_common()', file=sys.stderr)

def postprocess_loop_forever(clients):
    raise Exception('post.postprocess_loop_forever is deprecated. Instead of it, use post_process.loop_forever()', file=sys.stderr)
