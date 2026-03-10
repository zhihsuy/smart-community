"""
YOLOv8垃圾分类模型训练脚本
"""

from ultralytics import YOLO
import os

# 配置路径
YAML_PATH = r"e:\Zh\smart-community\ml-training\data\garbage_dataset\garbage_dataset.yaml"
MODEL_PATH = r"e:\Zh\smart-community\ml-training\yolov8n.pt"

# 训练参数
EPOCHS = 100
BATCH_SIZE = 8  # CPU训练建议用小批量
IMGSZ = 640

print("=" * 60)
print("🚀 YOLOv8垃圾分类模型训练")
print("=" * 60)

# 加载模型
if os.path.exists(MODEL_PATH):
    print(f"✅ 加载本地模型: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
else:
    print("⚠️ 未找到本地模型，将自动下载YOLOv8n...")
    model = YOLO('yolov8n.pt')

print("\n🚀 开始训练...")
print(f"📊 训练轮数: {EPOCHS}")
print(f"🔄 批量大小: {BATCH_SIZE}")
print(f"🖼️ 图片尺寸: {IMGSZ}")
print(f"💻 使用设备: CPU")
print("=" * 60)

# 启动训练
results = model.train(
    data=YAML_PATH,
    epochs=EPOCHS,
    batch=BATCH_SIZE,
    imgsz=IMGSZ,
    device='cpu',  # 使用CPU训练
    project="garbage_detection",
    name="yolov8_garbage",
    pretrained=True,
    patience=20,
    save=True,
    val=True,
    workers=0,  # Windows下设为0避免多进程问题
    optimizer='SGD',
    lr0=0.01,
    lrf=0.01,
    warmup_epochs=3
)

print("\n" + "=" * 60)
print("🎉 训练完成！")
print("=" * 60)
print(f"📁 模型保存路径: garbage_detection/yolov8_garbage/weights/")
print(f"🎯 最优模型: garbage_detection/yolov8_garbage/weights/best.pt")
print(f"📝 最后模型: garbage_detection/yolov8_garbage/weights/last.pt")
print("=" * 60)
