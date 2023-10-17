import base64


class Connect:

    def __init__(self, mv_sdk, base_url: str, domain: str):
        """
        Initialize the Asset Domain
        """
        super(Connect, self)
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def auth(self, params=None, data=None, headers=None, auth=None,
             object_id=None, domain_id=None):
        """
        """
        headers = headers or {}

        if auth:
            auth_string = base64.b64encode(
                bytes(f'{auth["client_id"]}:{auth["client_secret"]}', 'utf-8"')
                ).decode("utf-8")
            headers['Authorization'] = f'Basic {auth_string}'

        headers = headers or {}

        headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers['Accept'] = '*/*'

        return self.mv_sdk.request(
            'post',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            object_id=object_id,
            domain_id=domain_id,
            domain_action='token'
        )
