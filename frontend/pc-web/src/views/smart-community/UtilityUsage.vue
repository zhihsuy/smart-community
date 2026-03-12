<template>
  <div class="utility-usage-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📊 用量分析</h1>
      <p class="subtitle">详细的水电用量分析和趋势</p>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="表具类型">
          <el-select v-model="filterForm.meterType" placeholder="选择类型">
            <el-option label="全部" value="" />
            <el-option label="电表" value="electric" />
            <el-option label="水表" value="water" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-select v-model="filterForm.period" placeholder="选择时间" @change="loadData">
            <el-option label="近7天" value="7d" />
            <el-option label="近30天" value="30d" />
            <el-option label="近3个月" value="3m" />
            <el-option label="近6个月" value="6m" />
            <el-option label="近1年" value="1y" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="filterForm.period === 'custom'" label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 280px"
            @change="loadData"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据概览 -->
    <div class="overview-grid">
      <el-card class="overview-card">
        <div class="overview-item">
          <div class="overview-value">{{ stats.total_usage }} {{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}</div>
          <div class="overview-label">总用量</div>
        </div>
      </el-card>
      <el-card class="overview-card">
        <div class="overview-item">
          <div class="overview-value">¥{{ stats.total_cost }}</div>
          <div class="overview-label">总费用</div>
        </div>
      </el-card>
      <el-card class="overview-card">
        <div class="overview-item">
          <div class="overview-value">{{ stats.avg_daily_usage }} {{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}</div>
          <div class="overview-label">日均用量</div>
        </div>
      </el-card>
      <el-card class="overview-card">
        <div class="overview-item">
          <div class="overview-value" :class="stats.change > 0 ? 'increase' : 'decrease'">
            {{ stats.change > 0 ? '+' : '' }}{{ stats.change }}%
          </div>
          <div class="overview-label">同比变化</div>
        </div>
      </el-card>
    </div>

    <!-- 用量趋势图 -->
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>📈 用量趋势</span>
          <el-select v-model="chartType" size="small" @change="loadData">
            <el-option label="按日" value="day" />
            <el-option label="按月" value="month" />
            <el-option label="按年" value="year" />
          </el-select>
        </div>
      </template>
      <div class="chart-container">
        <el-empty v-if="!usageData.length" description="暂无数据" />
        <div v-else>
          <el-chart>
            <el-line-chart 
              :data="usageData" 
              x-field="date" 
              y-field="value"
              :smooth="true"
            >
              <el-tooltip :show-content="true" />
              <el-line-chart-series name="用量" />
            </el-line-chart>
          </el-chart>
        </div>
      </div>
    </el-card>

    <!-- 用量详情 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>📋 用量详情</span>
          <el-button type="primary" @click="exportData">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </div>
      </template>
      <el-table :data="usageDetails" style="width: 100%">
        <el-table-column prop="date" label="日期" width="150" />
        <el-table-column prop="usage" label="用量" width="120">
          <template #default="scope">
            {{ scope.row.usage }} {{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}
          </template>
        </el-table-column>
        <el-table-column prop="cost" label="费用" width="100">
          <template #default="scope">
            ¥{{ scope.row.cost }}
          </template>
        </el-table-column>
        <el-table-column prop="unit_price" label="单价" width="100">
          <template #default="scope">
            ¥{{ scope.row.unit_price }}/{{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}
          </template>
        </el-table-column>
        <el-table-column prop="peak_hours" label="峰时用量" width="120">
          <template #default="scope">
            {{ scope.row.peak_hours || 0 }} {{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}
          </template>
        </el-table-column>
        <el-table-column prop="valley_hours" label="谷时用量" width="120">
          <template #default="scope">
            {{ scope.row.valley_hours || 0 }} {{ filterForm.meterType === 'electric' ? 'kWh' : 'm³' }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination" style="margin-top: 20px">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 节能建议 -->
    <el-card class="suggestion-card">
      <template #header>
        <div class="card-header">
          <span>💡 节能建议</span>
        </div>
      </template>
      <div class="suggestions">
        <el-alert
          v-for="suggestion in suggestions"
          :key="suggestion.id"
          :title="suggestion.title"
          :description="suggestion.content"
          type="success"
          :closable="false"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Search, Download } from '@element-plus/icons-vue'

const filterForm = ref({
  meterType: 'electric',
  period: '30d',
  dateRange: null
})

const chartType = ref('day')
const usageData = ref([])
const usageDetails = ref([])
const stats = ref({
  total_usage: 0,
  total_cost: 0,
  avg_daily_usage: 0,
  change: 0
})
const pagination = ref({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

const suggestions = ref([
  {
    id: 1,
    title: '合理使用电器',
    content: '建议在不需要使用电器时及时关闭电源，减少待机能耗'
  },
  {
    id: 2,
    title: '使用节能电器',
    content: '更换LED灯泡，使用节能型家电，可减少30%的用电量'
  },
  {
    id: 3,
    title: '优化用水习惯',
    content: '修复漏水龙头，使用节水型淋浴喷头，可减少20%的用水量'
  }
])

// 加载数据
const loadData = async () => {
  try {
    const params = new URLSearchParams()
    params.append('meter_type', filterForm.value.meterType)
    params.append('period', filterForm.value.period)
    params.append('chart_type', chartType.value)
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (filterForm.value.period === 'custom' && filterForm.value.dateRange) {
      params.append('start_date', filterForm.value.dateRange[0])
      params.append('end_date', filterForm.value.dateRange[1])
    }

    const response = await fetch(`/api/v1/pc/utility/usage?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      usageData.value = result.data?.chart_data || []
      usageDetails.value = result.data?.list || []
      stats.value = result.data?.statistics || {}
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadData()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadData()
}

const exportData = async () => {
  try {
    const params = new URLSearchParams()
    params.append('meter_type', filterForm.value.meterType)
    params.append('period', filterForm.value.period)
    
    if (filterForm.value.period === 'custom' && filterForm.value.dateRange) {
      params.append('start_date', filterForm.value.dateRange[0])
      params.append('end_date', filterForm.value.dateRange[1])
    }

    const response = await fetch(`/api/v1/pc/utility/export?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    
    if (response.ok) {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `水电用量_${new Date().toISOString().split('T')[0]}.xlsx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
      ElMessage.success('导出成功')
    } else {
      ElMessage.error('导出失败')
    }
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.utility-usage-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.page-header h1 {
  margin: 10px 0 5px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.filter-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.overview-card {
  border-radius: 8px;
  text-align: center;
}

.overview-item {
  padding: 20px;
}

.overview-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.overview-label {
  color: #909399;
  font-size: 14px;
}

.overview-value.increase {
  color: #F56C6C;
}

.overview-value.decrease {
  color: #67C23A;
}

.chart-card,
.detail-card,
.suggestion-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.chart-container {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (max-width: 768px) {
  .filter-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>
