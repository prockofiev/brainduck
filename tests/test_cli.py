from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import brainduck

SCRIPT = Path(brainduck.__file__).resolve()


def run_cli(*args: str, cwd: Path, input_bytes: bytes | None = None):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        input=input_bytes,
    )
    return proc


class TestCLICompile:
    def test_compiles_file(self, tmp_path):
        src = tmp_path / "in.bd"
        src.write_text("def[1] a; a = 1;", encoding="utf-8")
        out = tmp_path / "out.bf"
        proc = run_cli("-i", str(src), "-o", str(out), cwd=tmp_path)
        assert proc.returncode == 0
        assert out.exists()
        assert out.read_text(encoding="utf-8")

    def test_compile_report_on_stdout(self, tmp_path):
        src = tmp_path / "in.bd"
        src.write_text("def[1] a; a = 1;", encoding="utf-8")
        proc = run_cli("-i", str(src), cwd=tmp_path)
        assert "compiled" in proc.stdout
        assert proc.returncode == 0

    def test_missing_input_returns_error(self, tmp_path):
        proc = run_cli("-i", "nope.bd", cwd=tmp_path)
        assert proc.returncode == 1
        assert "cannot read" in proc.stderr


class TestCLIVersion:
    def test_version_flag(self, tmp_path):
        proc = run_cli("--version", cwd=tmp_path)
        assert proc.returncode == 0
        assert "0.2.0" in proc.stdout

    def test_help_flag(self, tmp_path):
        proc = run_cli("--help", cwd=tmp_path)
        assert proc.returncode == 0
        assert "usage" in proc.stdout.lower()


class TestCLICompileError:
    def test_undefined_variable_returns_error(self, tmp_path):
        src = tmp_path / "bad.bd"
        src.write_text("def[1] a; del nope; a = 1;", encoding="utf-8")
        proc = run_cli("-i", str(src), cwd=tmp_path)
        assert proc.returncode == 1
        assert "failed" in proc.stderr