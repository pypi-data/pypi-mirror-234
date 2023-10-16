import os
import sys
import io
import tempfile
import subprocess
import requests
from concurrent import futures
from functools import partial
from contextlib import contextmanager
from typing import Optional, Generator, BinaryIO, Union, List
from pathlib import Path
from filelock import FileLock
from tqdm import tqdm
from urllib.parse import urlparse, urlunparse
from fnmatch import fnmatch
# from requests.adapters import Retry


from scoamp.globals import global_api as api
from scoamp.globals import Environment
from scoamp.utils.error import FileDownloadError, APIError, SubprocessError
from scoamp.utils.logger import get_logger

_mswindows = (sys.platform == "win32")

# constants
API_FILE_DOWNLOAD_RETRY_TIMES = 3
API_FILE_DOWNLOAD_TIMEOUT = 60 * 5
API_FILE_DOWNLOAD_READ_CHUNK_SIZE = 1 * 1024 * 1024
API_FILE_DOWNLOAD_PARALLEL_THRESHOLD = 500 * 1024 * 1024
API_FILE_DOWNLOAD_PARALLELS = 4
API_FILE_DOWNLOAD_PARALLEL_PART_SIE = 200 * 1024 * 1024

logger = get_logger()


def model_file_list(
    model_id: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
) -> list:
    """List all files in a model recursively
    Args:
        model_id (`str`):
            model id.
        is_public (`bool`):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.

    Returns:
        flatten file list
    """
    if is_public:
        return api.list_public_model_files(model_id, revision)
    else:
        return api.list_user_model_files(model_id, revision)


# TODO local cache system
def model_file_download(
    model_id: str,
    file_path: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
    local_dir: Optional[str] = None,
    force_download: bool = False,
    resume_download: bool = False,
    remote_validate: bool = True,
    parallels: int = API_FILE_DOWNLOAD_PARALLELS,
) -> str:
    """Download a given file from amp server
    Args:
        model_id (`str`):
            model id.
        file_path (`str`):
            file path in the repo, with subfolder.
        is_public (`bool`, *optional*):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.
        local_dir (`str` or `Path`, *optional*):
            If provided, the downloaded file will be placed under this directory
        force_download (`bool`, *optional*, defaults to `False`):
            Whether the file should be downloaded even if it already exists in
            the local dir.
        resume_download (`bool`, *optional*, defaults to `False`):
            If `True`, resume a previously interrupted download.
        remote_validate (`bool`, *optional*, defaults to `True`):
            If `True`, validate remote model access and file exists before downloading
        parallels(`int`, *optional*, defaults to `4`):
            if set to > 1, will use parallel downloading, and must set `resume_download` to `False` at the same time,
            otherwise Exception will be raised.

    Returns:
        Local path (string) of file
    """
    if parallels:
        if not isinstance(parallels, int):
            raise ValueError('parallel shoud be int type')
        if parallels < 1:
            parallels = 1
        elif parallels > API_FILE_DOWNLOAD_PARALLELS:
            parallels = API_FILE_DOWNLOAD_PARALLELS
    else:
        parallels = 1

    if parallels > 1 and resume_download:
        raise ValueError('condition conflict: parallels > 1 while set resume_download=True')

    if not model_id:
        raise ValueError('model_id shoud not be empty')

    if not file_path:
        raise ValueError('file_path should not be empty')

    if not local_dir:
        local_dir = '.'
    local_dir = Path(local_dir).expanduser()
    if not local_dir.exists():
        raise ValueError(f"local directory '{local_dir}' not exists")

    local_file_path = local_dir / file_path
    if local_file_path.exists() and not force_download:
        raise ValueError(f"'{file_path}' already exists at local, set 'force_download=True' to overwrite")

    if remote_validate:
        flag = False
        model_files = model_file_list(model_id, is_public=is_public, revision=revision)
        for mf in model_files:
            if mf['path'] == file_path:
                if mf['file_type'] == 'FileType_Dir':
                    raise ValueError(f"'{file_path}' is a remote direcotry, not a file path")
                flag = True
                break
        if not flag:
            raise ValueError(f"remote file '{file_path}' not exists, or you have no access permission")

    local_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Prevent parallel downloads of the same file with a lock.
    lock_path = Path(str(local_file_path) + ".lock")
    temp_file_name = None
    try:
        with FileLock(lock_path):
            if resume_download:
                incomplete_path = Path(str(local_file_path) + ".incomplete")

                @contextmanager
                def _resumable_file_manager() -> Generator[io.BufferedWriter, None, None]:
                    with open(incomplete_path, "ab") as f:
                        yield f

                temp_file_manager = _resumable_file_manager
            else:
                temp_file_manager = partial(  # type: ignore
                    tempfile.NamedTemporaryFile, mode="wb", dir=local_dir, delete=False
                )

            # Download to temporary file, then copy to local dir once finished.
            # Otherwise you get corrupt entries if the download gets interrupted.
            with temp_file_manager() as temp_file:
                temp_file_name = temp_file.name
                _http_get_model_file(
                    temp_file,
                    model_id,
                    file_path,
                    is_public=is_public,
                    revision=revision,
                    parallels=parallels,
                )

            os.replace(temp_file.name, local_file_path)
    finally: # gc
        # clear lock file
        try:
            lock_path.unlink()
        except OSError:
            pass

        # clear temp file
        if not resume_download and os.path.exists(temp_file_name):
            os.remove(temp_file_name)

    return str(local_file_path)


