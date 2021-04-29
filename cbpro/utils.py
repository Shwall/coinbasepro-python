def filter_empty(params: dict) -> dict:
    return dict((k, v) for k, v in params.items() if v is not None)
