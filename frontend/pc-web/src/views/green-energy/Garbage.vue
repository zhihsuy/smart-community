<template>
  <div class="garbage-classification">
    <div class="page-header">
      <h1>♻️ AI绿色垃圾分类</h1>
      <p>使用AI技术轻松识别和分类垃圾</p>
    </div>

    <div class="content-section">
      <div class="classification-methods">
        <div class="method-card active">
          <div class="method-icon">💬</div>
          <h3>文字识别</h3>
          <p>输入垃圾名称，AI帮你识别分类</p>
        </div>
        <div class="method-card">
          <div class="method-icon">📷</div>
          <h3>图片识别</h3>
          <p>上传垃圾图片，AI自动识别分类</p>
        </div>
      </div>

      <div class="input-section">
        <div class="text-input-container">
          <el-input
            v-model="garbageName"
            placeholder="请输入垃圾名称，例如：塑料瓶、废纸等"
            style="width: 400px"
            @keyup.enter="classifyGarbage"
          >
            <template #append>
              <el-button type="primary" @click="classifyGarbage">
                <el-icon><Search /></el-icon>
                识别
              </el-button>
            </template>
          </el-input>
        </div>
      </div>

      <div v-if="result" class="result-section">
        <div class="result-card">
          <div class="result-header">
            <h3>识别结果</h3>
          </div>
          <div class="result-content">
            <div class="garbage-info">
              <div class="garbage-name">{{ garbageName }}</div>
              <div class="garbage-category" :class="result.categoryClass">
                {{ result.category }}
              </div>
            </div>
            <div class="disposal-method">
              <h4>投放建议</h4>
              <p>{{ result.disposalMethod }}</p>
            </div>
            <div class="garbage-description">
              <h4>垃圾分类小知识</h4>
              <p>{{ result.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="knowledge-section">
        <h2>📚 垃圾分类知识库</h2>
        <div class="knowledge-grid">
          <div 
            v-for="item in garbageKnowledge" 
            :key="item.id"
            class="knowledge-card"
            :class="item.categoryClass"
          >
            <div class="knowledge-icon">{{ item.icon }}</div>
            <h3>{{ item.category }}</h3>
            <p>{{ item.description }}</p>
            <div class="example-list">
              <span v-for="(example, index) in item.examples" :key="index" class="example-tag">
                {{ example }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const garbageName = ref('')
const result = ref(null)

const garbageKnowledge = [
  {
    id: 1,
    category: '可回收物',
    icon: '♻️',
    description: '可回收物是指适宜回收循环使用和资源利用的废物',
    examples: ['废纸', '塑料瓶', '玻璃瓶', '易拉罐', '金属'],
    categoryClass: 'recyclable'
  },
  {
    id: 2,
    category: '有害垃圾',
    icon: '⚠️',
    description: '有害垃圾是指含有对人体健康有害的重金属、有毒的物质或者对环境造成现实危害或者潜在危害的废弃物',
    examples: ['废电池', '过期药品', '废油漆', '废灯管', '废化妆品'],
    categoryClass: 'hazardous'
  },
  {
    id: 3,
    category: '厨余垃圾',
    icon: '🍎',
    description: '厨余垃圾是指居民日常生活及食品加工、饮食服务、单位供餐等活动中产生的垃圾',
    examples: ['剩菜剩饭', '果皮', '蛋壳', '茶叶渣', '骨头'],
    categoryClass: 'kitchen'
  },
  {
    id: 4,
    category: '其他垃圾',
    icon: '🗑️',
    description: '其他垃圾是指除可回收物、有害垃圾、厨余垃圾以外的其他生活废弃物',
    examples: ['卫生纸', '尿不湿', '一次性餐具', '烟头', '灰土'],
    categoryClass: 'other'
  }
]

const classifyGarbage = () => {
  if (!garbageName.value.trim()) {
    return
  }

  // 模拟AI识别结果
  const mockResults = {
    '塑料瓶': {
      category: '可回收物',
      categoryClass: 'recyclable',
      description: '塑料瓶属于可回收物，应该投放到蓝色垃圾桶中。请确保清洗干净后再投放。',
      disposalMethod: '清洗干净后压扁投放'
    },
    '废纸': {
      category: '可回收物',
      categoryClass: 'recyclable',
      description: '废纸属于可回收物，应该投放到蓝色垃圾桶中。请确保纸张清洁干燥。',
      disposalMethod: '清洁干燥后投放'
    },
    '废电池': {
      category: '有害垃圾',
      categoryClass: 'hazardous',
      description: '废电池属于有害垃圾，应该投放到红色垃圾桶中。',
      disposalMethod: '投放至有害垃圾收集容器'
    },
    '剩菜剩饭': {
      category: '厨余垃圾',
      categoryClass: 'kitchen',
      description: '剩菜剩饭属于厨余垃圾，应该投放到绿色垃圾桶中。',
      disposalMethod: '沥干水分后投放'
    },
    '卫生纸': {
      category: '其他垃圾',
      categoryClass: 'other',
      description: '卫生纸属于其他垃圾，应该投放到灰色垃圾桶中。',
      disposalMethod: '投放至其他垃圾收集容器'
    }
  }

  // 如果没有匹配的结果，返回一个默认结果
  result.value = mockResults[garbageName.value] || {
    category: '其他垃圾',
    categoryClass: 'other',
    description: '该垃圾未在知识库中找到，建议投放到其他垃圾收集容器。',
    disposalMethod: '投放至其他垃圾收集容器'
  }
}
</script>

<style scoped>
.garbage-classification {
  min-height: 100vh;
  background: #f8fafc;
}

.page-header {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 10px;
  font-weight: 600;
}

.page-header p {
  font-size: 18px;
  opacity: 0.9;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.classification-methods {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
  justify-content: center;
}

.method-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  flex: 1;
  max-width: 200px;
}

.method-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.method-card.active {
  border: 2px solid #10b981;
  background: #f0fdf4;
}

.method-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.method-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.method-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.input-section {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.text-input-container {
  display: flex;
  align-items: center;
}

.result-section {
  margin-bottom: 60px;
}

.result-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.result-header h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
}

.garbage-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.garbage-name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.garbage-category {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  color: white;
}

.garbage-category.recyclable {
  background: #3b82f6;
}

.garbage-category.hazardous {
  background: #ef4444;
}

.garbage-category.kitchen {
  background: #10b981;
}

.garbage-category.other {
  background: #6b7280;
}

.disposal-method, .garbage-description {
  margin-bottom: 20px;
}

.disposal-method h4, .garbage-description h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.disposal-method p, .garbage-description p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}

.knowledge-section {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.knowledge-section h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.knowledge-card {
  padding: 25px;
  border-radius: 8px;
  color: white;
  transition: all 0.3s ease;
}

.knowledge-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.knowledge-card.recyclable {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.knowledge-card.hazardous {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.knowledge-card.kitchen {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.knowledge-card.other {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}

.knowledge-icon {
  font-size: 36px;
  margin-bottom: 15px;
}

.knowledge-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  font-weight: 600;
}

.knowledge-card p {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 20px;
  opacity: 0.9;
}

.example-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.example-tag {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 12px;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 20px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .content-section {
    padding: 20px;
  }
  
  .classification-methods {
    flex-direction: column;
    align-items: center;
  }
  
  .method-card {
    max-width: 100%;
    width: 100%;
  }
  
  .text-input-container {
    width: 100%;
  }
  
  .text-input-container .el-input {
    width: 100% !important;
  }
  
  .knowledge-section {
    padding: 20px;
  }
  
  .knowledge-grid {
    grid-template-columns: 1fr;
  }
}
</style>