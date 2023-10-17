import sys

import click
import jsonschema
from drb.dao import YamlDao


@click.command(name='cortex-validator')
@click.argument('cortex',
                type=click.Path(exists=True, file_okay=True, dir_okay=False))
def validate(cortex):
    try:
        YamlDao.validate(cortex)
    except jsonschema.exceptions.ValidationError as ex:
        print('Invalid schema: ', str(ex), file=sys.stderr)


def main():
    validate()
