from __future__ import annotations

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.utils.api import get_with_token, url_base
from anylearn.utils.errors import AnyLearnException


class DatasetArtifact(Artifact):
    @classmethod
    def from_full_name(cls, full_name: str) -> DatasetArtifact:
        res = get_with_token(
            f"{url_base()}/dataset/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnyLearnException("Request failed")
        return DatasetArtifact(**res[0])
