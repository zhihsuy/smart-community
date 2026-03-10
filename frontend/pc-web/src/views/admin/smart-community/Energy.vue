<template>
  <AdminLayout>
    <div class="energy-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>能耗管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="能耗记录" name="consumptions">
            <div class="mb-4">
              <el-button type="primary" @click="openConsumptionDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增能耗记录
              </el-button>
            </div>
            
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="searchForm" class="mb-4">
                <el-form-item label="类型">
                  <el-select v-model="searchForm.type" placeholder="选择类型">
                    <el-option label="全部" value="" />
                    <el-option label=" electricity" value="electricity" />
                    <el-option label=" water" value="water" />
                  </el-select>
                </el-form-item>
                <el-form-item label="日期范围">
                  <el-date-picker
                    v-model="dateRange"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    style="width: 250px"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchConsumptions">查询</el-button>
                  <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="consumptions" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="user_name" label="住户" />
              <el-table-column prop="building_name" label="楼栋" />
              <el-table-column prop="room_number" label="房号" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.type === 'electricity' ? 'primary' : 'success'">
                    {{ scope.row.type === 'electricity' ? ' electricity' : ' water' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="usage" label="用量" width="100">
                <template #default="scope">
                  {{ scope.row.usage }} {{ scope.row.unit }}
                </template>
              </el-table-column>
              <el-table-column prop="cost" label="费用" width="100">
                <template #default="scope">
                  ¥{{ scope.row.cost.toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column prop="reading_date" label="抄表日期" width="120" />
              <el-table-column prop="meter_id" label="表计ID" width="150" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="viewConsumption(scope.row)">
                    <el-icon><i-ep-view /></el-icon>
                    查看
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteConsumption(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="total > 0">
              <el-pagination
                v-model:current-page="page"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="表计管理" name="meters">
            <div class="mb-4">
              <el-button type="primary" @click="openMeterDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增表计
              </el-button>
            </div>
            
            <el-table :data="meters" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="meter_id" label="表计ID" width="150" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.type === 'electricity' ? 'primary' : 'success'">
                    {{ scope.row.type === 'electricity' ? ' electricity' : ' water' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="user_name" label="住户" />
              <el-table-column prop="building_name" label="楼栋" />
              <el-table-column prop="room_number" label="房号" />
              <el-table-column prop="last_reading" label="上次读数" width="100" />
              <el-table-column prop="last_reading_date" label="上次抄表日期" width="150" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '正常' : '停用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="updateMeterReading(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    更新读数
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="能耗分析" name="analysis">
            <div class="mb-4">
              <el-form :inline="true" :model="analysisForm" class="mb-4">
                <el-form-item label="日期范围">
                  <el-date-picker
                    v-model="analysisDateRange"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    style="width: 250px"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="loadAnalysis">查询</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-row :gutter="20" class="mb-4">
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-light /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总用电量</div>
                      <div class="stat-value">{{ analysis.total_electricity }} kWh</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-water /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总用水量</div>
                      <div class="stat-value">{{ analysis.total_water }} m³</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #E6A23C">
                      <el-icon><i-ep-data-analysis /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">月均用电量</div>
                      <div class="stat-value">{{ analysis.avg_electricity_per_month }} kWh</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #909399">
                      <el-icon><i-ep-data-line /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">月均用水量</div>
                      <div class="stat-value">{{ analysis.avg_water_per_month }} m³</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <el-card shadow="hover" class="mb-4">
              <template #header>
                <span>能耗趋势</span>
              </template>
              <div class="chart-container">
                <el-chart>
                  <el-line
                    :data="trendData"
                    x-field="month"
                    :y-field="['electricity', 'water']"
                  />
                </el-chart>
              </div>
            </el-card>
            
            <el-card shadow="hover">
              <template #header>
                <span>节能建议</span>
              </template>
              <el-list>
                <el-list-item v-for="(suggestion, index) in analysis.saving_suggestions" :key="index">
                  <template #prefix>
                    <el-icon class="suggestion-icon"><i-ep-lightbulb /></el-icon>
                  </template>
                  {{ suggestion }}
                </el-list-item>
              </el-list>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="consumptionDialogVisible"
        :title="consumptionDialogTitle"
        width="600px"
      >
        <el-form :model="consumptionForm" :rules="consumptionRules" ref="consumptionFormRef" label-width="100px" status-icon>
          <el-form-item label="住户" prop="user_id">
            <el-select v-model="consumptionForm.user_id" placeholder="选择住户">
              <el-option 
                v-for="user in users" 
                :key="user.id" 
                :label="user.username" 
                :value="user.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="楼栋" prop="building_id">
            <el-select v-model="consumptionForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.building_name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="consumptionForm.type" placeholder="选择类型">
              <el-option label=" electricity" value="electricity" />
              <el-option label=" water" value="water" />
            </el-select>
          </el-form-item>
          <el-form-item label="用量" prop="usage">
            <el-input-number v-model="consumptionForm.usage" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="单位" prop="unit">
            <el-input v-model="consumptionForm.unit" placeholder="如：kWh、m³" />
          </el-form-item>
          <el-form-item label="费用" prop="cost">
            <el-input-number v-model="consumptionForm.cost" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="抄表日期" prop="reading_date">
            <el-date-picker v-model="consumptionForm.reading_date" type="date" placeholder="选择抄表日期" style="width: 100%" />
          </el-form-item>
          <el-form-item label="表计ID" prop="meter_id">
            <el-input v-model="consumptionForm.meter_id" placeholder="请输入表计ID" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="consumptionForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="consumptionDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveConsumption">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="meterDialogVisible"
        :title="meterDialogTitle"
        width="500px"
      >
        <el-form :model="meterForm" :rules="meterRules" ref="meterFormRef" label-width="100px" status-icon>
          <el-form-item label="表计ID" prop="meter_id">
            <el-input v-model="meterForm.meter_id" placeholder="请输入表计ID" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="meterForm.type" placeholder="选择类型">
              <el-option label=" electricity" value="electricity" />
              <el-option label=" water" value="water" />
            </el-select>
          </el-form-item>
          <el-form-item label="住户" prop="user_id">
            <el-select v-model="meterForm.user_id" placeholder="选择住户">
              <el-option 
                v-for="user in users" 
                :key="user.id" 
                :label="user.username" 
                :value="user.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="楼栋" prop="building_id">
            <el-select v-model="meterForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.building_name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="安装日期" prop="install_date">
            <el-date-picker v-model="meterForm.install_date" type="date" placeholder="选择安装日期" style="width: 100%" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="meterForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="meterDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveMeter">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="readingDialogVisible"
        title="更新表计读数"
        width="400px"
      >
        <el-form :model="readingForm" ref="readingFormRef" label-width="100px" status-icon>
          <el-form-item label="当前读数" prop="reading">
            <el-input-number v-model="readingForm.reading" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="读数日期" prop="reading_date">
            <el-date-picker v-model="readingForm.reading_date" type="date" placeholder="选择读数日期" style="width: 100%" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="readingDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveReading">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const activeTab = ref('consumptions')
const consumptions = ref([])
const meters = ref([])
const users = ref([])
const buildings = ref([])
const analysis = ref({
  total_electricity: 0,
  total_water: 0,
  avg_electricity_per_month: 0,
  avg_water_per_month: 0,
  electricity_trend: [],
  water_trend: [],
  saving_suggestions: []
})
const trendData = ref([])

const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const searchForm = ref({
  type: ''
})

const dateRange = ref([])
const analysisForm = ref({})
const analysisDateRange = ref([])

const consumptionDialogVisible = ref(false)
const consumptionDialogTitle = ref('新增能耗记录')
const consumptionForm = ref({
  user_id: null,
  building_id: null,
  type: 'electricity',
  usage: 0,
  unit: '',
  cost: 0,
  reading_date: null,
  meter_id: '',
  remark: ''
})

const meterDialogVisible = ref(false)
const meterDialogTitle = ref('新增表计')
const meterForm = ref({
  meter_id: '',
  type: 'electricity',
  user_id: null,
  building_id: null,
  install_date: null,
  remark: ''
})

const readingDialogVisible = ref(false)
const readingForm = ref({
  meter_id: null,
  reading: 0,
  reading_date: null
})

const consumptionRules = {
  user_id: [{ required: true, message: '请选择住户', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  usage: [{ required: true, message: '请输入用量', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  cost: [{ required: true, message: '请输入费用', trigger: 'blur' }],
  reading_date: [{ required: true, message: '请选择抄表日期', trigger: 'change' }],
  meter_id: [{ required: true, message: '请输入表计ID', trigger: 'blur' }]
}

const meterRules = {
  meter_id: [{ required: true, message: '请输入表计ID', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  user_id: [{ required: true, message: '请选择住户', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  install_date: [{ required: true, message: '请选择安装日期', trigger: 'change' }]
}

const handleTabChange = (tab) => {
  if (tab === 'consumptions') {
    loadConsumptions()
  } else if (tab === 'meters') {
    loadMeters()
  } else if (tab === 'analysis') {
    loadAnalysis()
  }
}

const loadConsumptions = async () => {
  try {
    const params = {
      page: page.value,
      pageSize: pageSize.value,
      type: searchForm.value.type
    }
    
    if (dateRange.value.length) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    
    const response = await axios.get('/api/v1/pc/energy/consumptions', { params })
    consumptions.value = response.data.data.list
    total.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载能耗记录列表失败')
  }
}

const loadMeters = async () => {
  try {
    const response = await axios.get('/api/v1/pc/energy/meters')
    meters.value = response.data.data
  } catch (error) {
    ElMessage.error('加载表计列表失败')
  }
}

const loadAnalysis = async () => {
  try {
    const params = {}
    
    if (analysisDateRange.value.length) {
      params.start_date = analysisDateRange.value[0]
      params.end_date = analysisDateRange.value[1]
    }
    
    const response = await axios.get('/api/v1/pc/energy/consumptions/analysis', { params })
    analysis.value = response.data.data
    
    // 生成趋势数据
    const months = ['1月', '2月', '3月', '4月', '5月', '6月']
    trendData.value = months.map((month, index) => ({
      month,
      electricity: analysis.value.electricity_trend[index] || 0,
      water: analysis.value.water_trend[index] || 0
    }))
  } catch (error) {
    ElMessage.error('加载能耗分析失败')
  }
}

const openConsumptionDialog = () => {
  consumptionDialogTitle.value = '新增能耗记录'
  consumptionForm.value = {
    user_id: null,
    building_id: null,
    type: 'electricity',
    usage: 0,
    unit: '',
    cost: 0,
    reading_date: null,
    meter_id: '',
    remark: ''
  }
  consumptionDialogVisible.value = true
}

const saveConsumption = async () => {
  try {
    await axios.post('/api/v1/pc/energy/consumptions', consumptionForm.value)
    ElMessage.success('新增能耗记录成功')
    consumptionDialogVisible.value = false
    loadConsumptions()
  } catch (error) {
    ElMessage.error('保存能耗记录失败')
  }
}

const viewConsumption = (consumption) => {
  ElMessageBox.alert(
    `<div>
      <p><strong>住户：</strong>${consumption.user_name}</p>
      <p><strong>楼栋：</strong>${consumption.building_name}</p>
      <p><strong>房号：</strong>${consumption.room_number}</p>
      <p><strong>类型：</strong>${consumption.type === 'electricity' ? ' electricity' : ' water'}</p>
      <p><strong>用量：</strong>${consumption.usage} ${consumption.unit}</p>
      <p><strong>费用：</strong>¥${consumption.cost.toFixed(2)}</p>
      <p><strong>抄表日期：</strong>${consumption.reading_date}</p>
      <p><strong>表计ID：</strong>${consumption.meter_id}</p>
      <p><strong>备注：</strong>${consumption.remark || '无'}</p>
    </div>`,
    '能耗详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

const deleteConsumption = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该能耗记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/energy/consumptions/${id}`)
    ElMessage.success('删除成功')
    loadConsumptions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const openMeterDialog = () => {
  meterDialogTitle.value = '新增表计'
  meterForm.value = {
    meter_id: '',
    type: 'electricity',
    user_id: null,
    building_id: null,
    install_date: null,
    remark: ''
  }
  meterDialogVisible.value = true
}

const saveMeter = async () => {
  try {
    await axios.post('/api/v1/pc/energy/meters', meterForm.value)
    ElMessage.success('新增表计成功')
    meterDialogVisible.value = false
    loadMeters()
  } catch (error) {
    ElMessage.error('保存表计失败')
  }
}

const updateMeterReading = (meter) => {
  readingForm.value = {
    meter_id: meter.id,
    reading: meter.last_reading || 0,
    reading_date: new Date()
  }
  readingDialogVisible.value = true
}

const saveReading = async () => {
  try {
    await axios.put(`/api/v1/pc/energy/meters/${readingForm.value.meter_id}/reading`, readingForm.value)
    ElMessage.success('更新读数成功')
    readingDialogVisible.value = false
    loadMeters()
  } catch (error) {
    ElMessage.error('更新读数失败')
  }
}

const searchConsumptions = () => {
  page.value = 1
  loadConsumptions()
}

const resetSearch = () => {
  searchForm.value = {
    type: ''
  }
  dateRange.value = []
  page.value = 1
  loadConsumptions()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadConsumptions()
}

const handleCurrentChange = (currentPage) => {
  page.value = currentPage
  loadConsumptions()
}

onMounted(() => {
  loadConsumptions()
  loadMeters()
  loadAnalysis()
})
</script>

<style scoped>
.energy-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}

.search-filter {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 30px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.chart-container {
  height: 400px;
}

.suggestion-icon {
  color: #E6A23C;
  margin-right: 10px;
}
</style>
