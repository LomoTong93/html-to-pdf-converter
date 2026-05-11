# GitHub Actions 自動化打包指南

本項目使用 GitHub Actions 自動化構建 macOS 和 Windows 版本。

## 🚀 自動化構建流程

### 觸發方式

1. **標籤觸發（推薦）**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   推送標籤後會自動構建並創建 GitHub Release

2. **手動觸發**
   - 訪問 GitHub 倉庫
   - 點擊 "Actions" 標籤
   - 選擇 "Build and Release" workflow
   - 點擊 "Run workflow"

### 構建內容

GitHub Actions 會自動：
- ✅ 在 macOS 上構建 `.app` 和 `.dmg`
- ✅ 在 Windows 上構建 `.exe` 和 `.zip`
- ✅ 自動安裝 wkhtmltopdf
- ✅ 運行所有測試
- ✅ 創建 GitHub Release（標籤觸發時）
- ✅ 上傳構建產物

## 📦 構建產物

### macOS
- `HTMLtoPDF.dmg` - macOS 安裝程序（約 56MB）
- `HTMLtoPDF.app` - macOS 應用程序包

### Windows
- `HTMLtoPDF-Windows.zip` - Windows 可執行文件壓縮包（約 60-80MB）
  - 解壓後運行 `HTMLtoPDF.exe`

## 🔧 設置步驟

### 1. 初始化 Git 倉庫（如果還沒有）

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. 創建 GitHub 倉庫

1. 訪問 https://github.com/new
2. 創建新倉庫（例如：`html-to-pdf-converter`）
3. 不要初始化 README、.gitignore 或 license

### 3. 推送代碼到 GitHub

```bash
# 添加遠程倉庫
git remote add origin https://github.com/YOUR_USERNAME/html-to-pdf-converter.git

# 推送代碼
git branch -M main
git push -u origin main
```

### 4. 創建並推送標籤觸發構建

```bash
# 創建標籤
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送標籤
git push origin v1.0.0
```

### 5. 查看構建進度

1. 訪問 GitHub 倉庫
2. 點擊 "Actions" 標籤
3. 查看正在運行的 workflow

構建通常需要 10-15 分鐘。

### 6. 下載構建產物

#### 方法 A: 從 GitHub Release 下載（標籤觸發）

1. 訪問倉庫的 "Releases" 頁面
2. 找到對應的版本（例如 v1.0.0）
3. 下載 `HTMLtoPDF.dmg` 或 `HTMLtoPDF-Windows.zip`

#### 方法 B: 從 Actions Artifacts 下載（手動觸發）

1. 訪問 "Actions" 標籤
2. 點擊對應的 workflow run
3. 在 "Artifacts" 部分下載：
   - `macos-build`
   - `windows-build`

## 🔄 更新版本

每次發布新版本：

```bash
# 1. 提交所有更改
git add .
git commit -m "Update: 新功能描述"
git push

# 2. 創建新標籤
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0

# 3. GitHub Actions 自動構建並發布
```

## 🐛 故障排除

### 構建失敗

1. **檢查 Actions 日誌**
   - 訪問 "Actions" 標籤
   - 點擊失敗的 workflow
   - 查看詳細錯誤信息

2. **常見問題**
   - Python 依賴問題：檢查 `requirements.txt`
   - wkhtmltopdf 安裝失敗：檢查安裝命令
   - 測試失敗：本地運行 `pytest` 確認

### 權限問題

確保倉庫設置中啟用了 Actions：
1. 訪問倉庫 "Settings"
2. 點擊 "Actions" → "General"
3. 確保 "Allow all actions and reusable workflows" 已選中

### Release 創建失敗

確保 `GITHUB_TOKEN` 有足夠權限：
1. 訪問倉庫 "Settings"
2. 點擊 "Actions" → "General"
3. 在 "Workflow permissions" 中選擇 "Read and write permissions"

## 📊 構建時間

- macOS 構建：約 8-10 分鐘
- Windows 構建：約 8-10 分鐘
- 總計：約 15-20 分鐘（並行執行）

## 🎯 高級配置

### 添加測試步驟

在 `.github/workflows/build.yml` 中添加：

```yaml
- name: Run tests
  run: |
    pytest tests/ -v
```

### 添加代碼簽名（macOS）

```yaml
- name: Sign macOS app
  run: |
    codesign --force --deep --sign "Developer ID" dist/HTMLtoPDF.app
```

需要在 GitHub Secrets 中添加證書。

### 自定義構建觸發條件

```yaml
on:
  push:
    branches: [ main ]  # 推送到 main 分支時構建
  pull_request:
    branches: [ main ]  # PR 時構建
  release:
    types: [ created ]  # 創建 Release 時構建
```

## 📝 版本號規範

建議使用語義化版本號（Semantic Versioning）：

- `v1.0.0` - 主要版本（重大更改）
- `v1.1.0` - 次要版本（新功能）
- `v1.1.1` - 修訂版本（bug 修復）

## 🔗 相關資源

- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [PyInstaller 文檔](https://pyinstaller.org/)
- [語義化版本號](https://semver.org/)

---

**提示**: 首次構建可能需要更長時間，因為需要下載和緩存依賴。後續構建會更快。
