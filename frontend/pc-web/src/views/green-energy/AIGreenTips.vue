<template>
  <div class="ai-green-tips">
    <div class="page-header">
      <h1>🤖 AI绿色生活建议</h1>
      <p>基于人工智能，为您提供个性化的绿色生活建议</p>
    </div>

    <div class="content-section">
      <!-- AI建议生成 -->
      <div class="ai-tips-form-card">
        <h3>📋 获取个性化建议</h3>
        <p>请填写以下信息，AI将为您生成个性化的绿色生活建议</p>
        
        <div class="form-section">
          <h4>🏠 居住环境</h4>
          <div class="form-group">
            <label>居住城市</label>
            <el-input v-model="userProfile.city" placeholder="请输入居住城市" />
          </div>
          <div class="form-group">
            <label>居住类型</label>
            <el-select v-model="userProfile.housingType" placeholder="请选择居住类型" class="w-full">
              <el-option label="公寓" value="apartment" />
              <el-option label="别墅" value="villa" />
              <el-option label="联排别墅" value="townhouse" />
              <el-option label="其他" value="other" />
            </el-select>
          </div>
          <div class="form-group">
            <label>家庭成员数量</label>
            <el-input-number v-model="userProfile.familySize" :min="1" :max="10" class="w-full" />
          </div>
        </div>

        <div class="form-section">
          <h4>🌱 环保意识</h4>
          <div class="form-group">
            <label>环保关注度</label>
            <el-radio-group v-model="userProfile.interestLevel">
              <el-radio label="非常关注">非常关注</el-radio>
              <el-radio label="比较关注">比较关注</el-radio>
              <el-radio label="一般">一般</el-radio>
              <el-radio label="不太关注">不太关注</el-radio>
            </el-radio-group>
          </div>
          <div class="form-group">
            <label>主要关注的环保领域</label>
            <el-checkbox-group v-model="userProfile.focusAreas">
              <el-checkbox label="垃圾分类" />
              <el-checkbox label="节能降耗" />
              <el-checkbox label="绿色出行" />
              <el-checkbox label="健康饮食" />
              <el-checkbox label="环境保护" />
            </el-checkbox-group>
          </div>
        </div>

        <div class="form-section">
          <h4>📊 生活习惯</h4>
          <div class="form-group">
            <label>日常出行方式</label>
            <el-select v-model="userProfile.travelMode" placeholder="请选择主要出行方式" class="w-full">
              <el-option label="私家车" value="car" />
              <el-option label="公共交通" value="public" />
              <el-option label="自行车" value="bicycle" />
              <el-option label="步行" value="walk" />
              <el-option label="混合方式" value="mixed" />
            </el-select>
          </div>
          <div class="form-group">
            <label>饮食习惯</label>
            <el-select v-model="userProfile.dietHabit" placeholder="请选择饮食习惯" class="w-full">
              <el-option label="以肉类为主" value="meat" />
              <el-option label="均衡饮食" value="balanced" />
              <el-option label="以素食为主" value="vegetarian" />
              <el-option label="纯素食" value="vegan" />
            </el-select>
          </div>
          <div class="form-group">
            <label>购物习惯</label>
            <el-select v-model="userProfile.shoppingHabit" placeholder="请选择购物习惯" class="w-full">
              <el-option label="经常网购" value="online" />
              <el-option label="经常线下购物" value="offline" />
              <el-option label="线上线下结合" value="mixed" />
            </el-select>
          </div>
        </div>

        <div class="form-actions">
          <el-button type="primary" @click="generateAITips" :loading="generating">
            <el-icon><MagicStick /></el-icon>
            生成AI建议
          </el-button>
        </div>
      </div>

      <!-- AI建议结果 -->
      <div v-if="aiTips.length > 0" class="ai-tips-result">
        <h3>✨ AI个性化建议</h3>
        <div class="tips-list">
          <div 
            v-for="(tip, index) in aiTips" 
            :key="index"
            class="tip-card"
          >
            <div class="tip-header">
              <div class="tip-category" :class="tip.categoryClass">
                {{ tip.category }}
              </div>
              <div class="tip-priority" :class="tip.priorityClass">
                {{ tip.priority }}
              </div>
            </div>
            <div class="tip-content">
              <h4>{{ tip.title }}</h4>
              <p>{{ tip.description }}</p>
              <div class="tip-benefits">
                <div class="benefit-item" v-for="(benefit, bIndex) in tip.benefits" :key="bIndex">
                  <span class="benefit-icon">✅</span>
                  <span class="benefit-text">{{ benefit }}</span>
                </div>
              </div>
              <div class="tip-action">
                <el-button type="primary" size="small" @click="implementTip(tip)">
                  实施建议
                </el-button>
                <el-button size="small" @click="saveTip(tip)">
                  保存建议
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 历史建议 -->
      <div v-if="savedTips.length > 0" class="saved-tips-section">
        <h3>📋 已保存的建议</h3>
        <div class="saved-tips-list">
          <div 
            v-for="(tip, index) in savedTips" 
            :key="index"
            class="saved-tip-item"
          >
            <div class="saved-tip-content">
              <h4>{{ tip.title }}</h4>
              <p>{{ tip.description.substring(0, 80) }}...</p>
            </div>
            <div class="saved-tip-actions">
              <el-button type="primary" size="small" @click="viewSavedTip(tip)">
                查看详情
              </el-button>
              <el-button type="danger" size="small" @click="deleteSavedTip(index)">
                删除
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- AI建议设置 -->
      <div class="ai-settings-section">
        <h3>⚙️ AI建议设置</h3>
        <div class="settings-grid">
          <div class="setting-item">
            <label>建议推送频率</label>
            <el-select v-model="aiSettings.frequency" placeholder="请选择推送频率" class="w-full">
              <el-option label="每天" value="daily" />
              <el-option label="每周" value="weekly" />
              <el-option label="每月" value="monthly" />
              <el-option label="不推送" value="never" />
            </el-select>
          </div>
          <div class="setting-item">
            <label>建议数量</label>
            <el-select v-model="aiSettings.count" placeholder="请选择建议数量" class="w-full">
              <el-option label="3条" value="3" />
              <el-option label="5条" value="5" />
              <el-option label="10条" value="10" />
            </el-select>
          </div>
          <div class="setting-item">
            <label>建议类型</label>
            <el-checkbox-group v-model="aiSettings.types">
              <el-checkbox label="生活建议" />
              <el-checkbox label="出行建议" />
              <el-checkbox label="饮食建议" />
              <el-checkbox label="节能建议" />
            </el-checkbox-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MagicStick } from '@element-plus/icons-vue'

