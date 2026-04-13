from pathlib import Path

from directory_name_searcher.search import search_directories


def create_test_structure(root: Path) -> None:
    """
    テスト用のディレクトリ・ファイル構造を作成する

    root/
    ├─ build/
    ├─ build_debug/
    ├─ dist/
    ├─ src/
    │  └─ main.py
    └─ README.md
    """
    (root / "build").mkdir()
    (root / "build_debug").mkdir()
    (root / "dist").mkdir()
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('hello')")
    (root / "README.md").write_text("readme")


def test_search_exact_match_directory(tmp_path: Path) -> None:
    create_test_structure(tmp_path)

    results = search_directories(
        root=tmp_path,
        target_names=["build"],
        partial_match=False,
    )

    assert "build" in results
    assert len(results["build"]) == 1
    assert results["build"][0].name == "build"


def test_search_partial_match_directory(tmp_path: Path) -> None:
    create_test_structure(tmp_path)

    results = search_directories(
        root=tmp_path,
        target_names=["build"],
        partial_match=True,
    )

    names = {path.name for path in results["build"]}

    assert "build" in names
    assert "build_debug" in names
    assert len(names) == 2


def test_search_file_name(tmp_path: Path) -> None:
    create_test_structure(tmp_path)

    results = search_directories(
        root=tmp_path,
        target_names=["README.md"],
    )

    assert len(results["README.md"]) == 1
    assert results["README.md"][0].is_file()
    assert results["README.md"][0].name == "README.md"


def test_search_not_found(tmp_path: Path) -> None:
    create_test_structure(tmp_path)

    results = search_directories(
        root=tmp_path,
        target_names=["not_exist"],
    )

    assert results["not_exist"] == []


def test_search_order_is_preserved(tmp_path: Path) -> None:
    create_test_structure(tmp_path)

    targets = ["dist", "build", "README.md"]

    results = search_directories(
        root=tmp_path,
        target_names=targets,
    )

    # dict のキー順が入力順どおりであること
    assert list(results.keys()) == targets
