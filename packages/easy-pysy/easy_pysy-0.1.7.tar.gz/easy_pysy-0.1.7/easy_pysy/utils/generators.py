def tri_wave(min_value: int, max_value: int, step: int = 1):
    while True:
        yield from range(min_value, max_value, step)
        yield from range(max_value, min_value, -step)


def float_range(start: float, stop: float, step: float = 1.0, decimals: int = 2):
    for i in range(int(start / step), int(stop / step)):
        yield round(i * step, ndigits=decimals)
