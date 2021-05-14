import typing

Iterable = typing.TypeVar('Iterable', list, dict)


def assert_true(value: object, message: str):
    assert bool(value), message


def assert_false(value: object, message: str):
    assert not bool(value), message


def assert_and(object1: object, object2: object, message: str):
    assert object1 and object2, message


def assert_or(object1: object, object2: object, message: str):
    assert object1 or object2, message


def assert_xor(object1: object, object2: object, message: str):
    # * villagers screaming black magic from the distance *
    # https://stackoverflow.com/a/2451393/15147156
    assert (object1 is None) ^ (object2 is None), message


def assert_is(object1: object, object2: object, message: str):
    assert isinstance(object1, object2), message


def assert_in(value: object, accepted: Iterable, message: str):
    assert value and value in accepted, message


def assert_message(label: str, type_: str) -> str:
    return f'`{label}` must be of type {type_}'


def assert_int(value: int, label: str):
    assert_is(value, int, assert_message(label, 'int'))


def assert_float(value: float, label: str):
    assert_is(value, float, assert_message(label, 'float'))


def assert_str(value: str, label: str):
    assert_is(value, str, assert_message(label, 'str'))


def assert_list(value: list, label: str):
    assert_is(value, list, assert_message(label, 'str'))


def assert_dict(value: dict, label: str):
    assert_is(value, dict, assert_message(label, 'dict'))


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


def deposits_list_type(value: str):
    accepted = ['deposit', 'internal_depost']
    message = '`type` must be one of: {accepted}'
    assert_in(value, accepted, message)


def deposits_list_limit(value: int):
    condition = 0 < value <= 100
    message = '`value` must be type int where 0 < `value` <= 100'
    assert_true(condition, message)


# TODO:
#   - Clean up websocket params tests
#   - Seperate the functions from one another
def websocket_params(value: dict):
    def assert_params():
        assert_dict(value, 'params')

    def assert_params_type():
        assert_in('type', value, 'subscription `type` must be defined')
        assert_str(value['type'], 'type')

    def assert_params_value(key):
        key = 'product_ids'
        message = f'`{key}` must be defined for subscription'
        assert_in(key, value, message)

        assert_list(value[key], key)

        message = f'`{key}` must have a value of type list[str]'
        assert_true(value[key], message)

    assert_params()
    assert_params_type()
    assert_params_value('product_ids')
    assert_params_value('channels')


def websocket_disconnect(value: object):
    import websocket

    message = f'`Stream.connection` must be an instance of `websocket.WebSocket`'
    assert_is(value, websocket.WebSocket, message)
