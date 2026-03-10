# 智慧社区Web应用开发

## 项目概述

智慧社区Web应用是一个覆盖多平台（PC Web/移动端H5/管理端）的综合社区服务平台，集成了AI能力和智能推荐算法，为居民提供便捷的社区服务。项目重点打造智慧绿能模块，通过AI技术推动绿色生活方式。

## 核心功能

### 1. 多平台支持
- **PC Web端**: Vue 3 + Element Plus，适配Chrome 90+/Firefox 88+/Edge 90+
- **移动端H5**: Vue 3 + Vant，适配iOS 12+/Android 8+
- **管理端**: Element Plus，支持大屏数据可视化

### 2. 智慧绿能模块
- **碳足迹计算器**: 计算个人和家庭的碳排放量，提供减排建议
- **绿色社区论坛**: 社区居民交流绿色生活经验，分享环保心得
- **环保数据监测**: 实时监测社区环境数据，包括空气质量、噪音等
- **节能小贴士**: 提供日常生活中的节能环保建议和技巧
- **绿色购物指南**: 推荐环保产品，提供绿色消费指导
- **绿色积分系统**: 通过环保行为获取积分，积分可兑换环保产品

### 3. AI智能建议
- **AI绿色生活建议**: 基于AI规则引擎提供个性化绿色生活建议
- **绿色出行规划**: 集成地图API，提供绿色出行路线规划，比较不同出行方式的碳排放
- **家居节能优化**: 提供家居能耗分析和优化建议，实现节能方案模拟和效果预测

### 4. AI垃圾分类识别
- **文字识别**: 基于LSTM的文本分类模型，准确识别垃圾类型
- **图片识别**: 基于MobileNetV2的图像分类模型，支持拍照识别垃圾

### 5. 智慧社区管理
- **智能门禁管理**: 门禁设备管理、权限控制、出入记录、远程开门
- **物业报修管理**: 报修订单管理、维修人员管理、维修统计
- **公告通知管理**: 发布社区公告、通知管理、公告详情
- **智能水电管理**: 水电表管理、使用统计、异常预警
- **费用缴纳管理**: 账单管理、缴费记录、费用统计
- **智能停车管理**: 停车位管理、车辆管理、停车记录
- **快递柜管理**: 快递柜管理、包裹管理、取件记录
- **访客管理**: 访客预约、访客登记、访客记录
- **投诉建议管理**: 投诉提交、处理流程、统计分析
- **监控管理**: 监控设备管理、监控记录查询
- **社区活动管理**: 活动发布、报名管理、活动统计

### 6. 管理员系统
- **用户管理**: 查看和管理所有用户信息，支持角色分配
- **商家管理**: 审核商家入驻申请，管理商家店铺
- **商品管理**: 管理平台商品信息
- **评价管理**: 管理用户评价，支持AI内容检测
- **楼栋管理**: 管理社区楼栋和房间信息
- **数据统计**: 查看平台整体运营数据

## 技术架构

### 前端技术栈
- Vue 3.4 + Vite 5.0
- Pinia 2.1（状态管理）
- Vue Router 4.2
- Element Plus（PC端）
- Vant（移动端）
- Axios（HTTP请求）
- Chart.js（数据可视化）

### 后端技术栈
- **Python 3.9+** + Flask 3.0
- PyMySQL（MySQL连接）
- PyJWT（JWT认证）
- bcrypt（密码加密）
- Flask-CORS（跨域支持）

### 机器学习技术栈
- TensorFlow 2.13 + Keras 2.13
- NumPy, Pandas, Scikit-learn
- OpenCV（图像处理）
- Jieba（中文分词）
- Matplotlib, Seaborn（数据可视化）

### 数据库
- MySQL 8.0（主数据库）
- Redis 7.0（缓存，可选）

## 项目结构

