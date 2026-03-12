# init_smart_community_tables.py - 智慧社区基础功能数据库表初始化
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import get_db_connection as get_connection, logger

def create_access_control_tables():
    """创建智能门禁系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 门禁设备表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_access_device (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device_code VARCHAR(50) NOT NULL COMMENT '设备编号',
                device_name VARCHAR(100) NOT NULL COMMENT '设备名称',
                device_type ENUM('gate', 'door', 'elevator', 'parking') NOT NULL COMMENT '设备类型',
                location VARCHAR(200) COMMENT '安装位置',
                building_id INT COMMENT '关联楼栋ID',
                status ENUM('online', 'offline', 'maintenance') DEFAULT 'offline' COMMENT '设备状态',
                ip_address VARCHAR(50) COMMENT 'IP地址',
                last_heartbeat TIMESTAMP NULL COMMENT '最后心跳时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_building (building_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='门禁设备表'
        """)
        
        # 门禁权限表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_access_permission (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL COMMENT '用户ID',
                device_id INT NOT NULL COMMENT '设备ID',
                access_type ENUM('face', 'fingerprint', 'card', 'qr_code', 'password') NOT NULL COMMENT '开门方式',
                access_code VARCHAR(255) COMMENT '权限凭证（人脸特征/卡号/密码等）',
                start_time TIMESTAMP NULL COMMENT '权限开始时间',
                end_time TIMESTAMP NULL COMMENT '权限结束时间',
                status ENUM('active', 'inactive', 'expired') DEFAULT 'active' COMMENT '权限状态',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_device (device_id),
                INDEX idx_status (status),
                UNIQUE KEY uk_user_device (user_id, device_id, access_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='门禁权限表'
        """)
        
        # 出入记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_access_record (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT COMMENT '用户ID（注册用户）',
                visitor_id INT COMMENT '访客ID（临时访客）',
                device_id INT NOT NULL COMMENT '设备ID',
                access_type ENUM('face', 'fingerprint', 'card', 'qr_code', 'password', 'remote') NOT NULL COMMENT '开门方式',
                access_status ENUM('success', 'failed', 'timeout') NOT NULL COMMENT '开门状态',
                photo_url VARCHAR(500) COMMENT '抓拍照片URL',
                temperature DECIMAL(4,1) COMMENT '体温（支持测温的设备）',
                record_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
                INDEX idx_user (user_id),
                INDEX idx_device (device_id),
                INDEX idx_time (record_time),
                INDEX idx_status (access_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='出入记录表'
        """)
        
        conn.commit()
        logger.info("智能门禁系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建智能门禁系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_repair_tables():
    """创建物业报修系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 报修工单表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_repair_order (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '工单编号',
                user_id INT NOT NULL COMMENT '报修用户ID',
                building_id INT COMMENT '楼栋ID',
                room_number VARCHAR(50) COMMENT '房间号',
                contact_phone VARCHAR(20) COMMENT '联系电话',
                repair_type ENUM('water', 'electric', 'gas', 'door', 'elevator', 'cleaning', 'other') NOT NULL COMMENT '报修类型',
                title VARCHAR(200) NOT NULL COMMENT '报修标题',
                description TEXT COMMENT '问题描述',
                images TEXT COMMENT '图片URL（JSON数组）',
                urgency ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal' COMMENT '紧急程度',
                status ENUM('pending', 'assigned', 'processing', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '工单状态',
                assignee_id INT COMMENT '指派维修人员ID',
                assigned_at TIMESTAMP NULL COMMENT '指派时间',
                completed_at TIMESTAMP NULL COMMENT '完成时间',
                rating INT COMMENT '评价星级',
                comment TEXT COMMENT '评价内容',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_status (status),
                INDEX idx_type (repair_type),
                INDEX idx_time (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报修工单表'
        """)
        
        # 维修人员表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_repair_worker (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL COMMENT '关联用户ID',
                worker_name VARCHAR(50) NOT NULL COMMENT '维修人员姓名',
                phone VARCHAR(20) NOT NULL COMMENT '联系电话',
                skills TEXT COMMENT '技能标签（JSON数组）',
                work_status ENUM('available', 'busy', 'offduty') DEFAULT 'available' COMMENT '工作状态',
                rating DECIMAL(2,1) DEFAULT 5.0 COMMENT '评分',
                total_orders INT DEFAULT 0 COMMENT '完成工单数',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_status (work_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='维修人员表'
        """)
        
        # 工单处理记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_repair_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL COMMENT '工单ID',
                action ENUM('create', 'assign', 'accept', 'process', 'complete', 'cancel', 'comment') NOT NULL COMMENT '操作类型',
                operator_id INT NOT NULL COMMENT '操作人ID',
                operator_name VARCHAR(50) COMMENT '操作人姓名',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_order (order_id),
                INDEX idx_action (action)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工单处理记录表'
        """)
        
        conn.commit()
        logger.info("物业报修系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建物业报修系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_notice_tables():
    """创建公告通知系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 公告表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_notice (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL COMMENT '公告标题',
                content TEXT NOT NULL COMMENT '公告内容',
                notice_type ENUM('community', 'property', 'emergency', 'activity') DEFAULT 'community' COMMENT '公告类型',
                target_type ENUM('all', 'building', 'unit') DEFAULT 'all' COMMENT '发布对象类型',
                target_ids TEXT COMMENT '目标对象ID（JSON数组）',
                priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal' COMMENT '优先级',
                is_top TINYINT(1) DEFAULT 0 COMMENT '是否置顶',
                top_expire_time TIMESTAMP NULL COMMENT '置顶过期时间',
                publish_time TIMESTAMP NULL COMMENT '发布时间',
                expire_time TIMESTAMP NULL COMMENT '过期时间',
                publisher_id INT NOT NULL COMMENT '发布人ID',
                author VARCHAR(100) COMMENT '发布人姓名',
                read_count INT DEFAULT 0 COMMENT '阅读次数',
                status ENUM('draft', 'published', 'expired', 'withdrawn') DEFAULT 'draft' COMMENT '状态',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_type (notice_type),
                INDEX idx_status (status),
                INDEX idx_publish_time (publish_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告表'
        """)
        
        # 公告阅读记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_notice_read (
                id INT AUTO_INCREMENT PRIMARY KEY,
                notice_id INT NOT NULL COMMENT '公告ID',
                user_id INT NOT NULL COMMENT '用户ID',
                read_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '阅读时间',
                UNIQUE KEY uk_notice_user (notice_id, user_id),
                INDEX idx_user (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告阅读记录表'
        """)
        
        conn.commit()
        logger.info("公告通知系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建公告通知系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_utility_tables():
    """创建智能水电表系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 水电表设备表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_utility_meter (
                id INT AUTO_INCREMENT PRIMARY KEY,
                meter_no VARCHAR(50) NOT NULL UNIQUE COMMENT '表具编号',
                meter_type ENUM('water', 'electric', 'gas') NOT NULL COMMENT '表具类型',
                building_id INT NOT NULL COMMENT '楼栋ID',
                unit VARCHAR(20) COMMENT '单元',
                room_number VARCHAR(50) COMMENT '房间号',
                user_id INT COMMENT '绑定用户ID',
                location VARCHAR(200) COMMENT '安装位置',
                status ENUM('normal', 'abnormal', 'offline') DEFAULT 'normal' COMMENT '设备状态',
                current_reading DECIMAL(12,2) DEFAULT 0 COMMENT '当前读数',
                last_reading DECIMAL(12,2) DEFAULT 0 COMMENT '上次读数',
                last_reading_time TIMESTAMP NULL COMMENT '上次抄表时间',
                install_time TIMESTAMP NULL COMMENT '安装时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_building (building_id),
                INDEX idx_user (user_id),
                INDEX idx_type (meter_type),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='水电表设备表'
        """)
        
        # 用量记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_utility_usage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                meter_id INT NOT NULL COMMENT '表具ID',
                reading DECIMAL(12,2) NOT NULL COMMENT '读数',
                usage_amount DECIMAL(10,2) NOT NULL COMMENT '用量',
                reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '抄表时间',
                reading_type ENUM('auto', 'manual') DEFAULT 'auto' COMMENT '抄表方式',
                operator_id INT COMMENT '操作员ID（手动抄表）',
                INDEX idx_meter (meter_id),
                INDEX idx_time (reading_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用量记录表'
        """)
        
        # 用量预警表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_utility_alert (
                id INT AUTO_INCREMENT PRIMARY KEY,
                meter_id INT NOT NULL COMMENT '表具ID',
                user_id INT NOT NULL COMMENT '用户ID',
                alert_type ENUM('high_usage', 'leak', 'offline', 'abnormal') NOT NULL COMMENT '预警类型',
                alert_content TEXT COMMENT '预警内容',
                current_reading DECIMAL(12,2) COMMENT '当前读数',
                threshold_value DECIMAL(10,2) COMMENT '阈值',
                status ENUM('pending', 'processed', 'ignored') DEFAULT 'pending' COMMENT '处理状态',
                processed_by INT COMMENT '处理人ID',
                processed_time TIMESTAMP NULL COMMENT '处理时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_meter (meter_id),
                INDEX idx_user (user_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用量预警表'
        """)
        
        conn.commit()
        logger.info("智能水电表系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建智能水电表系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_payment_tables():
    """创建费用缴纳系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 费用账单表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_bill (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bill_no VARCHAR(50) NOT NULL UNIQUE COMMENT '账单编号',
                user_id INT NOT NULL COMMENT '用户ID',
                building_id INT NOT NULL COMMENT '楼栋ID',
                room_number VARCHAR(50) NOT NULL COMMENT '房间号',
                bill_type ENUM('property', 'water', 'electric', 'gas', 'parking', 'other') NOT NULL COMMENT '费用类型',
                bill_period_start DATE NOT NULL COMMENT '计费周期开始',
                bill_period_end DATE NOT NULL COMMENT '计费周期结束',
                amount DECIMAL(10,2) NOT NULL COMMENT '金额',
                late_fee DECIMAL(10,2) DEFAULT 0 COMMENT '滞纳金',
                total_amount DECIMAL(10,2) NOT NULL COMMENT '总金额',
                due_date DATE NOT NULL COMMENT '截止日期',
                paid_amount DECIMAL(10,2) DEFAULT 0 COMMENT '已付金额',
                paid_time TIMESTAMP NULL COMMENT '支付时间',
                payment_method VARCHAR(50) COMMENT '支付方式',
                payment_no VARCHAR(100) COMMENT '支付流水号',
                status ENUM('unpaid', 'paid', 'overdue', 'cancelled') DEFAULT 'unpaid' COMMENT '账单状态',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_status (status),
                INDEX idx_type (bill_type),
                INDEX idx_due_date (due_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='费用账单表'
        """)
        
        # 缴费表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_payment (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL COMMENT '用户ID',
                building_id INT COMMENT '楼栋ID',
                amount DECIMAL(10,2) NOT NULL COMMENT '金额',
                type ENUM('property', 'water', 'electricity', 'gas', 'parking') NOT NULL COMMENT '缴费类型',
                fee_type VARCHAR(50) COMMENT '费用类型',
                period_start DATE COMMENT '计费周期开始',
                period_end DATE COMMENT '计费周期结束',
                due_date DATE COMMENT '截止日期',
                paid_amount DECIMAL(10,2) DEFAULT 0 COMMENT '已付金额',
                paid_time TIMESTAMP NULL COMMENT '支付时间',
                status ENUM('pending', 'paid', 'failed') DEFAULT 'pending' COMMENT '状态',
                payment_method VARCHAR(50) COMMENT '支付方式',
                transaction_id VARCHAR(100) COMMENT '交易ID',
                remark TEXT COMMENT '备注',
                payment_no VARCHAR(100) UNIQUE COMMENT '支付单号',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_building (building_id),
                INDEX idx_status (status),
                INDEX idx_type (type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='缴费表'
        """)
        
        # 支付记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_payment_record (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bill_id INT NOT NULL COMMENT '账单ID',
                user_id INT NOT NULL COMMENT '用户ID',
                payment_no VARCHAR(100) NOT NULL UNIQUE COMMENT '支付流水号',
                amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
                payment_method ENUM('wechat', 'alipay', 'card', 'cash') NOT NULL COMMENT '支付方式',
                payment_status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending' COMMENT '支付状态',
                paid_time TIMESTAMP NULL COMMENT '支付时间',
                third_party_no VARCHAR(100) COMMENT '第三方支付单号',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_bill (bill_id),
                INDEX idx_user (user_id),
                INDEX idx_status (payment_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付记录表'
        """)
        
        conn.commit()
        logger.info("费用缴纳系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建费用缴纳系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_parking_tables():
    """创建智能停车系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 车位表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_parking_space (
                id INT AUTO_INCREMENT PRIMARY KEY,
                space_no VARCHAR(50) NOT NULL UNIQUE COMMENT '车位编号',
                space_type ENUM('fixed', 'temporary', 'visitor') DEFAULT 'fixed' COMMENT '车位类型',
                area VARCHAR(100) COMMENT '区域',
                status ENUM('idle', 'occupied', 'reserved', 'maintenance') DEFAULT 'idle' COMMENT '状态',
                user_id INT COMMENT '绑定用户ID',
                plate_number VARCHAR(20) COMMENT '绑定车牌号',
                monthly_fee DECIMAL(10,2) DEFAULT 0 COMMENT '月租费用',
                start_date DATE COMMENT '租期开始',
                end_date DATE COMMENT '租期结束',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_status (status),
                INDEX idx_plate (plate_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位表'
        """)
        
        # 车辆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_vehicle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL COMMENT '用户ID',
                plate_number VARCHAR(20) NOT NULL COMMENT '车牌号',
                vehicle_type ENUM('car', 'motorcycle', 'truck', 'other') DEFAULT 'car' COMMENT '车辆类型',
                brand VARCHAR(50) COMMENT '品牌',
                color VARCHAR(20) COMMENT '颜色',
                owner_name VARCHAR(50) COMMENT '车主姓名',
                owner_phone VARCHAR(20) COMMENT '车主电话',
                is_monthly TINYINT(1) DEFAULT 0 COMMENT '是否月租车',
                monthly_expire_date DATE COMMENT '月租到期日',
                status ENUM('active', 'inactive', 'blacklist') DEFAULT 'active' COMMENT '状态',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_plate (plate_number),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车辆表'
        """)
        
        # 停车记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_parking_record (
                id INT AUTO_INCREMENT PRIMARY KEY,
                space_id INT COMMENT '车位ID',
                vehicle_id INT COMMENT '车辆ID',
                plate_number VARCHAR(20) NOT NULL COMMENT '车牌号',
                entry_time TIMESTAMP NOT NULL COMMENT '入场时间',
                entry_gate VARCHAR(50) COMMENT '入口岗亭',
                entry_photo VARCHAR(500) COMMENT '入场照片',
                exit_time TIMESTAMP NULL COMMENT '出场时间',
                exit_gate VARCHAR(50) COMMENT '出口岗亭',
                exit_photo VARCHAR(500) COMMENT '出场照片',
                parking_duration INT COMMENT '停车时长（分钟）',
                fee DECIMAL(10,2) DEFAULT 0 COMMENT '停车费用',
                payment_status ENUM('unpaid', 'paid', 'free') DEFAULT 'unpaid' COMMENT '支付状态',
                payment_time TIMESTAMP NULL COMMENT '支付时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_plate (plate_number),
                INDEX idx_entry_time (entry_time),
                INDEX idx_status (payment_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='停车记录表'
        """)
        
        conn.commit()
        logger.info("智能停车系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建智能停车系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_locker_tables():
    """创建快递柜管理系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 快递柜表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_locker (
                id INT AUTO_INCREMENT PRIMARY KEY,
                locker_no VARCHAR(50) NOT NULL UNIQUE COMMENT '快递柜编号',
                locker_name VARCHAR(100) NOT NULL COMMENT '快递柜名称',
                location VARCHAR(200) COMMENT '位置',
                total_boxes INT NOT NULL DEFAULT 0 COMMENT '总格口数',
                large_boxes INT DEFAULT 0 COMMENT '大格口数',
                medium_boxes INT DEFAULT 0 COMMENT '中格口数',
                small_boxes INT DEFAULT 0 COMMENT '小格口数',
                status ENUM('online', 'offline', 'full', 'maintenance') DEFAULT 'online' COMMENT '状态',
                last_heartbeat TIMESTAMP NULL COMMENT '最后心跳',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='快递柜表'
        """)
        
        # 快递格口表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_locker_box (
                id INT AUTO_INCREMENT PRIMARY KEY,
                locker_id INT NOT NULL COMMENT '快递柜ID',
                box_no VARCHAR(20) NOT NULL COMMENT '格口编号',
                box_type ENUM('large', 'medium', 'small') DEFAULT 'medium' COMMENT '格口类型',
                status ENUM('idle', 'occupied', 'reserved', 'fault') DEFAULT 'idle' COMMENT '状态',
                current_package_id INT COMMENT '当前包裹ID',
                open_count INT DEFAULT 0 COMMENT '开箱次数',
                last_open_time TIMESTAMP NULL COMMENT '最后开箱时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_locker (locker_id),
                INDEX idx_status (status),
                UNIQUE KEY uk_locker_box (locker_id, box_no)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='快递格口表'
        """)
        
        # 包裹记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_package (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tracking_no VARCHAR(100) NOT NULL COMMENT '快递单号',
                courier_company VARCHAR(50) COMMENT '快递公司',
                locker_id INT NOT NULL COMMENT '快递柜ID',
                box_id INT NOT NULL COMMENT '格口ID',
                user_id INT NOT NULL COMMENT '收件用户ID',
                recipient_name VARCHAR(50) COMMENT '收件人姓名',
                recipient_phone VARCHAR(20) COMMENT '收件人电话',
                pickup_code VARCHAR(20) NOT NULL COMMENT '取件码',
                status ENUM('stored', 'picked', 'overdue', 'returned') DEFAULT 'stored' COMMENT '状态',
                store_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '存入时间',
                pickup_time TIMESTAMP NULL COMMENT '取件时间',
                overdue_time TIMESTAMP NULL COMMENT '超时时间',
                pickup_photo VARCHAR(500) COMMENT '取件照片',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_tracking (tracking_no),
                INDEX idx_status (status),
                INDEX idx_pickup_code (pickup_code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='包裹记录表'
        """)
        
        conn.commit()
        logger.info("快递柜管理系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建快递柜管理系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_visitor_tables():
    """创建访客管理系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 访客预约表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_visitor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visitor_name VARCHAR(50) NOT NULL COMMENT '访客姓名',
                visitor_phone VARCHAR(20) NOT NULL COMMENT '访客电话',
                visitor_idcard VARCHAR(18) COMMENT '身份证号',
                host_id INT NOT NULL COMMENT '被访用户ID',
                host_name VARCHAR(50) COMMENT '被访人姓名',
                host_phone VARCHAR(20) COMMENT '被访人电话',
                building_id INT COMMENT '楼栋ID',
                room_number VARCHAR(50) COMMENT '房间号',
                visit_purpose VARCHAR(200) COMMENT '来访事由',
                visit_date DATE NOT NULL COMMENT '来访日期',
                visit_time_start TIME COMMENT '预计到达时间',
                visit_time_end TIME COMMENT '预计离开时间',
                qr_code VARCHAR(255) COMMENT '访客二维码',
                status ENUM('pending', 'approved', 'rejected', 'completed', 'expired') DEFAULT 'pending' COMMENT '状态',
                approve_time TIMESTAMP NULL COMMENT '审批时间',
                entry_time TIMESTAMP NULL COMMENT '实际进入时间',
                exit_time TIMESTAMP NULL COMMENT '实际离开时间',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_host (host_id),
                INDEX idx_status (status),
                INDEX idx_date (visit_date),
                INDEX idx_phone (visitor_phone)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='访客预约表'
        """)
        
        # 访客进出记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_visitor_record (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visitor_id INT NOT NULL COMMENT '访客ID',
                device_id INT COMMENT '门禁设备ID',
                record_type ENUM('entry', 'exit') NOT NULL COMMENT '记录类型',
                record_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
                photo_url VARCHAR(500) COMMENT '抓拍照片',
                temperature DECIMAL(4,1) COMMENT '体温',
                remark TEXT COMMENT '备注',
                INDEX idx_visitor (visitor_id),
                INDEX idx_time (record_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='访客进出记录表'
        """)
        
        conn.commit()
        logger.info("访客管理系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建访客管理系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_complaint_tables():
    """创建投诉建议系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 投诉建议表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_complaint (
                id INT AUTO_INCREMENT PRIMARY KEY,
                complaint_no VARCHAR(50) NOT NULL UNIQUE COMMENT '投诉编号',
                user_id INT NOT NULL COMMENT '投诉人ID',
                user_name VARCHAR(50) COMMENT '投诉人姓名',
                user_phone VARCHAR(20) COMMENT '投诉人电话',
                complaint_type ENUM('service', 'facility', 'security', 'environment', 'noise', 'other') NOT NULL COMMENT '投诉类型',
                title VARCHAR(200) NOT NULL COMMENT '标题',
                content TEXT NOT NULL COMMENT '内容',
                images TEXT COMMENT '图片（JSON数组）',
                is_anonymous TINYINT(1) DEFAULT 0 COMMENT '是否匿名',
                contact_allowed TINYINT(1) DEFAULT 1 COMMENT '是否允许联系',
                status ENUM('pending', 'processing', 'resolved', 'closed') DEFAULT 'pending' COMMENT '状态',
                handler_id INT COMMENT '处理人ID',
                handler_name VARCHAR(50) COMMENT '处理人姓名',
                handle_result TEXT COMMENT '处理结果',
                handle_time TIMESTAMP NULL COMMENT '处理时间',
                satisfaction ENUM('very_satisfied', 'satisfied', 'neutral', 'dissatisfied', 'very_dissatisfied') COMMENT '满意度',
                feedback TEXT COMMENT '用户反馈',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user (user_id),
                INDEX idx_status (status),
                INDEX idx_type (complaint_type),
                INDEX idx_time (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='投诉建议表'
        """)
        
        # 投诉处理记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_complaint_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                complaint_id INT NOT NULL COMMENT '投诉ID',
                action ENUM('create', 'assign', 'process', 'resolve', 'close', 'feedback') NOT NULL COMMENT '操作类型',
                operator_id INT NOT NULL COMMENT '操作人ID',
                operator_name VARCHAR(50) COMMENT '操作人姓名',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_complaint (complaint_id),
                INDEX idx_action (action)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='投诉处理记录表'
        """)
        
        conn.commit()
        logger.info("投诉建议系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建投诉建议系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_monitoring_tables():
    """创建监控系统表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 监控设备表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_monitoring_device (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device_code VARCHAR(50) NOT NULL COMMENT '设备编号',
                device_name VARCHAR(100) NOT NULL COMMENT '设备名称',
                device_type ENUM('camera', 'sensor', 'alarm') NOT NULL COMMENT '设备类型',
                location VARCHAR(200) COMMENT '安装位置',
                building_id INT COMMENT '关联楼栋ID',
                status ENUM('online', 'offline', 'maintenance') DEFAULT 'offline' COMMENT '设备状态',
                ip_address VARCHAR(50) COMMENT 'IP地址',
                last_heartbeat TIMESTAMP NULL COMMENT '最后心跳时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_building (building_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='监控设备表'
        """)
        
        # 监控预警规则表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_monitoring_rule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rule_name VARCHAR(100) NOT NULL COMMENT '规则名称',
                device_type ENUM('camera', 'sensor', 'alarm') NOT NULL COMMENT '设备类型',
                alert_type VARCHAR(50) NOT NULL COMMENT '预警类型',
                threshold VARCHAR(100) COMMENT '阈值',
                is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_device_type (device_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='监控预警规则表'
        """)
        
        # 监控预警记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_monitoring_alert (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device_id INT NOT NULL COMMENT '设备ID',
                rule_id INT COMMENT '规则ID',
                alert_type VARCHAR(50) NOT NULL COMMENT '预警类型',
                alert_level ENUM('info', 'warning', 'error', 'critical') DEFAULT 'warning' COMMENT '预警级别',
                alert_content TEXT COMMENT '预警内容',
                status ENUM('pending', 'processed', 'ignored') DEFAULT 'pending' COMMENT '处理状态',
                processed_by INT COMMENT '处理人ID',
                processed_time TIMESTAMP NULL COMMENT '处理时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_device (device_id),
                INDEX idx_rule (rule_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='监控预警记录表'
        """)
        
        conn.commit()
        logger.info("监控系统表创建完成")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建监控系统表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_activity_tables():
    """创建社区活动表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 活动表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_activity (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL COMMENT '活动标题',
                description TEXT COMMENT '活动描述',
                start_time DATETIME NOT NULL COMMENT '开始时间',
                end_time DATETIME NOT NULL COMMENT '结束时间',
                location VARCHAR(200) COMMENT '活动地点',
                max_participants INT DEFAULT 0 COMMENT '最大参与人数',
                current_participants INT DEFAULT 0 COMMENT '当前参与人数',
                status ENUM('draft', 'published', 'completed', 'cancelled') DEFAULT 'draft' COMMENT '活动状态',
                image_url VARCHAR(500) COMMENT '活动图片URL',
                organizer VARCHAR(100) COMMENT '组织者',
                contact_phone VARCHAR(20) COMMENT '联系电话',
                category ENUM('culture', 'sports', 'education', 'charity', 'other') DEFAULT 'other' COMMENT '活动分类',
                tags VARCHAR(500) COMMENT '活动标签',
                remark TEXT COMMENT '备注',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_status (status),
                INDEX idx_category (category),
                INDEX idx_start_time (start_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社区活动表'
        """)
        
        # 活动参与者表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS t_activity_participant (
                id INT AUTO_INCREMENT PRIMARY KEY,
                activity_id INT NOT NULL COMMENT '活动ID',
                user_id INT NOT NULL COMMENT '用户ID',
                user_name VARCHAR(50) COMMENT '用户姓名',
                user_phone VARCHAR(20) COMMENT '用户电话',
                sign_in_status ENUM('not_signed', 'signed') DEFAULT 'not_signed' COMMENT '签到状态',
                sign_in_time TIMESTAMP NULL COMMENT '签到时间',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_activity (activity_id),
                INDEX idx_user (user_id),
                UNIQUE KEY uk_activity_user (activity_id, user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动参与者表'
        """)
        
        conn.commit()
        logger.info("✅ 社区活动表创建成功")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"创建社区活动表失败: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def init_all_tables():
    """初始化所有智慧社区基础功能表"""
    logger.info("开始创建智慧社区基础功能数据库表...")
    
    try:
        create_access_control_tables()
        create_repair_tables()
        create_notice_tables()
        create_utility_tables()
        create_payment_tables()
        create_parking_tables()
        create_locker_tables()
        create_visitor_tables()
        create_complaint_tables()
        create_monitoring_tables()
        create_activity_tables()
        
        logger.info("✅ 所有智慧社区基础功能数据库表创建完成！")
        
    except Exception as e:
        logger.error(f"初始化数据库表失败: {e}")
        raise


if __name__ == '__main__':
    init_all_tables()
