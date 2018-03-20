"""
Manage Finder tags on a file in OS X.
"""

from biplist import writePlistToString, readPlistFromString
from xattr import xattr

#: Color numbers
NONE = 0
GRAY = 1
GREEN = 2
PURPLE = 3
BLUE = 4
YELLOW = 5
RED = 6
ORANGE = 7


def tag_nocolor(tag):
    """
    Removes the color information from a Finder tag.
    """
    return tag.rsplit('\n', 1)[0]


def tag_colored(tag, color):
    """
    Sets the color of a tag.

    Parameters:
      tag(str): a tag name
      color(int): an integer from 1 through 7

    Return:
      (str) the tag with encoded color.
    """
    return '{}\n{}'.format(tag_nocolor(tag), color)


def tag_split(tag):
    """
    Extracts the color information from a Finder tag.
    """
    parts = tag.rsplit('\n', 1)
    if len(parts) == 1:
        return parts[0], 0
    elif len(parts[1]) != 1 or parts[1] not in '01234567':  # Not a color number
        return tag, 0
    else:
        return parts[0], int(parts[1])


def tag_normalize(tag):
    """
    Ensures a color is set if not none.
    :param tag: a possibly non-normal tag.
    :return: A colorized tag.
    """
    tag, color = tag_split(tag)
    return tag_colored(tag, color)


class Tags(object):
    """
    Holds an xattr object to read, write, add or remove Finder tags from a file on a volume that supports metadata.
    """
    def __init__(self, fileish):
        self.xa = xattr(fileish)

    TAG_XATTRS = ('com.apple.metadata:_kMDItemUserTags', 'com.apple.metadata:kMDItemOMUserTags')

    def read(self):
        """
        Returns a generator that iterates through the tags.
        """
        tags = set()
        for key in self.TAG_XATTRS:
            try:
                plist = self.xa.get(key)
            except (OSError, IOError):
                pass
            else:
                tags.update(map(tag_normalize, readPlistFromString(plist)))
        return tags

    def write(self, *tags):
        """
        Overwrites the existing tags with the iterable of tags provided.
        """
        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Tags must be strings")
        tag_plist = writePlistToString(list(map(tag_normalize, tags)))
        for key in self.TAG_XATTRS:
            self.xa.set(key, tag_plist)

    def clear(self):
        """
        Remove all tags from the file.
        """
        for key in self.TAG_XATTRS:
            try:
                self.xa.remove(key)
            except (IOError, OSError):
                pass

    def add(self, *tags):
        """
        Sets the tags to be the union of the existing and provided tags.
        """
        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Tags must be strings")
        new_tags = self.read() | set(map(tag_normalize, tags))
        self.write(*new_tags)

    def remove(self, *tags):
        """
        Sets the tags to be the difference of the existing tags with the provided tags.
        """
        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Tags must be strings")
        new_tags = self.read() - set(map(tag_normalize, tags))
        self.write(*new_tags)
