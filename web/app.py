import time
import random
from flask import Flask
import requests

from opentelemetry import trace
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


app = Flask(__name__)
trace.set_tracer_provider(TracerProvider())

tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="otel-agent:55680")
span_processor = BatchExportSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)


def wait_every_10s():
    now = int(time.time())

    # wait every 10s
    if (now // 10) % 2 == 0:
        time.sleep(3)


class InvalidCredentials(Exception):
    pass


@app.route("/home")
def home():
    random.uniform(0, 0.5)

    with tracer.start_as_current_span('find-movies'):
        wait_every_10s()

    try:
        _get_user()
    except InvalidCredentials:
        return 'InvalidCredentials'

    return 'movies list'


@app.route("/subscription", methods=['POST'])
def subscription():
    from lib.payments import start_subscription

    random.uniform(0.2, 0.5)

    start_subscription()

    return 'success'


def _get_user():
    with tracer.start_as_current_span('get-user'):
        res = requests.get('http://users:8082/get-user')

        if res.status_code == 500:
            raise InvalidCredentials('Error calling users service')

        return res
