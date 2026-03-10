<template>
  <div class="energy-tips">
    <div class="page-header">
      <h1>💡 节能小贴士</h1>
      <p>根据您的生活习惯，获取个性化的节能建议</p>
    </div>

    <div class="content-section">
      <!-- 用户生活习惯输入 -->
      <div class="habits-form-card">
        <h3>📋 生活习惯调查</h3>
        <p>请回答以下问题，我们将为您提供个性化的节能建议</p>
        
        <div class="form-section">
          <h4>🏠 家居情况</h4>
          <div class="form-group">
            <label>居住面积 (平方米)</label>
            <el-input-number v-model="habits.homeArea" :min="10" :max="500" class="w-full" />
          </div>
          <div class="form-group">
            <label>家庭人数</label>
            <el-input-number v-model="habits.familyMembers" :min="1" :max="10" class="w-full" />
          </div>
          <div class="form-group">
            <label>房屋类型</label>
            <el-select v-model="habits.homeType" placeholder="请选择房屋类型" class="w-full">
              <el-option label="公寓" value="apartment" />
              <el-option label="别墅" value="villa" />
              <el-option label="联排别墅" value="townhouse" />
              <el-option label="其他" value="other" />
            </el-select>
          </div>
        </div>

        <div class="form-section">
          <h4>💡 用电习惯</h4>
          <div class="form-group">
            <label>每天使用空调的时间 (小时)</label>
            <el-input-number v-model="habits.acHours" :min="0" :max="24" class="w-full" />
          </div>
          <div class="form-group">
            <label>使用的灯泡类型</label>
            <el-select v-model="habits.lightType" placeholder="请选择灯泡类型" class="w-full">
              <el-option label="传统白炽灯" value="incandescent" />
              <el-option label="荧光灯" value="fluorescent" />
              <el-option label="LED灯" value="led" />
            </el-select>
          </div>
          <div class="form-group">
            <label>电器待机习惯</label>
            <el-radio-group v-model="habits.standbyHabit">
              <el-radio label="经常让电器待机">经常让电器待机</el-radio>
              <el-radio label="偶尔让电器待机">偶尔让电器待机</el-radio>
              <el-radio label="从不让电器待机">从不让电器待机</el-radio>
            </el-radio-group>
          </div>
        </div>

        <div class="form-section">
          <h4>🚿 用水习惯</h4>
          <div class="form-group">
            <label>每天洗澡时间 (分钟)</label>
            <el-input-number v-model="habits.showerTime" :min="1" :max="60" class="w-full" />
          </div>
          <div class="form-group">
            <label>是否使用节水器具</label>
            <el-radio-group v-model="habits.waterSaving">
              <el-radio label="是">是</el-radio>
              <el-radio label="否">否</el-radio>
            </el-radio-group>
          </div>
        </div>

        <div class="form-actions">
          <el-button type="primary" @click="generateTips">
            <el-icon><MagicStick /></el-icon>
            生成节能建议
          </el-button>
        </div>
      </div>

      <!-- 个性化节能建议 -->
      <div v-if="personalizedTips.length > 0" class="tips-section">
        <h3>✨ 个性化节能建议</h3>
        <div class="tips-grid">
          <div 
            v-for="(tip, index) in personalizedTips" 
            :key="index"
            class="tip-card"
          >
            <div class="tip-icon">{{ tip.icon }}</div>
            <h4>{{ tip.title }}</h4>
            <p>{{ tip.description }}</p>
            <div class="tip-saving">
              <span class="saving-label">预计节能:</span>
              <span class="saving-value">{{ tip.saving }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 分类节能技巧 -->
      <div class="category-tips-section">
        <h3>📚 分类节能技巧</h3>
        <div class="category-tabs">
          <button 
            v-for="category in categories" 
            :key="category.id"
            :class="{ active: activeCategory === category.id }"
            @click="activeCategory = category.id"
          >
            {{ category.icon }} {{ category.name }}
          </button>
        </div>

        <div class="category-content">
          <div v-if="activeCategory === 'home'" class="category-tips">
            <div class="tip-item" v-for="tip in homeTips" :key="tip.id">
              <div class="tip-icon">{{ tip.icon }}</div>
              <div class="tip-content">
                <h4>{{ tip.title }}</h4>
                <p>{{ tip.description }}</p>
              </div>
            </div>
          </div>

          <div v-if="activeCategory === 'kitchen'" class="category-tips">
            <div class="tip-item" v-for="tip in kitchenTips" :key="tip.id">
              <div class="tip-icon">{{ tip.icon }}</div>
              <div class="tip-content">
                <h4>{{ tip.title }}</h4>
                <p>{{ tip.description }}</p>
              </div>
            </div>
          </div>

          <div v-if="activeCategory === 'bathroom'" class="category-tips">
            <div class="tip-item" v-for="tip in bathroomTips" :key="tip.id">
              <div class="tip-icon">{{ tip.icon }}</div>
              <div class="tip-content">
                <h4>{{ tip.title }}</h4>
                <p>{{ tip.description }}</p>
              </div>
            </div>
          </div>

          <div v-if="activeCategory === 'appliances'" class="category-tips">
            <div class="tip-item" v-for="tip in appliancesTips" :key="tip.id">
              <div class="tip-icon">{{ tip.icon }}</div>
              <div class="tip-content">
                <h4>{{ tip.title }}</h4>
                <p>{{ tip.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 节能效果预览 -->
      <div v-if="energySavingPreview" class="preview-section">
        <h3>📊 节能效果预览</h3>
        <div class="preview-card">
          <div class="preview-item">
            <div class="preview-icon">💡</div>
            <div class="preview-info">
              <div class="preview-label">预计每月节省电量</div>
              <div class="preview-value">{{ energySavingPreview.electricity }} kWh</div>
            </div>
          </div>
          <div class="preview-item">
            <div class="preview-icon">💧</div>
            <div class="preview-info">
              <div class="preview-label">预计每月节省水量</div>
              <div class="preview-value">{{ energySavingPreview.water }} 吨</div>
            </div>
          </div>
          <div class="preview-item">
            <div class="preview-icon">💰</div>
            <div class="preview-info">
              <div class="preview-label">预计每月节省费用</div>
              <div class="preview-value">¥{{ energySavingPreview.cost }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MagicStick } from '@element-plus/icons-vue'

const habits = ref({
  homeArea: 100,
  familyMembers: 3,
  homeType: 'apartment',
  acHours: 8,
  lightType: 'led',
  standbyHabit: '偶尔让电器待机',
  showerTime: 10,
  waterSaving: '否'
})

const activeCategory = ref('home')
const personalizedTips = ref([])
const energySavingPreview = ref(null)

const categories = [
  { id: 'home', name: '家居节能', icon: '🏠' },
  { id: 'kitchen', name: '厨房节能', icon: '🍳' },
  { id: 'bathroom', name: '浴室节能', icon: '🚿' },
  { id: 'appliances', name: '电器节能', icon: '📺' }
]

const homeTips = [
  {
    id: 1,
    icon: '💡',
    title: '使用LED灯泡',
    description: 'LED灯泡比传统白炽灯节能80%以上，寿命也更长。'
  },
  {
    id: 2,
    icon: '🌡️',
    title: '合理设置空调温度',
    description: '夏季空调温度设置26℃，冬季设置20℃，每调高/调低1℃，可节省6-10%的能耗。'
  },
  {
    id: 3,
    icon: ' 🪟',
    title: '改善门窗密封',
    description: '检查门窗密封情况，使用密封条或窗帘，减少冷热空气流失。'
  },
  {
    id: 4,
    icon: '☀️',
    title: '利用自然光线',
    description: '白天尽量使用自然光线，减少人工照明的使用。'
  }
]

const kitchenTips = [
  {
    id: 1,
    icon: '🍳',
    title: '合理使用厨具',
    description: '选择适合锅具大小的炉头，使用锅盖，减少热量流失。'
  },
  {
    id: 2,
    icon: '🔥',
    title: '控制火候',
    description: '烹饪时根据需要调整火候，避免大火空烧。'
  },
  {
    id: 3,
    icon: '🚿',
    title: '及时关闭水龙头',
    description: '洗菜、洗碗时不要让水龙头一直开着，使用盆接水。'
  },
  {
    id: 4,
    icon: '❄️',
    title: '冰箱使用技巧',
    description: '冰箱不要放得太满，保持通风，定期除霜，温度设置在4-5℃。'
  }
]

const bathroomTips = [
  {
    id: 1,
    icon: '🚿',
    title: '缩短淋浴时间',
    description: '淋浴时间控制在10分钟以内，可节省大量热水。'
  },
  {
    id: 2,
    icon: '💧',
    title: '安装节水器具',
    description: '使用节水淋浴喷头、节水马桶等节水器具。'
  },
  {
    id: 3,
    icon: '🧼',
    title: '集中洗衣',
    description: '衣物积累到一定量再洗，使用洗衣机的节能模式。'
  },
  {
    id: 4,
    icon: '💡',
    title: '使用浴后余温',
    description: '洗澡后及时关闭热水器，利用余温。'
  }
]

const appliancesTips = [
  {
    id: 1,
    icon: '📺',
    title: '关闭待机电器',
    description: '不使用的电器要彻底关闭，避免待机能耗。'
  },
  {
    id: 2,
    icon: '💻',
    title: '电脑节能',
    description: '设置电脑自动休眠，不用时关闭显示器。'
  },
  {
    id: 3,
    icon: '📱',
    title: '合理充电',
    description: '电池充满后及时拔掉充电器，避免过度充电。'
  },
  {
    id: 4,
    icon: '🧺',
    title: '洗衣机使用',
    description: '使用冷水洗涤，选择合适的洗涤程序，避免过度洗涤。'
  }
]

const generateTips = () => {
  personalizedTips.value = []
  
  // 根据居住面积和空调使用时间生成建议
  if (habits.value.acHours > 6) {
    personalizedTips.value.push({
      icon: '🌡️',
      title: '优化空调使用',
      description: '您每天使用空调时间较长，建议设置温度为26℃，并使用节能模式。',
      saving: '15-20% 能耗'
    })
  }
  
  // 根据灯泡类型生成建议
  if (habits.value.lightType !== 'led') {
    personalizedTips.value.push({
      icon: '💡',
      title: '更换LED灯泡',
      description: '建议将传统灯泡更换为LED灯泡，可节省80%以上的照明能耗。',
      saving: '80% 照明能耗'
    })
  }
  
  // 根据电器待机习惯生成建议
  if (habits.value.standbyHabit !== '从不让电器待机') {
    personalizedTips.value.push({
      icon: '📱',
      title: '减少待机能耗',
      description: '建议使用智能插座或手动关闭不使用的电器，避免待机能耗。',
      saving: '5-10% 总能耗'
    })
  }
  
  // 根据洗澡时间生成建议
  if (habits.value.showerTime > 15) {
    personalizedTips.value.push({
      icon: '🚿',
      title: '缩短淋浴时间',
      description: '建议将淋浴时间控制在10分钟以内，可节省大量热水。',
      saving: '30% 热水能耗'
    })
  }
  
  // 根据节水器具使用情况生成建议
  if (habits.value.waterSaving === '否') {
    personalizedTips.value.push({
      icon: '💧',
      title: '安装节水器具',
      description: '建议安装节水淋浴喷头和节水马桶，可减少30-50%的用水量。',
      saving: '30-50% 用水量'
    })
  }
  
  // 生成节能效果预览
  energySavingPreview.value = {
    electricity: (Math.random() * 50 + 20).toFixed(1),
    water: (Math.random() * 10 + 5).toFixed(1),
    cost: (Math.random() * 100 + 50).toFixed(0)
  }
}
</script>

<style scoped>
.energy-tips {
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

.habits-form-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

.habits-form-card h3 {
  margin-bottom: 10px;
  color: #10b981;
  font-size: 20px;
}

.habits-form-card p {
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

.tips-section {
  margin-bottom: 40px;
}

.tips-section h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.tip-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-align: center;
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.tip-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.tip-card h4 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.tip-card p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 15px;
}

.tip-saving {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: #d1fae5;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: #065f46;
}

.category-tips-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
  overflow: hidden;
}

.category-tips-section h3 {
  padding: 20px;
  margin: 0;
  background: #10b981;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.category-tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.category-tabs button {
  flex: 1;
  padding: 15px;
  border: none;
  background: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
}

.category-tabs button:hover {
  background: #f3f4f6;
}

.category-tabs button.active {
  background: #10b981;
  color: white;
}

.category-content {
  padding: 30px;
}

.category-tips {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tip-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tip-item .tip-icon {
  font-size: 32px;
  flex-shrink: 0;
  margin-top: 5px;
  color: #10b981;
}

.tip-content h4 {
  font-size: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.tip-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}

.preview-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.preview-section h3 {
  text-align: center;
  font-size: 20px;
  margin-bottom: 30px;
  color: #10b981;
}

.preview-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}

.preview-icon {
  font-size: 32px;
  flex-shrink: 0;
  color: #10b981;
}

.preview-info {
  flex: 1;
}

.preview-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.preview-value {
  font-size: 20px;
  font-weight: 600;
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
  
  .habits-form-card {
    padding: 20px;
  }
  
  .tips-grid {
    grid-template-columns: 1fr;
  }
  
  .category-content {
    padding: 20px;
  }
  
  .preview-card {
    grid-template-columns: 1fr;
  }
}
</style>