# routes/visitor.py - 访客管理路由
from flask import Blueprint, request, jsonify, send_file
from models.visitor import Visitor, VisitorRecord
from utils.jwt_util import login_required, admin_required
from config.database import logger
import uuid
from datetime import datetime, timedelta
import qrcode
import io
import base64

visitor_bp = Blueprint('visitor', __name__, url_prefix='/api/v1/<platform_type>/visitor')


@visitor_bp.route('', methods=['GET'])
@admin_required
def get_visitors(platform_type):
    """获取访客列表"""
    try:
        # 获取查询参数
        visitor_name = request.args.get('visitor_name')
        visitor_phone = request.args.get('visitor_phone')
        status = request.args.get('status')
        visit_date = request.args.get('visit_date')
        building_id = request.args.get('building_id')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        # 构建查询条件
        conditions = []
        params = []
        
        if visitor_name:
            conditions.append("visitor_name LIKE %s")
            params.append(f"%{visitor_name}%")
        
        if visitor_phone:
            conditions.append("visitor_phone LIKE %s")
            params.append(f"%{visitor_phone}%")
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        if visit_date:
            conditions.append("visit_date = %s")
            params.append(visit_date)
        
        if building_id:
            conditions.append("building_id = %s")
            params.append(building_id)
        
        # 执行查询
        visitors, total = Visitor.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        # 转换为字典列表
        visitors_list = [visitor.to_dict() for visitor in visitors]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': visitors_list,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取访客列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('', methods=['POST'])
