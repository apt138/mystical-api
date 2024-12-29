from model.creature import Creature
from service import creature
import pytest
from errors import Missing, Duplicate


sample: Creature = Creature(
    name="yeti service",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


def test_create():
    resp = creature.create(sample)
    assert resp == sample


def test_get_exists():
    resp = creature.get_one("yeti service")
    assert resp == resp


def test_get_missing():
    with pytest.raises(Missing) as e:
        resp = creature.get_one("test")
    assert str(e.value) == "Creature `test` not found"
