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
            # 将JSON字符串转换为Python列表
            import json
            try:
                self.images = json.loads(data.get('images', '[]'))
            except:
                self.images = []
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
        import json
        # 将images列表转换为JSON字符串
        images_json = json.dumps(images) if images else '[]'
        
        # 自动匹配维修师傅
        technician_id = cls._auto_assign_technician(type)
        
        # 根据是否匹配到维修师傅设置状态
        status = 'processing' if technician_id else 'pending'
        
        # 构建SQL语句和参数
        if technician_id:
            sql = """
                INSERT INTO t_repair_order (
                    user_id, title, type, description, address, images, 
                    priority, status, technician_id, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (user_id, title, type, description, address, images_json, priority, status, technician_id)
        else:
            sql = """
                INSERT INTO t_repair_order (
                    user_id, title, type, description, address, images, 
                    priority, status, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            params = (user_id, title, type, description, address, images_json, priority, status)
        
        try:
            order_id = execute_sql(sql, params, commit=True)
            logger.info(f"维修工单创建成功，ID: {order_id}，自动分配维修师傅: {technician_id}")
            return cls.find_by_id(order_id) if order_id else None
        except Exception as e:
            logger.error(f"维修工单创建失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    @classmethod
    def _auto_assign_technician(cls, repair_type):
        """自动分配维修师傅"""
        try:
            # 1. 获取所有活跃的维修师傅
            from models.repair import Technician
            # 尝试获取状态为 'active' 的维修师傅
            active_technicians = Technician.find_all(conditions=["status = %s"], params=['active'])
            
            # 如果没有，尝试获取状态为 'online' 的维修师傅
            if not active_technicians:
                active_technicians = Technician.find_all(conditions=["status = %s"], params=['online'])
                logger.info("使用状态为 'online' 的维修师傅")
            
            if not active_technicians:
                logger.info("没有活跃的维修师傅")
                return None
            
            logger.info(f"维修类型: {repair_type}, 活跃维修师傅数量: {len(active_technicians)}")
            
            # 2. 根据维修类型和专业技能匹配
            matched_technicians = []
            for tech in active_technicians:
                logger.info(f"检查维修师傅: {tech.name}, 专业技能: {tech.specialty}")
                # 更灵活的匹配逻辑
                if tech.specialty:
                    # 特殊匹配：水暖 -> 水电维修, 管道工, 水管, 水电
                    if repair_type == 'water' and ('水电' in tech.specialty or '管道' in tech.specialty or '水' in tech.specialty):
                        matched_technicians.append(tech)
                    # 特殊匹配：电路 -> 电工, 电
                    elif repair_type == 'electric' and ('电工' in tech.specialty or '电' in tech.specialty):
                        matched_technicians.append(tech)
                    # 特殊匹配：燃气 -> 燃气, 煤气
                    elif repair_type == 'gas' and ('燃气' in tech.specialty or '煤气' in tech.specialty):
                        matched_technicians.append(tech)
                    # 特殊匹配：门窗 -> 门窗, 木工
                    elif repair_type == 'door' and ('门窗' in tech.specialty or '木工' in tech.specialty):
                        matched_technicians.append(tech)
                    # 特殊匹配：电梯 -> 电梯
                    elif repair_type == 'elevator' and '电梯' in tech.specialty:
                        matched_technicians.append(tech)
                    # 特殊匹配：保洁 -> 保洁, 清洁
                    elif repair_type == 'cleaning' and ('保洁' in tech.specialty or '清洁' in tech.specialty):
                        matched_technicians.append(tech)
                    # 特殊匹配：其他 -> 其他
                    elif repair_type == 'other':
                        matched_technicians.append(tech)
            
            logger.info(f"匹配到的维修师傅数量: {len(matched_technicians)}")
            
            # 如果没有精确匹配，使用所有活跃的维修师傅
            if not matched_technicians:
                matched_technicians = active_technicians
                logger.info("没有精确匹配，使用所有活跃的维修师傅")
            
            # 3. 选择当前 workload 最小的维修师傅
            best_technician = None
            min_workload = float('inf')
            
            for tech in matched_technicians:
                # 计算当前维修师傅的 workload（正在处理的工单数量）
                workload_sql = "SELECT COUNT(*) FROM t_repair_order WHERE technician_id = %s AND status = 'processing'"
                workload_result = execute_sql(workload_sql, (tech.id,))
                workload = workload_result[0]['COUNT(*)'] if workload_result else 0
                logger.info(f"维修师傅: {tech.name}, 正在处理的工单数量: {workload}")
                
                if workload < min_workload:
                    min_workload = workload
                    best_technician = tech
            
            if best_technician:
                logger.info(f"自动分配维修师傅: {best_technician.name} (ID: {best_technician.id})")
                return best_technician.id
            else:
                logger.info("没有可用的维修师傅")
                return None
                
        except Exception as e:
            logger.error(f"自动分配维修师傅失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
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
        # 获取维修师傅信息
        handler_name = None
        if self.technician_id:
            from models.repair import Technician
            technician = Technician.find_by_id(self.technician_id)
            if technician:
                handler_name = technician.name
        
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
            'handler_name': handler_name,
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
