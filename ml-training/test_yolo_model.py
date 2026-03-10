from ultralytics import YOLO
import os

# 模型路径
model_path = r'e:\Zh\smart-community\ml-training\data\images\exp-WasteSorting4-300epoch\exp-WasteSorting4-500epoch\weights\best.pt'

# 测试图片路径
test_image_path = r'e:\Zh\smart-community\ml-training\data\images\exp-WasteSorting4-300epoch\exp-WasteSorting4-500epoch\val_batch0_pred.jpg'

print('正在加载YOLOv8模型...')

try:
    # 加载模型
    model = YOLO(model_path)
    print('✅ 模型加载成功！')
    print(f'模型信息: {model.info()}')
    
    # 进行预测
    print(f'\n正在测试预测: {test_image_path}')
    if os.path.exists(test_image_path):
        results = model(test_image_path)
        print('✅ 预测成功！')
        
        # 显示结果
        for i, result in enumerate(results):
            print(f'\n结果 {i+1}:')
            print(f'  检测到 {len(result.boxes)} 个物体')
            for j, box in enumerate(result.boxes):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]
                print(f'  物体 {j+1}: {class_name} (置信度: {confidence:.2f})')
        
        # 保存结果
        output_path = r'e:\Zh\smart-community\ml-training\test_result.jpg'
        results[0].save(output_path)
        print(f'\n✅ 结果已保存到: {output_path}')
    else:
        print(f'❌ 测试图片不存在: {test_image_path}')
        
except Exception as e:
    print(f'❌ 错误: {str(e)}')
    import traceback
    traceback.print_exc()
