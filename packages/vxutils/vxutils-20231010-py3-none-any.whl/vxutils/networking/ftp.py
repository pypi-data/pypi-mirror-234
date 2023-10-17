"""ftp网络链接 """


import os
import time
import contextlib
from multiprocessing import Lock
from ftplib import FTP, all_errors, Error as FTPError, FTP_TLS
from vxutils import logger
from vxutils.decorators import retry


class vxFTPConnector:
    """FTP网络连接器"""

    def __init__(
        self,
        host: str = "",
        port: int = 21,
        user: str = "",
        passwd: str = "",
        keyfile: str = "",
    ):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._timeout = 0
        self._lock = Lock()
        self._ftp = None
        self._keyfile = keyfile

    @retry(3)
    def login(self):
        """登录ftp服务器"""

        if self._ftp:
            self.logout()

        try:
            self._ftp = FTP() if self._keyfile else FTP_TLS(keyfile=self._keyfile)

            self._ftp.encoding = "GB2312"
            self._ftp.connect(self._host, self._port)
            self._ftp.login(self._user, self._passwd)
            time.sleep(0.1)
            logger.debug("ftp login Success. %s", self._ftp.pwd())
            self._timeout = time.time() + 60
            return True
        except all_errors as err:
            logger.error("ftp login error.%s", err)
            return False

    def __str__(self) -> str:
        return f"ftp://{self._user}@{self._host}:{self._port}/"

    __repr__ = __str__

    def logout(self):
        """登出ftp服务器"""
        try:
            with self._lock:
                self._ftp.quit()

        except all_errors as err:
            logger.error("ftp logout error: %s", err)
        finally:
            self._ftp = None
            self._timeout = 0

    @contextlib.contextmanager
    def autologin(self):
        """自动登录ftp服务器"""
        now = time.time()
        wait_to_retry = 0.3
        with self._lock:
            for i in range(1, 6):
                if self._ftp and now <= self._timeout:
                    break
                elif self._ftp:
                    with contextlib.suppress(all_errors):
                        self._ftp.pwd()
                        self._timeout = now + 60
                        break

                if self.login():
                    break
                wait_to_retry = min(wait_to_retry + i * 0.3, 3)

                if i >= 5:
                    raise FTPError("ftp connect error ...")

                logger.info(
                    "auto login  wait %s to retry the %dth times ...", wait_to_retry, i
                )
                time.sleep(wait_to_retry)

            try:
                yield self._ftp
                self._timeout = time.time() + 60
            except all_errors as err:
                self._timeout = 0
                logger.info("FTP Error occur: %s", err)

    def mkdir(self, remote_dir):
        """创建远程目录"""

        with self.autologin():
            self._ftp.mkd(remote_dir)
            logger.debug("ftp mkdir Success. %s", remote_dir)
        return self._timeout > 0

    def rmdir(self, remote_dir):
        """删除远程目录"""

        with self.autologin():
            self._ftp.rmd(remote_dir)
            logger.debug("ftp rmdir Success. %s", remote_dir)
        return self._timeout > 0

    def list(self, remote_dir):
        """list远程目录"""
        with self.autologin():
            remote_files = self._ftp.nlst(remote_dir)
        return (
            [os.path.join(remote_dir, remote_file) for remote_file in remote_files]
            if self._timeout > 0
            else []
        )

    def download(self, remote_file, local_file):
        """FTP下载文件

        Arguments:
            remote_file -- 远程文件路径
            local_file -- 本地文件目录_

        Returns:
            False -- 下载失败
            True  -- 下载成功
        """

        with self.autologin():
            if isinstance(local_file, str):
                with open(local_file, "wb") as fp:
                    self._ftp.retrbinary(f"RETR {remote_file}", fp.write)
            else:
                fp = local_file
                self._ftp.retrbinary(f"RETR {remote_file}", fp.write)
        return self._timeout > 0

    def upload(self, local_file, remote_file):
        """上传本地文件

        Arguments:
            local_file -- 本地文件
            remote_file -- 远程文件

        Returns:
            True -- 上传成功
            False -- 上传失败
        """

        with self.autologin():
            if isinstance(local_file, str):
                with open(local_file, "rb") as fp:
                    self._ftp.storbinary(f"STOR {remote_file}", fp)
            else:
                fp = local_file
                self._ftp.storbinary(f"STOR {remote_file}", fp)
        return self._timeout > 0

    def delete(self, remote_file):
        """删除ftp文件

        Arguments:
            remote_file -- 远程文件

        Returns:
            True -- 删除成功
            False -- 删除失败
        """

        with self.autologin():
            self._ftp.delete(remote_file)
        return self._timeout > 0

    def __eq__(self, __o: object) -> bool:
        return (
            (
                self._host == __o._host
                and self._port == __o._port
                and self._user == __o._user
                and self._passwd == __o._passwd
            )
            if isinstance(__o, vxFTPConnector)
            else False
        )
