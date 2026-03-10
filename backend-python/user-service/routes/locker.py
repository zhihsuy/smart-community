# routes/locker.py - 快递柜管理系统路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime, timedelta
import random
import string

locker_bp = Blueprint('locker', __name__, url_prefix='/api/v1/pc/locker')


# ==================== 快递柜管理 ====================

@locker_bp.route('/lockers', methods=['GET'])
@login_required
def get_lockers():
    """获取快递柜列表"""
    try:
        status = request.args.get('status')
        
        conditions = ["1=1"]
        params = []
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT l.*,
                   (SELECT COUNT(*) FROM t_locker_box WHERE locker_id = l.id AND status = 'idle') as idle_count,
                   (SELECT COUNT(*) FROM t_locker_box WHERE locker_id = l.id AND status = 'occupied') as occupied_count
            FROM t_locker l
            WHERE {where_clause}
            ORDER BY l.created_at DESC
        """
        
        lockers = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': lockers
        })
        
    except Exception as e:
        logger.error(f"获取快递柜列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@locker_bp.route('/lockers', methods=['POST'])
@admin_required
def create_locker():
    """创建快递柜（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            INSERT INTO t_locker 
            (locker_no, locker_name, location, total_boxes, large_boxes, medium_boxes, small_boxes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('locker_no'),
            data.get('locker_name'),
            data.get('location'),
            data.get('total_boxes'),
            data.get('large_boxes'),
            data.get('medium_boxes'),
            data.get('small_boxes')
        )
        
        execute_sql(sql, params)
        
        return jsonify({'code': 0, 'msg': '快递柜创建成功', 'data': None})
        
    except Exception as e:
        logger.error(f"创建快递柜失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@locker_bp.route('/lockers/<int:locker_id>/boxes', methods=['GET'])
@login_required
def get_boxes(locker_id):
    """获取格口列表"""
    try:
        status = request.args.get('status')
        
        conditions = ["locker_id = %s"]
        params = [locker_id]
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT b.*, p.tracking_no, p.recipient_name, p.pickup_code
            FROM t_locker_box b
            LEFT JOIN t_package p ON b.current_package_id = p.id
            WHERE {where_clause}
            ORDER BY b.box_no
        """
        
        boxes = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': boxes
        })
        
    except Exception as e:
        logger.error(f"获取格口列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 包裹管理 ====================

@locker_bp.route('/packages', methods=['GET'])
@login_required
def get_packages():
    """获取包裹列表"""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        
        conditions = ["1=1"]
        params = []
        
        if user_id:
            conditions.append("p.user_id = %s")
            params.append(user_id)
        if status:
            conditions.append("p.status = %s")
            params.append(status)
        
        where_clause = " AND ".join(conditions)
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM t_package p WHERE {where_clause}"
        count_result = execute_sql(count_sql, tuple(params), commit=False)
        total = count_result[0]['total'] if count_result else 0
        
        # 查询列表
        offset = (page - 1) * page_size
        sql = f"""
            SELECT p.*, l.locker_name, b.box_no, b.box_type
            FROM t_package p
            LEFT JOIN t_locker l ON p.locker_id = l.id
            LEFT JOIN t_locker_box b ON p.box_id = b.id
            WHERE {where_clause}
            ORDER BY p.store_time DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        
        packages = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': packages,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取包裹列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@locker_bp.route('/packages', methods=['POST'])
@login_required
def store_package():
    """存入包裹"""
    try:
        data = request.get_json()
        
        # 查找空闲格口
        box_sql = """
            SELECT id, box_type FROM t_locker_box 
            WHERE locker_id = %s AND status = 'idle' AND box_type = %s
            ORDER BY box_no LIMIT 1
        """
        box_result = execute_sql(box_sql, (data.get('locker_id'), data.get('box_type', 'medium')), commit=False)
        
        if not box_result:
            return jsonify({'code': 400, 'msg': '没有空闲格口', 'data': None})
        
        box_id = box_result[0]['id']
        
        # 生成取件码
        pickup_code = ''.join(random.choices(string.digits, k=6))
        
        # 计算超时时间（默认48小时）
        overdue_time = datetime.now() + timedelta(hours=48)
        
        sql = """
            INSERT INTO t_package 
            (tracking_no, courier_company, locker_id, box_id, user_id, recipient_name, recipient_phone, 
             pickup_code, overdue_time, remark)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('tracking_no'),
            data.get('courier_company'),
            data.get('locker_id'),
            box_id,
            data.get('user_id'),
            data.get('recipient_name'),
            data.get('recipient_phone'),
            pickup_code,
            overdue_time,
            data.get('remark')
        )
        
        execute_sql(sql, params)
        
        # 更新格口状态
        update_box_sql = """
            UPDATE t_locker_box 
            SET status = 'occupied', current_package_id = LAST_INSERT_ID(), open_count = open_count + 1, last_open_time = NOW()
            WHERE id = %s
        """
        execute_sql(update_box_sql, (box_id,))
        
        return jsonify({'code': 0, 'msg': '包裹存入成功', 'data': {'pickup_code': pickup_code}})
        
    except Exception as e:
        logger.error(f"存入包裹失败: {e}")
        return jsonify({'code': 500, 'msg': f'存入失败: {str(e)}', 'data': None})


@locker_bp.route('/packages/pickup', methods=['POST'])
@login_required
def pickup_package():
    """取件"""
    try:
        data = request.get_json()
        pickup_code = data.get('pickup_code')
        user_id = request.user_id
        
        # 查询包裹
        package_sql = """
            SELECT p.*, b.id as box_id
            FROM t_package p
            LEFT JOIN t_locker_box b ON p.box_id = b.id
            WHERE p.pickup_code = %s AND p.user_id = %s AND p.status = 'stored'
        """
        package_result = execute_sql(package_sql, (pickup_code, user_id), commit=False)
        
        if not package_result:
            return jsonify({'code': 404, 'msg': '取件码错误或包裹不存在', 'data': None})
        
        package = package_result[0]
        
        # 更新包裹状态
        update_package_sql = """
            UPDATE t_package 
            SET status = 'picked', pickup_time = NOW(), pickup_photo = %s
            WHERE id = %s
        """
        execute_sql(update_package_sql, (data.get('pickup_photo'), package['id']))
        
        # 更新格口状态
        update_box_sql = """
            UPDATE t_locker_box 
            SET status = 'idle', current_package_id = NULL, open_count = open_count + 1, last_open_time = NOW()
            WHERE id = %s
        """
        execute_sql(update_box_sql, (package['box_id'],))
        
        return jsonify({'code': 0, 'msg': '取件成功', 'data': None})
        
    except Exception as e:
        logger.error(f"取件失败: {e}")
        return jsonify({'code': 500, 'msg': f'取件失败: {str(e)}', 'data': None})


# ==================== 我的包裹 ====================

@locker_bp.route('/my-packages', methods=['GET'])
@login_required
def get_my_packages():
    """获取当前用户的包裹"""
    try:
        user_id = request.user_id
        status = request.args.get('status', 'stored')
        
        sql = """
            SELECT p.*, l.locker_name, l.location, b.box_no
            FROM t_package p
            LEFT JOIN t_locker l ON p.locker_id = l.id
            LEFT JOIN t_locker_box b ON p.box_id = b.id
            WHERE p.user_id = %s AND p.status = %s
            ORDER BY p.store_time DESC
        """
        
        packages = execute_sql(sql, (user_id, status), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': packages
        })
        
    except Exception as e:
        logger.error(f"获取我的包裹失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 统计 ====================

@locker_bp.route('/statistics', methods=['GET'])
@admin_required
def get_statistics():
    """获取快递柜统计（管理员）"""
    try:
        # 快递柜状态统计
        locker_sql = """
            SELECT status, COUNT(*) as count
            FROM t_locker
            GROUP BY status
        """
        locker_stats = execute_sql(locker_sql, commit=False)
        
        # 格口状态统计
        box_sql = """
            SELECT status, COUNT(*) as count
            FROM t_locker_box
            GROUP BY status
        """
        box_stats = execute_sql(box_sql, commit=False)
        
        # 包裹状态统计
        package_sql = """
            SELECT status, COUNT(*) as count
            FROM t_package
            GROUP BY status
        """
        package_stats = execute_sql(package_sql, commit=False)
        
        # 今日存取统计
        today_sql = """
            SELECT 
                SUM(CASE WHEN DATE(store_time) = CURDATE() THEN 1 ELSE 0 END) as store_count,
                SUM(CASE WHEN DATE(pickup_time) = CURDATE() THEN 1 ELSE 0 END) as pickup_count
            FROM t_package
        """
        today_stats = execute_sql(today_sql, commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'locker_stats': locker_stats,
                'box_stats': box_stats,
                'package_stats': package_stats,
                'today_stats': today_stats[0] if today_stats else {}
            }
        })
        
    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
