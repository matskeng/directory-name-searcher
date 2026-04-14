import csv
import sys
from pathlib import Path

import pytest

from directory_name_searcher.cli import main


def create_test_structure(root: Path) -> None:
    """
    テスト用のディレクトリ・ファイル構造を作成する

    root/
    ├─ build/
    ├─ build_debug/
    ├─ src/
    │  └─ main.py
    └─ README.md
    """
    (root / "build").mkdir()
    (root / "build_debug").mkdir()
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('hello')")
    (root / "README.md").write_text("readme")


def run_cli(argv: list[str]) -> None:
    """
    sys.argv を差し替えて CLI を実行するヘルパー
    """
    original_argv = sys.argv
    sys.argv = argv
    try:
        main()
    finally:
        sys.argv = original_argv


def read_csv(path: Path) -> list[list[str]]:
    """
    CSV を行単位で読み込む
    """
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def test_cli_basic_csv_output(tmp_path: Path) -> None:
    """
    --target 指定で CSV が正しく出力される
    """
    create_test_structure(tmp_path)

    output_csv = tmp_path / "result.csv"

    run_cli([
        "prog",
        "--target", "build", "README.md",
        "--root", str(tmp_path),
        "--output", str(output_csv),
    ])

    assert output_csv.exists()

    rows = read_csv(output_csv)

    # ヘッダ確認（path_1 まであれば十分）
    assert rows[0][:2] == ["name", "found"]
    assert rows[0][2].startswith("path_")

    # build（完全一致なので build のみ）
    build_row = rows[1]
    assert build_row[0] == "build"
    assert build_row[1] == "True"
    assert build_row[2].endswith("build")

    # README.md
    readme_row = rows[2]
    assert readme_row[0] == "README.md"
    assert readme_row[1] == "True"
    assert readme_row[2].endswith("README.md")


def test_cli_partial_match(tmp_path: Path) -> None:
    """
    --partial-match 指定時に複数パスが列として展開される
    """
    create_test_structure(tmp_path)

    output_csv = tmp_path / "result.csv"

    run_cli([
        "prog",
        "--target", "build",
        "--partial-match",
        "--root", str(tmp_path),
        "--output", str(output_csv),
    ])

    rows = read_csv(output_csv)
    build_row = rows[1]

    assert build_row[0] == "build"
    assert build_row[1] == "True"

    paths = build_row[2:]
    assert any(p.endswith("build") for p in paths)
    assert any(p.endswith("build_debug") for p in paths)


def test_cli_no_target_error(tmp_path: Path) -> None:
    """
    target 未指定時はエラーになる
    """
    output_csv = tmp_path / "result.csv"

    with pytest.raises(SystemExit):
        run_cli([
            "prog",
            "--output", str(output_csv),
        ])

def test_cli_target_file(tmp_path: Path) -> None:
    """
    --target-file 指定で検索できる
    """
    create_test_structure(tmp_path)

    target_file = tmp_path / "folders.txt"
    target_file.write_text("build\n", encoding="utf-8")

    output_csv = tmp_path / "result.csv"

    run_cli([
        "prog",
        "--target-file", str(target_file),
        "--root", str(tmp_path),
        "--output", str(output_csv),
    ])

    rows = read_csv(output_csv)

    assert rows[1][0] == "build"
    assert rows[1][1] == "True"

def test_cli_ignore_case(tmp_path: Path) -> None:
    """
    --ignore-case 指定で大文字小文字を無視する
    """
    create_test_structure(tmp_path)

    output_csv = tmp_path / "result.csv"

    run_cli([
        "prog",
        "--target", "BUILD",
        "--ignore-case",
        "--root", str(tmp_path),
        "--output", str(output_csv),
    ])

    rows = read_csv(output_csv)

    assert rows[1][0] == "BUILD"
    assert rows[1][1] == "True"

def test_cli_fail_on_found(tmp_path: Path) -> None:
    """
    --fail-on-found 指定時、結果を CSV に出力したうえで fail する
    """
    create_test_structure(tmp_path)

    output_csv = tmp_path / "result.csv"

    with pytest.raises(SystemExit) as excinfo:
        run_cli([
            "prog",
            "--target", "build",
            "--fail-on-found",
            "--root", str(tmp_path),
            "--output", str(output_csv),
        ])

    # exit code = 1
    assert excinfo.value.code == 1

    # CSV は出力されている
    assert output_csv.exists()

    rows = read_csv(output_csv)
    assert rows[1][0] == "build"
    assert rows[1][1] == "True"

def test_cli_fail_on_found_message(tmp_path, capsys):
    create_test_structure(tmp_path)

    output_csv = tmp_path / "result.csv"

    with pytest.raises(SystemExit):
        run_cli([
            "prog",
            "--target", "build",
            "--fail-on-found",
            "--root", str(tmp_path),
            "--output", str(output_csv),
        ])

    captured = capsys.readouterr()
    assert "forbidden targets detected" in captured.err
