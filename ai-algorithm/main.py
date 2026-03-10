from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import tensorflow as tf
import json
import time

app = FastAPI(
    title="Smart Community AI Service",
    description="AI services for smart community platform",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 垃圾分类模型
class GarbageClassifier:
    def __init__(self):
        # 模拟模型加载
        self.class_names = ['可回收物', '有害垃圾', '厨余垃圾', '其他垃圾']
        self.model_loaded = True
    
    def predict(self, image):
        # 模拟预测
        import random
        prediction = random.choice(self.class_names)
        confidence = round(random.uniform(0.8, 0.95), 4)
        return {
            "category": prediction,
            "confidence": confidence,
            "disposal_method": self.get_disposal_method(prediction),
            "recommended_activities": self.get_recommended_activities(prediction)
        }
    
    def get_disposal_method(self, category):
        methods = {
            '可回收物': '清洁干燥后投放至可回收物收集容器',
            '有害垃圾': '投放至有害垃圾收集容器',
            '厨余垃圾': '沥干水分后投放至厨余垃圾收集容器',
            '其他垃圾': '投放至其他垃圾收集容器'
        }
        return methods.get(category, '按照当地垃圾分类标准投放')
    
    def get_recommended_activities(self, category):
        activities = {
            '可回收物': ['社区回收日活动', '旧物改造手工课'],
            '有害垃圾': ['有害垃圾知识讲座', '电池回收活动'],
            '厨余垃圾': ['厨余堆肥体验', '环保厨艺大赛'],
            '其他垃圾': ['垃圾分类知识竞赛', '环保志愿者活动']
        }
        return activities.get(category, [])

# 推荐算法
class RecommendationEngine:
    def __init__(self):
        # 模拟推荐数据
        self.goods = [
            {"id": 1, "name": "新鲜水果套餐", "price": 99, "type": "food", "tags": ["新鲜", "健康"]},
            {"id": 2, "name": "社区健身卡", "price": 199, "type": "service", "tags": ["运动", "健康"]},
            {"id": 3, "name": "亲子活动门票", "price": 120, "type": "activity", "tags": ["亲子", "教育"]},
            {"id": 4, "name": "有机蔬菜包", "price": 68, "type": "food", "tags": ["有机", "健康"]},
            {"id": 5, "name": "家政服务套餐", "price": 299, "type": "service", "tags": ["家政", "便利"]}
        ]
    
    def recommend(self, user_id, platform_type, scene, limit=10):
        # 模拟推荐逻辑
        recommendations = []
        for item in self.goods:
            score = np.random.uniform(0.7, 0.99)
            recommendations.append({
                "item_id": item["id"],
                "item_type": "goods",
                "name": item["name"],
                "price": item["price"],
                "tags": item["tags"],
                "score": round(score, 6),
                "reason": f"基于您的兴趣标签推荐"
            })
        
        # 按分数排序
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]

# 智能客服
class AICustomerService:
    def __init__(self):
        # 简单的问答库
        self.qa_pairs = {
            "如何注册": "请点击首页的注册按钮，输入手机号和验证码即可注册",
            "如何下单": "在商品详情页点击立即购买，按照提示完成支付即可",
            "如何参加活动": "在活动页面选择感兴趣的活动，点击报名按钮即可",
            "客服电话": "客服热线：400-123-4567，工作时间：9:00-18:00",
            "垃圾分类": "您可以使用首页的AI垃圾分类功能进行识别"
        }
    
    def get_answer(self, question):
        # 简单的匹配逻辑
        question = question.lower()
        for key, answer in self.qa_pairs.items():
            if key in question:
                return answer
        return "抱歉，我暂时无法回答这个问题，请尝试其他问题或联系人工客服"

# 初始化服务
classifier = GarbageClassifier()
recommender = RecommendationEngine()
customer_service = AICustomerService()

# API端点
@app.post("/api/ai/garbage/classify")
async def classify_garbage(file: UploadFile = File(...)):
    start_time = time.time()
    
    try:
        # 读取图片
        image = Image.open(file.file)
        
        # 模型预测
        result = classifier.predict(image)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "result": result,
                "processing_time_ms": processing_time,
                "model_version": "v1.0"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/recommend")
async def get_recommendations(user_id: int, platform_type: str, scene: str = "home", limit: int = 10):
    try:
        recommendations = recommender.recommend(user_id, platform_type, scene, limit)
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "recommendations": recommendations,
                "algorithm": "collaborative+content",
                "scene": scene
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/customer-service")
async def get_customer_service_answer(question: str):
    try:
        answer = customer_service.get_answer(question)
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "answer": answer,
                "confidence": 0.9,
                "is_manual_transfer": False
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["garbage_classification", "recommendation", "customer_service"]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)