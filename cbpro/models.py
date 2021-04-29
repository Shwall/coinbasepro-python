import cbpro.utils
import cbpro.test


class ProductsModel(object):
    def order_book(self, level: int = None) -> dict:
        if level is None:
            return None

        cbpro.test.products_order_book(level)

        return {'level': level}

    def history(self,
                start: str = None,
                end: str = None,
                granularity: int = 86400) -> dict:

        params = dict()

        if start or end:
            params['start'] = start
            params['end'] = end

            cbpro.test.products_history_range(start, end)

        params['granularity'] = granularity

        cbpro.test.products_history_granularity(granularity)

        return params


class OrdersModel(object):
    def base(self,
             product_id: str,
             side: str,
             type_: str = None,
             client_oid: str = None,
             stp: str = None,
             stop: str = None,
             stop_price: float = None) -> dict:

        cbpro.test.orders_base_side(side)

        if type_:
            cbpro.test.orders_base_type(type_)

        if stp:
            cbpro.test.orders_base_stp(stp)

        if stop or stop_price:
            cbpro.test.orders_base_stop_price(stop, stop_price)
            cbpro.test.orders_base_stop(stop)

        params = {
            'product_id': product_id,
            'side': side,
            'type': type_,
            'client_oid': client_oid,
            'stp': stp,
            'stop': stop,
            'stop_price': stop_price
        }

        params = cbpro.utils.filter_empty(params)

        return params

    def limit(self,
              product_id: str,
              side: str,
              price: float,
              size: float,
              time_in_force: str = None,
              cancel_after: str = None,
              post_only: bool = None,
              type_: str = None,
              client_oid: str = None,
              stp: str = None,
              stop: str = None,
              stop_price: float = None) -> dict:

        cbpro.test.orders_base_side(side)

        if type_:
            cbpro.test.orders_base_type(type_)

        if stp:
            cbpro.test.orders_base_stp(stp)

        if stop or stop_price:
            cbpro.test.orders_base_stop_price(stop, stop_price)
            cbpro.test.orders_base_stop(stop)

        if time_in_force:
            cbpro.test.orders_limit_ioc_or_fok(time_in_force)
            cbpro.test.orders_limit_time_in_force(time_in_force)

        params = {
            'product_id': product_id,
            'side': side,
            'price': price,
            'size': size,
            'time_in_force': time_in_force,
            'cancel_after': cancel_after,
            'post_only': post_only,
            'type': type_,
            'client_oid': client_oid,
            'stp': stp,
            'stop': stop,
            'stop_price': stop_price
        }

        params = cbpro.utils.filter_empty(params)

        return params

    def market(self,
               product_id: str,
               side: str,
               size: float = None,
               funds: float = None,
               type_: str = None,
               client_oid: str = None,
               stp: str = None,
               stop: str = None,
               stop_price: float = None) -> dict:

        cbpro.test.orders_base_side(side)

        if size or funds:
            cbpro.test.orders_market_size_or_funds(size, funds)

        if type_:
            cbpro.test.orders_base_type(type_)

        if stp:
            cbpro.test.orders_base_stp(stp)

        if stop or stop_price:
            cbpro.test.orders_base_stop_price(stop, stop_price)
            cbpro.test.orders_base_stop(stop)

        params = {
            'product_id': product_id,
            'side': side,
            'size': size,
            'funds': funds,
            'type': type_,
            'client_oid': client_oid,
            'stp': stp,
            'stop': stop,
            'stop_price': stop_price
        }

        params = cbpro.utils.filter_empty(params)

        return params

    def cancel(self, product_id: str = None) -> dict:
        if product_id is None:
            return None

        return {'product_id': product_id}

    def list(self, status: str, product_id: str = None) -> dict:
        cbpro.test.orders_list_status(status)

        params = {
            'status': status,
            'product_id': product_id
        }

        params = cbpro.utils.filter_empty(params)

        return params


class FillsModel(object):
    def get(self, product_id: str = None, order_id: str = None) -> dict:
        cbpro.test.fills_get_id(product_id, order_id)

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

        return None


class PublicModel(object):
    def __init__(self):
        self.products = ProductsModel()


class PrivateModel(PublicModel):
    def __init__(self):
        super(PrivateModel, self).__init__()

        self.orders = OrdersModel()
        self.fills = FillsModel()
        self.deposits = DepositsModel()
