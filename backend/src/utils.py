import argparse
import os

from backend.src.data.context import Context


class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
            else:
                raise Exception(f"Can't found param {envvar}")
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def hash_id(source_id):
    return ((source_id + 1) * Context.id_shift) ^ Context.salt


def rehash_id(hash_id):
    return int((hash_id ^ Context.salt) / Context.id_shift) - 1
