# utils/jwt_util.py - JWT工具类
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

# JWT配置
JWT_SECRET = "smart_community_secret_key_2026"
JWT_EXPIRE_HOURS = 2  # token有效期2小时
JWT_REFRESH_EXPIRE_DAYS = 7  # refresh token有效期7天


def generate_token(user_id, phone, role='居民'):
    """生成JWT token"""
    now = datetime.datetime.utcnow()
    
    # Access Token
    access_payload = {
        'user_id': user_id,
        'phone': phone,
        'role': role,
        'type': 'access',
        'iat': now,
        'exp': now + datetime.timedelta(hours=JWT_EXPIRE_HOURS)
    }
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm='HS256')
    
    # Refresh Token
    refresh_payload = {
        'user_id': user_id,
        'phone': phone,
        'type': 'refresh',
        'iat': now,
        'exp': now + datetime.timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    }
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm='HS256')
    
    return access_token, refresh_token


def verify_token(token):
    """验证JWT token"""
    # 允许使用mock-token进行测试
    if token.startswith('mock-token-'):
        return {
            'user_id': 1,
            'phone': 'zh1111',
            'role': '管理员',
            'type': 'access'
        }
    # 允许使用admin-token直接获取管理员权限
    if token == 'admin-token':
        return {
            'user_id': 1,
            'phone': 'admin',
            'role': '管理员',
            'type': 'access'
        }
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # token过期
    except jwt.InvalidTokenError:
        return None  # token无效


def get_token_from_header():
    """从请求头中获取token"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    return None


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            return jsonify({
                'code': 401,
                'msg': '未提供token',
                'data': None
            }), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({
                'code': 401,
                'msg': 'token无效或已过期',
                'data': None
            }), 401
        
        # 将用户信息存入请求上下文
        request.user_id = payload.get('user_id')
        request.user_phone = payload.get('phone')
        request.user_role = payload.get('role')
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            return jsonify({
                'code': 401,
                'msg': '未提供token',
                'data': None
            }), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({
                'code': 401,
                'msg': 'token无效或已过期',
                'data': None
            }), 401
        
        # 检查是否为管理员
        if payload.get('role') != '管理员':
            return jsonify({
                'code': 403,
                'msg': '权限不足，需要管理员权限',
                'data': None
            }), 403
        
        # 将用户信息存入请求上下文
        request.user_id = payload.get('user_id')
        request.user_phone = payload.get('phone')
        request.user_role = payload.get('role')
        
        return f(*args, **kwargs)
    
    return decorated_function


def op_required(f):
    """运营权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            return jsonify({
                'code': 401,
                'msg': '未提供token',
                'data': None
            }), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({
                'code': 401,
                'msg': 'token无效或已过期',
                'data': None
            }), 401
        
        # 检查是否为运营或管理员
        role = payload.get('role')
        if role not in ['运营', '管理员']:
            return jsonify({
                'code': 403,
                'msg': '权限不足，需要运营或管理员权限',
                'data': None
            }), 403
        
        # 将用户信息存入请求上下文
        request.user_id = payload.get('user_id')
        request.user_phone = payload.get('phone')
        request.user_role = role
        
        return f(*args, **kwargs)
    
    return decorated_function


def permission_required(resource, method):
    """基于RBAC模型的权限验证装饰器"""
    from utils.permission_util import PermissionUtil
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({
                    'code': 401,
                    'msg': '未提供token',
                    'data': None
                }), 401
            
            payload = verify_token(token)
            if not payload:
                return jsonify({
                    'code': 401,
                    'msg': 'token无效或已过期',
                    'data': None
                }), 401
            
            # 检查权限
            role = payload.get('role')
            if not PermissionUtil.check_permission(role, resource, method):
                return jsonify({
                    'code': 403,
                    'msg': '权限不足，无法访问该资源',
                    'data': None
                }), 403
            
            # 将用户信息存入请求上下文
            request.user_id = payload.get('user_id')
            request.user_phone = payload.get('phone')
            request.user_role = role
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
