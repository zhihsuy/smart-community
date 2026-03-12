# routes/utility.py - 智能水电表系统路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime, timedelta

utility_bp = Blueprint('utility', __name__, url_prefix='/api/v1/pc/utility')


# ==================== 表具管理 ====================

@utility_bp.route('/meters', methods=['GET'])
@login_required
def get_meters():
    """获取表具列表"""
    try:
        building_id = request.args.get('building_id')
        meter_type = request.args.get('type')
        status = request.args.get('status')
        user_id = request.args.get('user_id')
        meter_no = request.args.get('meter_no')
        
        conditions = ["1=1"]
        params = []
        
        if building_id:
            conditions.append("m.building_id = %s")
            params.append(building_id)
        if meter_type:
            conditions.append("m.meter_type = %s")
            params.append(meter_type)
        if status:
            conditions.append("m.status = %s")
            params.append(status)
        if user_id:
            conditions.append("m.user_id = %s")
            params.append(user_id)
        if meter_no:
            conditions.append("m.meter_no LIKE %s")
            params.append(f"%{meter_no}%")
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT m.*, b.name as building_name, u.nickname, u.phone
            FROM t_utility_meter m
            LEFT JOIN t_building b ON m.building_id = b.id
            LEFT JOIN t_user u ON m.user_id = u.id
            WHERE {where_clause}
            ORDER BY m.created_at DESC
        """
        
        meters = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': meters
        })
        
    except Exception as e:
        logger.error(f"获取表具列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@utility_bp.route('/meters', methods=['POST'])
@admin_required
def create_meter():
    """创建表具（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            INSERT INTO t_utility_meter 
            (meter_no, meter_type, building_id, unit, room_number, user_id, location, install_time, current_reading, last_reading)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('meter_no'),
            data.get('meter_type'),
            data.get('building_id'),
            data.get('unit'),
            data.get('room_number'),
            data.get('user_id'),
            data.get('location'),
            data.get('install_time'),
            data.get('initial_reading', 0),  # 初始读数，默认为0
            data.get('initial_reading', 0)   # 上次读数，默认为0
        )
        
        execute_sql(sql, params)
        
        return jsonify({'code': 0, 'msg': '表具创建成功', 'data': None})
        
    except Exception as e:
        logger.error(f"创建表具失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@utility_bp.route('/meters/<int:meter_id>', methods=['PUT'])
@admin_required
def update_meter(meter_id):
    """更新表具信息（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            UPDATE t_utility_meter 
            SET user_id = %s, location = %s, status = %s
            WHERE id = %s
        """
        params = (
            data.get('user_id'),
            data.get('location'),
            data.get('status'),
            meter_id
        )
        
        execute_sql(sql, params)
        
        return jsonify({'code': 0, 'msg': '更新成功', 'data': None})
        
    except Exception as e:
        logger.error(f"更新表具失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@utility_bp.route('/meters/<int:meter_id>', methods=['DELETE'])
@admin_required
def delete_meter(meter_id):
    """删除表具（管理员）"""
    try:
        sql = "DELETE FROM t_utility_meter WHERE id = %s"
        execute_sql(sql, (meter_id,))
        
        return jsonify({'code': 0, 'msg': '删除成功', 'data': None})
        
    except Exception as e:
        logger.error(f"删除表具失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


# ==================== 用量记录 ====================

@utility_bp.route('/usage', methods=['GET'])
@login_required
def get_usage_records():
    """获取用量记录"""
    try:
        meter_id = request.args.get('meter_id')
        user_id = request.args.get('user_id')
        meter_type = request.args.get('meter_type')
        building_id = request.args.get('building_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        
        conditions = ["1=1"]
        params = []
        
        if meter_id:
            conditions.append("u.meter_id = %s")
            params.append(meter_id)
        if user_id:
            conditions.append("m.user_id = %s")
            params.append(user_id)
        if meter_type:
            conditions.append("m.meter_type = %s")
            params.append(meter_type)
        if building_id:
            conditions.append("m.building_id = %s")
            params.append(building_id)
        if start_date:
            conditions.append("u.reading_time >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("u.reading_time <= %s")
            params.append(end_date + ' 23:59:59')
        
        where_clause = " AND ".join(conditions)
        
        # 查询总数
        count_sql = f"""
            SELECT COUNT(*) as total 
            FROM t_utility_usage u
            LEFT JOIN t_utility_meter m ON u.meter_id = m.id
            WHERE {where_clause}
        """
        count_result = execute_sql(count_sql, tuple(params), commit=False)
        total = count_result[0]['total'] if count_result else 0
        
        # 查询列表
        offset = (page - 1) * page_size
        sql = f"""
            SELECT u.id, u.meter_id, u.reading as current_reading, u.usage_amount as usage_amount, 
                   u.reading_time as reading_date, u.reading_type,
                   m.meter_no as meter_code, m.meter_type, m.building_id, 
                   m.unit, m.room_number, m.last_reading as previous_reading,
                   b.name as building_name
            FROM t_utility_usage u
            LEFT JOIN t_utility_meter m ON u.meter_id = m.id
            LEFT JOIN t_building b ON m.building_id = b.id
            WHERE {where_clause}
            ORDER BY u.reading_time DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        
        records = execute_sql(sql, tuple(params), commit=False)
        
        # 计算统计数据
        stats_sql = f"""
            SELECT 
                SUM(CASE WHEN m.meter_type = 'electric' THEN u.usage_amount ELSE 0 END) as total_electric,
                SUM(CASE WHEN m.meter_type = 'water' THEN u.usage_amount ELSE 0 END) as total_water,
                SUM(CASE WHEN m.meter_type = 'gas' THEN u.usage_amount ELSE 0 END) as total_gas,
                SUM(CASE WHEN u.usage_amount > 50 THEN 1 ELSE 0 END) as alert_count
            FROM t_utility_usage u
            LEFT JOIN t_utility_meter m ON u.meter_id = m.id
            WHERE {where_clause}
        """
        stats_result = execute_sql(stats_sql, tuple(params[:len(params)-2]), commit=False)
        stats = stats_result[0] if stats_result else {}
        
        # 计算趋势数据（用电量和用水量）
        trend_sql = f"""
            SELECT 
                DATE(u.reading_time) as date,
                SUM(CASE WHEN m.meter_type = 'electric' THEN u.usage_amount ELSE 0 END) as electric_value,
                SUM(CASE WHEN m.meter_type = 'water' THEN u.usage_amount ELSE 0 END) as water_value
            FROM t_utility_usage u
            LEFT JOIN t_utility_meter m ON u.meter_id = m.id
            WHERE {where_clause}
            GROUP BY DATE(u.reading_time)
            ORDER BY date ASC
        """
        trend_result = execute_sql(trend_sql, tuple(params[:len(params)-2]), commit=False)
        
        electric_trend = [{'date': row['date'].strftime('%Y-%m-%d'), 'value': float(row['electric_value'])} for row in trend_result]
        water_trend = [{'date': row['date'].strftime('%Y-%m-%d'), 'value': float(row['water_value'])} for row in trend_result]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': records,
                'total': total,
                'page': page,
                'pageSize': page_size,
                'total_electric': float(stats.get('total_electric', 0)),
                'total_water': float(stats.get('total_water', 0)),
                'total_gas': float(stats.get('total_gas', 0)),
                'alert_count': int(stats.get('alert_count', 0)),
                'electric_trend': electric_trend,
                'water_trend': water_trend
            }
        })
        
    except Exception as e:
        logger.error(f"获取用量记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@utility_bp.route('/usage', methods=['POST'])
@admin_required
def create_usage_record():
    """创建用量记录（管理员/自动抄表）"""
    try:
        data = request.get_json()
        
        sql = """
            INSERT INTO t_utility_usage 
            (meter_id, reading, usage_amount, reading_type, operator_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('meter_id'),
            data.get('reading'),
            data.get('usage_amount'),
            data.get('reading_type', 'manual'),
            request.user_id if data.get('reading_type') == 'manual' else None
        )
        
        execute_sql(sql, params)
        
        # 更新表具当前读数
        update_sql = """
            UPDATE t_utility_meter 
            SET current_reading = %s, last_reading = current_reading, last_reading_time = NOW()
            WHERE id = %s
        """
        execute_sql(update_sql, (data.get('reading'), data.get('meter_id')))
        
        return jsonify({'code': 0, 'msg': '记录创建成功', 'data': None})
        
    except Exception as e:
        logger.error(f"创建用量记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


# ==================== 用量统计 ====================

@utility_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """获取用量统计"""
    try:
        meter_id = request.args.get('meter_id')
        user_id = request.args.get('user_id')
        meter_type = request.args.get('type')
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # 按天统计
        sql = """
            SELECT 
                DATE(u.reading_time) as date,
                SUM(u.usage_amount) as total_usage,
                COUNT(*) as record_count
            FROM t_utility_usage u
            LEFT JOIN t_utility_meter m ON u.meter_id = m.id
            WHERE u.reading_time BETWEEN %s AND %s
        """
        params = [start_date, end_date + ' 23:59:59']
        
        if meter_id:
            sql += " AND u.meter_id = %s"
            params.append(meter_id)
        if user_id:
            sql += " AND m.user_id = %s"
            params.append(user_id)
        if meter_type:
            sql += " AND m.meter_type = %s"
            params.append(meter_type)
        
        sql += " GROUP BY DATE(u.reading_time) ORDER BY date DESC"
        
        statistics = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取用量统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@utility_bp.route('/my-usage', methods=['GET'])
@login_required
def get_my_usage():
    """获取当前用户的用量"""
    try:
        user_id = request.user_id
        meter_type = request.args.get('type')
        
        # 获取用户的表具
        meter_sql = """
            SELECT m.*, b.name as building_name
            FROM t_utility_meter m
            LEFT JOIN t_building b ON m.building_id = b.id
            WHERE m.user_id = %s
        """
        params = [user_id]
        
        if meter_type:
            meter_sql += " AND m.meter_type = %s"
            params.append(meter_type)
        
        meters = execute_sql(meter_sql, tuple(params), commit=False)
        
        # 获取每个表具的最近用量
        for meter in meters:
            usage_sql = """
                SELECT reading, usage_amount, reading_time
                FROM t_utility_usage
                WHERE meter_id = %s
                ORDER BY reading_time DESC
                LIMIT 6
            """
            usages = execute_sql(usage_sql, (meter['id'],), commit=False)
            meter['recent_usage'] = usages
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': meters
        })
        
    except Exception as e:
        logger.error(f"获取我的用量失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 预警管理 ====================

@utility_bp.route('/alerts', methods=['GET'])
@login_required
def get_alerts():
    """获取用量预警"""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status', 'pending')
        
        conditions = ["1=1"]
        params = []
        
        if user_id:
            conditions.append("a.user_id = %s")
            params.append(user_id)
        if status:
            conditions.append("a.status = %s")
            params.append(status)
        
        where_clause = " AND ".join(conditions)
        
        sql = f"""
            SELECT a.*, m.meter_no, m.meter_type, u.nickname, u.phone
            FROM t_utility_alert a
            LEFT JOIN t_utility_meter m ON a.meter_id = m.id
            LEFT JOIN t_user u ON a.user_id = u.id
            WHERE {where_clause}
            ORDER BY a.created_at DESC
        """
        
        alerts = execute_sql(sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': alerts
        })
        
    except Exception as e:
        logger.error(f"获取预警失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@utility_bp.route('/alerts/<int:alert_id>/process', methods=['PUT'])
@admin_required
def process_alert(alert_id):
    """处理预警（管理员）"""
    try:
        data = request.get_json()
        
        sql = """
            UPDATE t_utility_alert 
            SET status = 'processed', processed_by = %s, processed_time = NOW(), remark = %s
            WHERE id = %s
        """
        execute_sql(sql, (request.user_id, data.get('remark'), alert_id))
        
        return jsonify({'code': 0, 'msg': '处理成功', 'data': None})
        
    except Exception as e:
        logger.error(f"处理预警失败: {e}")
        return jsonify({'code': 500, 'msg': f'处理失败: {str(e)}', 'data': None})
