from model.creature import Creature
from service import creature as code


sample: Creature = Creature(
    name="yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("yeti")
    assert resp == resp


def test_get_missing():
    resp = code.get_one("test")
    assert resp is None
