# flake8: noqa
from typing import Callable
import json
import os
import sys
import dataclasses
from . import context
from . import scopes
from . import credentials
from . import tokens
import jwt

from .version import __version__  # noqa

sys.path.append(os.path.dirname(__file__))  # noqa

from .agilicus_api import *  # noqa
from .agilicus_api import exceptions  # noqa
from . import patches  # noqa


ApiClient = patches.patched_api_client()


def find_guid(obj: dict):
    guid = obj.get("id", None)
    if guid:
        return guid
    md = obj.get("metadata", {})
    guid = md.get("id", None)
    if guid:
        return guid
    raise Exception(f"GUID cannot be found in obj {obj}")


def create_or_update(
    obj,
    create_method: Callable,
    update_method: Callable = None,
    to_dict=True,
) -> [dict, str]:
    """A helper method that handles duplicate (409)
    creation of objects. On 409, if the update_method is provided,
    it will apply a PUT on the resource to update it with
    the new requested data. The guid is searched for in the object
    returned from the 409, and this is then provided
    to the update method as an argument, along with the original
    object that should be applied.
        param: obj: the object to be created or updated
        param: create_method(obj, ...)
        param: update_method(guid, obj, ...)
        returns: tuple, the object, with the status code.

        Note the status code could be:
           409: a duplicate, no update was performed
           201: a create was succesfully made
           200: a duplicate occured, and the object was updated accordingly
    """
    result = None
    try:
        result = create_method(obj)
        if to_dict:
            return result.to_dict(), 201
        else:
            return result, 201
    except ApiException as exc:
        if exc.status == 409:
            body = exc.body
            if not body:
                raise
            result = json.loads(body)
            if update_method:
                guid = find_guid(result)
                if to_dict:
                    return update_method(guid, obj).to_dict(), 200
                else:
                    return update_method(guid, obj), 200
            else:
                return result, 409
        else:
            raise
    return result


def GetClient(
    issuer=context.ISSUER_DEFAULT,
    cacert=None,
    client_id="agilicus-builtin-cli",
    authentication_document=None,
    agilicus_scopes=scopes.DEFAULT_SCOPES,
    auth_local_webserver=True,
    api_url=None,
    expiry=None,
):

    config = Configuration(host=api_url, ssl_ca_cert=cacert)
    if authentication_document:
        creds = {}
        with open(authentication_document) as fd:
            ad = json.load(fd)
        token = tokens.create_service_token(
            auth_doc=ad,
            scope=agilicus_scopes,
            client_id=client_id,
            expiry=expiry,
            verify=cacert,
        )
        config.access_token = token.get("access_token")
    else:
        creds = credentials.get_credentials(
            issuer=issuer,
            cacert=cacert,
            client_id=client_id,
            agilicus_scopes=agilicus_scopes,
            auth_local_webserver=auth_local_webserver,
        )
        config.access_token = creds.access_token

    _default_org_id = None
    access_token = jwt.decode(
        config.access_token,
        algorithms=["ES256"],
        options={"verify_signature": False},
        leeway=60,
    )
    if "org" in access_token:
        _default_org_id = access_token["org"]

    @dataclasses.dataclass
    class api:
        default_org_id = _default_org_id
        users = UsersApi(ApiClient(config))
        billing = BillingApi(ApiClient(config))
        organisations = OrganisationsApi(ApiClient(config))
        policies = PolicyApi(ApiClient(config))
        certificates = CertificatesApi(ApiClient(config))
        applications = ApplicationsApi(ApiClient(config))
        groups = GroupsApi(ApiClient(config))
        connectors = ConnectorsApi(ApiClient(config))
        resouces = ResourcesApi(ApiClient(config))
        catalogues = CataloguesApi(ApiClient(config))
        permissions = PermissionsApi(ApiClient(config))
        audits = AuditsApi(ApiClient(config))
        files = FilesApi(ApiClient(config))
        tokens = TokensApi(ApiClient(config))
        diagnostics = DiagnosticsApi(ApiClient(config))
        metrics = MetricsApi(ApiClient(config))
        challenges = ChallengesApi(ApiClient(config))
        application_services = ApplicationServicesApi(ApiClient(config))
        issuers = IssuersApi(ApiClient(config))
        messages = MessagesApi(ApiClient(config))
        lookups = LookupsApi(ApiClient(config))
        trusted_certs = TrustedCertsApi(ApiClient(config))
        rules = RulesApi(ApiClient(config))

    return api
