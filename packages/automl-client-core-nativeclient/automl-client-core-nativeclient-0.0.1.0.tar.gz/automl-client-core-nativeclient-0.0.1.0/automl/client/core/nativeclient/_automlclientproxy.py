# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class AutoMLClientProxy(object):
    """
    Proxy class that proxies property access and method calls to the
    underlying client object.
    """
    def __init__(self,
                 client=None,
                 **kwargs):
        """
        Construct an instance of this proxy.

        :param client: the AutoML client object to proxy
        :param kwargs: arguments to pass to the client for initialization
        """

        if client is None:
            raise ValueError('A client object is required.')

        self._client = client
        self._client.initialize_client(**kwargs)
        self._client.start_experiment()

    def __getattr__(self, attr):
        """
        Use the underlying client object to retrieve attributes.

        :param attr: attribute name
        :type attr: str
        :return:
        """
        if not hasattr(self._client, attr):
            raise AttributeError("Attribute not found.")

        return getattr(self._client, attr)
