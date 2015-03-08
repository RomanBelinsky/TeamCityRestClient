
import json
import urllib3
import base64
import sys

class TCClient:
    def __init__(self, username, password, server, port):
        self.TC_REST_URL = "http://%s:%d/httpAuth/app/rest/" % (server, port)
        self.user_pass = '%s:%s' % (username, password)

    def list_queued_builds(self):
        url = self.TC_REST_URL + 'buildQueue'
        print(url)
        pool_manager = urllib3.PoolManager()

        base64string = base64.b64encode(self.user_pass.encode())
        response = pool_manager.request('GET', url,
                                        headers={'Authorization': "Basic %s" % base64string.decode("utf-8"),
                                                 'Accept': 'application/json'})
        json_data = json.loads(response.data.decode())
        response.close()
        return json_data

    def get_build_ids_by_build_type(self, build_type, builds_data):
        if not 'build' in in builds_data:
            return []
        result = list(map(lambda build: build['id'],
                          filter(lambda build: build['buildTypeId'] == build_type, builds_data['build'])))
        return result

    def cancel_queued_build(self, build_id):
        cancel_token = "<buildCancelRequest comment='cancelled automatically: one of dependent builds is failing' readdIntoQueue='false' />"
        url = self.TC_REST_URL + 'buildQueue/' + str(build_id)
        print('cancel build:' + url)
        pool_manager = urllib3.PoolManager()

        base64string = base64.b64encode(self.user_pass.encode())
        res = pool_manager.urlopen('POST', url,
                                   headers={'Authorization': "Basic %s" % base64string.decode("utf-8"),
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/xml'},
                                   body=cancel_token)

        return res.data.decode()

    def cancel_running_build(self, build_id):
        cancel_token = "<buildCancelRequest comment='cancelled automatically: one of dependent builds is failing' readdIntoQueue='false' />"
        url = self.TC_REST_URL + 'builds/' + str(build_id)
        print('cancel build:' + url)
        pool_manager = urllib3.PoolManager()

        base64string = base64.b64encode(self.user_pass.encode())
        res = pool_manager.urlopen('POST', url,
                                   headers={'Authorization': "Basic %s" % base64string.decode("utf-8"),
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/xml'},
                                   body=cancel_token)
        resdata = res.data.decode()
        print(resdata)
        return resdata


    def get_build_fail_status_by_type(self, type_id):
        url = self.TC_REST_URL + 'buildTypes/id:' + type_id + '/builds?count=1'
        print(url)
        pool_manager = urllib3.PoolManager()

        base64string = base64.b64encode(self.user_pass.encode())
        response = pool_manager.request('GET', url,
                                        headers={'Authorization': "Basic %s" % base64string.decode("utf-8"),
                                                 'Accept': 'application/json'})
        json_data = json.loads(response.data.decode())
        response.close()
        failure_ = lambda build: build['buildTypeId'] == type_id and build['status'] == "FAILURE"
        results = list(filter(failure_, json_data['build']))
        return len(results) > 0

    def get_running_builds_by_type(self, type_id):
        url = self.TC_REST_URL + 'buildTypes/id:' + type_id + '/builds/running:true'
        print(url)
        pool_manager = urllib3.PoolManager()

        base64string = base64.b64encode(self.user_pass.encode())
        response = pool_manager.request('GET', url,
                                        headers={'Authorization': "Basic %s" % base64string.decode("utf-8"),
                                                 'Accept': 'application/json'})
        if response.status == 404:
            return -1
        json_data = json.loads(response.data.decode())
        response.close()
        results = json_data['id']
        return results


def cancel_build_list(name, client, builds):
    ids = client.get_build_ids_by_build_type(name, builds)
    for build_id in ids:
        client.cancel_queued_build(build_id)