```
smart-community/
├── frontend/              # 前端项目
│   └── pc-web/           # PC Web端 (Vue 3 + Element Plus)
│       ├── src/
│       │   ├── views/           # 页面组件
│       │   │   ├── GreenEnergy.vue              # 智慧绿能主页面
│       │   │   ├── green-energy/               # 智慧绿能子模块
│       │   │   │   ├── CarbonFootprint.vue      # 碳足迹计算器
│       │   │   │   ├── GreenForum.vue          # 绿色社区论坛
│       │   │   │   ├── EnvironmentalData.vue    # 环保数据监测
│       │   │   │   ├── EnergyTips.vue          # 节能小贴士
│       │   │   │   ├── GreenShopping.vue       # 绿色购物指南
│       │   │   │   ├── GreenPoints.vue         # 绿色积分系统
│       │   │   │   ├── AIGreenTips.vue        # AI绿色生活建议
│       │   │   │   ├── GreenTravel.vue         # 绿色出行规划
│       │   │   │   └── HomeEnergyOptimization.vue  # 家居节能优化
│       │   │   ├── smart-community/           # 智慧社区子模块
│       │   │   │   ├── AccessControl.vue       # 智能门禁
│       │   │   │   ├── AccessRecords.vue       # 门禁记录
│       │   │   │   ├── Repair.vue              # 物业报修
│       │   │   │   ├── MyRepairOrders.vue      # 我的报修
│       │   │   │   ├── Notices.vue             # 公告通知
│       │   │   │   ├── NoticeDetail.vue        # 公告详情
│       │   │   │   ├── Utility.vue             # 智能水电
│       │   │   │   ├── UtilityUsage.vue        # 水电使用
│       │   │   │   ├── Payment.vue             # 费用缴纳
│       │   │   │   ├── MyBills.vue             # 我的账单
│       │   │   │   ├── Parking.vue             # 智能停车
│       │   │   │   ├── MyVehicles.vue          # 我的车辆
│       │   │   │   ├── Locker.vue              # 快递柜
│       │   │   │   ├── MyPackages.vue          # 我的包裹
│       │   │   │   ├── Visitor.vue             # 访客管理
│       │   │   │   ├── VisitorAppointments.vue # 访客预约
│       │   │   │   ├── VisitorRecords.vue      # 访客记录
│       │   │   │   ├── Complaint.vue           # 投诉建议
│       │   │   │   └── MyComplaints.vue        # 我的投诉
│       │   │   ├── admin/                     # 管理员页面
│       │   │   │   ├── Dashboard.vue          # 管理员仪表板
│       │   │   │   ├── UserManage.vue        # 用户管理
│       │   │   │   ├── BuildingManage.vue    # 楼栋管理
│       │   │   │   ├── ReviewManage.vue      # 评价管理
│       │   │   │   ├── Settings.vue          # 系统设置
│       │   │   │   ├── smart-community/       # 智慧社区管理
│       │   │   │   │   ├── AccessControlDevices.vue   # 门禁设备
│       │   │   │   │   ├── AccessControlPermissions.vue # 门禁权限
│       │   │   │   │   ├── AccessControlRecords.vue    # 门禁记录
│       │   │   │   │   ├── Activity.vue               # 活动管理
│       │   │   │   │   ├── RepairOrders.vue           # 报修订单
│       │   │   │   │   ├── RepairTechnicians.vue      # 维修人员
│       │   │   │   │   ├── RepairStatistics.vue       # 维修统计
│       │   │   │   │   ├── Notices.vue                # 公告管理
│       │   │   │   │   ├── UtilityMeters.vue          # 水电表管理
│       │   │   │   │   ├── UtilityUsage.vue           # 水电使用
│       │   │   │   │   ├── UtilityAlerts.vue          # 水电预警
│       │   │   │   │   ├── Payment.vue                # 费用管理
│       │   │   │   │   ├── Parking.vue                # 停车管理
│       │   │   │   │   ├── Locker.vue                 # 快递柜管理
│       │   │   │   │   ├── Visitor.vue                # 访客管理
│       │   │   │   │   ├── Complaints.vue             # 投诉管理
│       │   │   │   │   └── Monitoring.vue             # 监控管理
│       │   │   │   └── green-energy/           # 绿色能源管理
│       │   │   │       ├── GarbageClassification.vue  # 垃圾分类
│       │   │   │       ├── GarbageRecords.vue         # 垃圾记录
│       │   │   │       ├── GarbageStatistics.vue      # 垃圾统计
│       │   │   │       ├── CarbonFootprint.vue        # 碳足迹管理
│       │   │   │       ├── GreenForum.vue             # 绿色论坛
│       │   │   │       ├── Environment.vue            # 环保数据
│       │   │   │       ├── GreenPoints.vue            # 绿色积分
│       │   │   │       ├── AITips.vue                 # AI建议
│       │   │   │       ├── GreenTravel.vue            # 绿色出行
│       │   │   │       ├── EnergyOptimization.vue     # 节能优化
│       │   │   │       ├── Health.vue                 # 健康管理
│       │   │   │       ├── Diet.vue                   # 饮食养生
│       │   │   │       └── Knowledge.vue              # 养生知识
│       │   │   ├── op/                          # 运营页面
│       │   │   │   ├── UserManage.vue           # 运营用户管理
│       │   │   │   └── BuildingManage.vue       # 运营楼栋管理
│       │   │   ├── Login.vue               # 登录页面
│       │   │   ├── Register.vue            # 注册页面
│       │   │   ├── Home.vue               # 首页
│       │   │   ├── Activities.vue          # 社区活动
│       │   │   ├── ActivityDetail.vue      # 活动详情
│       │   │   ├── Services.vue            # 社区服务
│       │   │   └── Government.vue          # 政务服务
│       │   ├── router/               # 路由配置
│       │   ├── api/                  # API接口
│       │   ├── components/           # 公共组件
│       │   ├── stores/               # Pinia状态管理
│       │   └── styles/              # 全局样式
│       ├── package.json
│       └── vite.config.js
├── backend-python/       # Python后端服务
│   └── user-service/     # 用户服务
│       ├── app.py        # 主应用入口
│       ├── config/
│       │   └── database.py    # 数据库配置
│       ├── models/
│       │   ├── user.py        # 用户模型
│       │   ├── building.py    # 楼栋模型
│       │   ├── activity.py    # 活动模型
│       │   ├── access.py      # 门禁模型
│       │   ├── repair.py      # 报修模型
│       │   ├── notice.py      # 公告模型
│       │   ├── utility.py     # 水电模型
│       │   ├── payment.py     # 缴费模型
│       │   ├── parking.py     # 停车模型
│       │   ├── locker.py      # 快递柜模型
│       │   ├── visitor.py     # 访客模型
│       │   ├── complaint.py   # 投诉模型
│       │   ├── merchant.py    # 商家模型
│       │   ├── goods.py       # 商品模型
│       │   ├── comment.py    # 评价模型
│       │   └── order.py      # 订单模型
│       ├── routes/
│       │   ├── auth.py        # 认证路由
│       │   ├── user.py        # 用户管理路由
│       │   ├── building.py    # 楼栋路由
│       │   ├── activity.py    # 活动路由
│       │   ├── access.py      # 门禁路由
│       │   ├── repair.py      # 报修路由
│       │   ├── notice.py      # 公告路由
│       │   ├── utility.py     # 水电路由
│       │   ├── payment.py     # 缴费路由
│       │   ├── parking.py     # 停车路由
│       │   ├── locker.py      # 快递柜路由
│       │   ├── visitor.py     # 访客路由
│       │   ├── complaint.py   # 投诉路由
│       │   ├── merchant.py    # 商家路由
│       │   ├── goods.py       # 商品路由
│       │   ├── comment.py     # 评价路由
│       │   ├── admin.py       # 管理员路由
│       │   ├── ai.py         # AI接口路由
│       │   └── stats.py       # 统计路由
│       ├── utils/
│       │   ├── jwt_util.py    # JWT工具
│       │   ├── file_util.py   # 文件工具
│       │   └── time_util.py   # 时间工具
│       ├── requirements.txt   # Python依赖
│       └── start.bat         # Windows启动脚本
├── ml-training/         # 机器学习训练项目
│   ├── src/
│   │   ├── data/
│   │   │   └── data_preparation.py         # 数据准备脚本
│   │   └── training/
│   │       ├── text_classifier_training.py    # 文字识别模型训练
│   │       └── image_classifier_training.py  # 图片识别模型训练
│   ├── data/
│   │   └── images/
│   │       └── sample_dataset/              # 示例图片数据集
│   ├── models/                             # 训练后的模型
│   │   └── text_classifier/                # 文字识别模型
│   ├── results/                            # 训练结果
│   │   ├── logs/                          # 训练日志
│   │   └── plots/                         # 可视化图表
│   ├── requirements.txt                     # Python依赖
│   └── train_all.py                       # 主训练脚本
├── database/             # 数据库脚本
│   ├── schema.sql        # 完整数据库结构
│   └── init-database.sql # 初始化脚本
├── docs/                 # 项目文档
│   ├── README.md                          # 项目说明
│   ├── api/                               # API文档
│   ├── guides/                            # 使用指南
│   │   ├── 管理员权限说明.md
│   │   ├── 商家审核测试指南.md
│   │   └── 联调验证报告.md
│   ├── backend/                           # 后端文档
│   │   └── 后端服务说明.md
│   └── ml-training/                       # 机器学习文档
│       ├── 毕业设计使用指南.md
│       └── 机器学习项目说明.md
└── docker-compose.yml    # Docker配置
```

