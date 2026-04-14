
# directory-name-searcher

![Python Versions](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![CI - pytest](https://github.com/matskeng/directory-name-searcher/actions/workflows/pytest.yml/badge.svg)

フォルダ名およびファイル名を指定し、
**カレントディレクトリ配下を再帰的に検索して CSV に出力する Python 製 CLI ツール**です。

- フォルダ名・ファイル名の両方に対応
- 完全一致／部分一致の切り替えが可能
- 入力順を保持した安定した結果出力
- 1 行 = 1 検索対象、パスは複数列に展開
- Excel で文字化けしない UTF-8（BOM付き）CSV を出力
- CI / スクリプト用途を想定した軽量ツール

---

## 概要

本ツールは、以下のような用途での利用を想定しています。

- リポジトリ配下に **特定のフォルダ／ファイルが存在するかを確認**したい
- CI において **禁止フォルダ・禁止ファイルの有無を自動チェック**したい
- 検索結果を **CSV 形式で後続処理（Excel / スクリプト）に渡したい**

---

## リポジトリ構成

```text
directory-name-searcher/
├─ src/
│  └─ directory_name_searcher/
│     ├─ __init__.py
│     ├─ cli.py          # CLI エントリーポイント
│     ├─ search.py       # 再帰検索ロジック
│     └─ loader.py       # 入力ファイル読み込み処理
├─ tests/                # pytest による単体テスト
│  ├─ test_cli.py
│  ├─ test_search.py
│  └─ test_loader.py
├─ inputs/               # サンプル入力ファイル
├─ README.md
├─ pyproject.toml
├─ requirements.txt
└─ .gitignore
```

---

## 動作環境

- Python **3.10 以上**
- 外部ライブラリ不要（標準ライブラリのみ使用）

---

## インストール方法

本ツールは Python 製の CLI ツールとして、`pip` を用いてインストールできます。

### 前提条件

- Python **3.10 以上**
- `pip` が利用可能であること

### 開発用（推奨）：editable install

リポジトリを clone した状態で、リポジトリ直下にて以下を実行してください。

```bash
pip install -e .
```

この方法では、

- ソースコードを修正すると即座に CLI に反映される
- 開発・検証に適した形で利用できる

というメリットがあります。

インストール後、以下のコマンドが使用可能になります。

```bash
directory-name-searcher
```

### アンインストール

```bash
pip uninstall directory-name-searcher
```

---

## 実行方法

### 基本的な使い方

```bash
directory-name-searcher   --target build dist README.md   --output result.csv
```

---

### 検索対象をファイルで指定する場合

検索対象名を 1 行 1 件で記載したテキストファイルを用意します。

例：`inputs/folders.txt`

```text
build
dist
README.md
```

実行例：

```bash
directory-name-searcher   --target-file inputs/folders.txt   --output result.csv
```

---

### 部分一致で検索する場合

```bash
directory-name-searcher   --target build   --partial-match   --output result.csv
```

---

### 検索開始ディレクトリを指定する場合

```bash
directory-name-searcher   --target build   --root /path/to/project   --output result.csv
```

---

### バージョン表示

```bash
directory-name-searcher --version
```

---

### CI用途（fail-on-found）

```bash
directory-name-searcher \
  --target-file forbidden.txt \
  --output result.csv \
  --fail-on-found
```
検索対象が 1 件でも見つかった場合、CSV を出力したうえで終了コード 1 を返します。

---

### ヘルプの表示

利用可能なオプション一覧は以下で確認できます。

```bash
directory-name-searcher --help
```

---

## 出力形式（CSV）

CSV は **UTF-8（BOM付き）** で出力され、Windows 版 Excel でも文字化けせずに開くことができます。

### 出力仕様

- **1 行 = 1 検索対象（name）**
- 見つかったパスは **複数列（path_1, path_2, ...）として展開**
- 同一検索対象で複数ヒットした場合も 1 行に集約
- 見つからなかった場合は `found=False`、パス列は空

### 出力例

```csv
name,found,path_1,path_2
build,True,C:\work\projA\build,C:\work\projA\build_debug
dist,False,
README.md,True,C:\work\projA\README.md
```

### 各列の意味

| 列名 | 説明 |
|------|------|
| `name` | 検索対象名（フォルダ名／ファイル名） |
| `found` | 該当パスが 1 件以上存在する場合 `True` |
| `path_n` | n 番目に見つかったパス |

---

## テスト

本リポジトリでは `pytest` を用いた単体テストを実装しています。

```bash
pip install -e .[dev]
pytest
```

---

## ライセンス

MIT License
