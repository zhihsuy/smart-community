from flask import Blueprint, request, jsonify
from models.activity import Activity, ActivityParticipant, ActivityStatistics
from utils.jwt_util import login_required
import logging

logger = logging.getLogger(__name__)

activity_bp = Blueprint('activity', __name__, url_prefix='/api/v1/pc/activities')

@activity_bp.route('', methods=['GET'])
@login_required
def get_activities():
    """获取活动列表"""
    try:
        status = request.args.get('status')
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        activities, total = Activity.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        activities_list = [activity.to_dict() for activity in activities]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': activities_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取活动列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@activity_bp.route('', methods=['POST'])
@login_required
def create_activity():
    """创建活动"""
    try:
        data = request.get_json()
        
        activity = Activity.create(
            title=data.get('title'),
            description=data.get('description'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            location=data.get('location'),
            max_participants=data.get('max_participants'),
            organizer=data.get('organizer'),
            contact_phone=data.get('contact_phone'),
            category=data.get('category'),
            tags=data.get('tags'),
            image_url=data.get('image_url'),
            remark=data.get('remark')
        )
        
        if activity:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': activity.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    """获取活动详情"""
    try:
        activity = Activity.find_by_id(activity_id)
        
        if activity:
            # 获取活动统计数据
            statistics = ActivityStatistics.get_activity_statistics(activity_id)
            activity_data = activity.to_dict()
            activity_data['statistics'] = statistics
            
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': activity_data
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取活动详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>', methods=['PUT'])
@login_required
def update_activity(activity_id):
    """更新活动"""
    try:
        data = request.get_json()
        
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
        success = activity.update(**data)
        
        if success:
            updated_activity = Activity.find_by_id(activity_id)
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': updated_activity.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>/publish', methods=['POST'])
@login_required
def publish_activity(activity_id):
    """发布活动"""
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
        success = activity.publish()
        
        if success:
            updated_activity = Activity.find_by_id(activity_id)
            return jsonify({
                'code': 0,
                'msg': '发布成功',
                'data': updated_activity.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '发布失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"发布活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'发布失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>/cancel', methods=['POST'])
@login_required
def cancel_activity(activity_id):
    """取消活动"""
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
        success = activity.cancel()
        
        if success:
            updated_activity = Activity.find_by_id(activity_id)
            return jsonify({
                'code': 0,
                'msg': '取消成功',
                'data': updated_activity.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '取消失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"取消活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'取消失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>/complete', methods=['POST'])
@login_required
def complete_activity(activity_id):
    """完成活动"""
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
        success = activity.complete()
        
        if success:
            updated_activity = Activity.find_by_id(activity_id)
            return jsonify({
                'code': 0,
                'msg': '完成成功',
                'data': updated_activity.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '完成失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"完成活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'完成失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    """删除活动"""
    try:
        activity = Activity.find_by_id(activity_id)
        
        if not activity:
            return jsonify({
                'code': 404,
                'msg': '活动不存在',
                'data': None
            })
        
        success = activity.delete()
        
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
        logger.error(f"删除活动失败: {e}")
        return jsonify({'code': 500, 'msg': f'删除失败: {str(e)}', 'data': None})

@activity_bp.route('/upload-image', methods=['POST'])
@login_required
def upload_activity_image():
    """上传活动图片"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'msg': '请选择要上传的文件',
                'data': None
            })
        
        file = request.files['file']
        
        # 检查文件是否为空
        if file.filename == '':
            return jsonify({
                'code': 400,
                'msg': '请选择要上传的文件',
                'data': None
            })
        
        # 检查文件类型
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({
                'code': 400,
                'msg': '只支持上传图片文件',
                'data': None
            })
        
        # 检查文件大小
        if file.content_length > 5 * 1024 * 1024:  # 5MB
            return jsonify({
                'code': 400,
                'msg': '图片大小不能超过5MB',
                'data': None
            })
        
        # 创建上传目录
        import os
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'activity_images')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
        
        # 生成文件名
        import uuid
        ext = os.path.splitext(file.filename)[1]
        filename = f"activity_{uuid.uuid4()}{ext}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        file.save(file_path)
        
        # 生成访问路径
        base_url = f"http://{request.host}"
        image_url = f"{base_url}/static/activity_images/{filename}"
        
        return jsonify({
            'code': 0,
            'msg': '图片上传成功',
            'data': {
                'imageUrl': image_url
            }
        })
        
    except Exception as e:
        logger.error(f"上传活动图片失败: {e}")
        return jsonify({'code': 500, 'msg': f'上传失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>/participants', methods=['GET'])
@login_required
def get_activity_participants(activity_id):
    """获取活动参与者列表"""
    try:
        participants = ActivityParticipant.find_by_activity(activity_id)
        
        participants_list = [participant.to_dict() for participant in participants]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': participants_list
        })
        
    except Exception as e:
        logger.error(f"获取活动参与者列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@activity_bp.route('/<int:activity_id>/participants', methods=['POST'])
@login_required
def add_activity_participant(activity_id):
    """添加活动参与者"""
    try:
        data = request.get_json()
        
        participant = ActivityParticipant.create(
            activity_id=activity_id,
            user_id=data.get('user_id'),
            user_name=data.get('user_name'),
            user_phone=data.get('user_phone'),
            remark=data.get('remark')
        )
        
        if participant:
            return jsonify({
                'code': 0,
                'msg': '报名成功',
                'data': participant.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '报名失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"添加活动参与者失败: {e}")
        return jsonify({'code': 500, 'msg': f'报名失败: {str(e)}', 'data': None})

@activity_bp.route('/participants/<int:participant_id>/sign-in', methods=['POST'])
@login_required
def sign_in_participant(participant_id):
    """参与者签到"""
    try:
        participant = ActivityParticipant.find_by_id(participant_id)
        
        if not participant:
            return jsonify({
                'code': 404,
                'msg': '参与者不存在',
                'data': None
            })
        
        success = participant.sign_in()
        
        if success:
            updated_participant = ActivityParticipant.find_by_id(participant_id)
            return jsonify({
                'code': 0,
                'msg': '签到成功',
                'data': updated_participant.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '签到失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"参与者签到失败: {e}")
        return jsonify({'code': 500, 'msg': f'签到失败: {str(e)}', 'data': None})

@activity_bp.route('/statistics', methods=['GET'])
@login_required
def get_activity_statistics():
    """获取活动统计"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        statistics = ActivityStatistics.get_overall_statistics(
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取活动统计失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
