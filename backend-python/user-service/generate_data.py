#!/usr/bin/env python3
# generate_data.py - 生成测试数据脚本
import pymysql
import random
import bcrypt
import json
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('generate_data')

# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'smart_community',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}

# 生成随机手机号
def generate_phone():
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '170', '171', '172', '173', '175', '176', '177', '178',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices('0123456789', k=8))
    return f"{prefix}{suffix}"

# 生成随机昵称
def generate_nickname():
    adjectives = ['快乐的', '聪明的', '可爱的', '友善的', '活泼的', '温柔的', '勇敢的', '诚实的', '热情的', '幽默的']
    nouns = ['小猫', '小狗', '小兔', '小鸟', '小鱼', '小熊', '小鹿', '小象', '小狮子', '小老虎']
    numbers = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"

# 生成随机密码
def generate_password():
    return '123456'  # 统一密码，方便测试

# 生成随机性别
def generate_gender():
    return random.choice([0, 1, 2])

# 生成随机生日
def generate_birthday():
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2005, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# 生成随机邮箱
def generate_email(phone):
    domains = ['qq.com', '163.com', '126.com', 'gmail.com', 'outlook.com']
    return f"{phone}@{random.choice(domains)}"

# 生成随机单元
def generate_unit(building_id):
    unit_count = 2  # 每栋楼2个单元
    return str(random.randint(1, unit_count))

# 生成随机房号
def generate_room_number():
    floor = random.randint(1, 18)  # 18层
    room = random.randint(1, 4)    # 每层4户
    return f"{floor:02d}{room:02d}"

# 生成随机兴趣标签
def generate_interest_tags():
    tags = ['运动', '阅读', '音乐', '旅行', '美食', '电影', '摄影', '健身', '绘画', '编程']
    selected_tags = random.sample(tags, random.randint(1, 5))
    return json.dumps(selected_tags, ensure_ascii=False)

# 生成随机家庭结构
def generate_family_structure():
    structures = ['单身', '夫妻', '三口之家', '四口之家', '三代同堂']
    return random.choice(structures)

# 生成用户数据
def generate_user_data(community_id, building_id, index):
    phone = generate_phone()
    password = generate_password()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    return {
        'phone': phone,
        'password': password_hash,
        'nickname': generate_nickname(),
        'real_name': f"用户{index}",
        'gender': generate_gender(),
        'birthday': generate_birthday().strftime('%Y-%m-%d'),
        'email': generate_email(phone),
        'community_id': community_id,
        'building_id': building_id,
        'unit': generate_unit(building_id),
        'room_number': generate_room_number(),
        'platform_type': 'pc',
        'interest_tags': generate_interest_tags(),
        'family_structure': generate_family_structure(),
        'consumption_level': random.randint(1, 5),
        'role': '居民',
        'status': 1,
        'is_verified': random.choice([0, 1])
    }

# 生成楼栋数据
def generate_building_data(community_id, building_number):
    return {
        'community_id': community_id,
        'name': f"{building_number}号楼",
        'unit_count': 2,
        'floor_count': 18,
        'household_count': 72
    }

# 批量插入用户数据
def batch_insert_users(conn, users):
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO t_user (
                phone, password, nickname, real_name, gender, birthday, email, 
                community_id, building_id, unit, room_number, platform_type, 
                interest_tags, family_structure, consumption_level, role, status, is_verified
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        data = []
        for user in users:
            data.append((
                user['phone'], user['password'], user['nickname'], user['real_name'],
                user['gender'], user['birthday'], user['email'], user['community_id'],
                user['building_id'], user['unit'], user['room_number'], user['platform_type'],
                user['interest_tags'], user['family_structure'], user['consumption_level'],
                user['role'], user['status'], user['is_verified']
            ))
        
        cursor.executemany(sql, data)
        conn.commit()
        logger.info(f"批量插入 {len(users)} 条用户数据成功")
    except Exception as e:
        conn.rollback()
        logger.error(f"批量插入用户数据失败: {e}")
        raise
    finally:
        cursor.close()

# 批量插入楼栋数据
def batch_insert_buildings(conn, buildings):
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO t_building (community_id, name, unit_count, floor_count, household_count)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        data = []
        for building in buildings:
            data.append((
                building['community_id'], building['name'], building['unit_count'],
                building['floor_count'], building['household_count']
            ))
        
        cursor.executemany(sql, data)
        conn.commit()
        logger.info(f"批量插入 {len(buildings)} 条楼栋数据成功")
    except Exception as e:
        conn.rollback()
        logger.error(f"批量插入楼栋数据失败: {e}")
        raise
    finally:
        cursor.close()

# 主函数
def main():
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        logger.info("数据库连接成功")
        
        # 获取社区ID（使用现有社区）
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM t_community LIMIT 1")
        community = cursor.fetchone()
        if not community:
            logger.error("未找到社区数据")
            return
        community_id = community['id']
        cursor.close()
        
        # 生成楼栋数据
        logger.info("开始生成楼栋数据...")
        buildings = []
        # 生成20栋楼
        for i in range(6, 26):  # 从6开始，因为已有1-5号楼
            building_data = generate_building_data(community_id, i)
            buildings.append(building_data)
        
        if buildings:
            batch_insert_buildings(conn, buildings)
        
        # 获取所有楼栋ID
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM t_building WHERE community_id = %s", (community_id,))
        building_ids = [row['id'] for row in cursor.fetchall()]
        cursor.close()
        
        if not building_ids:
            logger.error("未找到楼栋数据")
            return
        
        logger.info(f"找到 {len(building_ids)} 栋楼")
        
        # 生成用户数据
        logger.info("开始生成用户数据...")
        total_users = 100
        batch_size = 50
        users = []
        
        for i in range(1, total_users + 1):
            building_id = random.choice(building_ids)
            user_data = generate_user_data(community_id, building_id, i)
            users.append(user_data)
            
            if len(users) >= batch_size:
                batch_insert_users(conn, users)
                users = []
                logger.info(f"已生成 {i} 条用户数据")
        
        # 插入剩余用户
        if users:
            batch_insert_users(conn, users)
        
        logger.info(f"成功生成 {total_users} 条用户数据")
        
    except Exception as e:
        logger.error(f"生成数据失败: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logger.info("数据库连接已关闭")

if __name__ == "__main__":
    main()
