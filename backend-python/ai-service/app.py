from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
import os
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np

# 导入详细物品分类器
from waste_classifier import waste_classifier

app = Flask(__name__)
CORS(app)

# 加载YOLOv8模型
model_path = r'e:\Zh\smart-community\ml-training\data\images\exp-WasteSorting4-300epoch\exp-WasteSorting4-500epoch\weights\best.pt'
model = YOLO(model_path)

# 垃圾类别映射
class_names = {
    0: '可回收物',
    1: '有害垃圾',
    2: '厨余垃圾',
    3: '其他垃圾'
}

# 类别颜色映射
class_colors = {
    0: (0, 255, 0),    # 可回收物 - 绿色
    1: (255, 0, 0),    # 有害垃圾 - 红色
    2: (255, 255, 0),  # 厨余垃圾 - 黄色
    3: (128, 128, 128) # 其他垃圾 - 灰色
}

@app.route('/api/v1/ai/garbage-classify', methods=['POST'])
def classify_garbage():
    """
    垃圾分类识别API接口
    支持图片文件上传和Base64编码图片
    返回详细的垃圾分类信息，包括具体物品名称
    """
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({
                'code': 400,
                'msg': '未找到图片文件',
                'data': None
            }), 400
        
        file = request.files['image']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({
                'code': 400,
                'msg': '未选择文件',
                'data': None
            }), 400
        
        # 读取图片
        image = Image.open(file.stream)
        
        # 保存临时图片用于预测
        temp_path = r'e:\Zh\smart-community\ml-training\temp_image.jpg'
        image.save(temp_path)
        
        # 使用YOLOv8模型进行预测
        results = model(temp_path)
        
        # 处理预测结果
        detections = []
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = class_names.get(class_id, '未知')
                
                # 只保留置信度大于0.3的检测结果
                if confidence > 0.3:
                    # 绘制 bounding box
                    bbox = box.xyxy.tolist()[0]
                    x1, y1, x2, y2 = map(int, bbox)
                    color = class_colors.get(class_id, (255, 255, 255))
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
                    
                    detections.append({
                        'class_id': class_id,
                        'class_name': class_name,
                        'confidence': round(confidence, 4),
                        'bbox': bbox  # [x1, y1, x2, y2]
                    })
        
        # 保存标注后的图片
        annotated_path = r'e:\Zh\smart-community\ml-training\annotated_image.jpg'
        annotated_image.save(annotated_path)
        
        # 如果没有检测到物体，返回默认分类
        if not detections:
            # 删除临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(annotated_path):
                os.remove(annotated_path)
                
            return jsonify({
                'code': 200,
                'msg': '未检测到垃圾物体',
                'data': {
                    'detected': False,
                    'class_name': '其他垃圾',
                    'item_name': '未知物品',
                    'confidence': 0.0
                }
            }), 200
        
        # 找到置信度最高的检测结果
        best_detection = max(detections, key=lambda x: x['confidence'])
        
        # 使用详细物品分类器识别具体物品
        detailed_result = waste_classifier.classify_item(
            temp_path, 
            best_detection['class_name']
        )
        
        # 将标注后的图片转换为Base64
        buffered = io.BytesIO()
        annotated_image.save(buffered, format="JPEG")
        annotated_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # 删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(annotated_path):
            os.remove(annotated_path)
        
        return jsonify({
            'code': 0,
            'msg': '识别成功',
            'data': {
                'detected': True,
                'class_id': best_detection['class_id'],
                'class_name': best_detection['class_name'],
                'item_name': detailed_result['item_name'],
                'confidence': best_detection['confidence'],
                'item_confidence': detailed_result['confidence'],
                'disposal_tips': detailed_result['disposal_tips'],
                'recycling_value': detailed_result['recycling_value'],
                'all_detections': detections,
                'annotated_image': f"data:image/jpeg;base64,{annotated_base64}",
                'model_info': {
                    'model_type': 'YOLOv8 + 分类器',
                    'model_size': 'nano',
                    'inference_time': '~200ms',
                    'capabilities': ['垃圾分类', '物品识别', '处理建议', '图片标注']
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'识别失败: {str(e)}',
            'data': None
        }), 500

@app.route('/api/v1/ai/garbage-classify-base64', methods=['POST'])
def classify_garbage_base64():
    """
    垃圾分类识别API接口（Base64编码）
    返回详细的垃圾分类信息，包括具体物品名称
    """
    try:
        # 获取Base64编码的图片
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'code': 400,
                'msg': '未找到图片数据',
                'data': None
            }), 400
        
        # 解码Base64图片
        image_data = data['image']
        
        # 移除数据URL前缀（如果有）
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # 解码
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # 保存临时图片
        temp_path = r'e:\Zh\smart-community\ml-training\temp_image.jpg'
        image.save(temp_path)
        
        # 使用YOLOv8模型进行预测
        results = model(temp_path)
        
        # 处理预测结果
        detections = []
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = class_names.get(class_id, '未知')
                
                if confidence > 0.3:
                    # 绘制 bounding box
                    bbox = box.xyxy.tolist()[0]
                    x1, y1, x2, y2 = map(int, bbox)
                    color = class_colors.get(class_id, (255, 255, 255))
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
                    
                    detections.append({
                        'class_id': class_id,
                        'class_name': class_name,
                        'confidence': round(confidence, 4),
                        'bbox': bbox
                    })
        
        # 保存标注后的图片
        annotated_path = r'e:\Zh\smart-community\ml-training\annotated_image.jpg'
        annotated_image.save(annotated_path)
        
        if not detections:
            # 删除临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(annotated_path):
                os.remove(annotated_path)
                
            return jsonify({
                'code': 200,
                'msg': '未检测到垃圾物体',
                'data': {
                    'detected': False,
                    'class_name': '其他垃圾',
                    'item_name': '未知物品',
                    'confidence': 0.0
                }
            }), 200
        
        best_detection = max(detections, key=lambda x: x['confidence'])
        
        # 使用详细物品分类器识别具体物品
        detailed_result = waste_classifier.classify_item(
            temp_path, 
            best_detection['class_name']
        )
        
        # 将标注后的图片转换为Base64
        buffered = io.BytesIO()
        annotated_image.save(buffered, format="JPEG")
        annotated_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # 删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(annotated_path):
            os.remove(annotated_path)
        
        return jsonify({
            'code': 0,
            'msg': '识别成功',
            'data': {
                'detected': True,
                'class_id': best_detection['class_id'],
                'class_name': best_detection['class_name'],
                'item_name': detailed_result['item_name'],
                'confidence': best_detection['confidence'],
                'item_confidence': detailed_result['confidence'],
                'disposal_tips': detailed_result['disposal_tips'],
                'recycling_value': detailed_result['recycling_value'],
                'all_detections': detections,
                'annotated_image': f"data:image/jpeg;base64,{annotated_base64}"
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'识别失败: {str(e)}',
            'data': None
        }), 500

@app.route('/api/v1/ai/model-info', methods=['GET'])
def get_model_info():
    """
    获取模型信息
    """
    try:
        return jsonify({
            'code': 0,
            'msg': '获取成功',
            'data': {
                'model_type': 'YOLOv8',
                'model_version': '8.4.21',
                'model_path': model_path,
                'model_info': 'YOLOv8 nano model for waste classification',
                'classes': class_names,
                'supported_formats': ['jpg', 'jpeg', 'png', 'bmp'],
                'max_image_size': '640x640',
                'inference_time': '~200ms',
                'accuracy': {
                    'mAP50': 0.83,
                    'precision': 0.53,
                    'recall': 0.81
                },
                'capabilities': [
                    '四大类垃圾分类识别',
                    '图片标注',
                    '个性化处理建议',
                    '回收价值评估'
                ]
            }
        }), 200
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}',
            'data': None
        }), 500

if __name__ == '__main__':
    print('🚀 垃圾分类AI服务启动中...')
    print(f'📦 模型路径: {model_path}')
    print(f'🎯 API地址: http://localhost:8082')
    print('✅ 服务已启动，按Ctrl+C停止')
    
    app.run(host='0.0.0.0', port=8082, debug=True)
