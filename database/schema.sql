-- 智慧社区Web应用数据库设计
-- MySQL 8.0 + InnoDB + utf8mb4
-- 创建时间: 2026-03-05

-- 创建数据库
CREATE DATABASE IF NOT EXISTS smart_community 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE smart_community;

-- ============================================
-- 1. 用户相关表
-- ============================================

-- 用户表
CREATE TABLE t_user (
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
    
    -- 社区信息
    community_id BIGINT UNSIGNED DEFAULT NULL COMMENT '所属社区ID',
    building_id BIGINT UNSIGNED DEFAULT NULL COMMENT '楼栋ID',
    unit VARCHAR(20) DEFAULT NULL COMMENT '单元',
    room_number VARCHAR(20) DEFAULT NULL COMMENT '房号',
    
    -- 多平台适配
    platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型: pc/h5/admin',
    device_id VARCHAR(100) DEFAULT NULL COMMENT '设备ID',
    
    -- 兴趣标签(用于推荐算法)
    interest_tags JSON DEFAULT NULL COMMENT '兴趣标签: ["亲子", "运动", "美食"]',
    family_structure VARCHAR(50) DEFAULT NULL COMMENT '家庭结构: 单身/夫妻/有孩/三代同堂',
    consumption_level TINYINT DEFAULT 2 COMMENT '消费能力: 1-低 2-中 3-高',
    
    -- 账户状态
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-禁用 1-正常 2-未认证',
    is_verified TINYINT DEFAULT 0 COMMENT '是否实名认证: 0-否 1-是',
    role VARCHAR(20) NOT NULL DEFAULT '居民' COMMENT '角色: 居民/运营/管理员',
    
    -- 时间戳
    last_login_time DATETIME DEFAULT NULL COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) DEFAULT NULL COMMENT '最后登录IP',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_phone (phone),
    KEY idx_community (community_id),
    KEY idx_status (status),
    KEY idx_platform (platform_type),
    KEY idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户行为日志表(按月分表: t_user_behavior_202401)
