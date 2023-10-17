import sys

import grpc

from .enums import ComputationMode
from .lib import auth


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class StubExceptionWrapper:
    def __init__(self, wrapped, debug=False, insecure=False, host=None):
        self._insecure = insecure
        self._host = host
        self.wrapped = wrapped
        self.debug = debug
        # Store metadata as an instance variable

    @staticmethod
    def _merge_auth_metadata(original_metadata, auth_metadata):
        if original_metadata is None:
            return auth_metadata
        # Remove existing authorization header if present
        merged_metadata = [
            item for item in original_metadata if item[0].lower() != "authorization"
        ]
        # Append the new authorization header
        merged_metadata.extend(auth_metadata)
        return merged_metadata

    @staticmethod
    def is_streaming_response(obj):
        return hasattr(obj, "__iter__") and not isinstance(
            obj, (str, bytes, dict, list)
        )

    def streaming_wrapper(self, multi_threaded_rendezvous):
        try:
            for message in multi_threaded_rendezvous:
                yield message
        except grpc.RpcError as e:
            # Handle the error gracefully here.
            self.handle_grpc_error(e)

    def __getattr__(self, name):
        insecure = self._insecure
        attr = getattr(self.wrapped, name)
        if name != "GetAuthConfig" and callable(attr):

            def wrapper(*args, **kwargs):
                try:
                    # Use the stored metadata for the call
                    token = auth.singleton.get_access_token_or_authenticate(
                        self._insecure, self._host
                    )
                    if token is not None:
                        kwargs["metadata"] = self._merge_auth_metadata(
                            kwargs.get("metadata"),
                            [("authorization", "Bearer " + token)],
                        )
                    result = attr(*args, **kwargs)
                    # If result is a streaming call, wrap it.
                    if self.is_streaming_response(result):
                        return self.streaming_wrapper(result)
                    return result
                except grpc.RpcError as e:
                    self.handle_grpc_error(e)

            return wrapper
        else:
            return attr

    def handle_grpc_error(self, e):
        sys.tracebacklimit = 0
        initial_ex = None
        if self.debug:
            initial_ex = e
            sys.tracebacklimit = None
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            auth.singleton.delete_expired_token()
            raise Exception(
                f"{BCOLORS.FAIL}Authentication failed.{BCOLORS.ENDC}\n"
                "Your access token is no longer valid. Please re-run the previous command to authenticate."
            )

        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            print("\n")
            raise Exception(
                f"{BCOLORS.FAIL}Could not connect to Featureform.{BCOLORS.ENDC}\n"
                "Please check if your FEATUREFORM_HOST and FEATUREFORM_CERT environment variables are set "
                "correctly or are explicitly set in the client or command line.\n"
                f"Details: {e.details()}"
            ) from initial_ex
        elif e.code() == grpc.StatusCode.UNKNOWN:
            raise Exception(
                f"{BCOLORS.FAIL}Error: {e.details()}{BCOLORS.ENDC}"
            ) from initial_ex
        else:
            raise e


class InvalidTrainingSetFeatureComputationMode(Exception):
    def __init__(
        self,
        feature_name,
        feature_variant,
        mode=ComputationMode.CLIENT_COMPUTED.value,
        message=None,
    ):
        if message is None:
            message = (
                f"Feature '{feature_name}:{feature_variant}' is on demand. "
                f"Cannot use {mode} features for training sets. "
            )

        Exception.__init__(self, message)


class FeatureNotFound(Exception):
    def __init__(self, feature_name, feature_variant, message=None):
        error_message = f"Feature '{feature_name}:{feature_variant}' not found. Verify that the feature is registered."

        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)


class LabelNotFound(Exception):
    def __init__(self, label_name, label_variant, message=None):
        error_message = f"Label '{label_name}:{label_variant}' not found. Verify that the label is registered."
        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)


class InvalidSQLQuery(Exception):
    def __init__(self, query, message=None):
        error_message = f"Invalid SQL query. Query: ' {query} '"
        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)
