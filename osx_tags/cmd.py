from json import dump
import sys

import click

from . import Tags, tag_colored, tag_split

color_numbers = {
    'none': 0,
    'gray': 1,
    'grey': 1,
    'green': 2,
    'purple': 3,
    'blue': 4,
    'yellow': 5,
    'red': 6,
    'orange': 7,
}
color_names = [
    'none',
    'gray',
    'green',
    'purple',
    'blue',
    'yellow',
    'red',
    'orange'
]
tags_to_ansi = [
    (None, False),
    ('black', True),
    ('green', False),
    ('magenta', True),
    ('blue', False),
    ('yellow', True),
    ('red', False),
    ('yellow', False),
]
_counter = 0


def style_tag(tag):
    """
    Style a tag using ANSI codes.
    :param tag: Either a regular tag or a tag with color information.
    :return: a string, possibly with escapes.
    """
    tag, color = tag_split(tag)
    color, bold = tags_to_ansi[color]
    if color:
        return click.style(tag, fg=color, bold=bold)
    else:
        return tag


class Ordered(click.ParamType):
    counter = 0

    def get_metavar(self, param):
        return '[' + param.upper() + ']'

    def convert(self, value, param, ctx):
        num = type(self).counter
        type(self).counter += 1
        return num, param, value


def combine(colors, tags):
    items = list(colors)
    items.extend(tags)
    items.sort()
    color = 0
    for _, param, value in items:
        if param.name == 'color':
            value = value.lower()
            if value not in color_numbers:
                raise ValueError("No such color {}, must be {}".format(value.lower(), ', '.join(color_names)))
            color = color_numbers[value.lower()]
        elif param.name == 'tag':
            yield tag_colored(tag=value, color=color) if color else value
        else:
            raise TypeError('Invalid param {}'.format(param.name))


@click.command(name='finder-tags')
@click.option('--color', '-c', multiple=True, type=Ordered(),
              help='Sets color of tags following this option.')
@click.option('--tag', '-t', multiple=True, type=Ordered(),
              help='Identify a tag, may be used multiple times.')
@click.option('--json', '-j', is_flag=True, help='Prefer json output.')
@click.argument('action', type=click.Choice(['read', 'set', 'add', 'del']))
@click.argument('paths', type=click.Path(), nargs=-1)
def main(action, paths, color, tag, json):
    if action == 'read':
        if tag or color:
            raise ValueError('The --tag and --color options are invalid when reading.')
        if json:
            output = []
            for path in paths:
                tags = []
                for tag in Tags(path).read():
                    text, color = tag_split(tag)
                    tags.append({'tag': text, 'color': color_names[color]})
                output.append({'path': path, 'tags': tags})
            dump(output, sys.stdout, indent=4)
        else:
            for path in paths:
                tags_strs = ' '.join('[' + style_tag(tag) + ']' for tag in Tags(path).read())
                print('{} {}'.format(path, tags_strs))
    elif action in 'set':
        tags = list(combine(color, tag))
        for path in paths:
            Tags(path).write(*tags)
    elif action in 'add':
        tags = list(combine(color, tag))
        for path in paths:
            Tags(path).add(*tags)
    elif action in 'del':
        tags = list(combine(color, tag))
        for path in paths:
            Tags(path).remove(*tags)
