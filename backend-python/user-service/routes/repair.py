# routes/repair.py - 维修管理相关API路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger

repair_bp = Blueprint('repair', __name__, url_prefix='/api/v1/pc/repair')


# ==================== 维修工单管理 ====================

@repair_bp.route('/orders', methods=['GET'])
@login_required
def get_repair_orders():
    """获取工单列表"""
    try:
        status = request.args.get('status')
        type = request.args.get('type')
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        if type:
            conditions.append("type = %s")
            params.append(type)
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        if start_date:
            conditions.append("created_at >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("created_at <= %s")
            params.append(end_date + ' 23:59:59')
        
        from models.repair import RepairOrder
        orders, total = RepairOrder.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        orders_list = [order.to_dict() for order in orders]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': orders_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取工单列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@repair_bp.route('/orders', methods=['POST'])
@login_required
def create_repair_order():
    """创建工单"""
    try:
        data = request.get_json()
        
        from models.repair import RepairOrder
        order = RepairOrder.create(
            user_id=request.user_id,
            title=data.get('title'),
            type=data.get('type'),
            description=data.get('description'),
            address=data.get('address'),
            images=data.get('images'),
            priority=data.get('priority', 'medium')
        )
        
        if order:
            return jsonify({
                'code': 0,
                'msg': '创建工单成功',
                'data': order.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建工单失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建工单失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@repair_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_repair_order_detail(order_id):
    """获取工单详情"""
    try:
        from models.repair import RepairOrder
        order = RepairOrder.find_by_id(order_id)
        
        if order:
            return jsonify({
                'code': 0,
                'msg': '获取成功',
                'data': order.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '工单不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取工单详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@repair_bp.route('/orders/<int:order_id>/assign', methods=['POST'])
@admin_required
def assign_technician(order_id):
    """指派维修人员"""
    try:
        data = request.get_json()
        
        from models.repair import RepairOrder
        order = RepairOrder.find_by_id(order_id)
        
        if not order:
            return jsonify({
                'code': 404,
                'msg': '工单不存在',
                'data': None
            })
        
        success = order.assign_technician(
            technician_id=data.get('technician_id'),
            estimated_time=data.get('estimated_time')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '指派成功',
                'data': order.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '指派失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"指派维修人员失败: {e}")
        return jsonify({'code': 500, 'msg': f'指派失败: {str(e)}', 'data': None})


@repair_bp.route('/orders/<int:order_id>/complete', methods=['POST'])
@admin_required
def complete_order(order_id):
    """完成工单"""
    try:
        data = request.get_json()
        
        from models.repair import RepairOrder
        order = RepairOrder.find_by_id(order_id)
        
        if not order:
            return jsonify({
                'code': 404,
                'msg': '工单不存在',
                'data': None
            })
        
        success = order.complete(process_result=data.get('process_result'))
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '工单已完成',
                'data': order.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '操作失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"完成工单失败: {e}")
        return jsonify({'code': 500, 'msg': f'操作失败: {str(e)}', 'data': None})


@repair_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@admin_required
def cancel_order(order_id):
    """取消工单"""
    try:
        from models.repair import RepairOrder
        order = RepairOrder.find_by_id(order_id)
        
        if not order:
            return jsonify({
                'code': 404,
                'msg': '工单不存在',
                'data': None
            })
        
        success = order.cancel()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '工单已取消',
                'data': order.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '操作失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"取消工单失败: {e}")
        return jsonify({'code': 500, 'msg': f'操作失败: {str(e)}', 'data': None})


# ==================== 维修人员管理 ====================

@repair_bp.route('/technicians', methods=['GET'])
@login_required
def get_technicians():
    """获取维修人员列表"""
    try:
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        from models.repair import Technician
        technicians, total = Technician.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        technicians_list = [tech.to_dict() for tech in technicians]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': technicians_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取维修人员列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@repair_bp.route('/technicians', methods=['POST'])
@admin_required
def add_technician():
    """添加维修人员"""
    try:
        data = request.get_json()
        
        from models.repair import Technician
        technician = Technician.create(
            name=data.get('name'),
            phone=data.get('phone'),
            specialty=data.get('specialty'),
            status=data.get('status', 'active')
        )
        
        if technician:
            return jsonify({
                'code': 0,
                'msg': '添加维修人员成功',
                'data': technician.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '添加维修人员失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"添加维修人员失败: {e}")
        return jsonify({'code': 500, 'msg': f'添加失败: {str(e)}', 'data': None})


@repair_bp.route('/technicians/<int:technician_id>', methods=['PUT'])
@admin_required
def update_technician(technician_id):
    """更新维修人员信息"""
    try:
        from models.repair import Technician
        technician = Technician.find_by_id(technician_id)
        
        if not technician:
            return jsonify({
                'code': 404,
                'msg': '维修人员不存在',
                'data': None
            })
        
        data = request.get_json()
        success = technician.update(
            name=data.get('name'),
            phone=data.get('phone'),
            specialty=data.get('specialty'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新维修人员成功',
                'data': technician.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新维修人员失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新维修人员失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@repair_bp.route('/technicians/<int:technician_id>', methods=['DELETE'])
@admin_required
def delete_technician(technician_id):
    """删除维修人员"""
    try:
        from models.repair import Technician
        technician = Technician.find_by_id(technician_id)
        
        if not technician:
            return jsonify({
                'code': 404,
                'msg': '维修人员不存在',
                'data': None
            })
        
        success = technician.delete()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除维修人员成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除维修人员失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"删除维修人员失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


# ==================== 维修统计 ====================

@repair_bp.route('/statistics', methods=['GET'])
@login_required
def get_repair_statistics():
    """获取维修统计数据"""
    try:
        from models.repair import RepairOrder
        from models.repair import Technician
        from config.database import execute_sql
        from flask import request
        
        # 获取日期范围参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建日期条件
        date_conditions = []
        date_params = []
        if start_date:
            date_conditions.append("created_at >= %s")
            date_params.append(start_date)
        if end_date:
            date_conditions.append("created_at <= %s")
            date_params.append(end_date + ' 23:59:59')
        date_where = " WHERE " + " AND ".join(date_conditions) if date_conditions else ""
        
        # 基本统计
        conditions = []
        params = []
        if date_conditions:
            conditions.extend(date_conditions)
            params.extend(date_params)
        total_orders = RepairOrder.find_all(conditions=conditions, params=params)
        total_count = len(total_orders)
        
        pending_conditions = conditions + ["status = %s"]
        pending_params = params + ['pending']
        pending_orders = RepairOrder.find_all(conditions=pending_conditions, params=pending_params)
        pending_count = len(pending_orders)
        
        processing_conditions = conditions + ["status = %s"]
        processing_params = params + ['processing']
        processing_orders = RepairOrder.find_all(conditions=processing_conditions, params=processing_params)
        processing_count = len(processing_orders)
        
        completed_conditions = conditions + ["status = %s"]
        completed_params = params + ['completed']
        completed_orders = RepairOrder.find_all(conditions=completed_conditions, params=completed_params)
        completed_count = len(completed_orders)
        
        cancelled_conditions = conditions + ["status = %s"]
        cancelled_params = params + ['cancelled']
        cancelled_orders = RepairOrder.find_all(conditions=cancelled_conditions, params=cancelled_params)
        cancelled_count = len(cancelled_orders)
        
        # 维修人员数量
        total_technicians = Technician.find_all(conditions=["status = %s OR status = %s"], params=['active', 'online'])
        
        # 工单类型分布
        type_distribution = []
        type_sql = f"SELECT type, COUNT(*) as count FROM t_repair_order{date_where} GROUP BY type"
        type_result = execute_sql(type_sql, date_params)
        for item in type_result:
            type_name = item['type']
            # 转换类型名称为中文
            type_name_map = {
                'water': '水暖',
                'electric': '电路',
                'gas': '燃气',
                'door': '门窗',
                'elevator': '电梯',
                'cleaning': '保洁',
                'other': '其他',
                'property': '物业',
                'water_elec': '水电维修'
            }
            type_distribution.append({
                'name': type_name_map.get(type_name, type_name),
                'value': item['count']
            })
        
        # 工单趋势
        trend_data = []
        if start_date and end_date:
            trend_sql = f"""
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM t_repair_order 
                {date_where} 
                GROUP BY DATE(created_at) 
                ORDER BY date
            """
        else:
            # 默认最近30天
            trend_sql = """
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM t_repair_order 
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) 
                GROUP BY DATE(created_at) 
                ORDER BY date
            """
            date_params = []
        trend_result = execute_sql(trend_sql, date_params)
        for item in trend_result:
            trend_data.append({
                'date': item['date'].strftime('%Y-%m-%d'),
                'value': item['count']
            })
        
        # 维修人员效率（已完成的工单数量）
        technician_efficiency = []
        if date_conditions:
            # 构建日期条件，不包含 WHERE 关键字，并且明确指定 created_at 列来自 ro 表
            ro_date_conditions = [condition.replace('created_at', 'ro.created_at') for condition in date_conditions]
            date_conditions_str = " AND ".join(ro_date_conditions)
            efficiency_sql = f"""
                SELECT t.name, COUNT(ro.id) as completed_count 
                FROM t_technician t 
                LEFT JOIN t_repair_order ro ON t.id = ro.technician_id AND ro.status = 'completed' AND {date_conditions_str} 
                WHERE t.status = 'active' OR t.status = 'online' 
                GROUP BY t.id, t.name 
                ORDER BY completed_count DESC
            """
        else:
            efficiency_sql = """
                SELECT t.name, COUNT(ro.id) as completed_count 
                FROM t_technician t 
                LEFT JOIN t_repair_order ro ON t.id = ro.technician_id AND ro.status = 'completed' 
                WHERE t.status = 'active' OR t.status = 'online' 
                GROUP BY t.id, t.name 
                ORDER BY completed_count DESC
            """
            date_params = []
        efficiency_result = execute_sql(efficiency_sql, date_params)
        for item in efficiency_result:
            technician_efficiency.append({
                'name': item['name'],
                'value': item['completed_count']
            })
        
        # 详细统计数据
        detail_data = []
        if start_date and end_date:
            detail_sql = f"""
                SELECT 
                    DATE(created_at) as date, 
                    COUNT(*) as total, 
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed, 
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending, 
                    SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing 
                FROM t_repair_order 
                {date_where} 
                GROUP BY DATE(created_at) 
                ORDER BY date
            """
        else:
            # 默认最近7天
            detail_sql = """
                SELECT 
                    DATE(created_at) as date, 
                    COUNT(*) as total, 
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed, 
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending, 
                    SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing 
                FROM t_repair_order 
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) 
                GROUP BY DATE(created_at) 
                ORDER BY date
            """
            date_params = []
        detail_result = execute_sql(detail_sql, date_params)
        for item in detail_result:
            total = item['total']
            completed = item['completed']
            completion_rate = round((completed / total) * 100) if total > 0 else 0
            detail_data.append({
                'date': item['date'].strftime('%Y-%m-%d'),
                'total': total,
                'completed': completed,
                'pending': item['pending'],
                'processing': item['processing'],
                'avg_time': 2.5,  # 暂时使用固定值
                'completion_rate': completion_rate
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'orders': {
                    'total': len(total_orders),
                    'pending': len(pending_orders),
                    'processing': len(processing_orders),
                    'completed': len(completed_orders),
                    'cancelled': len(cancelled_orders)
                },
                'technicians': {
                    'total': len(total_technicians)
                },
                'type_distribution': type_distribution,
                'trend_data': trend_data,
                'technician_efficiency': technician_efficiency,
                'detail_data': detail_data
            }
        })
        
    except Exception as e:
        logger.error(f"获取维修统计数据失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
