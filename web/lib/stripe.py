class StripeException(Exception):
    pass


def post_charge():
    raise StripeException('Credit card invalid')