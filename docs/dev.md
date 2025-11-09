# 開発者向けドキュメント

リリース方法のメモ

## 1. バージョン更新

pyproject.tomlのバージョンを書き換えます。

## 2. 変更をコミット

```sh
git status
git commit -m "v0.2.5"
git tag v0.2.5
git push && git push --tags
```

## 3. デプロイ

```sh
make deploy
```

