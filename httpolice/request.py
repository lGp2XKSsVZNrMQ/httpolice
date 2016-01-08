# -*- coding: utf-8; -*-

from httpolice import message, parse, syntax
from httpolice.common import Unparseable
from httpolice.transfer_coding import known_codings as tc


class Request(message.Message):

    def __repr__(self):
        return '<Request %s>' % self.method

    def __init__(self, method_, target, version_, header_entries,
                 was_tls=None, body=None, trailer_entries=None, raw=None):
        super(Request, self).__init__(version_, header_entries,
                                      body, trailer_entries, raw)
        self.method = method_
        self.target = target
        self.was_tls = was_tls


def parse_stream(stream, was_tls=None):
    state = parse.State(stream)
    reqs = []
    while not state.is_eof():
        try:
            (method_, target, version_) = syntax.request_line.parse(state)
            entries = \
                parse.many(syntax.header_field + ~syntax.crlf).parse(state)
            syntax.crlf.parse(state)
        except parse.ParseError:
            reqs.append(Unparseable)
            return reqs
        req = Request(method_, target, version_, entries, was_tls)
        req.body = Unparseable
        reqs.append(req)

        # RFC 7230 section 3.3.3
        if req.headers.transfer_encoding:
            codings = list(req.headers.transfer_encoding)
            if codings.pop() == tc.chunked:
                if not message.parse_chunked(req, state):
                    return reqs
            else:
                req.complain(1001)
                return reqs
            while codings and (req.body is not Unparseable):
                message.decode_transfer_coding(req, codings.pop())
        elif req.headers.content_length:
            n = req.headers.content_length.value
            if n is Unparseable:
                return reqs
            try:
                req.body = parse.nbytes(n, n).parse(state)
            except parse.ParseError:
                req.complain(1004)
                return reqs
        else:
            req.body = ''

    return reqs