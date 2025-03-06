# 使用 Python 3.10 作為基礎映像
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製所有專案檔案到容器內
COPY . /app

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# Expose 5050 端口
EXPOSE 5050

# 啟動 uvicorn 服務
CMD ["uvicorn", "app.line_service:app", "--host", "0.0.0.0", "--port", "5050"]
