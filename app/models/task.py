from app import db
from datetime import datetime


class Task(db.Model):
    """
    Task 資料表的 SQLAlchemy ORM 模型。

    欄位：
        id         -- 主鍵，自動遞增
        title      -- 任務名稱（必填）
        is_done    -- 完成狀態（預設 False）
        created_at -- 建立時間（自動填入）
    """

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        status = "✅" if self.is_done else "⬜"
        return f"<Task {self.id} {status} {self.title}>"

    # ──────────────────────────────────────────────
    # CRUD 方法
    # ──────────────────────────────────────────────

    @classmethod
    def create(cls, title: str) -> "Task":
        """新增一筆任務並寫入資料庫。

        Args:
            title: 任務名稱（不可為空字串）

        Returns:
            新建立的 Task 物件
        """
        task = cls(title=title.strip())
        db.session.add(task)
        db.session.commit()
        return task

    @classmethod
    def get_all(cls, status: str = "all") -> list["Task"]:
        """取得任務清單，可依完成狀態篩選，並以建立時間由新到舊排序。

        Args:
            status: 篩選條件，可傳入 "all"（全部）、"pending"（未完成）、"done"（已完成）

        Returns:
            符合條件的 Task 物件列表
        """
        query = cls.query

        if status == "pending":
            query = query.filter_by(is_done=False)
        elif status == "done":
            query = query.filter_by(is_done=True)

        return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, task_id: int) -> "Task":
        """依 id 取得單筆任務；若不存在則回傳 404。

        Args:
            task_id: 任務的主鍵 id

        Returns:
            對應的 Task 物件
        """
        return cls.query.get_or_404(task_id)

    @classmethod
    def toggle(cls, task_id: int) -> "Task":
        """切換指定任務的完成狀態（True ↔ False）。

        Args:
            task_id: 要切換的任務 id

        Returns:
            更新後的 Task 物件
        """
        task = cls.get_by_id(task_id)
        task.is_done = not task.is_done
        db.session.commit()
        return task

    @classmethod
    def delete(cls, task_id: int) -> None:
        """刪除指定任務。

        Args:
            task_id: 要刪除的任務 id
        """
        task = cls.get_by_id(task_id)
        db.session.delete(task)
        db.session.commit()
