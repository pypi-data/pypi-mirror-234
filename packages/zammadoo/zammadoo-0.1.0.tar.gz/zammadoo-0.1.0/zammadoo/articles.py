#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base64 import b64encode
from datetime import datetime
from mimetypes import guess_type
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Iterator, cast

import requests

from .resource import Resource
from .resources import Creatable, ResourcesT

if TYPE_CHECKING:
    from .client import Client
    from .tickets import Ticket
    from .types import JsonDict, PathType


class Attachment:
    id: int  #:
    filename: str  #:
    preferences: Dict[str, Any]  #:
    size: int  #:
    store_file_id: int  #:

    def __init__(self, client: "Client", content_url: str, info: "JsonDict") -> None:
        self._client = client
        self._url = content_url
        self._info = info

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self._url!r}>"

    def __getattr__(self, item):
        return self._info[item]

    @staticmethod
    def info_from_files(*paths: "PathType"):
        info_list = []
        for path in paths:
            filepath = Path(path)
            assert filepath.is_file()
            mime_type, _encoding = guess_type(filepath, strict=True)
            info_list.append(
                {
                    "filename": filepath.name,
                    "data": b64encode(filepath.read_bytes()),
                    "mime-type": mime_type,
                }
            )
        return info_list

    def view(self) -> MappingProxyType[str, Any]:
        return MappingProxyType(self._info)

    @property
    def url(self) -> str:
        return self._url

    def _response(self, encoding: Optional[str] = None) -> requests.Response:
        response = self._client.response("GET", self._url, stream=True)
        response.raise_for_status()
        if encoding:
            response.encoding = encoding

        return response

    def download(self, path: "PathType" = ".") -> "Path":
        filepath = Path(path)
        if filepath.is_dir():
            filepath = filepath / self.filename

        with filepath.open("wb") as fd:
            for chunk in self.iter_bytes():
                fd.write(chunk)

        return filepath

    def read_bytes(self) -> bytes:
        return self._response().content

    def read_text(self) -> str:
        return self._response(self.encoding).text

    @property
    def encoding(self) -> Optional[str]:
        preferences = cast(Dict[str, str], self._info.get("preferences", {}))
        return preferences.get("Charset")

    def iter_text(self, chunk_size=8192):
        response = self._response(encoding=self.encoding)
        assert response.encoding, "content is binary only, use .iter_bytes() instead"
        return response.iter_content(chunk_size=chunk_size, decode_unicode=True)

    def iter_bytes(self, chunk_size=8192) -> Iterator[bytes]:
        return self._response().iter_content(chunk_size=chunk_size)


class Article(Resource):
    body: str  #:
    cc: Optional[str]  #:
    content_type: str  #:
    created_at: datetime  #:
    created_by: str  #:
    from_: str  #:
    internal: bool  #:
    message_id: Optional[str]  #:
    message_id_md5: Optional[str]  #:
    subject: Optional[str]  #:
    to: Optional[str]  #:
    updated_at: datetime  #:
    updated_by: str  #:

    @property
    def ticket(self) -> "Ticket":
        return self.parent.client.tickets(self["ticket_id"])

    @property
    def attachments(self) -> List[Attachment]:
        attachment_list = []
        client = self.parent.client
        for info in self["attachments"]:
            url = f"{client.url}/ticket_attachment/{self['ticket_id']}/{self._id}/{info['id']}"
            attachment = Attachment(client, url, info)
            attachment_list.append(attachment)
        return attachment_list


class Articles(Creatable[Article], ResourcesT[Article]):
    RESOURCE_TYPE = Article

    def __init__(self, client: "Client"):
        super().__init__(client, "ticket_articles")

    def by_ticket(self, tid: int) -> List[Article]:
        items = self.client.get(self.endpoint, "by_ticket", tid)
        return [self(item["id"], info=item) for item in items]

    def create(self, ticket_id: int, body: str, **kwargs) -> Article:
        info = {
            "ticket_id": ticket_id,
            "body": body,
            **kwargs,
        }
        return super()._create(info)
