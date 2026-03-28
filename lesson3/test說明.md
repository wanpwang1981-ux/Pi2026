# test.py 程式說明

## 概述

這是一個 **Open WebUI Filter（過濾器）** 的範例程式。

Open WebUI 是一個可自架的 AI 聊天介面（類似 ChatGPT），支援透過 Filter 插件在對話流程中插入自訂邏輯。

---

## Filter 是什麼？

Filter 是 Open WebUI 的插件機制之一，會在以下兩個時間點自動被呼叫：

```
使用者輸入訊息
      ↓
  [ inlet ]  ← Filter 在這裡攔截，可驗證或修改請求
      ↓
   AI 模型處理
      ↓
  [ outlet ] ← Filter 在這裡攔截，可修改或記錄回應
      ↓
使用者看到回應
```

---

## 程式結構說明

### 1. `Valves`（管理員設定）

```python
class Valves(BaseModel):
    priority: int = 0       # Filter 執行優先順序
    max_turns: int = 8      # 系統允許的最大對話輪數
```

- 由**系統管理員**在後台設定
- 是整個系統的上限，使用者無法超越

### 2. `UserValves`（使用者設定）

```python
class UserValves(BaseModel):
    max_turns: int = 4      # 使用者自己的對話輪數上限
```

- 由**使用者**自行調整
- 預設值為 4，但不能超過管理員設定的 8

### 3. `__init__`（初始化）

```python
def __init__(self):
    self.valves = self.Valves()
```

- 建立 Valves 實例，載入管理員預設設定
- `self.file_handler = True`（已註解）：若啟用，可讓此 Filter 自行處理上傳檔案

### 4. `inlet`（前處理器）

```python
def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

**執行時機**：使用者送出訊息後、AI 處理前

**主要邏輯**：
1. 取得目前對話的所有訊息（`messages`）
2. 比較使用者設定與管理員設定，取較小值作為上限
3. 若訊息數量超過上限，拋出例外，阻止本次請求繼續

**範例情境**：
- 管理員設定 `max_turns = 8`
- 使用者設定 `max_turns = 4`
- 實際上限 = `min(4, 8)` = **4 輪**
- 第 5 輪開始會收到錯誤訊息

### 5. `outlet`（後處理器）

```python
def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

**執行時機**：AI 產生回應後、顯示給使用者前

**目前行為**：僅印出 log，不修改回應，直接回傳

**可擴充用途**：
- 過濾回應中的敏感詞
- 記錄對話到資料庫
- 在回應後附加額外資訊

---

## 資料流範例

假設使用者已對話 5 輪，且上限為 4：

```
使用者送出第 5 則訊息
      ↓
inlet 被呼叫
  → messages 長度 = 5
  → max_turns = min(4, 8) = 4
  → 5 > 4，拋出例外
      ↓
對話中斷，使用者看到錯誤：
"Conversation turn limit exceeded. Max turns: 4"
```

---

## 依賴套件

| 套件 | 用途 |
|------|------|
| `pydantic` | 定義 Valves / UserValves 資料模型，自動驗證型別 |
| `typing` | 提供 `Optional` 型別標註 |