@login_required
def add_visitor(platform_type):
    """新增访客"""
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['visitor_name', 'visitor_phone', 'visitor_idcard', 'host_id', 'host_name', 
                          'host_phone', 'building_id', 'room_number', 'visit_purpose', 
                          'visit_date', 'visit_time_start', 'visit_time_end']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        # 生成二维码
        qr_code = str(uuid.uuid4())[:8]
        
        # 创建访客
        visitor = Visitor.create(
            visitor_name=data['visitor_name'],
            visitor_phone=data['visitor_phone'],
            visitor_idcard=data['visitor_idcard'],
            host_id=data['host_id'],
            host_name=data['host_name'],
            host_phone=data['host_phone'],
            building_id=data['building_id'],
            room_number=data['room_number'],
            visit_purpose=data['visit_purpose'],
            visit_date=data['visit_date'],
            visit_time_start=data['visit_time_start'],
            visit_time_end=data['visit_time_end'],
            qr_code=qr_code
        )
        
        if visitor:
            return jsonify({
                'code': 0,
                'msg': '新增访客成功',
                'data': visitor.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '新增访客失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"新增访客失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'新增失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>', methods=['GET'])
@login_required
def get_visitor_detail(platform_type, visitor_id):
    """获取访客详情"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': visitor.to_dict()
        })
    
    except Exception as e:
        logger.error(f"获取访客详情失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>', methods=['PUT'])
@admin_required
def update_visitor(platform_type, visitor_id):
    """更新访客信息"""
    try:
        data = request.get_json()
        
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 更新访客信息
        update_data = {
            'visitor_name': data.get('visitor_name'),
            'visitor_phone': data.get('visitor_phone'),
            'visitor_idcard': data.get('visitor_idcard'),
            'host_id': data.get('host_id'),
            'host_name': data.get('host_name'),
            'host_phone': data.get('host_phone'),
            'building_id': data.get('building_id'),
            'room_number': data.get('room_number'),
            'visit_purpose': data.get('visit_purpose'),
            'visit_date': data.get('visit_date'),
            'visit_time_start': data.get('visit_time_start'),
            'visit_time_end': data.get('visit_time_end'),
            'status': data.get('status'),
            'entry_time': data.get('entry_time'),
            'exit_time': data.get('exit_time'),
            'approve_time': data.get('approve_time')
        }
        
        # 过滤掉None值
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if update_data:
            success = visitor.update(**update_data)
            if success:
                updated_visitor = Visitor.find_by_id(visitor_id)
                return jsonify({
                    'code': 0,
                    'msg': '更新访客成功',
                    'data': updated_visitor.to_dict()
                })
            else:
                return jsonify({
                    'code': 400,
                    'msg': '更新访客失败',
                    'data': None
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '没有要更新的内容',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"更新访客失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>', methods=['DELETE'])
@admin_required
def delete_visitor(platform_type, visitor_id):
    """删除访客"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 删除访客
        success = visitor.delete()
        if success:
            return jsonify({
                'code': 0,
                'msg': '删除访客成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '删除访客失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"删除访客失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/approve', methods=['POST'])
@admin_required
def approve_visitor(platform_type, visitor_id):
    """审核访客"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 更新状态为已审核
        success = visitor.update(status='approved', approve_time=datetime.now())
        if success:
            return jsonify({
                'code': 0,
                'msg': '审核通过',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '审核失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"审核访客失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'审核失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/reject', methods=['POST'])
@admin_required
def reject_visitor(platform_type, visitor_id):
    """拒绝访客"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 更新状态为已拒绝
        success = visitor.update(status='rejected', approve_time=datetime.now())
        if success:
            return jsonify({
                'code': 0,
                'msg': '拒绝成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '拒绝失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"拒绝访客失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'拒绝失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/complete', methods=['POST'])
@admin_required
def complete_visitor(platform_type, visitor_id):
    """完成访客"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 更新状态为已完成
        success = visitor.update(status='completed', exit_time=datetime.now())
        if success:
            return jsonify({
                'code': 0,
                'msg': '标记完成成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '标记完成失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"标记访客完成失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'标记完成失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/records', methods=['GET'])
@login_required
def get_visitor_records(platform_type):
    """获取访客记录列表"""
    try:
        # 获取查询参数
        visitor_id = request.args.get('visitor_id')
        device_id = request.args.get('device_id')
        record_type = request.args.get('record_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        # 构建查询条件
        conditions = []
        params = []
        
        if visitor_id:
            conditions.append("visitor_id = %s")
            params.append(visitor_id)
        
        if device_id:
            conditions.append("device_id = %s")
            params.append(device_id)
        
        if record_type:
            conditions.append("record_type = %s")
            params.append(record_type)
        
        if start_date:
            conditions.append("record_time >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("record_time <= %s")
            params.append(end_date)
        
        # 执行查询
        records, total = VisitorRecord.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        # 转换为字典列表
        records_list = [record.to_dict() for record in records]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': records_list,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取访客记录列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/records', methods=['POST'])
@login_required
def add_visitor_record(platform_type):
    """新增访客记录"""
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['visitor_id', 'device_id', 'record_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        # 创建记录
        record = VisitorRecord.create(
            visitor_id=data['visitor_id'],
            device_id=data['device_id'],
            record_type=data['record_type'],
            photo_url=data.get('photo_url'),
            temperature=data.get('temperature')
        )
        
        if record:
            # 更新访客状态
            visitor = Visitor.find_by_id(data['visitor_id'])
            if visitor and data['record_type'] == 'entry':
                visitor.update(entry_time=datetime.now())
            elif visitor and data['record_type'] == 'exit':
                visitor.update(exit_time=datetime.now(), status='completed')
            
            return jsonify({
                'code': 0,
                'msg': '新增记录成功',
                'data': record.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '新增记录失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"新增访客记录失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'新增失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/appointments', methods=['POST'])
@login_required
def create_appointment(platform_type):
    """创建访客预约"""
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['visitor_name', 'visitor_phone', 'visit_time', 'duration', 'purpose']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        # 生成二维码
        qr_code = str(uuid.uuid4())[:8]
        
        # 解析时间
        visit_time = datetime.fromisoformat(data['visit_time'])
        visit_date = visit_time.date()
        visit_time_start = visit_time.time()
        visit_time_end = (visit_time + timedelta(minutes=int(data['duration']))).time()
        
        # 获取用户信息作为被访人
        host_id = request.user_id
        host_name = '管理员'  # 这里应该从用户表中查询用户姓名，暂时使用固定值
        host_phone = request.user_phone
        
        # 创建访客
        visitor = Visitor.create(
            visitor_name=data['visitor_name'],
            visitor_phone=data['visitor_phone'],
            visitor_idcard=data.get('visitor_idcard', ''),
            host_id=host_id,
            host_name=host_name,
            host_phone=host_phone,
            building_id=data.get('building_id', 1),
            room_number=data.get('room_number', ''),
            visit_purpose=data['purpose'],
            visit_date=visit_date.strftime('%Y-%m-%d'),
            visit_time_start=visit_time_start.strftime('%H:%M:%S'),
            visit_time_end=visit_time_end.strftime('%H:%M:%S'),
            qr_code=qr_code
        )
        
        if visitor:
            return jsonify({
                'code': 0,
                'msg': '预约提交成功',
                'data': visitor.to_dict()
            })
        else:
            return jsonify({
                'code': 500,
                'msg': '预约提交失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"创建预约失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'预约失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/appointments', methods=['GET'])
@login_required
def get_appointments(platform_type):
    """获取预约列表"""
    try:
        # 获取查询参数
        status = request.args.get('status')
        keyword = request.args.get('keyword')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 只返回当前用户的预约
        conditions.append("host_id = %s")
        params.append(request.user_id)
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        if keyword:
            conditions.append("(visitor_name LIKE %s OR visitor_phone LIKE %s)")
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        
        # 执行查询
        visitors, total = Visitor.find_with_pagination(
            conditions=conditions,
            params=params,
            page=page,
            page_size=page_size
        )
        
        # 转换为字典列表
        appointments = []
        for visitor in visitors:
            visitor_dict = visitor.to_dict()
            # 计算预计时长
            start_time = datetime.strptime(visitor_dict['visit_time_start'], '%H:%M:%S')
            end_time = datetime.strptime(visitor_dict['visit_time_end'], '%H:%M:%S')
            duration = int((end_time - start_time).total_seconds() / 60)
            
            appointments.append({
                'id': visitor_dict['id'],
                'visitor_name': visitor_dict['visitor_name'],
                'visitor_phone': visitor_dict['visitor_phone'],
                'visit_time': f"{visitor_dict['visit_date']} {visitor_dict['visit_time_start']}",
                'duration': duration,
                'purpose': visitor_dict['visit_purpose'],
                'status': visitor_dict['status'],
                'created_at': visitor_dict['created_at'],
                'approved_at': visitor_dict['approve_time']
            })
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': appointments,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取预约列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(platform_type, appointment_id):
    """取消预约"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(appointment_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '预约不存在',
                'data': None
            })
        
        # 检查是否是当前用户的预约
        if visitor.host_id != request.user_id:
            return jsonify({
                'code': 403,
                'msg': '无权操作此预约',
                'data': None
            })
        
        # 只有待审核的预约可以取消
        if visitor.status != 'pending':
            return jsonify({
                'code': 400,
                'msg': '只能取消待审核的预约',
                'data': None
            })
        
        # 更新状态为已取消
        success = visitor.update(status='cancelled')
        if success:
            return jsonify({
                'code': 0,
                'msg': '预约已取消',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '取消失败',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"取消预约失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'取消失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/qrcode', methods=['GET'])
@login_required
def generate_qr_code(platform_type):
    """生成访客二维码"""
    try:
        appointment_id = request.args.get('appointment_id', type=int)
        if not appointment_id:
            return jsonify({
                'code': 400,
                'msg': '预约ID不能为空',
                'data': None
            })
        
        # 查找访客
        visitor = Visitor.find_by_id(appointment_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '预约不存在',
                'data': None
            })
        
        # 检查是否是当前用户的预约
        if visitor.host_id != request.user_id:
            return jsonify({
                'code': 403,
                'msg': '无权查看此预约二维码',
                'data': None
            })
        
        # 只有已通过的预约可以生成二维码
        if visitor.status != 'approved':
            return jsonify({
                'code': 400,
                'msg': '只有已通过的预约可以生成二维码',
                'data': None
            })
        
        # 生成二维码
        qr_data = f"VISITOR:{visitor.id}:{visitor.qr_code}:{datetime.now().strftime('%Y%m%d%H%M%S')}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # 创建图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为字节流
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # 返回图片
        return send_file(buffer, mimetype='image/png')
    
    except Exception as e:
        logger.error(f"生成二维码失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'生成二维码失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/statistics', methods=['GET'])
@login_required
def get_visitor_statistics(platform_type):
    """获取访客统计"""
    try:
        # 获取用户信息
        host_id = request.user_id
        
        # 计算时间范围
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # 构建查询条件
        conditions = ["host_id = %s"]
        params = [host_id]
        
        # 执行查询
        from config.database import get_db
        db = get_db()
        
        # 今日访客
        today_conditions = conditions.copy()
        today_conditions.append("DATE(visit_date) = %s")
        today_params = params.copy()
        today_params.append(today.strftime('%Y-%m-%d'))
        today_sql = f"SELECT COUNT(*) FROM t_visitor WHERE {' AND '.join(today_conditions)}"
        today_count = db.execute(today_sql, today_params).fetchone()[0]
        
        # 本周访客
        week_conditions = conditions.copy()
        week_conditions.append("DATE(visit_date) >= %s")
        week_params = params.copy()
        week_params.append(week_ago.strftime('%Y-%m-%d'))
        week_sql = f"SELECT COUNT(*) FROM t_visitor WHERE {' AND '.join(week_conditions)}"
        week_count = db.execute(week_sql, week_params).fetchone()[0]
        
        # 本月访客
        month_conditions = conditions.copy()
        month_conditions.append("DATE(visit_date) >= %s")
        month_params = params.copy()
        month_params.append(month_ago.strftime('%Y-%m-%d'))
        month_sql = f"SELECT COUNT(*) FROM t_visitor WHERE {' AND '.join(month_conditions)}"
        month_count = db.execute(month_sql, month_params).fetchone()[0]
        
        # 总访客数
        total_sql = f"SELECT COUNT(*) FROM t_visitor WHERE {' AND '.join(conditions)}"
        total_count = db.execute(total_sql, params).fetchone()[0]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'today_count': today_count,
                'week_count': week_count,
                'month_count': month_count,
                'total_count': total_count
            }
        })
    
    except Exception as e:
        logger.error(f"获取访客统计失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/access-permission', methods=['POST'])
@admin_required
def create_visitor_access_permission(platform_type, visitor_id):
    """为访客创建临时访问权限"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 检查访客状态
        if visitor.status != 'approved':
            return jsonify({
                'code': 400,
                'msg': '只有已通过的访客才能创建访问权限',
                'data': None
            })
        
        # 获取楼栋对应的门禁设备
        from models.access_control import AccessControlDevice
        devices = AccessControlDevice.find_all(
            conditions=["building_id = %s"],
            params=[visitor.building_id]
        )
        
        if not devices:
            return jsonify({
                'code': 404,
                'msg': '该楼栋没有门禁设备',
                'data': None
            })
        
        # 为每个设备创建临时权限
        from models.access_control import AccessControlPermission
        permissions = []
        
        # 计算权限时间范围
        visit_date = visitor.visit_date
        start_time = f"{visit_date} {visitor.visit_time_start}"
        end_time = f"{visit_date} {visitor.visit_time_end}"
        
        for device in devices:
            # 检查是否已存在权限
            existing = AccessControlPermission.find_by_user_and_device(visitor_id, device.id)
            if existing:
                # 更新现有权限
                existing.update(
                    start_time=start_time,
                    end_time=end_time,
                    status='active'
                )
                permissions.append(existing.to_dict())
            else:
                # 创建新权限
                permission = AccessControlPermission.create(
                    user_id=visitor_id,
                    device_id=device.id,
                    start_time=start_time,
                    end_time=end_time,
                    status='active'
                )
                if permission:
                    permissions.append(permission.to_dict())
        
        return jsonify({
            'code': 0,
            'msg': '临时访问权限创建成功',
            'data': permissions
        })
    
    except Exception as e:
        logger.error(f"创建访客访问权限失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'创建失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/access-permission', methods=['DELETE'])
@admin_required
def delete_visitor_access_permission(platform_type, visitor_id):
    """删除访客的临时访问权限"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 删除所有相关权限
        from models.access_control import AccessControlPermission
        from config.database import execute_sql
        
        sql = "DELETE FROM t_access_control_permission WHERE user_id = %s"
        affected = execute_sql(sql, (visitor_id,), commit=True)
        
        return jsonify({
            'code': 0,
            'msg': f'删除了 {affected} 条访问权限',
            'data': None
        })
    
    except Exception as e:
        logger.error(f"删除访客访问权限失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@visitor_bp.route('/<int:visitor_id>/access-permission', methods=['GET'])
@login_required
def get_visitor_access_permission(platform_type, visitor_id):
    """获取访客的临时访问权限"""
    try:
        # 查找访客
        visitor = Visitor.find_by_id(visitor_id)
        if not visitor:
            return jsonify({
                'code': 404,
                'msg': '访客不存在',
                'data': None
            })
        
        # 检查权限
        if request.user_id != visitor.host_id and request.user_role != '管理员':
            return jsonify({
                'code': 403,
                'msg': '无权查看此访客的访问权限',
                'data': None
            })
        
        # 获取权限列表
        from models.access_control import AccessControlPermission
        permissions = AccessControlPermission.find_all(
            conditions=["user_id = %s"],
            params=[visitor_id]
        )
        
        # 转换为字典列表
        permissions_list = [permission.to_dict() for permission in permissions]
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': permissions_list
        })
    
    except Exception as e:
        logger.error(f"获取访客访问权限失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })
