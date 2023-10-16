from argrelay.handler_response.AbstractClientResponseHandler import AbstractClientResponseHandler

# TODO: Figure out how to make schema be defined in terms of this value:
perf_arg_values_ = "arg_values"
"""
This constant avoids import of similar `ArgValuesSchema.arg_values_` triggering `Schema` import which more than doubles
total round trip time for the client - see also `test_ProposeArgValuesRemoteClientCommand_imports_minimum`.
"""


class ProposeArgValuesClientResponseHandler(AbstractClientResponseHandler):

    def __init__(
        self,
    ):
        super().__init__(
        )

    def handle_response(self, response_dict: dict):
        # TODO: This is not correct expectation:
        #       If this handler received data from JSON payload, it would print list in Python-style output.
        #       It works only because string behind `response_dict[perf_arg_values_]` is actually single `str`
        #       with value separated by `\n` (it is not a `list[str]`).
        # TODO: 1. Create command which sends JSON (and plugs into the framework where this handler is useful).
        #       2. Make `ProposeArgValuesRemoteClientCommand` execute without handler - print string directly.
        print(response_dict[perf_arg_values_])
