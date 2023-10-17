"""State module for managing Buckets."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

RESOURCE_TYPE_SIMPLE = "storage.bucket"
RESOURCE_TYPE_FULL = f"gcp.{RESOURCE_TYPE_SIMPLE}"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    project: str = None,
    predefined_acl: str = None,
    predefined_default_object_acl: str = None,
    user_project: str = None,
    billing: make_dataclass(
        "BillingProperties",
        [("requester_pays", bool, field(default=None))],
    ) = None,
    cors: List[
        make_dataclass(
            "CorsProperties",
            [
                ("max_age_seconds", int, field(default=None)),
                ("method", List[str], field(default=None)),
                ("origin", List[str], field(default=None)),
                ("response_header", List[str], field(default=None)),
            ],
        )
    ] = None,
    custom_placement_config: make_dataclass(
        "CustomPlacementConfigProperties",
        [("data_locations", List[str], field(default=None))],
    ) = None,
    default_event_based_hold: bool = None,
    encryption: make_dataclass(
        "EncryptionProperties",
        [("default_kms_key_name", str, field(default=None))],
    ) = None,
    iam_configuration: make_dataclass(
        "IamConfigurationProperties",
        [
            (
                "bucket_policy_only",
                make_dataclass(
                    "BucketPolicyOnlyProperties",
                    [
                        ("enabled", bool, field(default=None)),
                        ("locked_time", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "uniform_bucket_level_access",
                make_dataclass(
                    "UniformBucketLevelAccessProperties",
                    [
                        ("enabled", bool, field(default=None)),
                        ("locked_time", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("public_access_prevention", str, field(default=None)),
        ],
    ) = None,
    labels: Dict[str, Any] = None,
    lifecycle: make_dataclass(
        "LifecycleProperties",
        [
            (
                "rule",
                List[
                    make_dataclass(
                        "RuleProperties",
                        [
                            (
                                "action",
                                make_dataclass(
                                    "ActionProperties",
                                    [
                                        ("storage_class", str, field(default=None)),
                                        (
                                            "type_",
                                            (str, "alias=type"),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "condition",
                                make_dataclass(
                                    "ConditionProperties",
                                    [
                                        ("age", int, field(default=None)),
                                        ("created_before", str, field(default=None)),
                                        (
                                            "custom_time_before",
                                            str,
                                            field(default=None),
                                        ),
                                        (
                                            "days_since_custom_time",
                                            int,
                                            field(default=None),
                                        ),
                                        (
                                            "days_since_noncurrent_time",
                                            int,
                                            field(default=None),
                                        ),
                                        ("is_live", bool, field(default=None)),
                                        ("matches_pattern", str, field(default=None)),
                                        (
                                            "matches_prefix",
                                            List[str],
                                            field(default=None),
                                        ),
                                        (
                                            "matches_suffix",
                                            List[str],
                                            field(default=None),
                                        ),
                                        (
                                            "matches_storage_class",
                                            List[str],
                                            field(default=None),
                                        ),
                                        (
                                            "noncurrent_time_before",
                                            str,
                                            field(default=None),
                                        ),
                                        (
                                            "num_newer_versions",
                                            int,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
                field(default=None),
            )
        ],
    ) = None,
    autoclass: make_dataclass(
        "AutoclassProperties",
        [
            ("enabled", bool, field(default=None)),
        ],
    ) = None,
    location: str = None,
    logging: make_dataclass(
        "LoggingProperties",
        [
            ("log_bucket", str, field(default=None)),
            ("log_object_prefix", str, field(default=None)),
        ],
    ) = None,
    retention_policy: make_dataclass(
        "RetentionPolicyProperties",
        [
            ("retention_period", str, field(default=None)),
            ("is_locked", bool, field(default=None)),
        ],
    ) = None,
    rpo: str = None,
    storage_class: str = None,
    versioning: make_dataclass(
        "VersioningProperties",
        [("enabled", bool, field(default=None))],
    ) = None,
    website: make_dataclass(
        "WebsiteProperties",
        [
            ("main_page_suffix", str, field(default=None)),
            ("not_found_page", str, field(default=None)),
        ],
    ) = None,
    metageneration: str = None,
    if_metageneration_match: str = None,
    acl: List[
        make_dataclass(
            "BucketAccessControl",
            [
                ("bucket", str, field(default=None)),
                ("domain", str, field(default=None)),
                ("email", str, field(default=None)),
                ("entity", str, field(default=None)),
                ("entity_id", str, field(default=None)),
                ("etag", str, field(default=None)),
                ("id", str, field(default=None)),
                ("kind", str, field(default=None)),
                (
                    "project_team",
                    make_dataclass(
                        "ProjectTeam",
                        [
                            ("project_number", str, field(default=None)),
                            ("team", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("role", str, field(default=None)),
                ("self_link", str, field(default=None)),
            ],
        )
    ] = None,
    default_object_acl: List[
        make_dataclass(
            "ObjectAccessControl",
            [
                ("domain", str, field(default=None)),
                ("email", str, field(default=None)),
                ("entity", str, field(default=None)),
                ("entity_id", str, field(default=None)),
                ("etag", str, field(default=None)),
                ("kind", str, field(default=None)),
                (
                    "project_team",
                    make_dataclass(
                        "ProjectTeam",
                        [
                            ("project_number", str, field(default=None)),
                            ("team", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("role", str, field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    r"""Create or update a storage bucket resource.

    Changes to the bucket will be readable immediately after writing, but configuration changes may take time to propagate.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        project(str):
            A valid API project identifier.

        predefined_acl(str, Optional):
            Apply a predefined set of access controls to this bucket. Defaults to None.

        predefined_default_object_acl(str, Optional):
            Apply a predefined set of default object access controls to this bucket. Defaults to None.

        user_project(str, Optional):
            The project to be billed for this request. Required for Requester Pays buckets. Defaults to None.

        billing(Dict[str, Any], Optional):
            The bucket's billing configuration. Defaults to None.

            * requester_pays(bool, Optional):
                When set to true, Requester Pays is enabled for this bucket.

        cors(List[Dict[str, Any]], Optional):
            The bucket's Cross-Origin Resource Sharing (CORS) configuration. Defaults to None.

            * max_age_seconds(int, Optional):
                The value, in seconds, to return in the  Access-Control-Max-Age header used in preflight responses.
            * method(List[str], Optional):
                The list of HTTP methods on which to include CORS response headers, (GET, OPTIONS, POST, etc) Note: "*" is permitted in the list of methods, and means "any method".
            * origin(List[str], Optional):
                The list of Origins eligible to receive CORS response headers. Note: "*" is permitted in the list of origins, and means "any Origin".
            * response_header(List[str], Optional):
                The list of HTTP headers other than the simple response headers to give permission for the user-agent to share across domains.

        custom_placement_config(Dict[str, Any], Optional):
            The bucket's custom placement configuration for Custom Dual Regions. Defaults to None.

            * data_locations(List[str], Optional):
                The list of regional locations in which data is placed.

        default_event_based_hold(bool, Optional):
            The default value for event-based hold on newly created objects in this bucket. Event-based hold is a way to retain objects indefinitely until an event occurs, signified by the hold's release. After being released, such objects will be subject to bucket-level retention (if any). One sample use case of this flag is for banks to hold loan documents for at least 3 years after loan is paid in full. Here, bucket-level retention is 3 years and the event is loan being paid in full. In this example, these objects will be held intact for any number of years until the event has occurred (event-based hold on the object is released) and then 3 more years after that. That means retention duration of the objects begins from the moment event-based hold transitioned from true to false. Objects under event-based hold cannot be deleted, overwritten or archived until the hold is removed. Defaults to None.

        encryption(Dict[str, Any], Optional):
            Encryption configuration for a bucket. Defaults to None.

            * default_kms_key_name(str, Optional):
                A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified.

        iam_configuration(Dict[str, Any], Optional):
            The bucket's IAM configuration. Defaults to None.

            * bucket_policy_only(Dict[str, Any], Optional):
                The bucket's uniform bucket-level access configuration. The feature was formerly known as Bucket Policy Only. For backward compatibility, this field will be populated with identical information as the uniformBucketLevelAccess field. We recommend using the uniformBucketLevelAccess field to enable and disable the feature.

                * enabled(bool, Optional):
                    If set, access is controlled only by bucket-level or above IAM policies.
                * locked_time(str, Optional):
                    The deadline for changing iamConfiguration.bucketPolicyOnly.enabled from true to false in RFC 3339 format. iamConfiguration.bucketPolicyOnly.enabled may be changed from true to false until the locked time, after which the field is immutable.
            * uniform_bucket_level_access(Dict[str, Any], Optional):
                The bucket's uniform bucket-level access configuration.

                * enabled(bool, Optional):
                    If set, access is controlled only by bucket-level or above IAM policies.
                * locked_time(str, Optional):
                    The deadline for changing iamConfiguration.uniformBucketLevelAccess.enabled from true to false in RFC 3339  format. iamConfiguration.uniformBucketLevelAccess.enabled may be changed from true to false until the locked time, after which the field is immutable.
            * public_access_prevention(str, Optional):
                The bucket's Public Access Prevention configuration. Currently, 'inherited' and 'enforced' are supported.

        labels(Dict[str, Any], Optional):
            User-provided labels, in key/value pairs. Defaults to None.

        lifecycle(Dict[str, Any], Optional):
            The bucket's lifecycle configuration. See lifecycle management for more information. Defaults to None.

            * rule(List[Dict[str, Any]], Optional):
                A lifecycle management rule, which is made of an action to take and the condition(s) under which the action will be taken.

                * action(Dict[str, Any], Optional):
                    The action to take.

                    * storage_class(str, Optional):
                        Target storage class. Required iff the type of the action is SetStorageClass.
                    * type(str, Optional):
                        Type of the action. Currently, only Delete, SetStorageClass, and AbortIncompleteMultipartUpload are supported.
                * condition(Dict[str, Any], Optional):
                    The condition(s) under which the action will be taken.

                    * age(int, Optional):
                        Age of an object (in days). This condition is satisfied when an object reaches the specified age.
                    * created_before(str, Optional):
                        A date in RFC 3339 format with only the date part (for instance, "2013-01-15"). This condition is satisfied when an object is created before midnight of the specified date in UTC.
                    * custom_time_before(str, Optional):
                        A date in RFC 3339 format with only the date part (for instance, "2013-01-15"). This condition is satisfied when the custom time on an object is before this date in UTC.
                    * days_since_custom_time(int, Optional):
                        Number of days elapsed since the user-specified timestamp set on an object. The condition is satisfied if the days elapsed is at least this number. If no custom timestamp is specified on an object, the condition does not apply.
                    * days_since_noncurrent_time(int, Optional):
                        Number of days elapsed since the noncurrent timestamp of an object. The condition is satisfied if the days elapsed is at least this number. This condition is relevant only for versioned objects. The value of the field must be a nonnegative integer. If it's zero, the object version will become eligible for Lifecycle action as soon as it becomes noncurrent.
                    * is_live(bool, Optional):
                        Relevant only for versioned objects. If the value is true, this condition matches live objects; if the value is false, it matches archived objects.
                    * matches_pattern(str, Optional):
                        A regular expression that satisfies the RE2 syntax. This condition is satisfied when the name of the object matches the RE2 pattern. Note: This feature is currently in the "Early Access" launch stage and is only available to a whitelisted set of users; that means that this feature may be changed in backward-incompatible ways and that it is not guaranteed to be released.
                    * matches_prefix(List[str], Optional):
                        List of object name prefixes. This condition will be satisfied when at least one of the prefixes exactly matches the beginning of the object name.
                    * matches_suffix(List[str], Optional):
                        List of object name suffixes. This condition will be satisfied when at least one of the suffixes exactly matches the end of the object name.
                    * matches_storage_class(List[str], Optional):
                        Objects having any of the storage classes specified by this condition will be matched. Values include MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, and DURABLE_REDUCED_AVAILABILITY.
                    * noncurrent_time_before(str, Optional):
                        A date in RFC 3339 format with only the date part (for instance, "2013-01-15"). This condition is satisfied when the noncurrent time on an object is before this date in UTC. This condition is relevant only for versioned objects.
                    * num_newer_versions(int, Optional):
                        Relevant only for versioned objects. If the value is N, this condition is satisfied when there are at least N versions (including the live version) newer than this version of the object.

        autoclass(Dict[str, Any], Optional):
            The bucket's Autoclass configuration. Defaults to None.

            * enabled(bool, Optional):
                Whether or not Autoclass is enabled on this bucket
            * toggle_time(str, Optional):
                A date and time in RFC 3339 format representing the instant at which "enabled" was last toggled.

        location(str, Optional):
            The location of the bucket. Object data for objects in the bucket resides in physical storage within this region. Defaults to US. See the developer's guide for the authoritative list. Defaults to None.

        logging(Dict[str, Any], Optional):
            The bucket's logging configuration, which defines the destination bucket and optional name prefix for the current bucket's logs. Defaults to None.

            * log_bucket(str, Optional):
                The destination bucket where the current bucket's logs should be placed.
            * log_object_prefix(str, Optional):
                A prefix for log object names.

        retention_policy(Dict[str, Any], Optional):
            The bucket's retention policy. The retention policy enforces a minimum retention time for all objects contained in the bucket, based on their creation time. Any attempt to overwrite or delete objects younger than the retention period will result in a PERMISSION_DENIED error. An unlocked retention policy can be modified or removed from the bucket via a storage.buckets.update operation. A locked retention policy cannot be removed or shortened in duration for the lifetime of the bucket. Attempting to remove or decrease period of a locked retention policy will result in a PERMISSION_DENIED error. Defaults to None.

            * is_locked(bool, Optional):
                Locks the retention policy. Once locked, an object retention policy cannot be modified.
            * retention_period(str, Optional):
                The duration in seconds that objects need to be retained. Retention duration must be greater than zero and less than 100 years. Note that enforcement of retention periods less than a day is not guaranteed. Such periods should only be used for testing purposes.

        rpo(str, Optional):
            The Recovery Point Objective (RPO) of this bucket. Set to ASYNC_TURBO to turn on Turbo Replication on a bucket. Defaults to None.

        storage_class(str, Optional):
            The bucket's default storage class, used whenever no storageClass is specified for a newly-created object. This defines how objects in the bucket are stored and determines the SLA and the cost of storage. Values include MULTI_REGIONAL, REGIONAL, STANDARD, NEARLINE, COLDLINE, ARCHIVE, and DURABLE_REDUCED_AVAILABILITY. If this value is not specified when the bucket is created, it will default to STANDARD. For more information, see storage classes. Defaults to None.

        versioning(Dict[str, Any], Optional):
            The bucket's versioning configuration. Defaults to None.

            * enabled(bool, Optional):
                While set to true, versioning is fully enabled for this bucket.

        website(Dict[str, Any], Optional):
            The bucket's website configuration, controlling how the service behaves when accessing bucket contents as a web site. See the Static Website Examples for more information. Defaults to None.

            * main_page_suffix(str, Optional):
                If the requested object path is missing, the service will ensure the path has a trailing '/', append this suffix, and attempt to retrieve the resulting object. This allows the creation of index.html objects to represent directory pages.
            * not_found_page(str, Optional):
                If the requested object path is missing, and any mainPageSuffix object is missing, if applicable, the service will return the named object from this bucket as the content for a 404 Not Found result.

        metageneration(str, Optional):
            The metadata generation of this bucket. Read-only property

        if_metageneration_match(str, Optional):
            Makes the operation conditional on whether bucket's current metageneration matches the given value. Currently used only when locking retention policy

        acl(list[Dict[str, Any]], Optional):
            Access controls on the bucket. Defaults to None.

            * bucket(str, Optional):
                [OutputOnly] The name of the bucket.

            * domain(str, Optional):
                [OutputOnly] The domain associated with the entity, if any.

            * email(str, Optional):
                [OutputOnly] The email address associated with the entity, if any.

            * entity(str, Optional):
                The entity holding the permission, in one of the following forms:
                - user-userId
                - user-email
                - group-groupId
                - group-email
                - domain-domain
                - project-team-projectId
                - allUsers
                - allAuthenticatedUsers Examples:
                - The user liz@example.com would be user-liz@example.com.
                - The group example@googlegroups.com would be group-example@googlegroups.com.
                - To refer to all members of the Google Apps for Business domain example.com, the entity would be domain-example.com.

            * entity_id(str, Optional):
                [OutputOnly] The ID for the entity, if any.

            * etag(str, Optional):
                [OutputOnly] HTTP 1.1 Entity tag for the access-control entry.

            * id(str, Optional):
                [OutputOnly] The ID of the access-control entry.

            * kind(str, Optional):
                [OutputOnly] The kind of item this is. For bucket access control entries, this is always storage#bucketAccessControl.

            * project_team(Dict[str, Any], Optional):
                [OutputOnly] The project team associated with the entity, if any.

                * project_number(str, Optional):
                    [OutputOnly] The project number.

                * team(str, Optional):
                    [OutputOnly] The team.

            * role(str, Optional):
                The access permission for the entity.

            * self_link(str, Optional):
                [OutputOnly] The link to this access-control entry.

        default_object_acl(list[Dict[str, Any]], Optional):
            Default access controls to apply to new objects when no ACL is provided. Defaults to None.

            * domain(str, Optional):
                [OutputOnly] The domain associated with the entity, if any.

            * email(str, Optional):
                [OutputOnly] The email address associated with the entity, if any.

            * entity(str, Optional):
                The entity holding the permission, in one of the following forms:
                - user-userId
                - user-email
                - group-groupId
                - group-email
                - domain-domain
                - project-team-projectId
                - allUsers
                - allAuthenticatedUsers Examples:
                - The user liz@example.com would be user-liz@example.com.
                - The group example@googlegroups.com would be group-example@googlegroups.com.
                - To refer to all members of the Google Apps for Business domain example.com, the entity would be domain-example.com.

            * entity_id(str, Optional):
                [OutputOnly] The ID for the entity, if any.

            * etag(str, Optional):
                [OutputOnly] HTTP 1.1 Entity tag for the access-control entry.

            * kind(str, Optional):
                [OutputOnly] The kind of item this is. For object access control entries, this is always storage#objectAccessControl.

            * project_team(Dict[str, Any], Optional):
                [OutputOnly] The project team associated with the entity, if any.

                * project_number(str, Optional):
                    [OutputOnly] The project number.

                * team(str, Optional):
                    [OutputOnly] The team.

            * role(str, Optional):
                The access permission for the entity.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.storage.bucket.present:
                - name: value
                - project: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    resource_type_camel = hub.tool.gcp.case.camel(RESOURCE_TYPE_FULL.split(".")[-1])

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE_SIMPLE, resource_id, {**locals(), resource_type_camel: name}
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )
    if resource_id:
        old_get_ret = await hub.exec.gcp.storage.bucket.get(
            ctx, resource_id=resource_id, projection="full", user_project=user_project
        )

        if not old_get_ret["result"] or not old_get_ret["ret"]:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.resource_not_found_comment(
                    RESOURCE_TYPE_FULL, resource_id
                )
            )
            result["comment"].extend(old_get_ret["comment"])
            return result

        # if resource_id is provided explicitly or by ESM, we want update
        result["old_state"] = old_get_ret["ret"]
    elif not hub.OPT.idem.get("get_resource_only_with_resource_id", False):
        # attempt to discover existing resource which is not tracked by idem
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE_SIMPLE, {**locals(), "bucket": name}
        )

        old_get_ret = await hub.exec.gcp.storage.bucket.get(
            ctx, resource_id=resource_id, projection="full", user_project=user_project
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.resource_not_found_comment(
                    RESOURCE_TYPE_FULL, resource_id
                )
            )
            result["comment"].extend(old_get_ret["comment"])
            return result

        # resource we try to discover exists
        if old_get_ret["ret"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.resource_discovered_comment(
                    RESOURCE_TYPE_FULL, resource_id
                )
            )
            result["old_state"] = old_get_ret["ret"]

    old = result["old_state"]

    resource_body = {
        "name": name,
        "autoclass": autoclass,
        "billing": billing,
        "cors": cors,
        "custom_placement_config": custom_placement_config,
        "default_event_based_hold": default_event_based_hold,
        "encryption": encryption,
        "iam_configuration": iam_configuration,
        "labels": labels,
        "lifecycle": lifecycle,
        "location": location,
        "logging": logging,
        "retention_policy": retention_policy,
        "rpo": rpo,
        "storage_class": storage_class,
        "versioning": versioning,
        "website": website,
        "metageneration": metageneration,
        "acl": acl,
        "default_object_acl": default_object_acl,
    }

    plan_state = {
        "resource_id": resource_id,
        **resource_body,
    }

    plan_state = {k: v for (k, v) in plan_state.items() if v is not None}

    if old:
        result["new_state"] = old

        changes = hub.tool.gcp.utils.compare_states(
            old, plan_state, RESOURCE_TYPE_SIMPLE
        )

        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(RESOURCE_TYPE_FULL, name)
            )

            return result

        changed_non_updatable_properties = (
            hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                RESOURCE_TYPE_SIMPLE, changes
            )
        )

        if changed_non_updatable_properties:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    RESOURCE_TYPE_FULL, name, changed_non_updatable_properties
                )
            )
            return result

        # is_locked property is not updateable through the regular patch operation
        new_is_locked = (plan_state.get("retention_policy") or {}).pop(
            "is_locked", None
        )

        if changes.get("relevant_changes", {}) != {
            "root['retention_policy']['is_locked']"
        }:
            if ctx["test"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.would_update_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
                result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                    {**old, **plan_state}
                )
            else:
                # Perform update
                update_ret = await hub.exec.gcp_api.client.storage.bucket.patch(
                    hub,
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    body=plan_state,
                    userProject=user_project,
                )

                if not update_ret["result"]:
                    result["result"] = False
                    result["comment"] += update_ret["comment"]
                    return result

                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(RESOURCE_TYPE_FULL, name)
                )

                if not if_metageneration_match:
                    if_metageneration_match = update_ret.get("ret", {}).get(
                        "metageneration"
                    )

        # lock retention policy after update has succeeded to ensure that the retention period specified
        # has been applied
        old_is_locked = (old.get("retention_policy") or {}).get("is_locked")

        if not if_metageneration_match:
            if_metageneration_match = old.get("metageneration")
    else:
        result["old_state"] = None
        old_is_locked = False
        new_is_locked = (resource_body.get("retention_policy") or {}).pop(
            "is_locked", None
        )
        (resource_body.get("retention_policy") or {}).pop("effective_time", None)

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            hub.tool.gcp.resource_prop_utils.populate_resource_with_assumed_values(
                plan_state,
                RESOURCE_TYPE_SIMPLE,
                convert_to_present=True,
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                plan_state
            )

            if not if_metageneration_match:
                if_metageneration_match = "mock_value"
        else:
            project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

            # Create
            create_ret = await hub.exec.gcp_api.client.storage.bucket.insert(
                ctx,
                name=name,
                project=project,
                userProject=user_project,
                predefined_acl=predefined_acl,
                predefined_default_object_acl=predefined_default_object_acl,
                projection="full",
                body=resource_body,
            )

            if not create_ret["result"]:
                result["result"] = False
                if not create_ret["comment"]:
                    return result
                if next(
                    (
                        comment
                        for comment in create_ret["comment"]
                        if "HttpError 409" in comment
                    ),
                    None,
                ):
                    result["comment"].append(
                        hub.tool.gcp.comment_utils.already_exists_comment(
                            RESOURCE_TYPE_FULL, name
                        )
                    )
                    return result
                else:
                    result["comment"].extend(create_ret["comment"])
                return result

            result["comment"].append(
                hub.tool.gcp.comment_utils.create_comment(RESOURCE_TYPE_FULL, name)
            )

            resource_id = create_ret.get("ret", {}).get("resource_id")

            if not if_metageneration_match:
                if_metageneration_match = create_ret.get("ret", {}).get(
                    "metageneration"
                )

    enforce_retention_policy_result = (
        await hub.tool.gcp.storage.bucket.enforce_retention_policy(
            ctx,
            result,
            old_is_locked,
            new_is_locked,
            if_metageneration_match,
            user_project,
            resource_id,
        )
    )

    if not ctx["test"]:
        await _assign_new_state_from_get(hub, ctx, user_project, result, resource_id)

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    user_project: str = None,
):
    r"""Permanently deletes an empty bucket.

    Args:
        name(str):
            The name of the resource

        resource_id(str, Optional):
            The resource_id of the resource

        user_project(str, Optional):
            The project to be billed for this request. Required for Requester Pays buckets.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

        resource_is_absent:
          gcp.storage.bucket.absent

    """
    result = {
        "result": True,
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "comment": [],
    }

    if not resource_id and not hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    ):
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE_SIMPLE, {**locals(), "bucket": name}
        )

    if not resource_id:
        # we don't have enough information to know what to delete
        # TODO: should this be an error? The SLS inputs are invalid
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    get_ret = await hub.exec.gcp.storage.bucket.get(
        ctx, resource_id=resource_id, projection="full", user_project=user_project
    )

    if not get_ret["result"]:
        result["result"] = False
        result["comment"].append(
            hub.tool.gcp.comment_utils.resource_not_found_comment(
                RESOURCE_TYPE_FULL, resource_id
            )
        )
        result["comment"].extend(get_ret["comment"])
        return result

    if not get_ret["ret"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    result["old_state"] = get_ret["ret"]

    if ctx["test"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    # Delete the existing bucket (async call).
    del_ret = await hub.exec.gcp_api.client.storage.bucket.delete(
        ctx, resource_id=resource_id, userProject=user_project
    )

    if not del_ret["result"]:
        result["result"] = False
        result["comment"].extend(del_ret["comment"])
        return result

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment(RESOURCE_TYPE_FULL, name)
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of buckets.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.storage.bucket
    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp.storage.bucket.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe buckets {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.storage.bucket.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)


async def _assign_new_state_from_get(hub, ctx, user_project, result, resource_id):
    get_ret = await hub.exec.gcp.storage.bucket.get(
        ctx, resource_id=resource_id, projection="full", user_project=user_project
    )

    if not get_ret["result"] or not get_ret["ret"]:
        result["result"] = False
        result["comment"].append(
            hub.tool.gcp.comment_utils.resource_not_found_comment(
                RESOURCE_TYPE_FULL, resource_id
            )
        )
        result["comment"].extend(get_ret["comment"])
        return

    result["new_state"] = get_ret["ret"]
