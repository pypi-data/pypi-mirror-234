def to_side(side: str):  # either 'buy' or 'sell'
    return side


def to_symbol(base: str, quote: str):
    return f'{base}-{quote}-SWAP'
