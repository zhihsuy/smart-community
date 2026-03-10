"""
按照标准YOLOv8目录结构准备数据集
将train_data中的数据划分为训练集和验证集
"""

import os
import shutil
import random
from pathlib import Path

# 配置路径
SOURCE_DIR = r"e:\Zh\smart-community\ml-training\data\train_data"
OUTPUT_DIR = r"e:\Zh\smart-community\ml-training\data\garbage_dataset"

# 创建标准YOLOv8目录结构
def create_directory_structure():
    """创建YOLOv8标准目录结构"""
    dirs = [
        os.path.join(OUTPUT_DIR, 'train', 'images'),
        os.path.join(OUTPUT_DIR, 'train', 'labels'),
        os.path.join(OUTPUT_DIR, 'val', 'images'),
        os.path.join(OUTPUT_DIR, 'val', 'labels')
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ 创建目录: {dir_path}")

# 划分数据集
def split_dataset(train_ratio=0.8):
    """
    将数据集划分为训练集和验证集
    """
    print("\n🔄 开始划分数据集...")
    
    # 获取所有标签文件
    txt_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.txt')]
    print(f"📊 找到 {len(txt_files)} 个标签文件")
    
    # 随机打乱
    random.shuffle(txt_files)
    
    # 计算划分点
    split_idx = int(len(txt_files) * train_ratio)
    train_files = txt_files[:split_idx]
    val_files = txt_files[split_idx:]
    
    print(f"🎯 训练集: {len(train_files)} 个文件 ({train_ratio*100}%)")
    print(f"🎯 验证集: {len(val_files)} 个文件 ({(1-train_ratio)*100}%)")
    
    return train_files, val_files

# 复制文件到目标目录
def copy_files(file_list, split_name):
    """
    复制文件到训练集或验证集目录
    """
    print(f"\n🔄 复制{split_name}集文件...")
    
    img_dir = os.path.join(OUTPUT_DIR, split_name, 'images')
    label_dir = os.path.join(OUTPUT_DIR, split_name, 'labels')
    
    copied_count = 0
    for txt_file in file_list:
        txt_path = os.path.join(SOURCE_DIR, txt_file)
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
            
            if line:
                parts = line.split(', ')
                if len(parts) == 2:
                    img_name, class_id = parts
                    class_id = int(class_id)
                    
                    # 检查图片是否存在
                    img_path = os.path.join(SOURCE_DIR, img_name)
                    if os.path.exists(img_path):
                        # 生成新的文件名（使用序号命名，避免冲突）
                        new_name = f"{split_name}_{copied_count+1:06d}"
                        new_img_name = f"{new_name}.jpg"
                        new_txt_name = f"{new_name}.txt"
                        
                        # 复制图片
                        dest_img = os.path.join(img_dir, new_img_name)
                        shutil.copy2(img_path, dest_img)
                        
                        # 创建YOLO格式标签文件
                        # YOLO格式: class_id center_x center_y width height（归一化）
                        dest_txt = os.path.join(label_dir, new_txt_name)
                        with open(dest_txt, 'w') as f:
                            # 假设目标在图片中心，占据80%区域
                            f.write(f"{class_id} 0.5 0.5 0.8 0.8\n")
                        
                        copied_count += 1
                        
                        # 显示进度
                        if copied_count % 500 == 0:
                            print(f"🔄 {split_name}集进度: {copied_count}/{len(file_list)}")
        except Exception as e:
            print(f"❌ 处理 {txt_file} 时出错: {e}")
            continue
    
    print(f"✅ {split_name}集复制完成，共 {copied_count} 个文件")
    return copied_count

# 创建yaml配置文件
def create_yaml_config():
    """
    创建YOLOv8的yaml配置文件
    """
    print("\n📝 创建yaml配置文件...")
    
    yaml_path = os.path.join(OUTPUT_DIR, 'garbage_dataset.yaml')
    
    train_path = os.path.join(OUTPUT_DIR, 'train', 'images').replace('\\', '/')
    val_path = os.path.join(OUTPUT_DIR, 'val', 'images').replace('\\', '/')
    yaml_content = f"""# YOLOv8垃圾分类数据集配置
train: {train_path}
val: {val_path}

# 类别数量
nc: 4

# 类别名称
names:
  0: 可回收物
  1: 有害垃圾
  2: 厨余垃圾
  3: 其他垃圾
"""
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"✅ yaml配置文件创建完成: {yaml_path}")
    return yaml_path

# 主函数
def main():
    print("=" * 60)
    print("🚀 准备YOLOv8标准数据集")
    print("=" * 60)
    
    # 1. 创建目录结构
    create_directory_structure()
    
    # 2. 划分数据集
    train_files, val_files = split_dataset(train_ratio=0.8)
    
    # 3. 复制训练集文件
    train_count = copy_files(train_files, 'train')
    
    # 4. 复制验证集文件
    val_count = copy_files(val_files, 'val')
    
    # 5. 创建yaml配置文件
    yaml_path = create_yaml_config()
    
    print("\n" + "=" * 60)
    print("✅ 数据集准备完成！")
    print("=" * 60)
    print(f"📁 数据集目录: {OUTPUT_DIR}")
    print(f"📊 训练集: {train_count} 个样本")
    print(f"📊 验证集: {val_count} 个样本")
    print(f"📝 配置文件: {yaml_path}")
    print("\n💡 下一步: 运行训练脚本开始训练模型")
    print("=" * 60)

if __name__ == "__main__":
    main()
