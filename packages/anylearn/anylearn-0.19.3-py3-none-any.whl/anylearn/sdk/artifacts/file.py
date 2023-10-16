from __future__ import annotations

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.utils.api import get_with_token, url_base
from anylearn.utils.errors import AnyLearnException


class FileArtifact(Artifact):
    @classmethod
    def from_id(cls, id_: str) -> FileArtifact:
        res = get_with_token(
            f"{url_base()}/file/query",
            params={'id': id_},
        )
        if not res or not isinstance(res, list):
            raise AnyLearnException("Request failed")
        return FileArtifact(**res[0])
