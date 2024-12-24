# Mac Tags to Dropbox

這個程式可以讀取 MacOS 資料夾中的檔案標籤，並將這些標籤同步到 Dropbox 對應的檔案中。

## 功能特點

- 讀取 MacOS 檔案標籤
- 自動同步標籤到 Dropbox
- 詳細的操作日誌
- 支援批次處理

## 安裝需求

- Python 3.8+
- MacOS 作業系統
- Dropbox API Token

## 安裝步驟

1. 下載專案：
```bash
git clone https://github.com/yourusername/mac-tags-to-dropbox.git
```

2. 安裝依賴套件：
```bash
pip install -r requirements.txt
```

3. 在 config/config.yaml 中設定您的 Dropbox API Token

## 使用方式

1. 設定配置文件
2. 執行程式：
```bash
python src/main.py --folder "您的資料夾路徑"
```

## 注意事項

- 需要預先在 Dropbox 開發者控制台建立應用程式並取得 API Token
- 確保要同步的資料夾在本地端和 Dropbox 都存在