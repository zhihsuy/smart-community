# routes/auth.py - 认证相关路由
from flask import Blueprint, request, jsonify
from models.user import User
from utils.jwt_util import generate_token, verify_token
from config.database import logger
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/<platform_type>/auth')


def validate_phone(phone):
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_password(password):
    """验证密码格式"""
    return len(password) >= 6 and len(password) <= 20


@auth_bp.route('/register', methods=['POST'])
def register(platform_type):
    """用户注册"""
    try:
        data = request.get_json()
        
        # 参数验证
        phone = data.get('phone')
        password = data.get('password')
        code = data.get('code')
        
        if not phone or not password:
            return jsonify({
                'code': 400,
                'msg': '手机号和密码不能为空',
                'data': None
            })
        
        if not validate_phone(phone):
            return jsonify({
                'code': 400,
                'msg': '手机号格式不正确',
                'data': None
            })
        
        if not validate_password(password):
            return jsonify({
                'code': 400,
                'msg': '密码长度应在6-20个字符之间',
                'data': None
            })
        
        # 检查手机号是否已注册
        existing_user = User.find_by_phone(phone)
        if existing_user:
            return jsonify({
                'code': 400,
                'msg': '该手机号已注册',
                'data': None
            })
        
        # TODO: 验证短信验证码
        # 这里暂时跳过验证码验证
        
        # 创建用户
        user = User.create(
            phone=phone,
            password=password,
            nickname=data.get('nickname', phone),
            platform_type=platform_type,
            role=data.get('role', '居民')
        )
        
        if user:
            logger.info(f"用户注册成功: {phone}")
            return jsonify({
                'code': 0,
                'msg': '注册成功',
                'data': {
                    'userId': user.id,
                    'phone': user.phone
                }
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '注册失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"注册失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'注册失败: {str(e)}',
            'data': None
        })


@auth_bp.route('/login', methods=['POST'])
def login(platform_type):
    """用户登录"""
    try:
        data = request.get_json()
        
        # 参数验证
        phone = data.get('phone')
        password = data.get('password')
        verification_code = data.get('verificationCode')
        
        if not phone:
            return jsonify({
                'code': 400,
                'msg': '手机号不能为空',
                'data': None
            })
        
        # 查找用户
        user = User.find_by_phone(phone)
        if not user:
            return jsonify({
                'code': 400,
                'msg': '用户不存在',
                'data': None
            })
        
        # 验证密码或验证码
        if password:
            # 密码登录
            if not User.verify_password(password, user.password):
                return jsonify({
                    'code': 400,
                    'msg': '密码错误',
                    'data': None
                })
        elif verification_code:
            # 验证码登录（TODO: 实现验证码验证）
            # 暂时跳过验证
            pass
        else:
            return jsonify({
                'code': 400,
                'msg': '请提供密码或验证码',
                'data': None
            })
        
        # 检查用户状态
        if user.status == 0:
            return jsonify({
                'code': 403,
                'msg': '账号已被禁用',
                'data': None
            })
        
        # 更新登录信息
        ip = request.remote_addr
        user.update_login_info(ip)
        
        # 生成token，使用用户的实际角色
        access_token, refresh_token = generate_token(
            user_id=user.id,
            phone=user.phone,
            role=user.role or '居民'  # 使用用户的角色，默认为居民
        )
        
        logger.info(f"用户登录成功: {phone}")
        
        return jsonify({
            'code': 0,
            'msg': '登录成功',
            'data': {
                'token': access_token,
                'refreshToken': refresh_token,
                'userInfo': user.to_dict()
            }
        })
    
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'登录失败: {str(e)}',
            'data': None
        })


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token(platform_type):
    """刷新token"""
    try:
        data = request.get_json()
        refresh_token = data.get('refreshToken')
        
        if not refresh_token:
            return jsonify({
                'code': 400,
                'msg': 'refreshToken不能为空',
                'data': None
            })
        
        # 验证refresh token
        payload = verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return jsonify({
                'code': 401,
                'msg': 'refreshToken无效或已过期',
                'data': None
            })
        
        # 生成新的token
        access_token, new_refresh_token = generate_token(
            user_id=payload.get('user_id'),
            phone=payload.get('phone'),
            role=payload.get('role')
        )
        
        return jsonify({
            'code': 0,
            'msg': '刷新成功',
            'data': {
                'token': access_token,
                'refreshToken': new_refresh_token
            }
        })
    
    except Exception as e:
        logger.error(f"刷新token失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'刷新失败: {str(e)}',
            'data': None
        })


@auth_bp.route('/send-code', methods=['POST'])
def send_code(platform_type):
    """发送验证码"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone or not validate_phone(phone):
            return jsonify({
                'code': 400,
                'msg': '手机号格式不正确',
                'data': None
            })
        
        # TODO: 实现真实的短信验证码发送
        # 这里返回模拟成功
        logger.info(f"发送验证码到: {phone}")
        
        return jsonify({
            'code': 0,
            'msg': '验证码发送成功',
            'data': None
        })
    
    except Exception as e:
        logger.error(f"发送验证码失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'发送失败: {str(e)}',
            'data': None
        })
