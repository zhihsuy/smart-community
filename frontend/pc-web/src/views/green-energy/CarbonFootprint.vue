<template>
  <div class="carbon-footprint">
    <div class="page-header">
      <h1>🌍 碳足迹计算器</h1>
      <p>计算您的日常生活碳排放量，为环保贡献力量</p>
    </div>

    <div class="content-section">
      <div class="calculator-card">
        <div class="calculator-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>

        <div class="calculator-content">
          <!-- 交通部分 -->
          <div v-if="activeTab === 'transport'" class="tab-content">
            <h3>🚗 交通出行</h3>
            <div class="form-group">
              <label>出行方式</label>
              <el-select v-model="transport.type" placeholder="请选择出行方式" class="w-full">
                <el-option label="私家车" value="car" />
                <el-option label="公共汽车" value="bus" />
                <el-option label="地铁" value="subway" />
                <el-option label="自行车" value="bicycle" />
                <el-option label="步行" value="walk" />
                <el-option label="飞机" value="plane" />
              </el-select>
            </div>
            <div class="form-group">
              <label>每周出行次数</label>
              <el-input-number v-model="transport.frequency" :min="1" :max="7" class="w-full" />
            </div>
            <div class="form-group">
              <label>每次出行距离 (公里)</label>
              <el-input-number v-model="transport.distance" :min="0.1" :step="0.1" class="w-full" />
            </div>
            <div class="form-group">
              <label>车辆类型 (如果选择私家车)</label>
              <el-select v-model="transport.vehicleType" placeholder="请选择车辆类型" class="w-full">
                <el-option label="燃油车" value="gasoline" />
                <el-option label="混合动力车" value="hybrid" />
                <el-option label="电动车" value="electric" />
              </el-select>
            </div>
          </div>

          <!-- 饮食部分 -->
          <div v-if="activeTab === 'diet'" class="tab-content">
            <h3>🍎 饮食消费</h3>
            <div class="form-group">
              <label>每周肉类消费 (公斤)</label>
              <el-input-number v-model="diet.meat" :min="0" :step="0.1" class="w-full" />
            </div>
            <div class="form-group">
              <label>每周素食消费 (公斤)</label>
              <el-input-number v-model="diet.vegetables" :min="0" :step="0.1" class="w-full" />
            </div>
            <div class="form-group">
              <label>每周本地食材消费比例 (%)</label>
              <el-input-number v-model="diet.localFood" :min="0" :max="100" class="w-full" />
            </div>
            <div class="form-group">
              <label>每周外卖次数</label>
              <el-input-number v-model="diet.takeaway" :min="0" class="w-full" />
            </div>
          </div>

          <!-- 能源部分 -->
          <div v-if="activeTab === 'energy'" class="tab-content">
            <h3>💡 能源使用</h3>
            <div class="form-group">
              <label>每月 electricity 消耗 (度)</label>
              <el-input-number v-model="energy.electricity" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>每月天然气消耗 (立方米)</label>
              <el-input-number v-model="energy.gas" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>每月水消耗 (吨)</label>
              <el-input-number v-model="energy.water" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>家居节能措施</label>
              <el-checkbox-group v-model="energy.measures">
                <el-checkbox label="LED灯泡" />
                <el-checkbox label="节能家电" />
                <el-checkbox label="太阳能热水器" />
                <el-checkbox label="智能家居系统" />
              </el-checkbox-group>
            </div>
          </div>

          <!-- 其他部分 -->
          <div v-if="activeTab === 'other'" class="tab-content">
            <h3>📦 其他消费</h3>
            <div class="form-group">
              <label>每月网购次数</label>
              <el-input-number v-model="other.onlineShopping" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>每月纸质用品消费 (件)</label>
              <el-input-number v-model="other.paperProducts" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>每月塑料制品消费 (件)</label>
              <el-input-number v-model="other.plasticProducts" :min="0" class="w-full" />
            </div>
            <div class="form-group">
              <label>回收习惯</label>
              <el-checkbox-group v-model="other.recycling">
                <el-checkbox label="垃圾分类" />
                <el-checkbox label="纸张回收" />
                <el-checkbox label="塑料回收" />
                <el-checkbox label="电子废弃物回收" />
              </el-checkbox-group>
            </div>
          </div>
        </div>

        <div class="calculator-footer">
          <el-button type="primary" @click="calculateCarbonFootprint">
            <el-icon><DataAnalysis /></el-icon>
            计算碳足迹
          </el-button>
        </div>
      </div>

      <div v-if="result" class="result-section">
        <div class="result-card">
          <div class="result-header">
            <h3>计算结果</h3>
          </div>
          <div class="result-content">
            <div class="carbon-value">
              <div class="value">{{ result.total }} <span class="unit">kg CO₂e/月</span></div>
              <div class="label">您的月度碳足迹</div>
            </div>
            <div class="carbon-breakdown">
              <h4>碳排放分布</h4>
              <div class="breakdown-chart">
                <canvas ref="chartRef"></canvas>
              </div>
            </div>
            <div class="recommendations">
              <h4>减少碳排放建议</h4>
              <ul class="recommendation-list">
                <li v-for="(recommendation, index) in result.recommendations" :key="index">
                  {{ recommendation }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { DataAnalysis } from '@element-plus/icons-vue'
import Chart from 'chart.js/auto'

const activeTab = ref('transport')
const chartRef = ref(null)
const chart = ref(null)
const result = ref(null)

const tabs = [
  { id: 'transport', name: '交通出行', icon: '🚗' },
  { id: 'diet', name: '饮食消费', icon: '🍎' },
  { id: 'energy', name: '能源使用', icon: '💡' },
  { id: 'other', name: '其他消费', icon: '📦' }
]

const transport = ref({
  type: 'car',
  frequency: 5,
  distance: 10,
  vehicleType: 'gasoline'
})

const diet = ref({
  meat: 2,
  vegetables: 5,
  localFood: 50,
  takeaway: 3
})

const energy = ref({
  electricity: 100,
  gas: 10,
  water: 5,
  measures: []
})

const other = ref({
  onlineShopping: 5,
  paperProducts: 10,
  plasticProducts: 15,
  recycling: []
})

const calculateCarbonFootprint = () => {
  // 计算交通碳排放
  const transportEmission = calculateTransportEmission()
  
  // 计算饮食碳排放
  const dietEmission = calculateDietEmission()
  
  // 计算能源碳排放
  const energyEmission = calculateEnergyEmission()
  
  // 计算其他碳排放
  const otherEmission = calculateOtherEmission()
  
  // 总碳排放
  const total = transportEmission + dietEmission + energyEmission + otherEmission
  
  // 生成建议
  const recommendations = generateRecommendations(total, transportEmission, dietEmission, energyEmission, otherEmission)
  
  result.value = {
    total: total.toFixed(2),
    transport: transportEmission.toFixed(2),
    diet: dietEmission.toFixed(2),
    energy: energyEmission.toFixed(2),
    other: otherEmission.toFixed(2),
    recommendations
  }
  
  // 更新图表
  updateChart()
}

const calculateTransportEmission = () => {
  const factors = {
    car: {
      gasoline: 0.2,
      hybrid: 0.1,
      electric: 0.05
    },
    bus: 0.05,
    subway: 0.03,
    bicycle: 0,
    walk: 0,
    plane: 0.5
  }
  
  if (transport.value.type === 'car') {
    return transport.value.frequency * transport.value.distance * factors.car[transport.value.vehicleType] * 4
  } else {
    return transport.value.frequency * transport.value.distance * factors[transport.value.type] * 4
  }
}

const calculateDietEmission = () => {
  // 肉类碳排放因子：10kg CO₂e/kg
  // 素食碳排放因子：2kg CO₂e/kg
  // 本地食材减少30%碳排放
  const meatEmission = diet.value.meat * 10
  const vegetableEmission = diet.value.vegetables * 2
  const localReduction = (meatEmission + vegetableEmission) * (diet.value.localFood / 100) * 0.3
  const takeawayEmission = diet.value.takeaway * 0.5
  
  return (meatEmission + vegetableEmission - localReduction + takeawayEmission) * 4
}

const calculateEnergyEmission = () => {
  // 电力碳排放因子：0.6kg CO₂e/度
  // 天然气碳排放因子：2.2kg CO₂e/立方米
  // 水碳排放因子：0.1kg CO₂e/吨
  // 节能措施减少10-30%碳排放
  const electricityEmission = energy.value.electricity * 0.6
  const gasEmission = energy.value.gas * 2.2
  const waterEmission = energy.value.water * 0.1
  const savingFactor = 1 - (energy.value.measures.length * 0.05)
  
  return (electricityEmission + gasEmission + waterEmission) * savingFactor
}

const calculateOtherEmission = () => {
  // 网购碳排放因子：0.5kg CO₂e/次
  // 纸质用品碳排放因子：0.2kg CO₂e/件
  // 塑料制品碳排放因子：0.3kg CO₂e/件
  // 回收减少20-40%碳排放
  const onlineShoppingEmission = other.value.onlineShopping * 0.5
  const paperProductsEmission = other.value.paperProducts * 0.2
  const plasticProductsEmission = other.value.plasticProducts * 0.3
  const recyclingReduction = (onlineShoppingEmission + paperProductsEmission + plasticProductsEmission) * (other.value.recycling.length * 0.05)
  
  return onlineShoppingEmission + paperProductsEmission + plasticProductsEmission - recyclingReduction
}

const generateRecommendations = (total, transportEmission, dietEmission, energyEmission, otherEmission) => {
  const recommendations = []
  
  if (transportEmission > total * 0.3) {
    recommendations.push('考虑增加公共交通、自行车或步行的使用频率')
    recommendations.push('如果使用私家车，尽量选择拼车或减少不必要的出行')
  }
  
  if (dietEmission > total * 0.3) {
    recommendations.push('减少肉类消费，增加素食比例')
    recommendations.push('选择本地、当季的食材，减少运输碳排放')
    recommendations.push('减少外卖次数，自己烹饪更环保')
  }
  
  if (energyEmission > total * 0.3) {
    recommendations.push('使用LED灯泡和节能家电')
    recommendations.push('合理设置空调温度，夏季不低于26℃，冬季不高于20℃')
    recommendations.push('关闭不使用的电器，避免待机能耗')
  }
  
  if (otherEmission > total * 0.2) {
    recommendations.push('减少网购频率，选择环保包装')
    recommendations.push('使用可重复使用的购物袋和水杯')
    recommendations.push('积极参与垃圾分类和回收')
  }
  
  if (total < 100) {
    recommendations.push('您的碳足迹低于平均水平，继续保持！')
  } else if (total < 200) {
    recommendations.push('您的碳足迹在平均水平左右，还有改进空间')
  } else {
    recommendations.push('您的碳足迹高于平均水平，需要采取更多措施减少碳排放')
  }
  
  return recommendations
}

const updateChart = () => {
  if (chart.value) {
    chart.value.destroy()
  }
  
  if (chartRef.value) {
    chart.value = new Chart(chartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['交通出行', '饮食消费', '能源使用', '其他消费'],
        datasets: [{
          data: [
            parseFloat(result.value.transport),
            parseFloat(result.value.diet),
            parseFloat(result.value.energy),
            parseFloat(result.value.other)
          ],
          backgroundColor: [
            '#3b82f6',
            '#10b981',
            '#f59e0b',
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

onMounted(() => {
  // 初始化图表
  if (result.value) {
    updateChart()
  }
})

watch(() => result.value, () => {
  if (result.value) {
    updateChart()
  }
})
</script>

<style scoped>
.carbon-footprint {
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

.calculator-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
  overflow: hidden;
}

.calculator-tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.calculator-tabs button {
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

.calculator-tabs button:hover {
  background: #f3f4f6;
}

.calculator-tabs button.active {
  background: #10b981;
  color: white;
}

.calculator-content {
  padding: 30px;
}

.tab-content h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 20px;
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

.calculator-footer {
  padding: 20px 30px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: center;
}

.result-section {
  margin-top: 40px;
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

.carbon-value {
  text-align: center;
  margin-bottom: 30px;
}

.carbon-value .value {
  font-size: 48px;
  font-weight: 600;
  color: #10b981;
  margin-bottom: 10px;
}

.carbon-value .unit {
  font-size: 20px;
  color: #666;
}

.carbon-value .label {
  font-size: 16px;
  color: #666;
}

.carbon-breakdown {
  margin-bottom: 30px;
}

.carbon-breakdown h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.breakdown-chart {
  height: 300px;
}

.recommendations {
  margin-top: 30px;
}

.recommendations h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.recommendation-list {
  list-style: none;
  padding: 0;
}

.recommendation-list li {
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  position: relative;
  padding-left: 20px;
}

.recommendation-list li:before {
  content: '✅';
  position: absolute;
  left: 0;
  top: 10px;
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
  
  .calculator-content {
    padding: 20px;
  }
  
  .result-card {
    padding: 20px;
  }
  
  .carbon-value .value {
    font-size: 36px;
  }
  
  .breakdown-chart {
    height: 250px;
  }
}
</style>