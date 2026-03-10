# routes/complaint.py - 投诉建议管理相关API路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime

complaint_bp = Blueprint('complaint', __name__, url_prefix='/api/v1/pc/complaints')


# ==================== 投诉建议管理 ====================

@complaint_bp.route('', methods=['GET'])
@login_required
def get_complaints():
    """获取投诉建议列表"""
    try:
        status = request.args.get('status')
        type = request.args.get('type')
        category = request.args.get('category')
        priority = request.args.get('priority')
        user_id = request.args.get('user_id')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if status:
            conditions.append("c.status = %s")
            params.append(status)
        if type:
            conditions.append("c.type = %s")
            params.append(type)
        if category:
            conditions.append("c.category = %s")
            params.append(category)
        if priority:
            conditions.append("c.priority = %s")
            params.append(priority)
        if user_id:
            conditions.append("c.user_id = %s")
            params.append(user_id)
        
        from models.complaint import Complaint
        complaints, total = Complaint.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        complaints_list = [complaint.to_dict() for complaint in complaints]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': complaints_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取投诉建议列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@complaint_bp.route('', methods=['POST'])
@login_required
def create_complaint():
    """创建投诉建议"""
    try:
        data = request.get_json()
        
        from models.complaint import Complaint
        complaint = Complaint.create(
            user_id=request.user_id,
            title=data.get('title'),
            type=data.get('type'),
            category=data.get('category'),
            content=data.get('content'),
            address=data.get('address'),
            images=data.get('images'),
            priority=data.get('priority', 'medium')
        )
        
        if complaint:
            return jsonify({
                'code': 0,
                'msg': '提交投诉建议成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '提交投诉建议失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建投诉建议失败: {e}")
        return jsonify({'code': 500, 'msg': f'提交失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>', methods=['GET'])
@login_required
def get_complaint_detail(complaint_id):
    """获取投诉建议详情"""
    try:
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if complaint:
            return jsonify({
                'code': 0,
                'msg': '获取成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取投诉建议详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>', methods=['PUT'])
@login_required
def update_complaint(complaint_id):
    """更新投诉建议"""
    try:
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if not complaint:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
        data = request.get_json()
        success = complaint.update(
            title=data.get('title'),
            type=data.get('type'),
            category=data.get('category'),
            content=data.get('content'),
            address=data.get('address'),
            images=data.get('images'),
            priority=data.get('priority')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新投诉建议失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>', methods=['DELETE'])
@admin_required
def delete_complaint(complaint_id):
    """删除投诉建议"""
    try:
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if not complaint:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
        success = complaint.delete()
        
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
        logger.error(f"删除投诉建议失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>/assign', methods=['POST'])
@admin_required
def assign_handler(complaint_id):
    """分配处理人员"""
    try:
        data = request.get_json()
        
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if not complaint:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
        success = complaint.assign_handler(
            handler_id=data.get('handler_id'),
            handler_name=data.get('handler_name')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '分配成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '分配失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"分配处理人员失败: {e}")
        return jsonify({'code': 500, 'msg': f'分配失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>/handle', methods=['POST'])
@admin_required
def handle_complaint(complaint_id):
    """处理投诉建议"""
    try:
        data = request.get_json()
        
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if not complaint:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
        success = complaint.handle(
            handle_result=data.get('handle_result'),
            handler_id=request.user_id
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '处理成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '处理失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"处理投诉建议失败: {e}")
        return jsonify({'code': 500, 'msg': f'处理失败: {str(e)}', 'data': None})


@complaint_bp.route('/<int:complaint_id>/satisfaction', methods=['POST'])
@login_required
def submit_satisfaction(complaint_id):
    """提交满意度评价"""
    try:
        data = request.get_json()
        
        from models.complaint import Complaint
        complaint = Complaint.find_by_id(complaint_id)
        
        if not complaint:
            return jsonify({
                'code': 404,
                'msg': '投诉建议不存在',
                'data': None
            })
        
        success = complaint.submit_satisfaction(
            satisfaction=data.get('satisfaction'),
            comment=data.get('comment')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '评价提交成功',
                'data': complaint.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '评价提交失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"提交满意度评价失败: {e}")
        return jsonify({'code': 500, 'msg': f'提交失败: {str(e)}', 'data': None})


@complaint_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """获取投诉建议统计"""
    try:
        from models.complaint import Complaint
        statistics = Complaint.get_statistics()
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取投诉建议统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


# ==================== 投诉分类管理 ====================

@complaint_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """获取投诉分类列表"""
    try:
        from models.complaint import ComplaintCategory
        categories = ComplaintCategory.find_all()
        
        categories_list = [category.to_dict() for category in categories]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': categories_list
        })
        
    except Exception as e:
        logger.error(f"获取投诉分类列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@complaint_bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    """创建投诉分类"""
    try:
        data = request.get_json()
        
        from models.complaint import ComplaintCategory
        category = ComplaintCategory.create(
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            sort_order=data.get('sort_order', 0)
        )
        
        if category:
            return jsonify({
                'code': 0,
                'msg': '创建分类成功',
                'data': category.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建分类失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建投诉分类失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@complaint_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """更新投诉分类"""
    try:
        from models.complaint import ComplaintCategory
        category = ComplaintCategory.find_by_id(category_id)
        
        if not category:
            return jsonify({
                'code': 404,
                'msg': '分类不存在',
                'data': None
            })
        
        data = request.get_json()
        success = category.update(
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            sort_order=data.get('sort_order'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': category.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新投诉分类失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@complaint_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """删除投诉分类"""
    try:
        from models.complaint import ComplaintCategory
        category = ComplaintCategory.find_by_id(category_id)
        
        if not category:
            return jsonify({
                'code': 404,
                'msg': '分类不存在',
                'data': None
            })
        
        success = category.delete()
        
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
        logger.error(f"删除投诉分类失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})
