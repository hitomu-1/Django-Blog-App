## 概要
勉強した内容を記録するブログアプリ
チーム開発で使用するDjangoの学習のために作成

## URL（仮デプロイ）
https://hitomu01.pythonanywhere.com/

## 開発環境
Python 3.9.2


## 実行コマンド

### 必要なライブラリのインストール
```python
# pythonの仮装環境下で実行
pip install -r requirements.txt
```

### マイグレーション
```Python
# マイグレーション
python manage.py makemigrations

python manage.py migrate

```
### サーバーの起動
```python
python manage.py runserver
```

## 備考
SECRET_KEYはプロジェクト直下に.envを作成して追加する

## 今後の予定
- OpenAIのAPIサービスと連携して機能拡張
- Dockerコンテナでの運用
- AWSへのデプロイ
  （Webサーバー：Nginx、DB：RDS（MySQL））
