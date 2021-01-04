import random
from flask import Flask
import sqlite3

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

dbconn = sqlite3.connect(":memory:", check_same_thread=False)


class LoginException(Exception):
    pass


@app.route("/get-user")
def get_user():
    cursor = dbconn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = 1")
    cursor.close()
    dbconn.commit()

    flaky_function()

    return 'user found'


def flaky_function():
    with tracer.start_as_current_span('flaky-function'):
        foo()


def foo():
    bar()


def bar():
    if random.randint(0, 5) == 0:
        raise LoginException('Something failed getting user')


@app.before_first_request
def initialize_database():
    c = dbconn.cursor()

    # Create table
    c.execute("""
    CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username text
    );
    """)

    # Insert a row of data
    c.execute("INSERT INTO users (username) VALUES ('foo')")
    c.execute("INSERT INTO users (username) VALUES ('bar')")
    c.execute("INSERT INTO users (username) VALUES ('hash')")

    # Save (commit) the changes
    dbconn.commit()
