import cbpro.utils
import cbpro.check


#################
# Public Models #
#################
class ProductsModel(object):
    def order_book(self, level: int = None) -> dict:
        if level is None:
            return None

        cbpro.check.products_order_book(level)

        return {'level': level}

    def history(self,
                start: str = None,
                end: str = None,
                granularity: int = None) -> dict:

        if start or end:
            cbpro.check.products_history_range(start, end)

        if granularity is None:
            granularity = 86400  # default to 1 day

        cbpro.check.products_history_granularity(granularity)

        params = {
            'start': start,
            'end': end,
            'granularity': granularity
        }

        return cbpro.utils.filter_empty(params)


class PublicModel(object):
    def __init__(self):
        self.products = ProductsModel()


##################
# Private Models #
##################
class OrdersModel(object):
    def base(self,
             side: str,
             product_id: str,
             type_: str = None,
             client_oid: str = None,
             stp: str = None,
             stop: str = None,
             stop_price: float = None) -> dict:

        cbpro.check.orders_base_side(side)

        if type_:
            cbpro.check.orders_base_type(type_)

        if stp:
            cbpro.check.orders_base_stp(stp)

        if stop or stop_price:
            cbpro.check.orders_base_stop(stop)
            cbpro.check.orders_base_stop_price(stop, stop_price)

        params = {
            'side': side,
            'product_id': product_id,
            'type': type_,
            'client_oid': client_oid,
            'stp': stp,
            'stop': stop,
            'stop_price': stop_price
        }

        return cbpro.utils.filter_empty(params)

    def limit(self,
              side: str,
              product_id: str,
              price: float,
              size: float,
              time_in_force: str = None,
              cancel_after: str = None,
              post_only: bool = None,
              client_oid: str = None,
              stp: str = None,
              stop: str = None,
              stop_price: float = None) -> dict:

        params = self.base(
            side, product_id, 'limit', client_oid, stp, stop, stop_price
        )

        if time_in_force:
            cbpro.check.orders_limit_time_in_force(time_in_force)

        if cancel_after:
            cbpro.check.orders_limit_cancel_after(time_in_force)

        if post_only:
            cbpro.check.orders_limit_post_only(time_in_force)

        params.update({
            'price': price,
            'size': size,
            'time_in_force': time_in_force,
            'cancel_after': cancel_after,
            'post_only': post_only,
        })

        return cbpro.utils.filter_empty(params)

    def market(self,
               side: str,
               product_id: str,
               size: float = None,
               funds: float = None,
               client_oid: str = None,
               stp: str = None,
               stop: str = None,
               stop_price: float = None) -> dict:

        params = self.base(
            side, product_id, 'market', client_oid, stp, stop, stop_price
        )

        cbpro.check.orders_market_size_or_funds(size, funds)

        params.update({
            'size': size,
            'funds': funds,
        })

        return cbpro.utils.filter_empty(params)

    def cancel(self, product_id: str = None) -> dict:
        if product_id is None:
            return None

        return {'product_id': product_id}

    def list(self, status: str, product_id: str = None) -> dict:
        cbpro.check.orders_list_status(status)

        params = cbpro.utils.filter_empty({
            'status': status,
            'product_id': product_id
        })

        return params


class FillsModel(object):
    def list(self, product_id: str = None, order_id: str = None) -> dict:
        cbpro.check.fills_get_id(product_id, order_id)

        if product_id:
            return {'product_id': product_id}

        return {'order_id': order_id}


class DepositsModel(object):
    def list(self,
             type_: str = None,
             profile_id: str = None,
             before: str = None,
             after: str = None,
             limit: int = None) -> dict:

        if type_:
            cbpro.check.deposits_list_type(type_)

        if limit:
            cbpro.check.deposits_list_limit(limit)

        params = {
            'type': type_,
            'profile_id': profile_id,
            'before': before,
            'after': after,
            'limit': limit
        }

        return cbpro.utils.filter_empty(params)

    def payment(self,
                amount: float,
                currency: str,
                payment_id: str) -> dict:

        return {
            'amount': amount,
            'currency': currency,
            'payment_method_id': payment_id
        }

    def coinbase(self,
                 amount: float,
                 currency: str,
                 coinbase_id: str) -> dict:

        return {
            'amount': amount,
            'currency': currency,
            'coinbase_account_id': coinbase_id
        }


class WithdrawalsModel(DepositsModel):
    def __init__(self):
        super(WithdrawalsModel, self).__init__()

    def crypto(self,
               amount: float,
               currency: str,
               address: str) -> dict:

        return {
            'amount': amount,
            'currency': currency,
            'crypto_address': address
        }

    def estimate(self, currency: str, address: str) -> dict:
        return {
            'currency': currency,
            'crypto_address': address
        }


class ConversionsModel(object):
    def create(self,
               from_: str,
               to: str,
               amount: float) -> dict:

        return {
            'from': from_,
            'to': to,
            'amount': amount
        }


class ProfilesModel(object):
    def list(self, active: bool) -> dict:
        return {'active': active}

    def transfer(self,
                 from_: str,
                 to: str,
                 currency: str,
                 amount: float) -> dict:

        return {
            'from': from_,
            'to': to,
            'currency': currency,
            'amount': amount
        }


class PrivateModel(PublicModel):
    def __init__(self):
        super(PrivateModel, self).__init__()

        self.orders = OrdersModel()
        self.fills = FillsModel()
        self.deposits = DepositsModel()
        self.withdrawals = WithdrawalsModel()
        self.conversions = ConversionsModel()
        self.profiles = ProfilesModel()
