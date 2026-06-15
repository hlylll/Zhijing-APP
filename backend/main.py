# main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
import jwt
import uvicorn
from typing import Optional, List
import os
from sqlalchemy.orm import Session
from database import get_db
import models
from fastapi.responses import JSONResponse
import json
from sqlalchemy import text, Numeric
# 导入情绪识别模块
from emotion_model.predict import predict_mood
import pymysql
import pymysql.cursors
import mysql.connector
from mysql.connector import pooling

# 数据库配置 - mood数据库
mood_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'mood',
    'charset': 'utf8mb4'
}

# 数据库配置 - user数据库
user_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'user',
    'charset': 'utf8mb4'
}

# 创建mood数据库连接池
mood_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mood_pool",
    pool_size=5,
    **mood_db_config
)

# 创建user数据库连接池
user_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="user_pool",
    pool_size=5,
    **user_db_config
)

# 获取mood数据库连接（用于情绪日记）
def get_db_connection_mood():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='mood',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 获取user数据库连接（用于用户信息、路径等）
def get_db_connection_user():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='user',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

app = FastAPI(title="知径 - 后端API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 全局内存存储：{phone: {"code": str, "expire_at": datetime, "last_send": datetime}}
verification_store = {}

SECRET_KEY = "zijing-secret-key-20260116-change-this-in-production"

# ============ 请求模型定义 ============
class PhoneRequest(BaseModel):
    phone: str

class CodeLoginRequest(BaseModel):
    phone: str
    code: str

class MoodAnalysisRequest(BaseModel):
    text: str
    behavior: dict

class MoodDiaryRequest(BaseModel):
    user_id: str
    date: str
    diary_text: str
    manual_mood: int
    predicted_mood: Optional[int] = None
    is_treehole: bool = False
    analysis_result: Optional[dict] = None
    behavior_data: Optional[dict] = None

class UserProfile(BaseModel):
    nickname: str
    major: str
    grade: str
    plan_type: str
    target_career: str
    bio: Optional[str] = ""
    preferred_city: Optional[str] = ""
    skills: Optional[str] = ""
    avatar: Optional[str] = ""
    interest_tags: Optional[List[int]] = []

class PathRequest(BaseModel):
    user_id: int
    plan_type: Optional[str] = None

class TaskCompleteRequest(BaseModel):
    user_id: int
    task_id: int
    path_id: int

class PathSelectRequest(BaseModel):
    user_id: int
    path_id: int

# ============ 工具函数 ============
def generate_code() -> str:
    """生成6位数字验证码"""
    return ''.join(random.choices('0123456789', k=6))

# ============ 登录相关接口 ============
@app.post("/api/send-code")
def send_code(req: PhoneRequest):
    phone = req.phone.strip()
    
    if len(phone) != 11 or not phone.isdigit() or not phone.startswith(('13','14','15','17','18','19')):
        raise HTTPException(status_code=400, detail="请输入正确的11位中国大陆手机号")

    now = datetime.utcnow()

    # 限频：60秒内只能发送一次
    if phone in verification_store:
        last_send = verification_store[phone].get("last_send")
        if last_send and (now - last_send) < timedelta(seconds=60):
            raise HTTPException(status_code=429, detail="发送太频繁，请60秒后再试")

    code = generate_code()
    expire_at = now + timedelta(minutes=5)

    # 存入内存
    verification_store[phone] = {
        "code": code,
        "expire_at": expire_at,
        "last_send": now
    }

    print(f"\n【模拟短信】手机号 {phone} 验证码：{code} （有效至 {expire_at.strftime('%Y-%m-%d %H:%M:%S UTC')}）\n")

    return {
        "success": True,
        "message": "验证码已发送（这是模拟模式）",
        "debug_code": code
    }

@app.post("/api/login/code")
def login_code(req: CodeLoginRequest):
    phone = req.phone.strip()
    input_code = req.code.strip()

    if phone not in verification_store:
        raise HTTPException(status_code=400, detail="验证码不存在或已过期，请重新获取")

    stored = verification_store[phone]
    now = datetime.utcnow()

    # 检查是否过期
    if now > stored["expire_at"]:
        del verification_store[phone]
        raise HTTPException(status_code=400, detail="验证码已过期")

    # 校验验证码
    if stored["code"] != input_code:
        raise HTTPException(status_code=400, detail="验证码错误")

    # 模拟用户数据
    user = {
        "id": 10001,
        "phone": phone,
        "nickname": "知径新用户",
        "created_at": now.isoformat()
    }

    # 生成 JWT token
    payload = {
        "user_id": user["id"],
        "phone": user["phone"],
        "exp": int((now + timedelta(days=7)).timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # 用完即删
    del verification_store[phone]

    return {
        "success": True,
        "token": token,
        "user": user
    }

# ============ 首页卡片接口 ============
@app.get("/api/home-cards")
def get_home_cards(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM home_cards"))
        rows = result.fetchall()
        print(f"原生SQL查询到 {len(rows)} 条记录")
        
        cards_list = []
        for row in rows:
            row_dict = dict(row._mapping)
            
            # 处理 tags 字段
            tags = row_dict.get('tags')
            if tags and isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except:
                    tags = []
            
            cards_list.append({
                "id": row_dict.get('id'),
                "title": row_dict.get('title'),
                "subtitle": row_dict.get('subtitle'),
                "image": row_dict.get('image'),
                "badge": row_dict.get('badge'),
                "tags": tags if tags else [],
                "participants": row_dict.get('participants'),
                "rating": float(row_dict.get('rating')) if row_dict.get('rating') else 0,
                "sort_order": row_dict.get('sort_order')
            })
        
        return JSONResponse(content=cards_list, media_type="application/json; charset=utf-8")
        
    except Exception as e:
        print(f"错误详情: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"detail": str(e)}, status_code=500)

# ============ 推荐卡片接口 ============
@app.get("/api/recommend-cards")
def get_recommend_cards(category: str = None, db: Session = Depends(get_db)):
    try:
        # 构建查询
        query = db.query(models.RecommendCard)
        
        # 如果指定了分类且不是"全部"，则按分类筛选
        if category and category != "全部":
            query = query.filter(models.RecommendCard.category == category)
        
        # 按 sort_order 排序
        cards = query.order_by(models.RecommendCard.sort_order).all()
        print(f"查询到 {len(cards)} 条推荐卡片")
        
        cards_list = []
        for card in cards:
            # 处理 tags 字段
            tags = card.tags
            if tags and isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except:
                    tags = []
            
            cards_list.append({
                "id": card.id,
                "category": card.category,
                "title": card.title,
                "subtitle": card.subtitle,
                "image": card.image,
                "tags": tags if tags else [],
                "participants": card.participants,
                "rating": float(card.rating) if card.rating else 0,
                "badge": card.badge or "",
                "sort_order": card.sort_order
            })
        
        return JSONResponse(
            content=cards_list,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        print(f"获取推荐卡片出错：{str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"detail": str(e)},
            status_code=500,
            media_type="application/json; charset=utf-8"
        )

# 获取所有分类
@app.get("/api/recommend-categories")
def get_recommend_categories(db: Session = Depends(get_db)):
    try:
        # 查询所有不重复的分类
        result = db.execute(text("SELECT DISTINCT category FROM recommend_cards ORDER BY category"))
        categories = ['全部']
        for row in result:
            categories.append(row[0])
        
        return JSONResponse(content=categories)
    except Exception as e:
        print(f"获取分类出错：{str(e)}")
        return JSONResponse(content={"detail": str(e)}, status_code=500)

# ============ 情绪识别接口 ============
@app.post("/api/analyze-mood")
async def analyze_mood(request: MoodAnalysisRequest):
    try:
        result = predict_mood(request.text, request.behavior)
        if isinstance(result, dict) and 'success' in result:
            return result
        else:
            return {
                "success": True,
                **result
            }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "model_not_found",
            "message": "情绪模型正在训练中，请稍后再试"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ============ 广场相关接口 ============
@app.get("/api/hot-topics")
def get_hot_topics(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM hot_topics ORDER BY sort_order"))
        topics = []
        for row in result:
            topics.append({
                "id": row[0],
                "content": row[1],
                "tag": row[2] if row[2] else "",
                "sort_order": row[3]
            })
        
        return JSONResponse(
            content=topics,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        print(f"查询热议榜出错: {str(e)}")
        return JSONResponse(
            content={"detail": str(e)},
            status_code=500,
            media_type="application/json; charset=utf-8"
        )

@app.get("/api/posts")
def get_posts(category: str = None, db: Session = Depends(get_db)):
    try:
        sql = """
            SELECT p.*, c.name as category_name 
            FROM posts p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE 1=1
        """
        params = {}
        
        if category and category != "推荐":
            sql += " AND c.name = :category"
            params["category"] = category
        
        sql += " ORDER BY p.created_at DESC LIMIT 20"
        
        result = db.execute(text(sql), params)
        
        posts = []
        for row in result:
            row_dict = dict(row._mapping)
            
            tags = row_dict.get('tags')
            if tags:
                try:
                    if isinstance(tags, str):
                        tags = json.loads(tags)
                except:
                    tags = []
            else:
                tags = []
            
            posts.append({
                "id": row_dict.get('id'),
                "user_name": row_dict.get('user_name'),
                "user_meta": row_dict.get('user_meta'),
                "content": row_dict.get('content'),
                "tags": tags,
                "comments": row_dict.get('comments', 0),
                "likes": row_dict.get('likes', 0),
                "category_id": row_dict.get('category_id'),
                "created_at": str(row_dict.get('created_at')) if row_dict.get('created_at') else None
            })
        
        return JSONResponse(
            content=posts,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        print(f"查询帖子出错: {str(e)}")
        return JSONResponse(
            content={"detail": str(e)},
            status_code=500,
            media_type="application/json; charset=utf-8"
        )

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

# ============ 日记相关接口 ============
@app.post("/api/save-diary")
async def save_diary(request: dict):
    conn = None
    cursor = None
    try:
        print("收到保存日记请求:", request)
        
        conn = get_db_connection_mood()
        cursor = conn.cursor()
        
        user_id = request.get('user_id')
        date_str = request.get('date')
        diary_text = request.get('diary_text')
        manual_mood = request.get('manual_mood')
        predicted_mood = request.get('predicted_mood')
        is_treehole = request.get('is_treehole', False)
        analysis_result = request.get('analysis_result')
        behavior_data = request.get('behavior_data')
        
        if not all([user_id, date_str, diary_text, manual_mood]):
            return {"success": False, "error": "缺少必填字段"}
        
        if 'T' in date_str:
            date_str = date_str.split('.')[0]
            date_str = date_str.replace('T', ' ')
            if date_str.endswith('Z'):
                date_str = date_str[:-1]
        
        is_treehole_int = 1 if is_treehole else 0
        
        analysis_json = json.dumps(analysis_result, ensure_ascii=False) if analysis_result else None
        behavior_json = json.dumps(behavior_data, ensure_ascii=False) if behavior_data else None
        
        sql = """INSERT INTO mood_diaries 
                 (user_id, date, diary_text, manual_mood, predicted_mood, 
                  is_treehole, analysis_result, behavior_data) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (
            user_id, date_str, diary_text, manual_mood, 
            predicted_mood, is_treehole_int, analysis_json, behavior_json
        ))
        conn.commit()
        
        return {"success": True, "id": cursor.lastrowid}
        
    except Exception as e:
        print(f"保存日记错误: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/api/garden-data/{user_id}")
async def get_garden_data(user_id: str, year: int = None, month: int = None):
    conn = None
    cursor = None
    try:
        conn = get_db_connection_mood()
        cursor = conn.cursor()
        
        if year and month:
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"
            
            sql = """SELECT * FROM mood_diaries 
                     WHERE user_id = %s AND date >= %s AND date < %s
                     ORDER BY date DESC"""
            cursor.execute(sql, (user_id, start_date, end_date))
        else:
            sql = "SELECT * FROM mood_diaries WHERE user_id = %s ORDER BY date DESC"
            cursor.execute(sql, (user_id,))
        
        diaries = cursor.fetchall()
        
        stats = {
            "total": len(diaries),
            "byMood": {},
            "byMonth": {}
        }
        
        flowers = []
        for diary in diaries:
            mood = diary['predicted_mood'] or diary['manual_mood']
            if mood:
                stats["byMood"][mood] = stats["byMood"].get(mood, 0) + 1
            
            month_key = diary['date'].strftime('%Y-%m') if hasattr(diary['date'], 'strftime') else str(diary['date'])[:7]
            stats["byMonth"][month_key] = stats["byMonth"].get(month_key, 0) + 1
            
            analysis = None
            if diary['analysis_result']:
                try:
                    analysis = json.loads(diary['analysis_result'])
                except:
                    analysis = None
            
            flowers.append({
                "date": diary['date'].isoformat() if hasattr(diary['date'], 'isoformat') else str(diary['date']),
                "text": diary['diary_text'],
                "moodId": mood,
                "growth": 0.7,
                "analysis": analysis
            })
        
        streak_days = calculate_streak(diaries)
        
        return {
            "success": True,
            "flowers": flowers,
            "stats": stats,
            "streakDays": streak_days,
            "growthLevel": max(1, len(diaries) // 10 + 1)
        }
        
    except Exception as e:
        print(f"获取花园数据错误: {e}")
        return {
            "success": False, 
            "error": str(e),
            "flowers": [],
            "stats": {"total": 0, "byMood": {}, "byMonth": {}},
            "streakDays": 0,
            "growthLevel": 1
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def calculate_streak(diaries):
    if not diaries or len(diaries) == 0:
        return 0
    
    dates = []
    for d in diaries:
        if isinstance(d['date'], str):
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(d['date'].replace('Z', '+00:00')).date()
            except:
                date_obj = datetime.now().date()
        else:
            date_obj = d['date'].date() if hasattr(d['date'], 'date') else datetime.now().date()
        dates.append(date_obj)
    
    dates = sorted(dates, reverse=True)
    
    streak = 1
    from datetime import timedelta
    
    for i in range(len(dates) - 1):
        if dates[i] - timedelta(days=1) == dates[i + 1]:
            streak += 1
        else:
            break
    
    return streak

# ============ 用户信息接口 ============
TEST_USER_ID = 1  # 测试用户ID

@app.post("/user/profile")
async def get_user_profile():
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 检查用户是否存在
        cursor.execute("SELECT * FROM users WHERE id = %s", (TEST_USER_ID,))
        user = cursor.fetchone()
        
        if not user:
            # 创建默认用户
            cursor.execute("""
                INSERT INTO users (id, nickname, created_at) 
                VALUES (%s, %s, NOW())
            """, (TEST_USER_ID, f'用户{TEST_USER_ID}'))
            connection.commit()
            
            cursor.execute("SELECT * FROM users WHERE id = %s", (TEST_USER_ID,))
            user = cursor.fetchone()
        
        # 查询用户标签
        cursor.execute("SELECT tag_id FROM user_tags WHERE user_id = %s", (TEST_USER_ID,))
        tags = cursor.fetchall()
        interest_tags = [tag['tag_id'] for tag in tags] if tags else []
        
        # 处理skills字段
        skills_list = []
        if user and user.get('skills'):
            skills_list = user['skills'].split(',') if user['skills'] else []
        
        return {
            "code": 200,
            "data": {
                "avatar": user.get('avatar', '') if user else '',
                "nickname": user.get('nickname', '') if user else '',
                "major": user.get('major', '') if user else '',
                "grade": user.get('grade', '') if user else '',
                "plan_type": user.get('plan_type', 'job') if user else 'job',
                "target_career": user.get('target_career', '') if user else '',
                "bio": user.get('bio', '') if user else '',
                "preferred_city": user.get('preferred_city', '') if user else '',
                "skills": skills_list,
                "interest_tags": interest_tags,
                "is_first_edit": user.get('is_first_edit', 1) == 1 if user else True
            }
        }
        
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        import traceback
        traceback.print_exc()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.put("/user/profile")
async def update_user_profile(profile: UserProfile):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 获取修改前的数据
        cursor.execute("SELECT * FROM users WHERE id = %s", (TEST_USER_ID,))
        old_user_data = cursor.fetchone()
        
        # 获取修改前的标签
        cursor.execute("SELECT tag_id FROM user_tags WHERE user_id = %s", (TEST_USER_ID,))
        old_tags = cursor.fetchall()
        old_tags_list = [tag['tag_id'] for tag in old_tags] if old_tags else []
        
        # 保存历史记录
        if old_user_data:
            old_skills_str = old_user_data.get('skills', '')
            old_tags_str = ','.join(str(tag) for tag in old_tags_list) if old_tags_list else ''
            
            history_sql = """
            INSERT INTO user_profile_history (
                user_id, nickname, major, grade, plan_type, target_career,
                bio, preferred_city, skills, avatar, interest_tags, operation_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(history_sql, (
                TEST_USER_ID,
                old_user_data.get('nickname', ''),
                old_user_data.get('major', ''),
                old_user_data.get('grade', ''),
                old_user_data.get('plan_type', ''),
                old_user_data.get('target_career', ''),
                old_user_data.get('bio', ''),
                old_user_data.get('preferred_city', ''),
                old_skills_str,
                old_user_data.get('avatar', ''),
                old_tags_str,
                'UPDATE'
            ))
        
        # 处理新skills
        skills_str = ''
        if profile.skills:
            if isinstance(profile.skills, list):
                skills_str = ','.join(profile.skills)
            else:
                skills_str = profile.skills
        
        # 更新用户基本信息
        update_sql = """
        UPDATE users 
        SET nickname = %s, major = %s, grade = %s, 
            plan_type = %s, target_career = %s,
            bio = %s, preferred_city = %s, skills = %s,
            avatar = %s, is_first_edit = 0,
            updated_at = NOW()
        WHERE id = %s
        """
        
        cursor.execute(update_sql, (
            profile.nickname,
            profile.major,
            profile.grade,
            profile.plan_type,
            profile.target_career,
            profile.bio,
            profile.preferred_city,
            skills_str,
            profile.avatar,
            TEST_USER_ID
        ))
        
        # 更新标签
        if profile.interest_tags is not None:
            cursor.execute("DELETE FROM user_tags WHERE user_id = %s", (TEST_USER_ID,))
            
            if profile.interest_tags:
                # 检查哪些标签存在
                placeholders = ','.join(['%s'] * len(profile.interest_tags))
                cursor.execute(f"SELECT id FROM tags WHERE id IN ({placeholders})", 
                             profile.interest_tags)
                existing_tags = cursor.fetchall()
                existing_ids = [tag['id'] for tag in existing_tags]
                
                for tag_id in existing_ids:
                    cursor.execute(
                        "INSERT INTO user_tags (user_id, tag_id) VALUES (%s, %s)",
                        (TEST_USER_ID, tag_id)
                    )
        
        connection.commit()
        
        return {
            "code": 200,
            "message": "更新成功",
            "data": {"success": True}
        }
        
    except Exception as e:
        print(f"更新用户信息失败: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 路径推荐接口 ============
@app.post("/api/recommend-paths")
async def recommend_paths(request: PathRequest):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 根据规划类型获取路径
        if request.plan_type:
            cursor.execute("""
                SELECT * FROM paths 
                WHERE plan_type = %s 
                ORDER BY difficulty
            """, (request.plan_type,))
        else:
            cursor.execute("SELECT * FROM paths ORDER BY difficulty")
        
        paths = cursor.fetchall()
        
        return {
            "code": 200,
            "data": paths
        }
        
    except Exception as e:
        print(f"获取路径失败: {e}")
        import traceback
        traceback.print_exc()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 获取路径详情（包含任务） ============
@app.get("/api/path/{path_id}")
async def get_path_detail(path_id: int, user_id: int = 1):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 1. 获取路径信息
        cursor.execute("SELECT * FROM paths WHERE id = %s", (path_id,))
        path = cursor.fetchone()
        
        if not path:
            return {"code": 404, "message": "路径不存在"}
        
        # 2. 获取该路径下的任务 - 添加 WHERE 条件限制 path_id
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE path_id = %s 
            ORDER BY sort_order
        """, (path_id,))
        tasks = cursor.fetchall()
        
        print(f"路径 {path_id} 的任务数量: {len(tasks)}")  # 添加调试
        
        # 3. 获取用户在该路径上的完成情况
        cursor.execute("""
            SELECT task_id FROM user_task_completions 
            WHERE user_id = %s AND path_id = %s
        """, (user_id, path_id))
        completed_tasks = [row['task_id'] for row in cursor.fetchall()]
        
        # 4. 获取用户当前进度
        cursor.execute("""
            SELECT current_task_id, progress FROM user_paths 
            WHERE user_id = %s AND path_id = %s
        """, (user_id, path_id))
        user_path = cursor.fetchone()
        
        # 5. 处理任务列表
        task_list = []
        for i, task in enumerate(tasks):
            is_completed = task['id'] in completed_tasks
            is_current = False
            
            if user_path:
                is_current = task['id'] == user_path['current_task_id']
            else:
                # 如果还没选择路径，第一个未完成的任务作为当前任务
                is_current = (i == 0 and not is_completed)
            
            task_list.append({
                "id": task['id'],
                "title": task['title'],
                "description": task['description'],
                "type": task['type'],
                "difficulty": task['difficulty'],
                "estimated_days": task['estimated_days'],
                "completed": is_completed,
                "current": is_current
            })
        
        return {
            "code": 200,
            "data": {
                "path": path,
                "tasks": task_list,
                "progress": user_path['progress'] if user_path else 0
            }
        }
        
    except Exception as e:
        print(f"获取路径详情失败: {e}")
        import traceback
        traceback.print_exc()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 用户选择路径 ============
@app.post("/api/user/select-path")
async def select_path(request: PathSelectRequest):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 检查是否已选择
        cursor.execute("""
            SELECT id FROM user_paths 
            WHERE user_id = %s AND path_id = %s
        """, (request.user_id, request.path_id))
        existing = cursor.fetchone()
        
        if existing:
            return {"code": 200, "message": "已选择该路径"}
        
        # 获取路径的第一个任务
        cursor.execute("""
            SELECT id FROM tasks 
            WHERE path_id = %s 
            ORDER BY sort_order LIMIT 1
        """, (request.path_id,))
        first_task = cursor.fetchone()
        
        # 插入用户路径记录
        cursor.execute("""
            INSERT INTO user_paths (user_id, path_id, current_task_id, progress, status)
            VALUES (%s, %s, %s, 0, 'in_progress')
        """, (request.user_id, request.path_id, first_task['id'] if first_task else None))
        
        connection.commit()
        
        return {"code": 200, "message": "路径选择成功"}
        
    except Exception as e:
        print(f"选择路径失败: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 完成任务 ============
@app.post("/api/user/complete-task")
async def complete_task(request: TaskCompleteRequest):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 记录完成任务
        cursor.execute("""
            INSERT INTO user_task_completions (user_id, task_id, path_id)
            VALUES (%s, %s, %s)
        """, (request.user_id, request.task_id, request.path_id))
        
        # 获取下一个任务
        cursor.execute("""
            SELECT id FROM tasks 
            WHERE path_id = %s AND sort_order > (
                SELECT sort_order FROM tasks WHERE id = %s
            )
            ORDER BY sort_order LIMIT 1
        """, (request.path_id, request.task_id))
        next_task = cursor.fetchone()
        
        # 获取总任务数
        cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE path_id = %s", (request.path_id,))
        total_tasks = cursor.fetchone()['total']
        
        # 获取已完成任务数
        cursor.execute("""
            SELECT COUNT(*) as completed FROM user_task_completions 
            WHERE user_id = %s AND path_id = %s
        """, (request.user_id, request.path_id))
        completed_count = cursor.fetchone()['completed']
        
        # 计算进度
        progress = int((completed_count / total_tasks) * 100)
        
        # 更新用户路径
        if next_task:
            cursor.execute("""
                UPDATE user_paths 
                SET current_task_id = %s, progress = %s
                WHERE user_id = %s AND path_id = %s
            """, (next_task['id'], progress, request.user_id, request.path_id))
        else:
            # 所有任务完成
            cursor.execute("""
                UPDATE user_paths 
                SET status = 'completed', progress = 100, completed_at = NOW()
                WHERE user_id = %s AND path_id = %s
            """, (request.user_id, request.path_id))
        
        connection.commit()
        
        return {
            "code": 200,
            "message": "任务完成",
            "data": {
                "progress": progress,
                "has_next": bool(next_task)
            }
        }
        
    except Exception as e:
        print(f"完成任务失败: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 获取用户当前路径 ============
@app.get("/api/user/current-path/{user_id}")
async def get_user_current_path(user_id: int):
    connection = None
    cursor = None
    try:
        connection = get_db_connection_user()
        cursor = connection.cursor()
        
        # 获取用户当前进行的路径
        cursor.execute("""
            SELECT up.*, p.name, p.description, p.plan_type 
            FROM user_paths up
            JOIN paths p ON up.path_id = p.id
            WHERE up.user_id = %s AND up.status = 'in_progress'
            ORDER BY up.started_at DESC
            LIMIT 1
        """, (user_id,))
        
        current_path = cursor.fetchone()
        
        return {
            "code": 200,
            "data": current_path
        }
        
    except Exception as e:
        print(f"获取用户当前路径失败: {e}")
        import traceback
        traceback.print_exc()
        return {"code": 500, "message": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ============ 测试接口 ============
@app.get("/test")
async def test():
    return {"message": "API is working"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ============ 启动入口 ============
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )