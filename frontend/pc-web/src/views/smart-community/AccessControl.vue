<template>
  <div class="access-control">
    <div class="page-header">
      <h1>🚪 智能门禁</h1>
      <p class="subtitle">人脸识别、远程开门、出入记录查询</p>
    </div>

    <div class="feature-grid">
      <!-- 远程开门 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📱 远程开门</span>
          </div>
        </template>
        <div class="remote-open">
          <el-select v-model="selectedDevice" placeholder="选择门禁设备" style="width: 100%; margin-bottom: 15px;">
            <el-option
              v-for="device in devices"
              :key="device.id"
              :label="device.device_name"
              :value="device.id"
            />
          </el-select>
          <el-button type="primary" size="large" style="width: 100%;" @click="handleRemoteOpen">
            <el-icon><Unlock /></el-icon>
            一键开门
          </el-button>
        </div>
      </el-card>

      <!-- 我的权限 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>🔑 我的门禁权限</span>
          </div>
        </template>
        <div class="permission-list">
          <div v-for="perm in myPermissions" :key="perm.id" class="permission-item">
            <div class="perm-info">
              <span class="device-name">{{ perm.device_name }}</span>
              <el-tag size="small" :type="perm.access_type === 'face' ? 'success' : 'primary'">
                {{ perm.access_type === 'face' ? '人脸识别' : perm.access_type === 'fingerprint' ? '指纹' : '门禁卡' }}
              </el-tag>
            </div>
            <el-tag size="small" :type="perm.status === 'active' ? 'success' : 'danger'">
              {{ perm.status === 'active' ? '有效' : '已失效' }}
            </el-tag>
          </div>
          <el-empty v-if="myPermissions.length === 0" description="暂无门禁权限" />
        </div>
      </el-card>

      <!-- 今日统计 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📊 今日出入统计</span>
          </div>
        </template>
        <div class="statistics">
          <div class="stat-item">
            <div class="stat-value">{{ todayStats.entry_count || 0 }}</div>
            <div class="stat-label">进入人次</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ todayStats.exit_count || 0 }}</div>
            <div class="stat-label">离开人次</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ todayStats.visitor_count || 0 }}</div>
            <div class="stat-label">访客人数</div>
          </div>
        </div>
      </el-card>

      <!-- 快捷操作 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" plain @click="$router.push('/access-control/records')">
            <el-icon><List /></el-icon>
            出入记录
          </el-button>
          <el-button type="success" plain @click="$router.push('/visitor')">
            <el-icon><User /></el-icon>
            访客预约
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 最近出入记录 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>📝 最近出入记录</span>
          <el-button text @click="$router.push('/access-control/records')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="recentRecords" style="width: 100%">
        <el-table-column prop="record_time" label="时间" width="180" />
        <el-table-column prop="device_name" label="门禁设备" width="150" />
        <el-table-column prop="access_type" label="开门方式" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getAccessTypeType(scope.row.access_type)">
              {{ getAccessTypeText(scope.row.access_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="access_status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="scope.row.access_status === 'success' ? 'success' : 'danger'">
              {{ scope.row.access_status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="temperature" label="体温" width="100">
          <template #default="scope">
            <span v-if="scope.row.temperature">{{ scope.row.temperature }}°C</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Unlock, List, User } from '@element-plus/icons-vue'

const devices = ref([])
const myPermissions = ref([])
const recentRecords = ref([])
const todayStats = ref({})
const selectedDevice = ref('')

// 获取门禁设备列表
const loadDevices = async () => {
  try {
    const response = await fetch('/api/v1/pc/access/devices', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      devices.value = result.data || []
    }
  } catch (error) {
    console.error('加载设备失败:', error)
  }
}

// 获取我的权限
const loadMyPermissions = async () => {
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    const response = await fetch(`/api/v1/pc/access/permissions?user_id=${userInfo.id}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      myPermissions.value = result.data || []
    }
  } catch (error) {
    console.error('加载权限失败:', error)
  }
}

// 获取最近记录
const loadRecentRecords = async () => {
  try {
    const response = await fetch('/api/v1/pc/access/records?pageSize=5', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      recentRecords.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载记录失败:', error)
  }
}

// 远程开门
const handleRemoteOpen = async () => {
  if (!selectedDevice.value) {
    ElMessage.warning('请选择门禁设备')
    return
  }
  
  try {
    const response = await fetch('/api/v1/pc/access/remote-open', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ device_id: selectedDevice.value })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('开门指令已发送')
    } else {
      ElMessage.error(result.msg || '开门失败')
    }
  } catch (error) {
    console.error('远程开门失败:', error)
    ElMessage.error('开门失败')
  }
}

const getAccessTypeText = (type) => {
  const map = {
    'face': '人脸识别',
    'fingerprint': '指纹',
    'card': '门禁卡',
    'qr_code': '二维码',
    'password': '密码',
    'remote': '远程'
  }
  return map[type] || type
}

const getAccessTypeType = (type) => {
  const map = {
    'face': 'success',
    'fingerprint': 'primary',
    'card': 'warning',
    'qr_code': 'info',
    'password': 'danger',
    'remote': 'success'
  }
  return map[type] || 'info'
}

onMounted(() => {
  loadDevices()
  loadMyPermissions()
  loadRecentRecords()
})
</script>

<style scoped>
.access-control {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.permission-list {
  max-height: 200px;
  overflow-y: auto;
}

.permission-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.permission-item:last-child {
  border-bottom: none;
}

.perm-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.device-name {
  font-weight: 500;
}

.statistics {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #909399;
  margin-top: 5px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.records-card {
  border-radius: 8px;
}
</style>
