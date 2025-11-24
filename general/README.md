# 解答管理システム

generalフォルダの解答を一覧表示・閲覧できるWebアプリケーションです。

## 機能

- すべての解答（現在・過去問わず）を一覧表示
- 科目・セクション・問番号・日付で整理
- フィルタリング機能（科目、セクション、問番号で絞り込み）
- ソート機能（日付順、問番号順、科目順）
- クリックで解答を閲覧（モーダルウィンドウ）

## ファイル構成

```
general/
├── index.html          # メインのWebページ
├── styles.css          # スタイルシート
├── app.js              # JavaScript（解答一覧の読み込み、フィルタリング、ソート）
├── archive/            # 過去の解答保存フォルダ
│   └── (過去の解答ファイル)
├── output/
│   └── solution.html   # 現在の解答（最新）
├── template.html        # 解答のテンプレート
├── launcher.ipynb      # 解答生成用のノートブック
├── assignment.txt       # 問題番号
├── input.txt           # 講義資料
└── README.md           # このファイル
```

## 使い方

### 1. 解答の生成

1. `launcher.ipynb`を開く
2. セルを実行（▶️をクリック）
3. プロンプトがCursorに送信される
4. 解答が生成され、`output/solution.html`に保存される
5. 既存の解答は自動的に`archive/`フォルダに移動される

### 2. 解答の閲覧

1. `index.html`をブラウザで開く
2. 解答一覧が表示される
3. フィルタやソートで目的の解答を探す
4. 「閲覧」ボタンをクリックして解答を表示

### 3. 解答情報の抽出

解答の情報（科目、セクション、問番号、日付）は以下の方法で取得されます：

- **科目名**: `input.txt`の1行目から抽出
  - 例: 「線形代数（坂口）2025 90」→「線形代数（坂口）」
- **セクション**: `input.txt`の2行目から抽出
  - 例: 「§9 直交性」→「§9」
- **問番号**: `assignment.txt`から取得、またはファイル名から抽出
  - 例: 「問５」
- **日付**: ファイル名から抽出
  - 例: `solution_問５_20250101_120000.html`→「2025/01/01 12:00:00」

## GitHub Pagesでの公開

### 1. GitHubリポジトリの準備

1. GitHubで新しいリポジトリを作成
2. generalフォルダの内容をリポジトリにアップロード

```bash
cd /Users/user/Library/CloudStorage/Box-Box/Personal/dev/homework/general
git init
git add .
git commit -m "Initial commit: 解答管理システム"
git remote add origin https://github.com/kosei-doi/homework-storage.git
git branch -M main
git push -u origin main
```

### 2. GitHub Pagesの有効化

1. リポジトリの「Settings」→「Pages」に移動
2. Source: "Deploy from a branch" を選択
3. Branch: `main` / `/(root)` を選択
4. 「Save」をクリック

### 3. アクセス

数分後、以下のURLでアクセス可能になります：
```
https://kosei-doi.github.io/homework-storage/
```

リポジトリ: [https://github.com/kosei-doi/homework-storage](https://github.com/kosei-doi/homework-storage)

### 4. 注意事項

- GitHub Pagesでは、ファイルシステムへの直接アクセスができないため、アーカイブされた解答ファイルの自動検出が制限される場合があります
- アーカイブファイルを表示するには、`app.js`の`knownArchives`配列にファイル名を追加するか、メタデータJSONファイルを使用してください

## 今後の改善案

- 解答生成時にメタデータJSONファイルを自動生成
- アーカイブファイルの自動検出機能の改善
- 検索機能の追加
- 解答のプレビュー機能

## トラブルシューティング

### 解答が表示されない

- `output/solution.html`が存在するか確認
- ブラウザのコンソールでエラーを確認
- CORSエラーの場合、ローカルサーバーを使用（例: `python -m http.server`）

### フィルタが機能しない

- 解答情報が正しく抽出されているか確認
- `input.txt`と`assignment.txt`の形式を確認

### モーダルで解答が表示されない

- 解答ファイルのパスが正しいか確認
- MathJaxの読み込みエラーを確認

## ライセンス

このプロジェクトは個人の学習目的で使用されています。

