def assert_true(value: object, message: str):
    assert bool(value), message


def assert_false(value: object, message: str):
    assert not bool(value), message


def assert_and(object1: object, object2: object, message: str):
    assert object1 and object2, message


def assert_in(value: object, accepted: list, message: str):
    assert value and value in accepted, message


def assert_is(object1: object, object2: object, message: str):
    assert isinstance(object1, object2), message


def assert_xor(object1: object, object2: object, message: str):
    # * villagers screaming black magic from the distance *
    # https://stackoverflow.com/a/2451393/15147156
    assert (object1 is None) ^ (object2 is None), message


def products_order_book(level: int):
    accepted = [1, 2, 3]
    message = f'`level` must be one of: {accepted}'
    assert_in(level, accepted, message)


def products_history_range(start: str, end: str):
    message = 'both `start` and `end` must be defined'
    assert_and(start, end, message)


def products_history_granularity(value: int):
    accepted = [60, 300, 900, 3600, 21600, 86400]
    message = f'`granularity` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_base_side(value: str):
    accepted = ['buy', 'sell']
    message = f'`side` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_base_type(value: str):
    accepted = ['limit', 'market']
    message = f'`type` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_base_stp(value: str):
    accepted = ['dc', 'co', 'cn', 'cb']
    message = f'`stp` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_base_stop(value: str):
    accepted = ['loss', 'entry']
    message = f'`stop` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_base_stop_price(stop: str, stop_price: float):
    assert_and(stop, stop_price, 'both `stop` and `stop_price` must be defined')
    assert_is(stop_price, float, '`stop_price` must be of type float')


def orders_limit_time_in_force(value: str):
    accepted = ['GTC', 'GTT', 'IOC', 'FOK']
    message = f'`time_in_force` must be one of: {accepted}'
    assert_in(value, accepted, message)


def orders_limit_cancel_after(time_in_force: str):
    condition = time_in_force == 'GTT'
    message = 'requires `time_in_force` to be `GTT`'
    assert_true(condition, message)


def orders_limit_post_only(time_in_force: str):
    condition = time_in_force in ['IOC', 'FOK']
    message = 'invalid when `time_in_force` is `IOC` or `FOK`'
    assert_false(condition, message)


def orders_market_size_or_funds(size, funds):
    message = 'one of `size` or `funds` is required'
    assert_xor(size, funds, message)


def orders_list_status(value: str):
    accepted = ['open', 'pending', 'active', 'done', 'all']
    message = f'`status` must be one of: {accepted}'
    assert_in(value, accepted, message)


def fills_get_id(product_id: str, order_id: str):
    message = 'one of `product_id` or `order_id` is required'
    assert_xor(product_id, order_id, message)
