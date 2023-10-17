"""Exec module for managing Subnetworks."""
__func_alias__ = {"list_": "list"}

from typing import Any, Dict, List

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext


async def list_(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves a list of subnetworks available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            Name of the region scoping this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.subnetwork.list
              - kwargs:
                  project: project-name
                  region: region-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if region:
        list_result = await hub.exec.gcp_api.client.compute.subnetwork.list(
            ctx,
            project=project,
            region=region,
            filter=filter_,
            orderBy=order_by,
        )
    else:
        list_result = await hub.exec.gcp_api.client.compute.subnetwork.aggregatedList(
            ctx,
            project=project,
            filter=filter_,
            orderBy=order_by,
        )

    result["comment"] += list_result["comment"]
    if not list_result["result"]:
        result["result"] = False
        return result

    result["ret"] = list_result["ret"].get("items", [])
    return result


async def get(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    name: str = None,
    resource_id: str = None,
):
    r"""Returns the specified subnetwork. Gets a list of available subnetworks list() request.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        region(str, Optional):
            Name of the region scoping this request. Defaults to None.

        name(str, Optional):
            Name of the Subnetwork resource to return. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.subnetwork.get
              - kwargs:
                  project: project-name
                  region: region-name
                  name: subnetwork-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.subnetwork.get(
            ctx,
            resource_id=resource_id,
        )
    elif project and region and name:
        ret = await hub.exec.gcp_api.client.compute.subnetwork.get(
            ctx, project=project, region=region, subnetwork=name, name=name
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.subnetwork {name} either resource_id or project, region and name"
            f" should be specified."
        ]
        return result

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def update_ip_cidr_range(
    hub,
    ctx,
    new_ip_cidr_range: List[Dict[str, Any]],
    project: str = None,
    region: str = None,
    subnetwork: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Expands the IP CIDR range of the subnetwork to a specified value.

    Args:
        new_ip_cidr_range(List):
            The IP (in CIDR format or netmask) of internal addresses that are legal on
            this Subnetwork. This range should be disjoint from other subnetworks within this network.
            This range can only be larger than (i.e. a superset of) the range previously defined before the update.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            Name of the region scoping this request.

        subnetwork(str, Optional):
            Name of the Subnetwork resource to update.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that
            if you must retry your request, the server will know to ignore the request if it has already been completed.
            For example, consider a situation where you make an initial request and the request times out. If you make
            the request again with the same request ID, the server can check if original operation with the same request
            ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating
            duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """
    request_body = {"ip_cidr_range": new_ip_cidr_range}
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    execution_context = ExecutionContext(
        resource_type="compute.subnetwork",
        method_name="expandIpCidrRange",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "request_id": request_id,
            "project": project,
            "region": region,
            "subnetwork": subnetwork,
            "body": request_body,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