def _http_get_model_file(
    temp_file: BinaryIO,
    model_id: str,
    file_path: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
    parallels: int = 1,
):
    # TODO retry policy
    ## retry sleep 0.5s, 1s, 2s
    #retry = Retry(
    #    total= API_FILE_DOWNLOAD_RETRY_TIMES,
    #    backoff_factor=1,
    #    allowed_methods=['GET'])

    downloaded_size = temp_file.tell()
    if downloaded_size > 0 and parallels > 1:
        raise ValueError(f'conflict condition: parallels > 1 while using resume downloading')

    r = api.download_file(
        model_id,
        file_path,
        revision=revision,
        is_public=is_public,
        resume_size=downloaded_size,
        allow_redirects=False,
        timeout=API_FILE_DOWNLOAD_TIMEOUT,
    )

    parallel_flag = False
    real_url = ''
    if r.status_code < 300:
        content_length = r.headers.get('Content-Length')
    else:
        # LFS file
        content_length = r.headers['X-Linked-Size']
        real_url = r.headers['Location']
        if int(content_length) <= API_FILE_DOWNLOAD_PARALLEL_THRESHOLD or parallels <= 1:
            r = requests.get(real_url, stream=True, timeout=API_FILE_DOWNLOAD_TIMEOUT)
            r.raise_for_status()
        else:
            parallel_flag = True

    total = downloaded_size + int(content_length) if content_length is not None else None

    desc_file_name = file_path
    if len(desc_file_name) > 22:
        desc_file_name = f"(…){desc_file_name[-20:]}"

    progress = tqdm(
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        total=total,
        initial=downloaded_size,
        desc=f'Downloading {desc_file_name}',
        ascii='.#',
    )
    if not parallel_flag:
        for chunk in r.iter_content(chunk_size=API_FILE_DOWNLOAD_READ_CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                temp_file.write(chunk)
                progress.update(len(chunk))
        temp_file.flush()
    else:
        # parallel download
        def _download_part(start, end):
            headers = {}
            headers['Range'] = 'bytes=%s-%s' % (start, end)
            with open(temp_file.name, 'rb+') as f:
                f.seek(start)
                r = requests.get(real_url, stream=True, headers=headers, allow_redirects=True, timeout=API_FILE_DOWNLOAD_TIMEOUT)
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=API_FILE_DOWNLOAD_READ_CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        progress.update(len(chunk))
                f.flush()

        executor = futures.ThreadPoolExecutor(max_workers=parallels)
        part_size = API_FILE_DOWNLOAD_PARALLEL_PART_SIE 
        tasks = []
        for i in range(int((total + part_size - 1) / part_size)):
            start = i * part_size
            end = start + part_size - 1
            tasks.append(executor.submit(_download_part, start, end))

        # wait for first exception or all completed
        done, _ = futures.wait(tasks, return_when=futures.FIRST_EXCEPTION)

        # raise from failed task
        try:
            for task in done:
                task.result()
        except Exception as exc:
            # set err flag to notice running futures to terminate immediatly
            executor.shutdown(wait=False)
            raise exc
        else:
            executor.shutdown(wait=True)

    progress.close()

    downloaded_length = os.path.getsize(temp_file.name)
    if total and total != downloaded_length:
        msg = f"download file '{file_path}' from model '{model_id}' error: expect file size is '{total}', but download size is '{downloaded_length}'"
        raise FileDownloadError(msg)

    return downloaded_length


# TODO
#   1. parallel download
#   2. cache system
def snapshot_download(
    model_id: str,
    local_dir: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
    force_download: bool = False,
    resume_download: bool = False,
    ignore_patterns: Optional[Union[List[str], str]] = None,
    parallels: int = API_FILE_DOWNLOAD_PARALLELS,
) -> str:
    """Download repo files.

    Download a whole snapshot of a repo's files at the specified revision. This is useful when you want all files from
    a repo, because you don't know which ones you will need a priori. All files are nested inside a folder in order
    to keep their actual filename relative to that folder. You can also filter which files to download using
    `allow_patterns` and `ignore_patterns`.

    An alternative would be to clone the repo but this requires git and git-lfs to be installed and properly
    configured. It is also not possible to filter which files to download when cloning a repository using git.

    Args:
        model_id (`str`):
            model_id
        local_dir (`str` or `Path`, *optional*):
            the downloaded files will be placed under this directory
        is_public (`bool`, *optional*):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.
        force_download (`bool`, *optional*, defaults to `False`):
            Whether the file should be downloaded even if it already exists in the local dir.
        resume_download (`bool`, *optional*, defaults to `False):
            If `True`, resume a previously interrupted download.
        ignore_patterns (`List[str]` or `str`, *optional*):
            If provided, files matching any of the patterns are not downloaded.
        parallels(`int`, *optional*, defaults to `4`):
            if set to > 1, will use parallel downloading, and must set `resume_download` to `False` at the same time,
            otherwise Exception will be raised.

    Returns:
        Local folder path (string) of repo snapshot

    <Tip>

    Raises the following errors:

    - [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
      if `token=True` and the token cannot be found.
    - [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError) if
      ETag cannot be determined.
    - [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
      if some parameter value is invalid

    </Tip>
    """
    if parallels:
        if not isinstance(parallels, int):
            raise ValueError('parallel shoud be int type')
        if parallels < 1:
            parallels = 1
        elif parallels > API_FILE_DOWNLOAD_PARALLELS:
            parallels = API_FILE_DOWNLOAD_PARALLELS
    else:
        parallels = 1

    if parallels > 1 and resume_download:
        raise ValueError('condition conflict: parallels > 1 while set resume_download=True')

    if not model_id:
        raise ValueError('model_id shoud not be empty')

    if not local_dir:
        raise ValueError('local_dir shoud be specified')
    local_dir_path = Path(local_dir).expanduser()
    # TODO: whether allow local_dir exists
    if not local_dir_path.exists():
        local_dir_path.mkdir()

    if not ignore_patterns:
        ignore_patterns = []
    elif isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]

    model_files = model_file_list(model_id, is_public=is_public, revision=revision)

    for model_file in model_files:
        if model_file['file_type'] == 'FileType_Dir' or \
                any([fnmatch(model_file['name'], pattern) for pattern in ignore_patterns]):
            # TODO add log
            continue

        file_path = model_file['path']
        local_file_path = local_dir_path / file_path
        # check model_file exists, if exists and force_download=False, then skip, otherwise download
        if not force_download and local_file_path.exists():
            # TODO add more accurate check
            if local_file_path.stat().st_size != int(model_file['size_bytes']):
                raise FileExistsError(f"file '{file_path}' exists and different from remote server, you can set 'force_download=True' to override it")
            else:
                continue

        model_file_download(
            model_id,
            file_path,
            is_public=is_public,
            revision=revision,
            local_dir=local_dir,
            force_download=force_download,
            resume_download=resume_download,
            remote_validate=False,
            parallels=parallels,
        )
    return local_dir


