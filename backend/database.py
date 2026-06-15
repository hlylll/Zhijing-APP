from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接配置 - 把"你的密码"替换成实际的MySQL密码
# 修改这里：在连接URL中添加 charset=utf8mb4 和 use_unicode=True
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost/help_square?charset=utf8mb4&use_unicode=1"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # 添加连接检查
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True
    }
)
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()