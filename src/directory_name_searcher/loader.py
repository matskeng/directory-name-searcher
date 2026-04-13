"""
入力ファイルから検索対象のフォルダ名を読み込む処理を提供するモジュール。
"""

from pathlib import Path
from typing import List


def load_folder_names(path: Path) -> List[str]:
    """
    テキストファイルから検索対象のフォルダ名を読み込む。

    ファイルは以下の形式を想定する。
    - 1行につき1フォルダ名
    - 空行は無視される
    - 行頭・行末の空白は除去される

    Args:
        path (Path):
            フォルダ名を記載したテキストファイルのパス

    Returns:
        List[str]:
            読み込んだフォルダ名のリスト
    """
    folder_names: List[str] = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            name = line.strip()

            # 空行は無視する
            if not name:
                continue

            folder_names.append(name)

    return folder_names