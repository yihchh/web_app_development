from app import create_app, db
from app.models import Task

app = create_app()

with app.app_context():
    # 建立所有資料表
    db.create_all()
    print("資料庫初始化成功！")
