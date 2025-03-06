# Ragflow Agent to Linebot Connector

## 概述

這是一個將 **Ragflow Agent** 與 **Linebot** 連接的工具，旨在提供一個簡單且高效的解決方案，將 Ragflow Agent 的功能與 Linebot 的交互能力整合。此工具基於 **Docker** 技術封裝，並利用以下技術栈進行開發：

- **FastAPI**：高效的 Web 框架，用於提供 HTTP API 接口
- **Line-Bot-SDK**：專為開發 Line 聊天機器人提供的 SDK
- **Ragflow-SDK**：與 Ragflow Agent 進行通信的 SDK

## 先決條件

在開始之前，您需要確保以下軟體已正確安裝：

- **Docker**：用於容器化部署，確保您的開發環境能夠順利運行。
- **Docker Compose**：用於定義和運行多容器 Docker 應用。

請參考 [Docker 官方文檔](https://docs.docker.com/get-docker/) 進行安裝。

## 安裝與配置

### 1. 複製 `.env.example` 並創建 `.env` 配置文件

首先，您需要複製 `.env.example` 文件並將其重命名為 `.env`，然後填寫必要的配置參數：

```bash
cp .env.example .env
```

### 2. 編輯 `.env` 配置文件

打開 `.env` 文件並根據您的需求填入以下參數：

- `LINE_CHANNEL_SECRET`：Linebot 的 Channel Secret
- `LINE_CHANNEL_ACCESS_TOKEN`：Linebot 的 Access Token
- `RAGFLOW_API_KEY`：Ragflow API 金鑰
- `RAGFLOW_BASE_URL` : Ragflow API URL(需加上port, ragflow 預設為9380)
- `AGENT_ID` : Ragflow Agent ID

確保所有參數都已正確設置，這是應用程序正常運行的關鍵。

### 3. 啟動應用

一旦 `.env` 文件配置完成，使用以下命令來構建並啟動 Docker 容器：

```bash
docker compose up --build -d
```

該命令會執行以下操作：

- 構建 Docker 映像
- 在背景運行應用服務

## 訪問與使用

當應用成功啟動後，您可以通過 FastAPI 提供的端點與 **Linebot** 進行交互。默認情況下，FastAPI 應用運行在端口 **5050**。您可以透過ngrok等三方內網穿透服務部署，並將url提供與Line Developer。
  


## 停止應用

若您需要停止運行的應用，請使用以下命令：

```bash
docker compose down
```

這將停止並移除所有相關的 Docker 容器、網絡和服務。

## 注意事項

- **配置文件**：請仔細檢查 `.env` 配置文件中的所有參數，尤其是與 Linebot 和 Ragflow Agent 相關的 API 金鑰。
- **端口設置**：默認情況下，FastAPI 運行在 **5050** 端口。如果需要更改端口，請在 `.env` 文件中設置 `PORT` 參數。
- **安全性**：請勿將 `.env` 文件暴露於公共版本控制系統，確保您的 API 密鑰和 Token 受到妥善保護。


## 開源許可

本專案採用 **MIT 許可證**。

此文案由ChatGPT產生。