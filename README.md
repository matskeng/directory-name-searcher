# directory-name-searcher

フォルダ名およびファイル名を指定し、  
**カレントディレクトリ配下を再帰的に検索して CSV に出力する Python 製 CLI ツール**です。

- フォルダ名・ファイル名の両方に対応  
- 完全一致／部分一致の切り替えが可能  
- 出力順は入力順で安定  
- Excel で文字化けしない CSV を出力  

---

## 概要

本ツールは、以下のような用途を想定しています。

- プロジェクト配下に **特定のフォルダ／ファイルが存在するか確認**したい  
- CI において **禁止フォルダ・禁止ファイルの有無をチェック**したい  
- 結果を **CSV として後工程（Excel / スクリプト）で利用**したい  

---

## 動作環境

- Python **3.10 以上**
- 外部ライブラリ不要（標準ライブラリのみ使用）

---

## フォルダ構成

```text
directory-name-searcher/
├─ src/
│  └─ directory_name_searcher/
│     ├─ __init__.py
│     ├─ cli.py
│     └─ search.py
├─ README.md
├─ requirements.txt
└─ .gitignore
```

---

## インストール

### ローカルでそのまま実行する場合（推奨）

インストールは不要です。

```bat
cd src
```

---

## 使い方

### 基本

```bat
python -m directory_name_searcher.cli ^  --target build dist README.md ^  --output result.csv
```

---

### 部分一致で検索する場合

```bat
python -m directory_name_searcher.cli ^  --target build ^  --partial-match ^  --output result.csv
```

---

### 検索対象をファイルから指定する場合

```bat
python -m directory_name_searcher.cli ^  --target-file inputs/folders.txt ^  --output result.csv
```

`folders.txt` は以下の形式を想定します。

```text
build
dist
README.md
```

---

### 直接指定 + ファイル指定を併用する場合

```bat
python -m directory_name_searcher.cli ^  --target build ^  --target-file inputs/folders.txt ^  --output result.csv
```

※ 両方指定した場合は **和集合**が検索対象となります。

---

## オプション一覧

| オプション | 説明 |
|---|---|
| `--target` | 検索対象のフォルダ名／ファイル名（複数指定可） |
| `--target-file` | 検索対象名を1行1件で記載したファイル |
| `--root` | 検索開始ディレクトリ（デフォルト：カレントディレクトリ） |
| `--output` | 出力 CSV ファイルパス（必須） |
| `--partial-match` | 部分一致で検索する |
| `--ignore-case` | 大文字・小文字を区別しない |

---

## 出力形式（CSV）

CSV は **UTF-8（BOM付き）** で出力され、  
Windows 版 Excel でも文字化けせずに開けます。

### 出力例

```csv
name,found,paths
build,true,C:\work\projAbuild;C:\work\projBbuild_debug
dist,false,
README.md,true,C:\work\projA\README.md
```

### 各列の意味

| 列名 | 説明 |
|---|---|
| `name` | 検索対象名（フォルダ名／ファイル名） |
| `found` | 1件以上見つかった場合 `true` |
| `paths` | 該当パス一覧（`;` 区切り） |

---

## 仕様・注意点

- 検索は **再帰的** に行われます
- デフォルトでは **完全一致** です
- `--partial-match` 指定時は部分一致となります
- 出力結果の行順は **入力順を保持**します
- パスの並び順はアルファベット順にソートされます

---

## よくある用途例

- CI での **禁止フォルダ／ファイル検出**
- リポジトリ構成の定期チェック
- 大規模ディレクトリ調査の自動化

---

## ライセンス

MIT License
