# routes/access_control.py - 智能门禁系统路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime, timedelta

access_bp = Blueprint('access', __name__, url_prefix='/api/v1/pc/access')


# ==================== 门禁设备管理 ====================

@access_bp.route('/devices', methods=['GET'])
@login_required
def get_devices():
    """获取门禁设备列表"""
    try:
        building_id = request.args.get('building_id')
        device_type = request.args.get('type')
        status = request.args.get('status')
        
        conditions = ["1=1"]
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
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT d.*, b.name as building_name
            FROM t_access_control_device d
            LEFT JOIN t_building b ON d.building_id = b.id
            WHERE {where_clause}
            ORDER BY d.created_at DESC
        """
        
        devices = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': devices
        })
        
    except Exception as e:
        logger.error(f"获取门禁设备列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@access_bp.route('/devices', methods=['POST'])
@admin_required
def create_device():
    """创建设备（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            INSERT INTO t_access_control_device 
            (device_code, device_name, device_type, location, building_id, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('device_code'),
            data.get('device_name'),
            data.get('device_type'),
            data.get('location'),
            data.get('building_id'),
            data.get('ip_address')
        )
        
        execute_sql(sql, params, commit=True)
        
        return jsonify({'code': 0, 'msg': '创建设备成功', 'data': None})
        
    except Exception as e:
        logger.error(f"创建设备失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@access_bp.route('/devices/<int:device_id>', methods=['PUT'])
@admin_required
def update_device(device_id):
    """更新设备信息（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            UPDATE t_access_control_device 
            SET device_name = %s, location = %s, status = %s, ip_address = %s
            WHERE id = %s
        """
        params = (
            data.get('device_name'),
            data.get('location'),
            data.get('status'),
            data.get('ip_address'),
            device_id
        )
        
        execute_sql(sql, params)
        
        return jsonify({'code': 0, 'msg': '更新成功', 'data': None})
        
    except Exception as e:
        logger.error(f"更新设备失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


# ==================== 门禁权限管理 ====================

@access_bp.route('/permissions', methods=['GET'])
@login_required
def get_permissions():
    """获取门禁权限列表"""
    try:
        user_id = request.args.get('user_id')
        device_id = request.args.get('device_id')
        
        conditions = ["1=1"]
        params = []
        
        if user_id:
            conditions.append("p.user_id = %s")
            params.append(user_id)
        if device_id:
            conditions.append("p.device_id = %s")
            params.append(device_id)
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT p.*, u.nickname, u.phone, d.device_name, d.device_type
            FROM t_access_control_permission p
            LEFT JOIN t_user u ON p.user_id = u.id
            LEFT JOIN t_access_control_device d ON p.device_id = d.id
            WHERE {where_clause}
            ORDER BY p.created_at DESC
        """
        
        permissions = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': permissions
        })
        
    except Exception as e:
        logger.error(f"获取权限列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@access_bp.route('/permissions', methods=['POST'])
@admin_required
def create_permission():
    """创建门禁权限（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            INSERT INTO t_access_control_permission 
            (user_id, device_id, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, 'active')
        """
        params = (
            data.get('user_id'),
            data.get('device_id'),
            data.get('start_time'),
            data.get('end_time')
        )
        
        execute_sql(sql, params)
        
        return jsonify({'code': 0, 'msg': '权限创建成功', 'data': None})
        
    except Exception as e:
        logger.error(f"创建权限失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@access_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
@admin_required
def delete_permission(permission_id):
    """删除门禁权限（管理员）"""
    try:
        sql = "DELETE FROM t_access_control_permission WHERE id = %s"
        execute_sql(sql, (permission_id,))
        
        return jsonify({'code': 0, 'msg': '权限删除成功', 'data': None})
        
    except Exception as e:
        logger.error(f"删除权限失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


# ==================== 出入记录 ====================

@access_bp.route('/records', methods=['GET'])
@login_required
def get_access_records():
    """获取出入记录"""
    try:
        user_id = request.args.get('user_id')
        device_id = request.args.get('device_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = ["1=1"]
        params = []
        
        if user_id:
            conditions.append("r.user_id = %s")
            params.append(user_id)
        if device_id:
            conditions.append("r.device_id = %s")
            params.append(device_id)
        if start_date:
            conditions.append("r.record_time >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("r.record_time <= %s")
            params.append(end_date + ' 23:59:59')
        
        where_clause = " AND ".join(conditions)
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM t_access_control_record r WHERE {where_clause}"
        count_result = execute_sql(count_sql, tuple(params), commit=False)
        total = count_result[0]['total'] if count_result else 0
        
        # 查询记录
        offset = (page - 1) * page_size
        sql = f"""
            SELECT r.*, u.nickname, u.phone, d.device_name, d.location
            FROM t_access_control_record r
            LEFT JOIN t_user u ON r.user_id = u.id
            LEFT JOIN t_access_control_device d ON r.device_id = d.id
            WHERE {where_clause}
            ORDER BY r.created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        
        records = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': records,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取出入记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@access_bp.route('/records/statistics', methods=['GET'])
@login_required
def get_access_statistics():
    """获取出入统计"""
    try:
        building_id = request.args.get('building_id')
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # 按天统计
        sql = """
            SELECT 
                DATE(r.created_at) as date,
                COUNT(*) as total_count,
                SUM(CASE WHEN r.status = 'success' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN r.status = 'fail' THEN 1 ELSE 0 END) as failed_count
            FROM t_access_control_record r
            LEFT JOIN t_access_control_device d ON r.device_id = d.id
            WHERE r.created_at BETWEEN %s AND %s
        """
        params = [start_date, end_date + ' 23:59:59']
        
        if building_id:
            sql += " AND d.building_id = %s"
            params.append(building_id)
        
        sql += " GROUP BY DATE(r.created_at) ORDER BY date DESC"
        
        statistics = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取出入统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 远程开门 ====================

@access_bp.route('/remote-open', methods=['POST'])
@login_required
def remote_open():
    """远程开门"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        user_id = request.user_id
        
        # 记录开门请求
        sql = """
            INSERT INTO t_access_control_record 
            (user_id, device_id, access_type, status, message)
            VALUES (%s, %s, 'remote', 'success', '远程开门')
        """
        execute_sql(sql, (user_id, device_id))
        
        # TODO: 调用硬件接口实际开门
        
        return jsonify({
            'code': 0,
            'msg': '开门指令已发送',
            'data': None
        })
        
    except Exception as e:
        logger.error(f"远程开门失败: {e}")
        return jsonify({'code': 500, 'msg': f'开门失败: {str(e)}', 'data': None})
