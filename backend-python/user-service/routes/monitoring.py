from flask import Blueprint, request, jsonify
from models.monitoring import MonitoringDevice, AlertRule, AlertRecord, MonitoringRequest
from utils.jwt_util import login_required
import logging

logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/api/v1/pc/monitoring')

@monitoring_bp.route('/devices', methods=['GET'])
@login_required
def get_monitoring_devices():
    """获取监控设备列表"""
    try:
        type = request.args.get('type')
        status = request.args.get('status')
        location = request.args.get('location')
        
        devices = MonitoringDevice.find_all(
            type=type,
            status=status,
            location=location
        )
        
        devices_list = [device.to_dict() for device in devices]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': devices_list
        })
        
    except Exception as e:
        logger.error(f"获取监控设备列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@monitoring_bp.route('/devices', methods=['POST'])
@login_required
def create_monitoring_device():
    """创建监控设备"""
    try:
        data = request.get_json()
        
        device = MonitoringDevice.create(
            device_id=data.get('device_id'),
            name=data.get('name'),
            type=data.get('type'),
            location=data.get('location'),
            ip_address=data.get('ip_address'),
            port=data.get('port'),
            stream_url=data.get('stream_url'),
            username=data.get('username'),
            password=data.get('password'),
            resolution=data.get('resolution'),
            remark=data.get('remark')
        )
        
        if device:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': device.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建监控设备失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@monitoring_bp.route('/devices/<int:device_id>', methods=['GET'])
@login_required
def get_monitoring_device(device_id):
    """获取监控设备详情"""
    try:
        device = MonitoringDevice.find_by_id(device_id)
        
        if device:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': device.to_dict()
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"获取监控设备详情失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@monitoring_bp.route('/devices/<int:device_id>/status', methods=['PUT'])
@login_required
def update_device_status(device_id):
    """更新设备状态"""
    try:
        data = request.get_json()
        
        device = MonitoringDevice.find_by_id(device_id)
        
        if not device:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
        success = device.update_status(data.get('status'))
        
        if success:
            updated_device = MonitoringDevice.find_by_id(device_id)
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': updated_device.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"更新设备状态失败: {e}")
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}', 'data': None})

