import os
import pytest
from model.explorer import Explorer
from errors import Missing, Duplicate


os.environ["MYSTICAL_SQLITE_DB"] = ":memory:"
from data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    )


def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate) as e:
        explorer.create(sample)


def test_get_all(sample):
    resp = explorer.get_all()
    assert resp == [sample]


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        explorer.get_one("unknown_explorer")


def test_replace(sample):
    new_sample = Explorer(**sample.model_dump())
    new_sample.description = "testing"
    resp = explorer.replace(new_sample)
    assert resp == new_sample


def test_replace_missing(sample):
    new_sample = Explorer(**sample.model_dump())
    new_sample.name = "unknown_explorer"
    with pytest.raises(Missing):
        _ = explorer.replace(new_sample)


def test_delete(sample):
    resp = explorer.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        explorer.delete(sample.name)
