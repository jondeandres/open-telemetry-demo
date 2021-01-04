import time
import random
from flask import Flask

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
    if now / 5 % 2 == 0:
        time.sleep(3)


@app.route("/home")
def home():
    random.uniform(0, 0.5)
    with tracer.start_as_current_span('home-job'):
        wait_every_10s()

    return 'world!'
