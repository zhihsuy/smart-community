<template>
  <div class="garbage-classification">
    <div class="page-header">
      <h1>♻️ AI绿色垃圾分类</h1>
      <p>使用AI技术轻松识别和分类垃圾，让环保更简单</p>
    </div>

    <div class="classification-container">
      <div class="upload-section">
        <div class="upload-box" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
          <input 
            type="file" 
            ref="fileInput" 
            @change="handleFileChange" 
            accept="image/*"
            style="display: none"
          >
          
          <div v-if="!previewImage" class="upload-placeholder">
            <div class="upload-icon">📷</div>
            <h3>点击或拖拽上传图片</h3>
            <p>支持 JPG、PNG、BMP 格式</p>
          </div>
          
          <div v-else class="image-preview">
            <img :src="previewImage" alt="预览图片" />
            <button class="remove-btn" @click.stop="removeImage">✕</button>
          </div>
        </div>

        <div class="upload-actions">
          <button 
            class="btn btn-primary" 
            @click="classifyImage"
            :disabled="!selectedFile || isClassifying"
          >
            <span v-if="!isClassifying">🔍 开始识别</span>
            <span v-else>⏳ 识别中...</span>
          </button>
          
          <button 
            class="btn btn-secondary" 
            @click="clearResult"
            :disabled="!result"
          >
            🗑️ 清除结果
          </button>
        </div>
      </div>

      <div class="result-section">
        <div v-if="!result" class="result-placeholder">
          <div class="placeholder-icon">🤖</div>
          <h3>等待识别</h3>
          <p>上传图片后点击"开始识别"按钮</p>
        </div>

        <div v-else class="result-content">
          <div class="result-header">
            <h3>识别结果</h3>
            <span class="confidence-badge">置信度: {{ (result.confidence * 100).toFixed(2) }}%</span>
          </div>

          <div class="result-card" :class="result.class_name">
            <div class="result-icon">{{ getClassIcon(result.class_name) }}</div>
            <div class="result-info">
              <div class="item-name">{{ result.item_name || '未知物品' }}</div>
              <h2>{{ result.class_name }}</h2>
              <p>{{ getClassDescription(result.class_name) }}</p>
            </div>
          </div>

          <div v-if="result.all_detections && result.all_detections.length > 1" class="all-detections">
            <h4>所有检测结果</h4>
            <div class="detection-list">
              <div 
                v-for="(detection, index) in result.all_detections" 
                :key="index"
                class="detection-item"
                :class="{ active: detection.class_id === result.class_id }"
              >
                <span class="detection-class">{{ detection.class_name }}</span>
                <span class="detection-confidence">{{ (detection.confidence * 100).toFixed(2) }}%</span>
              </div>
            </div>
          </div>

          <div v-if="result.disposal_tips" class="result-tips specific-tips">
            <h4>💡 {{ result.item_name }}处理建议</h4>
            <p>{{ result.disposal_tips }}</p>
          </div>

          <div v-if="result.recycling_value" class="result-tips recycling-value">
            <h4>♻️ 回收价值</h4>
            <p>{{ result.recycling_value }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h3>🎯 垃圾分类指南</h3>
      <div class="guide-grid">
        <div class="guide-card recyclable">
          <div class="guide-icon">♻️</div>
          <div class="guide-title">可回收物</div>
          <div class="guide-examples">
            <span class="example-tag">塑料瓶</span>
            <span class="example-tag">易拉罐</span>
            <span class="example-tag">纸箱</span>
            <span class="example-tag">玻璃瓶</span>
            <span class="example-tag">报纸</span>
          </div>
          <div class="guide-tip">保持清洁干燥，避免污染</div>
        </div>
        <div class="guide-card hazardous">
          <div class="guide-icon">☢️</div>
          <div class="guide-title">有害垃圾</div>
          <div class="guide-examples">
            <span class="example-tag">电池</span>
            <span class="example-tag">灯管</span>
            <span class="example-tag">药品</span>
            <span class="example-tag">温度计</span>
            <span class="example-tag">油漆</span>
          </div>
          <div class="guide-tip">轻投轻放，避免破损</div>
        </div>
        <div class="guide-card kitchen">
          <div class="guide-icon">🍲</div>
          <div class="guide-title">厨余垃圾</div>
          <div class="guide-examples">
            <span class="example-tag">果皮</span>
            <span class="example-tag">剩菜</span>
            <span class="example-tag">蛋壳</span>
            <span class="example-tag">菜叶</span>
            <span class="example-tag">茶叶渣</span>
          </div>
          <div class="guide-tip">沥干水分，去除包装</div>
        </div>
        <div class="guide-card other">
          <div class="guide-icon">🗑️</div>
          <div class="guide-title">其他垃圾</div>
          <div class="guide-examples">
            <span class="example-tag">塑料袋</span>
            <span class="example-tag">烟蒂</span>
            <span class="example-tag">尘土</span>
            <span class="example-tag">陶瓷</span>
            <span class="example-tag">卫生纸</span>
          </div>
          <div class="guide-tip">难以分类请投此处</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const fileInput = ref(null)
const selectedFile = ref(null)
const previewImage = ref(null)
const isClassifying = ref(false)
const result = ref(null)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    processFile(file)
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    processFile(file)
  } else {
    ElMessage.error('请上传图片文件')
  }
}

