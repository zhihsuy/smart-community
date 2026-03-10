# config/database.py - 数据库连接配置与工具函数
import pymysql
from pymysql.err import OperationalError, ProgrammingError, InterfaceError
import logging
import json



# 配置日志（便于排查数据库问题）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('database')

# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',       # 数据库地址（本地/服务器IP）
    'user': 'root',            # 数据库用户名
    'password': '123456',      # 数据库密码
    'database': 'smart_community',  # 数据库名
    'port': 3306,              # 数据库端口（默认3306）
    'charset': 'utf8mb4',      # 字符集（支持emoji等特殊字符）
    'cursorclass': pymysql.cursors.DictCursor,  # 返回字典格式的结果
    'autocommit': False,       # 手动控制事务提交
    'connect_timeout': 10,     # 连接超时时间（秒）
}

class Database:
    """
    数据库操作类
    """
    
    def query_one(self, sql, params=None):
        """
        查询单条数据
        """
        result = execute_sql(sql, params, commit=False)
        return result[0] if result else None
    
    def query_all(self, sql, params=None):
        """
        查询多条数据
        """
        return execute_sql(sql, params, commit=False)
    
    def execute(self, sql, params=None):
        """
        执行SQL语句
        """
        return execute_sql(sql, params, commit=True)
    
    def get_user_by_token(self, token):
        """
        根据token获取用户信息
        """
        sql = """
            SELECT 
                u.*
            FROM t_user u
            WHERE u.token = %s
        """
        return self.query_one(sql, (token,))

def get_db_connection():
    """
    获取数据库连接
    :return: pymysql.Connection 对象
    :raise: 连接失败时抛出异常
    """
    try:
        # 创建数据库连接
        conn = pymysql.connect(**DB_CONFIG)
        logger.info("数据库连接成功")
        return conn
    except OperationalError as e:
        logger.error(f"数据库连接失败：{e}（检查地址/端口/密码/库名）")
        raise  # 抛出异常，让上层处理
    except InterfaceError as e:
        logger.error(f"数据库接口错误：{e}")
        raise
    except Exception as e:
        logger.error(f"未知数据库连接错误：{e}")
        raise

def close_db_connection(conn, cursor=None):
    """
    安全关闭数据库连接和游标
    :param conn: 数据库连接对象
    :param cursor: 游标对象（可选）
    """
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败：{e}")

def execute_sql(sql, params=None, commit=False):
    """
    通用SQL执行函数（简化CRUD操作）
    :param sql: SQL语句
    :param params: SQL参数（元组/列表，防止SQL注入）
    :param commit: 是否提交事务（增删改需True，查询False）
    :return: 查询结果（列表/字典）或受影响行数/最后插入ID
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 执行SQL
        affected_rows = cursor.execute(sql, params or ())
        logger.info(f"SQL执行成功，影响行数：{affected_rows}")
        
        if commit:
            conn.commit()
            logger.info("事务已提交")
            # 如果是INSERT操作，返回最后插入的ID
            if sql.strip().upper().startswith('INSERT'):
                last_id = cursor.lastrowid
                logger.info(f"最后插入ID：{last_id}")
                return last_id
            return affected_rows  # 增删改返回受影响行数
        else:
            result = cursor.fetchall()  # 查询返回所有结果
            return result
            
    except ProgrammingError as e:
        if conn:
            conn.rollback()  # 执行失败回滚事务
        logger.error(f"SQL语法错误：{e}（检查SQL语句/表结构）")
        raise
    except OperationalError as e:
        if conn:
            conn.rollback()
        logger.error(f"数据库操作失败：{e}")
        raise
    finally:
        close_db_connection(conn, cursor)  # 确保连接关闭

def init_database():
    """
    初始化数据库（创建表和初始数据）
    """
    try:
        # 先创建数据库（如果不存在）
        temp_config = DB_CONFIG.copy()
        temp_config['database'] = None  # 不指定数据库
        conn = pymysql.connect(**temp_config)
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS smart_community 
            DEFAULT CHARACTER SET utf8mb4 
            DEFAULT COLLATE utf8mb4_unicode_ci
        """)
        conn.commit()
        logger.info("数据库创建成功或已存在")
        
        cursor.close()
        conn.close()
        
        # 创建表
        create_tables()
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败：{e}")
        raise

def create_tables():
    """
    创建数据表
    """
    # 用户表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_user (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
            phone VARCHAR(20) NOT NULL COMMENT '手机号',
            password VARCHAR(255) NOT NULL COMMENT '加密密码',
            nickname VARCHAR(50) DEFAULT NULL COMMENT '昵称',
            avatar VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
            real_name VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
            id_card VARCHAR(18) DEFAULT NULL COMMENT '身份证号',
            gender TINYINT DEFAULT 0 COMMENT '性别: 0-未知 1-男 2-女',
            birthday DATE DEFAULT NULL COMMENT '生日',
            email VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
            community_id BIGINT UNSIGNED DEFAULT NULL COMMENT '所属社区ID',
            building_id BIGINT UNSIGNED DEFAULT NULL COMMENT '楼栋ID',
            unit VARCHAR(20) DEFAULT NULL COMMENT '单元',
            room_number VARCHAR(20) DEFAULT NULL COMMENT '房号',
            platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型',
            device_id VARCHAR(100) DEFAULT NULL COMMENT '设备ID',
            interest_tags JSON DEFAULT NULL COMMENT '兴趣标签',
            family_structure VARCHAR(50) DEFAULT NULL COMMENT '家庭结构',
            consumption_level TINYINT DEFAULT 2 COMMENT '消费能力',
            role VARCHAR(20) NOT NULL DEFAULT '居民' COMMENT '角色: 居民/物业管理员/运营/管理员',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态: active/inactive',
            is_verified TINYINT DEFAULT 0 COMMENT '是否实名认证',
            last_login_time DATETIME DEFAULT NULL COMMENT '最后登录时间',
            last_login_ip VARCHAR(50) DEFAULT NULL COMMENT '最后登录IP',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_phone (phone),
            KEY idx_community (community_id),
            KEY idx_status (status),
            KEY idx_platform (platform_type)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表'
    """, commit=True)
    
    # 楼栋表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_building (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            community_id BIGINT UNSIGNED NOT NULL COMMENT '社区ID',
            name VARCHAR(50) NOT NULL COMMENT '楼栋名称',
            unit_count INT UNSIGNED DEFAULT 1 COMMENT '单元数',
            floor_count INT UNSIGNED DEFAULT 0 COMMENT '层数',
            household_count INT UNSIGNED DEFAULT 0 COMMENT '户数',
            status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive',
            PRIMARY KEY (id),
            KEY idx_community (community_id),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='楼栋表'
    """, commit=True)
    
    # 为现有楼栋表添加status字段（如果不存在）
    try:
        execute_sql("""
            ALTER TABLE t_building ADD COLUMN IF NOT EXISTS `status` VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive'
        """, commit=True)
        execute_sql("""
            ALTER TABLE t_building ADD INDEX IF NOT EXISTS idx_status (`status`)
        """, commit=True)
    except Exception as e:
        # 忽略字段已存在的错误
        pass
    
    # 社区表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_community (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '社区ID',
            name VARCHAR(100) NOT NULL COMMENT '社区名称',
            code VARCHAR(50) NOT NULL COMMENT '社区编码',
            province VARCHAR(50) NOT NULL COMMENT '省',
            city VARCHAR(50) NOT NULL COMMENT '市',
            district VARCHAR(50) NOT NULL COMMENT '区/县',
            address VARCHAR(255) NOT NULL COMMENT '详细地址',
            longitude DECIMAL(10, 7) DEFAULT NULL COMMENT '经度',
            latitude DECIMAL(10, 7) DEFAULT NULL COMMENT '纬度',
            total_buildings INT UNSIGNED DEFAULT 0 COMMENT '总楼栋数',
            total_households INT UNSIGNED DEFAULT 0 COMMENT '总户数',
            property_company VARCHAR(100) DEFAULT NULL COMMENT '物业公司',
            contact_phone VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
            status TINYINT NOT NULL DEFAULT 1 COMMENT '状态',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_code (code),
            KEY idx_city (city),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社区表'
    """, commit=True)
    
    # 权限表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_permission (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权限ID',
            code VARCHAR(50) NOT NULL COMMENT '权限编码',
            name VARCHAR(100) NOT NULL COMMENT '权限名称',
            description VARCHAR(255) DEFAULT NULL COMMENT '权限描述',
            type VARCHAR(20) NOT NULL DEFAULT 'api' COMMENT '权限类型: api/page',
            resource VARCHAR(255) NOT NULL COMMENT '资源路径',
            method VARCHAR(10) DEFAULT NULL COMMENT 'HTTP方法',
            status TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-禁用 1-启用',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_code (code),
            KEY idx_type (type),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表'
    """, commit=True)
    
    # 角色权限关联表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_role_permission (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
            role VARCHAR(20) NOT NULL COMMENT '角色',
            permission_code VARCHAR(50) NOT NULL COMMENT '权限编码',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY uk_role_permission (role, permission_code),
            KEY idx_role (role)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表'
    """, commit=True)
    
    # 门禁设备表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_access_control_device (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '设备ID',
            device_code VARCHAR(50) NOT NULL COMMENT '设备编码',
            device_name VARCHAR(100) NOT NULL COMMENT '设备名称',
            device_type VARCHAR(20) NOT NULL COMMENT '设备类型: face/password/card/qrcode',
            building_id BIGINT UNSIGNED NOT NULL COMMENT '所属楼栋ID',
            location VARCHAR(255) NOT NULL COMMENT '安装位置',
            ip_address VARCHAR(50) NOT NULL COMMENT 'IP地址',
            status VARCHAR(20) NOT NULL DEFAULT 'normal' COMMENT '状态: normal/abnormal/offline',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            UNIQUE KEY uk_device_code (device_code),
            KEY idx_building (building_id),
            KEY idx_status (status),
            KEY idx_device_type (device_type)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='门禁设备表'
    """, commit=True)
    
    # 门禁权限表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_access_control_permission (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权限ID',
            user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
            device_id BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
            start_time DATETIME DEFAULT NULL COMMENT '开始时间',
            end_time DATETIME DEFAULT NULL COMMENT '结束时间',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态: active/inactive',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            UNIQUE KEY uk_user_device (user_id, device_id),
            KEY idx_user (user_id),
            KEY idx_device (device_id),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='门禁权限表'
    """, commit=True)
    
    # 门禁记录表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_access_control_record (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
            device_id BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
            user_id BIGINT UNSIGNED DEFAULT NULL COMMENT '用户ID',
            access_type VARCHAR(20) NOT NULL COMMENT '访问类型: face/card/password/qrcode/remote',
            status VARCHAR(20) NOT NULL COMMENT '状态: success/fail',
            message VARCHAR(255) DEFAULT NULL COMMENT '备注信息',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            PRIMARY KEY (id),
            KEY idx_device (device_id),
            KEY idx_user (user_id),
            KEY idx_access_type (access_type),
            KEY idx_status (status),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='门禁记录表'
    """, commit=True)
    
    # 访客表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_visitor (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '访客ID',
            visitor_name VARCHAR(50) NOT NULL COMMENT '访客姓名',
            visitor_phone VARCHAR(20) NOT NULL COMMENT '访客电话',
            visitor_idcard VARCHAR(18) NOT NULL COMMENT '访客身份证',
            host_id BIGINT UNSIGNED NOT NULL COMMENT '被访人ID',
            host_name VARCHAR(50) NOT NULL COMMENT '被访人姓名',
            host_phone VARCHAR(20) NOT NULL COMMENT '被访人电话',
            building_id BIGINT UNSIGNED NOT NULL COMMENT '楼栋ID',
            room_number VARCHAR(20) NOT NULL COMMENT '房间号',
            visit_purpose VARCHAR(255) NOT NULL COMMENT '访问目的',
            visit_date DATE NOT NULL COMMENT '访问日期',
            visit_time_start TIME NOT NULL COMMENT '开始时间',
            visit_time_end TIME NOT NULL COMMENT '结束时间',
            qr_code VARCHAR(50) NOT NULL COMMENT '二维码',
            status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending-待审批 approved-已通过 rejected-已拒绝 completed-已完成',
            entry_time DATETIME DEFAULT NULL COMMENT '进入时间',
            exit_time DATETIME DEFAULT NULL COMMENT '离开时间',
            approve_time DATETIME DEFAULT NULL COMMENT '审批时间',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            UNIQUE KEY uk_qr_code (qr_code),
            KEY idx_host_id (host_id),
            KEY idx_building_id (building_id),
            KEY idx_status (status),
            KEY idx_visit_date (visit_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='访客表'
    """, commit=True)
    
    # 访客记录表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_visitor_record (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
            visitor_id BIGINT UNSIGNED NOT NULL COMMENT '访客ID',
            device_id BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
            record_type VARCHAR(20) NOT NULL COMMENT '记录类型: entry-进入 exit-离开',
            photo_url VARCHAR(255) DEFAULT NULL COMMENT '照片URL',
            temperature DECIMAL(3,1) DEFAULT NULL COMMENT '体温',
            record_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
            PRIMARY KEY (id),
            KEY idx_visitor_id (visitor_id),
            KEY idx_device_id (device_id),
            KEY idx_record_type (record_type),
            KEY idx_record_time (record_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='访客记录表'
    """, commit=True)
    
    # 车位表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_parking_space (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '车位ID',
            space_code VARCHAR(50) NOT NULL COMMENT '车位编码',
            space_name VARCHAR(100) NOT NULL COMMENT '车位名称',
            type VARCHAR(20) NOT NULL COMMENT '车位类型: underground/ground/visitor',
            status VARCHAR(20) NOT NULL DEFAULT 'free' COMMENT '状态: free/occupied/reserved',
            building_id BIGINT UNSIGNED DEFAULT NULL COMMENT '所属楼栋ID',
            location VARCHAR(255) NOT NULL COMMENT '位置描述',
            price DECIMAL(10, 2) DEFAULT NULL COMMENT '月租金',
            owner_id BIGINT UNSIGNED DEFAULT NULL COMMENT '业主ID',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            UNIQUE KEY uk_space_code (space_code),
            KEY idx_status (status),
            KEY idx_type (type),
            KEY idx_building (building_id),
            KEY idx_owner (owner_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='车位表'
    """, commit=True)
    
    # 停车记录表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_parking_record (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
            space_id BIGINT UNSIGNED NOT NULL COMMENT '车位ID',
            user_id BIGINT UNSIGNED DEFAULT NULL COMMENT '用户ID',
            car_number VARCHAR(20) NOT NULL COMMENT '车牌号',
            entry_time DATETIME NOT NULL COMMENT '进入时间',
            exit_time DATETIME DEFAULT NULL COMMENT '离开时间',
            duration INT DEFAULT NULL COMMENT '停车时长(分钟)',
            fee DECIMAL(10, 2) DEFAULT NULL COMMENT '停车费用',
            payment_status VARCHAR(20) DEFAULT 'unpaid' COMMENT '支付状态: unpaid/paid',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            KEY idx_space (space_id),
            KEY idx_user (user_id),
            KEY idx_car_number (car_number),
            KEY idx_entry_time (entry_time),
            KEY idx_payment_status (payment_status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='停车记录表'
    """, commit=True)
    
    # 车辆信息表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_vehicle (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '车辆ID',
            user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
            car_number VARCHAR(20) NOT NULL COMMENT '车牌号',
            car_brand VARCHAR(50) DEFAULT NULL COMMENT '品牌',
            car_model VARCHAR(50) DEFAULT NULL COMMENT '型号',
            car_color VARCHAR(20) DEFAULT NULL COMMENT '颜色',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态: active/inactive',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            UNIQUE KEY uk_car_number (car_number),
            KEY idx_user (user_id),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='车辆信息表'
    """, commit=True)
    
    # 维修工单表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_repair_order (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '工单ID',
            user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
            title VARCHAR(200) NOT NULL COMMENT '报修标题',
            type VARCHAR(50) NOT NULL COMMENT '报修类型: water_elec/property/other',
            description TEXT NOT NULL COMMENT '问题描述',
            address VARCHAR(255) NOT NULL COMMENT '报修地址',
            images JSON DEFAULT NULL COMMENT '图片列表',
            priority VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '优先级: low/medium/high',
            status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending/processing/completed/cancelled',
            technician_id BIGINT UNSIGNED DEFAULT NULL COMMENT '维修人员ID',
            estimated_time DATETIME DEFAULT NULL COMMENT '预计完成时间',
            process_result TEXT DEFAULT NULL COMMENT '处理结果',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            KEY idx_user (user_id),
            KEY idx_status (status),
            KEY idx_type (type),
            KEY idx_priority (priority),
            KEY idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='维修工单表'
    """, commit=True)
    
    # 维修人员表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_technician (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '维修人员ID',
            name VARCHAR(50) NOT NULL COMMENT '姓名',
            phone VARCHAR(20) NOT NULL COMMENT '联系电话',
            specialty VARCHAR(100) DEFAULT NULL COMMENT '专业领域',
            status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态: active/inactive',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            KEY idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='维修人员表'
    """, commit=True)
    
    # 公告表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_notice (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '公告ID',
            title VARCHAR(200) NOT NULL COMMENT '公告标题',
            type VARCHAR(50) NOT NULL COMMENT '公告类型: notice/announcement/activity/other',
            content TEXT NOT NULL COMMENT '公告内容',
            author VARCHAR(50) DEFAULT NULL COMMENT '发布人',
            author_id BIGINT UNSIGNED DEFAULT NULL COMMENT '发布人ID',
            publish_time DATETIME NOT NULL COMMENT '发布时间',
            expire_time DATETIME DEFAULT NULL COMMENT '过期时间',
            status VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT '状态: draft/published/expired',
            view_count INT UNSIGNED DEFAULT 0 COMMENT '浏览量',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            KEY idx_status (status),
            KEY idx_type (type),
            KEY idx_publish_time (publish_time),
            KEY idx_author_id (author_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='公告表'
    """, commit=True)
    
    # 投诉表
    execute_sql("""
        CREATE TABLE IF NOT EXISTS t_complaint (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '投诉ID',
            user_id BIGINT UNSIGNED NOT NULL COMMENT '投诉人ID',
            title VARCHAR(200) NOT NULL COMMENT '投诉标题',
            type VARCHAR(50) NOT NULL COMMENT '投诉类型: service/facility/environment/security/other',
            content TEXT NOT NULL COMMENT '投诉内容',
            images TEXT DEFAULT NULL COMMENT '图片地址，多个用逗号分隔',
            priority VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '优先级: low/medium/high',
            status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending/processing/resolved/rejected',
            handler_id BIGINT UNSIGNED DEFAULT NULL COMMENT '处理人ID',
            handler_name VARCHAR(50) DEFAULT NULL COMMENT '处理人姓名',
            handle_result TEXT DEFAULT NULL COMMENT '处理结果',
            handle_time DATETIME DEFAULT NULL COMMENT '处理时间',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            PRIMARY KEY (id),
            KEY idx_user_id (user_id),
            KEY idx_status (status),
            KEY idx_type (type),
            KEY idx_priority (priority),
            KEY idx_handler_id (handler_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='投诉表'
    """, commit=True)
    
    logger.info("数据表创建完成")
    
    # 插入初始数据
    init_data()

