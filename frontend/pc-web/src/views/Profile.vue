<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p>管理您的个人信息和账户设置</p>
    </div>

    <div class="profile-content">
      <!-- 左侧导航 -->
      <div class="profile-sidebar">
        <div class="user-card">
          <div class="avatar-wrapper">
            <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" alt="头像" />
            <div v-else class="avatar-placeholder">
              {{ (userInfo.nickname || userInfo.phone || '用户').charAt(0) }}
            </div>
          </div>
          <h3 class="user-name">{{ userInfo.nickname || userInfo.phone }}</h3>
          <p class="user-role">{{ userInfo.role || '居民' }}</p>
        </div>

        <div class="menu-list">
          <div
            v-for="tab in tabs"
            :key="tab.name"
            class="menu-item"
            :class="{ active: activeTab === tab.name }"
            @click="() => {
              console.log('点击了标签页:', tab.name)
              activeTab = tab.name
              console.log('activeTab更新为:', activeTab)
            }"
          >
            <span class="menu-icon">{{ tab.icon }}</span>
            <span class="menu-label">{{ tab.label }}</span>
          </div>
        </div>
      </div>

      <!-- 右侧内容 -->
      <div class="profile-main">
        <!-- 基础信息 -->
        <div v-show="activeTab === 'basic'" class="tab-panel">
          <div class="panel-header">
            <h2>基础信息</h2>
            <p>管理您的基本资料</p>
          </div>

          <form ref="basicFormRef" class="info-form" @submit.prevent="saveBasicInfo">
            <div class="form-section">
              <h3>个人信息</h3>
              <div class="avatar-section">
                <div class="avatar-uploader">
                  <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar-preview" />
                  <div v-else class="avatar-placeholder-large">
                    <span class="upload-icon">+</span>
                    <span class="upload-text">点击上传头像</span>
                  </div>
                  <input
                    type="file"
                    ref="fileInput"
                    class="file-input"
                    accept="image/jpeg,image/png,image/gif"
                    @change="handleFileChange"
                  />
                </div>

                <div class="info-fields">
                  <div class="form-item">
                    <label>昵称 <span class="required">*</span></label>
                    <input v-model="userInfo.nickname" type="text" placeholder="请输入昵称" maxlength="20" required />
                  </div>

                  <div class="form-item">
                    <label>手机号</label>
                    <input v-model="userInfo.phone" type="text" disabled />
                  </div>

                  <div class="form-item">
                    <label>邮箱</label>
                    <input v-model="userInfo.email" type="email" placeholder="请输入邮箱" />
                  </div>

                  <div class="form-item">
                    <label>性别</label>
                    <div class="radio-group">
                      <label class="radio-label">
                        <input type="radio" v-model="userInfo.gender" :value="0" name="gender" />
                        <span>保密</span>
                      </label>
                      <label class="radio-label">
                        <input type="radio" v-model="userInfo.gender" :value="1" name="gender" />
                        <span>男</span>
                      </label>
                      <label class="radio-label">
                        <input type="radio" v-model="userInfo.gender" :value="2" name="gender" />
                        <span>女</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-section">
              <h3>居住信息</h3>
              <div class="info-grid">
                <div class="form-item">
                  <label>楼栋</label>
                  <select v-model="userInfo.buildingId" class="form-select">
                    <option value="">请选择楼栋</option>
                    <option v-for="building in buildings" :key="building.id" :value="building.id">
                      {{ building.name }}
                    </option>
                  </select>
                </div>

                <div class="form-item">
                  <label>单元</label>
                  <input v-model="userInfo.unit" type="text" placeholder="请输入单元" maxlength="10" />
                </div>

                <div class="form-item">
                  <label>房号</label>
                  <input v-model="userInfo.roomNumber" type="text" placeholder="请输入房号" maxlength="10" />
                </div>

                <div class="form-item">
                  <label>家庭结构</label>
                  <input v-model="userInfo.familyStructure" type="text" disabled placeholder="系统自动识别" />
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading">保存中...</span>
                <span v-else>✓ 保存修改</span>
              </button>
              <button type="button" class="btn btn-default" @click="resetBasicInfo">重置</button>
            </div>
          </form>
        </div>

        <!-- 兴趣标签 -->
        <div v-show="activeTab === 'interests'" class="tab-panel">
          <div class="panel-header">
            <h2>兴趣标签</h2>
            <p>选择您感兴趣的标签，我们将为您推荐相关内容</p>
          </div>

          <div class="tags-section">
            <div class="tag-category">
              <h3>生活方式</h3>
              <div class="tag-list">
                <span
                  v-for="tag in lifestyleTags"
                  :key="tag"
                  class="tag-item"
                  :class="{ active: Array.isArray(selectedTags) && selectedTags.includes(tag) }"
                  @click="toggleTag(tag)"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <div class="tag-category">
              <h3>社区服务</h3>
              <div class="tag-list">
                <span
                  v-for="tag in serviceTags"
                  :key="tag"
                  class="tag-item"
                  :class="{ active: Array.isArray(selectedTags) && selectedTags.includes(tag) }"
                  @click="toggleTag(tag)"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" :disabled="loading" @click="saveInterestTags">
              <span v-if="loading">保存中...</span>
              <span v-else>✓ 保存标签</span>
            </button>
          </div>
        </div>

        <!-- 安全设置 -->
        <div v-show="activeTab === 'security'" class="tab-panel">
          <div class="panel-header">
            <h2>安全设置</h2>
            <p>管理您的账户安全</p>
          </div>

          <div class="security-section">
            <div class="security-item">
              <div class="security-info">
                <h3>修改密码</h3>
                <p>定期修改密码可以保护您的账户安全</p>
              </div>
              <button class="btn btn-primary" @click="showPasswordModal = true">修改</button>
            </div>

            <div class="security-item">
              <div class="security-info">
                <h3>绑定手机号</h3>
                <p>当前手机号：{{ userInfo.phone }}</p>
              </div>
              <button class="btn btn-default" @click="showPhoneModal = true">更换</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="showPasswordModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>修改密码</h3>
          <button class="modal-close" @click="showPasswordModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-item">
            <label>原密码</label>
            <input v-model="passwordForm.oldPassword" type="password" placeholder="请输入原密码" />
          </div>
          <div class="form-item">
            <label>新密码</label>
            <input v-model="passwordForm.newPassword" type="password" placeholder="请输入新密码" />
          </div>
          <div class="form-item">
            <label>确认密码</label>
            <input v-model="passwordForm.confirmPassword" type="password" placeholder="请再次输入新密码" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-default" @click="showPasswordModal = false">取消</button>
          <button class="btn btn-primary" @click="changePassword">确认</button>
        </div>
      </div>
    </div>

    <!-- 更换手机号弹窗 -->
    <div v-if="showPhoneModal" class="modal-overlay" @click.self="showPhoneModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>更换手机号</h3>
          <button class="modal-close" @click="showPhoneModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-item">
            <label>新手机号</label>
            <input v-model="phoneForm.newPhone" type="text" placeholder="请输入新手机号" />
          </div>
          <div class="form-item">
            <label>验证码</label>
            <div class="verify-code">
              <input v-model="phoneForm.code" type="text" placeholder="请输入验证码" />
              <button class="btn btn-default" :disabled="countdown > 0" @click="sendCode">
                {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-default" @click="showPhoneModal = false">取消</button>
          <button class="btn btn-primary" @click="changePhone">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/request'

const router = useRouter()

// 消息提示函数
const showMessage = (message, type = 'success') => {
  alert(message)
}

const showConfirm = (message, title) => {
  return new Promise((resolve, reject) => {
    if (confirm(`${title}\n${message}`)) {
      resolve()
    } else {
      reject()
    }
  })
}

// 标签页
const tabs = [
  { name: 'basic', label: '基础信息', icon: '👤' },
  { name: 'interests', label: '兴趣标签', icon: '🏷️' },
  { name: 'security', label: '安全设置', icon: '🔒' }
]

// 兴趣标签
const lifestyleTags = ['亲子', '运动', '美食', '旅游', '阅读', '音乐', '电影', '摄影']
const serviceTags = ['团购', '家政', '维修', '养老', '教育', '医疗', '健身', '宠物']

// 状态
const activeTab = ref('basic')
const loading = ref(false)
const countdown = ref(0)
const showPasswordModal = ref(false)
const showPhoneModal = ref(false)
const selectedTags = ref([])
const selectedFile = ref(null)

// 表单引用
const basicFormRef = ref(null)
const fileInput = ref(null)

// 用户信息
const userInfo = reactive({
  id: '',
  phone: '',
  nickname: '',
  avatar: '',
  email: '',
  gender: 0,
  buildingId: '',
  unit: '',
  roomNumber: '',
  familyStructure: '',
  role: ''
})

// 楼栋数据
const buildings = ref([])

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 手机号表单
const phoneForm = reactive({
  newPhone: '',
  code: ''
})

// 用户存储
const userStore = useUserStore()

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const response = await axios.get('/v1/pc/user/info')
    if (response.data.code === 0) {
      const data = convertToCamelCase(response.data.data)
      console.log('获取到的用户信息:', data)
      
      // 更新用户信息，保留现有值作为后备
      Object.assign(userInfo, {
        id: data.id || userInfo.id,
        phone: data.phone || userInfo.phone,
        nickname: data.nickname || userInfo.nickname,
        avatar: data.avatar || userInfo.avatar,
        email: data.email || userInfo.email,
        gender: data.gender !== undefined ? data.gender : userInfo.gender,
        buildingId: data.buildingId || data.building_id || userInfo.buildingId,
        unit: data.unit || userInfo.unit,
        roomNumber: data.roomNumber || data.room_number || userInfo.roomNumber,
        familyStructure: data.familyStructure || data.family_structure || userInfo.familyStructure,
        role: data.role || userInfo.role
      })
      
      if (data.interestTags || data.interest_tags) {
        const tags = data.interestTags || data.interest_tags
        selectedTags.value = Array.isArray(tags) ? tags : []
      } else {
        selectedTags.value = []
      }
      
      // 更新store中的用户信息
      userStore.userInfo = { ...userInfo }
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showMessage('获取用户信息失败', 'error')
  }
}