## 快速开始

### 1. 环境要求
- Node.js 18+
- Python 3.9+
- MySQL 8.0+

### 2. 数据库配置

#### 创建数据库
```bash
# 登录MySQL
mysql -u root -p

# 执行初始化脚本
source e:/Zh/smart-community/database/init-database.sql
```

#### 数据库连接配置
编辑 `backend-python/user-service/config/database.py`：
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',  # 修改为您的密码
    'database': 'smart_community',
    'port': 3306,
    'charset': 'utf8mb4',
    ...
}
```

### 3. 启动后端服务

#### 方式一：使用启动脚本（推荐）
```bash
cd backend-python/user-service
start.bat
```

#### 方式二：手动启动
```bash
cd backend-python/user-service

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

后端服务启动后访问：http://localhost:8081

### 4. 启动前端

```bash
cd frontend/pc-web
npm install
npm run dev
```

前端访问地址：http://localhost:3000

### 5. 训练机器学习模型

```bash
cd ml-training

# 安装依赖
pip install -r requirements.txt

# 训练所有模型
python train_all.py

# 只训练文字识别模型
python train_all.py --text-only

# 只训练图片识别模型
python train_all.py --image-only
```

## API接口规范

### 接口格式
- **URL格式**: `/api/v1/[平台类型]/[模块]/[功能]`
- **请求方式**: RESTful
- **响应格式**: `{"code": 0, "msg": "success", "data": {}}`

