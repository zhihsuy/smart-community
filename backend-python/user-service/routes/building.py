# routes/building.py - 楼栋查询路由
from flask import Blueprint, request, jsonify
from models.building import Building
from utils.jwt_util import login_required, op_required
from config.database import logger

building_bp = Blueprint('building', __name__, url_prefix='/api/v1/<platform_type>/building')


@building_bp.route('/list', methods=['GET'])
@login_required
def list_buildings(platform_type):
    """获取楼栋列表"""
    try:
        # 获取社区ID参数
        community_id = request.args.get('community_id', 1, type=int)
        
        # 查询楼栋列表
        buildings = Building.find_by_community(community_id)
        
        # 转换为字典列表
        result = [building.to_dict() for building in buildings]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"获取楼栋列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@building_bp.route('/<int:building_id>', methods=['GET'])
@login_required
def get_building_by_id(platform_type, building_id):
    """根据ID获取楼栋详情"""
    try:
        building = Building.find_by_id(building_id)
        
        if not building:
            return jsonify({
                'code': 404,
                'msg': '楼栋不存在',
                'data': None
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': building.to_dict()
        })
    
    except Exception as e:
        logger.error(f"获取楼栋详情失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@building_bp.route('/all', methods=['GET'])
def get_all_buildings(platform_type):
    """获取所有楼栋（无需登录，用于注册时选择）"""
    try:
        buildings = Building.list_all()
        result = [building.to_dict() for building in buildings]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"获取所有楼栋失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


# ==================== 运营接口 ====================

@building_bp.route('/op/list', methods=['GET'])
@op_required
def list_op_buildings(platform_type):
    """获取楼栋列表（运营）"""
    try:
        # 获取社区ID参数
        community_id = request.args.get('community_id', 1, type=int)
        
        # 查询楼栋列表
        buildings = Building.find_by_community(community_id)
        
        # 转换为字典列表
        result = [building.to_dict() for building in buildings]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"获取楼栋列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })
