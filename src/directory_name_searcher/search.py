from pathlib import Path
from typing import Dict, Iterable, List


def search_directories(
    root: Path,
    target_names: Iterable[str],
    ignore_case: bool = False,
    partial_match: bool = False,
) -> Dict[str, List[Path]]:
    """
    指定した名前（フォルダ名・ファイル名）を、
    root 配下から再帰的に検索する。

    - フォルダ / ファイルの両方を対象
    - 完全一致 / 部分一致 切替可
    - 入力順・出力順を保証
    """
    target_list = list(target_names)
    results: Dict[str, List[Path]] = {name: [] for name in target_list}

    def normalize(value: str) -> str:
        return value.lower() if ignore_case else value

    normalized_targets = {
        normalize(name): name for name in target_list
    }

    for path in root.rglob("*"):
        name = normalize(path.name)

        for norm_target, original_target in normalized_targets.items():
            if partial_match:
                matched = norm_target in name
            else:
                matched = norm_target == name

            if matched:
                results[original_target].append(path)

    # パス順を安定化
    for paths in results.values():
        paths.sort()

    return results