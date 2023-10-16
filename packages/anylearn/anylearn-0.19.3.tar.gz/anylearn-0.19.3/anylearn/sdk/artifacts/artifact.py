import abc
import os
import time
import zipfile
from pathlib import Path
from typing import Optional, Union

import anylearn.env as env
from anylearn.config import AnylearnConfig
from anylearn.sdk.artifacts.compression import Compression
from anylearn.utils.api import url_base, get_with_token
from anylearn.utils.cmd import cmd_error, cmd_info
from anylearn.utils.errors import (
    AnyLearnException,
    AnyLearnNotSupportedException,
)
from anylearn.utils.util import ensure_dir


class Artifact(abc.ABC):
    """
    Attributes
    ----------
    id
        资源的唯一标识符，自动生成，由类名前四位+uuid1生成的编码中后28个有效位（小写字母和数字）组成（自动生成）
    name
        资源的名称（长度1~50）
    description
        资源描述（长度最大255）
    state
        资源状态
    public
        数据集是否为公开（默认为False）
    upload_time
        资源上传时间
    filename
        下一步中会被分片上传的资源的完整名（包括扩展名）
    is_zipfile
        是否为zip文件
    file_path
        资源文件路径
    size
        资源文件大小
    creator_username
        创建者用户名
    """

    """具体资源信息配置"""
    _fields = {
        # 资源创建/更新请求包体中必须包含且不能为空的字段
        'required': {
            'create': ['name', 'filename'],
            'update': ['id', 'name'],
        },
        # 资源创建/更新请求包体中包含的所有字段
        'payload': {
            'create': ['name', 'description', 'public', 'owner',
                       'filename'],
            'update': ['id', 'name', 'description', 'public', 'owner'],
        },
    }

    def __init__(self, *_, **kwargs):
        """
        Parameters
        ----------
        load_detail
            初始化时是否加载详情
        """
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)
        self.description = kwargs.pop('description', None)
        self.state = kwargs.pop('state', None)
        self.public = kwargs.pop('public', False)
        self.uploaded_at = kwargs.pop('upload_time', None)
        self.size = kwargs.pop('size', None)
        self.creator_username = kwargs.pop('creator_username', None)
        self.__original_filename = kwargs.pop('filename', None)
        self.__original_is_zipfile = kwargs.pop('is_zipfile', None)

    def ls(self, sub_path: str=None):
        """
        查询文件列表

        Parameters
        ----------
        sub_path : :obj:`str`
            资产文件目录内的子路径（相对路径），默认为空，即资产根目录
        """
        if not self.id:
            cmd_error("Artifact ID is required")
        return get_with_token(
            f"{url_base()}/resource/listdir",
            params={
                'file_id': self.id,
                'subpath': sub_path,
            },
        )

    def upload(self, path: Union[os.PathLike, str]) -> bool:
        raise AnyLearnNotSupportedException

    def download(
        self,
        dest_dir: Optional[Union[os.PathLike, str]]=None,
        sub_path: Optional[str]=None,
    ) -> str:
        if not self.id:
            cmd_error("Artifact ID is required")
        local_path = self._get_local_path_from_env()
        if not local_path:
            archive_path = self.compress_and_download(sub_path=sub_path)
            root_dir = dest_dir or (
                AnylearnConfig.workspace_path / "artifacts"
            )
            ensure_dir(root_dir)
            with zipfile.ZipFile(archive_path, "r") as zip_handle:
                zip_handle.extractall(root_dir)
            local_path = str(root_dir / self.id)
        return local_path

    def _get_local_path_from_env(self) -> Optional[Path]:
        paths = env.get_artifact_paths()
        return paths.get(self.id, None)

    def compress_and_download(
        self,
        dest_dir: Optional[Union[os.PathLike, str]]=None,
        sub_path: Optional[str]=None,
        polling: Union[float, int]=5,
    ) -> Path:
        cmd_info("Compressing...")
        t_elapsed = 0
        compression = Compression.create(self.id, sub_path)
        while not compression.ready_to_download():
            time.sleep(polling)
            t_elapsed += polling
            compression.reload()
            if compression.on_error():
                raise AnyLearnException('Compression failed')
            elif t_elapsed % 10 == 0:
                cmd_info(
                    "| Still waiting compression to be ready "
                    f"({t_elapsed}s)"
                )

        cmd_info("Downloading...")
        return compression.download(dest_dir)

    def __repr__(self) -> str:
        d = self.__dict__
        kv = ", ".join([f"{k}={d[k]!r}" for k in d])
        return f"{self.__class__.__name__}({kv})"

    def __str__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" fullname={self.creator_username}/{self.name}"
            ">"
        )


class ArtifactState:
    """
    资产状态标识：

    - 1(CREATED)表示已创建
    - 2(UPLOADING)表示上传中
    - 3(READY)表示就绪
    - -1(DELETED)表示已删除
    - -2(ERROR)表示出错
    """
    CREATED = 1
    UPLOADING = 2
    READY = 3
    DELETED = -1
    ERROR = -2
