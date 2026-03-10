<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>系统设置</h1>
        <p>管理系统配置、权限和系统信息</p>
      </div>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form :model="basicSettings" label-width="150px" class="settings-form">
            <el-form-item label="社区名称">
              <el-input v-model="basicSettings.community_name" placeholder="请输入社区名称" />
            </el-form-item>
            <el-form-item label="社区地址">
              <el-input v-model="basicSettings.community_address" placeholder="请输入社区地址" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="basicSettings.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="邮箱地址">
              <el-input v-model="basicSettings.contact_email" placeholder="请输入邮箱地址" />
            </el-form-item>
            <el-form-item label="系统标题">
              <el-input v-model="basicSettings.system_title" placeholder="请输入系统标题" />
            </el-form-item>
            <el-form-item label="系统logo">
              <el-upload
                class="upload-demo"
                action="#"
                :auto-upload="false"
                :on-change="handleLogoChange"
                :file-list="basicSettings.system_logo"
              >
                <el-button type="primary">
                  <el-icon><Upload /></el-icon> 选择logo
                </el-button>
              </el-upload>
            </el-form-item>
            <el-form-item label="版权信息">
              <el-input v-model="basicSettings.copyright" placeholder="请输入版权信息" />
            </el-form-item>
            <el-form-item label="系统状态">
              <el-switch v-model="basicSettings.system_status" />
              <span style="margin-left: 10px;">{{ basicSettings.system_status ? '运行中' : '维护中' }}</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="用户权限" name="permissions">
          <div class="permission-header">
            <h4>用户角色管理</h4>
            <el-button type="primary" @click="showAddRoleDialog = true">
              <el-icon><Plus /></el-icon> 添加角色
            </el-button>
          </div>

          <el-table :data="roles" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="角色名称" width="150" />
            <el-table-column prop="description" label="角色描述" min-width="200" />
            <el-table-column prop="user_count" label="用户数量" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editRole(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteRole(scope.row)">删除</el-button>
                <el-button size="small" type="warning" link @click="managePermissions(scope.row)">权限</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="通知设置" name="notifications">
          <el-form :model="notificationSettings" label-width="150px" class="settings-form">
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationSettings.email_enabled" />
            </el-form-item>
            <el-form-item label="SMTP服务器">
              <el-input v-model="notificationSettings.smtp_server" placeholder="请输入SMTP服务器地址" />
            </el-form-item>
            <el-form-item label="SMTP端口">
              <el-input-number v-model="notificationSettings.smtp_port" :min="1" :max="65535" />
            </el-form-item>
            <el-form-item label="发件人邮箱">
              <el-input v-model="notificationSettings.sender_email" placeholder="请输入发件人邮箱" />
            </el-form-item>
            <el-form-item label="SMTP用户名">
              <el-input v-model="notificationSettings.smtp_username" placeholder="请输入SMTP用户名" />
            </el-form-item>
            <el-form-item label="SMTP密码">
              <el-input v-model="notificationSettings.smtp_password" type="password" placeholder="请输入SMTP密码" />
            </el-form-item>
            <el-form-item label="短信通知">
              <el-switch v-model="notificationSettings.sms_enabled" />
            </el-form-item>
            <el-form-item label="短信API密钥">
              <el-input v-model="notificationSettings.sms_api_key" placeholder="请输入短信API密钥" />
            </el-form-item>
            <el-form-item label="短信模板ID">
              <el-input v-model="notificationSettings.sms_template_id" placeholder="请输入短信模板ID" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
              <el-button type="warning" @click="testNotification">测试通知</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="系统信息" name="system">
          <div class="system-info">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>系统基本信息</span>
                  </template>
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="系统版本">
                      {{ systemInfo.version }}
                    </el-descriptions-item>
                    <el-descriptions-item label="运行环境">
                      {{ systemInfo.environment }}
                    </el-descriptions-item>
                    <el-descriptions-item label="数据库版本">
                      {{ systemInfo.database_version }}
                    </el-descriptions-item>
                    <el-descriptions-item label="服务器时间">
                      {{ systemInfo.server_time }}
                    </el-descriptions-item>
                    <el-descriptions-item label="启动时间">
                      {{ systemInfo.start_time }}
                    </el-descriptions-item>
                  </el-descriptions>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>服务器资源</span>
                  </template>
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="CPU使用率">
                      <el-progress :percentage="systemInfo.cpu_usage" :stroke-width="10" />
                    </el-descriptions-item>
                    <el-descriptions-item label="内存使用率">
                      <el-progress :percentage="systemInfo.memory_usage" :stroke-width="10" />
                    </el-descriptions-item>
                    <el-descriptions-item label="磁盘使用率">
                      <el-progress :percentage="systemInfo.disk_usage" :stroke-width="10" />
                    </el-descriptions-item>
                    <el-descriptions-item label="网络流量">
                      {{ systemInfo.network_traffic }}
                    </el-descriptions-item>
                  </el-descriptions>
                </el-card>
              </el-col>
            </el-row>

            <el-card style="margin-top: 20px;">
              <template #header>
                <span>系统日志</span>
              </template>
              <div class="system-logs">
                <el-table :data="systemLogs" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="70" />
                  <el-table-column prop="level" label="级别" width="100">
                    <template #default="scope">
                      <el-tag :type="getLogLevelType(scope.row.level)" size="small">
                        {{ scope.row.level }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="message" label="消息" min-width="300" />
                  <el-table-column prop="create_time" label="时间" width="160" />
                </el-table>
                <div class="pagination-container">
                  <el-pagination
                    v-model:current-page="logCurrentPage"
                    v-model:page-size="logPageSize"
                    :total="logTotal"
                    :page-sizes="[10, 20, 50]"
                    layout="total, sizes, prev, pager, next"
                  />
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddRoleDialog" title="添加角色" width="400px">
      <el-form :model="roleForm" label-width="100px">
        <el-form-item label="角色名称">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色描述">
          <el-input v-model="roleForm.description" type="textarea" rows="3" placeholder="请输入角色描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRoleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRole">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showPermissionDialog" title="角色权限管理" width="600px">
      <div v-if="currentRole" class="permission-management">
        <h4>{{ currentRole.name }} - 权限设置</h4>
        <el-checkbox-group v-model="currentRole.permissions">
          <el-checkbox v-for="permission in allPermissions" :key="permission.id" :label="permission.id">
            {{ permission.name }}
          </el-checkbox>
        </el-checkbox-group>
      </div>
      <template #footer>
        <el-button @click="showPermissionDialog = false">取消</el-button>
        <el-button type="primary" @click="savePermissions">保存权限</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('basic')
const showAddRoleDialog = ref(false)
const showPermissionDialog = ref(false)
const logCurrentPage = ref(1)
const logPageSize = ref(10)
const logTotal = ref(0)

const basicSettings = ref({
  community_name: '智慧社区',
  community_address: '北京市朝阳区幸福小区',
  contact_phone: '13800138000',
  contact_email: 'contact@smart-community.com',
  system_title: '智慧社区管理系统',
  system_logo: [],
  copyright: '© 2024 智慧社区管理系统 版权所有',
  system_status: true
})

const notificationSettings = ref({
  email_enabled: true,
  smtp_server: 'smtp.qq.com',
  smtp_port: 465,
  sender_email: 'noreply@smart-community.com',
  smtp_username: 'noreply@smart-community.com',
  smtp_password: 'password',
  sms_enabled: false,
  sms_api_key: '',
  sms_template_id: ''
})

const systemInfo = ref({
  version: '1.0.0',
  environment: 'production',
  database_version: 'MySQL 8.0',
  server_time: new Date().toLocaleString(),
  start_time: '2024-01-01 00:00:00',
  cpu_usage: 35,
  memory_usage: 45,
  disk_usage: 60,
  network_traffic: '1.2 GB'
})

const roles = ref([])
const systemLogs = ref([])
const roleForm = ref({ name: '', description: '' })
const currentRole = ref(null)
const allPermissions = ref([])

const loadRoles = () => {
  roles.value = [
    { id: 1, name: '管理员', description: '系统管理员，拥有所有权限', user_count: 2, create_time: '2024-01-01 00:00:00' },
    { id: 2, name: '物业', description: '物业管理人员', user_count: 5, create_time: '2024-01-01 00:00:00' },
    { id: 3, name: '居民', description: '普通居民用户', user_count: 2890, create_time: '2024-01-01 00:00:00' }
  ]
}

const loadSystemLogs = () => {
  systemLogs.value = [
    { id: 1, level: 'info', message: '系统启动成功', create_time: '2024-01-15 00:00:00' },
    { id: 2, level: 'warning', message: '数据库连接超时', create_time: '2024-01-14 18:30:00' },
    { id: 3, level: 'error', message: 'API调用失败', create_time: '2024-01-14 15:20:00' },
    { id: 4, level: 'info', message: '用户登录成功', create_time: '2024-01-14 10:00:00' }
  ]
  logTotal.value = 4
}

const loadPermissions = () => {
  allPermissions.value = [
    { id: 1, name: '用户管理' },
    { id: 2, name: '建筑管理' },
    { id: 3, name: '门禁管理' },
    { id: 4, name: '报修管理' },
    { id: 5, name: '公告管理' },
    { id: 6, name: '水电管理' },
    { id: 7, name: '停车管理' },
    { id: 8, name: '快递柜管理' },
    { id: 9, name: '访客管理' },
    { id: 10, name: '投诉管理' },
    { id: 11, name: '系统设置' }
  ]
}

const handleLogoChange = (file) => {
  basicSettings.value.system_logo = [file]
}

const saveBasicSettings = () => {
  ElMessage.success('基本设置保存成功')
}

const saveNotificationSettings = () => {
  ElMessage.success('通知设置保存成功')
}

const testNotification = () => {
  ElMessage.info('测试通知发送中...')
  setTimeout(() => {
    ElMessage.success('测试通知发送成功')
  }, 1000)
}

const saveRole = () => {
  ElMessage.success('角色保存成功')
  showAddRoleDialog.value = false
  loadRoles()
}

const editRole = (role) => {
  roleForm.value = { ...role }
  showAddRoleDialog.value = true
}

const deleteRole = async (role) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗？', '提示', { type: 'warning' })
    ElMessage.success('角色删除成功')
    loadRoles()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const managePermissions = (role) => {
  currentRole.value = { ...role, permissions: [1, 2, 3] }
  showPermissionDialog.value = true
}

const savePermissions = () => {
  ElMessage.success('权限保存成功')
  showPermissionDialog.value = false
}

const getLogLevelType = (level) => {
  const map = { 'info': 'info', 'warning': 'warning', 'error': 'danger' }
  return map[level] || 'info'
}

onMounted(() => {
  loadRoles()
  loadSystemLogs()
  loadPermissions()
})
</script>

<style scoped>
.admin-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.main-card {
  border-radius: 12px;
}

.settings-form {
  max-width: 600px;
  padding: 20px;
}

.permission-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.permission-header h4 {
  margin: 0;
  font-size: 16px;
}

.system-info {
  padding: 20px;
}

.system-logs {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.permission-management {
  padding: 20px;
}

.permission-management h4 {
  margin: 0 0 20px 0;
}

.permission-management .el-checkbox {
  display: block;
  margin-bottom: 10px;
}
</style>