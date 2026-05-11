# HTML to PDF Batch Converter

一個功能強大的批量 HTML 轉 PDF 桌面應用程序，支援 macOS 和 Windows。

## ✨ 功能特性

- 🚀 批量轉換 HTML 文件為 PDF
- 📁 支援選擇單個文件或整個文件夾
- 🔄 遞歸掃描子文件夾選項
- 📊 實時進度顯示
- 🎨 高保真轉換（完整保留 CSS 樣式、圖片、佈局）
- ⚙️ 自動記憶上次使用的設置
- 🌐 完整支援中文和 UTF-8 編碼
- 💾 自定義輸出目錄
- ❌ 隨時停止轉換
- 📝 詳細的錯誤報告

## 📦 下載和安裝

### macOS

1. 下載 `HTMLtoPDF.dmg`
2. 雙擊打開 DMG 文件
3. 拖動應用到「應用程序」文件夾
4. 完成！無需安裝 Python 或其他依賴

### Windows

1. 下載 `HTMLtoPDF-Setup.exe`（或 `HTMLtoPDF.zip`）
2. 運行安裝程序（或解壓 ZIP）
3. 啟動應用
4. 完成！無需安裝 Python 或其他依賴

## 🚀 使用方法

1. **選擇 HTML 文件**
   - 點擊「選擇文件」選擇單個或多個 HTML 文件
   - 或點擊「選擇文件夾」選擇整個文件夾
   - 勾選「遞歸掃描子文件夾」以包含子目錄中的文件

2. **設置輸出目錄**
   - 點擊「選擇輸出目錄」
   - 選擇 PDF 文件的保存位置

3. **開始轉換**
   - 點擊「開始轉換」按鈕
   - 查看實時進度和狀態
   - 轉換完成後會顯示統計信息

4. **查看結果**
   - 點擊「打開輸出目錄」查看生成的 PDF 文件

## 🛠️ 開發者指南

### 環境要求

- Python 3.8+
- PyQt5
- wkhtmltopdf

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 運行應用

```bash
# 方法 1: 使用 Python 模塊
python -m src.main

# 方法 2: 設置 PYTHONPATH
export PYTHONPATH=.
python src/main.py
```

### 運行測試

```bash
pytest tests/ -v
```

### 打包應用

#### macOS

```bash
# 安裝打包依賴
pip install -r requirements-build.txt

# 運行構建腳本
chmod +x build.sh
./build.sh

# 輸出文件
# - dist/HTMLtoPDF.app (應用程序)
# - dist/HTMLtoPDF.dmg (安裝程序)
```

詳細說明請參考 [BUILD.md](BUILD.md)

#### Windows

```batch
# 安裝打包依賴
pip install -r requirements-build.txt

# 下載 wkhtmltopdf Windows 版本
# 放置到 wkhtmltopdf-windows\bin\wkhtmltopdf.exe

# 運行構建腳本
build-windows.bat

# 輸出文件
# - dist\HTMLtoPDF\HTMLtoPDF.exe
```

詳細說明請參考 [BUILD-WINDOWS.md](BUILD-WINDOWS.md)

## 📁 項目結構

```
html-pdf/
├── src/
│   ├── main.py              # 應用入口
│   ├── core/
│   │   ├── converter.py     # 轉換引擎
│   │   └── worker.py        # 後台工作線程
│   ├── ui/
│   │   ├── main_window.py   # 主窗口
│   │   └── dialogs.py       # 自定義對話框
│   └── utils/
│       ├── config.py        # 配置管理
│       └── file_utils.py    # 文件工具
├── tests/                   # 測試文件
├── docs/                    # 文檔
├── requirements.txt         # Python 依賴
├── requirements-build.txt   # 打包依賴
├── HTMLtoPDF.spec          # macOS 打包配置
├── HTMLtoPDF-windows.spec  # Windows 打包配置
├── build.sh                # macOS 構建腳本
└── build-windows.bat       # Windows 構建腳本
```

## 🔧 技術棧

- **GUI 框架**: PyQt5
- **PDF 轉換**: wkhtmltopdf
- **多線程**: QThread
- **配置管理**: QSettings
- **打包工具**: PyInstaller
- **測試框架**: pytest

## 📝 架構設計

採用 MVC 架構模式：

- **Model**: `ConverterEngine` - 處理 HTML 到 PDF 的轉換邏輯
- **View**: `MainWindow` - 用戶界面和交互
- **Controller**: `ConverterThread` - 協調轉換流程和更新 UI
- **Config**: `AppConfig` - 管理用戶設置持久化

## 🐛 故障排除

### wkhtmltopdf 未找到

應用會自動檢測 wkhtmltopdf：
1. 檢查嵌入的二進制文件（打包版本）
2. 檢查系統 PATH
3. 檢查常見安裝位置

如果仍未找到，可以手動指定路徑。

### 轉換失敗

常見原因：
- HTML 文件包含無效的 CSS 或 JavaScript
- 圖片路徑不正確（使用相對路徑）
- 文件編碼問題（確保使用 UTF-8）

### 應用啟動慢

打包後的應用首次啟動需要解壓文件，這是正常現象。

## 📄 許可證

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📧 聯繫

如有問題或建議，請提交 Issue。

---

**版本**: 1.0.0  
**最後更新**: 2024-05-11
