from __future__ import annotations

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.utils.api import get_with_token, url_base
from anylearn.utils.errors import AnyLearnException


class ModelArtifact(Artifact):
    @classmethod
    def from_full_name(cls, full_name: str) -> ModelArtifact:
        res = get_with_token(
            f"{url_base()}/model/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnyLearnException("Request failed")
        return ModelArtifact(**res[0])
