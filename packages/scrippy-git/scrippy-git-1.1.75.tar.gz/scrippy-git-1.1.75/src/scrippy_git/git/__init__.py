"""Scrippy basic Git client."""
import git
from scrippy_git import ScrippyGitError, logger


class Repo():
  """
  This class allows for the manipulation of a Git repository, including cloning, committing, pulling, and pushing changes.

  This class supports Git repository manipulation via SSH only.

  :param username: The username used to connect via SSH to the Git server.
  :type username: str, required
  :param host: The name of the remote host hosting the Git server.
  :type host: str, required
  :param port: The port number to connect to, default value: 22.
  :type port: int, optional
  :param reponame: The name of the remote repository.
  :type reponame: str, required
  """

  def __init__(self, username=None, host=None, port=22, reponame=None):
    self.url = f"ssh://{username}@{host}:{port}/{reponame}"
    self.name = reponame
    self.cloned = None
    self.path = None
    self.origin = None
    self.branch = None

  def clone(self, branch, path, origin="origin", options=None, env=None):
    if options is None:
      options = []
    if env is None:
      env = {}
    logger.debug(f"[+] Cloning repository: {self.url}")
    logger.debug(f" '-> {path}")
    self.path = path
    self.branch = branch
    try:
      self.cloned = git.Repo.clone_from(self.url, path, branch=branch, multi_options=options, env=env)
      self.origin = self.cloned.remote(name=origin)
    except Exception as err:
      err_msg = f"Error while cloning repository: [{err.__class__.__name__}]: {err}"
      raise ScrippyGitError(err_msg) from err

  def commit(self, message, error_on_clean_repo=True):
    logger.debug(f"[+] Commit message: [{self.name}]: {message}")
    if not self.cloned.is_dirty(untracked_files=True):
      if error_on_clean_repo:
        err_msg = "Nothing to commit. Aborting"
        raise ScrippyGitError(err_msg)
      logger.warning(" '-> Nothing to commit.")
      return
    self.cloned.git.add(".")
    self.cloned.git.commit(m=message)

  def pull(self):
    logger.debug(f"[+] Pulling: [{self.name}]: {self.origin}")
    self.cloned.git.pull()

  def push(self):
    logger.debug(f"[+] Pushing: [{self.name}]: {self.origin}")
    self.origin.push()

  def commit_push(self, message, error_on_clean_repo=True):
    try:
      self.commit(message=message, error_on_clean_repo=error_on_clean_repo)
      self.pull()
      self.push()
    except Exception as err:
      err_msg = f"Error while commiting: [{err.__class__.__name__}]: {err}"
      raise ScrippyGitError(err_msg) from err
