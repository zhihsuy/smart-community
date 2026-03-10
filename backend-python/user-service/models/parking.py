# models/parking.py - 停车管理模型
from config.database import execute_sql, logger
from datetime import datetime

class ParkingSpace:
    """车位模型"""
    
    def __init__(self, data=None):
        """初始化车位对象"""
        if data:
            self.id = data.get('id')
            self.space_code = data.get('space_code')
            self.space_name = data.get('space_name')
            self.type = data.get('type')
            self.status = data.get('status', 'free')
            self.building_id = data.get('building_id')
            self.location = data.get('location')
            self.price = data.get('price')
            self.owner_id = data.get('owner_id')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, space_id):
        """根据ID查找车位"""
        sql = "SELECT * FROM t_parking_space WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (space_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_code(cls, space_code):
        """根据编码查找车位"""
        sql = "SELECT * FROM t_parking_space WHERE space_code = %s LIMIT 1"
        result = execute_sql(sql, (space_code,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有车位"""
        sql = "SELECT * FROM t_parking_space"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找车位"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_parking_space{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_parking_space{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        spaces = [cls(item) for item in result]
        
        return spaces, total
    
    @classmethod
    def create(cls, space_code, space_name, type, location, building_id=None, price=None, owner_id=None, status='free'):
        """创建车位"""
        sql = """
            INSERT INTO t_parking_space (
                space_code, space_name, type, location, building_id, 
                price, owner_id, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (
            space_code, space_name, type, location, building_id,
            price, owner_id, status
        )
        try:
            space_id = execute_sql(sql, params, commit=True)
            logger.info(f"车位创建成功，ID: {space_id}")
            return cls.find_by_id(space_id) if space_id else None
        except Exception as e:
            logger.error(f"车位创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新车位信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_parking_space SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"车位更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"车位更新失败: {e}")
            raise
    
    def delete(self):
        """删除车位"""
        sql = "DELETE FROM t_parking_space WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"车位删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"车位删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'space_code': self.space_code,
            'space_name': self.space_name,
            'type': self.type,
            'status': self.status,
            'building_id': self.building_id,
            'location': self.location,
            'price': float(self.price) if self.price else None,
            'owner_id': self.owner_id,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class ParkingRecord:
    """停车记录模型"""
    
    def __init__(self, data=None):
        """初始化停车记录对象"""
        if data:
            self.id = data.get('id')
            self.space_id = data.get('space_id')
            self.user_id = data.get('user_id')
            self.car_number = data.get('car_number')
            self.entry_time = data.get('entry_time')
            self.exit_time = data.get('exit_time')
            self.duration = data.get('duration')
            self.fee = data.get('fee')
            self.payment_status = data.get('payment_status', 'unpaid')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, record_id):
        """根据ID查找停车记录"""
        sql = "SELECT * FROM t_parking_record WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (record_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有停车记录"""
        sql = "SELECT * FROM t_parking_record"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY entry_time DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找停车记录"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_parking_record{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_parking_record{where_clause} ORDER BY entry_time DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        records = [cls(item) for item in result]
        
        return records, total
    
    @classmethod
    def create(cls, space_id, car_number, user_id=None):
        """创建停车记录（车辆入场）"""
        sql = """
            INSERT INTO t_parking_record (
                space_id, user_id, car_number, entry_time, 
                payment_status, created_at, updated_at
            ) VALUES (%s, %s, %s, NOW(), 'unpaid', NOW(), NOW())
        """
        params = (space_id, user_id, car_number)
        try:
            record_id = execute_sql(sql, params, commit=True)
            logger.info(f"停车记录创建成功，ID: {record_id}")
            return cls.find_by_id(record_id) if record_id else None
        except Exception as e:
            logger.error(f"停车记录创建失败: {e}")
            raise
    
    def exit(self):
        """车辆出场"""
        if self.exit_time:
            return False
        
        exit_time = datetime.now()
        
        # 计算停车时长（分钟）
        duration = int((exit_time - self.entry_time).total_seconds() / 60)
        
        # 计算停车费用（每小时5元）
        fee = round(duration / 60 * 5, 2)
        
        # 更新记录
        sql = """
            UPDATE t_parking_record 
            SET exit_time = %s, duration = %s, fee = %s, updated_at = NOW()
            WHERE id = %s
        """
        params = (exit_time, duration, fee, self.id)
        
        try:
            affected = execute_sql(sql, params, commit=True)
            if affected > 0:
                self.exit_time = exit_time
                self.duration = duration
                self.fee = fee
                logger.info(f"车辆出场成功，停车时长: {duration}分钟，费用: {fee}元")
                return True
            return False
        except Exception as e:
            logger.error(f"车辆出场失败: {e}")
            raise
    
    def pay(self):
        """支付停车费用"""
        if self.payment_status == 'paid':
            return False
        
        sql = "UPDATE t_parking_record SET payment_status = 'paid', updated_at = NOW() WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            if affected > 0:
                self.payment_status = 'paid'
                logger.info(f"停车费用支付成功，ID: {self.id}")
                return True
            return False
        except Exception as e:
            logger.error(f"停车费用支付失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'space_id': self.space_id,
            'user_id': self.user_id,
            'car_number': self.car_number,
            'entry_time': str(self.entry_time) if self.entry_time else None,
            'exit_time': str(self.exit_time) if self.exit_time else None,
            'duration': self.duration,
            'fee': float(self.fee) if self.fee else None,
            'payment_status': self.payment_status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class Vehicle:
    """车辆信息模型"""
    
    def __init__(self, data=None):
        """初始化车辆对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.car_number = data.get('car_number')
            self.car_brand = data.get('car_brand')
            self.car_model = data.get('car_model')
            self.car_color = data.get('car_color')
            self.status = data.get('status', 'active')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, vehicle_id):
        """根据ID查找车辆"""
        sql = "SELECT * FROM t_vehicle WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (vehicle_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_car_number(cls, car_number):
        """根据车牌号查找车辆"""
        sql = "SELECT * FROM t_vehicle WHERE car_number = %s LIMIT 1"
        result = execute_sql(sql, (car_number,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有车辆"""
        sql = "SELECT * FROM t_vehicle"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找车辆"""
        offset = (page - 1) * page_size
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) FROM t_vehicle{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"SELECT * FROM t_vehicle{where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        vehicles = [cls(item) for item in result]
        
        return vehicles, total
    
    @classmethod
    def create(cls, user_id, car_number, car_brand=None, car_model=None, car_color=None, status='active'):
        """创建车辆"""
        sql = """
            INSERT INTO t_vehicle (
                user_id, car_number, car_brand, car_model, 
                car_color, status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (user_id, car_number, car_brand, car_model, car_color, status)
        try:
            vehicle_id = execute_sql(sql, params, commit=True)
            logger.info(f"车辆创建成功，ID: {vehicle_id}")
            return cls.find_by_id(vehicle_id) if vehicle_id else None
        except Exception as e:
            logger.error(f"车辆创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新车辆信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_vehicle SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"车辆更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"车辆更新失败: {e}")
            raise
    
    def delete(self):
        """删除车辆"""
        sql = "DELETE FROM t_vehicle WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"车辆删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"车辆删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'car_number': self.car_number,
            'car_brand': self.car_brand,
            'car_model': self.car_model,
            'car_color': self.car_color,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
