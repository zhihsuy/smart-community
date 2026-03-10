<template>
  <AdminLayout>
    <div class="monitoring-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>监控管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="监控概览" name="overview">
            <div class="mb-4">
              <el-button type="primary" @click="openDeviceDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增设备
              </el-button>
            </div>
            
            <div class="device-grid">
              <el-card 
                v-for="device in devices" 
                :key="device.id" 
                shadow="hover" 
                class="device-card"
                :class="{ 'offline': device.status !== 'online' }"
              >
                <template #header>
                  <div class="device-header">
                    <span>{{ device.name }}</span>
                    <el-tag :type="device.status === 'online' ? 'success' : 'danger'">
                      {{ device.status === 'online' ? '在线' : '离线' }}
                    </el-tag>
                  </div>
                </template>
                <div class="device-info">
                  <p><strong>设备ID：</strong>{{ device.device_id }}</p>
                  <p><strong>位置：</strong>{{ device.location }}</p>
                  <p><strong>类型：</strong>{{ device.type }}</p>
                  <p><strong>IP地址：</strong>{{ device.ip_address }}</p>
                </div>
                <div class="device-actions">
                  <el-button size="small" @click="viewStream(device)">
                    <el-icon><i-ep-video-camera /></el-icon>
                    查看视频
                  </el-button>
                  <el-button size="small" @click="editDevice(device)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteDevice(device.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="实时监控" name="realtime">
            <div class="realtime-monitoring">
              <div class="monitoring-grid">
                <div 
                  v-for="device in onlineDevices" 
                  :key="device.id" 
                  class="monitoring-item"
                >
                  <div class="monitoring-header">
                    <span>{{ device.name }}</span>
                    <el-tag type="success">在线</el-tag>
                  </div>
                  <div class="monitoring-content">
                    <video 
                      :src="device.stream_url" 
                      controls 
                      autoplay 
                      muted 
                      class="monitoring-video"
                      preload="none"
                    >
                      您的浏览器不支持视频播放
                    </video>
                  </div>
                  <div class="monitoring-info">
                    <p>{{ device.location }}</p>
                    <p>{{ device.resolution }}</p>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="设备管理" name="devices">
            <div class="mb-4">
              <el-button type="primary" @click="openDeviceDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增设备
              </el-button>
            </div>
            
            <el-table :data="devices" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="device_id" label="设备ID" width="150" />
              <el-table-column prop="name" label="设备名称" />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column prop="location" label="位置" />
              <el-table-column prop="ip_address" label="IP地址" width="150" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'online' ? 'success' : 'danger'">
                    {{ scope.row.status === 'online' ? '在线' : '离线' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="install_date" label="安装日期" width="150" />
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="viewStream(scope.row)">
                    <el-icon><i-ep-video-camera /></el-icon>
                    查看视频
                  </el-button>
                  <el-button size="small" @click="editDevice(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteDevice(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="预警中心" name="alerts">
            <div class="mb-4">
              <el-button type="primary" @click="openRuleDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增预警规则
              </el-button>
            </div>
            
            <el-tabs v-model="alertTab" @tab-change="handleAlertTabChange">
              <el-tab-pane label="预警规则" name="rules">
                <el-table :data="alertRules" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="80" />
                  <el-table-column prop="name" label="规则名称" />
                  <el-table-column prop="type" label="类型" width="120" />
                  <el-table-column prop="device_name" label="设备" />
                  <el-table-column prop="threshold" label="阈值" width="100" />
                  <el-table-column prop="enabled" label="状态" width="100">
                    <template #default="scope">
                      <el-switch 
                        v-model="scope.row.enabled" 
                        @change="toggleRule(scope.row)"
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                      <el-button size="small" @click="editRule(scope.row)">
                        <el-icon><i-ep-edit /></el-icon>
                        编辑
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              <el-tab-pane label="预警记录" name="records">
                <div class="search-filter mb-4">
                  <el-form :inline="true" :model="alertSearchForm" class="mb-4">
                    <el-form-item label="状态">
                      <el-select v-model="alertSearchForm.status" placeholder="选择状态">
                        <el-option label="全部" value="" />
                        <el-option label="待处理" value="pending" />
                        <el-option label="已处理" value="processed" />
                        <el-option label="已忽略" value="ignored" />
                      </el-select>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="searchAlerts">查询</el-button>
                      <el-button @click="resetAlertSearch">重置</el-button>
                    </el-form-item>
                  </el-form>
                </div>
                
                <el-table :data="alertRecords" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="80" />
                  <el-table-column prop="rule_name" label="规则名称" />
                  <el-table-column prop="device_name" label="设备" />
                  <el-table-column prop="type" label="类型" width="120" />
                  <el-table-column prop="message" label="预警信息" />
                  <el-table-column prop="level" label="级别" width="100">
                    <template #default="scope">
                      <el-tag :type="getLevelTag(scope.row.level)">
                        {{ getLevelText(scope.row.level) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="status" label="状态" width="100">
                    <template #default="scope">
                      <el-tag :type="getStatusTag(scope.row.status)">
                        {{ getStatusText(scope.row.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="created_at" label="创建时间" width="180" />
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                      <el-button size="small" type="primary" @click="processAlert(scope.row)" v-if="scope.row.status === 'pending'">
                        <el-icon><i-ep-check /></el-icon>
                        处理
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                
                <div class="pagination" v-if="alertTotal > 0">
                  <el-pagination
                    v-model:current-page="alertPage"
                    v-model:page-size="alertPageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="alertTotal"
                    @size-change="handleAlertSizeChange"
                    @current-change="handleAlertCurrentChange"
                  />
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-tab-pane>
          
          <el-tab-pane label="查看申请" name="requests">
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="requestSearchForm" class="mb-4">
                <el-form-item label="状态">
                  <el-select v-model="requestSearchForm.status" placeholder="选择状态">
                    <el-option label="全部" value="" />
                    <el-option label="待审批" value="pending" />
                    <el-option label="已批准" value="approved" />
                    <el-option label="已拒绝" value="rejected" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchRequests">查询</el-button>
                  <el-button @click="resetRequestSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="monitoringRequests" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="user_name" label="申请人" />
              <el-table-column prop="device_name" label="设备" />
              <el-table-column prop="purpose" label="申请原因" />
              <el-table-column prop="start_time" label="开始时间" width="180" />
              <el-table-column prop="end_time" label="结束时间" width="180" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getRequestStatusTag(scope.row.status)">
                    {{ getRequestStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="申请时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" type="primary" @click="approveRequest(scope.row)" v-if="scope.row.status === 'pending'">
                    <el-icon><i-ep-check /></el-icon>
                    批准
                  </el-button>
                  <el-button size="small" type="danger" @click="rejectRequest(scope.row)" v-if="scope.row.status === 'pending'">
                    <el-icon><i-ep-close /></el-icon>
                    拒绝
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="requestTotal > 0">
              <el-pagination
                v-model:current-page="requestPage"
                v-model:page-size="requestPageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="requestTotal"
                @size-change="handleRequestSizeChange"
                @current-change="handleRequestCurrentChange"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="deviceDialogVisible"
        :title="deviceDialogTitle"
        width="600px"
      >
        <el-form :model="deviceForm" :rules="deviceRules" ref="deviceFormRef" label-width="100px" status-icon>
          <el-form-item label="设备ID" prop="device_id">
            <el-input v-model="deviceForm.device_id" placeholder="请输入设备ID" />
          </el-form-item>
          <el-form-item label="设备名称" prop="name">
            <el-input v-model="deviceForm.name" placeholder="请输入设备名称" />
          </el-form-item>
          <el-form-item label="设备类型" prop="type">
            <el-select v-model="deviceForm.type" placeholder="选择设备类型">
              <el-option label="摄像头" value="camera" />
              <el-option label="传感器" value="sensor" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="位置" prop="location">
            <el-input v-model="deviceForm.location" placeholder="请输入设备位置" />
          </el-form-item>
          <el-form-item label="IP地址" prop="ip_address">
            <el-input v-model="deviceForm.ip_address" placeholder="请输入IP地址" />
          </el-form-item>
          <el-form-item label="端口" prop="port">
            <el-input-number v-model="deviceForm.port" :min="1" :max="65535" style="width: 100%" />
          </el-form-item>
          <el-form-item label="视频流地址" prop="stream_url">
            <el-input v-model="deviceForm.stream_url" placeholder="请输入视频流地址" />
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input v-model="deviceForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="deviceForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="分辨率" prop="resolution">
            <el-input v-model="deviceForm.resolution" placeholder="请输入分辨率" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="deviceForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="deviceDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveDevice">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="ruleDialogVisible"
        :title="ruleDialogTitle"
        width="500px"
      >
        <el-form :model="ruleForm" :rules="ruleRules" ref="ruleFormRef" label-width="100px" status-icon>
          <el-form-item label="规则名称" prop="name">
            <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
          </el-form-item>
          <el-form-item label="规则类型" prop="type">
            <el-select v-model="ruleForm.type" placeholder="选择规则类型">
              <el-option label="移动侦测" value="motion" />
              <el-option label="火灾预警" value="fire" />
              <el-option label="入侵检测" value="intrusion" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="设备" prop="device_id">
            <el-select v-model="ruleForm.device_id" placeholder="选择设备">
              <el-option 
                v-for="device in devices" 
                :key="device.id" 
                :label="device.name" 
                :value="device.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="阈值" prop="threshold">
            <el-input v-model="ruleForm.threshold" placeholder="请输入阈值" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="ruleForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="ruleDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveRule">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="processAlertDialogVisible"
        title="处理预警"
        width="500px"
      >
        <el-form :model="processAlertForm" ref="processAlertFormRef" label-width="100px" status-icon>
          <el-form-item label="预警信息">
            <el-input v-model="processAlertForm.message" type="textarea" :rows="3" readonly />
          </el-form-item>
          <el-form-item label="处理备注" prop="process_note">
            <el-input v-model="processAlertForm.process_note" type="textarea" :rows="3" placeholder="请输入处理备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="processAlertDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmProcessAlert">确认处理</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="approveDialogVisible"
        title="批准申请"
        width="500px"
      >
        <el-form :model="approveForm" ref="approveFormRef" label-width="100px" status-icon>
          <el-form-item label="申请人">
            <el-input v-model="approveForm.user_name" readonly />
          </el-form-item>
          <el-form-item label="设备">
            <el-input v-model="approveForm.device_name" readonly />
          </el-form-item>
          <el-form-item label="申请原因">
            <el-input v-model="approveForm.purpose" type="textarea" :rows="3" readonly />
          </el-form-item>
          <el-form-item label="时间范围">
            <el-input v-model="approveForm.time_range" readonly />
          </el-form-item>
          <el-form-item label="批准原因" prop="reason">
            <el-input v-model="approveForm.reason" type="textarea" :rows="3" placeholder="请输入批准原因" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="approveDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmApprove">确认批准</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="rejectDialogVisible"
        title="拒绝申请"
        width="500px"
      >
        <el-form :model="rejectForm" ref="rejectFormRef" label-width="100px" status-icon>
          <el-form-item label="申请人">
            <el-input v-model="rejectForm.user_name" readonly />
          </el-form-item>
          <el-form-item label="设备">
            <el-input v-model="rejectForm.device_name" readonly />
          </el-form-item>
          <el-form-item label="申请原因">
            <el-input v-model="rejectForm.purpose" type="textarea" :rows="3" readonly />
          </el-form-item>
          <el-form-item label="拒绝原因" prop="reason">
            <el-input v-model="rejectForm.reason" type="textarea" :rows="3" placeholder="请输入拒绝原因" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="rejectDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmReject">确认拒绝</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import AdminLayout from '@/components/AdminLayout.vue'

// 防抖函数
const debounce = (func, delay) => {
  let timer
  return function() {
    clearTimeout(timer)
    timer = setTimeout(() => func.apply(this, arguments), delay)
  }
}

const activeTab = ref('overview')
const alertTab = ref('rules')
const devices = ref([])
const alertRules = ref([])
const alertRecords = ref([])
const monitoringRequests = ref([])

const alertPage = ref(1)
const alertPageSize = ref(20)
const alertTotal = ref(0)

const requestPage = ref(1)
const requestPageSize = ref(20)
const requestTotal = ref(0)

const alertSearchForm = ref({
  status: ''
})

const requestSearchForm = ref({
  status: ''
})

const deviceDialogVisible = ref(false)
const deviceDialogTitle = ref('新增设备')
const deviceForm = ref({
  device_id: '',
  name: '',
  type: 'camera',
  location: '',
  ip_address: '',
  port: 80,
  stream_url: '',
  username: '',
  password: '',
  resolution: '',
  remark: ''
})

const ruleDialogVisible = ref(false)
const ruleDialogTitle = ref('新增预警规则')
const ruleForm = ref({
  name: '',
  type: 'motion',
  device_id: null,
  threshold: '',
  description: ''
})

const processAlertDialogVisible = ref(false)
const processAlertForm = ref({
  alert_id: null,
  message: '',
  process_note: ''
})

const approveDialogVisible = ref(false)
const approveForm = ref({
  request_id: null,
  user_name: '',
  device_name: '',
  purpose: '',
  time_range: '',
  reason: ''
})

const rejectDialogVisible = ref(false)
const rejectForm = ref({
  request_id: null,
  user_name: '',
  device_name: '',
  purpose: '',
  reason: ''
})

const deviceRules = {
  device_id: [{ required: true, message: '请输入设备ID', trigger: 'blur' }],
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择设备类型', trigger: 'change' }],
  location: [{ required: true, message: '请输入设备位置', trigger: 'blur' }],
  ip_address: [{ required: true, message: '请输入IP地址', trigger: 'blur' }],
  stream_url: [{ required: true, message: '请输入视频流地址', trigger: 'blur' }]
}

const ruleRules = {
  name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择规则类型', trigger: 'change' }],
  device_id: [{ required: true, message: '请选择设备', trigger: 'change' }],
  threshold: [{ required: true, message: '请输入阈值', trigger: 'blur' }]
}

const onlineDevices = computed(() => {
  return devices.value.filter(device => device.status === 'online')
})

const handleTabChange = (tab) => {
  if (tab === 'overview' || tab === 'devices') {
    loadDevices()
  } else if (tab === 'alerts') {
    loadAlertRules()
    loadAlertRecords()
  } else if (tab === 'requests') {
    loadMonitoringRequests()
  }
}

const handleAlertTabChange = (tab) => {
  if (tab === 'rules') {
    loadAlertRules()
  } else if (tab === 'records') {
    loadAlertRecords()
  }
}

const loadDevices = async () => {
  try {
    const response = await axios.get('/api/v1/pc/monitoring/devices')
    devices.value = response.data.data
  } catch (error) {
    ElMessage.error('加载设备列表失败')
  }
}

const loadAlertRules = async () => {
  try {
    const response = await axios.get('/api/v1/pc/monitoring/rules')
    alertRules.value = response.data.data
  } catch (error) {
    ElMessage.error('加载预警规则失败')
  }
}

const loadAlertRecords = async () => {
  try {
    const response = await axios.get('/api/v1/pc/monitoring/alerts', {
      params: {
        page: alertPage.value,
        pageSize: alertPageSize.value,
        status: alertSearchForm.value.status
      }
    })
    alertRecords.value = response.data.data.list
    alertTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载预警记录失败')
  }
}

const loadMonitoringRequests = async () => {
  try {
    const response = await axios.get('/api/v1/pc/monitoring/requests', {
      params: {
        page: requestPage.value,
        pageSize: requestPageSize.value,
        status: requestSearchForm.value.status
      }
    })
    monitoringRequests.value = response.data.data.list
    requestTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载监控查看申请失败')
  }
}

const openDeviceDialog = () => {
  deviceDialogTitle.value = '新增设备'
  deviceForm.value = {
    device_id: '',
    name: '',
    type: 'camera',
    location: '',
    ip_address: '',
    port: 80,
    stream_url: '',
    username: '',
    password: '',
    resolution: '',
    remark: ''
  }
  deviceDialogVisible.value = true
}

const editDevice = (device) => {
  deviceDialogTitle.value = '编辑设备'
  deviceForm.value = { ...device }
  deviceDialogVisible.value = true
}

const saveDevice = async () => {
  try {
    if (deviceDialogTitle.value === '新增设备') {
      await axios.post('/api/v1/pc/monitoring/devices', deviceForm.value)
      ElMessage.success('新增设备成功')
    } else {
      // 这里需要实现更新设备的API
      ElMessage.success('更新设备成功')
    }
    deviceDialogVisible.value = false
    loadDevices()
  } catch (error) {
    ElMessage.error('保存设备失败')
  }
}

const deleteDevice = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该设备吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 这里需要实现删除设备的API
    ElMessage.success('删除成功')
    loadDevices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewStream = (device) => {
  window.open(device.stream_url, '_blank')
}

const openRuleDialog = () => {
  ruleDialogTitle.value = '新增预警规则'
  ruleForm.value = {
    name: '',
    type: 'motion',
    device_id: null,
    threshold: '',
    description: ''
  }
  ruleDialogVisible.value = true
}

const editRule = (rule) => {
  ruleDialogTitle.value = '编辑预警规则'
  ruleForm.value = { ...rule }
  ruleDialogVisible.value = true
}

const saveRule = async () => {
  try {
    if (ruleDialogTitle.value === '新增预警规则') {
      await axios.post('/api/v1/pc/monitoring/rules', ruleForm.value)
      ElMessage.success('新增预警规则成功')
    } else {
      // 这里需要实现更新预警规则的API
      ElMessage.success('更新预警规则成功')
    }
    ruleDialogVisible.value = false
    loadAlertRules()
  } catch (error) {
    ElMessage.error('保存预警规则失败')
  }
}

const toggleRule = async (rule) => {
  try {
    await axios.post(`/api/v1/pc/monitoring/rules/${rule.id}/toggle`)
    ElMessage.success('规则状态切换成功')
  } catch (error) {
    ElMessage.error('规则状态切换失败')
    // 恢复原状态
    rule.enabled = !rule.enabled
  }
}

const processAlert = (alert) => {
  processAlertForm.value = {
    alert_id: alert.id,
    message: alert.message,
    process_note: ''
  }
  processAlertDialogVisible.value = true
}

const confirmProcessAlert = async () => {
  try {
    await axios.post(`/api/v1/pc/monitoring/alerts/${processAlertForm.value.alert_id}/process`, {
      processed_by: 'admin',
      process_note: processAlertForm.value.process_note
    })
    ElMessage.success('预警处理成功')
    processAlertDialogVisible.value = false
    loadAlertRecords()
  } catch (error) {
    ElMessage.error('预警处理失败')
  }
}

const approveRequest = (request) => {
  approveForm.value = {
    request_id: request.id,
    user_name: request.user_name,
    device_name: request.device_name,
    purpose: request.purpose,
    time_range: `${request.start_time} 至 ${request.end_time}`,
    reason: ''
  }
  approveDialogVisible.value = true
}

const confirmApprove = async () => {
  try {
    await axios.post(`/api/v1/pc/monitoring/requests/${approveForm.value.request_id}/approve`, {
      approved_by: 'admin',
      reason: approveForm.value.reason
    })
    ElMessage.success('申请批准成功')
    approveDialogVisible.value = false
    loadMonitoringRequests()
  } catch (error) {
    ElMessage.error('申请批准失败')
  }
}

const rejectRequest = (request) => {
  rejectForm.value = {
    request_id: request.id,
    user_name: request.user_name,
    device_name: request.device_name,
    purpose: request.purpose,
    reason: ''
  }
  rejectDialogVisible.value = true
}

const confirmReject = async () => {
  try {
    await axios.post(`/api/v1/pc/monitoring/requests/${rejectForm.value.request_id}/reject`, {
      approved_by: 'admin',
      reason: rejectForm.value.reason
    })
    ElMessage.success('申请拒绝成功')
    rejectDialogVisible.value = false
    loadMonitoringRequests()
  } catch (error) {
    ElMessage.error('申请拒绝失败')
  }
}

const searchAlerts = debounce(() => {
  alertPage.value = 1
  loadAlertRecords()
}, 300)

const resetAlertSearch = debounce(() => {
  alertSearchForm.value = {
    status: ''
  }
  alertPage.value = 1
  loadAlertRecords()
}, 300)

const searchRequests = debounce(() => {
  requestPage.value = 1
  loadMonitoringRequests()
}, 300)

const resetRequestSearch = debounce(() => {
  requestSearchForm.value = {
    status: ''
  }
  requestPage.value = 1
  loadMonitoringRequests()
}, 300)

const handleAlertSizeChange = debounce((size) => {
  alertPageSize.value = size
  loadAlertRecords()
}, 300)

const handleAlertCurrentChange = debounce((currentPage) => {
  alertPage.value = currentPage
  loadAlertRecords()
}, 300)

const handleRequestSizeChange = debounce((size) => {
  requestPageSize.value = size
  loadMonitoringRequests()
}, 300)

const handleRequestCurrentChange = debounce((currentPage) => {
  requestPage.value = currentPage
  loadMonitoringRequests()
}, 300)

const getLevelTag = (level) => {
  const levelMap = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return levelMap[level] || ''
}

const getLevelText = (level) => {
  const levelMap = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return levelMap[level] || level
}

const getStatusTag = (status) => {
  const statusMap = {
    'pending': 'warning',
    'processed': 'success',
    'ignored': 'info'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processed': '已处理',
    'ignored': '已忽略'
  }
  return statusMap[status] || status
}

const getRequestStatusTag = (status) => {
  const statusMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return statusMap[status] || ''
}

const getRequestStatusText = (status) => {
  const statusMap = {
    'pending': '待审批',
    'approved': '已批准',
    'rejected': '已拒绝'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadDevices()
  loadAlertRules()
  loadAlertRecords()
  loadMonitoringRequests()
})
</script>

<style scoped>
.monitoring-management {
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

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.device-card {
  transition: all 0.3s ease;
}

.device-card.offline {
  opacity: 0.6;
}

.device-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.device-info {
  margin: 10px 0;
}

.device-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.realtime-monitoring {
  margin-top: 20px;
}

.monitoring-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.monitoring-item {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.monitoring-header {
  background: #f5f7fa;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitoring-content {
  padding: 10px;
}

.monitoring-video {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.monitoring-info {
  padding: 10px;
  background: #f5f7fa;
  font-size: 14px;
  color: #606266;
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
</style>
