import cbpro.auth
import cbpro.messenger
import cbpro.public


class Accounts(cbpro.messenger.Subscriber):
    def list(self) -> list:
        return self.messenger.get('/accounts')

    def get(self, account_id: str) -> dict:
        return self.messenger.get(f'/accounts/{account_id}')

    def history(self, account_id: str, params: dict = None) -> list:
        return self.messenger.paginate(f'/accounts/{account_id}/ledger', params=params)

    def holds(self, account_id: str, params: dict = None) -> list:
        return self.messenger.paginate(f'/accounts/{account_id}/holds', params=params)


class Orders(cbpro.messenger.Subscriber):
    def post(self, json: dict) -> dict:
        return self.messenger.post('/orders', json=json)

    def cancel(self, id_: str, params: dict = None) -> list:
        return self.messenger.delete(f'/orders/{id_}', params=params)

    def cancel_client(self, oid: str, params: dict = None) -> list:
        return self.messenger.delete(f'/orders/client:{oid}', params=params)

    def cancel_all(self, params: dict = None) -> list:
        return self.messenger.delete('/orders', params=params)

    def list(self, params: dict) -> list:
        return self.messenger.paginate('/orders', params=params)

    def get(self, id_: str) -> dict:
        return self.messenger.get(f'/orders/{id_}')

    def get_client(self, oid: str) -> dict:
        return self.messenger.get(f'/orders/client:{oid}')


class Fills(cbpro.messenger.Subscriber):
    def list(self, params: dict) -> list:
        return self.messenger.paginate('/fills', params=params)


class Limits(cbpro.messenger.Subscriber):
    def get(self) -> dict:
        return self.messenger.get('/users/self/exchange-limits')


class Deposits(cbpro.messenger.Subscriber):
    def list(self, params: dict = None) -> list:
        return self.messenger.paginate('/transfers', params=params)

    def get(self, transfer_id: str) -> dict:
        return self.messenger.get(f'/transfers/:{transfer_id}')

    def payment(self, json: dict) -> dict:
        return self.messenger.post('/deposits/payment-method', json=json)

    def coinbase(self, json: dict) -> dict:
        return self.messenger.post('/deposits/coinbase-account', json=json)

    def generate(self, account_id: str) -> dict:
        return self.messenger.post(
            f'/coinbase-accounts/{account_id}/addresses'
        )


class Withdrawals(Deposits):
    def payment(self, json: dict) -> dict:
        return self.messenger.post('/withdrawals/payment-method', json=json)

    def coinbase(self, json: dict) -> dict:
        return self.messenger.post('/withdrawals/coinbase-account', json=json)

    def crypto(self, json: dict) -> dict:
        return self.messenger.post('/withdrawals/crypto', json=json)

    def estimate(self, params: dict) -> dict:
        return self.messenger.get('/withdrawals/fee-estimate', params=params)


class Conversions(cbpro.messenger.Subscriber):
    def create(self, json: dict) -> dict:
        return self.messenger.post('/conversions', json=json)


class Payments(cbpro.messenger.Subscriber):
    def list(self) -> list:
        return self.messenger.get('/payment-methods')


class Coinbase(cbpro.messenger.Subscriber):
    def list(self) -> list:
        return self.messenger.get('/coinbase-accounts')


class Fees(cbpro.messenger.Subscriber):
    def get(self) -> list:
        return self.messenger.get('/fees')


class Reports(cbpro.messenger.Subscriber):
    pass


class Profiles(cbpro.messenger.Subscriber):
    def list(self, params: dict = None) -> list:
        return self.messenger.get('/profiles', params=params)

    def get(self, profile_id: str) -> dict:
        return self.messenger.get(f'/profiles/{profile_id}')

    def transfer(self, json: dict) -> dict:
        return self.messenger.post('/profiles/transfer', json=json)


class Oracle(cbpro.messenger.Subscriber):
    pass


class PrivateClient(cbpro.public.PublicClient):
    def __init__(self, messenger: cbpro.messenger.Messenger) -> None:
        super(PrivateClient, self).__init__(messenger)

        self.accounts = Accounts(messenger)
        self.orders = Orders(messenger)
        self.fills = Fills(messenger)
        self.limits = Limits(messenger)
        self.deposits = Deposits(messenger)
        self.withdrawals = Withdrawals(messenger)
        self.conversions = Conversions(messenger)
        self.payments = Payments(messenger)
        self.coinbase = Coinbase(messenger)
        self.fees = Fees(messenger)
        self.reports = Reports(messenger)
        self.profiles = Profiles(messenger)
        self.oracle = Oracle(messenger)


def private_client(key: str,
                   secret: str,
                   passphrase: str,
                   url: str = None) -> PrivateClient:

    auth = cbpro.auth.Auth(key, secret, passphrase)
    messenger = cbpro.messenger.Messenger(auth=auth, url=url)
    return PrivateClient(messenger)
