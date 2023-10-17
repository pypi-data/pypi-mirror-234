"""Exec module for managing Disks."""
__func_alias__ = {"list_": "list"}

from dataclasses import make_dataclass, field
from typing import Dict, Any, List

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext


async def list_(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves a list of persistent disks.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone for this request.

        region(str, Optional):
            The name of the region for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk.list
              - kwargs:
                  project: project-name
                  zone: zone-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if zone:
        ret = await hub.exec.gcp_api.client.compute.disk.list(
            ctx,
            project=project,
            zone=zone,
            filter=filter_,
            orderBy=order_by,
        )
    elif region:
        ret = await hub.exec.gcp_api.client.compute.disk.list(
            ctx,
            project=project,
            region=region,
            filter=filter_,
            orderBy=order_by,
        )
    else:
        ret = await hub.exec.gcp_api.client.compute.disk.aggregatedList(
            ctx,
            project=project,
            filter=filter_,
            orderBy=order_by,
        )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"].get("items", [])
    return result


async def get(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    region: str = None,
    name: str = None,
    resource_id: str = None,
):
    r"""Returns a specified persistent disk.

    Use an un-managed disk as a data-source. Supply one of the inputs as the filter.
    Gets a list of available persistent disks by making a list() request.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        region(str, Optional):
            The name of the region for this request. Defaults to None.

        name(str, Optional):
            Name of the persistent disk to return. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk.get
              - kwargs:
                  name: disk-name
                  project: project-name
                  zone: zone-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.disk.get(
            ctx,
            resource_id=resource_id,
        )
    elif project and zone and name:
        ret = await hub.exec.gcp_api.client.compute.disk.get(
            ctx, project=project, zone=zone, disk=name
        )
    elif project and region and name:
        ret = await hub.exec.gcp_api.client.compute.disk.get(
            ctx, project=project, region=region, disk=name
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disk#get(): {name} either resource_id or project, zone/region and name"
            f" should be specified."
        ]
        return result

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def create_snapshot(
    hub,
    ctx,
    name: str,
    project: str = None,
    zone: str = None,
    region: str = None,
    disk: str = None,
    resource_id: str = None,
    storage_locations: List[str] = None,
    location_hint: str = None,
    label_fingerprint: str = None,
    description: str = None,
    labels: Dict[str, Any] = None,
    source_disk_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("kms_key_service_account", str, field(default=None)),
            ("sha256", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("raw_key", str, field(default=None)),
        ],
    ) = None,
    source_disk: str = None,
    chain_name: str = None,
    snapshot_type: str = None,
    snapshot_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("kms_key_service_account", str, field(default=None)),
            ("sha256", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("raw_key", str, field(default=None)),
        ],
    ) = None,
    request_id: str = None,
):
    r"""Creates a snapshot of a specified persistent disk. For regular snapshot creation, consider using snapshots.insert instead, as that method supports more features, such as creating snapshots in a project different from the source disk project.

    Args:
        name(str):
            Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.",
                                "pattern": "[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        region(str, Optional):
            The name of the region for this request. Defaults to None.

        disk(str, Optional):
            Name of the persistent disk to snapshot.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk.create_snapshot
              - kwargs:
                  name: snapshot-name
                  disk: disk-name
                  project: project-name
                  zone: zone-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    request_body = {
        "name": name,
        "storage_locations": storage_locations,
        "location_hint": location_hint,
        "label_fingerprint": label_fingerprint,
        "description": description,
        "labels": labels,
        "source_disk_encryption_key": source_disk_encryption_key,
        "source_disk": source_disk,
        "chain_name": chain_name,
        "snapshot_type": snapshot_type,
        "snapshot_encryption_key": snapshot_encryption_key,
    }

    execution_context = ExecutionContext(
        resource_type="compute.disk",
        method_name="createSnapshot",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "body": request_body,
            "requestId": request_id,
            "project": project,
            "zone": zone,
            "region": region,
            "disk": disk,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def create_from_snapshot(
    hub,
    ctx,
    source_snapshot: str,
    size_gb: str,
    type_: (str, "alias=type") = None,
    name: str = None,
    project: str = None,
    zone: str = None,
    region: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Create a disk from a snapshot.

    If you backed up a boot or non-boot disk with a snapshot, you can create a new disk based on the snapshot.

    Restrictions:
        The new disk must be at least the same size as the original source disk for the snapshot. If you create a disk that is larger than the original source disk for the snapshot, you must resize the file system on that persistent disk to include the additional disk space. Depending on your operating system and file system type, you might need to use a different file system resizing tool. For more information, see your operating system documentation.

        You can create a new zonal disk from a given snapshot at most once every ten minutes. If you want to issue a burst of requests to snapshot your disks, you can issue at most 6 requests in 60 minutes. This limit does not apply when creating regional disks from a snapshot.

    Args:
        name(str):
            Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.",

            "pattern": "[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            The name of the zone for this request. Defaults to None.

        region(str, Optional):
            The name of the region for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

        source_snapshot(str):
            The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource.
            For example, the following are valid values:

            - https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot
            - projects/project/global/snapshots/snapshot
            - global/snapshots/snapshot

        size_gb(str):
            Size, in GB, of the persistent disk.
            You can specify this field when creating a persistent disk using the sourceImage, sourceSnapshot,
            or sourceDisk parameter, or specify it alone to create an empty persistent disk.
            If you specify this field along with a source, the value of sizeGb must not
            be less than the size of the source. Acceptable values are 1 to 65536, inclusive.
            Defaults to None.

        type(str, Optional):
            URL of the disk type resource describing which disk type to use to create the disk.
            Provide this when creating the disk. For example: projects/project /zones/zone/diskTypes/pd-ssd.
            See Persistent disk types.
            Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk.create_from_snapshot
              - kwargs:
                  source_snapshot: snapshot_resource_id
                  name: restored-disk-name
                  project: project-name
                  zone: zone-name
                  size_gb: disk-size
    """
    request_body = {
        "type": type_,
        "name": name,
        "size_gb": size_gb,
        "zone": zone,
        "region": region,
        "source_snapshot": source_snapshot,
    }

    execution_context = ExecutionContext(
        resource_type="compute.disk",
        method_name="insert",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "region": region,
            "body": request_body,
            "requestId": request_id,
        },
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
