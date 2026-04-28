from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
def root():
    """
    重導向根目錄至任務列表。
    """
    return redirect(url_for("tasks.index"))

@tasks_bp.route("/tasks")
def index():
    """
    顯示任務清單。
    
    Query Parameters:
        status: 篩選狀態 (all, pending, done)
    """
    status = request.args.get("status", "all")
    tasks = Task.get_all(status=status)
    return render_template("tasks/index.html", tasks=tasks, current_status=status)

@tasks_bp.route("/tasks", methods=["POST"])
def create():
    """
    接收表單資料並建立新任務。
    
    Form Data:
        title: 任務名稱
    """
    title = request.form.get("title")
    
    if not title or not title.strip():
        flash("請輸入任務名稱！", "danger")
        return redirect(url_for("tasks.index"))
        
    task = Task.create(title=title)
    if task:
        flash(f"任務「{title}」已新增成功！", "success")
    else:
        flash("新增任務時發生錯誤，請稍後再試。", "danger")
        
    return redirect(url_for("tasks.index"))

@tasks_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id):
    """
    切換指定任務的完成狀態。
    
    Args:
        task_id: 任務 ID
    """
    task = Task.toggle(task_id)
    if task:
        status_text = "已完成" if task.is_done else "未完成"
        flash(f"任務狀態已切換為：{status_text}", "info")
    else:
        flash("找不到該任務或發生錯誤。", "danger")
        
    return redirect(url_for("tasks.index"))

@tasks_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete(task_id):
    """
    刪除指定任務。
    
    Args:
        task_id: 任務 ID
    """
    success = Task.delete(task_id)
    if success:
        flash("任務已成功刪除。", "warning")
    else:
        flash("刪除任務時發生錯誤。", "danger")
        
    return redirect(url_for("tasks.index"))
