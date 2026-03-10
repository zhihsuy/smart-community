# models/visitor.py - 访客管理模型
from config.database import execute_sql, logger
from datetime import datetime

class Visitor:
    """访客模型"""
    
    def __init__(self, data=None):
        """初始化访客对象"""
        if data:
            self.id = data.get('id')
            self.visitor_name = data.get('visitor_name')
            self.visitor_phone = data.get('visitor_phone')
            self.visitor_idcard = data.get('visitor_idcard')
            self.host_id = data.get('host_id')
            self.host_name = data.get('host_name')
            self.host_phone = data.get('host_phone')
            self.building_id = data.get('building_id')
            self.room_number = data.get('room_number')
            self.visit_purpose = data.get('visit_purpose')
            self.visit_date = data.get('visit_date')
            self.visit_time_start = data.get('visit_time_start')
            self.visit_time_end = data.get('visit_time_end')
            self.qr_code = data.get('qr_code')
            self.status = data.get('status', 'pending')
            self.entry_time = data.get('entry_time')
            self.exit_time = data.get('exit_time')
            self.approve_time = data.get('approve_time')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, visitor_id):
        """根据ID查找访客"""
        sql = "SELECT * FROM t_visitor WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (visitor_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有访客"""
        sql = "SELECT * FROM t_visitor"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找访客"""
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 构建查询条件
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM t_visitor{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        # 查询数据
        data_sql = f"SELECT * FROM t_visitor{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        visitors = [cls(item) for item in result]
        
        return visitors, total
    
    @classmethod
    def create(cls, visitor_name, visitor_phone, visitor_idcard, host_id, host_name, host_phone, building_id, room_number, visit_purpose, visit_date, visit_time_start, visit_time_end, qr_code):
        """创建访客"""
        sql = """
            INSERT INTO t_visitor (
                visitor_name, visitor_phone, visitor_idcard, host_id, host_name, host_phone, 
                building_id, room_number, visit_purpose, visit_date, visit_time_start, visit_time_end, 
                qr_code, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (
            visitor_name, visitor_phone, visitor_idcard, host_id, host_name, host_phone, 
            building_id, room_number, visit_purpose, visit_date, visit_time_start, visit_time_end, 
            qr_code, 'pending'
        )
        try:
            visitor_id = execute_sql(sql, params, commit=True)
            logger.info(f"访客创建成功，ID: {visitor_id}")
            return cls.find_by_id(visitor_id) if visitor_id else None
        except Exception as e:
            logger.error(f"访客创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新访客信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_visitor SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"访客更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"访客更新失败: {e}")
            raise
    
    def delete(self):
        """删除访客"""
        sql = "DELETE FROM t_visitor WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"访客删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"访客删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'visitor_name': self.visitor_name,
            'visitor_phone': self.visitor_phone,
            'visitor_idcard': self.visitor_idcard,
            'host_id': self.host_id,
            'host_name': self.host_name,
            'host_phone': self.host_phone,
            'building_id': self.building_id,
            'room_number': self.room_number,
            'visit_purpose': self.visit_purpose,
            'visit_date': str(self.visit_date) if self.visit_date else None,
            'visit_time_start': str(self.visit_time_start) if self.visit_time_start else None,
            'visit_time_end': str(self.visit_time_end) if self.visit_time_end else None,
            'qr_code': self.qr_code,
            'status': self.status,
            'entry_time': str(self.entry_time) if self.entry_time else None,
            'exit_time': str(self.exit_time) if self.exit_time else None,
            'approve_time': str(self.approve_time) if self.approve_time else None,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class VisitorRecord:
    """访客记录模型"""
    
    def __init__(self, data=None):
        """初始化记录对象"""
        if data:
            self.id = data.get('id')
            self.visitor_id = data.get('visitor_id')
            self.device_id = data.get('device_id')
            self.record_type = data.get('record_type')
            self.photo_url = data.get('photo_url')
            self.temperature = data.get('temperature')
            self.record_time = data.get('record_time')
    
    @classmethod
    def find_by_id(cls, record_id):
        """根据ID查找记录"""
        sql = "SELECT * FROM t_visitor_record WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (record_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_visitor_id(cls, visitor_id):
        """根据访客ID查找记录"""
        sql = "SELECT * FROM t_visitor_record WHERE visitor_id = %s ORDER BY record_time DESC"
        result = execute_sql(sql, (visitor_id,))
        return [cls(item) for item in result]
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有记录"""
        sql = "SELECT * FROM t_visitor_record ORDER BY record_time DESC"
        if conditions:
            sql = "SELECT * FROM t_visitor_record WHERE " + " AND ".join(conditions) + " ORDER BY record_time DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找记录"""
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 构建查询条件
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM t_visitor_record{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        # 查询数据
        data_sql = f"SELECT * FROM t_visitor_record{where_clause} ORDER BY record_time DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        records = [cls(item) for item in result]
        
        return records, total
    
    @classmethod
    def create(cls, visitor_id, device_id, record_type, photo_url=None, temperature=None):
        """创建记录"""
        sql = """
            INSERT INTO t_visitor_record (
                visitor_id, device_id, record_type, photo_url, temperature, record_time
            ) VALUES (%s, %s, %s, %s, %s, NOW())
        """
        params = (visitor_id, device_id, record_type, photo_url, temperature)
        try:
            record_id = execute_sql(sql, params, commit=True)
            logger.info(f"访客记录创建成功，ID: {record_id}")
            return cls.find_by_id(record_id) if record_id else None
        except Exception as e:
            logger.error(f"访客记录创建失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'visitor_id': self.visitor_id,
            'device_id': self.device_id,
            'record_type': self.record_type,
            'photo_url': self.photo_url,
            'temperature': self.temperature,
            'record_time': str(self.record_time) if self.record_time else None
        }
