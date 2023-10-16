"""Test scrippy_git."""
import os
from scrippy_git import git

USERNAME = "git"
HOST = "gitolite"
PORT = 2201
REPONAME = "gitolite-admin"
BRANCH = "master"
ENV = {"GIT_SSH_COMMAND": f"ssh -i {os.path.dirname(os.path.realpath(__file__))}/ssh/scrippy.rsa -o StrictHostKeyChecking=no"}


def test_git_pull():
  """Test Git pull."""
  repo = git.Repo(USERNAME, HOST, PORT, REPONAME)
  local_path = os.path.join("./", REPONAME)
  repo.clone(branch=BRANCH, path=local_path, env=ENV)
  gitolite_config_filename = os.path.join(local_path, "conf", "gitolite.conf")
  with open(gitolite_config_filename, mode="r") as gitolite_config_file:
    gitolite_conf = gitolite_config_file.readlines()
    assert gitolite_conf[0].strip() == "repo gitolite-admin"
  with open(gitolite_config_filename, mode="w") as gitolite_config_file:
    gitolite_config_file.write("Nobody expects the Spanish inquisition !")
  commit_message = "Inquisition shall not be expected"
  repo.commit(commit_message)
