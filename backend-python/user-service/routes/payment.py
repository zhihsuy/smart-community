# routes/payment.py - 缴费管理相关API路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/pc/payments')


# ==================== 缴费管理 ====================

@payment_bp.route('', methods=['GET'])
@login_required
def get_payments():
    """获取缴费记录列表"""
    try:
        status = request.args.get('status')
        type = request.args.get('type')
        fee_type = request.args.get('fee_type')
        user_id = request.args.get('user_id')
        building_id = request.args.get('building_id')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if status:
            conditions.append("p.status = %s")
            params.append(status)
        if type:
            conditions.append("p.type = %s")
            params.append(type)
        if fee_type:
            conditions.append("p.fee_type = %s")
            params.append(fee_type)
        if user_id:
            conditions.append("p.user_id = %s")
            params.append(user_id)
        if building_id:
            conditions.append("p.building_id = %s")
            params.append(building_id)
        
        from models.payment import Payment
        payments, total = Payment.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        payments_list = [payment.to_dict() for payment in payments]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': payments_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取缴费记录列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@payment_bp.route('', methods=['POST'])
@admin_required
def create_payment():
    """创建缴费记录"""
    try:
        data = request.get_json()
        
        from models.payment import Payment
        payment = Payment.create(
            user_id=data.get('user_id'),
            building_id=data.get('building_id'),
            type=data.get('type'),
            fee_type=data.get('fee_type'),
            amount=data.get('amount'),
            period_start=data.get('period_start'),
            period_end=data.get('period_end'),
            due_date=data.get('due_date'),
            remark=data.get('remark')
        )
        
        if payment:
            return jsonify({
                'code': 0,
                'msg': '创建缴费记录成功',
                'data': payment.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建缴费记录失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建缴费记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@payment_bp.route('/<int:payment_id>', methods=['GET'])
@login_required
def get_payment_detail(payment_id):
    """获取缴费记录详情"""
    try:
        from models.payment import Payment
        payment = Payment.find_by_id(payment_id)
        
        if payment:
            return jsonify({
                'code': 0,
                'msg': '获取成功',
                'data': payment.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '缴费记录不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取缴费记录详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@payment_bp.route('/<int:payment_id>', methods=['PUT'])
@admin_required
def update_payment(payment_id):
    """更新缴费记录"""
    try:
        from models.payment import Payment
        payment = Payment.find_by_id(payment_id)
        
        if not payment:
            return jsonify({
                'code': 404,
                'msg': '缴费记录不存在',
                'data': None
            })
        
        data = request.get_json()
        success = payment.update(
            type=data.get('type'),
            fee_type=data.get('fee_type'),
            amount=data.get('amount'),
            period_start=data.get('period_start'),
            period_end=data.get('period_end'),
            due_date=data.get('due_date'),
            remark=data.get('remark')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': payment.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新缴费记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
@admin_required
def delete_payment(payment_id):
    """删除缴费记录"""
    try:
        from models.payment import Payment
        payment = Payment.find_by_id(payment_id)
        
        if not payment:
            return jsonify({
                'code': 404,
                'msg': '缴费记录不存在',
                'data': None
            })
        
        success = payment.delete()
        
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
        logger.error(f"删除缴费记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


@payment_bp.route('/<int:payment_id>/pay', methods=['POST'])
@login_required
def pay_payment(payment_id):
    """缴费"""
    try:
        data = request.get_json()
        
        from models.payment import Payment
        payment = Payment.find_by_id(payment_id)
        
        if not payment:
            return jsonify({
                'code': 404,
                'msg': '缴费记录不存在',
                'data': None
            })
        
        success = payment.pay(
            paid_amount=data.get('paid_amount'),
            payment_method=data.get('payment_method'),
            transaction_id=data.get('transaction_id')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '缴费成功',
                'data': payment.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '缴费失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"缴费失败: {e}")
        return jsonify({'code': 500, 'msg': f'缴费失败: {str(e)}', 'data': None})


@payment_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """获取缴费统计"""
    try:
        from models.payment import Payment
        statistics = Payment.get_statistics()
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取缴费统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@payment_bp.route('/statistics/by-type', methods=['GET'])
@login_required
def get_statistics_by_type():
    """按类型获取缴费统计"""
    try:
        from models.payment import Payment
        statistics = Payment.get_statistics_by_type()
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取缴费统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 费用类型管理 ====================

@payment_bp.route('/fee-types', methods=['GET'])
@login_required
def get_fee_types():
    """获取费用类型列表"""
    try:
        type = request.args.get('type')
        
        from models.payment import FeeType
        fee_types = FeeType.find_all(type=type)
        
        fee_types_list = [fee_type.to_dict() for fee_type in fee_types]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': fee_types_list
        })
        
    except Exception as e:
        logger.error(f"获取费用类型列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@payment_bp.route('/fee-types', methods=['POST'])
@admin_required
def create_fee_type():
    """创建费用类型"""
    try:
        data = request.get_json()
        
        from models.payment import FeeType
        fee_type = FeeType.create(
            name=data.get('name'),
            code=data.get('code'),
            type=data.get('type'),
            unit_price=data.get('unit_price'),
            unit=data.get('unit'),
            description=data.get('description')
        )
        
        if fee_type:
            return jsonify({
                'code': 0,
                'msg': '创建费用类型成功',
                'data': fee_type.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建费用类型失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建费用类型失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@payment_bp.route('/fee-types/<int:fee_type_id>', methods=['PUT'])
@admin_required
def update_fee_type(fee_type_id):
    """更新费用类型"""
    try:
        from models.payment import FeeType
        fee_type = FeeType.find_by_id(fee_type_id)
        
        if not fee_type:
            return jsonify({
                'code': 404,
                'msg': '费用类型不存在',
                'data': None
            })
        
        data = request.get_json()
        success = fee_type.update(
            name=data.get('name'),
            code=data.get('code'),
            type=data.get('type'),
            unit_price=data.get('unit_price'),
            unit=data.get('unit'),
            description=data.get('description'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': fee_type.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新费用类型失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@payment_bp.route('/fee-types/<int:fee_type_id>', methods=['DELETE'])
@admin_required
def delete_fee_type(fee_type_id):
    """删除费用类型"""
    try:
        from models.payment import FeeType
        fee_type = FeeType.find_by_id(fee_type_id)
        
        if not fee_type:
            return jsonify({
                'code': 404,
                'msg': '费用类型不存在',
                'data': None
            })
        
        success = fee_type.delete()
        
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
        logger.error(f"删除费用类型失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})
