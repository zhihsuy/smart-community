from config.database import execute_sql
import random
from datetime import datetime, timedelta

print("开始填充测试数据...")

# 获取用户ID用于关联数据
users = execute_sql("SELECT id, nickname FROM t_user LIMIT 10", commit=False)
if not users:
    print("请先确保有用户数据！")
    exit(1)

admin_id = users[0]['id']
user_ids = [u['id'] for u in users]

# 获取楼栋数据
buildings = execute_sql("SELECT id, name FROM t_building LIMIT 5", commit=False)
building_ids = [b['id'] for b in buildings] if buildings else []

# ==================== 1. 公告通知数据 ====================
print("\n填充公告通知数据...")
notices = [
    {
        'title': '关于春节期间物业值班安排的通知',
        'type': 'notice',
        'content': '春节期间物业将安排专人值班，如有紧急事务请联系值班电话：13800138000',
        'author': '物业',
        'author_id': admin_id,
        'publish_time': datetime.now(),
        'status': 'published'
    },
    {
        'title': '停水通知',
        'type': 'announcement',
        'content': '因管道检修，3月12日上午9:00-12:00停水，请提前做好准备。',
        'author': '物业',
        'author_id': admin_id,
        'publish_time': datetime.now(),
        'status': 'published'
    },
    {
        'title': '社区文化节活动预告',
        'type': 'activity',
        'content': '下周六将举办社区文化节，有文艺表演、美食展示等活动，欢迎参加！',
        'author': '社区',
        'author_id': admin_id,
        'publish_time': datetime.now(),
        'status': 'published'
    }
]

for notice in notices:
    execute_sql("""
        INSERT INTO t_notice (title, type, content, author, author_id, publish_time, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (notice['title'], notice['type'], notice['content'], notice['author'], 
          notice['author_id'], notice['publish_time'], notice['status']), commit=True)

# ==================== 2. 投诉建议数据 ====================
print("填充投诉建议数据...")
complaints = [
    {
        'type': 'facility',
        'title': '小区路灯损坏',
        'content': '3栋楼下的路灯坏了好几天，晚上走路不安全。',
        'user_id': user_ids[0],
        'status': 'pending',
        'priority': 'high'
    },
    {
        'type': 'service',
        'title': '建议增加健身器材',
        'content': '建议在小花园增加一些健身器材，方便老人锻炼。',
        'user_id': user_ids[1],
        'status': 'processing',
        'priority': 'medium'
    },
    {
        'type': 'environment',
        'title': '夜间噪音扰民',
        'content': '最近晚上有人在小区里大声喧哗，影响休息。',
        'user_id': user_ids[2],
        'status': 'resolved',
        'priority': 'medium'
    }
]

for comp in complaints:
    execute_sql("""
        INSERT INTO t_complaint (user_id, type, title, content, status, priority, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (comp['user_id'], comp['type'], comp['title'], 
          comp['content'], comp['status'], comp['priority']), commit=True)

# ==================== 3. 报修管理数据 ====================
print("填充报修管理数据...")
repair_orders = [
    {
        'type': 'water_elec',
        'title': '楼道灯不亮',
        'description': '5单元3楼楼道灯不亮，请尽快维修。',
        'address': '5单元3楼',
        'status': 'pending',
        'user_id': user_ids[0],
        'priority': 'high'
    },
    {
        'type': 'property',
        'title': '水管漏水',
        'description': '家里厨房水管有点漏水。',
        'address': '8栋201室',
        'status': 'processing',
        'user_id': user_ids[1],
        'priority': 'medium'
    },
    {
        'type': 'other',
        'title': '门窗问题',
        'description': '防盗门开关有点卡住了。',
        'address': '12栋302室',
        'status': 'completed',
        'user_id': user_ids[2],
        'priority': 'low'
    }
]

for order in repair_orders:
    execute_sql("""
        INSERT INTO t_repair_order (user_id, type, title, description, address, status, priority, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (order['user_id'], order['type'], order['title'], 
          order['description'], order['address'], order['status'], order['priority']), commit=True)

# ==================== 4. 门禁设备数据 ====================
print("填充门禁设备数据...")
if building_ids:
    access_devices = [
        {'device_code': 'ACC001', 'device_name': '小区大门门禁', 'device_type': 'face', 'building_id': building_ids[0], 'location': '小区大门', 'ip_address': '192.168.1.101', 'status': 'normal'},
        {'device_code': 'ACC002', 'device_name': '1栋单元门', 'device_type': 'card', 'building_id': building_ids[0], 'location': '1栋单元门', 'ip_address': '192.168.1.102', 'status': 'normal'},
        {'device_code': 'ACC003', 'device_name': '2栋单元门', 'device_type': 'password', 'building_id': building_ids[1], 'location': '2栋单元门', 'ip_address': '192.168.1.103', 'status': 'normal'},
        {'device_code': 'ACC004', 'device_name': '地下车库入口', 'device_type': 'qrcode', 'building_id': building_ids[0], 'location': '地下车库', 'ip_address': '192.168.1.104', 'status': 'normal'},
        {'device_code': 'ACC005', 'device_name': '后门门禁', 'device_type': 'face', 'building_id': building_ids[0], 'location': '小区后门', 'ip_address': '192.168.1.105', 'status': 'offline'}
    ]

    for device in access_devices:
        execute_sql("""
            INSERT INTO t_access_control_device (device_code, device_name, device_type, building_id, location, ip_address, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (device['device_code'], device['device_name'], device['device_type'], 
              device['building_id'], device['location'], device['ip_address'], device['status']), commit=True)

# ==================== 5. 停车位数据 ====================
print("填充停车位数据...")
parking_spaces = []
for i in range(1, 31):
    status = 'free' if random.random() > 0.4 else 'occupied'
    p_type = random.choice(['underground', 'ground', 'visitor'])
    building_id = random.choice(building_ids) if building_ids else None
    parking_spaces.append({
        'space_code': f'PK{i:03d}',
        'space_name': f'A区{i}号车位',
        'type': p_type,
        'status': status,
        'building_id': building_id,
        'location': '地下停车场' if p_type == 'underground' else '地面停车场',
        'price': round(random.uniform(200, 500), 2)
    })

for space in parking_spaces:
    execute_sql("""
        INSERT INTO t_parking_space (space_code, space_name, type, status, building_id, location, price, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (space['space_code'], space['space_name'], space['type'], space['status'], 
          space['building_id'], space['location'], space['price']), commit=True)

print("\n✅ 测试数据填充完成！")