### 平台类型
- `pc`: PC Web端
- `h5`: 移动端H5
- `admin`: 管理端

### 主要API接口

#### 认证接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/pc/auth/register` | POST | 用户注册 |
| `/api/v1/pc/auth/login` | POST | 用户登录 |
| `/api/v1/pc/auth/refresh` | POST | 刷新Token |
| `/api/v1/pc/auth/send-code` | POST | 发送验证码 |

#### 用户接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/pc/user/info` | GET | 获取用户信息 |
| `/api/v1/pc/user/update` | PUT | 更新用户信息 |
| `/api/v1/pc/user/change-password` | PUT | 修改密码 |
| `/api/v1/pc/user/change-phone` | POST | 更换手机号 |

#### 楼栋接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/pc/building/list` | GET | 获取楼栋列表 |
| `/api/v1/pc/building/all` | GET | 获取所有楼栋 |

#### 活动接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/pc/activities` | GET | 获取活动列表 |
| `/api/v1/pc/activities/{id}` | GET | 获取活动详情 |
| `/api/v1/pc/activities` | POST | 报名活动 |
| `/api/v1/admin/activities` | GET | 获取活动列表（管理员） |
| `/api/v1/admin/activities` | POST | 新增活动 |
| `/api/v1/admin/activities/{id}` | PUT | 更新活动 |
| `/api/v1/admin/activities/{id}` | DELETE | 删除活动 |
| `/api/v1/admin/activities/upload-image` | POST | 上传活动图片 |

