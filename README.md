## Finder tags on OS X

This is a small library to manage Finder tags on OS X, and a command line utility.

Example:

    from osx_tags import Tags

    doc = Tags('Documents/some.doc')
    doc.add("tag one")
    print(doc.read())
    doc.clear()
