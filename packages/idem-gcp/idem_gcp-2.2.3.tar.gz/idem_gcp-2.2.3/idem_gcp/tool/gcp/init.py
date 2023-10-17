"""Idem plugin for the Google API Python client library.

Google API Python client library
:copyright: Copyright (c) 2020-2022 VMware, Inc. All Rights Reserved.
:license: SPDX-License-Identifier: Apache-2.0

This file declares and implements a class to wrap and make easy access to
Google's discovery based APIs. Additionally, it declares and implements the
entirety of the Plugin Oriented Programming (POP) exec Sub for Google API
Management via POP ReverseSub.

The basic operating model is building Subs as needed to match the nature of a
call to an exec. For example, a call like:

    gcp.compute.instance.get(ctx, ...)

Those are ultimately implemented by calls to the _GCPApi class runnable.

will work, even though no exec subdirectories exist to match that call path.
Instead, the API is dynamically discovered and built to match and tie
them to the appropriate Google Python SDK wrappers within the tool Sub of
this project.
"""
import time
from inspect import signature
from socket import timeout
from urllib.parse import urlparse

try:
    from googleapiclient import discovery
    from googleapiclient.discovery_cache import base as base_cache

    import idem_gcp.helpers.exc as idemexc

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def __init__(hub):
    # hub.pop.sub.load_subdirs(hub.tool.gcp, recurse=True)
    hub.pop.sub.add(dyne_name="metadata")
    hub.pop.sub.load_subdirs(hub.metadata, recurse=True)
    """
    Initialize default API versions and setup the root _GCPApi object.
    :param hub: The Idem hub to use for (attach to) the root of the
    GCPApi API tree that gets dynamically built.
    """
    # hub.pop.config.load(["idem", "acct", "idem_gcp", "rend", "evbus"], "idem", parse_cli=True)
    hub.tool.gcp.DEFAULT_VERSIONS = {
        "abusiveexperiencereport": "v1",
        "acceleratedmobilepageurl": "v1",
        "accessapproval": "v1",
        "accesscontextmanager": "v1",
        "adexchangebuyer2": "v2beta1",
        "adexperiencereport": "v1",
        #'admin': ['datatransfer_v1', 'directory_v1', 'reports_v1'],
        "admob": "v1",
        "adsense": "v2",
        "adsensehost": "v4.1",
        "alertcenter": "v1beta1",
        "analytics": "v3",
        "analyticsadmin": "v1alpha",
        "analyticsdata": "v1beta",
        "analyticshub": "v1beta1",
        "analyticsreporting": "v4",
        "androiddeviceprovisioning": "v1",
        "androidenterprise": "v1",
        "androidmanagement": "v1",
        "androidpublisher": "v3",
        "apigateway": "v1",
        "apigee": "v1",
        "apigeeregistry": "v1",
        "apikeys": "v2",
        "appengine": "v1",
        "area120tables": "v1alpha1",
        "artifactregistry": "v1",
        "assuredworkloads": "v1",
        "authorizedbuyersmarketplace": "v1",
        "baremetalsolution": "v2",
        "beyondcorp": "v1alpha",
        "bigquery": "v2",
        "bigqueryconnection": "v1beta1",
        "bigquerydatatransfer": "v1",
        "bigqueryreservation": "v1",
        "bigtableadmin": "v2",
        "billingbudgets": "v1",
        "binaryauthorization": "v1",
        "blogger": "v3",
        "books": "v1",
        "calendar": "v3",
        "certificatemanager": "v1",
        "chat": "v1",
        "chromemanagement": "v1",
        "chromepolicy": "v1",
        "chromeuxreport": "v1",
        "civicinfo": "v2",
        "classroom": "v1",
        "cloudasset": "v1",
        "cloudbilling": "v1",
        "cloudbuild": "v1",
        "cloudchannel": "v1",
        "clouddebugger": "v2",
        "clouddeploy": "v1",
        "clouderrorreporting": "v1beta1",
        "cloudfunctions": "v2",
        "cloudidentity": "v1",
        "cloudiot": "v1",
        "cloudkms": "v1",
        "cloudprofiler": "v2",
        "cloudresourcemanager": "v3",
        "cloudscheduler": "v1",
        "cloudsearch": "v1",
        "cloudshell": "v1",
        "cloudsupport": "v2beta",
        "cloudtasks": "v2",
        "cloudtrace": "v2",
        "composer": "v1",
        "compute": "v1",
        "connectors": "v1",
        "contactcenterinsights": "v1",
        "container": "v1",
        "containeranalysis": "v1",
        "content": "v2.1",
        "customsearch": "v1",
        "datacatalog": "v1",
        "dataflow": "v1b3",
        "datafusion": "v1",
        "datalabeling": "v1beta1",
        "datamigration": "v1",
        "datapipelines": "v1",
        "dataplex": "v1",
        "dataproc": "v1",
        "datastore": "v1",
        "datastream": "v1",
        "deploymentmanager": "v2",
        "dfareporting": "v3.5",
        "dialogflow": "v3",
        "digitalassetlinks": "v1",
        "discovery": "v1",
        "displayvideo": "v1",
        "dlp": "v2",
        "dns": "v1",
        "docs": "v1",
        "documentai": "v1",
        "domains": "v1",
        "domainsrdap": "v1",
        "doubleclickbidmanager": "v1.1",
        "doubleclicksearch": "v2",
        "drive": "v3",
        "driveactivity": "v2",
        "essentialcontacts": "v1",
        "eventarc": "v1",
        "factchecktools": "v1alpha1",
        "fcm": "v1",
        "fcmdata": "v1beta1",
        "file": "v1",
        "firebase": "v1beta1",
        "firebaseappcheck": "v1",
        "firebasedatabase": "v1beta",
        "firebasedynamiclinks": "v1",
        "firebasehosting": "v1",
        "firebaseml": "v1",
        "firebaserules": "v1",
        "firebasestorage": "v1beta",
        "firestore": "v1",
        "fitness": "v1",
        "forms": "v1",
        "games": "v1",
        "gamesConfiguration": "v1configuration",
        "gamesManagement": "v1management",
        "gameservices": "v1",
        "genomics": "v2alpha1",
        "gkebackup": "v1",
        "gkehub": "v1",
        "gmail": "v1",
        "gmailpostmastertools": "v1",
        "groupsmigration": "v1",
        "groupssettings": "v1",
        "healthcare": "v1",
        "homegraph": "v1",
        "iam": "v1",
        "iamcredentials": "v1",
        "iap": "v1",
        "ideahub": "v1beta",
        "identitytoolkit": "v3",
        "ids": "v1",
        "indexing": "v3",
        "jobs": "v4",
        "keep": "v1",
        "kgsearch": "v1",
        "language": "v1",
        "libraryagent": "v1",
        "licensing": "v1",
        "lifesciences": "v2beta",
        "localservices": "v1",
        "logging": "v2",
        "managedidentities": "v1",
        "manufacturers": "v1",
        "memcache": "v1",
        "metastore": "v1beta",
        "ml": "v1",
        "monitoring": "v3",
        "mybusinessaccountmanagement": "v1",
        "mybusinessbusinesscalls": "v1",
        "mybusinessbusinessinformation": "v1",
        "mybusinesslodging": "v1",
        "mybusinessnotifications": "v1",
        "mybusinessplaceactions": "v1",
        "mybusinessqanda": "v1",
        "mybusinessverifications": "v1",
        "networkconnectivity": "v1",
        "networkmanagement": "v1",
        "networksecurity": "v1",
        "networkservices": "v1",
        "notebooks": "v1",
        "oauth2": "v2",
        "ondemandscanning": "v1",
        "orgpolicy": "v2",
        "osconfig": "v1",
        "oslogin": "v1",
        "pagespeedonline": "v5",
        "paymentsresellersubscription": "v1",
        "people": "v1",
        "playcustomapp": "v1",
        "playdeveloperreporting": "v1beta1",
        "playintegrity": "v1",
        "policyanalyzer": "v1",
        "policysimulator": "v1",
        "policytroubleshooter": "v1",
        "poly": "v1",
        "privateca": "v1",
        "prod_tt_sasportal": "v1alpha1",
        "pubsub": "v1",
        "pubsublite": "v1",
        "realtimebidding": "v1",
        "recaptchaenterprise": "v1",
        "recommendationengine": "v1beta1",
        "recommender": "v1",
        "redis": "v1",
        "reseller": "v1",
        "resourcesettings": "v1",
        "retail": "v2",
        "run": "v2",
        "runtimeconfig": "v1",
        "safebrowsing": "v4",
        "sasportal": "v1alpha1",
        "script": "v1",
        "searchconsole": "v1",
        "secretmanager": "v1",
        "securitycenter": "v1",
        "serviceconsumermanagement": "v1",
        "servicecontrol": "v2",
        "servicedirectory": "v1",
        "servicemanagement": "v1",
        "servicenetworking": "v1",
        "serviceusage": "v1",
        "sheets": "v4",
        "siteVerification": "v1",
        "slides": "v1",
        "smartdevicemanagement": "v1",
        "sourcerepo": "v1",
        "spanner": "v1",
        "speech": "v1",
        "sqladmin": "v1",
        "storage": "v1",
        "storagetransfer": "v1",
        "streetviewpublish": "v1",
        "sts": "v1",
        "tagmanager": "v2",
        "tasks": "v1",
        "testing": "v1",
        "texttospeech": "v1",
        "toolresults": "v1beta3",
        "tpu": "v1",
        "trafficdirector": "v2",
        "transcoder": "v1",
        "translate": "v3",
        "vault": "v1",
        "verifiedaccess": "v2",
        "versionhistory": "v1",
        "videointelligence": "v1",
        "vision": "v1",
        "vmmigration": "v1",
        "webfonts": "v1",
        "webrisk": "v1",
        "websecurityscanner": "v1",
        "workflowexecutions": "v1",
        "workflows": "v1",
        "youtube": "v3",
        "youtubeAnalytics": "v2",
        "youtubereporting": "v1",
    }
    hub.tool.gcp.API = _GCPApi(hub, "gcp")