#### 管理员接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/admin/users` | GET | 获取用户列表 |
| `/api/v1/admin/users` | POST | 新增用户 |
| `/api/v1/admin/users/{id}` | PUT | 更新用户信息 |
| `/api/v1/admin/users/{id}` | DELETE | 删除用户 |
| `/api/v1/admin/merchants` | GET | 获取商家列表 |
| `/api/v1/admin/merchants/{id}/approve` | POST | 审核商家 |
| `/api/v1/admin/goods` | GET | 获取商品列表 |
| `/api/v1/admin/goods/{id}` | DELETE | 删除商品 |
| `/api/v1/admin/comments` | GET | 获取评价列表 |
| `/api/v1/admin/comments/{id}/hide` | POST | 屏蔽评价 |
| `/api/v1/admin/buildings` | GET | 获取楼栋列表 |
| `/api/v1/admin/buildings` | POST | 添加楼栋 |
| `/api/v1/admin/buildings/{id}` | PUT | 更新楼栋 |
| `/api/v1/admin/buildings/{id}` | DELETE | 删除楼栋 |

## 核心模块

### 1. 用户中心模块 ✅
- 用户注册/登录（支持手机号+密码/验证码）
- JWT Token认证（Access Token + Refresh Token）
- 用户信息管理（头像、昵称、联系方式、居住信息）
- 安全设置（修改密码、更换手机号）
- 跨平台登录态同步

### 2. 智慧绿能模块 ✅
- 碳足迹计算器：计算个人和家庭的碳排放量
- 绿色社区论坛：社区环保交流平台
- 环保数据监测：实时环境数据展示
- 节能小贴士：日常节能建议
- 绿色购物指南：环保产品推荐
- 绿色积分系统：环保行为积分奖励

### 3. AI智能建议模块 ✅
- AI绿色生活建议：个性化环保建议
- 绿色出行规划：低碳出行路线推荐
- 家居节能优化：家庭能耗分析

### 4. AI垃圾分类识别模块 ✅
- 文字识别：基于LSTM的文本分类
- 图片识别：基于MobileNetV2的图像分类
- 完整的训练流程和可视化结果

### 5. 智慧社区管理模块 ✅
- 智能门禁：设备管理、权限控制、出入记录、远程开门
- 物业报修：订单管理、维修人员管理、维修统计
- 公告通知：发布社区公告、通知管理、公告详情
- 智能水电：水电表管理、使用统计、异常预警
- 费用缴纳：账单管理、缴费记录、费用统计
- 智能停车：停车位管理、车辆管理、停车记录
- 快递柜：快递柜管理、包裹管理、取件记录
- 访客管理：访客预约、访客登记、访客记录
- 投诉建议：投诉提交、处理流程、统计分析
- 监控管理：监控设备管理、监控记录查询
- 社区活动：活动发布、报名管理、活动统计

