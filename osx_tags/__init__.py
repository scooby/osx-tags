'''
Manage Finder tags on a file in OS X.
'''

from biplist import writePlistToString, readPlistFromString
from xattr import xattr

#: Color numbers
GRAY = 1
GREEN = 2
PURPLE = 3
BLUE = 4
YELLOW = 5
RED = 6
ORANGE = 7


def tag_nocolor(tag):
    '''
    Removes the color information from a Finder tag.
    '''
    return tag.split('\n')[0]


def tag_colored(tag, color):
    '''
    Sets the color of a tag.

    Parameters:
      tag(str): a tag name
      color(int): an integer from 1 through 7

    Return:
      (str) the tag with encoded color.
    '''
    return '{}\n{}'.format(tag_nocolor(tag), color)


class Tags(object):
    '''
    Holds an xattr object to read, write, add or remove Finder tags from a file on a volume that supports metadata.
    '''
    def __init__(self, fileish):
        self.xa = xattr(fileish)

    TAG_XATTRS = ('com.apple.metadata:_kMDItemUserTags', 'com.apple.metadata:kMDItemOMUserTags')

    def read(self):
        '''
        Returns a generator that iterates through the tags.
        '''
        tags = set()
        for key in self.TAG_XATTRS:
            try:
                plist = self.xa.get(key)
            except OSError:
                pass
            else:
                tags.update(readPlistFromString(plist))
        return tags

    def write(self, *tags):
        '''
        Overwrites the existing tags with the iterable of tags provided.
        '''
        tag_plist = writePlistToString([str(tag) for tag in tags])
        for key in self.TAG_XATTRS:
            self.xa.set(key, tag_plist)

    def clear(self):
        '''
        Remove all tags from the file.
        '''
        for key in self.TAG_XATTRS:
            try:
                self.xa.remove(key)
            except OSError:
                pass

    def add(self, *tags):
        '''
        Sets the tags to be the union of the existing and provided tags.
        '''
        new_tags = self.read() | set(tags)
        self.write(*new_tags)

    def remove(self, *tags):
        '''
        Sets the tags to be the difference of the existing tags with the provided tags.
        '''
        new_tags = self.read() - set(tags)
        self.write(*new_tags)