CREATE TABLE t_user_behavior (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    item_id BIGINT UNSIGNED NOT NULL COMMENT '物品ID(商品/活动/服务)',
    item_type VARCHAR(20) NOT NULL COMMENT '物品类型: goods/activity/service',
    behavior_type VARCHAR(20) NOT NULL COMMENT '行为类型: view/click/collect/purchase/share',
    behavior_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行为时间',
    duration INT UNSIGNED DEFAULT 0 COMMENT '浏览时长(秒)',
    
    -- 多平台信息
    platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型: pc/h5/admin',
    device_info VARCHAR(255) DEFAULT NULL COMMENT '设备信息',
    
    -- 地理位置(用于推荐)
    longitude DECIMAL(10, 7) DEFAULT NULL COMMENT '经度',
    latitude DECIMAL(10, 7) DEFAULT NULL COMMENT '纬度',
    
    -- 扩展信息
    extra_data JSON DEFAULT NULL COMMENT '扩展数据',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    PRIMARY KEY (id),
    KEY idx_user_id (user_id),
    KEY idx_item (item_id, item_type),
    KEY idx_behavior (behavior_type),
    KEY idx_time (behavior_time),
    KEY idx_platform (platform_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户行为日志表';

-- 用户收藏表
CREATE TABLE t_user_favorite (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    item_id BIGINT UNSIGNED NOT NULL COMMENT '物品ID',
    item_type VARCHAR(20) NOT NULL COMMENT '物品类型',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_user_item (user_id, item_id, item_type),
    KEY idx_user (user_id),
    KEY idx_item (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- ============================================
-- 2. 社区相关表
-- ============================================

-- 社区表
CREATE TABLE t_community (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '社区ID',
    name VARCHAR(100) NOT NULL COMMENT '社区名称',
    code VARCHAR(50) NOT NULL COMMENT '社区编码',
    province VARCHAR(50) NOT NULL COMMENT '省',
    city VARCHAR(50) NOT NULL COMMENT '市',
    district VARCHAR(50) NOT NULL COMMENT '区/县',
    address VARCHAR(255) NOT NULL COMMENT '详细地址',
    longitude DECIMAL(10, 7) DEFAULT NULL COMMENT '经度',
    latitude DECIMAL(10, 7) DEFAULT NULL COMMENT '纬度',
    
    -- 社区信息
    total_buildings INT UNSIGNED DEFAULT 0 COMMENT '总楼栋数',
    total_households INT UNSIGNED DEFAULT 0 COMMENT '总户数',
    property_company VARCHAR(100) DEFAULT NULL COMMENT '物业公司',
    contact_phone VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
    
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-禁用 1-正常',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_code (code),
    KEY idx_city (city),
    KEY idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社区表';

-- 楼栋表
CREATE TABLE t_building (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    community_id BIGINT UNSIGNED NOT NULL COMMENT '社区ID',
    name VARCHAR(50) NOT NULL COMMENT '楼栋名称',
    unit_count INT UNSIGNED DEFAULT 1 COMMENT '单元数',
    floor_count INT UNSIGNED DEFAULT 0 COMMENT '层数',
    household_count INT UNSIGNED DEFAULT 0 COMMENT '户数',
    
    PRIMARY KEY (id),
    KEY idx_community (community_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='楼栋表';



-- ============================================
-- 4. 活动相关表
-- ============================================

-- 活动表
CREATE TABLE t_activity (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '活动ID',
    community_id BIGINT UNSIGNED NOT NULL COMMENT '社区ID',
    organizer_id BIGINT UNSIGNED NOT NULL COMMENT '组织者ID',
    
    -- 活动信息
    title VARCHAR(200) NOT NULL COMMENT '活动标题',
    type VARCHAR(50) NOT NULL COMMENT '活动类型: 亲子/运动/文化/公益',
    description TEXT COMMENT '活动描述',
    cover_image VARCHAR(255) DEFAULT NULL COMMENT '封面图',
    images JSON COMMENT '活动图片',
    
    -- 时间地点
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NOT NULL COMMENT '结束时间',
    location VARCHAR(255) NOT NULL COMMENT '活动地点',
    longitude DECIMAL(10, 7) DEFAULT NULL COMMENT '经度',
    latitude DECIMAL(10, 7) DEFAULT NULL COMMENT '纬度',
    
    -- 参与信息
    max_participants INT UNSIGNED DEFAULT 0 COMMENT '最大参与人数(0为不限)',
    current_participants INT UNSIGNED DEFAULT 0 COMMENT '当前参与人数',
    
    -- 标签(用于推荐算法)
    tags JSON DEFAULT NULL COMMENT '标签: ["亲子", "户外", "免费"]',
    
    -- 状态
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 0-草稿 1-报名中 2-进行中 3-已结束 4-已取消',
    
    -- 多平台同步
    sync_status TINYINT DEFAULT 0 COMMENT '同步状态',
    sync_time DATETIME DEFAULT NULL COMMENT '同步时间',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_community (community_id),
    KEY idx_type (type),
    KEY idx_status (status),
    KEY idx_time (start_time, end_time),
    KEY idx_platform (sync_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活动表';

-- 活动报名表
CREATE TABLE t_activity_registration (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    activity_id BIGINT UNSIGNED NOT NULL COMMENT '活动ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    participant_count INT UNSIGNED DEFAULT 1 COMMENT '参与人数',
    contact_name VARCHAR(50) DEFAULT NULL COMMENT '联系人',
    contact_phone VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
    remark VARCHAR(500) DEFAULT NULL COMMENT '备注',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-取消 1-正常',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_activity_user (activity_id, user_id),
    KEY idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活动报名表';

-- ============================================
-- 5. AI相关表
-- ============================================

-- AI分析结果表
CREATE TABLE t_ai_analysis (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分析ID',
    user_id BIGINT UNSIGNED DEFAULT NULL COMMENT '用户ID',
    analysis_type VARCHAR(50) NOT NULL COMMENT '分析类型: garbage_chat/service_match/complaint_classify',
    
    -- 输入内容
    input_content TEXT COMMENT '输入内容(文字)',
    input_image VARCHAR(255) DEFAULT NULL COMMENT '输入图片URL',
    
    -- 分析结果
    analysis_result TEXT NOT NULL COMMENT '分析结果',
    result_data JSON DEFAULT NULL COMMENT '结果结构化数据',
    confidence DECIMAL(5, 4) DEFAULT NULL COMMENT '置信度(0-1)',
    accuracy DECIMAL(5, 4) DEFAULT NULL COMMENT '准确率(人工标注后回填)',
    
    -- 处理信息
    processing_time_ms INT UNSIGNED DEFAULT NULL COMMENT '处理耗时(ms)',
    model_version VARCHAR(50) DEFAULT NULL COMMENT '模型版本',
    
    -- 反馈信息
    is_correct TINYINT DEFAULT NULL COMMENT '是否正确: 0-否 1-是',
    feedback TEXT DEFAULT NULL COMMENT '用户反馈',
    
    -- 多平台信息
    platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_user (user_id),
    KEY idx_type (analysis_type),
    KEY idx_created (created_at),
    KEY idx_platform (platform_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI分析结果表';

-- 垃圾分类知识库表
CREATE TABLE t_garbage_knowledge (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '垃圾名称',
    category VARCHAR(50) NOT NULL COMMENT '分类: 可回收物/有害垃圾/厨余垃圾/其他垃圾',
    description TEXT COMMENT '描述',
    disposal_method TEXT COMMENT '投放建议',
    image_url VARCHAR(255) DEFAULT NULL COMMENT '图片URL',
    keywords JSON DEFAULT NULL COMMENT '关键词',
    search_count INT UNSIGNED DEFAULT 0 COMMENT '搜索次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_category (category),
    KEY idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='垃圾分类知识库表';

-- ============================================
-- 4. 权限相关表
-- ============================================

-- 权限表
CREATE TABLE t_permission (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 角色权限关联表
CREATE TABLE t_role_permission (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '关联ID',
    role VARCHAR(20) NOT NULL COMMENT '角色名称',
    permission_id BIGINT UNSIGNED NOT NULL COMMENT '权限ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_role_permission (role, permission_id),
    KEY idx_role (role),
    KEY idx_permission (permission_id),
    CONSTRAINT fk_role_permission_permission FOREIGN KEY (permission_id) REFERENCES t_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- ============================================
-- 6. 推荐相关表
-- ============================================

-- 推荐记录表
CREATE TABLE t_recommendation (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '推荐ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 推荐内容
    item_id BIGINT UNSIGNED NOT NULL COMMENT '物品ID',
    item_type VARCHAR(20) NOT NULL COMMENT '物品类型: goods/activity',
    
    -- 推荐算法信息
    algorithm_type VARCHAR(50) NOT NULL COMMENT '算法类型: collaborative/content/hot/new',
    score DECIMAL(10, 6) NOT NULL COMMENT '推荐分数',
    reason TEXT DEFAULT NULL COMMENT '推荐理由',
    
    -- 用户反馈
    is_clicked TINYINT DEFAULT 0 COMMENT '是否点击: 0-否 1-是',
    is_liked TINYINT DEFAULT 0 COMMENT '是否喜欢: 0-无 1-喜欢 2-不喜欢',
    click_time DATETIME DEFAULT NULL COMMENT '点击时间',
    
    -- 多平台信息
    platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型',
    scene VARCHAR(50) DEFAULT 'home' COMMENT '推荐场景: home/detail/search/push',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_user (user_id),
    KEY idx_item (item_id, item_type),
    KEY idx_algorithm (algorithm_type),
    KEY idx_created (created_at),
    KEY idx_platform (platform_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推荐记录表';

-- 物品特征表(用于内容推荐)
CREATE TABLE t_item_feature (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    item_id BIGINT UNSIGNED NOT NULL COMMENT '物品ID',
    item_type VARCHAR(20) NOT NULL COMMENT '物品类型',
    feature_key VARCHAR(50) NOT NULL COMMENT '特征键',
    feature_value VARCHAR(255) NOT NULL COMMENT '特征值',
    weight DECIMAL(5, 4) DEFAULT 1.0 COMMENT '权重',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY uk_item_feature (item_id, item_type, feature_key),
    KEY idx_type (item_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物品特征表';

-- ============================================
-- 7. 消息通知表
-- ============================================

-- 消息表
CREATE TABLE t_message (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '消息ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 消息内容
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    type VARCHAR(50) NOT NULL COMMENT '类型: system/order/activity/ai',
    
    -- 推送方式
    push_channels JSON COMMENT '推送渠道: ["inbox", "browser", "sms"]',
    
    -- 状态
    is_read TINYINT DEFAULT 0 COMMENT '是否已读: 0-否 1-是',
    read_time DATETIME DEFAULT NULL COMMENT '阅读时间',
    
    -- 多平台信息
    platform_type VARCHAR(20) NOT NULL DEFAULT 'pc' COMMENT '平台类型',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_user (user_id),
    KEY idx_type (type),
    KEY idx_read (is_read),
    KEY idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- ============================================
-- 8. 政务/服务相关表
-- ============================================

-- 政务服务表
CREATE TABLE t_government_service (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '服务ID',
    category VARCHAR(50) NOT NULL COMMENT '服务类别',
    name VARCHAR(200) NOT NULL COMMENT '服务名称',
    description TEXT COMMENT '服务描述',
    required_materials JSON COMMENT '所需材料清单',
    process_steps JSON COMMENT '办理流程',
    processing_time VARCHAR(100) DEFAULT NULL COMMENT '办理时限',
    contact_phone VARCHAR(20) DEFAULT NULL COMMENT '咨询电话',
    location VARCHAR(255) DEFAULT NULL COMMENT '办理地点',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-停用 1-启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_category (category),
    KEY idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='政务服务表';

-- 服务预约表
CREATE TABLE t_service_appointment (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    service_id BIGINT UNSIGNED NOT NULL COMMENT '服务ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    appointment_date DATE NOT NULL COMMENT '预约日期',
    appointment_time VARCHAR(20) NOT NULL COMMENT '预约时间段',
    status TINYINT DEFAULT 0 COMMENT '状态: 0-待确认 1-已确认 2-已完成 3-已取消',
    remark VARCHAR(500) DEFAULT NULL COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_service (service_id),
    KEY idx_user (user_id),
    KEY idx_date (appointment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='服务预约表';

-- ============================================
-- 9. 投诉建议表
-- ============================================

-- 投诉建议表
CREATE TABLE t_complaint (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '投诉ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 投诉内容
    type VARCHAR(50) NOT NULL COMMENT '类型: 物业/环境/安全/噪音/其他',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    images JSON COMMENT '图片证据',
    
    -- AI分类结果
    ai_category VARCHAR(50) DEFAULT NULL COMMENT 'AI分类结果',
    ai_confidence DECIMAL(5, 4) DEFAULT NULL COMMENT 'AI置信度',
    
    -- 处理信息
    status TINYINT DEFAULT 0 COMMENT '状态: 0-待处理 1-处理中 2-已处理 3-已关闭',
    handler_id BIGINT UNSIGNED DEFAULT NULL COMMENT '处理人ID',
    handle_result TEXT DEFAULT NULL COMMENT '处理结果',
    handle_time DATETIME DEFAULT NULL COMMENT '处理时间',
    
    -- 满意度
    satisfaction TINYINT DEFAULT NULL COMMENT '满意度: 1-5星',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    KEY idx_user (user_id),
    KEY idx_type (type),
    KEY idx_status (status),
    KEY idx_ai_category (ai_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='投诉建议表';

-- ============================================
-- 初始化数据
-- ============================================

-- 插入垃圾分类知识库示例数据
INSERT INTO t_garbage_knowledge (name, category, description, disposal_method, keywords) VALUES
('废纸', '可回收物', '报纸、期刊、图书、各种包装纸等', '清洁干燥后投放', '["纸", "报纸", "书本"]'),
('塑料瓶', '可回收物', '饮料瓶、洗发水瓶等塑料制品', '清洗干净后压扁投放', '["塑料", "瓶子", "饮料瓶"]'),
('废电池', '有害垃圾', '充电电池、纽扣电池、蓄电池等', '投放至有害垃圾收集容器', '["电池", "充电电池", "纽扣电池"]'),
('剩菜剩饭', '厨余垃圾', '剩菜、剩饭、果皮、蛋壳等', '沥干水分后投放', '["食物", "剩菜", "果皮"]'),
('卫生纸', '其他垃圾', '污损的纸张、卫生纸、尿不湿等', '投放至其他垃圾收集容器', '["纸巾", "卫生纸", "尿不湿"]'),
('玻璃瓶', '可回收物', '酱油瓶、调料瓶等玻璃制品', '清洗干净后小心投放', '["玻璃", "瓶子", "酱油瓶"]'),
('过期药品', '有害垃圾', '过期药物、药品包装等', '连同包装投放至有害垃圾收集容器', '["药品", "药物", "过期"]'),
('茶叶渣', '厨余垃圾', '泡过的茶叶、茶包等', '沥干水分后投放', '["茶叶", "茶包", "茶渣"]'),
('一次性餐具', '其他垃圾', '一次性筷子、餐盒、纸杯等', '投放至其他垃圾收集容器', '["一次性", "筷子", "餐盒"]'),
('易拉罐', '可回收物', '铝制饮料罐、金属罐头等', '压扁后投放', '["金属", "铝罐", "罐头"]');



-- 插入政务服务示例数据
INSERT INTO t_government_service (category, name, description, required_materials, process_steps, processing_time, contact_phone) VALUES
('户籍办理', '居住证办理', '为非本地户籍居民提供居住证办理服务', '["身份证", "居住证明", "照片"]','["在线预约", "现场提交材料", "审核", "领取证件"]', '15个工作日', '12345'),
('社保服务', '社保查询', '查询个人社保缴纳记录和余额', '["身份证", "社保卡"]','["在线申请", "身份验证", "查询结果"]', '即时', '12333'),
('医疗服务', '医保报销', '办理医疗费用报销手续', '["发票", "病历", "医保卡"]','["提交申请", "材料审核", "报销到账"]', '30个工作日', '12320');
