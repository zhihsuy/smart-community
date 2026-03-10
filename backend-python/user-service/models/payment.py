# models/payment.py - 缴费管理模型
from config.database import execute_sql, logger
from datetime import datetime


class Payment:
    """缴费记录模型"""
    
    def __init__(self, data=None):
        """初始化缴费记录对象"""
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.user_phone = data.get('user_phone')
            self.building_id = data.get('building_id')
            self.building_name = data.get('building_name')
            self.room_number = data.get('room_number')
            self.type = data.get('type')
            self.fee_type = data.get('fee_type')
            self.amount = data.get('amount')
            self.period_start = data.get('period_start')
            self.period_end = data.get('period_end')
            self.due_date = data.get('due_date')
            self.paid_amount = data.get('paid_amount', 0)
            self.paid_time = data.get('paid_time')
            self.status = data.get('status', 'unpaid')
            self.payment_method = data.get('payment_method')
            self.transaction_id = data.get('transaction_id')
            self.remark = data.get('remark')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, payment_id):
        """根据ID查找缴费记录"""
        sql = """
            SELECT p.*, u.nickname as user_name, u.phone as user_phone,
                   b.name as building_name
            FROM t_payment p
            LEFT JOIN t_user u ON p.user_id = u.id
            LEFT JOIN t_building b ON p.building_id = b.id
            WHERE p.id = %s LIMIT 1
        """
        result = execute_sql(sql, (payment_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, conditions=None, params=None):
        """查找所有缴费记录"""
        sql = """
            SELECT p.*, u.nickname as user_name, u.phone as user_phone,
                   b.name as building_name
            FROM t_payment p
            LEFT JOIN t_user u ON p.user_id = u.id
            LEFT JOIN t_building b ON p.building_id = b.id
        """
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY p.created_at DESC"
        result = execute_sql(sql, params or ())
        return [cls(item) for item in result]
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=10):
        """分页查找缴费记录"""
        offset = (page - 1) * page_size
        
        base_sql = """
            FROM t_payment p
            LEFT JOIN t_user u ON p.user_id = u.id
            LEFT JOIN t_building b ON p.building_id = b.id
        """
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) {base_sql}{where_clause}"
        count_result = execute_sql(count_sql, params or ())
        total = count_result[0]['COUNT(*)'] if count_result else 0
        
        data_sql = f"""
            SELECT p.*, u.nickname as user_name, u.phone as user_phone,
                   b.name as building_name
            {base_sql}{where_clause}
            ORDER BY p.created_at DESC
            LIMIT %s OFFSET %s
        """
        data_params = (page_size, offset)
        if params:
            data_params = tuple(params) + data_params
        
        result = execute_sql(data_sql, data_params)
        payments = [cls(item) for item in result]
        
        return payments, total
    
    @classmethod
    def create(cls, user_id, building_id, type, fee_type, amount, period_start, period_end, due_date, remark=None):
        """创建缴费记录"""
        sql = """
            INSERT INTO t_payment (
                user_id, building_id, type, fee_type, amount, period_start, period_end, due_date,
                status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'unpaid', NOW(), NOW())
        """
        params = (user_id, building_id, type, fee_type, amount, period_start, period_end, due_date)
        try:
            payment_id = execute_sql(sql, params, commit=True)
            logger.info(f"缴费记录创建成功，ID: {payment_id}")
            return cls.find_by_id(payment_id) if payment_id else None
        except Exception as e:
            logger.error(f"缴费记录创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新缴费记录信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_payment SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"缴费记录更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"缴费记录更新失败: {e}")
            raise
    
    def delete(self):
        """删除缴费记录"""
        sql = "DELETE FROM t_payment WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"缴费记录删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"缴费记录删除失败: {e}")
            raise
    
    def pay(self, paid_amount, payment_method, transaction_id=None):
        """缴费"""
        return self.update(
            paid_amount=paid_amount,
            paid_time=datetime.now(),
            payment_method=payment_method,
            transaction_id=transaction_id,
            status='paid'
        )
    
    @classmethod
    def get_statistics(cls):
        """获取缴费统计"""
        sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'unpaid' THEN 1 ELSE 0 END) as unpaid,
                SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) as paid,
                SUM(CASE WHEN status = 'overdue' THEN 1 ELSE 0 END) as overdue,
                SUM(amount) as total_amount,
                SUM(CASE WHEN status = 'paid' THEN paid_amount ELSE 0 END) as paid_amount,
                SUM(CASE WHEN status = 'unpaid' THEN amount ELSE 0 END) as unpaid_amount
            FROM t_payment
        """
        result = execute_sql(sql)
        if result and len(result) > 0:
            stats = result[0]
            return {
                'total': stats['total'] or 0,
                'unpaid': stats['unpaid'] or 0,
                'paid': stats['paid'] or 0,
                'overdue': stats['overdue'] or 0,
                'total_amount': float(stats['total_amount'] or 0),
                'paid_amount': float(stats['paid_amount'] or 0),
                'unpaid_amount': float(stats['unpaid_amount'] or 0)
            }
        return {
            'total': 0,
            'unpaid': 0,
            'paid': 0,
            'overdue': 0,
            'total_amount': 0,
            'paid_amount': 0,
            'unpaid_amount': 0
        }
    
    @classmethod
    def get_statistics_by_type(cls):
        """按类型获取缴费统计"""
        sql = """
            SELECT 
                type,
                COUNT(*) as count,
                SUM(amount) as total_amount,
                SUM(CASE WHEN status = 'paid' THEN paid_amount ELSE 0 END) as paid_amount
            FROM t_payment
            GROUP BY type
        """
        result = execute_sql(sql)
        return [
            {
                'type': item['type'],
                'count': item['count'] or 0,
                'total_amount': float(item['total_amount'] or 0),
                'paid_amount': float(item['paid_amount'] or 0)
            }
            for item in result
        ]
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'building_id': self.building_id,
            'building_name': self.building_name,
            'room_number': self.room_number,
            'type': self.type,
            'fee_type': self.fee_type,
            'amount': float(self.amount) if self.amount else 0,
            'period_start': str(self.period_start) if self.period_start else None,
            'period_end': str(self.period_end) if self.period_end else None,
            'due_date': str(self.due_date) if self.due_date else None,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'paid_time': str(self.paid_time) if self.paid_time else None,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'remark': self.remark,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }


class FeeType:
    """费用类型模型"""
    
    def __init__(self, data=None):
        """初始化费用类型对象"""
        if data:
            self.id = data.get('id')
            self.name = data.get('name')
            self.code = data.get('code')
            self.type = data.get('type')
            self.unit_price = data.get('unit_price')
            self.unit = data.get('unit')
            self.description = data.get('description')
            self.status = data.get('status', 'active')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def find_by_id(cls, fee_type_id):
        """根据ID查找费用类型"""
        sql = "SELECT * FROM t_fee_type WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (fee_type_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_all(cls, type=None, status='active'):
        """查找所有费用类型"""
        sql = "SELECT * FROM t_fee_type WHERE status = %s"
        params = [status]
        if type:
            sql += " AND type = %s"
            params.append(type)
        sql += " ORDER BY created_at DESC"
        result = execute_sql(sql, tuple(params))
        return [cls(item) for item in result]
    
    @classmethod
    def create(cls, name, code, type, unit_price, unit, description=None):
        """创建费用类型"""
        sql = """
            INSERT INTO t_fee_type (name, code, type, unit_price, unit, description, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, 'active', NOW(), NOW())
        """
        params = (name, code, type, unit_price, unit, description)
        try:
            fee_type_id = execute_sql(sql, params, commit=True)
            logger.info(f"费用类型创建成功，ID: {fee_type_id}")
            return cls.find_by_id(fee_type_id) if fee_type_id else None
        except Exception as e:
            logger.error(f"费用类型创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新费用类型信息"""
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = NOW()")
        sql = f"UPDATE t_fee_type SET {', '.join(updates)} WHERE id = %s"
        params.append(self.id)
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"费用类型更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"费用类型更新失败: {e}")
            raise
    
    def delete(self):
        """删除费用类型"""
        sql = "DELETE FROM t_fee_type WHERE id = %s"
        try:
            affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"费用类型删除成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"费用类型删除失败: {e}")
            raise
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.type,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'unit': self.unit,
            'description': self.description,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
