# routes/access.py - 门禁管理路由
from flask import Blueprint, request, jsonify
from models.access_control import AccessControlDevice, AccessControlPermission, AccessControlRecord
from utils.jwt_util import login_required, admin_required
from config.database import logger
import json

access_bp = Blueprint('access', __name__, url_prefix='/api/v1/<platform_type>/access')


@access_bp.route('/devices', methods=['GET'])
@login_required
def get_access_devices(platform_type):
    """获取门禁设备列表"""
    try:
        # 获取查询参数
        building_id = request.args.get('building_id')
        device_type = request.args.get('type')
        status = request.args.get('status')
        
        # 构建查询条件
        conditions = []
        params = []
        
        if building_id:
            conditions.append("building_id = %s")
            params.append(building_id)
        
        if device_type:
            conditions.append("device_type = %s")
            params.append(device_type)
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        # 执行查询
        devices = AccessControlDevice.find_all(conditions, params)
        
        # 转换为字典列表
        devices_list = [device.to_dict() for device in devices]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': devices_list
        })
    
    except Exception as e:
        logger.error(f"获取门禁设备列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@access_bp.route('/devices', methods=['POST'])
@admin_required
def add_access_device(platform_type):
    """新增门禁设备"""
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['device_code', 'device_name', 'device_type', 'building_id', 'location', 'ip_address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        # 创建设备
        device = AccessControlDevice.create(
            device_code=data['device_code'],
            device_name=data['device_name'],
            device_type=data['device_type'],
            building_id=data['building_id'],
            location=data['location'],
            ip_address=data['ip_address'],
            status=data.get('status', 'normal')
        )
        
        if device:
            return jsonify({
                'code': 0,
                'msg': '新增设备成功',
                'data': device.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '新增设备失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"新增门禁设备失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'新增失败: {str(e)}',
            'data': None
        })


@access_bp.route('/devices/<int:device_id>', methods=['PUT'])
@admin_required
def update_access_device(platform_type, device_id):
    """编辑门禁设备"""
    try:
        data = request.get_json()
        
        # 查找设备
        device = AccessControlDevice.find_by_id(device_id)
        if not device:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
        # 更新设备信息
        update_data = {
            'device_code': data.get('device_code'),
            'device_name': data.get('device_name'),
            'device_type': data.get('device_type'),
            'building_id': data.get('building_id'),
            'location': data.get('location'),
            'ip_address': data.get('ip_address'),
            'status': data.get('status')
        }
        
        # 过滤掉None值
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if update_data:
            success = device.update(**update_data)
            if success:
                updated_device = AccessControlDevice.find_by_id(device_id)
                return jsonify({
                    'code': 0,
                    'msg': '编辑设备成功',
                    'data': updated_device.to_dict()
                })
            else:
                return jsonify({
                    'code': 400,
                    'msg': '编辑设备失败',
                    'data': None
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '没有要更新的内容',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"编辑门禁设备失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'编辑失败: {str(e)}',
            'data': None
        })


@access_bp.route('/devices/<int:device_id>', methods=['DELETE'])
@admin_required
def delete_access_device(platform_type, device_id):
    """删除门禁设备"""
    try:
        # 查找设备
        device = AccessControlDevice.find_by_id(device_id)
        if not device:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
        # 删除设备
        success = device.delete()
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除设备成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除设备失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"删除门禁设备失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@access_bp.route('/remote-open', methods=['POST'])
@login_required
def remote_open_door(platform_type):
    """远程开门"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        
        if not device_id:
            return jsonify({
                'code': 400,
                'msg': '设备ID不能为空',
                'data': None
            })
        
        # 查找设备
        device = AccessControlDevice.find_by_id(device_id)
        if not device:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
        # 检查设备状态
        if device.status != 'normal':
            return jsonify({
                'code': 400,
                'msg': '设备状态异常，无法远程开门',
                'data': None
            })
        
        # TODO: 实现远程开门逻辑
        # 这里需要调用实际的设备接口
        
        # 记录开门记录
        AccessControlRecord.create(
            device_id=device_id,
            user_id=request.user_id,
            access_type='remote',
            status='success',
            message='远程开门'
        )
        
        return jsonify({
            'code': 0,
            'msg': '开门指令已发送',
            'data': None
        })
    
    except Exception as e:
        logger.error(f"远程开门失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'远程开门失败: {str(e)}',
            'data': None
        })


@access_bp.route('/permissions', methods=['GET'])
@admin_required
def get_access_permissions(platform_type):
    """获取门禁权限列表"""
    try:
        # 获取查询参数
        user_id = request.args.get('user_id')
        device_id = request.args.get('device_id')
        
        # 构建查询条件
        conditions = []
        params = []
        
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        
        if device_id:
            conditions.append("device_id = %s")
            params.append(device_id)
        
        # 执行查询
        permissions = AccessControlPermission.find_all(conditions, params)
        
        # 转换为字典列表
        permissions_list = [permission.to_dict() for permission in permissions]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': permissions_list
        })
    
    except Exception as e:
        logger.error(f"获取门禁权限列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@access_bp.route('/permissions', methods=['POST'])
@admin_required
def add_access_permission(platform_type):
    """新增门禁权限"""
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['user_id', 'device_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        # 检查是否已存在权限
        existing = AccessControlPermission.find_by_user_and_device(data['user_id'], data['device_id'])
        if existing:
            return jsonify({
                'code': 400,
                'msg': '该用户已拥有此设备的权限',
                'data': None
            })
        
        # 创建权限
        permission = AccessControlPermission.create(
            user_id=data['user_id'],
            device_id=data['device_id'],
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 'active')
        )
        
        if permission:
            return jsonify({
                'code': 0,
                'msg': '新增权限成功',
                'data': permission.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '新增权限失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"新增门禁权限失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'新增失败: {str(e)}',
            'data': None
        })


@access_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
@admin_required
def delete_access_permission(platform_type, permission_id):
    """删除门禁权限"""
    try:
        # 查找权限
        permission = AccessControlPermission.find_by_id(permission_id)
        if not permission:
            return jsonify({
                'code': 404,
                'msg': '权限不存在',
                'data': None
            })
        
        # 删除权限
        success = permission.delete()
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除权限成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除权限失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"删除门禁权限失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@access_bp.route('/records', methods=['GET'])
@login_required
def get_access_records(platform_type):
    """获取门禁记录列表"""
    try:
        # 获取查询参数
        user_id = request.args.get('user_id')
        device_id = request.args.get('device_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        # 构建查询条件
        conditions = []
        params = []
        
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        
        if device_id:
            conditions.append("device_id = %s")
            params.append(device_id)
        
        if start_date:
            conditions.append("created_at >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("created_at <= %s")
            params.append(end_date)
        
        # 执行查询
        records, total = AccessControlRecord.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        # 转换为字典列表
        records_list = [record.to_dict() for record in records]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': records_list,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取门禁记录列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })
