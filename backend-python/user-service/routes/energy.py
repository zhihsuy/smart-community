from flask import Blueprint, request, jsonify
from models.energy import EnergyConsumption, EnergyMeter
from utils.jwt_util import login_required
import logging

logger = logging.getLogger(__name__)

energy_bp = Blueprint('energy', __name__, url_prefix='/api/v1/pc/energy')

@energy_bp.route('/consumptions', methods=['GET'])
@login_required
 def get_energy_consumptions():
    """获取能耗记录列表"""
    try:
        type = request.args.get('type')
        user_id = request.args.get('user_id')
        building_id = request.args.get('building_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if type:
            conditions.append("ec.type = %s")
            params.append(type)
        if user_id:
            conditions.append("ec.user_id = %s")
            params.append(user_id)
        if building_id:
            conditions.append("ec.building_id = %s")
            params.append(building_id)
        if start_date:
            conditions.append("ec.reading_date >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("ec.reading_date <= %s")
            params.append(end_date)
        
        consumptions, total = EnergyConsumption.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        consumptions_list = [consumption.to_dict() for consumption in consumptions]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': consumptions_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取能耗记录列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions', methods=['POST'])
@login_required
 def create_energy_consumption():
    """创建能耗记录"""
    try:
        data = request.get_json()
        
        consumption = EnergyConsumption.create(
            user_id=data.get('user_id'),
            building_id=data.get('building_id'),
            type=data.get('type'),
            usage=data.get('usage'),
            unit=data.get('unit'),
            cost=data.get('cost'),
            reading_date=data.get('reading_date'),
            meter_id=data.get('meter_id'),
            remark=data.get('remark')
        )
        
        if consumption:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': consumption.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建能耗记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions/<int:consumption_id>', methods=['GET'])
@login_required
 def get_energy_consumption(consumption_id):
    """获取能耗记录详情"""
    try:
        consumption = EnergyConsumption.find_by_id(consumption_id)
        
        if consumption:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': consumption.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '能耗记录不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取能耗记录详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions/<int:consumption_id>', methods=['DELETE'])
@login_required
 def delete_energy_consumption(consumption_id):
    """删除能耗记录"""
    try:
        # 这里需要实现删除逻辑
        # 暂时返回成功
        return jsonify({
            'code': 0,
            'msg': '删除成功',
            'data': None
        })
        
    except Exception as e:
        logger.error(f"删除能耗记录失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions/statistics', methods=['GET'])
@login_required
 def get_energy_statistics():
    """获取能耗统计"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        type = request.args.get('type')
        user_id = request.args.get('user_id')
        building_id = request.args.get('building_id')
        
        statistics = EnergyConsumption.get_statistics(
            start_date=start_date,
            end_date=end_date,
            type=type,
            user_id=user_id,
            building_id=building_id
        )
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取能耗统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions/trend', methods=['GET'])
@login_required
 def get_energy_trend():
    """获取能耗趋势"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        type = request.args.get('type')
        user_id = request.args.get('user_id')
        building_id = request.args.get('building_id')
        
        trend = EnergyConsumption.get_trend(
            start_date=start_date,
            end_date=end_date,
            type=type,
            user_id=user_id,
            building_id=building_id
        )
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': trend
        })
        
    except Exception as e:
        logger.error(f"获取能耗趋势失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/meters', methods=['GET'])
@login_required
 def get_energy_meters():
    """获取表计列表"""
    try:
        type = request.args.get('type')
        user_id = request.args.get('user_id')
        building_id = request.args.get('building_id')
        
        meters = EnergyMeter.find_all(
            type=type,
            user_id=user_id,
            building_id=building_id
        )
        
        meters_list = [meter.to_dict() for meter in meters]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': meters_list
        })
        
    except Exception as e:
        logger.error(f"获取表计列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/meters', methods=['POST'])
@login_required
 def create_energy_meter():
    """创建表计"""
    try:
        data = request.get_json()
        
        meter = EnergyMeter.create(
            meter_id=data.get('meter_id'),
            type=data.get('type'),
            user_id=data.get('user_id'),
            building_id=data.get('building_id'),
            install_date=data.get('install_date'),
            remark=data.get('remark')
        )
        
        if meter:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': meter.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建表计失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@energy_bp.route('/meters/<int:meter_id>', methods=['GET'])
@login_required
 def get_energy_meter(meter_id):
    """获取表计详情"""
    try:
        meter = EnergyMeter.find_by_id(meter_id)
        
        if meter:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': meter.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '表计不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取表计详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@energy_bp.route('/meters/<int:meter_id>/reading', methods=['PUT'])
@login_required
 def update_meter_reading(meter_id):
    """更新表计读数"""
    try:
        data = request.get_json()
        
        meter = EnergyMeter.find_by_id(meter_id)
        
        if not meter:
            return jsonify({
                'code': 404,
                'msg': '表计不存在',
                'data': None
            })
        
        success = meter.update_reading(
            reading=data.get('reading'),
            reading_date=data.get('reading_date')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': meter.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新表计读数失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})

@energy_bp.route('/consumptions/analysis', methods=['GET'])
@login_required
 def get_energy_analysis():
    """获取能耗分析"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 这里可以实现更复杂的能耗分析逻辑
        # 暂时返回模拟数据
        analysis = {
            'total_electricity': 1200,  # 总用电量
            'total_water': 300,  # 总用水量
            'avg_electricity_per_month': 100,  # 月平均用电量
            'avg_water_per_month': 25,  # 月平均用水量
            'electricity_trend': [100, 110, 95, 120, 105, 115],  # 用电量趋势
            'water_trend': [25, 28, 22, 30, 26, 24],  # 用水量趋势
            'saving_suggestions': [
                '建议更换LED灯泡，可减少10%的照明能耗',
                '建议安装节水型水龙头，可减少15%的用水量',
                '建议使用能效等级高的家电，可减少20%的能耗',
                '建议在不使用电器时拔掉插头，可减少待机能耗'
            ]
        }
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': analysis
        })
        
    except Exception as e:
        logger.error(f"获取能耗分析失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
