import io
import json
import os
from logging import Logger
from typing import Optional
from pathlib import Path

from obs import ObsClient

from prefect.blocks.core import Block
from prefect.filesystems import WritableDeploymentStorage, WritableFileSystem
from pydantic import Field, SecretStr

from prefect.utilities.asyncutils import sync_compatible, run_sync_in_worker_thread
from prefect.utilities.filesystem import filter_files
from prefect.logging.loggers import get_logger, get_run_logger
from prefect.exceptions import MissingContextError


class ObsBlock(WritableFileSystem, WritableDeploymentStorage, Block):


    _logo_url = "https://res-static.hc-cdn.cn/cloudbu-site/public/header-icon/Storage/OBS.png"  # noqa
    _block_type_name = "HuaweiCloud Obs"
    _documentation_url = ("https://support.huaweicloud.com/intl/zh-cn/sdk-python-devg-obs/obs_22_0100.html")  # noqa

    huawei_cloud_access_key_id: Optional[SecretStr] = Field(
        default=None,
        description="A specific Huawei Cloud access key ID.",
        title="Huawei Cloud Access Key ID",
    )
    huawei_cloud_secret_access_key: Optional[SecretStr] = Field(
        default=None,
        description="A specific Huawei Cloud secret access key.",
        title="Huawei Cloud Access Key Secret",
    )
    huawei_cloud_security_token: Optional[SecretStr] = Field(
        default=None,
        description="SecurityToken in the temporary access key, "
                    "You can select a temporary token or AK/SK for authentication",
        title="Huawei Cloud Security Token",
    )
    end_point: str = Field(
        default="https://obs.cn-south-1.myhuaweicloud.com",
        description=(
            "Service address for connecting to OBS. The value can contain the protocol type, domain name, "
            "and port number. Example: https://your-endpoint:443. (For security purposes, HTTPS is recommended.)"
        ),
        title="End Point",
    )
    bucket: str = Field(
        default=None,
        description=(
            "Name of the bucket for creating a bucket client"
        ),
        title="Bucket",
    )

    prefix: Optional[str] = Field(
        default=None,
        description=(
            "Name prefix that the objects to be listed must contain. example: xxx/xxx. prefix cannot start with /"
        ),
        title="Prefix",
    )

    extra_params: Optional[str] = Field(
        default='{}',
        description=(
            "Additional parameters such as max_retry_count,"
            " max_redirect_count, and ssl_verify are written in JSON format,"
            " as shown in {'max_retry_count': 3,'max_redirect_count': 2}."
            "Detailed link: https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0601.html"
        ),
        title="Extra Params",
    )

    @property
    def logger(self) -> Logger:
        """
        Returns a logger based on whether the ObjectStorageBlock
        is called from within a flow or task run context.
        If a run context is present, the logger property returns a run logger.
        Else, it returns a default logger labeled with the class's name.

        Returns:
            The run logger or a default logger with the class's name.
        """
        try:
            return get_run_logger()
        except MissingContextError:
            return get_logger(self.__class__.__name__)

    @sync_compatible
    async def read_path(self, path: str) -> bytes:
        """
        Reading OBS File Objects
        Args:
            path: OBS File Object Key

        Returns: OBS File BytesIO

        """
        path = self._resolve_path(path)
        return await run_sync_in_worker_thread(self._download_file_object, path)

    @sync_compatible
    async def write_path(self, path: str, content: bytes) -> None:
        """
        Writing a File Object to OBS
        Args:
            path: OBS Storage Path
            content: File Object Flow
        Returns:

        """
        path = self._resolve_path(path)

        await run_sync_in_worker_thread(self._upload_file_object, path, content)

        return path

    @sync_compatible
    async def get_directory(
        self, from_path: str = None, local_path: str = None
    ) -> None:
        """
        Download all files from the folder path in the OBS bucket to the local path.
        Args:
            from_path: obs dir path
            local_path: local dir path

        Returns:

        """

        folder_path = self.prefix if not self.prefix == "/" else None
        if from_path is None:
            from_path = str(folder_path) if folder_path else None

        if local_path is None:
            local_path = str(Path("..").absolute())
        else:
            local_path = str(Path(local_path).expanduser())
        obs_client = self._get_obs_client()
        for path, is_dir in self._bucket_list_object(from_path):
            self.logger.info(path)
            target_path = os.path.join(
                local_path,
                path
            )
            target_path = os.path.normpath(target_path)
            if is_dir:
                os.makedirs(target_path, exist_ok=True)
                continue
            try:
                resp = obs_client.getObject(self.bucket, path, downloadPath=target_path)
                if resp.status < 300:
                    self.logger.info('requestId: %s', resp.requestId)
                else:
                    self.logger.error('errorCode: %s', resp.errorCode)
                    self.logger.error('errorMessage: %s', resp.errorMessage)
            except Exception as e:
                import traceback
                self.logger.error(traceback.format_exc())

    @sync_compatible
    async def put_directory(
        self, local_path: str = None, to_path: str = None, ignore_file: str = None
    ) -> int:
        """
        Pushes all files in the local folder to the specified folder in the OBS bucket.

        Args:
            local_path: Path to local directory to upload from.
            to_path: Path in OBS bucket to upload to. Defaults to block's configured
                basepath.
            ignore_file: Path to file containing gitignore style expressions for
                filepaths to ignore.
        Returns:

        """

        if local_path is None:
            raise Exception("local_path can't be None")

        local_path = os.path.normpath(local_path)
        included_files = None
        if ignore_file:
            with open(ignore_file, "r") as f:
                ignore_patterns = f.readlines()

            included_files = filter_files(local_path, ignore_patterns)

        uploaded_file_count = 0
        for local_file_path in Path(local_path).expanduser().rglob("*"):
            if (
                    included_files is not None
                    and str(local_file_path.relative_to(local_path)) not in included_files
            ):
                continue
            elif not local_file_path.is_dir():
                remote_file_path = Path(to_path) / local_file_path.relative_to(
                    local_path
                )
                with open(local_file_path, "rb") as local_file:
                    local_file_content = local_file.read()

                await self.write_path(
                    path=remote_file_path.as_posix(), content=local_file_content
                )
                uploaded_file_count += 1

        return uploaded_file_count

    def _get_obs_client(self) -> ObsClient:
        """
        The authenticated OBS client is returned. You can select a temporary token or AK/SK for authentication.
        Returns: ObsClient
        """
        extra_params = json.loads(self.extra_params)

        if self.huawei_cloud_security_token:
            return ObsClient(
                security_token=self.huawei_cloud_security_token.get_secret_value(),
                server=self.end_point,
                **extra_params
            )
        if not self.huawei_cloud_access_key_id or not self.huawei_cloud_secret_access_key:
            raise Exception("please input both huawei_cloud_access_key_id and huawei_cloud_secret_access_key")

        return ObsClient(
            access_key_id=self.huawei_cloud_access_key_id.get_secret_value(),
            secret_access_key=self.huawei_cloud_secret_access_key.get_secret_value(),
            server=self.end_point,
            **extra_params
            )

    def _resolve_path(self, path):
        """
        Concatenate the file object path based on the preset path prefix.

        Args:
            path: Path before splicing

        Returns: Path after splicing

        """

        path = (
            (Path(self.prefix) / path).as_posix() if self.prefix else path
        )

        return path

    def _download_file_object_inner(self, obs_client, key, stream):
        resp = obs_client.getObject(self.bucket, key, loadStreamInMemory=False)

        if resp.status < 300:
            self.logger.info('requestId: %s', resp.requestId)
            # 读取对象内容
            while True:
                chunk = resp.body.response.read(65536)
                if not chunk:
                    break
                stream.write(chunk)
            resp.body.response.close()
        else:
            self.logger.error('errorCode: %s', resp.errorCode)
            self.logger.error('errorMessage: %s', resp.errorMessage)

    def _download_file_object(self, key: str):
        """
        Downloading a File Object from OBS

        Args:
            key: OBS File Object Key

        Returns: OBS File BytesIO

        """
        obs_client = self._get_obs_client()
        with io.BytesIO() as stream:
            try:
                self._download_file_object_inner(obs_client, key, stream)
            except Exception as e:
                import traceback
                self.logger.error(traceback.format_exc())
            stream.seek(0)
            output = stream.read()
            obs_client.close()
            return output

    def _upload_file_object(self, path: str, data: bytes) -> None:
        """
        Uploading a File Object to OBS
        Args:
            path: OBS Storage Path
            data: File Object Flow

        Returns:

        """
        obs_client = self._get_obs_client()
        try:

            resp = obs_client.putContent(self.bucket, path, content=data)

            if resp.status < 300:
                self.logger.info('requestId: %s', resp.requestId)
            else:
                self.logger.error('errorCode: %s', resp.errorCode)
                self.logger.error('errorMessage: %s', resp.errorMessage)
        except Exception as e:
            import traceback
            self.logger.error(traceback.format_exc())

    def _bucket_list_object_inner(self, obs_client, prefix, mark, max_num):
        object_list = []
        resp = obs_client.listObjects(self.bucket, prefix=prefix, marker=mark, max_keys=max_num)
        self.logger.info(resp)
        if resp.status < 300:
            self.logger.info('requestId: %s', resp.requestId)
            index = 1
            for content in resp.body.contents:
                self.logger.info('object [%s]', str(index))
                index += 1
                if content.size == 0:
                    object_list.append((content.key, True))
                else:
                    object_list.append((content.key, False))
            if resp.body.is_truncated is True:
                return object_list, False, resp.body.next_marker
            else:
                return object_list, True, resp.body.next_marker
        else:
            self.logger.error('errorCode: %s', resp.errorCode)
            self.logger.error('errorMessage: %s', resp.errorMessage)
            return [], True, False

    def _bucket_list_object(self, prefix):
        """
        Querying All Objects in a Bucket
        Args:
            prefix: Path Prefix

        Returns: file object key and is dir bool

        """
        obs_client = self._get_obs_client()
        max_num = 1000
        mark = None
        all_object_list = []
        is_break = False
        try:
            while not is_break:
                object_list, is_break, mark = self._bucket_list_object_inner(obs_client, prefix, mark, max_num)
                all_object_list.extend(object_list)
        except Exception as e:
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            obs_client.close()
        return all_object_list
