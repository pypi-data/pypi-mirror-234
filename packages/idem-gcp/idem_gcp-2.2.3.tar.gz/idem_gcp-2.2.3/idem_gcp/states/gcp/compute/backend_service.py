"""State module for managing Backend Services."""

__contracts__ = ["resource"]

from dataclasses import field
from dataclasses import make_dataclass
from typing import Dict, Any, List


async def present(
    hub,
    ctx,
    name: str,
    health_checks: List[str],
    load_balancing_scheme: str,
    protocol: str = None,
    project: str = None,
    timeout_sec: int = 30,
    port_name: str = None,
    fingerprint: str = None,
    locality_lb_policy: str = None,
    circuit_breakers: make_dataclass(
        "CircuitBreakers",
        [
            ("max_requests_per_connection", int, field(default=None)),
            ("max_connections", int, field(default=None)),
            ("max_requests", int, field(default=None)),
            ("max_retries", int, field(default=None)),
            ("max_pending_requests", int, field(default=None)),
        ],
    ) = None,
    failover_policy: make_dataclass(
        "BackendServiceFailoverPolicy",
        [
            ("drop_traffic_if_unhealthy", bool, field(default=None)),
            ("disable_connection_drain_on_failover", bool, field(default=None)),
            ("failover_ratio", float, field(default=None)),
        ],
    ) = None,
    port: int = None,
    network: str = None,
    cdn_policy: make_dataclass(
        "BackendServiceCdnPolicy",
        [
            ("request_coalescing", bool, field(default=None)),
            ("default_ttl", int, field(default=None)),
            (
                "bypass_cache_on_request_headers",
                List[
                    make_dataclass(
                        "BackendServiceCdnPolicyBypassCacheOnRequestHeader",
                        [("header_name", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("cache_mode", str, field(default=None)),
            ("client_ttl", int, field(default=None)),
            ("negative_caching", bool, field(default=None)),
            ("signed_url_cache_max_age_sec", str, field(default=None)),
            (
                "negative_caching_policy",
                List[
                    make_dataclass(
                        "BackendServiceCdnPolicyNegativeCachingPolicy",
                        [
                            ("ttl", int, field(default=None)),
                            ("code", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "cache_key_policy",
                make_dataclass(
                    "CacheKeyPolicy",
                    [
                        ("include_named_cookies", List[str], field(default=None)),
                        ("include_host", bool, field(default=None)),
                        ("include_protocol", bool, field(default=None)),
                        ("query_string_blacklist", List[str], field(default=None)),
                        ("include_query_string", bool, field(default=None)),
                        ("query_string_whitelist", List[str], field(default=None)),
                        ("include_http_headers", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("serve_while_stale", int, field(default=None)),
            ("max_ttl", int, field(default=None)),
            ("signed_url_key_names", List[str], field(default=None)),
        ],
    ) = None,
    log_config: make_dataclass(
        "BackendServiceLogConfig",
        [
            ("enable", bool, field(default=None)),
            ("sample_rate", float, field(default=None)),
        ],
    ) = None,
    security_settings: make_dataclass(
        "SecuritySettings",
        [
            ("client_tls_policy", str, field(default=None)),
            ("subject_alt_names", List[str], field(default=None)),
        ],
    ) = None,
    backends: List[
        make_dataclass(
            "Backend",
            [
                ("max_connections", int, field(default=None)),
                ("max_connections_per_instance", int, field(default=None)),
                ("max_rate_per_endpoint", float, field(default=None)),
                ("max_utilization", float, field(default=None)),
                ("max_rate", int, field(default=None)),
                ("capacity_scaler", float, field(default=None)),
                ("group", str, field(default=None)),
                ("balancing_mode", str, field(default=None)),
                ("failover", bool, field(default=None)),
                ("max_connections_per_endpoint", int, field(default=None)),
                ("description", str, field(default=None)),
                ("max_rate_per_instance", float, field(default=None)),
            ],
        )
    ] = None,
    max_stream_duration: make_dataclass(
        "Duration",
        [("nanos", int, field(default=None)), ("seconds", str, field(default=None))],
    ) = None,
    subsetting: make_dataclass(
        "Subsetting", [("policy", str, field(default=None))]
    ) = None,
    region: str = None,
    description: str = None,
    connection_draining: make_dataclass(
        "ConnectionDraining", [("draining_timeout_sec", int, field(default=None))]
    ) = None,
    outlier_detection: make_dataclass(
        "OutlierDetection",
        [
            ("consecutive_errors", int, field(default=None)),
            (
                "base_ejection_time",
                make_dataclass(
                    "Duration",
                    [
                        ("nanos", int, field(default=None)),
                        ("seconds", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("consecutive_gateway_failure", int, field(default=None)),
            ("enforcing_success_rate", int, field(default=None)),
            ("enforcing_consecutive_gateway_failure", int, field(default=None)),
            ("enforcing_consecutive_errors", int, field(default=None)),
            ("max_ejection_percent", int, field(default=None)),
            (
                "interval",
                make_dataclass(
                    "Duration",
                    [
                        ("nanos", int, field(default=None)),
                        ("seconds", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("success_rate_request_volume", int, field(default=None)),
            ("success_rate_stdev_factor", int, field(default=None)),
            ("success_rate_minimum_hosts", int, field(default=None)),
        ],
    ) = None,
    enable_cdn: bool = None,
    affinity_cookie_ttl_sec: int = None,
    connection_tracking_policy: make_dataclass(
        "BackendServiceConnectionTrackingPolicy",
        [
            ("idle_timeout_sec", int, field(default=None)),
            ("connection_persistence_on_unhealthy_backends", str, field(default=None)),
            ("enable_strong_affinity", bool, field(default=None)),
            ("tracking_mode", str, field(default=None)),
        ],
    ) = None,
    service_bindings: List[str] = None,
    compression_mode: str = None,
    consistent_hash: make_dataclass(
        "ConsistentHashLoadBalancerSettings",
        [
            (
                "http_cookie",
                make_dataclass(
                    "ConsistentHashLoadBalancerSettingsHttpCookie",
                    [
                        ("name", str, field(default=None)),
                        ("path", str, field(default=None)),
                        (
                            "ttl",
                            make_dataclass(
                                "Duration",
                                [
                                    ("nanos", int, field(default=None)),
                                    ("seconds", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            ("minimum_ring_size", str, field(default=None)),
            ("http_header_name", str, field(default=None)),
        ],
    ) = None,
    locality_lb_policies: List[
        make_dataclass(
            "BackendServiceLocalityLoadBalancingPolicyConfig",
            [
                (
                    "custom_policy",
                    make_dataclass(
                        "BackendServiceLocalityLoadBalancingPolicyConfigCustomPolicy",
                        [
                            ("name", str, field(default=None)),
                            ("data", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "policy",
                    make_dataclass(
                        "BackendServiceLocalityLoadBalancingPolicyConfigPolicy",
                        [("name", str, field(default=None))],
                    ),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    custom_request_headers: List[str] = None,
    iap: make_dataclass(
        "BackendServiceIAP",
        [
            ("oauth2_client_id", str, field(default=None)),
            ("oauth2_client_secret", str, field(default=None)),
            ("enabled", bool, field(default=None)),
            ("oauth2_client_secret_sha256", str, field(default=None)),
        ],
    ) = None,
    custom_response_headers: List[str] = None,
    session_affinity: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Create or update a compute backend service resource.

    Creates a BackendService resource in the specified project using the data included in the request. For more information, see Backend services overview .
    or
    Updates the specified BackendService resource with the data included in the request. For more information, see Backend services overview.

    Args:
        name(str):
            An Idem name of the resource.

        fingerprint(str, Optional):
            Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a BackendService. An up-to-date fingerprint must be provided in order to update the BackendService, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a BackendService. Defaults to None.

        health_checks(List[str], Optional):
            The list of URLs to the healthChecks, httpHealthChecks (legacy), or httpsHealthChecks (legacy) resource for health checking this backend service. Not all backend services support legacy health checks. See Load balancer guide. Currently, at most one health check can be specified for each backend service. Backend services with instance group or zonal NEG backends must have a health check. Backend services with internet or serverless NEG backends must not have a health check. Defaults to None.

        locality_lb_policy(str, Optional):
            The load balancing algorithm used within the scope of the locality. The possible values are: - ROUND_ROBIN: This is a simple policy in which each healthy backend is selected in round robin order. This is the default. - LEAST_REQUEST: An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - RING_HASH: The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - RANDOM: The load balancer selects a random healthy host. - ORIGINAL_DESTINATION: Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - MAGLEV: used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, see https://ai.google/research/pubs/pub44824 This field is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, or HTTP2, and load_balancing_scheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. If sessionAffinity is not NONE, and this field is not set to MAGLEV or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
            Enum type. Allowed values:
                "INVALID_LB_POLICY"
                "LEAST_REQUEST" - An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests.
                "MAGLEV" - This algorithm implements consistent hashing to backends. Maglev can be used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, see https://ai.google/research/pubs/pub44824
                "ORIGINAL_DESTINATION" - Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer.
                "RANDOM" - The load balancer selects a random healthy host.
                "RING_HASH" - The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests.
                "ROUND_ROBIN" - This is a simple policy in which each healthy backend is selected in round robin order. This is the default. Defaults to None.

        circuit_breakers(Dict[str, Any], Optional):
            CircuitBreakers: Settings controlling the volume of requests, connections and retries to this backend service. Defaults to None.

            * max_requests_per_connection(int, Optional):
                Maximum requests for a single connection to the backend service. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
            * max_connections(int, Optional):
                The maximum number of connections to the backend service. If not specified, there is no limit. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
            * max_requests (int, Optional):
                The maximum number of parallel requests that allowed to the backend service. If not specified, there is no limit.
            * max_retries (int, Optional):
                The maximum number of parallel retries allowed to the backend cluster. If not specified, the default is 1. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
            * max_pending_requests (int, Optional):
                The maximum number of pending requests allowed to the backend service. If not specified, there is no limit. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.

        failover_policy(Dict[str, Any], Optional):
            Requires at least one backend instance group to be defined as a backup (failover) backend. For load balancers that have configurable failover: [Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal/failover-overview) and [external TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-failover-overview).
            BackendServiceFailoverPolicy: For load balancers that have configurable failover: [Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal/failover-overview) and [external TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-failover-overview). On failover or failback, this field indicates whether connection draining will be honored. Google Cloud has a fixed connection draining timeout of 10 minutes. A setting of true terminates existing TCP connections to the active pool during failover and failback, immediately draining traffic. A setting of false allows existing TCP connections to persist, even on VMs no longer in the active pool, for up to the duration of the connection draining timeout (10 minutes). Defaults to None.

            * drop_traffic_if_unhealthy (bool, Optional):
                If set to true, connections to the load balancer are dropped when all primary and all backup backend VMs are unhealthy.If set to false, connections are distributed among all primary VMs when all primary and all backup backend VMs are unhealthy. For load balancers that have configurable failover: [Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal/failover-overview) and [external TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-failover-overview). The default is false.
            * disable_connection_drain_on_failover (bool, Optional):
                This can be set to true only if the protocol is TCP. The default is false.
            * failover_ratio (float, Optional):
                The value of the field must be in the range [0, 1]. If the value is 0, the load balancer performs a failover when the number of healthy primary VMs equals zero. For all other values, the load balancer performs a failover when the total number of healthy primary VMs is less than this ratio. For load balancers that have configurable failover: [Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal/failover-overview) and [external TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-failover-overview).

        protocol(str, Optional):
            The protocol this BackendService uses to communicate with backends. Possible values are HTTP, HTTPS, HTTP2, TCP, SSL, UDP or GRPC. depending on the chosen load balancer or Traffic Director configuration. Refer to the documentation for the load balancers or for Traffic Director for more information. Must be set to GRPC when the backend service is referenced by a URL map that is bound to target gRPC proxy.
            Enum type. Allowed values:
                "GRPC" - gRPC (available for Traffic Director).
                "HTTP"
                "HTTP2" - HTTP/2 with SSL.
                "HTTPS"
                "SSL" - TCP proxying with SSL.
                "TCP" - TCP proxying or TCP pass-through.
                "UDP" - UDP.
                "UNSPECIFIED" - If a Backend Service has UNSPECIFIED as its protocol, it can be used with any L3/L4 Forwarding Rules. Defaults to None.

        port(int, Optional): Deprecated in favor of portName. The TCP port to connect on the backend. The default value is 80. For Internal TCP/UDP Load Balancing and Network Load Balancing, omit port. Defaults to None.

        network(str, Optional): The URL of the network to which this backend service belongs. This field can only be specified when the load balancing scheme is set to INTERNAL. Defaults to None.

        cdn_policy(Dict[str, Any], Optional):
            Cloud CDN configuration for this BackendService. Only available for specified load balancer types.
            BackendServiceCdnPolicy: Message containing Cloud CDN configuration for a backend service. Defaults to None.

            * request_coalescing (bool, Optional):
                If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin.
            * default_ttl (int, Optional):
                Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Setting a TTL of "0" means "always revalidate". The value of defaultTTL cannot be set to a value greater than that of maxTTL, but can be equal. When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses. The maximum allowed value is 31,622,400s (1 year), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.
            * bypass_cache_on_request_headers (List[Dict[str, Any]], Optional):
                Bypass the cache when the specified request headers are matched - e.g. Pragma or Authorization headers. Up to 5 headers can be specified. The cache is bypassed for all cdnPolicy.cacheMode settings.

                * header_name (str, Optional):
                    The header field name to match on when bypassing cache. Values are case-insensitive.
            * cache_mode (str, Optional):
                Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS Requires the origin to set valid caching headers to cache content. Responses without these headers will not be cached at Google's edge, and will require a full trip to the origin on every request, potentially impacting performance and increasing load on the origin server. FORCE_CACHE_ALL Cache all content, ignoring any "private", "no-store" or "no-cache" directives in Cache-Control response headers. Warning: this may result in Cloud CDN caching private, per-user (user identifiable) content. CACHE_ALL_STATIC Automatically cache static content, including common image formats, media (video and audio), and web assets (JavaScript and CSS). Requests and responses that are marked as uncacheable, as well as dynamic content (including HTML), will not be cached.
                Enum type. Allowed values:
                    "CACHE_ALL_STATIC" - Automatically cache static content, including common image formats, media (video and audio), and web assets (JavaScript and CSS). Requests and responses that are marked as uncacheable, as well as dynamic content (including HTML), will not be cached.
                    "FORCE_CACHE_ALL" - Cache all content, ignoring any "private", "no-store" or "no-cache" directives in Cache-Control response headers. Warning: this may result in Cloud CDN caching private, per-user (user identifiable) content.
                    "INVALID_CACHE_MODE"
                    "USE_ORIGIN_HEADERS" - Requires the origin to set valid caching headers to cache content. Responses without these headers will not be cached at Google's edge, and will require a full trip to the origin on every request, potentially impacting performance and increasing load on the origin server.

            * client_ttl (int, Optional):
                Specifies a separate client (e.g. browser client) maximum TTL. This is used to clamp the max-age (or Expires) value sent to the client. With FORCE_CACHE_ALL, the lesser of client_ttl and default_ttl is used for the response max-age directive, along with a "public" directive. For cacheable content in CACHE_ALL_STATIC mode, client_ttl clamps the max-age from the origin (if specified), or else sets the response max-age directive to the lesser of the client_ttl and default_ttl, and also ensures a "public" cache-control directive is present. If a client TTL is not specified, a default value (1 hour) will be used. The maximum allowed value is 31,622,400s (1 year).
            * negative_caching (bool, Optional):
                Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. This can reduce the load on your origin and improve end-user experience by reducing response latency. When the cache mode is set to CACHE_ALL_STATIC or USE_ORIGIN_HEADERS, negative caching applies to responses with the specified response code that lack any Cache-Control, Expires, or Pragma: no-cache directives. When the cache mode is set to FORCE_CACHE_ALL, negative caching applies to all responses with the specified response code, and override any caching headers. By default, Cloud CDN will apply the following default TTLs to these status codes: HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s HTTP 405 (Method Not Found), 421 (Misdirected Request), 501 (Not Implemented): 60s. These defaults can be overridden in negative_caching_policy.
            * signed_url_cache_max_age_sec (str, Optional):
                Maximum number of seconds the response to a signed URL request will be considered fresh. After this time period, the response will be revalidated before being served. Defaults to 1hr (3600s). When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered.

            * negative_caching_policy (List[Dict[str, Any]], Optional):
                Sets a cache TTL for the specified HTTP status code. negative_caching must be enabled to configure negative_caching_policy. Omitting the policy and leaving negative_caching enabled will use Cloud CDN's default cache TTLs. Note that when specifying an explicit negative_caching_policy, you should take care to specify a cache TTL for all response codes that you wish to cache. Cloud CDN will not apply any default negative caching when a policy exists.

                * ttl (int, Optional):
                    The TTL (in seconds) for which to cache responses with the corresponding status code. The maximum allowed value is 1800s (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.
                * code (int, Optional):
                    The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 302, 307, 308, 404, 405, 410, 421, 451 and 501 are can be specified as values, and you cannot specify a status code more than once.
            * cache_key_policy (Dict[str, Any], Optional):
                The CacheKeyPolicy for this CdnPolicy.
                CacheKeyPolicy: Message containing what to include in the cache key for a request for Cloud CDN.

                    * include_named_cookies (List[str], Optional):
                        Allows HTTP cookies (by name) to be used in the cache key. The name=value pair will be used in the cache key Cloud CDN generates.
                    * include_host (bool, Optional):
                        If true, requests to different hosts will be cached separately.
                    * include_protocol (bool, Optional):
                        If true, http and https requests will be cached separately.
                    * query_string_blacklist (List[str], Optional):
                        Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters.
                    * include_query_string (bool, Optional):
                        If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely.
                    * query_string_whitelist (List[str], Optional):
                        Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters.
                    * include_http_headers (List[str], Optional):
                        Allows HTTP request headers (by name) to be used in the cache key.

            * serve_while_stale (int, Optional):
                Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. This setting defines the default "max-stale" duration for any cached responses that do not specify a max-stale directive. Stale responses that exceed the TTL configured here will not be served. The default limit (max-stale) is 86400s (1 day), which will allow stale content to be served up to this limit beyond the max-age (or s-max-age) of a cached response. The maximum allowed value is 604800 (1 week). Set this to zero (0) to disable serve-while-stale.
            * max_ttl (int, Optional):
                Specifies the maximum allowed TTL for cached content served by this origin. Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTTL seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive. Headers sent to the client will not be modified. Setting a TTL of "0" means "always revalidate". The maximum allowed value is 31,622,400s (1 year), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.
            * signed_url_key_names (List[str], Optional):
                [Output Only] Names of the keys for signing request URLs.

        log_config(Dict[str, Any], Optional):
            This field denotes the logging options for the load balancer traffic served by this backend service. If logging is enabled, logs will be exported to Stackdriver.
            BackendServiceLogConfig: The available logging options for the load balancer traffic served by this backend service. Defaults to None.

            * enable (bool, Optional):
                Denotes whether to enable logging for the load balancer traffic served by this backend service. The default value is false.
            * sample_rate (float, Optional):
                This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0.

        security_settings(Dict[str, Any], Optional):
            This field specifies the security settings that apply to this backend service. This field is applicable to a global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED.
            SecuritySettings: The authentication and authorization settings for a BackendService. Defaults to None.

            * client_tls_policy (str, Optional):
                Optional. A URL referring to a networksecurity.ClientTlsPolicy resource that describes how clients should authenticate with this service's backends. clientTlsPolicy only applies to a global BackendService with the loadBalancingScheme set to INTERNAL_SELF_MANAGED. If left blank, communications are not encrypted. Note: This field currently has no impact.
            * subject_alt_names (List[str], Optional):
                Optional. A list of Subject Alternative Names (SANs) that the client verifies during a mutual TLS handshake with an server/endpoint for this BackendService. When the server presents its X.509 certificate to the client, the client inspects the certificate's subjectAltName field. If the field contains one of the specified values, the communication continues. Otherwise, it fails. This additional check enables the client to verify that the server is authorized to run the requested service. Note that the contents of the server certificate's subjectAltName field are configured by the Public Key Infrastructure which provisions server identities. Only applies to a global BackendService with loadBalancingScheme set to INTERNAL_SELF_MANAGED. Only applies when BackendService has an attached clientTlsPolicy with clientCertificate (mTLS mode). Note: This field currently has no impact.

        backends(List[Dict[str, Any]], Optional):
            The list of backends that serve this BackendService. Defaults to None.

            * max_connections (int, Optional):
                Defines a target maximum number of simultaneous connections. For usage guidelines, see Connection balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is RATE.
            * max_connections_per_instance (int, Optional):
                Defines a target maximum number of simultaneous connections. For usage guidelines, see Connection balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is RATE.
            * max_rate_per_endpoint (float, Optional):
                Defines a maximum target for requests per second (RPS). For usage guidelines, see Rate balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is CONNECTION.
            * max_utilization (float, Optional):
                Optional parameter to define a target capacity for the UTILIZATION balancing mode. The valid range is [0.0, 1.0]. For usage guidelines, see Utilization balancing mode.
            * max_rate (int, Optional):
                Defines a maximum number of HTTP requests per second (RPS). For usage guidelines, see Rate balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is CONNECTION.
            * capacity_scaler (float, Optional):
                A multiplier applied to the backend's target capacity of its balancing mode. The default value is 1, which means the group serves up to 100% of its configured capacity (depending on balancingMode). A setting of 0 means the group is completely drained, offering 0% of its available capacity. The valid ranges are 0.0 and [0.1,1.0]. You cannot configure a setting larger than 0 and smaller than 0.1. You cannot configure a setting of 0 when there is only one backend attached to the backend service.
            * group (str, Optional):
                The fully-qualified URL of an instance group or network endpoint group (NEG) resource. To determine what types of backends a load balancer supports, see the [Backend services overview](https://cloud.google.com/load-balancing/docs/backend-service#backends). You must use the *fully-qualified* URL (starting with https://www.googleapis.com/) to specify the instance group or NEG. Partial URLs are not supported.
            * balancing_mode (str, Optional):
                Specifies how to determine whether the backend of a load balancer can handle additional traffic or is fully loaded. For usage guidelines, see Connection balancing mode. Backends must use compatible balancing modes. For more information, see Supported balancing modes and target capacity settings and Restrictions and guidance for instance groups. Note: Currently, if you use the API to configure incompatible balancing modes, the configuration might be accepted even though it has no impact and is ignored. Specifically, Backend.maxUtilization is ignored when Backend.balancingMode is RATE. In the future, this incompatible combination will be rejected.
                Enum type. Allowed values:
                    "CONNECTION" - Balance based on the number of simultaneous connections.
                    "RATE" - Balance based on requests per second (RPS).
                    "UTILIZATION" - Balance based on the backend utilization.

            * failover (bool, Optional):
                This field designates whether this is a failover backend. More than one failover backend can be configured for a given BackendService.
            * max_connections_per_endpoint (int, Optional):
                Defines a target maximum number of simultaneous connections. For usage guidelines, see Connection balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is RATE.
            * description (str, Optional):
                An optional description of this resource. Provide this property when you create the resource.
            * max_rate_per_instance (float, Optional):
                Defines a maximum target for requests per second (RPS). For usage guidelines, see Rate balancing mode and Utilization balancing mode. Not available if the backend's balancingMode is CONNECTION.

        max_stream_duration(Dict[str, Any], Optional):
            Specifies the default maximum duration (timeout) for streams to this service. Duration is computed from the beginning of the stream until the response has been completely processed, including all retries. A stream that does not complete in this duration is closed. If not specified, there will be no timeout limit, i.e. the maximum duration is infinite. This value can be overridden in the PathMatcher configuration of the UrlMap that references this backend service. This field is only allowed when the loadBalancingScheme of the backend service is INTERNAL_SELF_MANAGED.
            Duration: A Duration represents a fixed-length span of time represented as a count of seconds and fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month". Range is approximately 10,000 years. Defaults to None.

            * nanos (int, Optional):
                Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 `seconds` field and a positive `nanos` field. Must be from 0 to 999,999,999 inclusive.
            * seconds (str, Optional):
                Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Note: these bounds are computed from: 60 sec/min * 60 min/hr * 24 hr/day * 365.25 days/year * 10000 years

        subsetting(Dict[str, Any], Optional):
            Subsetting: Subsetting configuration for this BackendService. Currently this is applicable only for Internal TCP/UDP load balancing, Internal HTTP(S) load balancing and Traffic Director. Defaults to None.

            * policy (str, Optional):
                Enum type. Allowed values:
                    "CONSISTENT_HASH_SUBSETTING" - Subsetting based on consistent hashing. For Traffic Director, the number of backends per backend group (the subset size) is based on the `subset_size` parameter. For Internal HTTP(S) load balancing, the number of backends per backend group (the subset size) is dynamically adjusted in two cases: - As the number of proxy instances participating in Internal HTTP(S) load balancing increases, the subset size decreases. - When the total number of backends in a network exceeds the capacity of a single proxy instance, subset sizes are reduced automatically for each service that has backend subsetting enabled.
                    "NONE" - No Subsetting. Clients may open connections and send traffic to all backends of this backend service. This can lead to performance issues if there is substantial imbalance in the count of clients and backends.

        region(str, Optional): The region where the regional backend service resides.

        description(str, Optional): An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        timeout_sec(int, Optional): The backend service timeout has a different meaning depending on the type of load balancer. For more information see, Backend service settings. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. This value can be overridden in the PathMatcher configuration of the UrlMap that references this backend service. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true. Instead, use maxStreamDuration. Defaults to None.

        connection_draining(Dict[str, Any], Optional):
            ConnectionDraining: Message containing connection draining configuration. Defaults to None.

            * draining_timeout_sec (int, Optional):
                Configures a duration timeout for existing requests on a removed backend instance. For supported load balancers and protocols, as described in Enabling connection draining.

        outlier_detection(Dict[str, Any], Optional):
                Settings controlling the eviction of unhealthy hosts from the load balancing pool for the backend service. If not set, this feature is considered disabled. This field is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2, or GRPC, and load_balancing_scheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED.
                OutlierDetection: Settings controlling the eviction of unhealthy hosts from the load balancing pool for the backend service. Defaults to None.

                * consecutive_errors (int, Optional):
                    Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
                * base_ejection_time (Dict[str, Any], Optional):
                    The base time that a host is ejected for. The real ejection time is equal to the base ejection time multiplied by the number of times the host has been ejected. Defaults to 30000ms or 30s.
                    Duration: A Duration represents a fixed-length span of time represented as a count of seconds and fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month". Range is approximately 10,000 years.

                    * nanos (int, Optional):
                        Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 `seconds` field and a positive `nanos` field. Must be from 0 to 999,999,999 inclusive.
                    * seconds (str, Optional):
                        Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Note: these bounds are computed from: 60 sec/min * 60 min/hr * 24 hr/day * 365.25 days/year * 10000 years
                * consecutive_gateway_failure (int, Optional):
                    The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 3. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
                * enforcing_success_rate (int, Optional):
                    The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100.
                * enforcing_consecutive_gateway_failure (int, Optional):
                    The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
                * enforcing_consecutive_errors (int, Optional):
                    The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
                * max_ejection_percent (int, Optional):
                    Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 50%.
                * interval (Dict[str, Any], Optional):
                    Time interval between ejection analysis sweeps. This can result in both new ejections as well as hosts being returned to service. Defaults to 1 second.
                    Duration: A Duration represents a fixed-length span of time represented as a count of seconds and fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month". Range is approximately 10,000 years.

                    * nanos (int, Optional):
                        Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 `seconds` field and a positive `nanos` field. Must be from 0 to 999,999,999 inclusive.
                    * seconds (str, Optional):
                        Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Note: these bounds are computed from: 60 sec/min * 60 min/hr * 24 hr/day * 365.25 days/year * 10000 years
                * success_rate_request_volume (int, Optional):
                    The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100.
                * success_rate_stdev_factor (int, Optional):
                    This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900.
                * success_rate_minimum_hosts (int, Optional):
                    The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5.

        enable_cdn(bool, Optional): If true, enables Cloud CDN for the backend service of an external HTTP(S) load balancer. Defaults to None.

        affinity_cookie_ttl_sec(int, Optional): Lifetime of cookies in seconds. This setting is applicable to external and internal HTTP(S) load balancers and Traffic Director and requires GENERATED_COOKIE or HTTP_COOKIE session affinity. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value is two weeks (1,209,600). Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true. Defaults to None.

        connection_tracking_policy(Dict[str, Any], Optional):
            Connection Tracking configuration for this BackendService. Connection tracking policy settings are only available for Network Load Balancing and Internal TCP/UDP Load Balancing.
            BackendServiceConnectionTrackingPolicy: Connection Tracking configuration for this BackendService. Defaults to None.

            * idle_timeout_sec (int, Optional):
                Specifies how long to keep a Connection Tracking entry while there is no matching traffic (in seconds). For Internal TCP/UDP Load Balancing: - The minimum (default) is 10 minutes and the maximum is 16 hours. - It can be set only if Connection Tracking is less than 5-tuple (i.e. Session Affinity is CLIENT_IP_NO_DESTINATION, CLIENT_IP or CLIENT_IP_PROTO, and Tracking Mode is PER_SESSION). For Network Load Balancer the default is 60 seconds. This option is not available publicly.
            * connection_persistence_on_unhealthy_backends (str, Optional):
                Specifies connection persistence when backends are unhealthy. The default value is DEFAULT_FOR_PROTOCOL. If set to DEFAULT_FOR_PROTOCOL, the existing connections persist on unhealthy backends only for connection-oriented protocols (TCP and SCTP) and only if the Tracking Mode is PER_CONNECTION (default tracking mode) or the Session Affinity is configured for 5-tuple. They do not persist for UDP. If set to NEVER_PERSIST, after a backend becomes unhealthy, the existing connections on the unhealthy backend are never persisted on the unhealthy backend. They are always diverted to newly selected healthy backends (unless all backends are unhealthy). If set to ALWAYS_PERSIST, existing connections always persist on unhealthy backends regardless of protocol and session affinity. It is generally not recommended to use this mode overriding the default. For more details, see [Connection Persistence for Network Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-backend-service#connection-persistence) and [Connection Persistence for Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal#connection-persistence).
                Enum type. Allowed values:
                    "ALWAYS_PERSIST"
                    "DEFAULT_FOR_PROTOCOL"
                    "NEVER_PERSIST"

            * enable_strong_affinity (bool, Optional):
                Enable Strong Session Affinity for Network Load Balancing. This option is not available publicly.
            * tracking_mode (str, Optional):
                Specifies the key used for connection tracking. There are two options: - PER_CONNECTION: This is the default mode. The Connection Tracking is performed as per the Connection Key (default Hash Method) for the specific protocol. - PER_SESSION: The Connection Tracking is performed as per the configured Session Affinity. It matches the configured Session Affinity. For more details, see [Tracking Mode for Network Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-backend-service#tracking-mode) and [Tracking Mode for Internal TCP/UDP Load Balancing](https://cloud.google.com/load-balancing/docs/internal#tracking-mode).
                Enum type. Allowed values:
                    "INVALID_TRACKING_MODE"
                    "PER_CONNECTION"
                    "PER_SESSION"

        service_bindings(List[str], Optional): URLs of networkservices.ServiceBinding resources. Can only be set if load balancing scheme is INTERNAL_SELF_MANAGED. If set, lists of backends and health checks must be both empty. Defaults to None.

        load_balancing_scheme(str, Optional):
            Specifies the load balancer type. A backend service created for one type of load balancer cannot be used with another. For more information, refer to Choosing a load balancer.
            Enum type. Allowed values:
                "EXTERNAL" - Signifies that this will be used for external HTTP(S), SSL Proxy, TCP Proxy, or Network Load Balancing
                "EXTERNAL_MANAGED" - Signifies that this will be used for External Managed HTTP(S) Load Balancing.
                "INTERNAL" - Signifies that this will be used for Internal TCP/UDP Load Balancing.
                "INTERNAL_MANAGED" - Signifies that this will be used for Internal HTTP(S) Load Balancing.
                "INTERNAL_SELF_MANAGED" - Signifies that this will be used by Traffic Director.
                "INVALID_LOAD_BALANCING_SCHEME". Defaults to None.

        compression_mode(str, Optional):
            Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header.
            Enum type. Allowed values:
                "AUTOMATIC" - Automatically uses the best compression based on the Accept-Encoding header sent by the client.
                "DISABLED" - Disables compression. Existing compressed responses cached by Cloud CDN will not be served to clients. Defaults to None.

        consistent_hash(Dict[str, Any], Optional):
            Consistent Hash-based load balancing can be used to provide soft session affinity based on HTTP headers, cookies or other properties. This load balancing policy is applicable only for HTTP connections. The affinity to a particular destination host will be lost when one or more hosts are added/removed from the destination service. This field specifies parameters that control consistent hashing. This field is only applicable when localityLbPolicy is set to MAGLEV or RING_HASH. This field is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, or HTTP2, and load_balancing_scheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED.
            ConsistentHashLoadBalancerSettings: This message defines settings for a consistent hash style load balancer. Defaults to None.

            * http_cookie (Dict[str, Any], Optional):
                Hash is based on HTTP Cookie. This field describes a HTTP cookie that will be used as the hash key for the consistent hash load balancer. If the cookie is not present, it will be generated. This field is applicable if the sessionAffinity is set to HTTP_COOKIE. Not supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true.
                ConsistentHashLoadBalancerSettingsHttpCookie: The information about the HTTP Cookie on which the hash function is based for load balancing policies that use a consistent hash.

                * name (str, Optional):
                    Name of the cookie.
                * path (str, Optional):
                    Path to set for the cookie.
                * ttl (Dict[str, Any], Optional):
                    Lifetime of the cookie.
                    Duration: A Duration represents a fixed-length span of time represented as a count of seconds and fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month". Range is approximately 10,000 years.

                    * nanos (int, Optional):
                        Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 `seconds` field and a positive `nanos` field. Must be from 0 to 999,999,999 inclusive.
                    * seconds (str, Optional):
                        Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Note: these bounds are computed from: 60 sec/min * 60 min/hr * 24 hr/day * 365.25 days/year * 10000 years
            * minimum_ring_size (str, Optional): The minimum number of virtual nodes to use for the hash ring. Defaults to 1024. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node.
            * http_header_name (str, Optional): The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD.

        locality_lb_policies(List[Dict[str, Any]], Optional):
            A list of locality load balancing policies to be used in order of preference. Either the policy or the customPolicy field should be set. Overrides any value set in the localityLbPolicy field. localityLbPolicies is only supported when the BackendService is referenced by a URL Map that is referenced by a target gRPC proxy that has the validateForProxyless field set to true. Defaults to None.

            * custom_policy (Dict[str, Any], Optional):
             BackendServiceLocalityLoadBalancingPolicyConfigCustomPolicy: The configuration for a custom policy implemented by the user and deployed with the client.
                * name (str, Optional):
                    Identifies the custom policy. The value should match the type the custom implementation is registered with on the gRPC clients. It should follow protocol buffer message naming conventions and include the full path (e.g. myorg.CustomLbPolicy). The maximum length is 256 characters. Note that specifying the same custom policy more than once for a backend is not a valid configuration and will be rejected.
                * data (str, Optional):
                    An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation.
            * policy (Dict[str, Any], Optional):
                BackendServiceLocalityLoadBalancingPolicyConfigPolicy: The configuration for a built-in load balancing policy.
                * name (str, Optional):
                    The name of a locality load balancer policy to be used. The value should be one of the predefined ones as supported by localityLbPolicy, although at the moment only ROUND_ROBIN is supported. This field should only be populated when the customPolicy field is not used. Note that specifying the same policy more than once for a backend is not a valid configuration and will be rejected.
                    Enum type. Allowed values:
                        "INVALID_LB_POLICY"
                        "LEAST_REQUEST" - An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests.
                        "MAGLEV" - This algorithm implements consistent hashing to backends. Maglev can be used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, see https://ai.google/research/pubs/pub44824
                        "ORIGINAL_DESTINATION" - Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer.
                        "RANDOM" - The load balancer selects a random healthy host.
                        "RING_HASH" - The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests.
                        "ROUND_ROBIN" - This is a simple policy in which each healthy backend is selected in round robin order. This is the default.

        custom_request_headers(List[str], Optional): Headers that the load balancer adds to proxied requests. See [Creating custom headers](https://cloud.google.com/load-balancing/docs/custom-headers). Defaults to None.

        iap(Dict[str, Any], Optional):
            The configurations for Identity-Aware Proxy on this resource. Not available for Internal TCP/UDP Load Balancing and Network Load Balancing.
            BackendServiceIAP: Identity-Aware Proxy. Defaults to None.

            * oauth2_client_id (str, Optional):
                OAuth2 client ID to use for the authentication flow.
            * oauth2_client_secret (str, Optional):
                OAuth2 client secret to use for the authentication flow. For security reasons, this value cannot be retrieved via the API. Instead, the SHA-256 hash of the value is returned in the oauth2ClientSecretSha256 field. @InputOnly
            * enabled (bool, Optional):
                Whether the serving infrastructure will authenticate and authorize all incoming requests. If true, the oauth2ClientId and oauth2ClientSecret fields must be non-empty.
            * oauth2_client_secret_sha256 (str, Optional):
                [Output Only] SHA256 hash value for the field oauth2_client_secret above.

        custom_response_headers(List[str], Optional): Headers that the load balancer adds to proxied responses. See [Creating custom headers](https://cloud.google.com/load-balancing/docs/custom-headers). Defaults to None.

        port_name(str, Optional): A named port on a backend instance group representing the port for communication to the backend VMs in that group. The named port must be [defined on each backend instance group](https://cloud.google.com/load-balancing/docs/backend-service#named_ports). This parameter has no meaning if the backends are NEGs. For Internal TCP/UDP Load Balancing and Network Load Balancing, omit port_name. Defaults to None.

        session_affinity(str, Optional):
            Type of session affinity to use. The default is NONE. Only NONE and HEADER_FIELD are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validateForProxyless field set to true. For more details, see: [Session Affinity](https://cloud.google.com/load-balancing/docs/backend-service#session_affinity).
            Enum type. Allowed values:
                "CLIENT_IP" - 2-tuple hash on packet's source and destination IP addresses. Connections from the same source IP address to the same destination IP address will be served by the same backend VM while that VM remains healthy.
                "CLIENT_IP_NO_DESTINATION" - 1-tuple hash only on packet's source IP address. Connections from the same source IP address will be served by the same backend VM while that VM remains healthy. This option can only be used for Internal TCP/UDP Load Balancing.
                "CLIENT_IP_PORT_PROTO" - 5-tuple hash on packet's source and destination IP addresses, IP protocol, and source and destination ports. Connections for the same IP protocol from the same source IP address and port to the same destination IP address and port will be served by the same backend VM while that VM remains healthy. This option cannot be used for HTTP(S) load balancing.
                "CLIENT_IP_PROTO" - 3-tuple hash on packet's source and destination IP addresses, and IP protocol. Connections for the same IP protocol from the same source IP address to the same destination IP address will be served by the same backend VM while that VM remains healthy. This option cannot be used for HTTP(S) load balancing.
                "GENERATED_COOKIE" - Hash based on a cookie generated by the L7 loadbalancer. Only valid for HTTP(S) load balancing.
                "HEADER_FIELD" - The hash is based on a user specified header field.
                "HTTP_COOKIE" - The hash is based on a user provided cookie.
                "NONE" - No session affinity. Connections from the same client IP may go to any instance in the pool. Defaults to None.

        request_id(str, Optional): An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str): Project ID for this request.

        backend_service(str): Name of the BackendService resource to return.

        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.compute.backend_services.present:
                - name: backend-service-name
                - region: us-central1
                - health_checks:
                  - https://www.googleapis.com/compute/v1/projects/gcp-project/global/healthChecks/healthcheck-name
                - load_balancing_scheme: INTERNAL_MANAGED
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if ctx.get("wrapper_result"):
        result = ctx.get("wrapper_result")

    # to be autogenerated by pop-create based on insert/update props in properties.yaml
    resource_body = {
        "compression_mode": compression_mode,
        "service_bindings": service_bindings,
        "max_stream_duration": max_stream_duration,
        "port": port,
        "log_config": log_config,
        "consistent_hash": consistent_hash,
        "session_affinity": session_affinity,
        "connection_tracking_policy": connection_tracking_policy,
        "locality_lb_policies": locality_lb_policies,
        "name": name,
        "timeout_sec": timeout_sec,
        "iap": iap,
        "custom_response_headers": custom_response_headers,
        "load_balancing_scheme": load_balancing_scheme,
        "description": description,
        "cdn_policy": cdn_policy,
        "connection_draining": connection_draining,
        "enable_cdn": enable_cdn,
        "backends": backends,
        "locality_lb_policy": locality_lb_policy,
        "circuit_breakers": circuit_breakers,
        "custom_request_headers": custom_request_headers,
        "outlier_detection": outlier_detection,
        "failover_policy": failover_policy,
        "affinity_cookie_ttl_sec": affinity_cookie_ttl_sec,
        "protocol": protocol,
        "subsetting": subsetting,
        "port_name": port_name,
        "network": network,
        "security_settings": security_settings,
        "health_checks": health_checks,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        # The fingerprint is required upon an update operation but in the time of creation the
        # resource still do not have fingerprint so, we cannot make it a required param for present method.
        resource_body["fingerprint"] = fingerprint or result["old_state"].get(
            "fingerprint"
        )
        # Output only property. Shouldn't be changed.
        resource_body["region"] = region or result["old_state"].get("region")
        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            {"resource_id": resource_id, **resource_body},
            "compute.backend_service",
        )

        if changes:
            changed_non_updatable_properties = (
                hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                    "compute.backend_service", changes
                )
            )
            if changed_non_updatable_properties:
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.compute.backend_service",
                        name,
                        changed_non_updatable_properties,
                    )
                )
                result["new_state"] = result["old_state"]
                return result

        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.backend_service", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.backend_service", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        if changes:
            update_ret = (
                await hub.exec.gcp_api.client.compute.region_backend_service.update(
                    hub,
                    ctx,
                    resource_id=resource_id,
                    request_id=request_id,
                    body=resource_body,
                )
            )

            if not update_ret["result"] or not update_ret["ret"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            if hub.tool.gcp.operation_utils.is_operation(update_ret["ret"]):
                operation = update_ret["ret"]
    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.backend_service", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        # Create
        create_ret = (
            await hub.exec.gcp_api.client.compute.region_backend_service.insert(
                ctx,
                name=name,
                project=project,
                region=region,
                request_id=request_id,
                body=resource_body,
            )
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and any(
                "alreadyExists" in c for c in create_ret["comment"]
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        "gcp.compute.backend_service", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret["ret"]):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.region_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }
        return result

    return result


async def absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified BackendService resource.

    Args:
        name(str):
            An Idem name of the resource.
        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        project(str):
            Project ID for this request.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              gcp.compute.backend_services.absent:
                - name: value
                - region: value
                - project: value
    """
    result = {
        "result": True,
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "comment": [],
    }

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if not resource_id and not hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    ):
        resource_id = (ctx.get("old_state") or {}).get(
            "resource_id"
        ) or hub.tool.gcp.resource_prop_utils.construct_resource_id(
            "compute.backend_service", {**locals(), "backendService": name}
        )

    if not resource_id:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                "gcp.compute.backend_service", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        get_ret = await hub.exec.gcp.compute.backend_service.get(
            ctx, resource_id=resource_id
        )

        if not get_ret["result"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        if not get_ret["ret"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_absent_comment(
                    "gcp.compute.backend_service", name
                )
            )
            return result

        result["old_state"] = get_ret["ret"]

    if ctx["test"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.compute.backend_service", name
            )
        )
        return result

    if not ctx.get("rerun_data"):
        delete_ret = (
            await hub.exec.gcp_api.client.compute.region_backend_service.delete(
                ctx, resource_id=resource_id, request_id=request_id
            )
        )
        if not delete_ret.get(
            "result"
        ) or not hub.tool.gcp.operation_utils.is_operation(delete_ret.get("ret")):
            result["result"] = False
            result["comment"].append(
                f"Unexpected return value from gcp.compute.region_backend_service.delete - {delete_ret}"
            )
            return result

        result["result"] = True
        result["comment"] += delete_ret["comment"]
        result["rerun_data"] = {
            "operation_id": hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                delete_ret["ret"].get("selfLink"),
                "compute.region_operation",
            ),
        }
        return result
    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.backend_service"
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

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment("gcp.compute.backend_service", name)
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of BackendService resources available to the specified project.

    Args:
        return_partial_success(bool, Optional): Opt-in for partial success behavior which provides partial results in case of failure. The default value is false. Defaults to None.
        include_all_scopes(bool, Optional): Indicates whether every visible scope for each scope type (zone, region, global) should be included in the response. For new resource types added after this field, the flag has no effect as new resource types will always include every visible scope for each scope type in response. For resource types which predate this field, if this flag is omitted or false, only scopes of the scope types where the resource type is expected to be found will be included. Defaults to None.
        project(str): Project ID for this request.
        max_results(int, Optional): The maximum number of results per page that should be returned. If the number of available results is larger than `maxResults`, Compute Engine returns a `nextPageToken` that can be used to get the next page of results in subsequent list requests. Acceptable values are `0` to `500`, inclusive. (Default: `500`). Defaults to 500.
        filter(str, Optional): A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = "Intel Skylake") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = "Intel Skylake") OR (cpuPlatform = "Intel Broadwell") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq "double quoted literal"` `(fieldname1 eq literal) (fieldname2 ne "literal")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`. Defaults to None.
        page_token(str, Optional): Specifies a page token to use. Set `pageToken` to the `nextPageToken` returned by a previous list request to get the next page of results. Defaults to None.
        order_by(str, Optional): Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy="creationTimestamp desc"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported. Defaults to None.
        backend_service(str): Name of the BackendService resource to return.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.backend_service
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.backend_service.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe backend services {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        if resource_id:
            result[resource_id] = {
                "gcp.compute.backend_service.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource.items()
                ]
            }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
