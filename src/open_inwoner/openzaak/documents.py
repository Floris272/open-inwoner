import base64
import logging
from datetime import date
from typing import Optional

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

import requests
from requests import HTTPError, RequestException, Response
from zds_client import ClientError
from zgw_consumers.api_models.base import factory

from open_inwoner.openzaak.api_models import InformatieObject
from open_inwoner.openzaak.clients import build_client
from open_inwoner.openzaak.models import (
    OpenZaakConfig,
    ZaakTypeInformatieObjectTypeConfig,
)

from .api_models import Zaak
from .utils import cache as cache_result

logger = logging.getLogger(__name__)


@cache_result("information_object_url:{url}", timeout=settings.CACHE_ZGW_ZAKEN_TIMEOUT)
def fetch_single_information_object_url(url: str) -> Optional[InformatieObject]:
    return _fetch_single_information_object(url=url)


# not cached because currently only used in info-object download view
def fetch_single_information_object_uuid(uuid: str) -> Optional[InformatieObject]:
    return _fetch_single_information_object(uuid=uuid)


def _fetch_single_information_object(
    *, url: Optional[str] = None, uuid: Optional[str] = None
) -> Optional[InformatieObject]:
    if (url and uuid) or (not url and not uuid):
        raise ValueError("supply either 'url' or 'uuid' argument")

    client = build_client("document")

    if client is None:
        return

    try:
        if url:
            response = client.retrieve("enkelvoudiginformatieobject", url=url)
        else:
            response = client.retrieve("enkelvoudiginformatieobject", uuid=uuid)
    except RequestException as e:
        logger.exception("exception while making request", exc_info=e)
        return
    except ClientError as e:
        logger.exception("exception while making request", exc_info=e)
        return

    info_object = factory(InformatieObject, response)

    return info_object


def download_document(url: str) -> Optional[Response]:
    config = OpenZaakConfig.get_solo()
    client = config.document_service.build_client()
    if client is None:
        return

    service = config.document_service

    req_args = {}

    if client.auth:
        req_args["headers"] = client.auth.credentials()

    if service.server_certificate:
        req_args["verify"] = service.server_certificate.public_certificate.path

    if service.client_certificate:
        if service.client_certificate.private_key:
            req_args["cert"] = (
                service.client_certificate.public_certificate.path,
                service.client_certificate.private_key.path,
            )
        else:
            req_args["cert"] = service.client_certificate.public_certificate.path

    try:
        res = requests.get(url, **req_args)
        res.raise_for_status()
    except HTTPError as e:
        logger.exception("exception while making request", exc_info=e)
    else:
        return res


def upload_document(
    file: InMemoryUploadedFile, title: str, user_choice: int, source_organization: str
) -> dict:

    client = build_client("document")
    if client is None:
        return

    document_body = {
        "bronorganisatie": source_organization,
        "creatiedatum": date.today().strftime("%Y-%m-%d"),
        "titel": title,
        "auteur": "Open Inwoner Platform",
        "inhoud": base64.b64encode(file.read()).decode("utf-8"),
        "bestandsomvang": file.size,
        "bestandsnaam": file.name,
        "taal": "nld",
        "informatieobjecttype": ZaakTypeInformatieObjectTypeConfig.objects.get(
            id=user_choice
        ).informatieobjecttype_url,
    }

    try:
        response = client.create("enkelvoudiginformatieobject", document_body)
    except RequestException as e:
        logger.exception("exception while making request", exc_info=e)
        return
    except ClientError as e:
        logger.exception("exception while making request", exc_info=e)
        return

    return response
