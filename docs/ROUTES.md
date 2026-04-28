# 路由設計文件 — 任務管理系統

> 依據 `docs/PRD.md`、`docs/ARCHITECTURE.md`、`docs/DB_DESIGN.md` 與 `docs/FLOWCHART.md` 撰寫  
> 使用技術：Flask Blueprint + Jinja2 模板

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (重導向) | GET | `/` | — | 重導向至 `/tasks` |
| 任務清單 | GET | `/tasks` | `templates/tasks/index.html` | 顯示任務列表，支援狀態篩選 |
| 建立任務 | POST | `/tasks` | — | 接收新任務表單，存入 DB 後重導向 |
| 切換完成狀態 | POST | `/tasks/<int:id>/toggle` | — | 翻轉任務 `is_done` 狀態後重導向 |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除指定任務後重導向 |

---

## 2. 路由詳細說明

### 2.1 顯示任務清單
- **URL**: `/tasks`
- **方法**: `GET`
- **輸入 (Query String)**:
  - `status`: 篩選條件 (可選，預設 `all`)。有效值：`all`, `pending`, `done`。
- **處理邏輯**:
  - 呼叫 `Task.get_all(status=status)`。
- **輸出**:
  - 渲染 `tasks/index.html`，傳入任務列表及目前篩選狀態。

### 2.2 建立任務
- **URL**: `/tasks`
- **方法**: `POST`
- **輸入 (Form Data)**:
  - `title`: 任務名稱 (必填，不可為空)。
- **處理邏輯**:
  - 驗證 `title` 是否為空。
  - 若有效，呼叫 `Task.create(title=title)`。
  - 若無效，導回首頁並顯示錯誤訊息。
- **輸出**:
  - 成功後重導向至 `url_for('tasks.index')`。

### 2.3 切換任務完成狀態
- **URL**: `/tasks/<int:id>/toggle`
- **方法**: `POST`
- **輸入 (URL 參數)**:
  - `id`: 任務主鍵。
- **處理邏輯**:
  - 呼叫 `Task.toggle(id)`。
- **輸出**:
  - 操作完成後重導向至 `url_for('tasks.index')`。
- **錯誤處理**:
  - 若 ID 不存在，回傳 404。

### 2.4 刪除任務
- **URL**: `/tasks/<int:id>/delete`
- **方法**: `POST`
- **輸入 (URL 參數)**:
  - `id`: 任務主鍵。
- **處理邏輯**:
  - 呼叫 `Task.delete(id)`。
- **輸出**:
  - 操作完成後重導向至 `url_for('tasks.index')`。
- **錯誤處理**:
  - 若 ID 不存在，回傳 404。

---

## 3. Jinja2 模板清單

| 模板路徑 | 繼承模板 | 說明 |
| :--- | :--- | :--- |
| `templates/base.html` | — | 基礎版型，包含 HTML 骨架、導覽列與靜態資源引用 |
| `templates/tasks/index.html` | `base.html` | 主頁面，包含：新增任務表單、篩選按鈕、任務列表 |

---

## 4. 下一步（建議執行順序）

1. **實作** → 執行 `/implementation` skill，逐步建立 `app/__init__.py`、`app.py`、路由實作與 HTML 模板。
