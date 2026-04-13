"""
フォルダ名検索 CLI ツール
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Set
from importlib.metadata import version

from directory_name_searcher.search import search_directories


def load_targets_from_file(path: Path) -> List[str]:
    """ファイルからフォルダ名を読み込む（1行1件）"""
    targets: List[str] = []

    with path.open(encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                targets.append(name)

    return targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="フォルダ名を再帰的に検索し、CSVに出力します。"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('directory-name-searcher')}",
        help="バージョンを表示して終了する",
    )

    parser.add_argument(
        "--target",
        nargs="+",
        help="検索対象のフォルダ名（複数指定可）",
    )

    parser.add_argument(
        "--target-file",
        type=Path,
        help="検索対象フォルダ名を記載したファイル（1行1件）",
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="検索開始ディレクトリ（デフォルト：カレントディレクトリ）",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="結果を出力するCSVファイル",
    )

    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="大文字・小文字を区別しない",
    )

    parser.add_argument(
        "--partial-match",
        action="store_true",
        help="フォルダ名を部分一致で検索する",
    )

    parser.add_argument(
        "--fail-on-found",
        action="store_true",
        help="検索対象が1つでも見つかった場合に終了コード1で終了する",
    )
    
    return parser.parse_args()

def unique_preserve_order(values: List[str]) -> List[str]:
    seen = set()
    result = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result

def main() -> None:
    args = parse_args()

    # --- 検索対象フォルダ名を収集 ---
    targets: List[str] = []

    if args.target:
        targets.extend(args.target)

    if args.target_file:
        targets.extend(load_targets_from_file(args.target_file))

    targets = unique_preserve_order(targets)

    if not targets:
        raise SystemExit(
            "error: --target または --target-file を指定してください"
        )

    # --- 検索実行 ---
    results = search_directories(
        root=args.root,
        target_names=targets,
        ignore_case=args.ignore_case,
        partial_match=args.partial_match,
    )

    # --- CSV 出力 ---
    with args.output.open(
        "w",
        newline="",
        encoding="utf-8-sig"  # Excel対策：UTF-8 BOM付き
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "found", "paths"])

        for folder_name, paths in results.items():
            writer.writerow(
                [
                    folder_name,
                    bool(paths),
                    ";".join(str(p) for p in paths),
                ]
            )

    print(f"検索結果を CSV に出力しました: {args.output}")

    if args.fail_on_found and any(paths for paths in results.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()