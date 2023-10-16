from __future__ import annotations

from anylearn.utils.api import get_with_token, url_base
from anylearn.utils.errors import AnyLearnException


class Project:
    """
    AnyLearn训练项目类

    Attributes
    ----------
    id
        项目的唯一标识符，自动生成，由PROJ+uuid1生成的编码中后28个有效位（小写字母和数字）组成
    name
        项目名称（非空 长度1~50）
    description
        项目描述（可为空 长度最大255）
    created_at
        创建时间
    updated_at
        更新时间
    creator_id
        创建者的ID
    creator_username
    """

    def __init__(self, *_, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created_at = kwargs.get('create_time', None)
        self.updated_at = kwargs.get('update_time', None)
        self.creator_id = kwargs.get('creator_id', None)
        self.creator_username = kwargs.get('creator_username', None)

    @classmethod
    def from_full_name(cls, full_name: str) -> Project:
        res = get_with_token(
            f"{url_base()}/project/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnyLearnException("Request failed")
        return Project(**res[0])
