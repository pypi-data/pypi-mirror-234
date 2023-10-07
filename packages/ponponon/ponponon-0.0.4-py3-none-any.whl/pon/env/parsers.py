import os
import re
from functools import partial

import yaml


has_regex_module = False
ENV_VAR_MATCHER = re.compile(
    r"""
        \$\{       # match characters `${` literally
        ([^}:\s]+) # 1st group: matches any character except `}` or `:`
        :?         # matches the literal `:` character zero or one times
        ([^}]+)?   # 2nd group: matches any character except `}`
        \}         # match character `}` literally
    """, re.VERBOSE
)


IMPLICIT_ENV_VAR_MATCHER = re.compile(
    r"""
        .*          # matches any number of any characters
        \$\{.*\}    # matches any number of any characters
                    # between `${` and `}` literally
        .*          # matches any number of any characters
    """, re.VERBOSE
)


RECURSIVE_ENV_VAR_MATCHER = re.compile(
    r"""
        \$\{       # match characters `${` literally
        ([^}]+)?   # matches any character except `}`
        \}         # match character `}` literally
        ([^$}]+)?  # matches any character except `}` or `$`
        \}         # match character `}` literally
    """,
    re.VERBOSE,
)


def _replace_env_var(match):
    env_var, default = match.groups()
    value = os.environ.get(env_var, None)
    if value is None:
        # expand default using other vars
        if default is None:
            # regex module return None instead of
            #  '' if engine didn't entered default capture group
            default = ''

        value = default
        while IMPLICIT_ENV_VAR_MATCHER.match(value):  # pragma: no cover
            value = ENV_VAR_MATCHER.sub(_replace_env_var, value)
    return value


def env_var_constructor(loader, node, raw=False):
    raw_value = loader.construct_scalar(node)

    # detect and error on recursive environment variables
    if not has_regex_module and RECURSIVE_ENV_VAR_MATCHER.match(
        raw_value
    ):  # pragma: no cover
        raise Exception(
            "Nested environment variable lookup requires the `regex` module"
        )
    value = ENV_VAR_MATCHER.sub(_replace_env_var, raw_value)
    if value == raw_value:
        return value  # avoid recursion
    return value if raw else yaml.safe_load(value)


def setup_yaml_parser():
    yaml.add_constructor('!env_var', env_var_constructor, yaml.SafeLoader)
    yaml.add_constructor(
        '!raw_env_var',
        partial(env_var_constructor, raw=True),
        yaml.SafeLoader
    )
    yaml.add_implicit_resolver(
        '!env_var', IMPLICIT_ENV_VAR_MATCHER, Loader=yaml.SafeLoader
    )

# copy from nameko https://github.com/nameko/nameko/blob/v2.14.1/nameko/cli/main.py
