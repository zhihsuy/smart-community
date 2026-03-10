# models/notice.py - 公告管理模型
from config.database import execute_sql, logger
from datetime import datetime

class Notice:
    """公告模型"""
    
    def __init__(self, data=None):
        """初始化公告对象"""
        if data:
            self.id = data.get('id')
            self.title = data.get('title')
            self.type = data.get('type')
            self.content = data.get('content')
            self.author = data.get('author')
            self.author_id = data.get('author_id')
            self.publish_time = data.get('publish_time')
            self.expire_time = data.get('expire_time')
            self.status = data.get('status', 'draft')
            self.view_count = data.get('view_count', 0)
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, notice_id):
        """根据ID查找公告"""
        sql = "SELECT * FROM t_notice WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (notice_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有公告"""
        sql = "SELECT * FROM t_notice"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY publish_time DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找公告"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_notice{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_notice{where_clause} ORDER BY publish_time DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        notices = [cls(item) for item in result]
        
        return notices, total
    
    @classmethod
    def create(cls, title, type, content, author, author_id, publish_time, expire_time=None, status='published'):
        """创建公告"""
        sql = """
            INSERT INTO t_notice (
                title, type, content, author, author_id, 
                publish_time, expire_time, status, view_count, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, NOW(), NOW())
        """
        params = (title, type, content, author, author_id, publish_time, expire_time, status)
        try:
            notice_id = execute_sql(sql, params, commit=True)
            logger.info(f"公告创建成功，ID: {notice_id}")
            return cls.find_by_id(notice_id) if notice_id else None
        except Exception as e:
            logger.error(f"公告创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新公告信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_notice SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"公告更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"公告更新失败: {e}")
            raise
    
    def delete(self):
        """删除公告"""
        sql = "DELETE FROM t_notice WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"公告删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"公告删除失败: {e}")
            raise
    
    def increment_view_count(self):
        """增加浏览量"""
        sql = "UPDATE t_notice SET view_count = view_count + 1 WHERE id = %s"
        try:
            execute_sql(sql, (self.id,), commit=True)
            self.view_count += 1
        except Exception as e:
            logger.error(f"增加浏览量失败: {e}")
    
    def publish(self):
        """发布公告"""
        return self.update(status='published', publish_time=datetime.now())
    
    def unpublish(self):
        """取消发布"""
        return self.update(status='draft')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'content': self.content,
            'author': self.author,
            'author_id': self.author_id,
            'publish_time': str(self.publish_time) if self.publish_time else None,
            'expire_time': str(self.expire_time) if self.expire_time else None,
            'status': self.status,
            'view_count': self.view_count,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
