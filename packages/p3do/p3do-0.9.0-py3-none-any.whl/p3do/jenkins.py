#!/usr/bin/env python3

from jenkinsapi.jenkins import Jenkins
from loguru import logger


def _get_server_instance(api_user: str, api_key: str):
    jenkins_url = "https://ci2.semantic-web.at/"

    logger.debug("Connecting to {}", jenkins_url)
    server = Jenkins(jenkins_url, username=api_user, password=api_key, timeout=30)
    return server

@logger.catch
def run_build(job: str, branch: str, api_user: str, api_key: str):
    logger.info("Running {} on branch {}", job, branch)


    logger.info("Getting server instance")
    server = _get_server_instance(api_user, api_key)
    params = {'branch': branch}

    # This will start the job and will return a QueueItem object which
    # can be used to get build results
    jk_job = server[job]
    logger.debug("Got job {}", jk_job)
    qi = jk_job.invoke(build_params=params)
    logger.debug("Got job invocation {}", qi)

    logger.info("Block until building")
    qi.block_until_building()
    logger.info("Started build {}", qi.get_build())
    return qi.get_build().get_build_url()


@logger.catch
def run_deploy(job: str, target: str, branch: str, api_user: str, api_key: str):
    logger.info("Running {} on branch {} for server {}", job, branch, target)


    logger.info("Getting server instance")
    server = _get_server_instance(api_user, api_key)
    params = {'branch': branch, 'Server': target}

    # This will start the job and will return a QueueItem object which
    # can be used to get build results
    jk_job = server[job]
    logger.debug("Got job {}", jk_job)
    qi = jk_job.invoke(build_params=params)
    logger.debug("Got job invocation {}", qi)

    logger.info("Block until building")
    qi.block_until_building()
    logger.info("Started build {}", qi.get_build())
    return qi.get_build().get_build_url()
