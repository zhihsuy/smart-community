"""
垃圾分类识别器
只做四大类垃圾分类，不进行具体物品识别
"""

class WasteClassifier:
    def __init__(self):
        # 四大类垃圾
        self.categories = {
            '可回收物': '适宜回收利用和资源化利用的生活废弃物',
            '有害垃圾': '对人体健康或自然环境造成直接或潜在危害的废弃物',
            '厨余垃圾': '易腐烂的、含有机质的生活废弃物',
            '其他垃圾': '除可回收物、有害垃圾、厨余垃圾以外的其他生活废弃物'
        }
        
        print("✅ 垃圾分类器初始化成功")
    
    def classify_item(self, image_path, detected_class):
        """
        识别垃圾类别（简化版本）
        
        Args:
            image_path: 图片路径
            detected_class: YOLO检测到的类别（可回收物/有害垃圾/厨余垃圾/其他垃圾）
        
        Returns:
            dict: 包含分类信息、处理建议和回收价值
        """
        try:
            # 直接返回分类结果
            return {
                'item_name': detected_class,
                'category': detected_class,
                'confidence': 0.90,
                'disposal_tips': self._get_disposal_tips(detected_class),
                'recycling_value': self._get_recycling_value(detected_class),
                'note': 'AI识别仅供参考，请根据实际情况确认'
            }
            
        except Exception as e:
            print(f"识别错误: {e}")
            return {
                'item_name': '未知垃圾',
                'category': '其他垃圾',
                'confidence': 0.0,
                'disposal_tips': '请按照当地垃圾分类标准进行处理',
                'recycling_value': '无法评估',
                'note': 'AI识别仅供参考，请根据实际情况确认'
            }
    
    def _get_disposal_tips(self, category):
        """获取处理建议"""
        tips = {
            '可回收物': '请保持清洁干燥，避免污染。纸类应折叠整齐，瓶罐类应清空内容物并压扁。',
            '有害垃圾': '请轻投轻放，避免破损。电池应保持完整，灯管应防止破损。',
            '厨余垃圾': '请沥干水分，去除包装物。避免混入塑料袋等非厨余垃圾。',
            '其他垃圾': '请沥干水分，难以辨识类别的生活垃圾请投入其他垃圾收集容器。'
        }
        return tips.get(category, '请按照当地垃圾分类标准进行处理')
    
    def _get_recycling_value(self, category):
        """获取回收价值信息"""
        value_info = {
            '可回收物': '高回收价值，可循环利用',
            '有害垃圾': '需要专业处理，含有有害物质',
            '厨余垃圾': '可制作有机肥料或沼气',
            '其他垃圾': '低回收价值，主要进行无害化处理'
        }
        return value_info.get(category, '请咨询当地回收站')

# 创建全局分类器实例
waste_classifier = WasteClassifier()
