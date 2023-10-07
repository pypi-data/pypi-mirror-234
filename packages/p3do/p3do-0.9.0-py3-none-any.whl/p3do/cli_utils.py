#!/usr/bin/env python3

import click

import sys
import os
import appdirs
import subprocess

from functools import update_wrapper, partial, wraps
from configparser import ConfigParser
from typing import List

from loguru import logger

def kc_admin_command(func):
    """Decorator to encapsulate common logic for kc admin commands that need authentication"""

    @click.option("--server", help="The server url")
    @click.option("--username", help="The username for import must have rights to modify the realm")
    @click.option("--password", help="The password")
    @click.option("--user_realm_name", help="The realm the user is in")
    @click.option("--realm_name", help="The realm the mappers should be added to")
    @click.option("--auth_config", type=click.Path(exists=True, dir_okay=False, readable=True), help="Read KC authorization from a config file")
    @click.option("--auth", help="Read KC authorization from a config file")
    @click.pass_context
    def inner(ctx, *args, **kwargs):
        # make sure ctx.obj is a dict
        ctx.ensure_object(dict)

        # fill params with cli args
        params = {
            'server': kwargs['server'],
            'username': kwargs['username'],
            'password': kwargs['password'],
            'user_realm_name': kwargs['user_realm_name'],
            'realm_name': kwargs['realm_name']
        }

        # read from config file and set params if not already set by cli arg
        if 'auth_config' in kwargs and 'auth' in kwargs:
            def set_from_config(config, param_name):
                if param_name in config[kwargs['auth']] and params[param_name] is None:
                    params[param_name] = config[kwargs['auth']][param_name]

            config = ConfigParser()
            config.read(kwargs['auth_config'])

            list(map(partial(set_from_config, config), params.keys()))

        # prompt for missing values that are still missing
        def prompt_if_missing(param_name: str):
            if params[param_name] is None:
                params[param_name] = click.prompt(param_name.capitalize())
        list(map(prompt_if_missing, params.keys()))

        # remove arguments from `**kwargs` that are consumed by this auth decorator
        # this is needed s.t. decorated functions don't have to be modified to accept
        # those values too (`click` is a bit strange there unfortunately)
        #
        # if we just add `**kwargs` to the decorated function it adds params of
        # sub-commands twice once as positional and then again in `**kwargs` so
        # that ain't not going to working either. Also we'd have to modify
        # downstream to cater for upstream particularities which we want to
        # avoid.
        #
        # maybe there's a better way with some `click` magic
        for param_name in params.keys(): del kwargs[param_name]
        del kwargs['auth_config']
        del kwargs['auth']

        if not params['server'].endswith('/'): params['server'] += '/'

        ctx.obj.update(params)

        return ctx.invoke(func, ctx, **kwargs)
    return update_wrapper(inner, func)



def platforms(platforms: List[str]):
    def _wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not sys.platform in platforms:
                logger.error("This command is only implemented for Linux")
                sys.exit(1)
            f(args, kwargs)
        return inner
    return _wrapper


def with_cache(var, config_name, prompt) -> str:
    if not var:
        cache_dir = appdirs.user_cache_dir("p3do")
        os.makedirs(cache_dir, exist_ok=True)
        config_file = os.path.join(cache_dir, config_name)

        try:
            with open(config_file, 'r') as f:
                return f.read()
        except:
            new_value = click.prompt(prompt)
            with open(config_file, 'w') as f:
                f.write(new_value)
            return new_value
    return var


def detect_branch():
    res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
    if res.returncode != 0:
        logger.info("Not in a git directory")
        return None

    branch = res.stdout.decode('utf-8').strip(" \n")
    logger.info("Found current branch {} of git directory {}", branch, os.getcwd())
    return branch