const generating = ref(false)
const userProfile = ref({
  city: '',
  housingType: 'apartment',
  familySize: 3,
  interestLevel: '比较关注',
  focusAreas: ['垃圾分类', '节能降耗'],
  travelMode: 'public',
  dietHabit: 'balanced',
  shoppingHabit: 'mixed'
})

const aiSettings = ref({
  frequency: 'weekly',
  count: '5',
  types: ['生活建议', '出行建议', '饮食建议', '节能建议']
})

const aiTips = ref([])
const savedTips = ref([])

const generateAITips = () => {
  generating.value = true
  
  // 模拟AI生成建议的过程
  setTimeout(() => {
    aiTips.value = [
      {
        category: '绿色出行',
        categoryClass: 'travel',
        priority: '高优先级',
        priorityClass: 'high',
        title: '优化出行方式，减少碳足迹',
        description: '根据您的出行习惯，建议您在短途出行时优先选择步行或自行车，中长途出行时选择公共交通。这样可以显著减少碳排放，同时也有益于身体健康。',
        benefits: [
          '每周减少碳排放约5-10kg',
          '节省交通费用约50-100元',
          '增加日常运动量，改善身体健康'
        ]
      },
      {
        category: '节能降耗',
        categoryClass: 'energy',
        priority: '高优先级',
        priorityClass: 'high',
        title: '优化家庭能源使用',
        description: '建议您将家中的照明设备更换为LED灯泡，并在不使用时关闭电器。同时合理设置空调温度，夏季不低于26℃，冬季不高于20℃。',
        benefits: [
          '每月节省电费约30-50元',
          '减少家庭碳排放约20-30%',
          '延长电器使用寿命'
        ]
      },
      {
        category: '健康饮食',
        categoryClass: 'diet',
        priority: '中优先级',
        priorityClass: 'medium',
        title: '调整饮食结构，选择绿色食品',
        description: '建议您增加蔬菜和水果的摄入量，减少红肉消费。选择本地、当季的食材，减少食品运输过程中的碳排放。',
        benefits: [
          '降低个人碳足迹约15-25%',
          '改善营养均衡，有益健康',
          '支持本地农业发展'
        ]
      },
      {
        category: '垃圾分类',
        categoryClass: 'garbage',
        priority: '中优先级',
        priorityClass: 'medium',
        title: '完善垃圾分类习惯',
        description: '建议您在家中设置四个分类垃圾桶：可回收物、有害垃圾、厨余垃圾和其他垃圾。确保垃圾正确分类投放。',
        benefits: [
          '提高资源回收利用率',
          '减少环境污染',
          '为社区环保做贡献'
        ]
      },
      {
        category: '环境保护',
        categoryClass: 'environment',
        priority: '低优先级',
        priorityClass: 'low',
        title: '参与社区环保活动',
        description: '建议您积极参与社区组织的环保活动，如植树、清洁环境等。这不仅能改善社区环境，还能结识志同道合的朋友。',
        benefits: [
          '改善社区环境质量',
          '增强社区凝聚力',
          '获得环保积分奖励'
        ]
      }
    ]
    
    generating.value = false
  }, 2000)
}

