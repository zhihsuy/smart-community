import datetime
import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)

class MonitoringDevice:
    """监控设备模型
    
    该模型用于管理监控设备的基本信息，包括设备ID、名称、类型、位置、状态等
    支持设备的创建、查询、状态更新等操作
    """
    
    def __init__(self, data=None):
        """初始化监控设备对象
        
        Args:
            data (dict, optional): 设备数据字典
        """
        if data:
            self.id = data.get('id')
            self.device_id = data.get('device_id')  # 设备唯一标识
            self.name = data.get('name')  # 设备名称
            self.type = data.get('type')  # 设备类型：camera, sensor等
            self.location = data.get('location')  # 安装位置
            self.ip_address = data.get('ip_address')  # IP地址
            self.port = data.get('port')  # 端口号
            self.status = data.get('status')  # 设备状态：online, offline, maintenance
            self.resolution = data.get('resolution')  # 分辨率
            self.stream_url = data.get('stream_url')  # 视频流地址
            self.username = data.get('username')  # 登录用户名
            self.password = data.get('password')  # 登录密码
            self.install_date = data.get('install_date')  # 安装日期
            self.last_maintenance = data.get('last_maintenance')  # 最后维护日期
            self.remark = data.get('remark')  # 备注信息
            self.created_at = data.get('created_at')  # 创建时间
            self.updated_at = data.get('updated_at')  # 更新时间
    
    @classmethod
    def create(cls, device_id, name, type, location, ip_address, port, 
               stream_url, username, password, resolution=None, remark=None):
        """创建监控设备
        
        Args:
            device_id (str): 设备唯一标识
            name (str): 设备名称
            type (str): 设备类型
            location (str): 安装位置
            ip_address (str): IP地址
            port (int): 端口号
            stream_url (str): 视频流地址
            username (str): 登录用户名
            password (str): 登录密码
            resolution (str, optional): 分辨率
            remark (str, optional): 备注信息
            
        Returns:
            MonitoringDevice: 创建的监控设备对象
            None: 创建失败时返回
        """
        sql = """
            INSERT INTO t_monitoring_device (
                device_id, name, type, location, ip_address, port, 
                stream_url, username, password, resolution, status, 
                install_date, remark, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'online', 
                      NOW(), %s, NOW(), NOW())
        """
        params = (device_id, name, type, location, ip_address, port, 
                  stream_url, username, password, resolution, remark)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            device_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"监控设备创建成功，ID: {device_id}")
            return cls.find_by_id(device_id) if device_id else None
        except Exception as e:
            logger.error(f"监控设备创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, device_id):
        """根据ID查询监控设备
        
        Args:
            device_id (int): 设备ID
            
        Returns:
            MonitoringDevice: 监控设备对象
            None: 设备不存在时返回
        """
        sql = "SELECT * FROM t_monitoring_device WHERE id = %s"
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (device_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询监控设备失败: {e}")
            return None
    
    @classmethod
    def find_all(cls, type=None, status=None, location=None):
        """查询监控设备列表
        
        Args:
            type (str, optional): 设备类型
            status (str, optional): 设备状态
            location (str, optional): 安装位置（模糊匹配）
            
        Returns:
            list: 监控设备对象列表
        """
        sql = "SELECT * FROM t_monitoring_device"
        
        conditions = []
        params = []
        
        if type:
            conditions.append("type = %s")
            params.append(type)
        if status:
            conditions.append("status = %s")
            params.append(status)
        if location:
            conditions.append("location LIKE %s")
            params.append(f"%{location}%")
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        sql += " ORDER BY created_at DESC"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [cls(result) for result in results]
        except Exception as e:
            logger.error(f"查询监控设备列表失败: {e}")
            return []
    
    def update_status(self, status):
        """更新设备状态
        
        Args:
            status (str): 设备状态（online, offline, maintenance）
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        sql = """
            UPDATE t_monitoring_device 
            SET status = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (status, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"监控设备状态更新成功，ID: {self.id}, 状态: {status}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"监控设备状态更新失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'ip_address': self.ip_address,
            'port': self.port,
            'status': self.status,
            'resolution': self.resolution,
            'stream_url': self.stream_url,
            'install_date': self.install_date,
            'last_maintenance': self.last_maintenance,
            'remark': self.remark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class AlertRule:
    """预警规则模型
    
    该模型用于管理监控预警规则，包括规则名称、类型、设备关联、阈值等
    支持规则的创建、查询、状态切换等操作
    """
    
    def __init__(self, data=None):
        """初始化预警规则对象
        
        Args:
            data (dict, optional): 规则数据字典
        """
        if data:
            self.id = data.get('id')  # 规则ID
            self.name = data.get('name')  # 规则名称
            self.type = data.get('type')  # 规则类型：motion, fire, intrusion等
            self.device_id = data.get('device_id')  # 关联设备ID
            self.device_name = data.get('device_name')  # 关联设备名称
            self.threshold = data.get('threshold')  # 预警阈值
            self.enabled = data.get('enabled', True)  # 规则是否启用
            self.description = data.get('description')  # 规则描述
            self.created_at = data.get('created_at')  # 创建时间
            self.updated_at = data.get('updated_at')  # 更新时间
    
    @classmethod
    def create(cls, name, type, device_id, threshold, description=None):
        """创建预警规则
        
        Args:
            name (str): 规则名称
            type (str): 规则类型
            device_id (int): 关联设备ID
            threshold (float): 预警阈值
            description (str, optional): 规则描述
            
        Returns:
            AlertRule: 创建的预警规则对象
            None: 创建失败时返回
        """
        sql = """
            INSERT INTO t_alert_rule (
                name, type, device_id, threshold, enabled, 
                description, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, true, %s, NOW(), NOW())
        """
        params = (name, type, device_id, threshold, description)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rule_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"预警规则创建成功，ID: {rule_id}")
            return cls.find_by_id(rule_id) if rule_id else None
        except Exception as e:
            logger.error(f"预警规则创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, rule_id):
        """根据ID查询预警规则
        
        Args:
            rule_id (int): 规则ID
            
        Returns:
            AlertRule: 预警规则对象
            None: 规则不存在时返回
        """
        sql = """
            SELECT ar.*, md.name as device_name 
            FROM t_alert_rule ar
            LEFT JOIN t_monitoring_device md ON ar.device_id = md.id
            WHERE ar.id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (rule_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询预警规则失败: {e}")
            return None
    
    @classmethod
    def find_all(cls, device_id=None, type=None, enabled=None):
        """查询预警规则列表
        
        Args:
            device_id (int, optional): 设备ID
            type (str, optional): 规则类型
            enabled (bool, optional): 规则是否启用
            
        Returns:
            list: 预警规则对象列表
        """
        sql = """
            SELECT ar.*, md.name as device_name 
            FROM t_alert_rule ar
            LEFT JOIN t_monitoring_device md ON ar.device_id = md.id
        """
        
        conditions = []
        params = []
        
        if device_id:
            conditions.append("ar.device_id = %s")
            params.append(device_id)
        if type:
            conditions.append("ar.type = %s")
            params.append(type)
        if enabled is not None:
            conditions.append("ar.enabled = %s")
            params.append(enabled)
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        sql += " ORDER BY ar.created_at DESC"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [cls(result) for result in results]
        except Exception as e:
            logger.error(f"查询预警规则列表失败: {e}")
            return []
    
    def toggle(self):
        """切换规则状态
        
        切换规则的启用/禁用状态
        
        Returns:
            bool: 切换成功返回True，失败返回False
        """
        new_status = not self.enabled
        sql = """
            UPDATE t_alert_rule 
            SET enabled = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (new_status, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"预警规则状态切换成功，ID: {self.id}, 新状态: {new_status}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"预警规则状态切换失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'threshold': self.threshold,
            'enabled': self.enabled,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class AlertRecord:
    """预警记录模型"""
    
    def __init__(self, data=None):
        """初始化预警记录对象"""
        if data:
            self.id = data.get('id')
            self.rule_id = data.get('rule_id')
            self.rule_name = data.get('rule_name')
            self.device_id = data.get('device_id')
            self.device_name = data.get('device_name')
            self.type = data.get('type')
            self.message = data.get('message')
            self.level = data.get('level')  # low, medium, high
            self.status = data.get('status')  # pending, processed, ignored
            self.processed_by = data.get('processed_by')
            self.processed_at = data.get('processed_at')
            self.process_note = data.get('process_note')
            self.created_at = data.get('created_at')
    
    @classmethod
    def create(cls, rule_id, device_id, type, message, level='medium'):
        """创建预警记录"""
        sql = """
            INSERT INTO t_alert_record (
                rule_id, device_id, type, message, level, status, 
                created_at
            ) VALUES (%s, %s, %s, %s, %s, 'pending', NOW())
        """
        params = (rule_id, device_id, type, message, level)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            record_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"预警记录创建成功，ID: {record_id}")
            return cls.find_by_id(record_id) if record_id else None
        except Exception as e:
            logger.error(f"预警记录创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, record_id):
        """根据ID查询预警记录"""
        sql = """
            SELECT ar.*, ar2.name as rule_name, md.name as device_name 
            FROM t_alert_record ar
            LEFT JOIN t_alert_rule ar2 ON ar.rule_id = ar2.id
            LEFT JOIN t_monitoring_device md ON ar.device_id = md.id
            WHERE ar.id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (record_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询预警记录失败: {e}")
            return None
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=20):
        """分页查询预警记录"""
        base_sql = """
            SELECT ar.*, ar2.name as rule_name, md.name as device_name 
            FROM t_alert_record ar
            LEFT JOIN t_alert_rule ar2 ON ar.rule_id = ar2.id
            LEFT JOIN t_monitoring_device md ON ar.device_id = md.id
        """
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) as total FROM t_alert_record ar {where_clause}"
        
        offset = (page - 1) * page_size
        query_sql = f"{base_sql} {where_clause} ORDER BY ar.created_at DESC LIMIT %s OFFSET %s"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 获取总数
            cursor.execute(count_sql, params or ())
            total_result = cursor.fetchone()
            total = total_result['total'] if total_result else 0
            
            # 获取分页数据
            cursor.execute(query_sql, (page_size, offset) + (tuple(params) if params else ()))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            alerts = [cls(result) for result in results]
            return alerts, total
        except Exception as e:
            logger.error(f"分页查询预警记录失败: {e}")
            return [], 0
    
    def process(self, processed_by, process_note):
        """处理预警"""
        sql = """
            UPDATE t_alert_record 
            SET status = 'processed', processed_by = %s, 
                processed_at = NOW(), process_note = %s
            WHERE id = %s
        """
        params = (processed_by, process_note, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"预警记录处理成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"预警记录处理失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'type': self.type,
            'message': self.message,
            'level': self.level,
            'status': self.status,
            'processed_by': self.processed_by,
            'processed_at': self.processed_at,
            'process_note': self.process_note,
            'created_at': self.created_at
        }

class MonitoringRequest:
    """监控查看申请模型"""
    
    def __init__(self, data=None):
        """初始化监控查看申请对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.device_id = data.get('device_id')
            self.device_name = data.get('device_name')
            self.purpose = data.get('purpose')
            self.start_time = data.get('start_time')
            self.end_time = data.get('end_time')
            self.status = data.get('status')  # pending, approved, rejected
            self.approved_by = data.get('approved_by')
            self.approved_at = data.get('approved_at')
            self.reason = data.get('reason')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def create(cls, user_id, device_id, purpose, start_time, end_time):
        """创建监控查看申请"""
        sql = """
            INSERT INTO t_monitoring_request (
                user_id, device_id, purpose, start_time, end_time, status, 
                created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, 'pending', NOW(), NOW())
        """
        params = (user_id, device_id, purpose, start_time, end_time)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            request_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"监控查看申请创建成功，ID: {request_id}")
            return cls.find_by_id(request_id) if request_id else None
        except Exception as e:
            logger.error(f"监控查看申请创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, request_id):
        """根据ID查询监控查看申请"""
        sql = """
            SELECT mr.*, u.nickname as user_name, md.name as device_name 
            FROM t_monitoring_request mr
            LEFT JOIN t_user u ON mr.user_id = u.id
            LEFT JOIN t_monitoring_device md ON mr.device_id = md.id
            WHERE mr.id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (request_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询监控查看申请失败: {e}")
            return None
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=20):
        """分页查询监控查看申请"""
        base_sql = """
            SELECT mr.*, u.nickname as user_name, md.name as device_name 
            FROM t_monitoring_request mr
            LEFT JOIN t_user u ON mr.user_id = u.id
            LEFT JOIN t_monitoring_device md ON mr.device_id = md.id
        """
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) as total FROM t_monitoring_request mr {where_clause}"
        
        offset = (page - 1) * page_size
        query_sql = f"{base_sql} {where_clause} ORDER BY mr.created_at DESC LIMIT %s OFFSET %s"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 获取总数
            cursor.execute(count_sql, params or ())
            total_result = cursor.fetchone()
            total = total_result['total'] if total_result else 0
            
            # 获取分页数据
            cursor.execute(query_sql, (page_size, offset) + (tuple(params) if params else ()))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            requests = [cls(result) for result in results]
            return requests, total
        except Exception as e:
            logger.error(f"分页查询监控查看申请失败: {e}")
            return [], 0
    
    def approve(self, approved_by, reason=None):
        """批准申请"""
        sql = """
            UPDATE t_monitoring_request 
            SET status = 'approved', approved_by = %s, 
                approved_at = NOW(), reason = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (approved_by, reason, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"监控查看申请批准成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"监控查看申请批准失败: {e}")
            return False
    
    def reject(self, approved_by, reason):
        """拒绝申请"""
        sql = """
            UPDATE t_monitoring_request 
            SET status = 'rejected', approved_by = %s, 
                approved_at = NOW(), reason = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (approved_by, reason, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"监控查看申请拒绝成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"监控查看申请拒绝失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'purpose': self.purpose,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at,
            'reason': self.reason,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
