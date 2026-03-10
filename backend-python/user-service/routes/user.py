# routes/user.py - 用户管理路由
from flask import Blueprint, request, jsonify
from models.user import User
from models.building import Building
from utils.jwt_util import login_required, admin_required, op_required
from config.database import logger
import json

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/<platform_type>/user')


@user_bp.route('/info', methods=['GET'])
@login_required
def get_user_info(platform_type):
    """获取当前用户信息"""
    try:
        user_id = request.user_id
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': user.to_dict()
        })
    
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@user_bp.route('/update', methods=['PUT'])
@login_required
def update_user_info(platform_type):
    """更新用户信息"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        # 更新用户信息
        success = user.update(**data)
        
        if success:
            # 重新获取更新后的用户信息
            updated_user = User.find_by_id(user_id)
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': updated_user.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败，没有数据被修改',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@user_bp.route('/interest-tags', methods=['PUT'])
@login_required
def update_interest_tags(platform_type):
    """更新兴趣标签"""
    try:
        user_id = request.user_id
        data = request.get_json()
        interest_tags = data.get('interestTags')
        
        if interest_tags is None:
            return jsonify({
                'code': 400,
                'msg': '兴趣标签不能为空',
                'data': None
            })
        
        # 解析JSON字符串
        if isinstance(interest_tags, str):
            try:
                interest_tags = json.loads(interest_tags)
            except:
                interest_tags = []
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        success = user.update(interest_tags=interest_tags)
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': {
                    'userId': user.id
                }
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"更新兴趣标签失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@user_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password(platform_type):
    """修改密码"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        
        if not old_password or not new_password:
            return jsonify({
                'code': 400,
                'msg': '原密码和新密码不能为空',
                'data': None
            })
        
        if len(new_password) < 6 or len(new_password) > 20:
            return jsonify({
                'code': 400,
                'msg': '新密码长度应在6-20个字符之间',
                'data': None
            })
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        # 验证原密码
        if not User.verify_password(old_password, user.password):
            return jsonify({
                'code': 400,
                'msg': '原密码错误',
                'data': None
            })
        
        # 更新密码
        success = user.update_password(new_password)
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '密码修改成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '密码修改失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"修改密码失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'修改失败: {str(e)}',
            'data': None
        })


@user_bp.route('/change-phone', methods=['POST'])
@login_required
def change_phone(platform_type):
    """更换手机号"""
    try:
        user_id = request.user_id
        data = request.get_json()
        
        new_phone = data.get('newPhone')
        code = data.get('code')
        
        if not new_phone or not code:
            return jsonify({
                'code': 400,
                'msg': '新手机号和验证码不能为空',
                'data': None
            })
        
        # TODO: 验证验证码
        
        # 检查新手机号是否已被使用
        existing_user = User.find_by_phone(new_phone)
        if existing_user and existing_user.id != user_id:
            return jsonify({
                'code': 400,
                'msg': '该手机号已被其他用户使用',
                'data': None
            })
        
        # TODO: 实现更换手机号逻辑
        # 这里需要更新数据库中的手机号
        
        return jsonify({
            'code': 0,
            'msg': '手机号更换成功',
            'data': None
        })
    
    except Exception as e:
        logger.error(f"更换手机号失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更换失败: {str(e)}',
            'data': None
        })


@user_bp.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar(platform_type):
    """上传头像"""
    try:
        user_id = request.user_id
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'msg': '请选择要上传的文件',
                'data': None
            })
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({
                'code': 400,
                'msg': '请选择要上传的文件',
                'data': None
            })
        
        # 检查文件类型
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({
                'code': 400,
                'msg': '只支持上传图片文件',
                'data': None
            })
        
        # 检查文件大小
        if file.content_length > 2 * 1024 * 1024:  # 2MB
            return jsonify({
                'code': 400,
                'msg': '图片大小不能超过2MB',
                'data': None
            })
        
        # 创建上传目录
        import os
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'avatars')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
        
        # 生成文件名
        import uuid
        ext = os.path.splitext(file.filename)[1]
        filename = f"{user_id}_{uuid.uuid4()}{ext}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        file.save(file_path)
        
        # 生成访问路径
        base_url = f"http://{request.host}"
        avatar_url = f"{base_url}/static/avatars/{filename}"
        
        # 更新用户头像
        user = User.find_by_id(user_id)
        if user:
            user.update(avatar=avatar_url)
        
        return jsonify({
            'code': 0,
            'msg': '头像上传成功',
            'data': {
                'avatarUrl': avatar_url
            }
        })
    
    except Exception as e:
        logger.error(f"上传头像失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'上传失败: {str(e)}',
            'data': None
        })


# ==================== 运营接口 ====================

@user_bp.route('/op/list', methods=['GET'])
@op_required
def list_op_users(platform_type):
    """获取用户列表（运营）"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        phone = request.args.get('phone')
        status = request.args.get('status', type=int)
        
        # 构建过滤条件
        filters = {}
        if phone:
            filters['phone'] = phone
        if status is not None:
            filters['status'] = status
        
        result = User.list_all(page=page, page_size=page_size, **filters)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@user_bp.route('/op/<int:user_id>', methods=['PUT'])
@op_required
def update_op_user(platform_type, user_id):
    """编辑用户信息（运营）"""
    try:
        data = request.get_json()
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        # 更新用户信息
        user.update(**data)
        
        return jsonify({
            'code': 0,
            'msg': '更新成功',
            'data': user.to_dict()
        })
    
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


# ==================== 管理员接口 ====================

@user_bp.route('/list', methods=['GET'])
@admin_required
def list_users(platform_type):
    """获取用户列表（管理员）"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        phone = request.args.get('phone')
        status = request.args.get('status', type=int)
        
        # 构建过滤条件
        filters = {}
        if phone:
            filters['phone'] = phone
        if status is not None:
            filters['status'] = status
        
        result = User.list_all(page=page, page_size=page_size, **filters)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@user_bp.route('/<int:user_id>', methods=['GET'])
@admin_required
def get_user_by_id(platform_type, user_id):
    """根据ID获取用户信息（管理员）"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': user.to_dict()
        })
    
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@user_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def admin_update_user(platform_type, user_id):
    """管理员更新用户信息"""
    try:
        data = request.get_json()
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        success = user.update(**data)
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': {
                    'userId': user.id
                }
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"管理员更新用户失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@user_bp.route('/<int:user_id>/status', methods=['PUT'])
@admin_required
def update_user_status(platform_type, user_id):
    """更新用户状态（管理员）"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status is None:
            return jsonify({
                'code': 400,
                'msg': '状态不能为空',
                'data': None
            })
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
        
        # TODO: 实现状态更新
        
        return jsonify({
            'code': 0,
            'msg': '状态更新成功',
            'data': None
        })
    
    except Exception as e:
        logger.error(f"更新用户状态失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })
