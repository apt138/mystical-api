import os
import pytest
from errors import Missing, Duplicate
from model.creature import Creature

os.environ["MYSTICAL_SQLITE_DB"] = ":memory:"
from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti data",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate) as e:
        creature.create(sample)


def test_get_all(sample):
    resp = creature.get_all()
    assert resp == [sample]


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        creature.get_one("unknown_creature")


def test_replace(sample):
    new_sample = Creature(**sample.model_dump())
    new_sample.description = "test"
    resp = creature.replace(new_sample.name, new_sample)
    assert resp == new_sample


def test_replace_missing(sample):
    new_sample = Creature(**sample.model_dump())
    name = "unknown_creature"
    new_sample.name = "tesing"
    with pytest.raises(Missing):
        creature.replace(name, new_sample)


def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        creature.delete(sample.name)
