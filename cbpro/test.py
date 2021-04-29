def assert_true(value: object, message: str):
    assert bool(value), message


def assert_false(value: object, message: str):
    assert not bool(value), message


def assert_both(object1: object, object2: object, message: str):
    assert object1 and object2, message


def assert_list(value: object, accepted: list, message: str):
    assert value and value in accepted, message


def assert_xor(object1: object, object2: object) -> bool:
    # * villagers screaming black magic from the distance *
    # https://stackoverflow.com/a/2451393/15147156
    return not (object1 is None) ^ (object2 is None)


def products_order_book(value: int):
    accepted = [1, 2, 3]
    message = f'`level` must be one of: {accepted}'
    assert_list(value, accepted, message)


def products_history_range(start: str, end: str):
    message = f'both `start` and `end` must be defined'
    assert_both(start, end, message)


def products_history_granularity(value: int):
    accepted = [60, 300, 900, 3600, 21600, 86400]
    message = f'`granularity` must be one of: {accepted}'
    assert_list(value, accepted, message)


def orders_base_side(value: str):
    accepted = ['buy', 'sell']
    message = f'`side` must be one of: {accepted}'
    assert_list(value, accepted, message)


def orders_base_type(value: str):
    accepted = ['limit', 'market']
    message = f'`type` must be one of: {accepted}'
    assert_list(value, accepted, message)


def orders_base_stp(value: str):
    accepted = ['dc', 'co', 'cn', 'cb']
    message = f'`stp` must be one of: {accepted}'
    assert_list(value, accepted, message)


def orders_base_stop(value: str):
    accepted = ['loss', 'entry']
    message = f'`stop` must be one of: {accepted}'
    assert_list(value, accepted, message)


def orders_base_stop_price(stop: str, stop_price: float):
    message = 'both `stop` and `stop_price` must be defined'
    assert_both(stop, stop_price, message)


def orders_limit_ioc_or_fok(value: str):
    message = 'invalid when `time_in_force` is `IOC` or `FOK`'
    condition = value in ['IOC', 'FOK']
    assert_false(condition, message)


def orders_limit_time_in_force(value: str):
    message = 'requires `time_in_force` to be `GTT`'
    condition = value == 'GTT'
    assert_true(condition, message)


def orders_market_size_or_funds(size, funds) -> bool:
    message = 'one of `size` or `funds` is required'
    condition = assert_xor(size, funds)
    assert_false(condition, message)


def orders_list_status(value: str):
    accepted = ['all', 'open', 'pending', 'active']
    message = f'`status` must be one of: {accepted}'
    assert_list(value, accepted, message)


def fills_get_id(product_id: str, order_id: str):
    message = 'one of `product_id` or `order_id` is required'
    condition = assert_xor(order_id, product_id)
    assert_false(condition, message)


def overdraft_enabled(order: dict) -> bool:
    return order.get('overdraft_enabled') is not None


def funding_amount(order: dict) -> bool:
    return order.get('funding_amount') is not None


def cancel_after(order: dict) -> bool:
    return order.get('cancel_after') is not None


def post_only(order: dict) -> bool:
    return order.get('post_only') is not None


def time_in_force(order: dict) -> bool:
    return order.get('time_in_force') is not None


def not_good_till_time(order: dict) -> bool:
    return order.get('time_in_force') != 'GTT'


def is_fill_or_kill(order: dict) -> bool:
    return order.get('time_in_force') in ['IOC', 'FOK']


def ismarket(order: dict) -> bool:
    return order.get('type') == 'market'


def islimit(order: dict) -> bool:
    return order.get('type') == 'limit'


def isstop(order: dict) -> bool:
    return order.get('type') == 'stop'


def market(order: dict) -> None:
    if ismarket(order) or isstop(order):
        if size_or_funds(order):
            message = 'Either `size` or `funds` must be specified ' \
                      'for market/stop orders (but not both).'
            raise ValueError(message)


def limit(order: dict) -> None:
    if islimit(order):
        if cancel_after(order) and not_good_till_time(order):
            message = 'May only specify a cancel period when time_' \
                      'in_force is `GTT`'
            raise ValueError(message)

        if post_only(order) and is_fill_or_kill(order):
            message = 'post_only is invalid when time in force is ' \
                      '`IOC` or `FOK`'
            raise ValueError(message)


def margin(order: dict) -> None:
    if overdraft_enabled(order) and funding_amount(order):
        message = 'Margin funding must be specified through use of ' \
                  'overdraft or by setting a funding amount, but not ' \
                  'both'
        raise ValueError(message)
