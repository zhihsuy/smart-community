import datetime
import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)

class EnergyConsumption:
    """能耗数据模型"""
    
    def __init__(self, data=None):
        """初始化能耗数据对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.building_id = data.get('building_id')
            self.building_name = data.get('building_name')
            self.room_number = data.get('room_number')
            self.type = data.get('type')  # electricity, water
            self.usage = data.get('usage')  # 用量
            self.unit = data.get('unit')  # 单位
            self.cost = data.get('cost')  # 费用
            self.reading_date = data.get('reading_date')  # 抄表日期
            self.meter_id = data.get('meter_id')  # 表计ID
            self.remark = data.get('remark')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def create(cls, user_id, building_id, type, usage, unit, cost, reading_date, meter_id, remark=None):
        """创建能耗记录"""
        sql = """
            INSERT INTO t_energy_consumption (
                user_id, building_id, type, usage, unit, cost, reading_date, meter_id, 
                remark, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (user_id, building_id, type, usage, unit, cost, reading_date, meter_id, remark)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            energy_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"能耗记录创建成功，ID: {energy_id}")
            return cls.find_by_id(energy_id) if energy_id else None
        except Exception as e:
            logger.error(f"能耗记录创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, energy_id):
        """根据ID查询能耗记录"""
        sql = """
            SELECT ec.*, u.nickname as user_name, b.building_name, b.room_number 
            FROM t_energy_consumption ec
            LEFT JOIN t_user u ON ec.user_id = u.id
            LEFT JOIN t_building b ON ec.building_id = b.id
            WHERE ec.id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (energy_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询能耗记录失败: {e}")
            return None
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=20):
        """分页查询能耗记录"""
        base_sql = """
            SELECT ec.*, u.nickname as user_name, b.building_name, b.room_number 
            FROM t_energy_consumption ec
            LEFT JOIN t_user u ON ec.user_id = u.id
            LEFT JOIN t_building b ON ec.building_id = b.id
        """
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) as total FROM t_energy_consumption ec {where_clause}"
        
        offset = (page - 1) * page_size
        query_sql = f"{base_sql} {where_clause} ORDER BY ec.reading_date DESC LIMIT %s OFFSET %s"
        
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
            
            energies = [cls(result) for result in results]
            return energies, total
        except Exception as e:
            logger.error(f"分页查询能耗记录失败: {e}")
            return [], 0
    
    @classmethod
    def get_statistics(cls, start_date, end_date, type=None, user_id=None, building_id=None):
        """获取能耗统计"""
        sql = """
            SELECT 
                SUM(usage) as total_usage, 
                SUM(cost) as total_cost,
                type
            FROM t_energy_consumption
            WHERE reading_date BETWEEN %s AND %s
        """
        
        params = [start_date, end_date]
        
        if type:
            sql += " AND type = %s"
            params.append(type)
        
        if user_id:
            sql += " AND user_id = %s"
            params.append(user_id)
        
        if building_id:
            sql += " AND building_id = %s"
            params.append(building_id)
        
        sql += " GROUP BY type"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"获取能耗统计失败: {e}")
            return []
    
    @classmethod
    def get_trend(cls, start_date, end_date, type=None, user_id=None, building_id=None):
        """获取能耗趋势"""
        sql = """
            SELECT 
                DATE_FORMAT(reading_date, '%Y-%m') as month, 
                SUM(usage) as usage, 
                SUM(cost) as cost
            FROM t_energy_consumption
            WHERE reading_date BETWEEN %s AND %s
        """
        
        params = [start_date, end_date]
        
        if type:
            sql += " AND type = %s"
            params.append(type)
        
        if user_id:
            sql += " AND user_id = %s"
            params.append(user_id)
        
        if building_id:
            sql += " AND building_id = %s"
            params.append(building_id)
        
        sql += " GROUP BY DATE_FORMAT(reading_date, '%Y-%m') ORDER BY month"
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"获取能耗趋势失败: {e}")
            return []
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'building_id': self.building_id,
            'building_name': self.building_name,
            'room_number': self.room_number,
            'type': self.type,
            'usage': self.usage,
            'unit': self.unit,
            'cost': self.cost,
            'reading_date': self.reading_date,
            'meter_id': self.meter_id,
            'remark': self.remark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class EnergyMeter:
    """能耗表计模型"""
    
    def __init__(self, data=None):
        """初始化表计对象"""
        if data:
            self.id = data.get('id')
            self.meter_id = data.get('meter_id')
            self.type = data.get('type')  # electricity, water
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.building_id = data.get('building_id')
            self.building_name = data.get('building_name')
            self.room_number = data.get('room_number')
            self.install_date = data.get('install_date')
            self.last_reading = data.get('last_reading')
            self.last_reading_date = data.get('last_reading_date')
            self.status = data.get('status')  # active, inactive
            self.remark = data.get('remark')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def create(cls, meter_id, type, user_id, building_id, install_date, remark=None):
        """创建表计"""
        sql = """
            INSERT INTO t_energy_meter (
                meter_id, type, user_id, building_id, install_date, 
                status, remark, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, 'active', %s, NOW(), NOW())
        """
        params = (meter_id, type, user_id, building_id, install_date, remark)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            meter_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"表计创建成功，ID: {meter_id}")
            return cls.find_by_id(meter_id) if meter_id else None
        except Exception as e:
            logger.error(f"表计创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, meter_id):
        """根据ID查询表计"""
        sql = """
            SELECT em.*, u.nickname as user_name, b.building_name, b.room_number 
            FROM t_energy_meter em
            LEFT JOIN t_user u ON em.user_id = u.id
            LEFT JOIN t_building b ON em.building_id = b.id
            WHERE em.id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (meter_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询表计失败: {e}")
            return None
    
    @classmethod
    def find_all(cls, type=None, user_id=None, building_id=None):
        """查询表计列表"""
        sql = """
            SELECT em.*, u.nickname as user_name, b.building_name, b.room_number 
            FROM t_energy_meter em
            LEFT JOIN t_user u ON em.user_id = u.id
            LEFT JOIN t_building b ON em.building_id = b.id
        """
        
        conditions = []
        params = []
        
        if type:
            conditions.append("em.type = %s")
            params.append(type)
        
        if user_id:
            conditions.append("em.user_id = %s")
            params.append(user_id)
        
        if building_id:
            conditions.append("em.building_id = %s")
            params.append(building_id)
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [cls(result) for result in results]
        except Exception as e:
            logger.error(f"查询表计列表失败: {e}")
            return []
    
    def update_reading(self, reading, reading_date):
        """更新表计读数"""
        sql = """
            UPDATE t_energy_meter 
            SET last_reading = %s, last_reading_date = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (reading, reading_date, self.id)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"表计读数更新成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"表计读数更新失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'type': self.type,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'building_id': self.building_id,
            'building_name': self.building_name,
            'room_number': self.room_number,
            'install_date': self.install_date,
            'last_reading': self.last_reading,
            'last_reading_date': self.last_reading_date,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