def init_data():
    """
    初始化数据
    """
    # 检查是否已有数据
    result = execute_sql("SELECT COUNT(*) as count FROM t_community")
    if result and result[0]['count'] > 0:
        logger.info("初始数据已存在，跳过")
        return
    
    # 插入社区数据
    execute_sql("""
        INSERT INTO t_community (name, code, province, city, district, address, total_buildings, total_households, property_company, contact_phone)
        VALUES ('智慧花园小区', 'ZH_HY_001', '广东省', '深圳市', '南山区', '科技园南区123号', 10, 500, '万科物业', '400-123-4567')
    """, commit=True)
    
    # 插入楼栋数据
    buildings = [
        (1, 1, '1号楼', 2, 18, 72),
        (2, 1, '2号楼', 2, 18, 72),
        (3, 1, '3号楼', 2, 18, 72),
        (4, 1, '4号楼', 2, 18, 72),
        (5, 1, '5号楼', 2, 18, 72)
    ]
    for b in buildings:
        execute_sql("""
            INSERT INTO t_building (id, community_id, name, unit_count, floor_count, household_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, b, commit=True)
    
    # 插入权限数据
    execute_sql("""
        INSERT INTO t_permission (code, name, description, type, resource, method) VALUES
        -- 基础用户权限
        ('user:info:read', '查看用户信息', '查看用户基本信息', 'api', '/v1/*/user/info', 'GET'),
        ('user:info:update', '更新用户信息', '更新用户基本信息', 'api', '/v1/*/user/info', 'PUT'),
        -- 管理员权限
        ('admin:user:list', '查看用户列表', '查看所有用户列表', 'api', '/v1/*/admin/users', 'GET'),
        ('admin:user:create', '创建用户', '创建新用户', 'api', '/v1/*/admin/users', 'POST'),
        -- 运营权限
        ('op:user:list', '查看用户列表', '查看用户列表', 'api', '/v1/*/op/users', 'GET'),
        ('op:user:update', '编辑用户', '编辑用户信息', 'api', '/v1/*/op/users/*', 'PUT'),
        -- 商品权限
        ('admin:goods:list', '查看商品列表', '查看商品列表', 'api', '/v1/*/admin/goods', 'GET'),
        ('admin:goods:create', '创建商品', '创建商品', 'api', '/v1/*/admin/goods', 'POST'),
        ('op:goods:list', '查看商品列表', '查看商品列表', 'api', '/v1/*/op/goods', 'GET'),
        ('op:goods:update', '编辑商品', '编辑商品', 'api', '/v1/*/op/goods/*', 'PUT')
    """, commit=True)
    
    # 插入角色权限关联数据
    execute_sql("""
        INSERT INTO t_role_permission (role, permission_code) VALUES
        -- 管理员权限
        ('管理员', 'user:info:read'),
        ('管理员', 'user:info:update'),
        ('管理员', 'admin:user:list'),
        ('管理员', 'admin:user:create'),
        ('管理员', 'admin:goods:list'),
        ('管理员', 'admin:goods:create'),
        ('管理员', 'op:user:list'),
        ('管理员', 'op:user:update'),
        ('管理员', 'op:goods:list'),
        ('管理员', 'op:goods:update'),
        -- 运营权限
        ('运营', 'user:info:read'),
        ('运营', 'user:info:update'),
        ('运营', 'op:user:list'),
        ('运营', 'op:user:update'),
        ('运营', 'op:goods:list'),
        ('运营', 'op:goods:update'),
        -- 居民权限
        ('居民', 'user:info:read'),
        ('居民', 'user:info:update')
    """, commit=True)
    
    # 插入管理员账号
    # 密码: SLG123 (使用bcrypt加密)
    import bcrypt
    password_hash = bcrypt.hashpw('SLG123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    execute_sql("""
        INSERT INTO t_user (phone, password, nickname, role, status, is_verified)
        VALUES ('zh1111', %s, '超级管理员', '管理员', 1, 1)
    """, (password_hash,), commit=True)
    
    # 插入门禁设备测试数据
    execute_sql("""
        INSERT INTO t_access_control_device (device_code, device_name, device_type, building_id, location, ip_address, status)
        VALUES
        ('AC001', '1号楼南门', 'face', 1, '1号楼南门入口', '192.168.1.101', 'normal'),
        ('AC002', '1号楼北门', 'card', 1, '1号楼北门入口', '192.168.1.102', 'normal'),
        ('AC003', '2号楼南门', 'face', 2, '2号楼南门入口', '192.168.1.103', 'normal'),
        ('AC004', '2号楼北门', 'password', 2, '2号楼北门入口', '192.168.1.104', 'normal'),
        ('AC005', '3号楼南门', 'qrcode', 3, '3号楼南门入口', '192.168.1.105', 'normal')
    """, commit=True)
    
    # 插入门禁权限测试数据
    execute_sql("""
        INSERT INTO t_access_control_permission (user_id, device_id, status)
        VALUES
        (1, 1, 'active'), -- 测试用户对1号楼南门有权限
        (1, 2, 'active'), -- 测试用户对1号楼北门有权限
        (3, 1, 'active'), -- 管理员对1号楼南门有权限
        (3, 2, 'active'), -- 管理员对1号楼北门有权限
        (3, 3, 'active'), -- 管理员对2号楼南门有权限
        (3, 4, 'active'), -- 管理员对2号楼北门有权限
        (3, 5, 'active')  -- 管理员对3号楼南门有权限
    """, commit=True)
    
    # 插入门禁记录测试数据
    execute_sql("""
        INSERT INTO t_access_control_record (device_id, user_id, access_type, status, message)
        VALUES
        (1, 1, 'face', 'success', '人脸识别成功'),
        (1, 3, 'remote', 'success', '远程开门成功'),
        (2, 1, 'card', 'success', '刷卡成功'),
        (3, 3, 'face', 'success', '人脸识别成功'),
        (4, 3, 'password', 'success', '密码验证成功')
    """, commit=True)
    
    logger.info("初始数据插入完成")

# 创建数据库操作实例
db = Database()
