# update_notice_table.py - 更新公告表结构
from config.database import get_db_connection, logger

def update_notice_table():
    """更新公告表，添加 author 字段"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 检查 author 字段是否存在
        cursor.execute("""
            SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 't_notice' AND COLUMN_NAME = 'author'
        """)
        result = cursor.fetchone()
        
        if result['count'] == 0:
            # 添加 author 字段
            cursor.execute("""
                ALTER TABLE t_notice 
                ADD COLUMN author VARCHAR(100) COMMENT '发布人姓名' AFTER publisher_id
            """)
            conn.commit()
            logger.info("成功添加 author 字段到 t_notice 表")
        else:
            logger.info("author 字段已存在")
        
        # 检查 notice_type 字段是否存在（如果不存在，说明表结构是旧的）
        cursor.execute("""
            SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 't_notice' AND COLUMN_NAME = 'notice_type'
        """)
        result = cursor.fetchone()
        
        if result['count'] == 0:
            logger.warning("表结构可能是旧的，建议重新初始化数据库表")
        else:
            logger.info("表结构正确")
        
        logger.info("公告表更新完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"更新公告表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    update_notice_table()
