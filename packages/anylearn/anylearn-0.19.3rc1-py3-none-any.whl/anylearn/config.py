from pathlib import Path
import requests
import shutil

from anylearn.utils import logger
from anylearn.utils.errors import InvalidArguments, AnyLearnAuthException


class AnylearnConfig(object):
    """
    Anylearn SDK配置类，
    包含Anylearn后端引擎的连接配置和SDK的本地存储配置。
    """

    cluster_address = None
    """Anylearn后端引擎集群网关地址"""

    username = None
    """Anylearn后端引擎账户用户名"""

    user_id = None
    """Anylearn后端引擎账户ID"""

    password = None
    """Anylearn后端引擎账户密码"""

    token = None
    """Anylearn后端引擎API令牌"""

    refresh_token = None
    """Anylearn后端引擎API令牌刷新令牌"""

    workspace_path = Path().home() / ".anylearn"
    """SDK本地存储工作区路径"""

    git_ready = False

    @classmethod
    def init(cls, cluster_address=None, username=None, password=None,
             token=None, workspace=None, disable_git=False):
        """
        初始化SDK与后端连接以及本地存储。
        可通过用户名密码建立后端连接，也可直接传入有效的后端API令牌。
        
        Parameters
        ----------
        cluster_address : :obj:`str`, optional
            Anylearn后端引擎集群网关地址。
        username : :obj:`str`, optional
            Anylearn后端引擎账户用户名。
        password : :obj:`str`, optional
            Anylearn后端引擎账户密码。
        token : :obj:`str`, optional
            Anylearn后端引擎API令牌。
        workspace : :obj:`str`, optional
            SDK本地存储工作区路径，
            默认将工作区建立在 :obj:`<home>/.anylearn` 目录下。
        disable_git : :obj:`bool`, optional
            是否禁用基于本地git的算法同步，
            默认为否。
        """
        # Cluster Auth
        cls.init_cluster(cluster_address, username, password, token)
        # Local workspace
        cls.init_workspace(workspace)
        # Detect git
        cls.git_ready = not disable_git and cls.check_git()

    @classmethod
    def init_cluster_by_token(
        cls,
        host: str,
        token: str,
        refresh_token: str,
    ) -> None:
        if host.endswith("/"):
            host = host[:-1]
        cls.cluster_address = host
        cls.token = token
        cls.refresh_token = refresh_token
        cls.cluster_login_by_token()

    @classmethod
    def init_cluster(cls, cluster_address=None, username=None, password=None,
                     token=None):
        """
        仅初始化SDK与后端连接。
        可通过用户名密码建立后端连接，也可直接传入有效的后端API令牌。
        
        Parameters
        ----------
        cluster_address : :obj:`str`, optional
            Anylearn后端引擎集群网关地址。
        username : :obj:`str`, optional
            Anylearn后端引擎账户用户名。
        password : :obj:`str`, optional
            Anylearn后端引擎账户密码。
        token : :obj:`str`, optional
            Anylearn后端引擎API令牌。
        """
        if not all([
            cluster_address,
            isinstance(cluster_address, str),
            any([username and password, token]),
        ]):
            raise InvalidArguments('无有效登录配置')
        if cluster_address.endswith('/'):
            cluster_address = cluster_address[:-1]
        cls.cluster_address = cluster_address
        cls.username = username
        cls.password = password
        cls.token = token
        if token is None:
            cls.cluster_login()
    
    @classmethod
    def cluster_login(cls):
        """
        通过用户名密码建立SDK与后端连接，
        获取后端API令牌。
        在以用户名密码的方式初始化后方可调用。
        """
        res = requests.post('%s/api/user/login' % cls.cluster_address, {
            'username': cls.username,
            'password': cls.password,
        })
        if res.status_code == 200:
            res = res.json()
            cls.token = res['token']
            cls.refresh_token = res['refresh_token']
            cls.user_id = res['id']
            cls.username = res['username']
        else:
            raise AnyLearnAuthException()

    @classmethod
    def cluster_login_by_token(cls) -> None:
        if not cls.token:
            raise InvalidArguments(f"Cannot login with empty token")
        headers = {'Authorization': f"Bearer {cls.token}"}
        res = requests.get(
            f"{cls.cluster_address}/api/user/me",
            headers=headers,
        )
        if res.status_code == 200:
            res = res.json()
            cls.user_id = res['id']
            cls.username = res['username']
        elif cls.refresh_token:
            cls.cluster_relogin_by_token()
        else:
            raise AnyLearnAuthException()

    @classmethod
    def cluster_relogin_by_token(cls) -> None:
        if not cls.refresh_token:
            raise InvalidArguments(f"Cannot relogin with empty refresh token")
        headers = {'Authorization': f"Bearer {cls.refresh_token}"}
        res = requests.get(
            f"{cls.cluster_address}/api/user/refresh_token",
            headers=headers,
        )
        if res.status_code == 200:
            res = res.json()
            cls.token = res['token']
        else:
            raise AnyLearnAuthException()

    @classmethod
    def init_workspace(cls, workspace=None):
        """
        仅初始化SDK本地存储。
        
        Parameters
        ----------
        workspace : :obj:`str`, optional
            SDK本地存储工作区路径，
            默认将工作区建立在 :obj:`<home>/.anylearn` 目录下。
        """
        cls.workspace_path = Path(workspace) if workspace \
                                             else cls.workspace_path
        # Remove if workspace path points to a file
        if cls.workspace_path.is_file():
            cls.workspace_path.unlink()
        # Ensure workspace folder exists
        cls.workspace_path.mkdir(exist_ok=True)

    @classmethod
    def clear_workspace(cls):
        """
        清空SDK本地存储。
        本地元信息存储、临时文件、资源缓存等均会被删除。
        请谨慎调用。
        """
        shutil.rmtree(cls.workspace_path)

    @classmethod
    def check_git(cls):
        try:
            from git import Repo
            return True
        except:
            logger.warning("Git executable not found.")
            cls.git_ready = False
            return False


def init_sdk(cluster_address, username, password, disable_git=False):
    """
    初始化SDK与后端连接的接口。
    调用本接口并传入后端地址、用户名和密码，
    SDK将自动以相应账户进行登录并获取后端API令牌。

    Parameters
    ----------
    cluster_address : :obj:`str`
        Anylearn后端引擎集群网关地址。
    username : :obj:`str`
        Anylearn后端引擎账户用户名。
    password : :obj:`str`
        Anylearn后端引擎账户密码。
    """
    AnylearnConfig.init(
        cluster_address=cluster_address,
        username=username,
        password=password,
        disable_git=disable_git,
    )


def init_sdk_incontainer(cluster_address):
    """
    初始化无鉴权信息的SDK与后端连接的接口。
    调用本接口仅需传入后端地址，
    无需账户信息。
    以此方式初始化的SDK将无法调用需要鉴权信息的接口，
    仅可调用无需API令牌的公共接口。

    此接口的使用场景多为任务执行容器内与后端建立通信，
    不建议用户使用。

    Parameters
    ----------
    cluster_address : :obj:`str`
        Anylearn后端引擎集群网关地址。
    """
    AnylearnConfig.init(
        cluster_address=cluster_address,
        token="INCONTAINER"
    )


def print_config():
    print(AnylearnConfig.cluster_address)
