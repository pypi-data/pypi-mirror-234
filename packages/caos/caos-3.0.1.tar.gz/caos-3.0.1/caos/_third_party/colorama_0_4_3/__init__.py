from caos._third_party.colorama_0_4_3.colorama import init


def load_colorama() -> bool:
    try:
        init()
    except:
        return False
    return True