class _MemoryCache(base_cache.Cache):
    """Class to cover for the lack of discovery client file_cache when using recent oauth2client releases.

    See `Github commit
    <https://github.com/GoogleCloudPlatform/python-docs-samples/commit/22788da481a8441500203ccc7fbf37cd9fcafa3b>`_.
    """

    _CACHE = {}

    def get(self, url):
        return _MemoryCache._CACHE.get(url)

    def set(self, url, content):
        _MemoryCache._CACHE[url] = content


class _GCPApi:
    """Class to represent (wrap) `Google's discovery based APIs <https://github.com/googleapis/google-api-python-client>`_.

    Each instance represents a single service or (sub)resource in a way that
    enables writing code such as::

        my_gcpapi.iam.roles.projects.list(ctx, *args, **kwargs)

    in order to call specific apis. The class is callable and creates the
    Google API objects as needed to resolve such code.
    """

    _DISCOVERY_CACHE = _MemoryCache()

    # Operational Flags
    WAIT_ON_OPERATIONS = False

    # Call return codes
    E_NONE = 0
    E_NOTFOUND = -1
    E_JSONERROR = -2
    E_MEDIAERROR = -3
    E_MUTUALTLSCHANNELERROR = -4
    E_UNACCEPTABLEMIMETYPEERROR = -5

    def __init__(
        self, hub, resource_type: str, parent=None, cache: base_cache.Cache = None
    ):
        """Initializes the instance.

        :param hub: The Idem hub to use for related calls (e.g., logging).
        :param resource_type: The name of the service or resource to wrap.
        :type resource_type: str
        :param parent: The _GCPApi parent for this service or resource.
            If parent is None, then it the instance is considered a 'cloud'
            level API interface. For example, a resource_type of 'gcp' can be
            set with a parent of None to signify this is the root of the
            cloud API tree. Child instances would be initialized, for example,
            with resource_type as 'iam' and parent set to the _GCPApi root
            instance or some intermediate GCP API Resource (wrapper) instance.

            (default is None)
        :type parent: _GCPApi
        :param cache: The discovery document cache implementation. If set to
            None, an internal MemoryCache will be used.
        :type cache: Cache
        :return: The googleapiclient service or sub Resource.
        :rtype: _GCPApi
        """
        self._hub = hub
        self._parent = parent
        self._resources = {}
        self._api_resource = None
        if cache == None:
            self._cache = _GCPApi._DISCOVERY_CACHE
        else:
            self._cache = cache
        self.name = resource_type
        self._is_operation = (
            resource_type in ("zoneOperations", "regionOperations", "globalOperations")
            or self._parent
            and self._parent._is_operation
        )

    def get_dotted_notation(self) -> str:
        """Builds fully qualified 'dotted' path to self."""
        if self._parent is None:
            return self.name
        else:
            str = self._parent.get_dotted_notation()
            return f"{str}.{self.name}"

    def _build_service(self, ctx):
        """Return the top level gcp (client) service Resource.

        :param ctx: The Idem acct context (credentials) to use for
            the Google API calls.
        return: Google API Resource this instance wraps.
        :rtype: Resource
        """
        api_versions = ctx.acct.get("api_versions", {})
        api_version = api_versions.get(
            self.name, self._hub.tool.gcp.DEFAULT_VERSIONS[self.name]
        )

        ret = discovery.build(
            serviceName=self.name,
            version=api_version,
            credentials=ctx.acct["credentials"],
            cache=self._cache,
            discoveryServiceUrl=ctx.acct.get("discovery_service_url"),
        )
        self._api_resource = ret

        return ret

    def __getattr__(self, attr: str):
        """Gets and returns the named _GCPApi child.

        :type self: _GCPAPI
        :param attr: The name of the service or subresource, e.g.,
            'iam', or 'roles' or the like.
        :type attr: str
        :return: The googleapiclient (client) resource.
        :rtype: _GCPApi
        """
        if attr == "wait_on_operations":
            return self.wait_on_operations

        # If no existing resource exists, create it and attach it as a child
        try:
            ret = self._resources[attr]
        except KeyError:
            ret = _GCPApi(self._hub, attr, self)
            self._resources[attr] = ret

        return self._resources[attr]

    def build_call_resource(self, ctx, *args, **kwargs):
        """Recursively builds all _GCPApi Resources.

        This call walks a branch of a Google discovered API tree. For
        example, a call such as:

            my_gcpapi.iam.roles.list(ctx, *args, **kwargs)

        would result in a the creation (if not already created)
        the necessary _GCPApi wrappers for each of the dotted
        notation entries (indirectly via __getattr__). As well,
        for each of those wrappers, this call will create the
        Google API Resource that relates.

        :param ctx: The Idem acct context (credentials) to use for
            the Google API calls.
        :param args: A list of positional arguments to pass, as needed based
            on Google API signatures, each Resource to obtain subresources.
        type args: tuple
        :param kwargs: Named parameters as key/value pairs.
        :type kwargs: dictionary
        :return: The googleapiclient (client) resource.
        :rtype: _GCPApi
        """
        if self._parent is None:
            # Terminate the recursion at the top of the call tree:
            # the top of the tree is the cloud api object and has only
            # child callable services, therefore nothing to contribute.
            return None

        # build the parent api resource
        resource = self._parent.build_call_resource(ctx, *args, **kwargs)

        if resource is None:
            # This is a top level service (e.g., iam), return the result of
            # discovery build (i.e., the gcp api service client).
            if self._api_resource is None:
                self._api_resource = self._build_service(ctx)
            return self._api_resource
        else:
            # Subresource -- use the parent resource directly to avoid
            # another recursive buildout; it should be already created.
            resource = getattr(self._parent._api_resource, self.name)
            call_args = []
            call_kwargs = {}
            sig = signature(resource)
            for param in sig.parameters.values():
                if param.kind == param.POSITIONAL_ONLY:
                    call_args = args[call_args_index]
                    call_args_index + 1
                elif param.kind == param.POSITIONAL_OR_KEYWORD:
                    self._hub.log.debug("Error: Unsupported -- POSITIONAL_OR_KEYWORD")
                elif param.kind == param.KEYWORD_ONLY:
                    self._hub.log.debug("Error: Unsupported -- KEYWORD_ONLY")
                elif param.kind == param.VAR_POSITIONAL:
                    self._hub.log.debug("Error: Unsupported -- VAR_POSITIONAL")
                elif param.kind == param.VAR_KEYWORD:
                    call_kwargs = kwargs
            self._api_resource = resource(*call_args, **call_kwargs)
            return self._api_resource

    def wait_on_operations(self, wait: bool):
        """Set this object instance to wait for the completion, or related error, of all long running GCP API calls.

        :param wait: Whether to wait (True) or not (False).
        """
        _GCPApi.WAIT_ON_OPERATIONS = wait

    def _wait_on_operation(self, ctx, project, operation):
        """Waits for an operation to complete or error out.

        :type self: _GCPAPI
        :param ctx: The name of the service or subresource, e.g.,
            'iam', or 'roles' or the like.
        :param operation: The GCP API operation on which to wait.
        """
        if self.WAIT_ON_OPERATIONS:
            done = False
            kind = operation["kind"].split("#")[0]
            gcpapi = getattr(self._hub.tool.gcp.API, kind)
            call_args = []
            call_kwargs = {}
            call_kwargs["project"] = project
            call_kwargs["operation"] = operation["name"]
            while not done:
                # The wait calls below wait until the operation is DONE.
                # However, the GCP wait API makes no promises it will
                # truly wait until DONE, it is merely a 'best effort'
                # so multiple calls to wait may be required. Sleep one
                # second between to prevent potential call bursts.
                time.sleep(1)
                if "zone" in operation:
                    # The zone may get returned as a full URL such as
                    # https://www.googleapis.com/compute/v1/projects/project/zones/us-central1-a.
                    # In that case, parse it
                    path_split = urlparse(operation["zone"]).path.split("/")
                    last_path_element = path_split[len(path_split) - 1]
                    call_kwargs["zone"] = last_path_element
                    api = gcpapi.zoneOperations.wait
                elif "region" in operation:
                    # The region may get returned as a full URL. In that case, parse it
                    path_split = urlparse(operation["region"]).path.split("/")
                    last_path_element = path_split[len(path_split) - 1]
                    call_kwargs["region"] = last_path_element
                    api = gcpapi.regionOperations.wait
                else:
                    api = gcpapi.globalOperations.wait

                call = api.build_call_resource(ctx, *call_args, **call_kwargs)
                try:
                    operation = call.execute()
                    done = operation["status"] == "DONE"
                except timeout:
                    # This hits if the operation fails to finish
                    # though is still running. Other exceptions
                    # gather more deleterious failures.
                    done = False

        return operation

    async def __call__(self, ctx, *args, **kwargs) -> dict:
        """Calls the Google API associated with this instance (self).

        :param ctx: The Idem acct context (credentials) to use for
            the Google API calls.
        :param args: A list of positional arguments to pass, as needed based
            on Google API signatures, each Resource to obtain subresources.
        type args: tuple
        :param kwargs: Named parameters as key/value pairs. These will correspond
            to the Google Google API Python client library API specifics. `See, e.g.,
            <https://googleapis.github.io/google-api-python-client/docs/dyn/compute_v1.instances.html#insert>_`
            for an example of a large set of kwargs.
        :type kwargs: dictionary
        :return: The api client return value.
        """
        call = self.build_call_resource(ctx, *args, **kwargs)
        try:
            resp = call.execute()
            ret = resp
        except discovery.HttpError as httpError:
            if httpError.status_code == 404:
                raise idemexc.NotFoundError(str(httpError))
            else:
                raise httpError
        #     ret['error'] = str(httpError)
        #     ret['code'] = httpError.status_code
        # except discovery.InvalidJsonError as jsonError:
        #     ret['error'] = str(jsonError)
        #     ret['code'] = _GCPApi.E_JSONERROR
        # except discovery.MediaUploadSizeError as mediaError:
        #     ret['error'] = str(mediaError)
        #     ret['code'] = _GCPApi.E_MUTUALTLSCHANNELERROR
        # except discovery.UnacceptableMimeTypeError as mimeError:
        #     ret['error'] = str(mimeError)
        #     ret['code'] = _GCPApi.E_UNACCEPTABLEMIMETYPEERROR

        if "warnings" in resp:
            self._hub.log.warning(str(resp["warnings"]))

        if "error" in resp:
            raise idemexc.OperationError(resp["error"])

        if "kind" in resp and resp["kind"].endswith("#operation"):
            ret = self._wait_on_operation(ctx, kwargs.get("project", None), resp)

        return ret
