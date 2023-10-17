import requests
import json
from urllib.parse import urlencode
import logging


def create_params(**kwargs):
    '''
    Used to create url parameters for API call
    '''
    path = kwargs.get("path")
    params = kwargs.get("params")
    if params:
        query_string = urlencode(params)
    return f'{path}?{query_string}'


def mocked_requests_get(url, headers, data):
    class MockResponse:
        def __init__(self, url, headers, status_code):
            self.verb = "GET"
            self.url = url
            self.headers = headers
            self.data = data
            self.status_code = status_code

        def json(self):
            return {
                "verb": self.verb,
                "url": self.url,
                "headers": self.headers,
                "data": self.data
            }

    return MockResponse(url, headers, 200)


class APIRequester:
    '''
    Used to make the request
    '''
    def __init__(self, **kwargs):

        self.method = kwargs.get("method")
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers")
        self.data = kwargs.get("data")
        self.verify_ssl = kwargs.get("verify_ssl") or True

    def get(self):
        logging.debug('Request:\nVerb: GET\nURL: %s\nHeaders: %s\nData: %s',
                      self.url, json.dumps(self.headers), self.data)
        response = requests.get(
                self.url,
                headers=self.headers,
                data=self.data,
                verify=bool(self.verify_ssl)
            )
        return response

    def post(self):
        logging.debug('Request:\nVerb:POST\nURL: %s\nHeaders: %s\nData: %s',
                      self.url, json.dumps(self.headers), self.data)
        response = requests.post(
                self.url,
                headers=self.headers,
                data=self.data,
                verify=bool(self.verify_ssl)
            )
        return response

    def delete(self):
        logging.debug('Request:\nVerb: DELETE\nURL: %s\nHeaders: %s\nData: %s',
                      self.url, json.dumps(self.headers), self.data)
        response = requests.delete(
                self.url,
                headers=self.headers,
                data=self.data,
                verify=bool(self.verify_ssl)
            )
        return response


class PathBuilder:
    '''
    Used to build the correct API path that includes
    parameters & filters
    '''
    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url')
        self.domain = kwargs.get('domain')
        self.version = kwargs.get('version')
        self.object_id = kwargs.get('object_id')
        self.object_action = kwargs.get('object_action')
        self.domain_id = kwargs.get('domain_id')
        self.domain_action = kwargs.get('domain_action')
        self.params = kwargs.get('params')

    def build(self):
        paths = {
            "domains": {
                "asset": {
                    "path": 'assets'
                },
                "attribute": {
                    "path": 'attributes'
                },
                "branded_portal": {
                    "path": 'brandedportals'
                },
                "bulk": {
                    "path": 'bulk'
                },
                "category": {
                    "path": 'categories'
                },
                "config": {
                    "path": 'config'
                },
                "connect": {
                    "path": 'connect'
                },
                "crop": {
                    "path": 'crop'
                },
                "direct_link": {
                    "path": 'directlinks'
                },
                "download": {
                    "path": 'downloads'
                },
                "home": {
                    "path": ''
                },
                "introduction_and_help": {
                    "path": 'introductionAndHelp'
                },
                "keyword_group": {
                    "path": 'keywordGroups'
                },
                "keyword": {
                    "path": 'keywords'
                },
                "notification": {
                    "path": 'notification'
                },
                "org_unit": {
                    "path": 'organizationalUnits'
                },
                "reports": {
                    "path": 'reports'
                },
                "saved_search": {
                    "path": 'savedsearches'
                },
                "search": {
                    "path": 'search'
                },
                "share": {
                    "path": 'share'
                },
                "public": {
                    "path": 'public'
                },
                "upload": {
                    "path": 'uploads'
                },
                "user_group": {
                    "path": 'groups'
                },
                "user": {
                    "path": 'users'
                }
            }
        }
        domain_info = paths['domains'][self.domain]
        sections = [domain_info['path']]

        if self.domain_action:
            sections.append(self.domain_action)
        if self.object_id:
            sections.append(self.object_id)
        if self.object_action:
            sections.append(self.object_action)

        uri = f'/{"/".join(sections)}'

        # manage params and filtering
        params = {}
        for param in self.params.keys():
            params[param] = self.params[param]
        if params:
            uri = create_params(params=json.dumps(params), path=uri)

        url = f'https://{self.base_url}{uri}'

        return [uri, url]