const processFile = (file) => {
  selectedFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    previewImage.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  selectedFile.value = null
  previewImage.value = null
  result.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const classifyImage = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  isClassifying.value = true
  result.value = null

  try {
    const formData = new FormData()
    formData.append('image', selectedFile.value)

    const response = await fetch('http://localhost:8082/api/v1/ai/garbage-classify', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (data.code === 0) {
      result.value = data.data
      ElMessage.success('识别成功！')
    } else {
      ElMessage.error(data.msg || '识别失败')
    }
  } catch (error) {
    console.error('识别错误:', error)
    ElMessage.error('识别失败，请检查网络连接')
  } finally {
    isClassifying.value = false
  }
}

const clearResult = () => {
  result.value = null
}

const getClassIcon = (className) => {
  const icons = {
    '可回收物': '♻️',
    '有害垃圾': '☢️',
    '厨余垃圾': '🍲',
    '其他垃圾': '🗑️'
  }
  return icons[className] || '❓'
}

const getClassDescription = (className) => {
  const descriptions = {
    '可回收物': '适宜回收利用和资源化利用的生活废弃物',
    '有害垃圾': '对人体健康或自然环境造成直接或潜在危害的废弃物',
    '厨余垃圾': '易腐烂的、含有机质的生活废弃物',
    '其他垃圾': '除可回收物、有害垃圾、厨余垃圾以外的其他生活废弃物'
  }
  return descriptions[className] || '未知垃圾类型'
}

const getDisposalTips = (className) => {
  const tips = {
    '可回收物': '请保持清洁干燥，避免污染。纸类应折叠整齐，瓶罐类应清空内容物并压扁。',
    '有害垃圾': '请轻投轻放，避免破损。电池应保持完整，灯管应防止破损。',
    '厨余垃圾': '请沥干水分，去除包装物。避免混入塑料袋等非厨余垃圾。',
    '其他垃圾': '请沥干水分，难以辨识类别的生活垃圾请投入其他垃圾收集容器。'
  }
  return tips[className] || '请按照当地垃圾分类标准进行处理'
}
</script>

<style scoped>
.garbage-classification {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.classification-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

@media (max-width: 768px) {
  .classification-container {
    grid-template-columns: 1fr;
  }
}

.upload-section {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.upload-box {
  border: 2px dashed #3498db;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-box:hover {
  border-color: #2980b9;
  background: #f8fbff;
}

.upload-placeholder {
  width: 100%;
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.upload-placeholder h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.upload-placeholder p {
  color: #7f8c8d;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 100%;
}

.image-preview img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 8px;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.remove-btn:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

.upload-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-secondary {
  background: #ecf0f1;
  color: #2c3e50;
}

.btn-secondary:hover:not(:disabled) {
  background: #bdc3c7;
}

.result-section {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.result-placeholder {
  text-align: center;
  padding: 60px 20px;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.result-placeholder h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.result-placeholder p {
  color: #7f8c8d;
}

.result-content {
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-header h3 {
  font-size: 1.5rem;
  color: #2c3e50;
}

.confidence-badge {
  background: #27ae60;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.result-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.result-card.可回收物 {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.result-card.有害垃圾 {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
}

.result-card.厨余垃圾 {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.result-card.其他垃圾 {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.result-icon {
  font-size: 4rem;
}

.result-info .item-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 5px;
  opacity: 0.95;
}

.result-info h2 {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.result-info p {
  font-size: 1rem;
  opacity: 0.9;
}

.all-detections {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.all-detections h4 {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.detection-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: white;
  border-radius: 6px;
  transition: all 0.3s;
}

.detection-item.active {
  background: #3498db;
  color: white;
}

.detection-class {
  font-weight: 500;
}

.detection-confidence {
  font-size: 0.9rem;
  opacity: 0.8;
}

.result-tips {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 15px 20px;
  border-radius: 6px;
  margin-bottom: 15px;
}

.result-tips.specific-tips {
  background: #d4edda;
  border-left-color: #28a745;
}

.result-tips.specific-tips h4,
.result-tips.specific-tips p {
  color: #155724;
}

.result-tips.recycling-value {
  background: #d1ecf1;
  border-left-color: #17a2b8;
}

.result-tips.recycling-value h4,
.result-tips.recycling-value p {
  color: #0c5460;
}

.result-tips h4 {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.result-tips p {
  line-height: 1.6;
}

.info-section {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.info-section h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

.guide-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.guide-card {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.guide-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.guide-card.recyclable {
  border-color: #27ae60;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

.guide-card.hazardous {
  border-color: #e74c3c;
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
}

.guide-card.kitchen {
  border-color: #f39c12;
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
}

.guide-card.other {
  border-color: #95a5a6;
  background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%);
}

.guide-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.guide-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
}

.guide-examples {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 15px;
}

.example-tag {
  background: rgba(255, 255, 255, 0.8);
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.85rem;
  color: #2c3e50;
}

.guide-tip {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-style: italic;
}
</style>
