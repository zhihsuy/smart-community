# app.py - Flask应用主入口
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import init_database, logger
from init_smart_community_tables import init_all_tables
from routes.auth import auth_bp
from routes.user import user_bp
from routes.building import building_bp
from routes.admin import admin_bp
from routes.access_control import access_bp
from routes.repair import repair_bp
from routes.notice import notice_bp
from routes.utility import utility_bp
from routes.payment import payment_bp
from routes.parking import parking_bp
from routes.locker import locker_bp
from routes.visitor import visitor_bp
from routes.complaint import complaint_bp
from routes.monitoring import monitoring_bp
from routes.activity import activity_bp
from routes.stats import stats_bp

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 启用CORS，允许前端跨域访问
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:3002", "http://127.0.0.1:3002"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 配置静态文件目录
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    app.static_folder = static_dir
    app.static_url_path = '/static'
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(building_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(access_bp)
    app.register_blueprint(repair_bp)
    app.register_blueprint(notice_bp)
    app.register_blueprint(utility_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(locker_bp)
    app.register_blueprint(visitor_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(stats_bp)
    
    # 添加全局请求日志
    @app.before_request
    def log_request_info():
        logger.info(f"=== 收到请求 ===")
        logger.info(f"请求方法: {request.method}")
        logger.info(f"请求路径: {request.path}")
        logger.info(f"请求头: {dict(request.headers)}")
        if request.method in ['POST', 'PUT']:
            logger.info(f"请求体: {request.get_json(silent=True) or request.form.to_dict()}")
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'code': 404,
            'msg': '接口不存在',
            'data': None
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'code': 500,
            'msg': '服务器内部错误',
            'data': None
        }), 500
    
    # 健康检查接口
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'code': 0,
            'msg': '服务运行正常',
            'data': {
                'service': 'user-service',
                'status': 'running'
            }
        })
    
    return app


def init_app():
    """初始化应用（数据库等）"""
    try:
        logger.info("正在初始化数据库...")
        init_database()
        logger.info("正在创建所有表...")
        init_all_tables()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        logger.info("请确保MySQL服务已启动，并且用户名密码正确")


if __name__ == '__main__':
    # 初始化数据库
    init_app()
    
    # 创建应用
    app = create_app()
    
    # 启动服务
    logger.info("正在启动用户服务...")
    logger.info("服务地址: http://localhost:8081")
    logger.info("API文档:")
    logger.info("  - 健康检查: GET http://localhost:8081/health")
    logger.info("  - 用户注册: POST http://localhost:8081/api/v1/pc/auth/register")
    logger.info("  - 用户登录: POST http://localhost:8081/api/v1/pc/auth/login")
    logger.info("  - 获取用户信息: GET http://localhost:8081/api/v1/pc/user/info")
    logger.info("  - 更新用户信息: PUT http://localhost:8081/api/v1/pc/user/update")
    logger.info("  - 获取楼栋列表: GET http://localhost:8081/api/v1/pc/building/list")
    # 商品相关接口
    logger.info("  - 商品列表: GET http://localhost:8081/api/v1/pc/goods/list")
    logger.info("  - 商品详情: GET http://localhost:8081/api/v1/pc/goods/{id}")
    logger.info("  - 商品分类: GET http://localhost:8081/api/v1/pc/goods/categories")
    # 订单相关接口
    logger.info("  - 创建订单: POST http://localhost:8081/api/v1/pc/order/create")
    logger.info("  - 订单列表: GET http://localhost:8081/api/v1/pc/order/list")
    logger.info("  - 订单详情: GET http://localhost:8081/api/v1/pc/order/{id}")
    logger.info("  - 取消订单: POST http://localhost:8081/api/v1/pc/order/{id}/cancel")
    logger.info("  - 支付订单: POST http://localhost:8081/api/v1/pc/order/{id}/pay")
    # AI服务接口
    logger.info("  - 库存预测: POST http://localhost:8081/api/v1/pc/ai/stock/predict")
    logger.info("  - 价格分析: POST http://localhost:8081/api/v1/pc/ai/price/analysis")
    logger.info("  - 内容检测: POST http://localhost:8081/api/v1/pc/ai/content/check")
    logger.info("  - 商品推荐: GET http://localhost:8081/api/v1/pc/ai/recommend/goods")
    
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=True
    )
