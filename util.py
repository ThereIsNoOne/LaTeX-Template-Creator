from settings import WIDTH, HEIGHT


def height_prc(percent: int) -> int:
    return HEIGHT/100 * percent


def width_prc(percent: int) -> int:
    return WIDTH/100 * percent
