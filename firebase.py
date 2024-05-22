import urequests as requests
class Firebase:
    def __init__(self, url, auth=''):
        self.url = url
        self.auth = auth

    def set(self, path, data):
        full_url = self.url + path + '.json'
        if self.auth:
            full_url += '?auth=' + self.auth
        headers = {'Content-Type': 'application/json'}
        response = requests.put(full_url, json=data, headers=headers)
        return response.json()

    def get(self, path):
        full_url = self.url + path + '.json'
        if self.auth:
            full_url += '?auth=' + self.auth
        headers = {'Content-Type': 'application/json'}
        response = requests.get(full_url, headers=headers)
        return response.json()