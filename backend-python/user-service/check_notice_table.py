# check_notice_table.py - 检查公告表结构
from config.database import get_db_connection, logger

def check_notice_table():
    """检查公告表结构"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 获取表结构
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 't_notice'
            ORDER BY ORDINAL_POSITION
        """)
        columns = cursor.fetchall()
        
        logger.info("t_notice 表结构:")
        for col in columns:
            logger.info(f"  {col['COLUMN_NAME']}: {col['DATA_TYPE']} - {col['COLUMN_COMMENT']}")
        
    except Exception as e:
        logger.error(f"检查表结构失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_notice_table()
