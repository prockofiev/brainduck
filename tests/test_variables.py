from __future__ import annotations

import pytest

from variables import Variables


class TestAllocation:
    def test_first_variable_starts_at_zero(self):
        a = Variables(name="a", size=3)
        assert a.index == 0
        assert a.size == 3

    def test_consecutive_variables_append(self):
        a = Variables(name="a", size=3)
        b = Variables(name="b", size=1)
        assert a.index == 0
        assert b.index == 3

    def test_variable_allocates_into_first_fit_gap(self):
        a = Variables(name="a", size=3)   # 0-2
        b = Variables(name="b", size=2)   # 3-4
        b.remove()
        c = Variables(name="c", size=1)   # should reuse index 3 first, not append at 5
        assert c.index == 3

    def test_large_variable_skips_small_gap(self):
        # a(0), b(1-4), c(5): gap of 3 at 1-3 from removing b
        a = Variables(name="a", size=1)   # 0
        b = Variables(name="b", size=4)   # 1-4
        c = Variables(name="c", size=1)   # 5
        b.remove()                        # gap of 4 at 1-4
        # size 5 cannot fit the gap, and is bounded by c -> appends at... 6
        a2 = Variables(name="a2", size=5)  # too big for gap, appends at c end
        assert a2.index == 6

    def test_small_variable_skips_to_next_index_when_single(self):
        # With a single remaining variable, no upper bound exists: allocate
        # immediately after it.
        a = Variables(name="a", size=1)   # 0
        b = Variables(name="b", size=1)   # 1
        b.remove()
        a2 = Variables(name="a2", size=1)
        assert a2.index == 1

    def test_remove_reuses_cell(self):
        a = Variables(name="a", size=2)
        a.remove()
        b = Variables(name="b", size=2)
        assert b.index == 0

    def test_remove_idempotent(self):
        a = Variables(name="a", size=1)
        a.remove()
        a.remove()  # should not raise


class TestValidation:
    def test_zero_size_rejected(self):
        with pytest.raises(ValueError):
            Variables(name="a", size=0)

    def test_negative_size_rejected(self):
        with pytest.raises(ValueError):
            Variables(name="a", size=-1)

    def test_duplicate_name_rejected(self):
        Variables(name="a", size=1)
        with pytest.raises(ValueError):
            Variables(name="a", size=1)

    def test_anonymous_duplicate_allowed(self):
        # Temporary variables have name=None and may repeat
        Variables(name=None, size=1)
        Variables(name=None, size=1)

    def test_get_by_name_returns_none_for_unknown(self):
        assert Variables.get_by_name("ghost") is None

    def test_get_by_name_finds_defined(self):
        Variables(name="x", size=1)
        assert Variables.get_by_name("x") is not None


class TestRegistry:
    def test_memory_tracks_all(self):
        a = Variables(name="a", size=1)
        b = Variables(name="b", size=1)
        assert a in Variables.memory
        assert b in Variables.memory

    def test_remove_drops_from_registry(self):
        a = Variables(name="a", size=1)
        a.remove()
        assert a not in Variables.memory

    def test_sorted_by_index(self):
        a = Variables(name="a", size=1)   # index 0
        c = Variables(name="c", size=3)   # index 1-3
        b = Variables(name="b", size=1)   # append index 4
        indexes = [v.index for v in Variables.memory]
        assert indexes == sorted(indexes)
        assert indexes == [0, 1, 4]
        assert a.size == 1 and c.size == 3 and b.size == 1