@monitoring_bp.route('/rules', methods=['GET'])
@login_required
def get_alert_rules():
    """获取预警规则列表"""
    try:
        device_id = request.args.get('device_id')
        type = request.args.get('type')
        enabled = request.args.get('enabled')
        
        rules = AlertRule.find_all(
            device_id=device_id,
            type=type,
            enabled=enabled
        )
        
        rules_list = [rule.to_dict() for rule in rules]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': rules_list
        })
        
    except Exception as e:
        logger.error(f"获取预警规则列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@monitoring_bp.route('/rules', methods=['POST'])
@login_required
def create_alert_rule():
    """创建预警规则"""
    try:
        data = request.get_json()
        
        rule = AlertRule.create(
            name=data.get('name'),
            type=data.get('type'),
            device_id=data.get('device_id'),
            threshold=data.get('threshold'),
            description=data.get('description')
        )
        
        if rule:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': rule.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建预警规则失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@monitoring_bp.route('/rules/<int:rule_id>/toggle', methods=['POST'])
@login_required
def toggle_alert_rule(rule_id):
    """切换预警规则状态"""
    try:
        rule = AlertRule.find_by_id(rule_id)
        
        if not rule:
            return jsonify({
                'code': 404,
                'msg': '规则不存在',
                'data': None
            })
        
        success = rule.toggle()
        
        if success:
            updated_rule = AlertRule.find_by_id(rule_id)
            return jsonify({
                'code': 0,
                'msg': '切换成功',
                'data': updated_rule.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '切换失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"切换预警规则状态失败: {e}")
        return jsonify({'code': 500, 'msg': f'切换失败: {str(e)}', 'data': None})

@monitoring_bp.route('/alerts', methods=['GET'])
@login_required
def get_alert_records():
    """获取预警记录列表"""
    try:
        device_id = request.args.get('device_id')
        type = request.args.get('type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if device_id:
            conditions.append("ar.device_id = %s")
            params.append(device_id)
        if type:
            conditions.append("ar.type = %s")
            params.append(type)
        if status:
            conditions.append("ar.status = %s")
            params.append(status)
        
        alerts, total = AlertRecord.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        alerts_list = [alert.to_dict() for alert in alerts]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': alerts_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取预警记录列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@monitoring_bp.route('/alerts/<int:alert_id>/process', methods=['POST'])
@login_required
def process_alert(alert_id):
    """处理预警"""
    try:
        data = request.get_json()
        
        alert = AlertRecord.find_by_id(alert_id)
        
        if not alert:
            return jsonify({
                'code': 404,
                'msg': '预警记录不存在',
                'data': None
            })
        
        success = alert.process(
            processed_by=data.get('processed_by'),
            process_note=data.get('process_note')
        )
        
        if success:
            updated_alert = AlertRecord.find_by_id(alert_id)
            return jsonify({
                'code': 0,
                'msg': '处理成功',
                'data': updated_alert.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '处理失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"处理预警失败: {e}")
        return jsonify({'code': 500, 'msg': f'处理失败: {str(e)}', 'data': None})

@monitoring_bp.route('/requests', methods=['GET'])
@login_required
def get_monitoring_requests():
    """获取监控查看申请列表"""
    try:
        user_id = request.args.get('user_id')
        device_id = request.args.get('device_id')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append("mr.user_id = %s")
            params.append(user_id)
        if device_id:
            conditions.append("mr.device_id = %s")
            params.append(device_id)
        if status:
            conditions.append("mr.status = %s")
            params.append(status)
        
        requests, total = MonitoringRequest.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        requests_list = [req.to_dict() for req in requests]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': requests_list,
                'total': total,
                'page': page,
                'pageSize': page_size
            }
        })
        
    except Exception as e:
        logger.error(f"获取监控查看申请列表失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})

@monitoring_bp.route('/requests', methods=['POST'])
@login_required
def create_monitoring_request():
    """创建监控查看申请"""
    try:
        data = request.get_json()
        
        req = MonitoringRequest.create(
            user_id=data.get('user_id'),
            device_id=data.get('device_id'),
            purpose=data.get('purpose'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        )
        
        if req:
            return jsonify({
                'code': 0,
                'msg': 'success',
                'data': req.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '创建失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"创建监控查看申请失败: {e}")
        return jsonify({'code': 500, 'msg': f'创建失败: {str(e)}', 'data': None})

@monitoring_bp.route('/requests/<int:request_id>/approve', methods=['POST'])
@login_required
def approve_monitoring_request(request_id):
    """批准监控查看申请"""
    try:
        data = request.get_json()
        
        req = MonitoringRequest.find_by_id(request_id)
        
        if not req:
            return jsonify({
                'code': 404,
                'msg': '申请不存在',
                'data': None
            })
        
        success = req.approve(
            approved_by=data.get('approved_by'),
            reason=data.get('reason')
        )
        
        if success:
            updated_req = MonitoringRequest.find_by_id(request_id)
            return jsonify({
                'code': 0,
                'msg': '批准成功',
                'data': updated_req.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '批准失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"批准监控查看申请失败: {e}")
        return jsonify({'code': 500, 'msg': f'批准失败: {str(e)}', 'data': None})

@monitoring_bp.route('/requests/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_monitoring_request(request_id):
    """拒绝监控查看申请"""
    try:
        data = request.get_json()
        
        req = MonitoringRequest.find_by_id(request_id)
        
        if not req:
            return jsonify({
                'code': 404,
                'msg': '申请不存在',
                'data': None
            })
        
        success = req.reject(
            approved_by=data.get('approved_by'),
            reason=data.get('reason')
        )
        
        if success:
            updated_req = MonitoringRequest.find_by_id(request_id)
            return jsonify({
                'code': 0,
                'msg': '拒绝成功',
                'data': updated_req.to_dict()
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '拒绝失败',
                'data': None
            })
        
    except Exception as e:
        logger.error(f"拒绝监控查看申请失败: {e}")
        return jsonify({'code': 500, 'msg': f'拒绝失败: {str(e)}', 'data': None})

@monitoring_bp.route('/devices/<int:device_id>/stream', methods=['GET'])
@login_required
def get_device_stream(device_id):
    """获取设备视频流"""
    try:
        device = MonitoringDevice.find_by_id(device_id)
        
        if not device:
            return jsonify({
                'code': 404,
                'msg': '设备不存在',
                'data': None
            })
        
        if device.status != 'online':
            return jsonify({
                'code': 400,
                'msg': '设备离线',
                'data': None
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'stream_url': device.stream_url,
                'device_info': device.to_dict()
            }
        })
        
    except Exception as e:
        logger.error(f"获取设备视频流失败: {e}")
        return jsonify({'code': 500, 'msg': f'获取失败: {str(e)}', 'data': None})
