#!/usr/bin/env python3
"""
添加 role 字段到用户表并创建管理员账号
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from config.database import db, logger, execute_sql

def add_role_field():
    """添加 role 字段到用户表"""
    try:
        # 检查字段是否已存在
        result = db.query_one("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 't_user' AND COLUMN_NAME = 'role'
        """)
        
        if result:
            logger.info("role 字段已存在")
            print("✅ role 字段已存在")
        else:
            # 添加 role 字段
            execute_sql("""
                ALTER TABLE t_user 
                ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT '居民' 
                COMMENT '角色: 居民/物业管理员/运营/管理员'
            """, commit=True)
            logger.info("role 字段添加成功")
            print("✅ role 字段添加成功")
        
        return True
    except Exception as e:
        logger.error(f"添加 role 字段失败: {e}")
        print(f"❌ 添加 role 字段失败: {e}")
        return False

def create_admin():
    """创建管理员账号"""
    try:
        # 检查管理员是否已存在
        existing = db.query_one("SELECT id FROM t_user WHERE phone = 'zh1111'")
        if existing:
            # 更新为管理员角色
            db.execute("UPDATE t_user SET role = '管理员' WHERE phone = 'zh1111'")
            logger.info("管理员账号已存在，已更新角色")
            print("✅ 管理员账号已存在，已更新为管理员角色")
            return
        
        # 密码加密
        password = 'SLG123'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 创建管理员账号
        sql = """
            INSERT INTO t_user (phone, password, nickname, role, status, is_verified, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        user_id = db.execute(sql, ('zh1111', password_hash, '超级管理员', '管理员', 1, 1))
        
        logger.info(f"管理员账号创建成功，ID: {user_id}")
        print("✅ 管理员账号创建成功！")
        print(f"   账号: zh1111")
        print(f"   密码: SLG123")
        print(f"   角色: 管理员")
        
    except Exception as e:
        logger.error(f"创建管理员账号失败: {e}")
        print(f"❌ 创建失败: {e}")

if __name__ == '__main__':
    print("🚀 开始添加 role 字段并创建管理员账号...")
    if add_role_field():
        create_admin()
    print("✨ 完成！")
