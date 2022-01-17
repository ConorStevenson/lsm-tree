import pytest

from lsm import LSM


def test_lsm():
    store = LSM()
    store.set("Conor", "92")
    store.set("Conor", "29")
    assert store.get("Conor") == "29"
    store.set("Rhys", "25")
    assert store.get("Rhys") == "25"
    with pytest.raises(KeyError):
        store.get("Tara")
    store.flush()
    store.set("Tara", "28")
    assert store.get("Tara") == "28"
    assert store.get("Conor") == "29"
    store.set("Alan", "59")
    store.flush()
    store.compact()
    assert store.get("Tara") == "28"
