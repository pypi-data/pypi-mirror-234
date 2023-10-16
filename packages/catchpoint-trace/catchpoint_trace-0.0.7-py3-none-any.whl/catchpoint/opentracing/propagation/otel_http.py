import re

from catchpoint import constants

from catchpoint.opentracing.propagation.text import TextMapPropagator
from catchpoint.opentracing.span_context import CatchpointSpanContext

PATTERN = "([0-9a-f]{2})\-([0-9a-f]{32})\-([0-9a-f]{16})\-([0-9a-f]{2})"
INVALID_TRACE_ID = "00000000000000000000000000000000"
INVALID_PARENT_SPAN_ID = "0000000000000000"

traceparent_regex = re.compile(PATTERN)

class OTELHTTPPropagator(TextMapPropagator):

    @staticmethod
    def extract_value_from_header(header_name, headers):
        for header, value in headers.items():
            if header.lower() == header_name.lower():
                return value


    def inject(self, span_context, carrier):
        raise Exception("Inject is not supported yet")


    def extract(self, carrier):
        try:
            traceparent = OTELHTTPPropagator.extract_value_from_header(constants.OTEL_TRACEPARENT_KEY, carrier)
            if not traceparent:
                return None
            match = traceparent_regex.search(traceparent)
            if not match:
                return None
            trace_id = match.groups()[1]
            span_id = match.groups()[2]
        except:
            return None

        if not (trace_id and span_id):
            return None

        if INVALID_TRACE_ID == trace_id or INVALID_PARENT_SPAN_ID == span_id:
            return None

        return CatchpointSpanContext(trace_id=trace_id, span_id=span_id, transaction_id=None, baggage={})
