#!/usr/bin/env python3
"""
创建管理员账号脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from config.database import db, logger

def create_admin():
    """创建管理员账号"""
    try:
        # 检查管理员是否已存在
        existing = db.query_one("SELECT id FROM t_user WHERE phone = 'zh1111'")
        if existing:
            logger.info("管理员账号已存在")
            print("✅ 管理员账号已存在")
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
    create_admin()
