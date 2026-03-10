# models/complaint.py - 投诉建议管理模型
from config.database import execute_sql, logger
from datetime import datetime


class Complaint:
    """投诉建议模型"""
    
    def __init__(self, data=None):
        """初始化投诉建议对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.user_phone = data.get('user_phone')
            self.title = data.get('title')
            self.type = data.get('type')
            self.category = data.get('category')
            self.content = data.get('content')
            self.images = data.get('images')
            self.address = data.get('address')
            self.status = data.get('status', 'pending')
            self.priority = data.get('priority', 'medium')
            self.handler_id = data.get('handler_id')
            self.handler_name = data.get('handler_name')
            self.handle_result = data.get('handle_result')
            self.handle_time = data.get('handle_time')
            self.satisfaction = data.get('satisfaction')
            self.satisfaction_comment = data.get('satisfaction_comment')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, complaint_id):
        """根据ID查找投诉建议"""
        sql = """
            SELECT c.*, u.nickname as user_name, u.phone as user_phone,
                   h.nickname as handler_name
            FROM t_complaint c
            LEFT JOIN t_user u ON c.user_id = u.id
            LEFT JOIN t_user h ON c.handler_id = h.id
            WHERE c.id = %s LIMIT 1
        """
        result = execute_sql(sql, (complaint_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有投诉建议"""
        sql = """
            SELECT c.*, u.nickname as user_name, u.phone as user_phone,
                   h.nickname as handler_name
            FROM t_complaint c
            LEFT JOIN t_user u ON c.user_id = u.id
            LEFT JOIN t_user h ON c.handler_id = h.id
        """
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY c.created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找投诉建议"""
        offset = (page - 1) * page_size
        
        base_sql = """
            FROM t_complaint c
            LEFT JOIN t_user u ON c.user_id = u.id
            LEFT JOIN t_user h ON c.handler_id = h.id
        """
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) {base_sql}{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"""
            SELECT c.*, u.nickname as user_name, u.phone as user_phone,
                   h.nickname as handler_name
            {base_sql}{where_clause}
            ORDER BY c.created_at DESC
            LIMIT %s OFFSET %s
        """
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        complaints = [cls(item) for item in result]
        
        return complaints, total
    
    @classmethod
    def create(cls, user_id, title, type, category, content, address=None, images=None, priority='medium'):
        """创建投诉建议"""
        sql = """
            INSERT INTO t_complaint (
                user_id, title, type, category, content, address, images,
                priority, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW(), NOW())
        """
        params = (user_id, title, type, category, content, address, images, priority)
        try:
            complaint_id = execute_sql(sql, params, commit=True)
            logger.info(f"投诉建议创建成功，ID: {complaint_id}")
            return cls.find_by_id(complaint_id) if complaint_id else None
        except Exception as e:
            logger.error(f"投诉建议创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新投诉建议信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_complaint SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"投诉建议更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"投诉建议更新失败: {e}")
            raise
    
    def delete(self):
        """删除投诉建议"""
        sql = "DELETE FROM t_complaint WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"投诉建议删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"投诉建议删除失败: {e}")
            raise
    
    def assign_handler(self, handler_id, handler_name=None):
        """分配处理人员"""
        return self.update(
            handler_id=handler_id,
            handler_name=handler_name,
            status='processing'
        )
    
    def handle(self, handle_result, handler_id=None):
        """处理投诉建议"""
        updates = {
            'handle_result': handle_result,
            'handle_time': datetime.now(),
            'status': 'completed'
        }
        if handler_id:
            updates['handler_id'] = handler_id
        return self.update(**updates)
    
    def submit_satisfaction(self, satisfaction, comment=None):
        """提交满意度评价"""
        return self.update(
            satisfaction=satisfaction,
            satisfaction_comment=comment
        )
    
    @classmethod
    def get_statistics(cls):
        """获取投诉建议统计"""
        sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN satisfaction IS NOT NULL THEN 1 ELSE 0 END) as evaluated,
                AVG(satisfaction) as avg_satisfaction
            FROM t_complaint
        """
        result = execute_sql(sql)
        if result and len(result) > 0:
            stats = result[0]
            return {
                'total': stats['total'] or 0,
                'pending': stats['pending'] or 0,
                'processing': stats['processing'] or 0,
                'completed': stats['completed'] or 0,
                'evaluated': stats['evaluated'] or 0,
                'avg_satisfaction': round(stats['avg_satisfaction'], 2) if stats['avg_satisfaction'] else 0
            }
        return {
            'total': 0,
            'pending': 0,
            'processing': 0,
            'completed': 0,
            'evaluated': 0,
            'avg_satisfaction': 0
        }
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'title': self.title,
            'type': self.type,
            'category': self.category,
            'content': self.content,
            'images': self.images,
            'address': self.address,
            'status': self.status,
            'priority': self.priority,
            'handler_id': self.handler_id,
            'handler_name': self.handler_name,
            'handle_result': self.handle_result,
            'handle_time': str(self.handle_time) if self.handle_time else None,
            'satisfaction': self.satisfaction,
            'satisfaction_comment': self.satisfaction_comment,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class ComplaintCategory:
    """投诉分类模型"""
    
    def __init__(self, data=None):
        """初始化投诉分类对象"""
        if data:
            self.id = data.get('id')
            self.name = data.get('name')
            self.code = data.get('code')
            self.description = data.get('description')
            self.sort_order = data.get('sort_order', 0)
            self.status = data.get('status', 'active')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, category_id):
        """根据ID查找分类"""
        sql = "SELECT * FROM t_complaint_category WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (category_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, status='active'):
        """查找所有分类"""
        sql = "SELECT * FROM t_complaint_category WHERE status = %s ORDER BY sort_order ASC"
        result = execute_sql(sql, (status,))
        return [cls(item) for item in result]
    
    @classmethod
    def create(cls, name, code, description=None, sort_order=0):
        """创建分类"""
        sql = """
            INSERT INTO t_complaint_category (name, code, description, sort_order, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 'active', NOW(), NOW())
        """
        params = (name, code, description, sort_order)
        try:
            category_id = execute_sql(sql, params, commit=True)
            logger.info(f"投诉分类创建成功，ID: {category_id}")
            return cls.find_by_id(category_id) if category_id else None
        except Exception as e:
            logger.error(f"投诉分类创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新分类信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_complaint_category SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"投诉分类更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"投诉分类更新失败: {e}")
            raise
    
    def delete(self):
        """删除分类"""
        sql = "DELETE FROM t_complaint_category WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"投诉分类删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"投诉分类删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'sort_order': self.sort_order,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
