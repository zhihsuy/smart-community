# routes/ai.py - AI服务集成路由
from flask import Blueprint, request, jsonify
from config.database import logger
import random
from datetime import datetime, timedelta

# 创建蓝图
ai_bp = Blueprint('ai', __name__, url_prefix='/api/v1/<platform_type>/ai')

# ==================== AI服务接口 ====================

# 库存预测
@ai_bp.route('/stock/predict', methods=['POST'])
def predict_stock(platform_type):
    """AI库存预测接口"""
    try:
        data = request.get_json()
        goods_id = data.get('goodsId')
        days = data.get('days', 7)
        
        if not goods_id:
            return jsonify({
                'code': 400,
                'msg': '商品ID不能为空',
                'data': None
            })
        
        # 模拟AI预测结果
        # 基于历史销量 + 节假日 + 天气
        predictions = []
        base_stock = random.randint(50, 200)
        
        for i in range(days):
            # 生成未来日期
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            
            # 模拟销量波动
            fluctuation = random.uniform(0.7, 1.3)
            predicted_stock = int(base_stock * fluctuation)
            
            # 标记库存低于阈值的情况
            is_low = predicted_stock < 50
            
            predictions.append({
                'date': date,
                'predictedStock': predicted_stock,
                'isLow': is_low
            })
        
        return jsonify({
            'code': 0,
            'msg': '预测成功',
            'data': {
                'goodsId': goods_id,
                'predictions': predictions,
                'threshold': 50
            }
        })
    
    except Exception as e:
        logger.error(f"库存预测失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'预测失败: {str(e)}',
            'data': None
        })

# 价格分析
@ai_bp.route('/price/analysis', methods=['POST'])
def analyze_price(platform_type):
    """AI价格分析接口"""
    try:
        data = request.get_json()
        goods_id = data.get('goodsId')
        
        if not goods_id:
            return jsonify({
                'code': 400,
                'msg': '商品ID不能为空',
                'data': None
            })
        
        # 模拟AI价格分析结果
        current_price = random.uniform(10, 100)
        historical_low = current_price * random.uniform(0.7, 0.95)
        
        # 周边社区价格对比
        community_prices = []
        for i in range(5):
            community_prices.append({
                'communityName': f'社区{i+1}',
                'price': current_price * random.uniform(0.8, 1.2)
            })
        
        # 计算当前价格相对于其他社区的水平
        lower_than_percent = random.randint(60, 95)
        
        return jsonify({
            'code': 0,
            'msg': '分析成功',
            'data': {
                'goodsId': goods_id,
                'currentPrice': round(current_price, 2),
                'historicalLow': round(historical_low, 2),
                'communityPrices': community_prices,
                'lowerThanPercent': lower_than_percent,
                'suggestion': f'当前价格低于{lower_than_percent}%的同类团购'
            }
        })
    
    except Exception as e:
        logger.error(f"价格分析失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'分析失败: {str(e)}',
            'data': None
        })

# 违规检测
@ai_bp.route('/content/check', methods=['POST'])
def check_content(platform_type):
    """AI内容违规检测接口"""
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({
                'code': 400,
                'msg': '内容不能为空',
                'data': None
            })
        
        # 模拟AI违规检测结果
        # 简单的关键词检测
        sensitive_words = ['垃圾', '骗子', '假货', '退款', '投诉']
        is_violation = any(word in content for word in sensitive_words)
        
        violation_type = None
        if is_violation:
            # 随机生成违规类型
            violation_types = ['spam', 'abuse', 'false_info']
            violation_type = random.choice(violation_types)
        
        return jsonify({
            'code': 0,
            'msg': '检测成功',
            'data': {
                'isViolation': is_violation,
                'violationType': violation_type,
                'confidence': round(random.uniform(0.7, 0.99), 2),
                'suggestion': '内容违规，建议屏蔽' if is_violation else '内容正常'
            }
        })
    
    except Exception as e:
        logger.error(f"内容检测失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'检测失败: {str(e)}',
            'data': None
        })

# 商品推荐
@ai_bp.route('/recommend/goods', methods=['GET'])
def recommend_goods(platform_type):
    """商品推荐接口"""
    try:
        user_id = request.args.get('userId', type=int)
        
        # 模拟推荐结果
        # 基于用户行为 + 地理位置
        recommended_goods = []
        
        for i in range(10):
            recommended_goods.append({
                'id': i + 1,
                'name': f'推荐商品{i+1}',
                'mainImage': f'https://example.com/goods{i+1}.jpg',
                'salePrice': round(random.uniform(10, 100), 2),
                'soldCount': random.randint(0, 1000),
                'isGroupBuy': random.choice([0, 1]),
                'groupBuyPrice': round(random.uniform(5, 80), 2) if random.choice([0, 1]) else None,
                'relevanceScore': round(random.uniform(0.7, 1.0), 2)
            })
        
        return jsonify({
            'code': 0,
            'msg': '推荐成功',
            'data': {
                'userId': user_id,
                'platformType': platform_type,
                'recommendedGoods': recommended_goods
            }
        })
    
    except Exception as e:
        logger.error(f"商品推荐失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'推荐失败: {str(e)}',
            'data': None
        })

@ai_bp.route('/recommend', methods=['POST'])
def recommend(platform_type):
    """综合推荐接口"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        scene = data.get('scene', 'home')
        limit = data.get('limit', 8)
        
        recommendations = []
        
        for i in range(limit):
            recommendations.append({
                'item_id': i + 1,
                'item_type': random.choice(['goods', 'activity']),
                'name': f'推荐项目{i+1}',
                'price': round(random.uniform(10, 200), 2),
                'tags': random.sample(['新鲜', '健康', '运动', '亲子', '教育', '有机'], 2),
                'reason': random.choice(['基于您的兴趣推荐', '热门商品', '新用户专享', '限时优惠']),
                'image': f'/images/recommend{i+1}.jpg'
            })
        
        return jsonify({
            'code': 0,
            'msg': '推荐成功',
            'data': {
                'user_id': user_id,
                'scene': scene,
                'recommendations': recommendations
            }
        })
    
    except Exception as e:
        logger.error(f"综合推荐失败: {e}")
        return jsonify({
            'code': 500,
            'msg': f'推荐失败: {str(e)}',
            'data': None
        })