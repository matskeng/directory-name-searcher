from pathlib import Path

from directory_name_searcher.loader import load_folder_names


def test_load_folder_names_basic(tmp_path: Path) -> None:
    """
    基本的な読み込みができること
    """
    input_file = tmp_path / "folders.txt"
    input_file.write_text(
        "build\ndist\nout\n",
        encoding="utf-8",
    )

    result = load_folder_names(input_file)

    assert result == ["build", "dist", "out"]


def test_load_folder_names_ignore_empty_lines(tmp_path: Path) -> None:
    """
    空行が無視されること
    """
    input_file = tmp_path / "folders.txt"
    input_file.write_text(
        "\nbuild\n\n\ndist\n\n",
        encoding="utf-8",
    )

    result = load_folder_names(input_file)

    assert result == ["build", "dist"]


def test_load_folder_names_strip_whitespace(tmp_path: Path) -> None:
    """
    行頭・行末の空白が除去されること
    """
    input_file = tmp_path / "folders.txt"
    input_file.write_text(
        "  build  \n\tdist\t\n out \n",
        encoding="utf-8",
    )

    result = load_folder_names(input_file)

    assert result == ["build", "dist", "out"]


def test_load_folder_names_preserve_order(tmp_path: Path) -> None:
    """
    入力順が保持されること
    """
    input_file = tmp_path / "folders.txt"
    input_file.write_text(
        "zeta\nalpha\nbeta\n",
        encoding="utf-8",
    )

    result = load_folder_names(input_file)

    assert result == ["zeta", "alpha", "beta"]


def test_load_folder_names_utf8(tmp_path: Path) -> None:
    """
    UTF-8（日本語）を正しく読み込めること
    """
    input_file = tmp_path / "folders.txt"
    input_file.write_text(
        "ビルド\n出力\n",
        encoding="utf-8",
    )

    result = load_folder_names(input_file)

    assert result == ["ビルド", "出力"]