# models/access_control.py - 门禁管理模型
from config.database import execute_sql, logger
from datetime import datetime

class AccessControlDevice:
    """门禁设备模型"""
    
    def __init__(self, data=None):
        """初始化设备对象"""
        if data:
            self.id = data.get('id')
            self.device_code = data.get('device_code')
            self.device_name = data.get('device_name')
            self.device_type = data.get('device_type')
            self.building_id = data.get('building_id')
            self.location = data.get('location')
            self.ip_address = data.get('ip_address')
            self.status = data.get('status', 'normal')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, device_id):
        """根据ID查找设备"""
        sql = "SELECT * FROM t_access_control_device WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (device_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有设备"""
        sql = "SELECT * FROM t_access_control_device"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def create(cls, device_code, device_name, device_type, building_id, location, ip_address, status='normal'):
        """创建设备"""
        sql = """
            INSERT INTO t_access_control_device (
                device_code, device_name, device_type, building_id, 
                location, ip_address, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (
            device_code, device_name, device_type, building_id,
            location, ip_address, status
        )
        try:
            device_id = execute_sql(sql, params, commit=True)
            logger.info(f"设备创建成功，ID: {device_id}")
            return cls.find_by_id(device_id) if device_id else None
        except Exception as e:
            logger.error(f"设备创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新设备信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_access_control_device SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"设备更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"设备更新失败: {e}")
            raise
    
    def delete(self):
        """删除设备"""
        sql = "DELETE FROM t_access_control_device WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"设备删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"设备删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'device_type': self.device_type,
            'building_id': self.building_id,
            'location': self.location,
            'ip_address': self.ip_address,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class AccessControlPermission:
    """门禁权限模型"""
    
    def __init__(self, data=None):
        """初始化权限对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.device_id = data.get('device_id')
            self.start_time = data.get('start_time')
            self.end_time = data.get('end_time')
            self.status = data.get('status', 'active')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, permission_id):
        """根据ID查找权限"""
        sql = "SELECT * FROM t_access_control_permission WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (permission_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_user_and_device(cls, user_id, device_id):
        """根据用户ID和设备ID查找权限"""
        sql = "SELECT * FROM t_access_control_permission WHERE user_id = %s AND device_id = %s LIMIT 1"
        result = execute_sql(sql, (user_id, device_id))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有权限"""
        sql = "SELECT * FROM t_access_control_permission"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def create(cls, user_id, device_id, start_time=None, end_time=None, status='active'):
        """创建权限"""
        sql = """
            INSERT INTO t_access_control_permission (
                user_id, device_id, start_time, end_time, 
                status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (user_id, device_id, start_time, end_time, status)
        try:
            permission_id = execute_sql(sql, params, commit=True)
            logger.info(f"权限创建成功，ID: {permission_id}")
            return cls.find_by_id(permission_id) if permission_id else None
        except Exception as e:
            logger.error(f"权限创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新权限信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_access_control_permission SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"权限更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"权限更新失败: {e}")
            raise
    
    def delete(self):
        """删除权限"""
        sql = "DELETE FROM t_access_control_permission WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"权限删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"权限删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'device_id': self.device_id,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class AccessControlRecord:
    """门禁记录模型"""
    
    def __init__(self, data=None):
        """初始化记录对象"""
        if data:
            self.id = data.get('id')
            self.device_id = data.get('device_id')
            self.user_id = data.get('user_id')
            self.access_type = data.get('access_type')
            self.status = data.get('status')
            self.message = data.get('message')
            self.created_at = data.get('created_at')
    
    @classmethod
    def find_by_id(cls, record_id):
        """根据ID查找记录"""
        sql = "SELECT * FROM t_access_control_record WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (record_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有记录"""
        sql = "SELECT * FROM t_access_control_record ORDER BY created_at DESC"
        if conditions:
            sql = "SELECT * FROM t_access_control_record WHERE " + " AND ".join(conditions) + " ORDER BY created_at DESC"
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
        count_sql = f"SELECT COUNT(*) FROM t_access_control_record{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        # 查询数据
        data_sql = f"SELECT * FROM t_access_control_record{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        records = [cls(item) for item in result]
        
        return records, total
    
    @classmethod
    def create(cls, device_id, user_id, access_type, status, message):
        """创建记录"""
        sql = """
            INSERT INTO t_access_control_record (
                device_id, user_id, access_type, status, message, created_at
            ) VALUES (%s, %s, %s, %s, %s, NOW())
        """
        params = (device_id, user_id, access_type, status, message)
        try:
            record_id = execute_sql(sql, params, commit=True)
            logger.info(f"记录创建成功，ID: {record_id}")
            return cls.find_by_id(record_id) if record_id else None
        except Exception as e:
            logger.error(f"记录创建失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'user_id': self.user_id,
            'access_type': self.access_type,
            'status': self.status,
            'message': self.message,
            'created_at': str(self.created_at) if self.created_at else None
        }
