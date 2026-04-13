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

    # ヘッダ確認
    assert rows[0] == ["folder_name", "found", "paths"]

    # build は見つかる
    assert rows[1][0] == "build"
    assert rows[1][1] == "True"
    assert "build" in rows[1][2]

    # README.md も見つかる
    assert rows[2][0] == "README.md"
    assert rows[2][1] == "True"
    assert rows[2][2].endswith("README.md")


def test_cli_partial_match(tmp_path: Path) -> None:
    """
    --partial-match 指定時に複数ヒットする
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

    paths = rows[1][2]

    assert "build" in paths
    assert "build_debug" in paths


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