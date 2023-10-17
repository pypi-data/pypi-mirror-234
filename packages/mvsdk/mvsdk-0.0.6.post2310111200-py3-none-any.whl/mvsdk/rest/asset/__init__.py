class Asset:

    def __init__(self, mv_sdk, base_url: str, domain: str):
        """
        Initialize the Asset Domain
        """
        super(Asset, self)
        self.mv_sdk = mv_sdk
        self.base_url = base_url
        self.domain = domain

    def get(self, params=None, data=None, headers=None, auth=None, object_id=None,
            domain_id=None, domain_action=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'get',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def put(self, params=None, data=None, headers=None, auth=None, profile_id=None,
            domain_id=None, domain_action=None):
        """

        """

    # --------------
    # ASSET KEYWORDS
    # --------------

    def create_keywords(self, params=None, data=None, headers=None, auth=None,
                        object_id=None, object_action='keywords', domain_id=None,
                        domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Accept'] = "application/json"
        headers['Content-Type'] = "application/json"
        headers['Accept-Encoding'] = "gzip, deflate, br"
        headers['Connection'] = "keep-alive"

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
            domain_action=domain_action,
            bulk=bulk
        )

    def delete_keyword(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='keyword', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'delete',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def get_keywords(self, params=None, data=None, headers=None, auth=None,
                     object_id=None, object_action='keywords', domain_id=None,
                     domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

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
            domain_action=domain_action,
            bulk=bulk
        )

    # --------------
    # ASSET ATTRIBUTES
    # --------------

    def create_attribute(self, params=None, data=None, headers=None, auth=None,
                        object_id=None, object_action='keywords', domain_id=None,
                        domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Accept'] = "application/json"
        headers['Content-Type'] = "application/json"
        headers['Accept-Encoding'] = "gzip, deflate, br"
        headers['Connection'] = "keep-alive"

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
            domain_action=domain_action,
            bulk=bulk
        )

    def delete_attribute(self, params=None, data=None, headers=None, auth=None,
                       object_id=None, object_action='keyword', domain_id=None,
                       domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

        return self.mv_sdk.request(
            'delete',
            self.base_url,
            self.domain,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            object_id=object_id,
            object_action=object_action,
            domain_id=domain_id,
            domain_action=domain_action,
            bulk=bulk
        )

    def get_attributes(self, params=None, data=None, headers=None, auth=None,
                     object_id=None, object_action='attributes', domain_id=None,
                     domain_action=None, bulk=None):
        """

        """
        headers = headers or {}
        headers['Content-Type'] = 'application/json'

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
            domain_action=domain_action,
            bulk=bulk
        )