### 6. 管理员系统 ✅
- 用户管理：查看和管理用户信息
- 商家管理：审核商家入驻申请
- 商品管理：管理平台商品
- 评价管理：管理用户评价
- 楼栋管理：管理社区楼栋
- 数据统计：平台运营数据

## 配置说明

### JWT配置
在 `backend-python/user-service/utils/jwt_util.py` 中配置：
```python
JWT_SECRET = "smart_community_secret_key_2026"
JWT_EXPIRE_HOURS = 2  # Access Token有效期2小时
JWT_REFRESH_EXPIRE_DAYS = 7  # Refresh Token有效期7天
```

### 前端代理配置
在 `frontend/pc-web/vite.config.js` 中配置：
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8081',
      changeOrigin: true
    }
  }
}
```

## 部署指南

### 生产环境部署

#### 1. 后端部署
```bash
cd backend-python/user-service

# 安装依赖
pip install -r requirements.txt

# 使用Gunicorn启动（生产环境）
gunicorn -w 4 -b 0.0.0.0:8081 app:create_app()
```

#### 2. 前端部署
```bash
cd frontend/pc-web
npm run build

# 将dist目录部署到Nginx
```

#### 3. Nginx配置
```nginx
server {
    listen 80;
    server_name pc.smartcommunity.com;
    
    location / {
        root /var/www/pc-web/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker部署
```bash
docker-compose up -d
```

## 开发规范

### 代码规范
- 前端: ESLint + Prettier
- 后端: PEP 8
- 提交信息: Conventional Commits

### 分支管理
- `main`: 生产分支
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

## 性能指标

- 接口响应时间: ≤500ms
- 页面首屏加载: ≤3秒
- AI识别响应: ≤1秒
- 推荐算法响应: ≤500ms

## 安全规范

- 所有接口使用HTTPS（生产环境）
- JWT Token加密传输
- 敏感数据加密存储（bcrypt）
- 防止SQL注入（参数化查询）
- 防止XSS攻击

## 管理员账号

- **账号**: zh1111
- **密码**: SLG123
- **登录地址**: http://localhost:3000/login

## 更新日志

### v3.0.0 (2026-03-10)
- ✅ 完成智慧社区管理模块开发，包括智能门禁、物业报修、公告通知、智能水电、费用缴纳、智能停车、快递柜、访客管理、投诉建议、监控管理、社区活动等子功能
- ✅ 实现社区活动管理功能，支持活动发布、报名管理、活动统计
- ✅ 新增活动图片上传功能，支持文件上传方式
- ✅ 修复活动时间格式转换问题，支持多种时间格式
- ✅ 优化活动管理页面，确保对话框正常显示
- ✅ 修复API 404和401错误，确保请求包含正确的认证信息
- ✅ 清理项目中的无用文件，保持项目整洁
- ✅ 更新项目文档，添加新功能模块说明

### v2.0.0 (2026-03-08)
- ✅ 完成智慧绿能模块开发，包括碳足迹计算器、绿色社区论坛等子功能
- ✅ 实现AI智能建议功能，包括绿色生活建议、绿色出行规划和家居节能优化
- ✅ 完成AI垃圾分类识别模型训练，包括文字识别和图片识别
- ✅ 实现完整的管理员系统，包括用户、商家、商品、评价和楼栋管理
- ✅ 优化项目结构，整理项目文档
- ✅ 清理无用文件，保持项目整洁

### v1.0.0 (2026-03-07)
- ✅ 重构后端：从Java Spring Boot迁移到Python Flask
- ✅ 完成用户中心模块（注册、登录、用户信息管理）
- ✅ 实现JWT认证机制
- ✅ 完成楼栋管理功能
- ✅ 优化项目结构，删除无用文件

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT](LICENSE)

## 联系方式

- 项目主页: https://github.com/smartcommunity/smart-community
- 问题反馈: https://github.com/smartcommunity/smart-community/issues
- 邮箱: support@smartcommunity.com
