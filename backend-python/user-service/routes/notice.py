# routes/notice.py - 公告管理相关API路由
from flask import Blueprint, request, jsonify
from utils.jwt_util import login_required, admin_required
from config.database import execute_sql, logger
from datetime import datetime

notice_bp = Blueprint('notice', __name__, url_prefix='/api/v1/pc/notices')


# ==================== 公告管理 ====================

@notice_bp.route('', methods=['GET'])
@login_required
def get_notices():
    """获取公告列表"""
    try:
        title = request.args.get('title')
        type = request.args.get('type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if title:
            conditions.append("title LIKE %s")
            params.append(f"%{title}%")
        if type:
            conditions.append("type = %s")
            params.append(type)
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        from models.notice import Notice
        notices, total = Notice.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        notices_list = [notice.to_dict() for notice in notices]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': notices_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取公告列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@notice_bp.route('', methods=['POST'])
@admin_required
def create_notice():
    """创建公告"""
    try:
        data = request.get_json()
        
        from models.notice import Notice
        notice = Notice.create(
            title=data.get('title'),
            type=data.get('type'),
            content=data.get('content'),
            author=data.get('author'),
            author_id=request.user_id,
            publish_time=datetime.now(),
            expire_time=data.get('expire_time'),
            status=data.get('status', 'published')
        )
        
        if notice:
            return jsonify({
                'code': 0,
                'msg': '创建公告成功',
                'data': notice.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '创建公告失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建公告失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})


@notice_bp.route('/<int:notice_id>', methods=['GET'])
@login_required
def get_notice_detail(notice_id):
    """获取公告详情"""
    try:
        from models.notice import Notice
        notice = Notice.find_by_id(notice_id)
        
        if notice:
            # 增加浏览量
            notice.increment_view_count()
            
            return jsonify({
                'code': 0,
                'msg': '获取成功',
                'data': notice.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '公告不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取公告详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})


@notice_bp.route('/<int:notice_id>', methods=['PUT'])
@admin_required
def update_notice(notice_id):
    """更新公告"""
    try:
        from models.notice import Notice
        notice = Notice.find_by_id(notice_id)
        
        if not notice:
            return jsonify({
                'code': 404,
                'msg': '公告不存在',
                'data': None
            })
        
        data = request.get_json()
        success = notice.update(
            title=data.get('title'),
            type=data.get('type'),
            content=data.get('content'),
            author=data.get('author'),
            expire_time=data.get('expire_time'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': notice.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新公告失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})


@notice_bp.route('/<int:notice_id>', methods=['DELETE'])
@admin_required
def delete_notice(notice_id):
    """删除公告"""
    try:
        from models.notice import Notice
        notice = Notice.find_by_id(notice_id)
        
        if not notice:
            return jsonify({
                'code': 404,
                'msg': '公告不存在',
                'data': None
            })
        
        success = notice.delete()
        
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
        logger.error(f"删除公告失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})


@notice_bp.route('/<int:notice_id>/publish', methods=['POST'])
@admin_required
def publish_notice(notice_id):
    """发布公告"""
    try:
        from models.notice import Notice
        notice = Notice.find_by_id(notice_id)
        
        if not notice:
            return jsonify({
                'code': 404,
                'msg': '公告不存在',
                'data': None
            })
        
        success = notice.publish()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '发布成功',
                'data': notice.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '发布失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"发布公告失败: {e}")
        return jsonify({'code': 500, 'msg': f'发布失败: {str(e)}', 'data': None})


@notice_bp.route('/<int:notice_id>/unpublish', methods=['POST'])
@admin_required
def unpublish_notice(notice_id):
    """取消发布"""
    try:
        from models.notice import Notice
        notice = Notice.find_by_id(notice_id)
        
        if not notice:
            return jsonify({
                'code': 404,
                'msg': '公告不存在',
                'data': None
            })
        
        success = notice.unpublish()
        
        if success:
            return jsonify({
                'code': 0,
                'msg': '取消发布成功',
                'data': notice.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '取消发布失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"取消发布失败: {e}")
        return jsonify({'code': 500, 'msg': f'取消发布失败: {str(e)}', 'data': None})
