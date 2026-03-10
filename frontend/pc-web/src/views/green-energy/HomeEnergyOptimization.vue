<template>
  <div class="home-energy-optimization">
    <div class="page-header">
      <h1>🏠 家居节能优化</h1>
      <p>分析家居能耗，获取节能优化方案</p>
    </div>

    <div class="content-section">
      <!-- 家居信息输入 -->
      <div class="home-info-card">
        <h3>📋 家居信息</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>居住面积 (平方米)</label>
            <el-input-number v-model="homeInfo.area" :min="20" :max="500" class="w-full" />
          </div>
          <div class="form-group">
            <label>房屋类型</label>
            <el-select v-model="homeInfo.type" placeholder="请选择房屋类型" class="w-full">
              <el-option label="公寓" value="apartment" />
              <el-option label="别墅" value="villa" />
              <el-option label="联排别墅" value="townhouse" />
              <el-option label="其他" value="other" />
            </el-select>
          </div>
          <div class="form-group">
            <label>家庭成员数量</label>
            <el-input-number v-model="homeInfo.members" :min="1" :max="10" class="w-full" />
          </div>
          <div class="form-group">
            <label>建筑年代</label>
            <el-select v-model="homeInfo.year" placeholder="请选择建筑年代" class="w-full">
              <el-option label="2020年后" value="2020+" />
              <el-option label="2010-2019" value="2010-2019" />
              <el-option label="2000-2009" value="2000-2009" />
              <el-option label="2000年前" value="before2000" />
            </el-select>
          </div>
        </div>
      </div>

      <!-- 能耗信息输入 -->
      <div class="energy-info-card">
        <h3>⚡ 能耗信息</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>每月用电量 (度)</label>
            <el-input-number v-model="energyInfo.electricity" :min="0" class="w-full" />
          </div>
          <div class="form-group">
            <label>每月用气量 (立方米)</label>
            <el-input-number v-model="energyInfo.gas" :min="0" class="w-full" />
          </div>
          <div class="form-group">
            <label>每月用水量 (吨)</label>
            <el-input-number v-model="energyInfo.water" :min="0" class="w-full" />
          </div>
          <div class="form-group">
            <label>每月电费 (元)</label>
            <el-input-number v-model="energyInfo.electricityCost" :min="0" class="w-full" />
          </div>
        </div>

        <div class="appliances-section">
          <h4>📺 家用电器</h4>
          <div class="appliances-grid">
            <div 
              v-for="appliance in appliances" 
              :key="appliance.id"
              class="appliance-item"
            >
              <div class="appliance-header">
                <input 
                  type="checkbox" 
                  v-model="appliance.selected"
                  :id="appliance.id"
                />
                <label :for="appliance.id" class="appliance-name">
                  {{ appliance.name }}
                </label>
              </div>
              <div class="appliance-details" v-if="appliance.selected">
                <div class="detail-item">
                  <label>使用时长 (小时/天)</label>
                  <el-input-number 
                    v-model="appliance.usageHours" 
                    :min="0" 
                    :max="24" 
                    size="small" 
                  />
                </div>
                <div class="detail-item">
                  <label>数量</label>
                  <el-input-number 
                    v-model="appliance.count" 
                    :min="1" 
                    size="small" 
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <el-button type="primary" @click="analyzeEnergy" :loading="analyzing">
            <el-icon><DataAnalysis /></el-icon>
            分析能耗
          </el-button>
          <el-button @click="resetForm">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
      </div>

      <!-- 能耗分析结果 -->
      <div v-if="energyAnalysis" class="analysis-result-section">
        <div class="result-grid">
          <!-- 能耗概览 -->
          <div class="overview-card">
            <h4>📊 能耗概览</h4>
            <div class="overview-stats">
              <div class="stat-item">
                <div class="stat-icon">💡</div>
                <div class="stat-info">
                  <div class="stat-value">{{ energyAnalysis.totalEnergy }} kWh</div>
                  <div class="stat-label">总能耗</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon">💰</div>
                <div class="stat-info">
                  <div class="stat-value">¥{{ energyAnalysis.totalCost }}</div>
                  <div class="stat-label">总费用</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon">🌱</div>
                <div class="stat-info">
                  <div class="stat-value">{{ energyAnalysis.carbonEmission }} kg CO₂</div>
                  <div class="stat-label">碳排放</div>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon">📈</div>
                <div class="stat-info">
                  <div class="stat-value">{{ energyAnalysis.efficiency }}%</div>
                  <div class="stat-label">能效评级</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 能耗分布图表 -->
          <div class="chart-card">
            <h4>📈 能耗分布</h4>
            <div class="chart-container">
              <canvas ref="energyChart"></canvas>
            </div>
          </div>
        </div>

        <!-- 节能建议 -->
        <div class="suggestions-section">
          <h4>💡 节能建议</h4>
          <div class="suggestions-grid">
            <div 
              v-for="(suggestion, index) in energyAnalysis.suggestions" 
              :key="index"
              class="suggestion-card"
            >
              <div class="suggestion-header">
                <div class="suggestion-icon">{{ suggestion.icon }}</div>
                <h5>{{ suggestion.title }}</h5>
                <div class="suggestion-priority" :class="suggestion.priorityClass">
                  {{ suggestion.priority }}
                </div>
              </div>
              <div class="suggestion-content">
                <p>{{ suggestion.description }}</p>
                <div class="suggestion-benefits">
                  <div class="benefit-item">
                    <span class="benefit-label">预计节能:</span>
                    <span class="benefit-value">{{ suggestion.saving }}%</span>
                  </div>
                  <div class="benefit-item">
                    <span class="benefit-label">预计节省费用:</span>
                    <span class="benefit-value">¥{{ suggestion.costSaving }}/月</span>
                  </div>
                  <div class="benefit-item">
                    <span class="benefit-label">投资回报期:</span>
                    <span class="benefit-value">{{ suggestion.paybackPeriod }}</span>
                  </div>
                </div>
                <div class="suggestion-actions">
                  <el-button type="primary" size="small" @click="implementSuggestion(suggestion)">
                    实施建议
                  </el-button>
                  <el-button size="small" @click="simulateSuggestion(suggestion)">
                    模拟效果
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 节能方案模拟 -->
        <div v-if="simulationResult" class="simulation-section">
          <h4>🔮 节能方案模拟</h4>
          <div class="simulation-grid">
            <div class="simulation-card">
              <h5>当前方案</h5>
              <div class="simulation-stats">
                <div class="sim-stat">
                  <span class="sim-label">月度能耗:</span>
                  <span class="sim-value">{{ simulationResult.current.energy }} kWh</span>
                </div>
                <div class="sim-stat">
                  <span class="sim-label">月度费用:</span>
                  <span class="sim-value">¥{{ simulationResult.current.cost }}</span>
                </div>
                <div class="sim-stat">
                  <span class="sim-label">碳排放:</span>
                  <span class="sim-value">{{ simulationResult.current.carbon }} kg CO₂</span>
                </div>
              </div>
            </div>
            <div class="simulation-card optimized">
              <h5>优化方案</h5>
              <div class="simulation-stats">
                <div class="sim-stat">
                  <span class="sim-label">月度能耗:</span>
                  <span class="sim-value eco">{{ simulationResult.optimized.energy }} kWh</span>
                </div>
                <div class="sim-stat">
                  <span class="sim-label">月度费用:</span>
                  <span class="sim-value eco">¥{{ simulationResult.optimized.cost }}</span>
                </div>
                <div class="sim-stat">
                  <span class="sim-label">碳排放:</span>
                  <span class="sim-value eco">{{ simulationResult.optimized.carbon }} kg CO₂</span>
                </div>
              </div>
            </div>
          </div>
          <div class="simulation-comparison">
            <div class="comparison-item">
              <span class="comparison-label">节能效果:</span>
              <span class="comparison-value positive">-{{ simulationResult.saving.energy }} kWh (-{{ simulationResult.saving.percentage }}%)</span>
            </div>
            <div class="comparison-item">
              <span class="comparison-label">节省费用:</span>
              <span class="comparison-value positive">¥{{ simulationResult.saving.cost }}/月</span>
            </div>
            <div class="comparison-item">
              <span class="comparison-label">减少碳排放:</span>
              <span class="comparison-value positive">-{{ simulationResult.saving.carbon }} kg CO₂</span>
            </div>
            <div class="comparison-item">
              <span class="comparison-label">年度节省:</span>
              <span class="comparison-value positive">¥{{ simulationResult.saving.annual }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { DataAnalysis, Refresh } from '@element-plus/icons-vue'
import Chart from 'chart.js/auto'

const analyzing = ref(false)
const energyChart = ref(null)
const chartInstance = ref(null)

const homeInfo = ref({
  area: 100,
  type: 'apartment',
  members: 3,
  year: '2010-2019'
})

const energyInfo = ref({
  electricity: 200,
  gas: 30,
  water: 10,
  electricityCost: 150
})

const appliances = ref([
  { id: 'ac', name: '空调', selected: true, usageHours: 6, count: 2 },
  { id: 'fridge', name: '冰箱', selected: true, usageHours: 24, count: 1 },
  { id: 'tv', name: '电视', selected: true, usageHours: 4, count: 2 },
  { id: 'washing', name: '洗衣机', selected: true, usageHours: 1, count: 1 },
  { id: 'waterHeater', name: '热水器', selected: true, usageHours: 2, count: 1 },
  { id: 'computer', name: '电脑', selected: false, usageHours: 4, count: 1 },
  { id: 'microwave', name: '微波炉', selected: false, usageHours: 0.5, count: 1 }
])

const energyAnalysis = ref(null)
const simulationResult = ref(null)

const analyzeEnergy = () => {
  analyzing.value = true

  setTimeout(() => {
    const totalEnergy = energyInfo.value.electricity + energyInfo.value.gas * 10 + energyInfo.value.water * 0.5
    const totalCost = energyInfo.value.electricityCost + energyInfo.value.gas * 2.5 + energyInfo.value.water * 5
    const carbonEmission = energyInfo.value.electricity * 0.6 + energyInfo.value.gas * 2.2 + energyInfo.value.water * 0.1
    const efficiency = Math.max(0, Math.min(100, 100 - (totalEnergy / homeInfo.value.area * 0.5)))

    energyAnalysis.value = {
      totalEnergy: totalEnergy.toFixed(1),
      totalCost: totalCost.toFixed(0),
      carbonEmission: carbonEmission.toFixed(1),
      efficiency: efficiency.toFixed(0),
      suggestions: [
        {
          icon: '💡',
          title: '更换LED灯泡',
          priority: '高优先级',
          priorityClass: 'high',
          description: '将传统白炽灯和荧光灯更换为LED灯泡，可节省80%以上的照明能耗。',
          saving: 15,
          costSaving: 25,
          paybackPeriod: '6个月'
        },
        {
          icon: '🌡️',
          title: '优化空调使用',
          priority: '高优先级',
          priorityClass: 'high',
          description: '合理设置空调温度（夏季26℃，冬季20℃），使用节能模式，定期清洗滤网。',
          saving: 20,
          costSaving: 40,
          paybackPeriod: '立即生效'
        },
        {
          icon: '❄️',
          title: '升级热水器',
          priority: '中优先级',
          priorityClass: 'medium',
          description: '更换为节能型热水器或太阳能热水器，可显著减少热水能耗。',
          saving: 25,
          costSaving: 35,
          paybackPeriod: '18个月'
        },
        {
          icon: '📺',
          title: '优化家电使用',
          priority: '中优先级',
          priorityClass: 'medium',
          description: '关闭不使用的电器，使用节能模式，定期维护家电。',
          saving: 10,
          costSaving: 15,
          paybackPeriod: '立即生效'
        },
        {
          icon: '🪟',
          title: '改善保温性能',
          priority: '低优先级',
          priorityClass: 'low',
          description: '检查门窗密封，使用保温窗帘，改善墙体保温性能。',
          saving: 12,
          costSaving: 20,
          paybackPeriod: '12个月'
        }
      ]
    }

    // 更新图表
    updateChart()

    analyzing.value = false
  }, 1500)
}

const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  if (energyChart.value) {
    chartInstance.value = new Chart(energyChart.value, {
      type: 'doughnut',
      data: {
        labels: ['照明', '空调', '热水器', '其他电器'],
        datasets: [{
          data: [30, 40, 15, 15],
          backgroundColor: [
            '#f59e0b',
            '#3b82f6',
            '#10b981',
            '#8b5cf6'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
}

const resetForm = () => {
  homeInfo.value = {
    area: 100,
    type: 'apartment',
    members: 3,
    year: '2010-2019'
  }
  energyInfo.value = {
    electricity: 200,
    gas: 30,
    water: 10,
    electricityCost: 150
  }
  energyAnalysis.value = null
  simulationResult.value = null
}

const implementSuggestion = (suggestion) => {
  alert(`已标记实施建议：${suggestion.title}`)
}

const simulateSuggestion = (suggestion) => {
  const currentEnergy = parseFloat(energyAnalysis.value.totalEnergy)
  const currentCost = parseFloat(energyAnalysis.value.totalCost)
  const currentCarbon = parseFloat(energyAnalysis.value.carbonEmission)

  const savingPercentage = suggestion.saving / 100
  const optimizedEnergy = currentEnergy * (1 - savingPercentage)
  const optimizedCost = currentCost * (1 - savingPercentage)
  const optimizedCarbon = currentCarbon * (1 - savingPercentage)

  simulationResult.value = {
    current: {
      energy: currentEnergy.toFixed(1),
      cost: currentCost.toFixed(0),
      carbon: currentCarbon.toFixed(1)
    },
    optimized: {
      energy: optimizedEnergy.toFixed(1),
      cost: optimizedCost.toFixed(0),
      carbon: optimizedCarbon.toFixed(1)
    },
    saving: {
      energy: (currentEnergy - optimizedEnergy).toFixed(1),
      percentage: suggestion.saving,
      cost: (currentCost - optimizedCost).toFixed(0),
      carbon: (currentCarbon - optimizedCarbon).toFixed(1),
      annual: ((currentCost - optimizedCost) * 12).toFixed(0)
    }
  }
}

onMounted(() => {
  // 初始化图表
  if (energyAnalysis.value) {
    updateChart()
  }
})
</script>

<style scoped>
.home-energy-optimization {
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

.home-info-card,
.energy-info-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.home-info-card h3,
.energy-info-card h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.appliances-section {
  margin-top: 30px;
}

.appliances-section h4 {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}

.appliances-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.appliance-item {
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.appliance-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.appliance-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
}

.appliance-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-item label {
  font-size: 12px;
  color: #666;
  flex-shrink: 0;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 30px;
}

.analysis-result-section {
  margin-top: 40px;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.overview-card,
.chart-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.overview-card h4,
.chart-card h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
}

.stat-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #10b981;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.chart-container {
  height: 300px;
}

.suggestions-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.suggestions-section h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.suggestion-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.suggestion-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.suggestion-header {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8fafc;
}

.suggestion-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.suggestion-header h5 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.suggestion-priority {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.suggestion-priority.high {
  background: #ef4444;
}

.suggestion-priority.medium {
  background: #f59e0b;
}

.suggestion-priority.low {
  background: #10b981;
}

.suggestion-content {
  padding: 15px;
}

.suggestion-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 15px;
}

.suggestion-benefits {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.benefit-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.benefit-label {
  color: #666;
}

.benefit-value {
  font-weight: 600;
  color: #10b981;
}

.suggestion-actions {
  display: flex;
  gap: 10px;
}

.simulation-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.simulation-section h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.simulation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.simulation-card {
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
}

.simulation-card.optimized {
  border-color: #10b981;
  background: #f0fdf4;
}

.simulation-card h5 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.simulation-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sim-stat {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.sim-label {
  color: #666;
}

.sim-value {
  font-weight: 600;
  color: #333;
}

.sim-value.eco {
  color: #10b981;
}

.simulation-comparison {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.comparison-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
}

.comparison-label {
  font-size: 14px;
  color: #666;
}

.comparison-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.comparison-value.positive {
  color: #10b981;
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
  
  .home-info-card,
  .energy-info-card {
    padding: 20px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .appliances-grid {
    grid-template-columns: 1fr;
  }
  
  .result-grid {
    grid-template-columns: 1fr;
  }
  
  .overview-stats {
    grid-template-columns: 1fr;
  }
  
  .suggestions-grid {
    grid-template-columns: 1fr;
  }
  
  .simulation-grid {
    grid-template-columns: 1fr;
  }
  
  .simulation-comparison {
    grid-template-columns: 1fr;
  }
}
</style>