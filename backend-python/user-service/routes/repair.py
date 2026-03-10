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
        
        total_orders = RepairOrder.find_all()
        pending_orders = RepairOrder.find_all(conditions=["status = %s"], params=['pending'])
        processing_orders = RepairOrder.find_all(conditions=["status = %s"], params=['processing'])
        completed_orders = RepairOrder.find_all(conditions=["status = %s"], params=['completed'])
        cancelled_orders = RepairOrder.find_all(conditions=["status = %s"], params=['cancelled'])
        
        from models.repair import Technician
        total_technicians = Technician.find_all(conditions=["status = %s"], params=['active'])
        
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
                }
            }
        })
        
    except Exception as e:
        logger.error(f"获取维修统计数据失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
