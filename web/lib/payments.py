from .stripe import post_charge


def start_subscription():
    do_charge()


def do_charge():
    import random
    random.uniform(1, 1.5)
    post_charge()
