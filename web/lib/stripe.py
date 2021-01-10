from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class StripeException(Exception):
    pass


def post_charge():
    with tracer.start_as_current_span('stripe-charge'):
        raise StripeException('Credit card invalid')