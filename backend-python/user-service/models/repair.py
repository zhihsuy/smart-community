# models/repair.py - 报修管理模型
from config.database import execute_sql, logger
from datetime import datetime

class RepairOrder:
    """维修工单模型"""
    
    def __init__(self, data=None):
        """初始化维修工单对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.title = data.get('title')
            self.type = data.get('type')
            self.description = data.get('description')
            self.address = data.get('address')
            self.images = data.get('images')
            self.priority = data.get('priority', 'medium')
            self.status = data.get('status', 'pending')
            self.technician_id = data.get('technician_id')
            self.estimated_time = data.get('estimated_time')
            self.process_result = data.get('process_result')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, order_id):
        """根据ID查找维修工单"""
        sql = "SELECT * FROM t_repair_order WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (order_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有维修工单"""
        sql = "SELECT * FROM t_repair_order"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找维修工单"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_repair_order{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_repair_order{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        orders = [cls(item) for item in result]
        
        return orders, total
    
    @classmethod
    def create(cls, user_id, title, type, description, address, images=None, priority='medium'):
        """创建维修工单"""
        sql = """
            INSERT INTO t_repair_order (
                user_id, title, type, description, address, images, 
                priority, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending', NOW(), NOW())
        """
        params = (user_id, title, type, description, address, images, priority)
        try:
            order_id = execute_sql(sql, params, commit=True)
            logger.info(f"维修工单创建成功，ID: {order_id}")
            return cls.find_by_id(order_id) if order_id else None
        except Exception as e:
            logger.error(f"维修工单创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新维修工单信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_repair_order SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"维修工单更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"维修工单更新失败: {e}")
            raise
    
    def assign_technician(self, technician_id, estimated_time=None):
        """分配维修人员"""
        return self.update(
            technician_id=technician_id,
            estimated_time=estimated_time,
            status='processing'
        )
    
    def complete(self, process_result):
        """完成维修"""
        return self.update(
            process_result=process_result,
            status='completed'
        )
    
    def cancel(self):
        """取消维修工单"""
        return self.update(status='cancelled')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'address': self.address,
            'images': self.images,
            'priority': self.priority,
            'status': self.status,
            'technician_id': self.technician_id,
            'estimated_time': str(self.estimated_time) if self.estimated_time else None,
            'process_result': self.process_result,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class Technician:
    """维修人员模型"""
    
    def __init__(self, data=None):
        """初始化维修人员对象"""
        if data:
            self.id = data.get('id')
            self.name = data.get('name')
            self.phone = data.get('phone')
            self.specialty = data.get('specialty')
            self.status = data.get('status', 'active')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, technician_id):
        """根据ID查找维修人员"""
        sql = "SELECT * FROM t_technician WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (technician_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有维修人员"""
        sql = "SELECT * FROM t_technician"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找维修人员"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_technician{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_technician{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        technicians = [cls(item) for item in result]
        
        return technicians, total
    
    @classmethod
    def create(cls, name, phone, specialty=None, status='active'):
        """创建维修人员"""
        sql = """
            INSERT INTO t_technician (
                name, phone, specialty, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, NOW(), NOW())
        """
        params = (name, phone, specialty, status)
        try:
            technician_id = execute_sql(sql, params, commit=True)
            logger.info(f"维修人员创建成功，ID: {technician_id}")
            return cls.find_by_id(technician_id) if technician_id else None
        except Exception as e:
            logger.error(f"维修人员创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新维修人员信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_technician SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"维修人员更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"维修人员更新失败: {e}")
            raise
    
    def delete(self):
        """删除维修人员"""
        sql = "DELETE FROM t_technician WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"维修人员删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"维修人员删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'specialty': self.specialty,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
