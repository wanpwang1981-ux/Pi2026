# Lesson 2

本專案使用 [uv](https://docs.astral.sh/uv/) 管理 Python 環境與套件，並透過 `.env` 檔案管理敏感設定。

---

## 1. 設定 .env 檔案

在專案根目錄建立 `.env` 檔案，填入所需的環境變數：

```env
GEMINI_API_KEY=你的_API_金鑰
```

> 注意：`.env` 已加入 `.gitignore`，請勿將真實金鑰提交至版本控制。

---

## 2. 安裝 uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows（PowerShell）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝完成後確認版本：

```bash
uv --version
```

---

## 3. 使用 uv 建立虛擬環境（venv）

```bash
# 在專案目錄下建立 .venv（自動使用 .python-version 指定的版本）
uv venv

# 或指定 Python 版本
uv venv --python 3.13
```

啟動虛擬環境：

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

## 4. 初始化新專案

如果是從零開始建立新專案，使用 `uv init`：

```bash
# 在當前目錄初始化
uv init

# 或建立新資料夾並初始化
uv init 專案名稱
```

這會自動產生 `pyproject.toml`、`main.py`、`.python-version` 與 `.gitignore`。

---

## 5. 安裝專案依賴

```bash
# 依照 pyproject.toml 安裝所有依賴
uv sync
```

---

## 6. uv 常用指令

| 指令 | 說明 |
|------|------|
| `uv init` | 初始化新專案，產生 pyproject.toml 等基本檔案 |
| `uv venv` | 建立虛擬環境 |
| `uv sync` | 安裝 pyproject.toml 中的所有依賴 |
| `uv add <套件>` | 新增套件並更新 pyproject.toml |
| `uv remove <套件>` | 移除套件 |
| `uv run <script.py>` | 在虛擬環境中執行 Python 腳本 |
| `uv pip list` | 列出已安裝的套件 |
| `uv lock` | 重新產生 uv.lock 鎖定檔 |
| `uv python list` | 列出可用的 Python 版本 |
| `uv python install 3.13` | 安裝指定的 Python 版本 |

---

## 7. 執行專案

```bash
uv run main.py
```
