# Study Async App
バックエンドで非同期処理を実行するWebアプリ開発の勉強  
環境構築を Docker + UV で行い、Cloud run にデプロイする

## 環境構築
1. UV で仮想環境構築
```
mkdir study-async-app
cd study-async-app
uv init 
uv venv
uv add fastapi uvicorn
```

2. `app` ディレクトリに `main.py` で FastAPI のアプリを作成しスクリプトで起動
```
bash rebuild.sh
```

3. uvicorn のホットリロードで実行しているので、スクリプト編集が即座に反映される

## 参考
- uv on docker: [uv 公式ドキュメント](https://docs.astral.sh/uv/guides/integration/docker/#non-editable-installs)