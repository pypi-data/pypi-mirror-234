"""State module for managing HealthChecks."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

from idem_gcp.tool.gcp.utils import global_absent

# prevent commit hook from removing the import
absent = global_absent

__contracts__ = ["resource"]
RESOURCE_TYPE = "compute.health_check"
RESOURCE_TYPE_FULL = "gcp.compute.health_check"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    health_check: str = None,
    ssl_health_check: make_dataclass(
        "SSLHealthCheck",
        [
            ("port_name", str, field(default=None)),
            ("response", str, field(default=None)),
            ("proxy_header", str, field(default=None)),
            ("port_specification", str, field(default=None)),
            ("port", int, field(default=None)),
            ("request", str, field(default=None)),
        ],
    ) = None,
    https_health_check: make_dataclass(
        "HTTPSHealthCheck",
        [
            ("host", str, field(default=None)),
            ("port_specification", str, field(default=None)),
            ("port_name", str, field(default=None)),
            ("proxy_header", str, field(default=None)),
            ("request_path", str, field(default=None)),
            ("port", int, field(default=None)),
            ("response", str, field(default=None)),
        ],
    ) = None,
    type_: (str, "alias=type") = None,
    description: str = None,
    http2_health_check: make_dataclass(
        "HTTP2HealthCheck",
        [
            ("port_specification", str, field(default=None)),
            ("port", int, field(default=None)),
            ("port_name", str, field(default=None)),
            ("request_path", str, field(default=None)),
            ("proxy_header", str, field(default=None)),
            ("response", str, field(default=None)),
            ("host", str, field(default=None)),
        ],
    ) = None,
    tcp_health_check: make_dataclass(
        "TCPHealthCheck",
        [
            ("proxy_header", str, field(default=None)),
            ("port_specification", str, field(default=None)),
            ("response", str, field(default=None)),
            ("request", str, field(default=None)),
            ("port_name", str, field(default=None)),
            ("port", int, field(default=None)),
        ],
    ) = None,
    check_interval_sec: int = None,
    unhealthy_threshold: int = None,
    timeout_sec: int = None,
    log_config: make_dataclass(
        "HealthCheckLogConfig", [("enable", bool, field(default=None))]
    ) = None,
    grpc_health_check: make_dataclass(
        "GRPCHealthCheck",
        [
            ("port_specification", str, field(default=None)),
            ("grpc_service_name", str, field(default=None)),
            ("port_name", str, field(default=None)),
            ("port", int, field(default=None)),
        ],
    ) = None,
    http_health_check: make_dataclass(
        "HTTPHealthCheck",
        [
            ("request_path", str, field(default=None)),
            ("port", int, field(default=None)),
            ("host", str, field(default=None)),
            ("response", str, field(default=None)),
            ("port_specification", str, field(default=None)),
            ("port_name", str, field(default=None)),
            ("proxy_header", str, field(default=None)),
        ],
    ) = None,
    healthy_threshold: int = None,
) -> Dict[str, Any]:
    r"""Creates or updates a HealthCheck resource in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str):
            Project ID for this request.

        ssl_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * port_name(str, Optional):
                Not supported.

            * response(str, Optional):
                Creates a content-based SSL health check. In addition to establishing a TCP connection and the TLS handshake, you can configure the health check to pass only when the backend sends this exact response ASCII string, up to 1024 bytes in length. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-ssl-tcp

            * proxy_header(str, Optional):
                Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.

            * port_specification(str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Not supported by target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * port(int, Optional):
                The TCP port number to which the health check prober sends packets. The default value is 443. Valid values are 1 through 65535.

            * request(str, Optional):
                Instructs the health check prober to send this exact ASCII string, up to 1024 bytes in length, after establishing the TCP connection and SSL handshake.

        https_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * host(str, Optional):
                The value of the host header in the HTTPS health check request. If left empty (default value), the host header is set to the destination IP address to which health check packets are sent. The destination IP address depends on the type of load balancer. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#hc-packet-dest

            * port_specification (str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Not supported by target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * port_name (str, Optional):
                Not supported.

            * proxy_header (str, Optional):
                Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.
                Enum type. Allowed values:
                    "NONE"
                    "PROXY_V1"

            * request_path (str, Optional):
                The request path of the HTTPS health check request. The default value is /.

            * port (int, Optional):
                The TCP port number to which the health check prober sends packets. The default value is 443. Valid values are 1 through 65535.

            * response (str, Optional):
                Creates a content-based HTTPS health check. In addition to the required HTTP 200 (OK) status code, you can configure the health check to pass only when the backend sends this specific ASCII response string within the first 1024 bytes of the HTTP response body. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-http

        type(str, Optional):
            Specifies the type of the healthCheck, either TCP, SSL, HTTP, HTTPS, HTTP2 or GRPC. Exactly one of the protocol-specific health check fields must be specified, which must match type field.
            Enum type. Allowed values:
                "GRPC"
                "HTTP"
                "HTTP2"
                "HTTPS"
                "INVALID"
                "SSL"
                "TCP". Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        http2_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * port_specification (str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Not supported by target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * port (int, Optional):
                The TCP port number to which the health check prober sends packets. The default value is 443. Valid values are 1 through 65535.

            * port_name (str, Optional):
                Not supported.

            * request_path (str, Optional):
                The request path of the HTTP/2 health check request. The default value is /.

            * proxy_header (str, Optional):
                Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.
                Enum type. Allowed values:
                    "NONE"
                    "PROXY_V1"

            * response (str, Optional):
                Creates a content-based HTTP/2 health check. In addition to the required HTTP 200 (OK) status code, you can configure the health check to pass only when the backend sends this specific ASCII response string within the first 1024 bytes of the HTTP response body. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-http

            * host (str, Optional):
                The value of the host header in the HTTP/2 health check request. If left empty (default value), the host header is set to the destination IP address to which health check packets are sent. The destination IP address depends on the type of load balancer. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#hc-packet-dest

        tcp_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * proxy_header (str, Optional):
                Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.
                Enum type. Allowed values:
                    "NONE"
                    "PROXY_V1"

            * port_specification (str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Not supported by target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * response (str, Optional):
                Creates a content-based TCP health check. In addition to establishing a TCP connection, you can configure the health check to pass only when the backend sends this exact response ASCII string, up to 1024 bytes in length. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-ssl-tcp
            * request (str, Optional):
                Instructs the health check prober to send this exact ASCII string, up to 1024 bytes in length, after establishing the TCP connection.
            * port_name (str, Optional):
                Not supported.
            * port (int, Optional):
                The TCP port number to which the health check prober sends packets. The default value is 80. Valid values are 1 through 65535.

        check_interval_sec(int, Optional):
            How often (in seconds) to send a health check. The default value is 5 seconds. Defaults to None.

        unhealthy_threshold(int, Optional):
            A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Defaults to None.

        timeout_sec(int, Optional):
            How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Defaults to None.

        log_config(Dict[str, Any], Optional):
            Configure logging on this health check.
            HealthCheckLogConfig: Configuration of logging on a health check. If logging is enabled, logs will be exported to Stackdriver. Defaults to None.

            * enable (bool, Optional):
                Indicates whether or not to export logs. This is false by default, which means no health check logging will be done.

        grpc_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * port_specification (str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Not supported by target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * grpc_service_name (str, Optional):
                The gRPC service name for the health check. This field is optional. The value of grpc_service_name has the following meanings by convention: - Empty service_name means the overall status of all services at the backend. - Non-empty service_name means the health of that gRPC service, as defined by the owner of the service. The grpc_service_name can only be ASCII.

            * port_name (str, Optional):
                Not supported.

            * port (int, Optional):
                The TCP port number to which the health check prober sends packets. Valid values are 1 through 65535.

        http_health_check(Dict[str, Any], Optional):
            Defaults to None.

            * request_path (str, Optional):
                The request path of the HTTP health check request. The default value is /.

            * port (int, Optional):
                The TCP port number to which the health check prober sends packets. The default value is 80. Valid values are 1 through 65535.

            * host (str, Optional):
                The value of the host header in the HTTP health check request. If left empty (default value), the host header is set to the destination IP address to which health check packets are sent. The destination IP address depends on the type of load balancer. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#hc-packet-dest

            * response (str, Optional):
                Creates a content-based HTTP health check. In addition to the required HTTP 200 (OK) status code, you can configure the health check to pass only when the backend sends this specific ASCII response string within the first 1024 bytes of the HTTP response body. For details, see: https://cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-http

            * port_specification (str, Optional):
                Specifies how a port is selected for health checking. Can be one of the following values: USE_FIXED_PORT: Specifies a port number explicitly using the port field in the health check. Supported by backend services for pass-through load balancers and backend services for proxy load balancers. Also supported in legacy HTTP health checks for target pools. The health check supports all backends supported by the backend service provided the backend can be health checked. For example, GCE_VM_IP network endpoint groups, GCE_VM_IP_PORT network endpoint groups, and instance group backends. USE_NAMED_PORT: Not supported. USE_SERVING_PORT: Provides an indirect method of specifying the health check port by referring to the backend service. Only supported by backend services for proxy load balancers. Not supported by target pools. Not supported by backend services for pass-through load balancers. Supports all backends that can be health checked; for example, GCE_VM_IP_PORT network endpoint groups and instance group backends. For GCE_VM_IP_PORT network endpoint group backends, the health check uses the port number specified for each endpoint in the network endpoint group. For instance group backends, the health check uses the port number determined by looking up the backend service's named port in the instance group's list of named ports.
                Enum type. Allowed values:
                    "USE_FIXED_PORT" - The port number in the health check's port is used for health checking. Applies to network endpoint group and instance group backends.
                    "USE_NAMED_PORT" - Not supported.
                    "USE_SERVING_PORT" - For network endpoint group backends, the health check uses the port number specified on each endpoint in the network endpoint group. For instance group backends, the health check uses the port number specified for the backend service's named port defined in the instance group's named ports.

            * port_name (str, Optional):
                Not supported.

            * proxy_header (str, Optional):
                Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.
                Enum type. Allowed values:
                    "NONE"
                    "PROXY_V1"

        healthy_threshold(int, Optional):
            A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Defaults to None.

        health_check(str):
            Name of the HealthCheck resource to return.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.compute.health_check.present:
                - name: value
                - project: value
                - type_: TCP
                - tcp_health_check:
                    port: 80
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    resource_type_camel = hub.tool.gcp.case.camel(RESOURCE_TYPE_FULL.split(".")[-1])

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE, resource_id, {**locals(), resource_type_camel: name}
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )

    # Handle operation(s) in progress, if any
    if ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), RESOURCE_TYPE
        )

        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            if handle_operation_ret.get("rerun_data"):
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                if handle_operation_ret["rerun_data"].get("has_error", False):
                    result["result"] = False
            else:
                result["result"] = False

            return result

        resource_id = handle_operation_ret["resource_id"]

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    if resource_id:
        old_get_ret = await hub.exec.gcp.compute.health_check.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"]
            and (ctx["rerun_data"] or get_resource_only_with_resource_id)
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        # long running operation has succeeded - both update and create
        if ctx.get("rerun_data"):
            result["new_state"] = old_get_ret["ret"]
            result["old_state"] = ctx["rerun_data"]["old_state"]
            if result["old_state"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(RESOURCE_TYPE_FULL, name)
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.create_comment(RESOURCE_TYPE_FULL, name)
                )
            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE, {**locals(), "healthCheck": name}
        )
        get_ret = await hub.exec.gcp.compute.health_check.get(
            ctx, resource_id=resource_id
        )

        if not get_ret["result"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        if get_ret["ret"]:
            result["old_state"] = get_ret["ret"]

    resource_body = {
        "log_config": log_config,
        "unhealthy_threshold": unhealthy_threshold,
        "name": name,
        "timeout_sec": timeout_sec,
        "description": description,
        "http_health_check": http_health_check,
        "http2_health_check": http2_health_check,
        "grpc_health_check": grpc_health_check,
        "tcp_health_check": tcp_health_check,
        "check_interval_sec": check_interval_sec,
        "healthy_threshold": healthy_threshold,
        "https_health_check": https_health_check,
        "ssl_health_check": ssl_health_check,
        "type_": type_,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        resource_body["resource_id"] = resource_id
        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            resource_body,
            RESOURCE_TYPE,
        )

        if not changes:
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(RESOURCE_TYPE_FULL, name)
            )
            result["new_state"] = result["old_state"]
            return result

        changed_non_updatable_properties = (
            hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                RESOURCE_TYPE, changes
            )
        )
        if changed_non_updatable_properties:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    RESOURCE_TYPE_FULL,
                    name,
                    changed_non_updatable_properties,
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            return result

        # Perform update
        update_ret = await hub.exec.gcp_api.client.compute.health_check.update(
            hub,
            ctx,
            name=name,
            resource_id=resource_id,
            request_id=request_id,
            body=resource_body,
        )
        if not update_ret["result"] or not update_ret["ret"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(update_ret["ret"]):
            operation = update_ret["ret"]
    else:
        if ctx.get("test", False):
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.compute.health_check.insert(
            ctx,
            name=name,
            project=project,
            request_id=request_id,
            body=resource_body,
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and next(
                (
                    comment
                    for comment in create_ret["comment"]
                    if "alreadyExists" in comment
                ),
                None,
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret["ret"]):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.global_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of HealthCheck resources available to the specified project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.health_check
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.health_check.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe {RESOURCE_TYPE_FULL} {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            f"{RESOURCE_TYPE_FULL}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
