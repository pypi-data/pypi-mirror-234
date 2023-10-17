import re
from typing import Any
from typing import Callable


GCP_URL_PREFIX_REGEX = re.compile(r"^https:\/\/\w+\.googleapis\.com\/\w+\/v\w+\/(\S+)")


def sanitize_resource_urls(hub, resource: Any) -> Any:
    return _convert_resource(hub, resource, _sanitize_url)


def _sanitize_url(hub, value: Any) -> Any:
    if not isinstance(value, str):
        return value

    # GCP resources have urls in the following format:
    #   https://www.googleapis.com/<service-name>/<service-version>/<partial-url>
    # This code strips the prefix up to <partial-url> part
    match = re.match(GCP_URL_PREFIX_REGEX, value)
    return match.group(1) if match else value


def _convert_resource(
    hub,
    resource,
    value_transformer: Callable[[Any, Any], Any],
) -> Any:
    if resource is None:
        return None

    if isinstance(resource, list):
        return list(
            _convert_resource(
                hub,
                v,
                value_transformer,
            )
            for v in resource
        )
    elif isinstance(resource, set):
        return {
            _convert_resource(
                hub,
                v,
                value_transformer,
            )
            for v in resource
        }
    elif isinstance(resource, dict):
        return {
            k: _convert_resource(
                hub,
                v,
                value_transformer,
            )
            for k, v in resource.items()
        }
    else:
        return value_transformer(hub, resource)
