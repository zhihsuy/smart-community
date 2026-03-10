# routes/parking.py - 停车管理路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime

parking_bp = Blueprint('parking', __name__, url_prefix='/api/v1/pc/parking')


# ==================== 车位管理 ====================

@parking_bp.route('/spaces', methods=['GET'])
@login_required
def get_parking_spaces():
    """获取车位列表"""
    try:
        building_id = request.args.get('building_id')
        type = request.args.get('type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if building_id:
            conditions.append("building_id = %s")
            params.append(building_id)
        if type:
            conditions.append("type = %s")
            params.append(type)
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        from models.parking import ParkingSpace
        spaces, total = ParkingSpace.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        spaces_list = [space.to_dict() for space in spaces]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': spaces_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取车位列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@parking_bp.route('/spaces', methods=['POST'])
@admin_required
def create_parking_space():
    """创建车位（管理员）"""
    try:
        data = request.get_json()
        
        from models.parking import ParkingSpace
        space = ParkingSpace.create(
            space_code=data.get('space_code'),
            space_name=data.get('space_name'),
            type=data.get('type'),
            location=data.get('location'),
            building_id=data.get('building_id'),
            price=data.get('price'),
            owner_id=data.get('owner_id'),
            status=data.get('status', 'free')
        )
        
        if space:
            return jsonify({
                'code': 0,
                'msg': '创建车位成功',
                'data': space.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建车位失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建车位失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@parking_bp.route('/spaces/<int:space_id>', methods=['PUT'])
@admin_required
def update_parking_space(space_id):
    """更新车位信息（管理员）"""
    try:
        from models.parking import ParkingSpace
        space = ParkingSpace.find_by_id(space_id)
        
        if not space:
            return jsonify({
                'code': 404,
                'msg': '车位不存在',
                'data': None
            })
        
        data = request.get_json()
        success = space.update(
            space_name=data.get('space_name'),
            type=data.get('type'),
            location=data.get('location'),
            building_id=data.get('building_id'),
            price=data.get('price'),
            owner_id=data.get('owner_id'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': space.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新车位失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@parking_bp.route('/spaces/<int:space_id>', methods=['DELETE'])
@admin_required
def delete_parking_space(space_id):
    """删除车位（管理员）"""
    try:
        from models.parking import ParkingSpace
        space = ParkingSpace.find_by_id(space_id)
        
        if not space:
            return jsonify({
                'code': 404,
                'msg': '车位不存在',
                'data': None
            })
        
        success = space.delete()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"删除车位失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


# ==================== 车辆管理 ====================

@parking_bp.route('/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    """获取车辆列表"""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        from models.parking import Vehicle
        vehicles, total = Vehicle.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        vehicles_list = [vehicle.to_dict() for vehicle in vehicles]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': vehicles_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取车辆列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@parking_bp.route('/vehicles', methods=['POST'])
@login_required
def create_vehicle():
    """添加车辆"""
    try:
        data = request.get_json()
        
        from models.parking import Vehicle
        vehicle = Vehicle.create(
            user_id=request.user_id,
            car_number=data.get('car_number'),
            car_brand=data.get('car_brand'),
            car_model=data.get('car_model'),
            car_color=data.get('car_color'),
            status=data.get('status', 'active')
        )
        
        if vehicle:
            return jsonify({
                'code': 0,
                'msg': '添加车辆成功',
                'data': vehicle.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '添加车辆失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"添加车辆失败: {e}")
        return jsonify({'code': 500, 'msg': f'添加失败: {str(e)}', 'data': None})


@parking_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
@login_required
def update_vehicle(vehicle_id):
    """更新车辆信息"""
    try:
        from models.parking import Vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({
                'code': 404,
                'msg': '车辆不存在',
                'data': None
            })
        
        # 检查是否是当前用户的车辆
        if vehicle.user_id != request.user_id:
            return jsonify({
                'code': 403,
                'msg': '无权操作此车辆',
                'data': None
            })
        
        data = request.get_json()
        success = vehicle.update(
            car_number=data.get('car_number'),
            car_brand=data.get('car_brand'),
            car_model=data.get('car_model'),
            car_color=data.get('car_color'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': vehicle.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新车辆失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@parking_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
@login_required
def delete_vehicle(vehicle_id):
    """删除车辆"""
    try:
        from models.parking import Vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({
                'code': 404,
                'msg': '车辆不存在',
                'data': None
            })
        
        # 检查是否是当前用户的车辆
        if vehicle.user_id != request.user_id:
            return jsonify({
                'code': 403,
                'msg': '无权操作此车辆',
                'data': None
            })
        
        success = vehicle.delete()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"删除车辆失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


# ==================== 停车记录管理 ====================

@parking_bp.route('/records', methods=['GET'])
@login_required
def get_parking_records():
    """获取停车记录列表"""
    try:
        user_id = request.args.get('user_id')
        car_number = request.args.get('car_number')
        payment_status = request.args.get('payment_status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
        if car_number:
            conditions.append("car_number LIKE %s")
            params.append(f"%{car_number}%")
        if payment_status:
            conditions.append("payment_status = %s")
            params.append(payment_status)
        if start_date:
            conditions.append("entry_time >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("entry_time <= %s")
            params.append(end_date + ' 23:59:59')
        
        from models.parking import ParkingRecord
        records, total = ParkingRecord.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        records_list = [record.to_dict() for record in records]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': records_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取停车记录列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@parking_bp.route('/records', methods=['POST'])
@login_required
def create_parking_record():
    """创建停车记录（车辆入场）"""
    try:
        data = request.get_json()
        
        # 查找车位
        from models.parking import ParkingSpace
        space = ParkingSpace.find_by_id(data.get('space_id'))
        
        if not space:
            return jsonify({
                'code': 404,
                'msg': '车位不存在',
                'data': None
            })
        
        # 检查车位状态
        if space.status != 'free':
            return jsonify({
                'code': 400,
                'msg': '车位不可用',
                'data': None
            })
        
        # 查找车辆
        vehicle = Vehicle.find_by_car_number(data.get('car_number'))
        user_id = vehicle.user_id if vehicle else None
        
        # 创建停车记录
        record = ParkingRecord.create(
            space_id=data.get('space_id'),
            car_number=data.get('car_number'),
            user_id=user_id
        )
        
        if record:
            # 更新车位状态
            space.update(status='occupied')
            
            return jsonify({
                'code': 0,
                'msg': '车辆入场成功',
                'data': record.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '车辆入场失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建停车记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@parking_bp.route('/records/<int:record_id>/exit', methods=['POST'])
@login_required
def exit_parking_record(record_id):
    """车辆出场"""
    try:
        from models.parking import ParkingRecord
        record = ParkingRecord.find_by_id(record_id)
        
        if not record:
            return jsonify({
                'code': 404,
                'msg': '停车记录不存在',
                'data': None
            })
        
        success = record.exit()
        
        if success:
            # 更新车位状态
            from models.parking import ParkingSpace
            space = ParkingSpace.find_by_id(record.space_id)
            if space:
                space.update(status='free')
            
            return jsonify({
                'code': 0,
                'msg': '车辆出场成功',
                'data': record.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '车辆出场失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"车辆出场失败: {e}")
        return jsonify({'code': 500, 'msg': f'出场失败: {str(e)}', 'data': None})


@parking_bp.route('/records/<int:record_id>/pay', methods=['POST'])
@login_required
def pay_parking_record(record_id):
    """支付停车费用"""
    try:
        from models.parking import ParkingRecord
        record = ParkingRecord.find_by_id(record_id)
        
        if not record:
            return jsonify({
                'code': 404,
                'msg': '停车记录不存在',
                'data': None
            })
        
        success = record.pay()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '支付成功',
                'data': record.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '支付失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"支付停车费用失败: {e}")
        return jsonify({'code': 500, 'msg': f'支付失败: {str(e)}', 'data': None})


# ==================== 停车统计 ====================

@parking_bp.route('/statistics', methods=['GET'])
@login_required
def get_parking_statistics():
    """获取停车统计"""
    try:
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询条件
        conditions = []
        params = []
        
        if start_date:
            conditions.append("entry_time >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("entry_time <= %s")
            params.append(end_date + ' 23:59:59')
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # 总停车次数
        total_sql = f"SELECT COUNT(*) as count FROM t_parking_record{where_clause}"
        total_result = execute_sql(total_sql, tuple(params))
        total_count = total_result[0]['count'] if total_result else 0
        
        # 总停车时长（小时）
        duration_sql = f"SELECT SUM(duration) as total_duration FROM t_parking_record{where_clause}"
        duration_result = execute_sql(duration_sql, tuple(params))
        total_duration = duration_result[0]['total_duration'] if duration_result and duration_result[0]['total_duration'] else 0
        total_hours = round(total_duration / 60, 2)
        
        # 总停车费用
        fee_sql = f"SELECT SUM(fee) as total_fee FROM t_parking_record{where_clause} WHERE payment_status = 'paid'"
        fee_result = execute_sql(fee_sql, tuple(params))
        total_fee = fee_result[0]['total_fee'] if fee_result and fee_result[0]['total_fee'] else 0
        
        # 待支付费用
        unpaid_sql = f"SELECT SUM(fee) as unpaid_fee FROM t_parking_record{where_clause} WHERE payment_status = 'unpaid'"
        unpaid_result = execute_sql(unpaid_sql, tuple(params))
        unpaid_fee = unpaid_result[0]['unpaid_fee'] if unpaid_result and unpaid_result[0]['unpaid_fee'] else 0
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'total_count': total_count,
                'total_hours': total_hours,
                'total_fee': float(total_fee),
                'unpaid_fee': float(unpaid_fee)
            }
        })
        
    except Exception as e:
        logger.error(f"获取停车统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
