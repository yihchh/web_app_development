# 流程圖文件 — 任務管理系統

> 依據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md` 撰寫

---

## 1. 使用者流程圖（User Flow）

描述使用者從開啟網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🙋 使用者開啟網頁]) --> Home[首頁\n顯示所有任務清單]

    Home --> Filter{要篩選清單嗎？}
    Filter -->|點選「全部」| Home
    Filter -->|點選「未完成」| ShowPending[顯示未完成任務]
    Filter -->|點選「已完成」| ShowDone[顯示已完成任務]
    ShowPending --> Home
    ShowDone --> Home

    Home --> Action{要執行什麼操作？}

    Action -->|新增任務| InputForm[在輸入框填寫任務名稱]
    InputForm --> Submit{送出表單}
    Submit -->|名稱為空| ErrorMsg[⚠️ 提示：請輸入任務名稱]
    ErrorMsg --> InputForm
    Submit -->|名稱有效| AddSuccess[✅ 任務新增成功\n回到首頁，清單更新]
    AddSuccess --> Home

    Action -->|標註完成狀態| ToggleStatus[點選任務旁的\n完成 / 未完成按鈕]
    ToggleStatus --> ToggleSuccess[🔄 狀態切換成功\n回到首頁，清單更新]
    ToggleSuccess --> Home

    Action -->|刪除任務| ConfirmDelete{確認刪除？}
    ConfirmDelete -->|取消| Home
    ConfirmDelete -->|確認| DeleteSuccess[🗑️ 任務刪除成功\n回到首頁，清單更新]
    DeleteSuccess --> Home
```

---

## 2. 系統序列圖（System Sequence Diagrams）

描述使用者操作觸發後，系統各元件之間的資料傳遞順序。

### 2.1 查看任務清單（含篩選）

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as Flask Route\n(tasks.py)
    participant Model as Model\n(task.py)
    participant DB as 💾 SQLite

    User->>Browser: 開啟網頁 / 點選篩選按鈕
    Browser->>Flask: GET /tasks?status=all|pending|done
    Flask->>Model: 呼叫 get_tasks(status)
    Model->>DB: SELECT * FROM tasks\n[WHERE is_done = ?]
    DB-->>Model: 回傳任務列表
    Model-->>Flask: Task 物件列表
    Flask-->>Browser: render_template("tasks/index.html", tasks=...)
    Browser-->>User: 顯示任務清單頁面
```

---

### 2.2 新增任務

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as Flask Route\n(tasks.py)
    participant Model as Model\n(task.py)
    participant DB as 💾 SQLite

    User->>Browser: 填寫任務名稱，點選「新增」
    Browser->>Flask: POST /tasks\n(body: title=任務名稱)
    Flask->>Flask: 驗證表單（title 不可為空）

    alt 驗證失敗
        Flask-->>Browser: render_template（顯示錯誤訊息）
        Browser-->>User: ⚠️ 提示輸入錯誤
    else 驗證通過
        Flask->>Model: 呼叫 create_task(title)
        Model->>DB: INSERT INTO tasks\n(title, is_done=False, created_at=now)
        DB-->>Model: 新增成功
        Model-->>Flask: 回傳新 Task 物件
        Flask-->>Browser: redirect(GET /tasks)
        Browser->>Flask: GET /tasks
        Flask-->>Browser: 任務清單頁面（含新增的任務）
        Browser-->>User: ✅ 顯示更新後的清單
    end
```

---

### 2.3 切換任務完成狀態

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as Flask Route\n(tasks.py)
    participant Model as Model\n(task.py)
    participant DB as 💾 SQLite

    User->>Browser: 點選任務旁的狀態按鈕
    Browser->>Flask: POST /tasks/<id>/toggle
    Flask->>Model: 呼叫 toggle_task(id)
    Model->>DB: SELECT is_done FROM tasks WHERE id=?
    DB-->>Model: 目前狀態（True / False）
    Model->>DB: UPDATE tasks SET is_done=NOT is_done\nWHERE id=?
    DB-->>Model: 更新成功
    Model-->>Flask: 回傳更新後的 Task
    Flask-->>Browser: redirect(GET /tasks)
    Browser->>Flask: GET /tasks
    Flask-->>Browser: 任務清單頁面（狀態已切換）
    Browser-->>User: 🔄 顯示更新後的清單
```

---

### 2.4 刪除任務

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Flask as Flask Route\n(tasks.py)
    participant Model as Model\n(task.py)
    participant DB as 💾 SQLite

    User->>Browser: 點選「刪除」按鈕
    Browser->>Flask: POST /tasks/<id>/delete
    Flask->>Model: 呼叫 delete_task(id)
    Model->>DB: DELETE FROM tasks WHERE id=?
    DB-->>Model: 刪除成功
    Model-->>Flask: 操作完成
    Flask-->>Browser: redirect(GET /tasks)
    Browser->>Flask: GET /tasks
    Flask-->>Browser: 任務清單頁面（已移除該任務）
    Browser-->>User: 🗑️ 顯示更新後的清單
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | Controller 動作 | 說明 |
|------|---------|----------|----------------|------|
| 顯示所有任務 | `/tasks` | `GET` | `index()` | 取得所有任務並渲染清單頁面 |
| 依狀態篩選 | `/tasks?status=pending` | `GET` | `index()` | 加上 `status` 查詢參數進行篩選 |
| 新增任務 | `/tasks` | `POST` | `create()` | 接收表單資料，寫入資料庫後重導向 |
| 切換完成狀態 | `/tasks/<id>/toggle` | `POST` | `toggle()` | 翻轉指定任務的 `is_done` 欄位 |
| 刪除任務 | `/tasks/<id>/delete` | `POST` | `delete()` | 從資料庫中移除指定任務 |

> 📌 **說明**：因為 HTML 表單僅支援 `GET` 與 `POST`，修改與刪除操作統一使用 `POST` 方法，不使用 `PUT` / `DELETE`。

---

## 4. 下一步（建議執行順序）

1. **資料庫設計** → 執行 `/db-design` skill，定義 `tasks` 資料表欄位與 Schema
2. **API / 路由設計** → 執行 `/api-design` skill，根據上方功能對照表展開完整路由規格
3. **實作** → 執行 `/implementation` skill，逐步建立 Model、Route、Template
