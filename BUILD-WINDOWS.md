# Windows 打包指南

## 前置要求

1. **Windows 系统**（Windows 10 或更高版本）
2. **Python 3.8+** 已安装
3. **Git**（可选，用于克隆代码）

## 步骤 1: 准备项目

```cmd
# 克隆或复制项目到 Windows 机器
cd html-pdf

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-build.txt
```

## 步骤 2: 下载 wkhtmltopdf Windows 版本

### 方法 A: 自动下载（推荐）

```cmd
# 创建目录
mkdir wkhtmltopdf-windows\bin

# 下载 wkhtmltopdf Windows 版本
# 访问: https://wkhtmltopdf.org/downloads.html
# 下载: wkhtmltox-0.12.6-1.msvc2015-win64.exe
# 安装后，复制 wkhtmltopdf.exe 到项目目录
```

### 方法 B: 使用已安装的版本

如果你已经安装了 wkhtmltopdf，修改 `HTMLtoPDF-windows.spec` 文件：

```python
datas=[
    ('C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe', 'wkhtmltopdf/bin'),
],
```

## 步骤 3: 运行打包

```cmd
# 使用 Windows spec 文件打包
pyinstaller HTMLtoPDF-windows.spec --clean --noconfirm

# 打包完成后，可执行文件位于:
# dist\HTMLtoPDF\HTMLtoPDF.exe
```

## 步骤 4: 测试应用

```cmd
# 运行打包后的应用
dist\HTMLtoPDF\HTMLtoPDF.exe
```

## 步骤 5: 创建安装程序（可选）

### 使用 Inno Setup 创建安装程序

1. 下载并安装 [Inno Setup](https://jrsoftware.org/isinfo.php)
2. 创建安装脚本（见下方）
3. 编译生成 `HTMLtoPDF-Setup.exe`

### Inno Setup 脚本示例

创建文件 `installer.iss`:

```ini
[Setup]
AppName=HTML to PDF Converter
AppVersion=1.0
DefaultDirName={pf}\HTMLtoPDF
DefaultGroupName=HTML to PDF Converter
OutputDir=dist
OutputBaseFilename=HTMLtoPDF-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\HTMLtoPDF\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\HTML to PDF Converter"; Filename: "{app}\HTMLtoPDF.exe"
Name: "{commondesktop}\HTML to PDF Converter"; Filename: "{app}\HTMLtoPDF.exe"
```

## 自动化脚本

创建 `build-windows.bat`:

```batch
@echo off
echo ========================================
echo Building HTML to PDF Converter for Windows
echo ========================================

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt
pip install -r requirements-build.txt

echo.
echo Step 2: Checking wkhtmltopdf...
if not exist "wkhtmltopdf-windows\bin\wkhtmltopdf.exe" (
    echo ERROR: wkhtmltopdf.exe not found!
    echo Please download wkhtmltopdf and place it in wkhtmltopdf-windows\bin\
    echo Download from: https://wkhtmltopdf.org/downloads.html
    pause
    exit /b 1
)

echo.
echo Step 3: Building executable...
pyinstaller HTMLtoPDF-windows.spec --clean --noconfirm

echo.
echo ========================================
echo Build completed!
echo ========================================
echo Executable: dist\HTMLtoPDF\HTMLtoPDF.exe
echo.
pause
```

## 故障排除

### 问题 1: 缺少 DLL 文件

如果运行时提示缺少 DLL，在 spec 文件中添加：

```python
binaries=[
    ('C:\\Windows\\System32\\msvcp140.dll', '.'),
    ('C:\\Windows\\System32\\vcruntime140.dll', '.'),
],
```

### 问题 2: wkhtmltopdf 未找到

确保 `wkhtmltopdf.exe` 已正确嵌入：
- 检查 `dist\HTMLtoPDF\wkhtmltopdf\bin\wkhtmltopdf.exe` 是否存在
- 检查 spec 文件中的 datas 路径是否正确

### 问题 3: 应用启动慢

这是正常的，PyInstaller 打包的应用首次启动需要解压文件。

## 文件大小优化

如果 EXE 文件太大，可以：

1. 使用 UPX 压缩（已在 spec 中启用）
2. 排除不需要的模块：

```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
],
```

## 分发

最终可以分发：
- **单文件夹**: `dist\HTMLtoPDF\` 整个文件夹（约 60-80MB）
- **安装程序**: `HTMLtoPDF-Setup.exe`（使用 Inno Setup 创建）

用户无需安装 Python 或 wkhtmltopdf，直接运行即可！