def create_and_upload_model(
    model_id: str,
    local_dir: str,
    model_space_name: str,
    allow_exist: bool = False,
) -> str:
    """Create a new model and upload files from local directory

    `local_dir` should contains all the model files, and must not have a '.git' directory in it (not a git repo).
    This method will use 'git' and 'git-lfs' to init the local dir, and push to remote server, then de-init by remove '.git'.

    Args:
        model_id (`str`):
            model id/name
        local_dir (`str` or `Path`, *optional*):
            all model files should be placed under this directory
        model_space_name (`str`):
            model space name in AMP platform
        allow_exist (`bool`):
            if remote repo with given 'model_id' has been create before and no files uploaded yet, reuse it.

    Returns:
        remote repo path
    """
    if not isinstance(model_id, str):
        raise ValueError("'model_id' should be string type")
    if not model_space_name:
        raise ValueError("'model_space_name' should not be None or empty")
    if not local_dir:
        raise ValueError('local_dir shoud be specified')
    local_dir_path = Path(local_dir).expanduser().absolute()
    if not local_dir_path.exists():
        raise FileNotFoundError(f"local directory '{local_dir}' not exists")

    if len(os.listdir(local_dir_path)) == 0:
        raise ValueError(f"local_dir '{local_dir}' is empty")

    # ensure local dir not a git repo
    for fn in ['.git', '.gitattributes']:
        if (local_dir_path / fn).exists():
            raise FileExistsError(f"local dir should not contains '{fn}'")

    # check git/lfs install
    Environment.check_git_and_lfs()

    # check whether model with given 'model_id' exists at amp
    try:
        model_info = api.get_user_model_info(model_id)
        if not allow_exist:
            raise ValueError(f"model id '{model_id}' has been exists at amp")
        files = model_file_list(model_id)
        # ensure has only one file, and must named '.gitattributes'
        if len(files) != 1 or files[0]['path'] != '.gitattributes':
            raise ValueError(f"invalid remote model repo '{model_id}': has more than one file")
        logger.warning("model has been created on AMP before, resuse it!")
    except APIError as err:
        if err.status_code != 404: raise
        # create a new one
        model_info = api.create_user_model(model_id, model_space_name)
    git_url = model_info['repository_uri']
    logger.info(f"remote model url: {git_url}")

    # get git token
    git_info = api.get_user_gitinfo()
    git_user, git_secret = git_info['git_user_name'], git_info['git_user_secret']

    # compose new git url with auth
    parsed_url = urlparse(git_url)
    authed_git_url = urlunparse((parsed_url.scheme, f'{git_user}:{git_secret}@{parsed_url.netloc}',
                                 parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

    with tempfile.TemporaryDirectory(prefix='scoamp') as tmp_git_dir_path:
        logger.info('clone remote model...')
        r = subprocess.run(f'git clone {authed_git_url} {tmp_git_dir_path}', shell=True, check=False, capture_output=True, encoding='utf-8')
        if r.returncode:
            raise RuntimeError(f'git clone remote model error: {r.stderr}')

        logger.info('upload local model to remote repo...')

        shell_script = f"""
        git config user.name "scoamp-agent"
        git config user.email "scoamp-agent@sensecore.cn"
        scoamp lfs setup .
        git --work-tree {local_dir_path} add --no-all .
        git commit -m "add model files"
        git push origin master
        """

        if _mswindows:
            # for windows
            new_cmds = ["@echo on\n"]
            for line in shell_script.strip().split('\n'):
                # exit on each command error
                new_cmds.append(line + " || exit /b 1\n")
            bat_file = tempfile.NamedTemporaryFile(mode='w+t', suffix='.bat', delete=False)
            bat_file.write(''.join(new_cmds))
            bat_file.close()
            # on windows, 'shell_script' should be the path of script file
            shell_script = bat_file.name
        else:
            # for unix
            shell_script = "set -ex\n" + shell_script

        try:
            subprocess.run(
                shell_script,
                shell=True,
                check=True,
                cwd=tmp_git_dir_path,
                capture_output=True,
                encoding='utf-8',
            )
        except subprocess.CalledProcessError as exc:
            logger.error("something error when uploading local model files to AMP")
            raise SubprocessError(
                f"run sub-process error, see details below\n"\
                f"[origin output]\n{exc.stderr}\n"\
                f"[exit code]\n{exc.returncode}"
            )
        finally:
            if _mswindows:
                os.remove(shell_script)

    logger.info("upload model success!")
    return git_url
