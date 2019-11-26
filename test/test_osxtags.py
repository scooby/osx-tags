import osx_tags as o


def test_tag_nocolor():
    assert o.tag_nocolor("purple\n3") == "purple"


def test_tag_colored():
    assert o.tag_colored("some tag", o.GREEN) == "some tag\n2"
    assert o.tag_colored("purple\n5", o.PURPLE) == "purple\n3"


def test_tag_split():
    assert o.tag_split("regular tag") == ("regular tag", o.NONE)
    assert o.tag_split("two\nlines") == ("two\nlines", o.NONE)
    assert o.tag_split("purple\n3") == ("purple", o.PURPLE)


def test_tag_normalize():
    assert o.tag_normalize("purple\n3") == "purple\n3"
    assert o.tag_normalize("no color") == "no color\n0"
