from __future__ import annotations

import pytest

from compile import Compile


@pytest.fixture
def compiler():
    return Compile(DEBUG=False, ONLY_RESULT=False, SHOW_MEMORY=100)


class TestErrors:
    def test_del_undefined_variable_raises(self, compiler):
        with pytest.raises(ValueError):
            compiler.compile("def[1] a; del missing; a = 1;")

    def test_duplicate_definition_raises(self, compiler):
        with pytest.raises(ValueError):
            compiler.compile("def[1] a; def[1] a;")

    def test_reassign_normalizes_code(self, compiler):
        result = compiler.compile("def[1] a; a = 1;")
        assert isinstance(result, str)
        assert len(result) > 0


class TestCompileOutput:
    def test_compiles_simple_program_to_nonempty(self, compiler):
        out = compiler.compile("def[1] a; a = 1;")
        assert isinstance(out, str) and out

    def test_declaration_only_compiles_without_error(self, compiler):
        # A bare declaration reserves memory and therefore emits no code.
        out = compiler.compile("def[2] a;")
        assert isinstance(out, str)

    def test_compile_is_deterministic(self, compiler):
        a = compiler.compile("def[3] x; x = 5;")
        # Reset the shared registry, then compile an identical program with a
        # fresh compiler; the emitted Brainfuck must be byte-identical.
        from variables import Variables
        Variables.memory = []
        compiler2 = Compile(DEBUG=False, ONLY_RESULT=False, SHOW_MEMORY=100)
        b = compiler2.compile("def[3] x; x = 5;")
        assert a == b

    def test_output_contains_brainfuck_primitives(self, compiler):
        out = compiler.compile("def[1] a; a = 1;")
        assert any(ch in out for ch in "+-<>[].,")


class TestRun:
    def test_run_executes_without_error(self, compiler, capsys):
        compiler.compile("def[1] a; a = 1;")
        compiler.run()  # should not raise