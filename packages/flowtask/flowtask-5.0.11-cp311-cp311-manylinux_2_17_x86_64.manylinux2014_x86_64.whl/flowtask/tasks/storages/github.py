from pathlib import PurePath
from navconfig.logging import logging
from flowtask.exceptions import FlowTaskError
from .filesystem import FileTaskStorage

gitlog = logging.getLogger('git')
gitlog.setLevel(logging.WARNING)

from git import Repo
from git import GitCommandError

class GitTaskStorage(FileTaskStorage):
    """Getting Tasks on Filesystem with Github Support.
    """
    def __init__(
        self,
        path: PurePath,
        git_url: str,
        git_private_key: str = None,
        *args, **kwargs
    ):
        super(GitTaskStorage, self).__init__(path, *args, **kwargs)

        if git_url:
            self.git_url = git_url
            self.git_private_key = git_private_key
            self.refresh_repository()

    def refresh_repository(self):
        try:
            if not self.path.exists() or not any(self.path.iterdir()):
                # If the directory is empty or doesn't exist, clone the repository
                if self.git_private_key:
                    Repo.clone_from(
                        self.git_url,
                        self.path,
                        env={"GIT_SSH_COMMAND": f"ssh -i {self.git_private_key}"}
                    )
                else:
                    Repo.clone_from(self.git_url, self.path)
                self.logger.info(
                    f'Cloned repository: {self.git_url}'
                )
            else:
                # If the directory exists and is not empty, pull the latest changes
                repo = Repo(self.path)
                if self.git_private_key:
                    with repo.git.custom_environment(
                        GIT_SSH_COMMAND=f"ssh -i {self.git_private_key}"
                    ):
                        repo.git.pull()
                else:
                    repo.git.pull()
                self.logger.info(
                    f'Pulled the latest changes from repository: {self.git_url}'
                )
        except GitCommandError as err:
            raise FlowTaskError(
                f"Error interacting with Git repository: {err}"
            ) from err
