class MySettings:
    def __init__(self, client_id=None, client_secret=None, account_id=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._account_id = account_id

    def set_client_id(self, client_id):
        self._client_id = client_id

    def set_client_secret(self, client_secret):
        self._client_secret = client_secret

    def set_account_id(self, account_id):
        self._account_id = account_id

def configure(client_id, client_secret, account_id):
    settings = MySettings(client_id, client_secret, account_id)
    return settings
