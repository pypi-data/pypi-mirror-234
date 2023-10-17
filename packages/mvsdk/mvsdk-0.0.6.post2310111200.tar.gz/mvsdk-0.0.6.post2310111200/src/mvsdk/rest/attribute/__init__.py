class Attribute:

    def __init__(self, mv_sdk, base_url: str, domain: str, **kwargs: dict):
        """
        Initialize the Attribute Domain
        """
        super()
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def create(self, params=None, data=None, headers=None, auth=None, object_id=None,
               object_action=None, domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#38562514-52f6-457e-9b7a-25486661112c
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return self.mv_sdk.request(
            'post',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def get(self, params=None, data=None, headers=None, auth=None, object_id=None,
            object_action=None, domain_id=None, domain_action=None):
        """
        https://docs.mediavalet.com/#1e6608b7-5d9a-4904-8ffc-731fc6c4e9c3
        """
        headers = headers or {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action
        )
