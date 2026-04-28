import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # 建立與設定 Flask 實例
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'database.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 載入實例設定 (如果有的話)
        app.config.from_pyfile("config.py", silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保實例資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    db.init_app(app)

    # 註冊 Blueprints
    from app.routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
