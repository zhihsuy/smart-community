# models/user.py - 用户模型和数据操作
import bcrypt
import json
from datetime import datetime
from config.database import execute_sql, logger

class User:
    """用户模型类"""
    
    def __init__(self, data=None):
        """初始化用户对象"""
        if data:
            self.id = data.get('id')
            self.phone = data.get('phone')
            self.password = data.get('password')
            self.nickname = data.get('nickname')
            self.avatar = data.get('avatar')
            self.real_name = data.get('real_name')
            self.id_card = data.get('id_card')
            self.gender = data.get('gender', 0)
            self.birthday = data.get('birthday')
            self.email = data.get('email')
            self.community_id = data.get('community_id')
            self.building_id = data.get('building_id')
            self.unit = data.get('unit')
            self.room_number = data.get('room_number')
            self.platform_type = data.get('platform_type', 'pc')
            self.device_id = data.get('device_id')
            self.interest_tags = data.get('interest_tags')
            self.family_structure = data.get('family_structure')
            self.consumption_level = data.get('consumption_level', 2)
            self.status = data.get('status', 1)
            self.is_verified = data.get('is_verified', 0)
            self.role = data.get('role', '居民')
            self.last_login_time = data.get('last_login_time')
            self.last_login_ip = data.get('last_login_ip')
            self.created_at = data.get('created_at')
            self.updated_at = data.get('updated_at')
    
    @staticmethod
    def hash_password(password):
        """密码加密"""
        salt = bcrypt.gensalt(rounds=10)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @classmethod
    def find_by_phone(cls, phone):
        """根据手机号查找用户"""
        sql = "SELECT * FROM t_user WHERE phone = %s LIMIT 1"
        result = execute_sql(sql, (phone,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_id(cls, user_id):
        """根据ID查找用户"""
        sql = "SELECT * FROM t_user WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (user_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def create(cls, phone, password, nickname=None, **kwargs):
        """创建新用户"""
        hashed_password = cls.hash_password(password)
        
        sql = """
            INSERT INTO t_user (phone, password, nickname, email, gender, 
                               building_id, unit, room_number, family_structure,
                               interest_tags, status, role, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        interest_tags = kwargs.get('interest_tags', [])
        if isinstance(interest_tags, list):
            interest_tags = json.dumps(interest_tags, ensure_ascii=False)
        
        params = (
            phone,
            hashed_password,
            nickname or phone,
            kwargs.get('email'),
            kwargs.get('gender', 0),
            kwargs.get('building_id'),
            kwargs.get('unit'),
            kwargs.get('room_number'),
            kwargs.get('family_structure'),
            interest_tags,
            kwargs.get('status', 1),
            kwargs.get('role', '居民')
        )
        
        try:
            user_id = execute_sql(sql, params, commit=True)
            logger.info(f"用户创建成功，ID: {user_id}")
            return cls.find_by_id(user_id) if user_id else None
        except Exception as e:
            logger.error(f"用户创建失败: {e}")
            raise
    
    def update(self, **kwargs):
        """更新用户信息"""
        allowed_fields = ['nickname', 'avatar', 'email', 'gender', 
                         'building_id', 'unit', 'room_number', 
                         'family_structure', 'interest_tags', 'role']
        
        updates = []
        params = []
        
        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = %s")
                value = kwargs[field]
                if field == 'interest_tags' and isinstance(value, list):
                    value = json.dumps(value, ensure_ascii=False)
                params.append(value)
        
        if not updates:
            return False
        
        params.append(self.id)
        sql = f"UPDATE t_user SET {', '.join(updates)} WHERE id = %s"
        
        try:
            affected = execute_sql(sql, tuple(params), commit=True)
            logger.info(f"用户更新成功，影响行数: {affected}")
            return affected > 0
        except Exception as e:
            logger.error(f"用户更新失败: {e}")
            raise
    
    def update_password(self, new_password):
        """更新密码"""
        hashed = self.hash_password(new_password)
        sql = "UPDATE t_user SET password = %s WHERE id = %s"
        
        try:
            affected = execute_sql(sql, (hashed, self.id), commit=True)
            logger.info(f"密码更新成功")
            return affected > 0
        except Exception as e:
            logger.error(f"密码更新失败: {e}")
            raise
    
    def update_login_info(self, ip=None):
        """更新登录信息"""
        sql = "UPDATE t_user SET last_login_time = NOW(), last_login_ip = %s WHERE id = %s"
        try:
            execute_sql(sql, (ip, self.id), commit=True)
        except Exception as e:
            logger.error(f"登录信息更新失败: {e}")
    
    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        # 处理头像URL，确保返回完整的URL
        avatar_url = self.avatar
        if avatar_url and not avatar_url.startswith('http'):
            # 如果头像URL不是完整的URL，添加基础URL
            avatar_url = f"http://localhost:8081{avatar_url}"
        
        data = {
            'id': self.id,
            'phone': self.phone,
            'nickname': self.nickname,
            'avatar': avatar_url,
            'real_name': self.real_name,
            'gender': self.gender,
            'birthday': str(self.birthday) if self.birthday else None,
            'email': self.email,
            'community_id': self.community_id,
            'building_id': self.building_id,
            'unit': self.unit,
            'room_number': self.room_number,
            'family_structure': self.family_structure,
            'interest_tags': self.interest_tags,
            'status': self.status,
            'is_verified': self.is_verified,
            'role': self.role,
            'last_login_time': str(self.last_login_time) if self.last_login_time else None,
            'created_at': str(self.created_at) if self.created_at else None
        }
        
        if include_sensitive:
            data['password'] = self.password
        
        # 解析JSON字段
        if data['interest_tags'] and isinstance(data['interest_tags'], str):
            try:
                data['interest_tags'] = json.loads(data['interest_tags'])
            except:
                data['interest_tags'] = []
        
        return data
    
    @classmethod
    def list_all(cls, page=1, page_size=20, **filters):
        """获取用户列表"""
        where_clause = "WHERE 1=1"
        params = []
        
        if 'status' in filters:
            where_clause += " AND status = %s"
            params.append(filters['status'])
        
        if 'phone' in filters:
            where_clause += " AND phone LIKE %s"
            params.append(f"%{filters['phone']}%")
        
        # 获取总数
        count_sql = f"SELECT COUNT(*) as total FROM t_user {where_clause}"
        count_result = execute_sql(count_sql, tuple(params))
        total = count_result[0]['total'] if count_result else 0
        
        # 获取列表
        offset = (page - 1) * page_size
        sql = f"""
            SELECT * FROM t_user 
            {where_clause} 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        
        result = execute_sql(sql, tuple(params))
        users = [cls(row).to_dict() for row in result] if result else []
        
        return {
            'list': users,
            'total': total,
            'page': page,
            'page_size': page_size
        }
