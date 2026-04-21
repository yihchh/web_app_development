-- 任務管理系統 — SQLite 資料庫建表語法
-- 依據 docs/DB_DESIGN.md

CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,   -- 主鍵，自動遞增
    title      TEXT     NOT NULL,                    -- 任務名稱，不可為空
    is_done    BOOLEAN  NOT NULL DEFAULT 0,          -- 完成狀態：0=未完成, 1=已完成
    created_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))  -- 建立時間
);
