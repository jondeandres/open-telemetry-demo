from opentelemetry import trace

from .stripe import post_charge

tracer = trace.get_tracer(__name__)


def start_subscription():
    do_charge()


def do_charge():
    with tracer.start_as_current_span('do-charge'):
        import random
        random.uniform(1, 1.5)

        post_charge()
