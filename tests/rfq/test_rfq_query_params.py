from unittest import TestCase
from urllib.parse import urlencode

from py_clob_client.rfq import GetRfqRequestsParams, GetRfqQuotesParams
from py_clob_client.rfq.rfq_helpers import (
    parse_rfq_requests_params,
    parse_rfq_quotes_params,
)


class TestRfqQueryParams(TestCase):
    def test_get_rfq_requests_request_ids_are_repeated_query_params(self):
        id_1 = "019b69d4-2eb6-7ef9-8595-d149c97de10b"
        id_2 = "019b69c3-d49e-7abf-88d0-cb3fd79fb721"
        params = GetRfqRequestsParams(request_ids=[id_1, id_2])

        parsed = parse_rfq_requests_params(params)
        query_string = urlencode(parsed, doseq=True)

        self.assertEqual(query_string, f"requestIds={id_1}&requestIds={id_2}")

    def test_get_rfq_quotes_quote_ids_are_repeated_query_params(self):
        quote_1 = "019b69d4-2eb6-7ef9-8595-d149c97de10b"
        quote_2 = "019b69c3-d49e-7abf-88d0-cb3fd79fb721"
        params = GetRfqQuotesParams(quote_ids=[quote_1, quote_2])

        parsed = parse_rfq_quotes_params(params)
        query_string = urlencode(parsed, doseq=True)

        self.assertEqual(query_string, f"quoteIds={quote_1}&quoteIds={quote_2}")
