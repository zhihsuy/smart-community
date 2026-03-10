# routes/admin.py - 管理员路由
from flask import Blueprint, request, jsonify
from models.user import User
from models.building import Building
from utils.jwt_util import admin_required
from config.database import logger

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    """创建用户（管理员）"""
    try:
        data = request.get_json()
        
        # 必填字段验证
        required_fields = ['phone', 'password', 'nickname']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        phone = data.get('phone')
        password = data.get('password')
        nickname = data.get('nickname')
        role = data.get('role', '居民')
        building_id = data.get('building_id')
        status = data.get('status', 'active')
        
        # 检查手机号是否已存在
        from config.database import execute_sql
        check_sql = "SELECT id FROM t_user WHERE phone = %s"
        existing = execute_sql(check_sql, (phone,), commit=False)
        
        if existing:
            return jsonify({
                'code': 400,
                'msg': '手机号已存在',
                'data': None
            })
        
        # 密码加密
        import hashlib
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # 插入用户
        insert_sql = """
            INSERT INTO t_user (phone, password, nickname, role, building_id, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        
        execute_sql(insert_sql, (phone, hashed_password, nickname, role, building_id, status), commit=True)
        
        return jsonify({
            'code': 0,
            'msg': '创建成功',
            'data': None
        })
        
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'创建失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """获取用户列表（管理员）"""
    try:
        page = int(request.args.get('page', 1))
        pageSize = int(request.args.get('pageSize', 10))
        keyword = request.args.get('keyword', '')
        
        # 构建查询条件
        conditions = []
        params = []
        
        if keyword:
            conditions.append("(phone LIKE %s OR nickname LIKE %s OR real_name LIKE %s)")
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM t_user WHERE {where_clause}"
        from config.database import execute_sql
        count_result = execute_sql(count_sql, tuple(params), commit=False)
        total = count_result[0]['total'] if count_result else 0
        
        # 查询用户列表
        offset = (page - 1) * pageSize
        list_sql = f"""
            SELECT 
                id, phone, nickname, real_name, gender, birthday, email,
                community_id, building_id, unit, room_number,
                platform_type, interest_tags, family_structure, consumption_level,
                role, status, is_verified, last_login_time, created_at
            FROM t_user 
            WHERE {where_clause}
            ORDER BY id ASC
            LIMIT %s OFFSET %s
        """
        params.extend([pageSize, offset])
        
        users = execute_sql(list_sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': users,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/users', methods=['PUT'])
@admin_required
def update_user():
    """更新用户信息（管理员）"""
    try:
        data = request.get_json()
        user_id = data.get('id')
        
        if not user_id:
            return jsonify({
                'code': 400,
                'msg': '用户ID不能为空',
                'data': None
            })
        
        # 构建更新SQL
        update_fields = []
        update_params = []
        
        allowed_fields = ['nickname', 'real_name', 'gender', 'birthday', 'email',
                        'community_id', 'building_id', 'unit', 'room_number',
                        'family_structure', 'consumption_level', 'role', 'status']
        
        for field in allowed_fields:
            if field in data and data[field] is not None:
                update_fields.append(f"{field} = %s")
                update_params.append(data[field])
        
        if not update_fields:
            return jsonify({
                'code': 400,
                'msg': '没有需要更新的字段',
                'data': None
            })
        
        update_params.append(user_id)
        
        sql = f"""
            UPDATE t_user 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        from config.database import execute_sql
        affected_rows = execute_sql(sql, tuple(update_params), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败，用户不存在或没有数据被修改',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@admin_required
def toggle_user_status(user_id):
    """切换用户状态（管理员）"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status is None:
            return jsonify({
                'code': 400,
                'msg': '状态不能为空',
                'data': None
            })
        
        from config.database import execute_sql
        sql = "UPDATE t_user SET status = %s WHERE id = %s"
        affected_rows = execute_sql(sql, (status, user_id), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '状态更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"切换用户状态失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'操作失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """删除用户（管理员）"""
    try:
        from config.database import execute_sql
        sql = "DELETE FROM t_user WHERE id = %s"
        affected_rows = execute_sql(sql, (user_id,), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '用户不存在',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/buildings', methods=['GET'])
@admin_required
def get_buildings():
    """获取楼栋列表（管理员）"""
    try:
        page = int(request.args.get('page', 1))
        pageSize = int(request.args.get('pageSize', 10))
        keyword = request.args.get('keyword', '')
        
        # 构建查询条件
        conditions = []
        params = []
        
        if keyword:
            conditions.append("b.name LIKE %s")
            params.append(f"%{keyword}%")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM t_building b WHERE {where_clause}"
        from config.database import execute_sql
        count_result = execute_sql(count_sql, tuple(params), commit=False)
        total = count_result[0]['total'] if count_result else 0
        
        # 查询楼栋列表
        offset = (page - 1) * pageSize
        list_sql = f"""
            SELECT 
                b.*,
                c.name as community_name,
                (SELECT COUNT(*) FROM t_user WHERE building_id = b.id) as user_count
            FROM t_building b
            LEFT JOIN t_community c ON b.community_id = c.id
            WHERE {where_clause}
            ORDER BY b.id
            LIMIT %s OFFSET %s
        """
        params.extend([pageSize, offset])
        
        buildings = execute_sql(list_sql, tuple(params), commit=False)
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'list': buildings,
                'total': total
            }
        })
    
    except Exception as e:
        logger.error(f"获取楼栋列表失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/buildings', methods=['POST'])
@admin_required
def create_building():
    """创建楼栋（管理员）"""
    try:
        data = request.get_json()
        
        required_fields = ['community_id', 'name', 'unit_count', 'floor_count', 'household_count']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })
        
        from config.database import execute_sql
        sql = """
            INSERT INTO t_building (community_id, name, unit_count, floor_count, household_count)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['community_id'], data['name'], data['unit_count'],
            data['floor_count'], data['household_count']
        )
        
        building_id = execute_sql(sql, params, commit=True)
        
        return jsonify({
            'code': 0,
            'msg': '创建成功',
            'data': {'id': building_id}
        })
    
    except Exception as e:
        logger.error(f"创建楼栋失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'创建失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/buildings/<int:building_id>', methods=['PUT'])
@admin_required
def update_building(building_id):
    """更新楼栋信息（管理员）"""
    try:
        data = request.get_json()
        
        # 构建更新SQL
        update_fields = []
        update_params = []
        
        allowed_fields = ['name', 'unit_count', 'floor_count', 'household_count', 'address']
        
        for field in allowed_fields:
            if field in data and data[field] is not None:
                update_fields.append(f"{field} = %s")
                update_params.append(data[field])
        
        if not update_fields:
            return jsonify({
                'code': 400,
                'msg': '没有需要更新的字段',
                'data': None
            })
        
        update_params.append(building_id)
        
        from config.database import execute_sql
        sql = f"""
            UPDATE t_building 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        affected_rows = execute_sql(sql, tuple(update_params), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '更新失败，楼栋不存在或没有数据被修改',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"更新楼栋信息失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/buildings/<int:building_id>/status', methods=['PUT'])
@admin_required
def toggle_building_status(building_id):
    """切换楼栋状态（管理员）"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status is None:
            return jsonify({
                'code': 400,
                'msg': '状态不能为空',
                'data': None
            })
        
        from config.database import execute_sql
        sql = "UPDATE t_building SET status = %s WHERE id = %s"
        affected_rows = execute_sql(sql, (status, building_id), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '状态更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '楼栋不存在',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"切换楼栋状态失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'操作失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/buildings/<int:building_id>', methods=['DELETE'])
@admin_required
def delete_building(building_id):
    """删除楼栋（管理员）"""
    try:
        from config.database import execute_sql
        
        # 检查是否有用户关联
        check_sql = "SELECT COUNT(*) as count FROM t_user WHERE building_id = %s"
        check_result = execute_sql(check_sql, (building_id,), commit=False)
        
        if check_result and check_result[0]['count'] > 0:
            return jsonify({
                'code': 400,
                'msg': '该楼栋下还有用户，无法删除',
                'data': None
            })
        
        sql = "DELETE FROM t_building WHERE id = %s"
        affected_rows = execute_sql(sql, (building_id,), commit=True)
        
        if affected_rows > 0:
            return jsonify({
                'code': 0,
                'msg': '删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 404,
                'msg': '楼栋不存在',
                'data': None
            })
    
    except Exception as e:
        logger.error(f"删除楼栋失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}',
            'data': None
        })


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """获取统计数据（管理员）"""
    try:
        from config.database import execute_sql
        
        # 用户总数
        user_count_sql = "SELECT COUNT(*) as count FROM t_user"
        user_count = execute_sql(user_count_sql, commit=False)[0]['count']
        
        # 楼栋总数
        building_count_sql = "SELECT COUNT(*) as count FROM t_building"
        building_count = execute_sql(building_count_sql, commit=False)[0]['count']
        
        # 活动总数
        activity_count_sql = "SELECT COUNT(*) as count FROM t_activity"
        activity_count = execute_sql(activity_count_sql, commit=False)[0]['count']
        
        # 报修总数
        repair_count_sql = "SELECT COUNT(*) as count FROM t_repair"
        repair_count = execute_sql(repair_count_sql, commit=False)[0]['count']
        
        # 今日新增用户
        today_user_sql = "SELECT COUNT(*) as count FROM t_user WHERE DATE(created_at) = CURDATE()"
        today_user_count = execute_sql(today_user_sql, commit=False)[0]['count']
        
        # 今日活动数
        today_activity_sql = "SELECT COUNT(*) as count FROM t_activity WHERE DATE(created_at) = CURDATE()"
        today_activity_count = execute_sql(today_activity_sql, commit=False)[0]['count']
        
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': {
                'userCount': user_count,
                'buildingCount': building_count,
                'activityCount': activity_count,
                'repairCount': repair_count,
                'todayUserCount': today_user_count,
                'todayActivityCount': today_activity_count
            }
        })
    
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        })
