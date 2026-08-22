from __future__ import annotations

from render_code import clear_code, blocking, expression_blocking, optimizer_code


class TestClearCode:
    def test_removes_newlines(self):
        assert clear_code("a\nb") == "ab"

    def test_collapses_spaces(self):
        assert clear_code("def[1]   a ;") == "def[1] a ;"

    def test_tabs_preserved_by_regex_multispace_only(self):
        # re.sub(r' +', ' ') collapses runs of spaces but leaves tabs
        assert clear_code("a\t\tb") == "a\t\tb"


class TestBlocking:
    def test_splits_on_semicolon(self):
        assert blocking("def[1] a; def[1] b;") == ["def[1] a", " def[1] b", ""]

    def test_does_not_split_inside_braces(self):
        blocks = blocking("if(x) { a=1; b=2; }; c=3;")
        assert blocks == ["if(x) { a=1; b=2; }", " c=3", ""]

    def test_nested_braces_kept_together(self):
        blocks = blocking("while(x) { if(y) { z=1; }; w=2; };")
        assert blocks[0] == "while(x) { if(y) { z=1; }; w=2; }"


class TestExpressionBlocking:
    def test_plain_identifier(self):
        assert expression_blocking("foo") == "foo"

    def test_plain_number(self):
        assert expression_blocking("42") == "42"

    def test_binary_expression_splits_into_parts(self):
        result = expression_blocking("(a) == (b)")
        assert result[0] == "a"
        assert result[1] == "=="
        assert result[2] == "b"

    def test_quoted_string_operand(self):
        result = expression_blocking('(x) != ("Y")')
        assert result[0] == "x"
        assert result[1] == "!="
        assert result[2] == '"Y"'


class TestOptimizerCode:
    """Verifies no-op cancellation in the Brainfuck dialect.

    ``>``/``<`` pairs cancel (cursor returns), and ``+`` toggles a bit so
    an even run is a no-op while an odd run reduces to a single ``+``.
    """

    def test_cancels_adjacent_move_pair(self):
        assert optimizer_code("><") == ""
        assert optimizer_code("<>") == ""

    def test_cancels_pair_after_removal(self):
        # `+><+` -> series of cancellations -> empty
        assert optimizer_code("+><+") == ""

    def test_triple_plus_reduces_to_single(self):
        assert optimizer_code("+++") == "+"

    def test_even_run_is_noop(self):
        assert optimizer_code("++++") == ""

    def test_mixed_nontrivial_program_unchanged(self):
        program = "+[>+<-]"
        # No cancelling adjacent pairs, no even +/- runs.
        assert optimizer_code(program) == program

    def test_leading_plus_pair_removed(self):
        # Leading `++` is a cancelling toggle pair -> removed.
        assert optimizer_code("++[->+<]") == "[->+<]"

    def test_prefix_plus_and_cancel_pair(self):
        assert optimizer_code("+><+") == ""

    def test_returns_empty_for_empty(self):
        assert optimizer_code("") == ""

    def test_push_through_cancellation_then_reduce(self):
        # Starts irreducible-like but repeated passes collapse it.
        assert optimizer_code("><++<>") == ""