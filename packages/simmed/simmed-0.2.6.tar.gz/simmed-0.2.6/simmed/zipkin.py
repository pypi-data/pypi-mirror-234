import random
import functools
from flask import request, g
import requests
from py_zipkin.zipkin import zipkin_span, ZipkinAttrs, create_http_headers_for_new_span
# , zipkin_client_span
from py_zipkin.transport import BaseTransportHandler
# from py_zipkin.request_helpers import create_http_headers

import simmed.config as config
import logging


def gen_hex_str(length=16):
    charset = (
        'abcdef'
        '0123456789'
    )
    return ''.join([random.choice(charset) for _ in range(length)])


class HttpTransport(BaseTransportHandler):
    def get_max_payload_bytes(self):
        return None

    def send(self, encoded_span):
        # The collector expects a thrift-encoded list of spans.
        try:
            requests.post(
                f'http://{config.ZIPKIN_HOST}:{config.ZIPKIN_PORT}/api/v1/spans',
                data=encoded_span,
                headers={'Content-Type': 'application/x-thrift'},
                timeout=(1, 5),
            )
        except Exception as e:
            logging.exception("Failed to send to zipkin:" + str(e))


# class KafkaTransport(BaseTransportHandler):

#     def get_max_payload_bytes(self):
#         # By default Kafka rejects messages bigger than 1000012 bytes.
#         return 1000012

#     def send(self, message):
#         from kafka import SimpleProducer, KafkaClient
#         kafka_client = KafkaClient('{}:{}'.format('localhost', 9092))
#         producer = SimpleProducer(kafka_client)
#         producer.send_messages('kafka_topic_name', message)


def with_zipkin_span(span_name, **kwargs):
    """https://github.com/Yelp/py_zipkin/issues/96
    """
    def decorate(f):
        @functools.wraps(f)
        def inner(*args, **kw):
            zipkin_kwargs = dict(
                span_name=span_name,
                service_name=config.APPNAME
            )
            zipkin_kwargs.update(**kwargs)
            with zipkin_span(**zipkin_kwargs):
                return f(*args, **kw)
        return inner
    return decorate


def set_tags(extra_annotations):
    if not config.ZIPKIN_ENABLE:
        return

    if getattr(g, '_zipkin_span', None):
        logging.debug("Set tags")
        try:
            span = g._zipkin_span
            if span:
                #logging.info("update: %s", extra_annotations)
                span.update_binary_annotations(extra_annotations)
        except Exception as e:
            logging.log_critical_error("Failed to set zipkin:" + str(e))


def get_zipkin_attrs(headers):
    trace_id = headers.get('X-B3-TraceID') or gen_hex_str()
    span_id = headers.get('X-B3-SpanID') or gen_hex_str()
    parent_span_id = headers.get('X-B3-ParentSpanID')
    flags = headers.get('X-B3-Flags')
    is_sampled = headers.get('X-B3-Sampled') == '1'

    return ZipkinAttrs(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        flags=flags,
        is_sampled=is_sampled,
    )


def flask_start_zipkin():
    """
    Put it to before_request event.
    :return:
    """
    if not config.ZIPKIN_ENABLE:
        return
    zipkin_attrs = get_zipkin_attrs(request.headers)
    if request.headers.get('X-B3-TraceID') or request.headers.get('X-B3-SpanID'):
        logging.debug(f'Zipkin Debug: received header: {request.headers}')
    span = zipkin_span(
        service_name=config.APPNAME,
        span_name=f'{request.endpoint}.{request.method}',
        transport_handler=HttpTransport(),
        host=config.ZIPKIN_HOST,
        port=config.ZIPKIN_PORT,
        sample_rate=config.ZIPKIN_SAMPLE_RATE,
        zipkin_attrs=zipkin_attrs,
    )
    g._zipkin_span = span
    g._zipkin_span.start()


def flask_stop_zipkin():
    """
    Put it to tear_request event.
    :return:
    """
    if not config.ZIPKIN_ENABLE:
        return

    if getattr(g, '_zipkin_span', None):
        logging.debug(f'stop zipkin span {g._zipkin_span}')
        g._zipkin_span.stop()


# @zipkin_client_span(service_name=config.APPNAME, span_name="rpc")
def with_zipkin_request(func, headers):
    if not config.ZIPKIN_ENABLE:
        return func(headers)

    headers.update(create_http_headers_for_new_span())
    return func(headers)
