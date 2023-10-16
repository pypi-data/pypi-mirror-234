def to_side(side: str):  # either 'buy' or 'sell'
    return side.upper()


def to_symbol(base: str, quote: str):
    return f'{base}{quote}'
