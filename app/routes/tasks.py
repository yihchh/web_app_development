from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
def root():
    """
    重導向根目錄至任務列表。
    """
    pass

@tasks_bp.route("/tasks")
def index():
    """
    顯示任務清單。
    
    Query Parameters:
        status: 篩選狀態 (all, pending, done)
    """
    pass

@tasks_bp.route("/tasks", methods=["POST"])
def create():
    """
    接收表單資料並建立新任務。
    
    Form Data:
        title: 任務名稱
    """
    pass

@tasks_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id):
    """
    切換指定任務的完成狀態。
    
    Args:
        task_id: 任務 ID
    """
    pass

@tasks_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete(task_id):
    """
    刪除指定任務。
    
    Args:
        task_id: 任務 ID
    """
    pass
