# models.py
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float  # 改为 Float
from sqlalchemy.sql import func
from database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50, collation='utf8mb4_unicode_ci'))
    description = Column(String(100, collation='utf8mb4_unicode_ci'))

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100, collation='utf8mb4_unicode_ci'))
    user_meta = Column(String(200, collation='utf8mb4_unicode_ci'))
    content = Column(Text(collation='utf8mb4_unicode_ci'))
    tags = Column(JSON)
    comments = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class HotTopic(Base):
    __tablename__ = "hot_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255, collation='utf8mb4_unicode_ci'))
    tag = Column(String(50, collation='utf8mb4_unicode_ci'))
    sort_order = Column(Integer)

class HomeCard(Base):
    __tablename__ = "home_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    subtitle = Column(String(255))
    image = Column(String(500))
    badge = Column(String(50))
    tags = Column(JSON)
    participants = Column(String(50))
    rating = Column(Float)  # 改为 Float
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 在 models.py 中添加
class RecommendCard(Base):
    __tablename__ = "recommend_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50))
    title = Column(String(255))
    subtitle = Column(String(255))
    image = Column(String(500))
    tags = Column(JSON)
    participants = Column(String(50))
    rating = Column(Float)
    badge = Column(String(50))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())