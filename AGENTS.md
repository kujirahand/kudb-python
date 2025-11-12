# KUDB-Python プロジェクト仕様書

## プロジェクト概要

**プロジェクト名**: kudb-python  
**作成者**: kujirahand  
**ライセンス**: MIT  
**説明**: Pythonのためのシンプルなドキュメントデータベースライブラリ

## 技術仕様

### アーキテクチャ

- **バックエンド**: SQLite3
- **対応Python版**: 3.6以上
- **パッケージタイプ**: Pure Python Package
- **配布方法**: PyPI (pip install kudb)

### 主要機能

1. **ドキュメントベースDB**: JSON形式のドキュメント保存・検索
2. **キーバリューストア**: シンプルなKVS機能
3. **メモリDB対応**: ":memory:"での一時的なデータベース
4. **キャッシュ機能**: データベース接続のキャッシュ

## プロジェクト構造

```text
kudb-python/
├── kudb/                      # メインパッケージ
│   ├── __init__.py           # パッケージ初期化
│   ├── kudb.py               # メインモジュール (960行)
│   └── py.typed              # 型ヒント対応
├── tests/                     # テストディレクトリ
│   ├── __init__.py
│   ├── test_doc.py           # ドキュメントDB機能テスト
│   ├── test_kvs.py           # KVS機能テスト
│   └── test_set_keys_from_dict.py # 辞書からキー設定のテスト
├── docs/                      # ドキュメント
│   ├── functions.md          # 関数リファレンス
│   ├── README_ja.md          # 日本語README
│   └── dev.md                # 開発者向けドキュメント
├── sample-*.py               # サンプルコード
├── pyproject.toml            # プロジェクト設定
├── setup.py                  # セットアップスクリプト
├── requirements.txt          # 依存関係
└── requirements-dev.txt      # 開発用依存関係
```

## 核となるクラスと関数

### 主要クラス

- **KudbError**: カスタム例外クラス

### グローバル変数

- `db`: SQLite接続オブジェクト
- `cache_db`: データベース接続キャッシュ
- `cur_filename`: 現在のファイル名
- `cur_tablename`: 現在のテーブル名
- `SQLS`: SQL文テンプレート辞書

### 接続管理関数

- `connect(filename, table_name)`: データベース接続
- `change_db(filename, table_name)`: データベース変更
- `close()`: データベース切断

### ドキュメントDB関数

- `insert(value, tag)`: ドキュメント挿入
- `insert_many(values)`: 複数ドキュメント挿入
- `get_all()`: 全ドキュメント取得
- `get_by_id(doc_id)`: ID指定取得
- `get_by_tag(tag)`: タグ指定取得
- `update(doc_id, value, tag)`: ドキュメント更新
- `delete(doc_id)`: ドキュメント削除
- `find(callback)`: 条件検索
- `count_doc()`: ドキュメント数カウント

### キーバリューストア関数

- `set_key(key, value)`: キー設定
- `get_key(key)`: キー取得
- `has_key(key)`: キー存在確認
- `keys()`: 全キー一覧
- `delete_key(key)`: キー削除
- `set_keys_from_dict(dic)`: 辞書からキー一括設定

### ユーティリティ関数

- `clear()`: 全データクリア
- `clear_doc()`: ドキュメントのみクリア
- `clear_keys()`: キーのみクリア
- `recent(limit, offset)`: 最新ドキュメント取得

## データベーススキーマ

### ドキュメントテーブル (doc_テーブル名)

```sql
CREATE TABLE IF NOT EXISTS doc__TABLE_NAME__ (
    id INTEGER PRIMARY KEY,
    tag TEXT DEFAULT '',
    value TEXT DEFAULT '',
    ctime INTEGER DEFAULT 0,
    mtime INTEGER DEFAULT 0
)
```

### キーバリューテーブル (テーブル名)

```sql
CREATE TABLE IF NOT EXISTS __TABLE_NAME__ (
    key_id INTEGER PRIMARY KEY,
    key TEXT UNIQUE,
    value TEXT DEFAULT '',
    ctime INTEGER DEFAULT 0,
    mtime INTEGER DEFAULT 0
)
```

## テスト仕様

### テスト構成

- **フレームワーク**: pytest
- **カバレッジ**: 6個のテスト (100%成功)
- **テストファイル**: tests/ディレクトリ内

### pytest設定 (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### 実行方法

```bash
# 全テスト実行
python -m pytest

# 詳細モードでテスト実行
python -m pytest -v

# 特定ディレクトリのテスト実行
python -m pytest tests/ -v
```

## 使用例

### 基本的な使用方法

```python
import kudb

# データベース接続
kudb.connect('test.db')

# データ挿入
kudb.insert({'name': 'Tako', 'age': 18})
kudb.insert({'name': 'Ika', 'age': 19})

# データ取得
for row in kudb.get_all():
    print('データ:', row)

# データベース切断
kudb.close()
```

### キーバリューストア使用例

```python
import kudb

kudb.connect('kvs.db')

# キー設定
kudb.set_key('user_name', 'Tako')
kudb.set_key('user_age', 18)

# キー取得
name = kudb.get_key('user_name')
age = kudb.get_key('user_age')

kudb.close()
```

## 配布・デプロイ

### PyPI配布

- **パッケージ名**: kudb
- **インストール**: `pip install kudb`
- **リポジトリ**: <https://pypi.org/project/kudb/>

### 開発環境セットアップ

```bash
# リポジトリクローン
git clone https://github.com/kujirahand/kudb-python.git
cd kudb-python

# 依存関係インストール
pip install -r requirements-dev.txt

# テスト実行
python -m pytest tests/
```

## 開発ワークフロー

### バージョン管理

- **Git**: GitHub (kujirahand/kudb-python)
- **ブランチ**: main

### 品質管理

- **テストカバレッジ**: pytestによる自動テスト
- **型チェック**: py.typedファイルによる型ヒント対応
- **コードスタイル**: Python標準スタイル準拠

### リリースプロセス

1. バージョン更新 (`update_version.py`)
2. テスト実行 (`test_all.sh`)
3. ドキュメント生成 (`mkdoc.py`)
4. PyPI公開 (`publish_test.sh`)

## 依存関係

### 実行時依存関係

- **Python**: >= 3.6
- **標準ライブラリのみ**: sqlite3, json, time, typing

### 開発時依存関係

- **pytest**: テスト実行
- **その他**: requirements-dev.txtに記載

## 制限事項・注意点

1. **SQLite制限**: SQLite3の制限に従う
2. **スレッドセーフティ**: 明示的な同期制御なし
3. **メモリ使用量**: 大量データ時の考慮が必要
4. **バックアップ**: ユーザー責任でのデータバックアップ

## 今後の拡張予定

- パフォーマンス最適化
- 同期処理の改善
- 追加的なクエリ機能
- ドキュメントの充実

---

**最終更新**: 2025年11月12日  
**対象バージョン**: kudb 0.2.7