// 获取楼栋列表
const fetchBuildings = async () => {
  try {
    console.log('开始获取楼栋列表...')
    const response = await axios.get('/v1/pc/building/all')
    console.log('楼栋列表响应:', response.data)
    if (response.data.code === 0) {
      buildings.value = response.data.data
      console.log('楼栋数据已加载:', buildings.value)
    } else {
      console.error('获取楼栋列表失败:', response.data.msg)
    }
  } catch (error) {
    console.error('获取楼栋列表失败:', error)
  }
}

// 转换字段格式
const convertToCamelCase = (obj) => {
  if (!obj || typeof obj !== 'object') return obj
  const result = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const camelKey = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase())
      result[camelKey] = typeof obj[key] === 'object' ? convertToCamelCase(obj[key]) : obj[key]
    }
  }
  return result
}

// 保存基础信息
const saveBasicInfo = async () => {
  // 验证昵称
  if (!userInfo.nickname || userInfo.nickname.length < 2) {
    showMessage('请输入昵称，长度至少2个字符', 'error')
    return
  }

  try {
    await showConfirm('确定要保存修改吗？', '提示')

    loading.value = true

    // 先上传头像（如果有新头像）
    if (selectedFile.value) {
      const formData = new FormData()
      formData.append('file', selectedFile.value)

      const response = await axios.post('/v1/pc/user/upload-avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      if (response.data.code === 0) {
        userInfo.avatar = response.data.data.avatarUrl
        selectedFile.value = null
      } else {
        showMessage('头像上传失败: ' + response.data.msg, 'error')
        return
      }
    }

    // 只发送后端需要的字段
    const updateData = {
      nickname: userInfo.nickname,
      avatar: userInfo.avatar,
      email: userInfo.email,
      gender: userInfo.gender,
      building_id: userInfo.buildingId || null,
      unit: userInfo.unit,
      room_number: userInfo.roomNumber,
      family_structure: userInfo.familyStructure
    }

    console.log('发送的更新数据:', updateData)

    const response = await axios.put('/v1/pc/user/update', updateData)
    console.log('更新响应:', response.data)

    if (response.data.code === 0) {
      showMessage('保存成功')
      // 更新本地数据
      const updatedData = convertToCamelCase(response.data.data)
      // 保留原有的role字段
      updatedData.role = updatedData.role || userInfo.role
      Object.assign(userInfo, updatedData)
      // 更新store
      userStore.userInfo = { ...updatedData }
      localStorage.setItem('userInfo', JSON.stringify(updatedData))
    } else {
      showMessage(response.data.msg || '保存失败', 'error')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('保存失败:', error)
      showMessage('保存失败，请重试', 'error')
    }
  } finally {
    loading.value = false
  }
}

