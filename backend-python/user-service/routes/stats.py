# routes/stats.py - 统计数据路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import admin_required
from config.database import logger, execute_sql
from datetime import datetime, timedelta

stats_bp = Blueprint('stats', __name__, url_prefix='/api/v1/admin/stats')


def get_date_range(range_type):
    """根据时间范围类型获取日期范围"""
    today = datetime.now().date()
    
    if range_type == 'today':
        start_date = today
        end_date = today
    elif range_type == 'week':
        start_date = today - timedelta(days=7)
        end_date = today
    elif range_type == 'month':
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        start_date = today - timedelta(days=7)
        end_date = today
    
    return start_date, end_date


@stats_bp.route('/overview', methods=['GET'])
@admin_required
def get_overview_stats():
    """获取概览统计数据"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        # 用户统计
        user_count_sql = "SELECT COUNT(*) as count FROM t_user"
        user_count = execute_sql(user_count_sql, commit=False)[0]['count']
        
        # 新增用户（指定时间范围）
        new_user_sql = f"SELECT COUNT(*) as count FROM t_user WHERE DATE(created_at) BETWEEN %s AND %s"
        new_user_count = execute_sql(new_user_sql, (start_date, end_date), commit=False)[0]['count']
        
        # 楼栋统计
        building_count_sql = "SELECT COUNT(*) as count FROM t_building"
        building_count = execute_sql(building_count_sql, commit=False)[0]['count']
        
        # 活动统计
        activity_count_sql = "SELECT COUNT(*) as count FROM t_activity"
        activity_count = execute_sql(activity_count_sql, commit=False)[0]['count']
        
        # 报修统计
        repair_count_sql = "SELECT COUNT(*) as count FROM t_repair"
        repair_count = execute_sql(repair_count_sql, commit=False)[0]['count']
        
        # 今日报修
        today_repair_sql = "SELECT COUNT(*) as count FROM t_repair WHERE DATE(created_at) = CURDATE()"
        today_repair_count = execute_sql(today_repair_sql, commit=False)[0]['count']
        
        # 门禁设备统计
        access_device_sql = "SELECT COUNT(*) as count FROM t_access_control_device"
        access_device_count = execute_sql(access_device_sql, commit=False)[0]['count']
        
        # 今日门禁记录
        today_access_sql = "SELECT COUNT(*) as count FROM t_access_control_record WHERE DATE(access_time) = CURDATE()"
        today_access_count = execute_sql(today_access_sql, commit=False)[0]['count']
        
        # 监控设备统计
        monitoring_sql = "SELECT COUNT(*) as count FROM t_monitoring_device"
        monitoring_count = execute_sql(monitoring_sql, commit=False)[0]['count']
        
        # 在线监控设备
        online_monitoring_sql = "SELECT COUNT(*) as count FROM t_monitoring_device WHERE status = 'online'"
        online_monitoring_count = execute_sql(online_monitoring_sql, commit=False)[0]['count']
        
        # 水电表统计
        utility_sql = "SELECT COUNT(*) as count FROM t_utility_meter"
        utility_count = execute_sql(utility_sql, commit=False)[0]['count']
        
        # 停车位统计
        parking_sql = "SELECT COUNT(*) as count FROM t_parking_space"
        parking_count = execute_sql(parking_sql, commit=False)[0]['count']
        
        # 空闲车位
        free_parking_sql = "SELECT COUNT(*) as count FROM t_parking_space WHERE status = 'free'"
        free_parking_count = execute_sql(free_parking_sql, commit=False)[0]['count']
        
        # 公告统计
        notice_sql = "SELECT COUNT(*) as count FROM t_notice"
        notice_count = execute_sql(notice_sql, commit=False)[0]['count']
        
        # 活跃公告
        active_notice_sql = "SELECT COUNT(*) as count FROM t_notice WHERE status = 'active'"
        active_notice_count = execute_sql(active_notice_sql, commit=False)[0]['count']
        
        # 快递柜统计
        locker_sql = "SELECT COUNT(*) as count FROM t_locker"
        locker_count = execute_sql(locker_sql, commit=False)[0]['count']
        
        # 待缴费账单
        pending_payment_sql = "SELECT COUNT(*) as count FROM t_payment WHERE status = 'pending'"
        pending_payment_count = execute_sql(pending_payment_sql, commit=False)[0]['count']
        
        # 投诉统计
        complaint_sql = "SELECT COUNT(*) as count FROM t_complaint"
        complaint_count = execute_sql(complaint_sql, commit=False)[0]['count']
        
        # 待处理投诉
        pending_complaint_sql = "SELECT COUNT(*) as count FROM t_complaint WHERE status = 'pending'"
        pending_complaint_count = execute_sql(pending_complaint_sql, commit=False)[0]['count']
        
        # 访客统计
        visitor_sql = "SELECT COUNT(*) as count FROM t_visitor WHERE DATE(visit_date) = CURDATE()"
        visitor_count = execute_sql(visitor_sql, commit=False)[0]['count']
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'userCount': user_count,
                'newUserCount': new_user_count,
                'buildingCount': building_count,
                'activityCount': activity_count,
                'repairCount': repair_count,
                'todayRepairCount': today_repair_count,
                'accessDeviceCount': access_device_count,
                'todayAccessCount': today_access_count,
                'monitoringCount': monitoring_count,
                'onlineMonitoringCount': online_monitoring_count,
                'utilityCount': utility_count,
                'parkingCount': parking_count,
                'freeParkingCount': free_parking_count,
                'noticeCount': notice_count,
                'activeNoticeCount': active_notice_count,
                'lockerCount': locker_count,
                'pendingPaymentCount': pending_payment_count,
                'complaintCount': complaint_count,
                'pendingComplaintCount': pending_complaint_count,
                'visitorCount': visitor_count
            }
        })
    
    except Exception as e:
        logger.error(f"获取概览统计数据失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/user-trend', methods=['GET'])
@admin_required
def get_user_trend():
    """获取用户增长趋势"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        if range_type == 'today':
            sql = """
                SELECT 
                    HOUR(created_at) as time_label,
                    COUNT(*) as count
                FROM t_user
                WHERE DATE(created_at) = %s
                GROUP BY HOUR(created_at)
                ORDER BY time_label
            """
            params = (start_date,)
        elif range_type == 'week':
            sql = """
                SELECT 
                    DATE(created_at) as time_label,
                    COUNT(*) as count
                FROM t_user
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY DATE(created_at)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        else:
            sql = """
                SELECT 
                    DATE(created_at) as time_label,
                    COUNT(*) as count
                FROM t_user
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY DATE(created_at)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        
        results = execute_sql(sql, params, commit=False)
        
        labels = [str(row['time_label']) for row in results]
        values = [row['count'] for row in results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'labels': labels,
                'values': values
            }
        })
    
    except Exception as e:
        logger.error(f"获取用户增长趋势失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/repair-trend', methods=['GET'])
@admin_required
def get_repair_trend():
    """获取报修趋势"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        if range_type == 'today':
            sql = """
                SELECT 
                    HOUR(created_at) as time_label,
                    COUNT(*) as count
                FROM t_repair
                WHERE DATE(created_at) = %s
                GROUP BY HOUR(created_at)
                ORDER BY time_label
            """
            params = (start_date,)
        elif range_type == 'week':
            sql = """
                SELECT 
                    DATE(created_at) as time_label,
                    COUNT(*) as count
                FROM t_repair
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY DATE(created_at)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        else:
            sql = """
                SELECT 
                    DATE(created_at) as time_label,
                    COUNT(*) as count
                FROM t_repair
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY DATE(created_at)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        
        results = execute_sql(sql, params, commit=False)
        
        labels = [str(row['time_label']) for row in results]
        values = [row['count'] for row in results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'labels': labels,
                'values': values
            }
        })
    
    except Exception as e:
        logger.error(f"获取报修趋势失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/repair-status', methods=['GET'])
@admin_required
def get_repair_status():
    """获取报修状态分布"""
    try:
        sql = """
            SELECT 
                status,
                COUNT(*) as count
            FROM t_repair
            GROUP BY status
        """
        
        results = execute_sql(sql, commit=False)
        
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        
        labels = [status_map.get(row['status'], row['status']) for row in results]
        values = [row['count'] for row in results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'labels': labels,
                'values': values
            }
        })
    
    except Exception as e:
        logger.error(f"获取报修状态分布失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/payment-stats', methods=['GET'])
@admin_required
def get_payment_stats():
    """获取费用统计"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        # 按费用类型统计
        type_sql = """
            SELECT 
                payment_type,
                SUM(amount) as total_amount,
                COUNT(*) as count
            FROM t_payment
            WHERE DATE(created_at) BETWEEN %s AND %s
            GROUP BY payment_type
        """
        results = execute_sql(type_sql, (start_date, end_date), commit=False)
        
        type_map = {
            'property': '物业费',
            'water': '水费',
            'electricity': '电费',
            'parking': '停车费',
            'other': '其他'
        }
        
        labels = [type_map.get(row['payment_type'], row['payment_type']) for row in results]
        values = [float(row['total_amount']) for row in results]
        
        # 按支付状态统计
        status_sql = """
            SELECT 
                status,
                SUM(amount) as total_amount,
                COUNT(*) as count
            FROM t_payment
            WHERE DATE(created_at) BETWEEN %s AND %s
            GROUP BY status
        """
        status_results = execute_sql(status_sql, (start_date, end_date), commit=False)
        
        status_map = {
            'pending': '待支付',
            'paid': '已支付',
            'overdue': '逾期'
        }
        
        status_labels = [status_map.get(row['status'], row['status']) for row in status_results]
        status_values = [float(row['total_amount']) for row in status_results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'type': {
                    'labels': labels,
                    'values': values
                },
                'status': {
                    'labels': status_labels,
                    'values': status_values
                }
            }
        })
    
    except Exception as e:
        logger.error(f"获取费用统计失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/access-trend', methods=['GET'])
@admin_required
def get_access_trend():
    """获取门禁进出趋势"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        if range_type == 'today':
            sql = """
                SELECT 
                    HOUR(access_time) as time_label,
                    COUNT(*) as count
                FROM t_access_control_record
                WHERE DATE(access_time) = %s
                GROUP BY HOUR(access_time)
                ORDER BY time_label
            """
            params = (start_date,)
        elif range_type == 'week':
            sql = """
                SELECT 
                    DATE(access_time) as time_label,
                    COUNT(*) as count
                FROM t_access_control_record
                WHERE DATE(access_time) BETWEEN %s AND %s
                GROUP BY DATE(access_time)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        else:
            sql = """
                SELECT 
                    DATE(access_time) as time_label,
                    COUNT(*) as count
                FROM t_access_control_record
                WHERE DATE(access_time) BETWEEN %s AND %s
                GROUP BY DATE(access_time)
                ORDER BY time_label
            """
            params = (start_date, end_date)
        
        results = execute_sql(sql, params, commit=False)
        
        labels = [str(row['time_label']) for row in results]
        values = [row['count'] for row in results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'labels': labels,
                'values': values
            }
        })
    
    except Exception as e:
        logger.error(f"获取门禁进出趋势失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/building-stats', methods=['GET'])
@admin_required
def get_building_stats():
    """获取楼栋统计"""
    try:
        sql = """
            SELECT 
                b.id,
                b.name,
                b.unit_count,
                b.floor_count,
                b.household_count,
                (SELECT COUNT(*) FROM t_user WHERE building_id = b.id) as user_count,
                (SELECT COUNT(*) FROM t_repair r 
                 JOIN t_user u ON r.user_id = u.id 
                 WHERE u.building_id = b.id AND r.status = 'pending') as pending_repair_count
            FROM t_building b
            ORDER BY b.id
        """
        
        results = execute_sql(sql, commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': results
            }
        })
    
    except Exception as e:
        logger.error(f"获取楼栋统计失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/activity-stats', methods=['GET'])
@admin_required
def get_activity_stats():
    """获取活动统计"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        # 活动参与人数统计
        sql = """
            SELECT 
                a.id,
                a.title,
                a.start_time,
                a.end_time,
                a.max_participants,
                (SELECT COUNT(*) FROM t_activity_registration WHERE activity_id = a.id) as participant_count
            FROM t_activity a
            WHERE DATE(a.start_time) BETWEEN %s AND %s
            ORDER BY a.start_time DESC
        """
        
        results = execute_sql(sql, (start_date, end_date), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': results
            }
        })
    
    except Exception as e:
        logger.error(f"获取活动统计失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/complaint-stats', methods=['GET'])
@admin_required
def get_complaint_stats():
    """获取投诉统计"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        # 按类型统计
        type_sql = """
            SELECT 
                complaint_type,
                COUNT(*) as count
            FROM t_complaint
            WHERE DATE(created_at) BETWEEN %s AND %s
            GROUP BY complaint_type
        """
        results = execute_sql(type_sql, (start_date, end_date), commit=False)
        
        type_map = {
            'service': '服务问题',
            'facility': '设施问题',
            'environment': '环境问题',
            'noise': '噪音问题',
            'other': '其他'
        }
        
        labels = [type_map.get(row['complaint_type'], row['complaint_type']) for row in results]
        values = [row['count'] for row in results]
        
        # 按状态统计
        status_sql = """
            SELECT 
                status,
                COUNT(*) as count
            FROM t_complaint
            WHERE DATE(created_at) BETWEEN %s AND %s
            GROUP BY status
        """
        status_results = execute_sql(status_sql, (start_date, end_date), commit=False)
        
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'resolved': '已解决',
            'closed': '已关闭'
        }
        
        status_labels = [status_map.get(row['status'], row['status']) for row in status_results]
        status_values = [row['count'] for row in status_results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'type': {
                    'labels': labels,
                    'values': values
                },
                'status': {
                    'labels': status_labels,
                    'values': status_values
                }
            }
        })
    
    except Exception as e:
        logger.error(f"获取投诉统计失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@stats_bp.route('/utility-trend', methods=['GET'])
@admin_required
def get_utility_trend():
    """获取水电使用趋势"""
    try:
        range_type = request.args.get('range', 'week')
        start_date, end_date = get_date_range(range_type)
        
        # 水费统计
        water_sql = """
            SELECT 
                DATE(created_at) as time_label,
                SUM(amount) as total_amount
            FROM t_payment
            WHERE payment_type = 'water' 
            AND DATE(created_at) BETWEEN %s AND %s
            GROUP BY DATE(created_at)
            ORDER BY time_label
        """
        water_results = execute_sql(water_sql, (start_date, end_date), commit=False)
        
        water_labels = [str(row['time_label']) for row in water_results]
        water_values = [float(row['total_amount']) for row in water_results]
        
        # 电费统计
        electricity_sql = """
            SELECT 
                DATE(created_at) as time_label,
                SUM(amount) as total_amount
            FROM t_payment
            WHERE payment_type = 'electricity' 
            AND DATE(created_at) BETWEEN %s AND %s
            GROUP BY DATE(created_at)
            ORDER BY time_label
        """
        electricity_results = execute_sql(electricity_sql, (start_date, end_date), commit=False)
        
        electricity_labels = [str(row['time_label']) for row in electricity_results]
        electricity_values = [float(row['total_amount']) for row in electricity_results]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'water': {
                    'labels': water_labels,
                    'values': water_values
                },
                'electricity': {
                    'labels': electricity_labels,
                    'values': electricity_values
                }
            }
        })
    
    except Exception as e:
        logger.error(f"获取水电使用趋势失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })
