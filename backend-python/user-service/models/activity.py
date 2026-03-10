import datetime
import logging
from config.database import get_db_connection, execute_sql

logger = logging.getLogger(__name__)

class Activity:
    """社区活动模型"""
    
    def __init__(self, data=None):
        """初始化活动对象"""
        if data:
            self.id = data.get('id')
            self.title = data.get('title')
            self.description = data.get('description')
            self.start_time = data.get('start_time')
            self.end_time = data.get('end_time')
            self.location = data.get('location')
            self.max_participants = data.get('max_participants')
            self.current_participants = data.get('current_participants', 0)
            self.status = data.get('status')  # draft, published, completed, cancelled
            self.image_url = data.get('image_url')
            self.organizer = data.get('organizer')
            self.contact_phone = data.get('contact_phone')
            self.category = data.get('category')
            self.tags = data.get('tags')
            self.remark = data.get('remark')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def create(cls, title, description, start_time, end_time, location, 
               max_participants, organizer, contact_phone, category, tags=None, 
               image_url=None, remark=None):
        """创建活动"""
        # 转换时间格式为MySQL支持的格式
        import datetime
        from dateutil import parser as date_parser
        
        def parse_time(value):
            """解析多种时间格式"""
            if not value:
                return None
            if isinstance(value, str):
                # 无论什么格式，直接用dateutil解析
                return date_parser.parse(value).strftime('%Y-%m-%d %H:%M:%S')
            return value
        
        try:
            start_time = parse_time(start_time)
            end_time = parse_time(end_time)
        except Exception as e:
            logger.error(f"时间格式转换失败: {e}")
            raise
        
        sql = """
            INSERT INTO t_activity (
                title, description, start_time, end_time, location, 
                max_participants, status, organizer, contact_phone, category, 
                tags, image_url, remark, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, 'draft', %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        params = (title, description, start_time, end_time, location, 
                  max_participants, organizer, contact_phone, category, 
                  tags, image_url, remark)
        try:
            activity_id = execute_sql(sql, params, commit=True)
            logger.info(f"活动创建成功，ID: {activity_id}")
            return cls.find_by_id(activity_id) if activity_id else None
        except Exception as e:
            logger.error(f"活动创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, activity_id):
        """根据ID查询活动"""
        sql = "SELECT * FROM t_activity WHERE id = %s"
        try:
            result = execute_sql(sql, (activity_id,))
            if result and len(result) > 0:
                return cls(result[0])
            return None
        except Exception as e:
            logger.error(f"查询活动失败: {e}")
            return None
    
    @classmethod
    def find_with_pagination(cls, conditions=None, params=None, page=1, page_size=20):
        """分页查询活动"""
        base_sql = "SELECT * FROM t_activity"
        
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        count_sql = f"SELECT COUNT(*) as total FROM t_activity {where_clause}"
        
        offset = (page - 1) * page_size
        query_params = list(params) if params else []
        query_params.extend([page_size, offset])
        query_sql = f"{base_sql} {where_clause} ORDER BY created_at DESC LIMIT %s OFFSET %s"
        
        try:
            # 获取总数
            count_result = execute_sql(count_sql, params)
            total = count_result[0]['total'] if count_result and len(count_result) > 0 else 0
            
            # 获取分页数据
            results = execute_sql(query_sql, tuple(query_params))
            
            activities = [cls(result) for result in results]
            return activities, total
        except Exception as e:
            logger.error(f"分页查询活动失败: {e}")
            return [], 0
    
    def update(self, **kwargs):
        """更新活动信息"""
        set_clause = []
        params = []
        
        # 转换时间格式为MySQL支持的格式
        import datetime
        from dateutil import parser as date_parser
        
        for key, value in kwargs.items():
            # 跳过id、created_at、updated_at字段和空值字段
            if key in ['id', 'created_at', 'updated_at'] or value is None:
                continue
            # 处理时间字段
            if key in ['start_time', 'end_time']:
                try:
                    # 无论什么格式，直接用dateutil解析
                    if isinstance(value, str):
                        value = date_parser.parse(value).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    logger.error(f"时间格式转换失败，key={key}, value={value}, error={e}")
                    raise
            set_clause.append(f"{key} = %s")
            params.append(value)
        
        if not set_clause:
            logger.warning(f"没有需要更新的字段，活动ID: {self.id}")
            return True
        
        set_clause.append("updated_at = NOW()")
        
        sql = f"UPDATE t_activity SET {', '.join(set_clause)} WHERE id = %s"
        params.append(self.id)
        
        try:
            rows_affected = execute_sql(sql, params, commit=True)
            logger.info(f"活动更新成功，ID: {self.id}, 影响行数: {rows_affected}")
            return True
        except Exception as e:
            logger.error(f"活动更新失败: {e}")
            return False
    
    def publish(self):
        """发布活动"""
        return self.update(status='published')
    
    def cancel(self):
        """取消活动"""
        return self.update(status='cancelled')
    
    def complete(self):
        """完成活动"""
        return self.update(status='completed')
    
    def delete(self):
        """删除活动"""
        sql = "DELETE FROM t_activity WHERE id = %s"
        try:
            rows_affected = execute_sql(sql, (self.id,), commit=True)
            logger.info(f"活动删除成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"活动删除失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'status': self.status,
            'image_url': self.image_url,
            'organizer': self.organizer,
            'contact_phone': self.contact_phone,
            'category': self.category,
            'tags': self.tags,
            'remark': self.remark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class ActivityParticipant:
    """活动参与者模型"""
    
    def __init__(self, data=None):
        """初始化参与者对象"""
        if data:
            self.id = data.get('id')
            self.activity_id = data.get('activity_id')
            self.user_id = data.get('user_id')
            self.user_name = data.get('user_name')
            self.user_phone = data.get('user_phone')
            self.sign_in_status = data.get('sign_in_status', 'not_signed')  # not_signed, signed
            self.sign_in_time = data.get('sign_in_time')
            self.remark = data.get('remark')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @classmethod
    def create(cls, activity_id, user_id, user_name, user_phone, remark=None):
        """创建参与者记录"""
        sql = """
            INSERT INTO t_activity_participant (
                activity_id, user_id, user_name, user_phone, sign_in_status, 
                remark, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, 'not_signed', %s, NOW(), NOW())
        """
        params = (activity_id, user_id, user_name, user_phone, remark)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            participant_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"参与者记录创建成功，ID: {participant_id}")
            return cls.find_by_id(participant_id) if participant_id else None
        except Exception as e:
            logger.error(f"参与者记录创建失败: {e}")
            raise
    
    @classmethod
    def find_by_id(cls, participant_id):
        """根据ID查询参与者"""
        sql = "SELECT * FROM t_activity_participant WHERE id = %s"
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (participant_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return cls(result) if result else None
        except Exception as e:
            logger.error(f"查询参与者失败: {e}")
            return None
    
    @classmethod
    def find_by_activity(cls, activity_id):
        """查询活动的参与者"""
        sql = """
            SELECT ap.*, u.nickname as user_name, u.phone as user_phone 
            FROM t_activity_participant ap
            LEFT JOIN t_user u ON ap.user_id = u.id
            WHERE ap.activity_id = %s
            ORDER BY ap.created_at DESC
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (activity_id,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [cls(result) for result in results]
        except Exception as e:
            logger.error(f"查询活动参与者失败: {e}")
            return []
    
    @classmethod
    def find_by_user(cls, user_id):
        """查询用户参与的活动"""
        sql = """
            SELECT ap.*, a.title, a.start_time, a.end_time, a.location, a.status 
            FROM t_activity_participant ap
            LEFT JOIN t_activity a ON ap.activity_id = a.id
            WHERE ap.user_id = %s
            ORDER BY a.start_time DESC
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return [cls(result) for result in results]
        except Exception as e:
            logger.error(f"查询用户参与的活动失败: {e}")
            return []
    
    def sign_in(self):
        """签到"""
        sql = """
            UPDATE t_activity_participant 
            SET sign_in_status = 'signed', sign_in_time = NOW(), updated_at = NOW()
            WHERE id = %s
        """
        params = (self.id,)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"参与者签到成功，ID: {self.id}")
            return rows_affected > 0
        except Exception as e:
            logger.error(f"参与者签到失败: {e}")
            return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'sign_in_status': self.sign_in_status,
            'sign_in_time': self.sign_in_time,
            'remark': self.remark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class ActivityStatistics:
    """活动统计模型"""
    
    @classmethod
    def get_activity_statistics(cls, activity_id):
        """获取活动统计数据"""
        sql = """
            SELECT 
                COUNT(*) as total_participants,
                SUM(CASE WHEN sign_in_status = 'signed' THEN 1 ELSE 0 END) as signed_participants
            FROM t_activity_participant
            WHERE activity_id = %s
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (activity_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"获取活动统计数据失败: {e}")
            return {'total_participants': 0, 'signed_participants': 0}
    
    @classmethod
    def get_overall_statistics(cls, start_date=None, end_date=None):
        """获取整体活动统计"""
        sql = """
            SELECT 
                COUNT(*) as total_activities,
                SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published_activities,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_activities,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_activities
            FROM t_activity
        """
        
        params = []
        if start_date:
            sql += " WHERE created_at >= %s"
            params.append(start_date)
            if end_date:
                sql += " AND created_at <= %s"
                params.append(end_date)
        elif end_date:
            sql += " WHERE created_at <= %s"
            params.append(end_date)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"获取整体活动统计失败: {e}")
            return {
                'total_activities': 0,
                'published_activities': 0,
                'completed_activities': 0,
                'cancelled_activities': 0
            }