// 重置基础信息
const resetBasicInfo = () => {
  fetchUserInfo()
  selectedFile.value = null
  showMessage('已重置')
}

// 处理文件选择
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    showMessage('只能上传图片文件', 'error')
    return
  }

  if (!isLt2M) {
    showMessage('图片大小不能超过2MB', 'error')
    return
  }

  // 保存文件用于后续上传
  selectedFile.value = file

  // 预览
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = () => {
    userInfo.avatar = reader.result
  }

  showMessage('头像已选择，点击保存修改后上传')
}

// 切换标签
const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

// 保存兴趣标签
const saveInterestTags = async () => {
  loading.value = true
  try {
    const response = await axios.put('/v1/pc/user/interest-tags', {
      interestTags: selectedTags.value
    })

    if (response.data.code === 0) {
      showMessage('保存成功')
    } else {
      showMessage(response.data.msg || '保存失败', 'error')
    }
  } catch (error) {
    console.error('保存兴趣标签失败:', error)
    showMessage('保存失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 修改密码
const changePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    showMessage('两次输入的密码不一致', 'error')
    return
  }

  try {
    const response = await axios.put('/v1/pc/user/password', {
      oldPassword: passwordForm.oldPassword,
      newPassword: passwordForm.newPassword
    })

    if (response.data.code === 0) {
      showMessage('密码修改成功')
      showPasswordModal.value = false
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    } else {
      showMessage(response.data.msg || '修改失败', 'error')
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    showMessage('修改失败，请重试', 'error')
  }
}

// 发送验证码
const sendCode = () => {
  if (!phoneForm.newPhone) {
    showMessage('请输入新手机号', 'error')
    return
  }

  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)

  showMessage('验证码已发送')
}

// 更换手机号
const changePhone = async () => {
  if (!phoneForm.newPhone || !phoneForm.code) {
    showMessage('请填写完整信息', 'error')
    return
  }

  try {
    const response = await axios.put('/v1/pc/user/phone', {
      newPhone: phoneForm.newPhone,
      code: phoneForm.code
    })

    if (response.data.code === 0) {
      showMessage('手机号更换成功')
      showPhoneModal.value = false
      userInfo.phone = phoneForm.newPhone
      phoneForm.newPhone = ''
      phoneForm.code = ''
    } else {
      showMessage(response.data.msg || '更换失败', 'error')
    }
  } catch (error) {
    console.error('更换手机号失败:', error)
    showMessage('更换失败，请重试', 'error')
  }
}

// 组件挂载
onMounted(() => {
  // 先从store加载用户信息
  if (userStore.userInfo && userStore.userInfo.id) {
    const storeUserInfo = { ...userStore.userInfo }
    // 转换字段名
    Object.assign(userInfo, {
      id: storeUserInfo.id,
      phone: storeUserInfo.phone,
      nickname: storeUserInfo.nickname || '',
      avatar: storeUserInfo.avatar || '',
      email: storeUserInfo.email || '',
      gender: storeUserInfo.gender || 0,
      buildingId: storeUserInfo.buildingId || storeUserInfo.building_id || '',
      unit: storeUserInfo.unit || '',
      roomNumber: storeUserInfo.roomNumber || storeUserInfo.room_number || '',
      familyStructure: storeUserInfo.familyStructure || storeUserInfo.family_structure || '',
      role: storeUserInfo.role || '居民'
    })
    if (storeUserInfo.interestTags || storeUserInfo.interest_tags) {
      const tags = storeUserInfo.interestTags || storeUserInfo.interest_tags
      selectedTags.value = Array.isArray(tags) ? tags : []
    } else {
      selectedTags.value = []
    }
  }
  // 然后从服务器获取最新信息
  fetchUserInfo()
  fetchBuildings()
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
}

.profile-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.profile-header p {
  color: #666;
}

.profile-content {
  display: flex;
  gap: 20px;
}

.profile-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.user-card {
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.avatar-wrapper {
  margin-bottom: 15px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
  margin: 0 auto;
}

.user-name {
  font-size: 18px;
  color: #333;
  margin-bottom: 5px;
}

.user-role {
  color: #666;
  font-size: 14px;
}

.menu-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.menu-item:hover {
  background: #f5f7fa;
}

.menu-item.active {
  background: #ecf5ff;
  border-left-color: #409eff;
  color: #409eff;
}

.menu-icon {
  margin-right: 10px;
  font-size: 18px;
}

.menu-label {
  font-size: 14px;
}

.profile-main {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.panel-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.panel-header h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
}

.panel-header p {
  color: #666;
  font-size: 14px;
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.avatar-section {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.avatar-uploader {
  position: relative;
  width: 120px;
  height: 120px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.3s;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder-large {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.upload-icon {
  font-size: 32px;
  margin-bottom: 5px;
}

.upload-text {
  font-size: 12px;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.info-fields {
  flex: 1;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-size: 14px;
}

.form-item label .required {
  color: #f56c6c;
  margin-left: 4px;
}

.form-item input,
.form-item select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-item input:focus,
.form-item select:focus {
  outline: none;
  border-color: #409eff;
}

.form-item input:disabled {
  background: #f5f7fa;
  color: #909399;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
}

.radio-label input {
  width: auto;
  margin-right: 6px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #409eff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #66b1ff;
}

.btn-default {
  background: #fff;
  color: #606266;
  border: 1px solid #dcdfe6;
}

.btn-default:hover:not(:disabled) {
  color: #409eff;
  border-color: #c6e2ff;
  background: #ecf5ff;
}

.tags-section {
  margin-bottom: 30px;
}

.tag-category {
  margin-bottom: 25px;
}

.tag-category h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  padding: 8px 16px;
  font-size: 14px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  background: #fff;
  color: #606266;
}

.tag-item:hover {
  color: #409eff;
  border-color: #c6e2ff;
}

.tag-item.active {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.security-section {
  margin-bottom: 30px;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
}

.security-info h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}

.security-info p {
  color: #666;
  font-size: 14px;
}

.merchant-section {
  margin-bottom: 30px;
}

.merchant-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40px;
  background: #f0f9ff;
  border-radius: 8px;
}

.status-icon {
  font-size: 48px;
  margin-right: 30px;
}

.status-info h3 {
  font-size: 20px;
  color: #409EFF;
  margin-bottom: 10px;
}

.status-info p {
  color: #666;
  font-size: 14px;
}

.merchant-apply {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.apply-card {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  max-width: 400px;
}

.apply-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.apply-card h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.apply-card p {
  font-size: 14px;
  margin-bottom: 20px;
  opacity: 0.9;
}

.feature-list {
  text-align: left;
  margin: 20px 0;
  padding-left: 20px;
}

.feature-list li {
  margin: 10px 0;
  font-size: 14px;
}

.verify-code {
  display: flex;
  gap: 10px;
}

.verify-code input {
  flex: 1;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  max-height: 80vh;
  overflow: hidden;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #909399;
  cursor: pointer;
}

.modal-close:hover {
  color: #409eff;
}

.modal-body {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .profile-content {
    flex-direction: column;
  }

  .profile-sidebar {
    width: 100%;
  }

  .avatar-section {
    flex-direction: column;
    align-items: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    width: 95%;
    margin: 20px;
  }
}
</style>
