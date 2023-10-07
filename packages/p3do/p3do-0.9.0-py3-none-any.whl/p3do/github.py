#!/usr/bin/env python3

from github import Github
from loguru import logger

@logger.catch
def deploy_key(repository, ssh_key, token, title, read_only):
    gh = Github(token)
    gh_repo = gh.get_repo(repository)
    gh_repo.create_key(title, ssh_key, read_only=read_only)
