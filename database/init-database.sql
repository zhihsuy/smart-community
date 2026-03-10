-- 智慧社区数据库初始化脚本
-- 执行方式：在MySQL中运行此脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS smart_community 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE smart_community;

-- ============================================
-- 1. 用户相关表
-- ============================================

-- 用户表
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

-- 楼栋表
CREATE TABLE IF NOT EXISTS t_building (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    community_id BIGINT UNSIGNED NOT NULL COMMENT '社区ID',
    name VARCHAR(50) NOT NULL COMMENT '楼栋名称',
    unit_count INT UNSIGNED DEFAULT 1 COMMENT '单元数',
    floor_count INT UNSIGNED DEFAULT 0 COMMENT '层数',
    household_count INT UNSIGNED DEFAULT 0 COMMENT '户数',
    
    PRIMARY KEY (id),
    KEY idx_community (community_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='楼栋表';

-- 社区表
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

-- ============================================
-- 初始化数据
-- ============================================

-- 插入社区数据
INSERT INTO t_community (name, code, province, city, district, address, total_buildings, total_households, property_company, contact_phone) VALUES
('智慧花园小区', 'ZH_HY_001', '广东省', '深圳市', '南山区', '科技园南区123号', 10, 500, '万科物业', '400-123-4567')
ON DUPLICATE KEY UPDATE name = name;

-- 插入楼栋数据
INSERT INTO t_building (id, community_id, name, unit_count, floor_count, household_count) VALUES
(1, 1, '1号楼', 2, 18, 72),
(2, 1, '2号楼', 2, 18, 72),
(3, 1, '3号楼', 2, 18, 72),
(4, 1, '4号楼', 2, 18, 72),
(5, 1, '5号楼', 2, 18, 72)
ON DUPLICATE KEY UPDATE name = name;

-- 插入测试用户数据（密码: 123456）
INSERT INTO t_user (id, phone, password, nickname, email, gender, building_id, unit, room_number, family_structure, interest_tags, status, is_verified, role) VALUES
(1, '13800138000', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '测试用户', 'test@example.com', 1, 1, '1单元', '101', '三口之家', '["团购", "亲子"]', 1, 0, '居民'),
(2, '13900139000', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '运营用户', 'op@example.com', 1, 2, '1单元', '201', '四口之家', '["运动", "美食"]', 1, 1, '运营'),
(3, '13700137000', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EO', '管理员', 'admin@example.com', 1, 3, '1单元', '301', '两口之家', '["旅游", "阅读"]', 1, 1, '管理员')
ON DUPLICATE KEY UPDATE phone = phone;

-- 查看创建结果
SELECT '数据库初始化完成' AS message;
SELECT * FROM t_community LIMIT 1;
SELECT * FROM t_building;

-- ============================================
-- 权限相关初始化数据
-- ============================================

-- 插入默认权限
INSERT INTO t_permission (code, name, description, type, resource, method) VALUES
-- 基础用户权限
('user:info:read', '查看用户信息', '查看用户基本信息', 'api', '/v1/*/user/info', 'GET'),
('user:info:update', '更新用户信息', '更新用户基本信息', 'api', '/v1/*/user/info', 'PUT'),
('user:avatar:upload', '上传头像', '上传用户头像', 'api', '/v1/*/user/upload-avatar', 'POST'),
('user:password:change', '修改密码', '修改用户密码', 'api', '/v1/*/user/password', 'PUT'),
('user:phone:change', '修改手机号', '修改用户手机号', 'api', '/v1/*/user/phone', 'PUT'),
('user:interest-tags:update', '更新兴趣标签', '更新用户兴趣标签', 'api', '/v1/*/user/interest-tags', 'PUT'),

-- 楼栋相关权限
('building:list:read', '查看楼栋列表', '查看社区楼栋列表', 'api', '/v1/*/buildings', 'GET'),

-- 管理员权限
('admin:user:list', '查看用户列表', '查看所有用户列表', 'api', '/v1/*/admin/users', 'GET'),
('admin:user:create', '创建用户', '创建新用户', 'api', '/v1/*/admin/users', 'POST'),
('admin:user:update', '编辑用户', '编辑用户信息', 'api', '/v1/*/admin/users/*', 'PUT'),
('admin:user:delete', '删除用户', '删除用户', 'api', '/v1/*/admin/users/*', 'DELETE'),
('admin:building:list', '查看楼栋列表', '查看所有楼栋列表', 'api', '/v1/*/admin/buildings', 'GET'),
('admin:building:create', '创建楼栋', '创建新楼栋', 'api', '/v1/*/admin/buildings', 'POST'),
('admin:building:update', '编辑楼栋', '编辑楼栋信息', 'api', '/v1/*/admin/buildings/*', 'PUT'),
('admin:building:delete', '删除楼栋', '删除楼栋', 'api', '/v1/*/admin/buildings/*', 'DELETE'),

-- 运营权限
('op:user:list', '查看用户列表', '查看用户列表', 'api', '/v1/*/op/users', 'GET'),
('op:user:update', '编辑用户', '编辑用户信息', 'api', '/v1/*/op/users/*', 'PUT'),
('op:building:list', '查看楼栋列表', '查看楼栋列表', 'api', '/v1/*/op/buildings', 'GET');

-- 插入角色权限关联
-- 居民角色权限
INSERT INTO t_role_permission (role, permission_id) VALUES
('居民', (SELECT id FROM t_permission WHERE code = 'user:info:read')),
('居民', (SELECT id FROM t_permission WHERE code = 'user:info:update')),
('居民', (SELECT id FROM t_permission WHERE code = 'user:avatar:upload')),
('居民', (SELECT id FROM t_permission WHERE code = 'user:password:change')),
('居民', (SELECT id FROM t_permission WHERE code = 'user:phone:change')),
('居民', (SELECT id FROM t_permission WHERE code = 'user:interest-tags:update')),
('居民', (SELECT id FROM t_permission WHERE code = 'building:list:read'));

-- 运营角色权限
INSERT INTO t_role_permission (role, permission_id) VALUES
('运营', (SELECT id FROM t_permission WHERE code = 'user:info:read')),
('运营', (SELECT id FROM t_permission WHERE code = 'user:info:update')),
('运营', (SELECT id FROM t_permission WHERE code = 'user:avatar:upload')),
('运营', (SELECT id FROM t_permission WHERE code = 'user:password:change')),
('运营', (SELECT id FROM t_permission WHERE code = 'user:phone:change')),
('运营', (SELECT id FROM t_permission WHERE code = 'user:interest-tags:update')),
('运营', (SELECT id FROM t_permission WHERE code = 'building:list:read')),
('运营', (SELECT id FROM t_permission WHERE code = 'op:user:list')),
('运营', (SELECT id FROM t_permission WHERE code = 'op:user:update')),
('运营', (SELECT id FROM t_permission WHERE code = 'op:building:list'));

-- 管理员角色权限 (拥有所有权限)
INSERT INTO t_role_permission (role, permission_id) 
SELECT '管理员', id FROM t_permission;
SELECT id, phone, nickname, email, building_id, unit, room_number, family_structure FROM t_user LIMIT 1;