const implementTip = (tip) => {
  alert(`已标记实施建议：${tip.title}`)
}

const saveTip = (tip) => {
  savedTips.value.push({
    ...tip,
    savedAt: new Date().toISOString()
  })
  alert('建议已保存')
}

const viewSavedTip = (tip) => {
  alert(tip.description)
}

const deleteSavedTip = (index) => {
  savedTips.value.splice(index, 1)
}
</script>

<style scoped>
.ai-green-tips {
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

.ai-tips-form-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

.ai-tips-form-card h3 {
  margin-bottom: 10px;
  color: #10b981;
  font-size: 20px;
}

.ai-tips-form-card p {
  margin-bottom: 30px;
  color: #666;
  font-size: 14px;
}

.form-section {
  margin-bottom: 30px;
}

.form-section h4 {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.ai-tips-result {
  margin-bottom: 40px;
}

.ai-tips-result h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tip-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.tip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.tip-category {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.tip-category.travel {
  background: #3b82f6;
}

.tip-category.energy {
  background: #f59e0b;
}

.tip-category.diet {
  background: #10b981;
}

.tip-category.garbage {
  background: #8b5cf6;
}

.tip-category.environment {
  background: #ef4444;
}

.tip-priority {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.tip-priority.high {
  background: #ef4444;
}

.tip-priority.medium {
  background: #f59e0b;
}

.tip-priority.low {
  background: #10b981;
}

.tip-content {
  padding: 20px;
}

.tip-content h4 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.tip-content p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 15px;
}

.tip-benefits {
  margin-bottom: 20px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  font-size: 14px;
  color: #666;
}

.benefit-icon {
  flex-shrink: 0;
  color: #10b981;
}

.tip-action {
  display: flex;
  gap: 10px;
}

.saved-tips-section {
  margin-bottom: 40px;
}

.saved-tips-section h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.saved-tips-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.saved-tip-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.saved-tip-content {
  flex: 1;
}

.saved-tip-content h4 {
  font-size: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.saved-tip-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}

.saved-tip-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.ai-settings-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.ai-settings-section h3 {
  text-align: center;
  font-size: 20px;
  margin-bottom: 30px;
  color: #10b981;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.setting-item label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
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
  
  .ai-tips-form-card {
    padding: 20px;
  }
  
  .tip-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .tip-action {
    flex-direction: column;
  }
  
  .saved-tip-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .saved-tip-actions {
    width: 100%;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>