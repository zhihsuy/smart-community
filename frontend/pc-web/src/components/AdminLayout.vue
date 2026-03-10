<template>
  <div class="admin-layout">
    <!-- 左侧导航栏 -->
    <aside class="admin-sidebar" :class="{ collapsed: !isSidebarOpen }">
      <div class="sidebar-header">
        <div class="logo">
          <h1>管理中心</h1>
        </div>
        <div class="admin-info">
          <div class="avatar">
            {{ userInfo.nickname?.charAt(0) || '管' }}
          </div>
          <div class="info" v-if="isSidebarOpen">
            <div class="name">{{ userInfo.nickname || '超级管理员' }}</div>
            <div class="role">{{ userInfo.role || '管理员' }}</div>
          </div>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">核心功能</div>
          <div class="nav-items">
            <router-link to="/admin" class="nav-item" active-class="active">
              <span class="nav-icon">📊</span>
              <span class="nav-text" v-if="isSidebarOpen">仪表盘</span>
            </router-link>
            <router-link to="/admin/users" class="nav-item" active-class="active">
              <span class="nav-icon">👥</span>
              <span class="nav-text" v-if="isSidebarOpen">用户管理</span>
            </router-link>
            <router-link to="/admin/buildings" class="nav-item" active-class="active">
              <span class="nav-icon">🏢</span>
              <span class="nav-text" v-if="isSidebarOpen">楼栋管理</span>
            </router-link>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">智慧绿能</div>
          <div class="nav-items">
            <div class="nav-item" @click="toggleGreenEnergy">
              <span class="nav-icon">♻️</span>
              <span class="nav-text" v-if="isSidebarOpen">垃圾分类管理</span>
              <span class="nav-arrow" v-if="isSidebarOpen">{{ greenEnergyOpen ? '▼' : '▶' }}</span>
              <div class="sub-nav" v-if="greenEnergyOpen && isSidebarOpen">
                <router-link to="/admin/garbage/classification" class="sub-nav-item">AI垃圾分类</router-link>
                <router-link to="/admin/garbage/records" class="sub-nav-item">分类记录</router-link>
                <router-link to="/admin/garbage/statistics" class="sub-nav-item">分类统计</router-link>
              </div>
            </div>
            <router-link to="/admin/carbon-footprint" class="nav-item" active-class="active">
              <span class="nav-icon">🌍</span>
              <span class="nav-text" v-if="isSidebarOpen">碳足迹管理</span>
            </router-link>
            <router-link to="/admin/green-forum" class="nav-item" active-class="active">
              <span class="nav-icon">💬</span>
              <span class="nav-text" v-if="isSidebarOpen">绿色论坛管理</span>
            </router-link>
            <router-link to="/admin/environment" class="nav-item" active-class="active">
              <span class="nav-icon">🌿</span>
              <span class="nav-text" v-if="isSidebarOpen">环保数据监测</span>
            </router-link>
            <router-link to="/admin/green-points" class="nav-item" active-class="active">
              <span class="nav-icon">🎯</span>
              <span class="nav-text" v-if="isSidebarOpen">绿色积分管理</span>
            </router-link>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">智能建议</div>
          <div class="nav-items">
            <router-link to="/admin/ai-tips" class="nav-item" active-class="active">
              <span class="nav-icon">💡</span>
              <span class="nav-text" v-if="isSidebarOpen">AI生活建议</span>
            </router-link>
            <router-link to="/admin/green-travel" class="nav-item" active-class="active">
              <span class="nav-icon">🚲</span>
              <span class="nav-text" v-if="isSidebarOpen">绿色出行规划</span>
            </router-link>
            <router-link to="/admin/energy-optimization" class="nav-item" active-class="active">
              <span class="nav-icon">⚡</span>
              <span class="nav-text" v-if="isSidebarOpen">家居节能优化</span>
            </router-link>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">健康养生</div>
          <div class="nav-items">
            <router-link to="/admin/health" class="nav-item" active-class="active">
              <span class="nav-icon">🏥</span>
              <span class="nav-text" v-if="isSidebarOpen">健康管理</span>
            </router-link>
            <router-link to="/admin/diet" class="nav-item" active-class="active">
              <span class="nav-icon">🥗</span>
              <span class="nav-text" v-if="isSidebarOpen">饮食养生</span>
            </router-link>
            <router-link to="/admin/knowledge" class="nav-item" active-class="active">
              <span class="nav-icon">📚</span>
              <span class="nav-text" v-if="isSidebarOpen">养生知识库</span>
            </router-link>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">智慧社区</div>
          <div class="nav-items">
            <div class="nav-item" @click="toggleSmartCommunity">
              <span class="nav-icon">🔒</span>
              <span class="nav-text" v-if="isSidebarOpen">智能门禁管理</span>
              <span class="nav-arrow" v-if="isSidebarOpen">{{ smartCommunityOpen ? '▼' : '▶' }}</span>
              <div class="sub-nav" v-if="smartCommunityOpen && isSidebarOpen">
                <router-link to="/admin/access-control/devices" class="sub-nav-item">门禁设备管理</router-link>
                <router-link to="/admin/access-control/permissions" class="sub-nav-item">门禁权限管理</router-link>
                <router-link to="/admin/access-control/records" class="sub-nav-item">进出记录查询</router-link>
              </div>
            </div>
            <div class="nav-item" @click="toggleRepairManagement">
              <span class="nav-icon">🔧</span>
              <span class="nav-text" v-if="isSidebarOpen">物业报修管理</span>
              <span class="nav-arrow" v-if="isSidebarOpen">{{ repairManagementOpen ? '▼' : '▶' }}</span>
              <div class="sub-nav" v-if="repairManagementOpen && isSidebarOpen">
                <router-link to="/admin/repair/orders" class="sub-nav-item">报修工单管理</router-link>
                <router-link to="/admin/repair/technicians" class="sub-nav-item">维修人员管理</router-link>
                <router-link to="/admin/repair/statistics" class="sub-nav-item">报修统计分析</router-link>
              </div>
            </div>
            <router-link to="/admin/notices" class="nav-item" active-class="active">
              <span class="nav-icon">📢</span>
              <span class="nav-text" v-if="isSidebarOpen">公告通知管理</span>
            </router-link>
            <div class="nav-item" @click="toggleUtilityManagement">
              <span class="nav-icon">💡</span>
              <span class="nav-text" v-if="isSidebarOpen">智能水电管理</span>
              <span class="nav-arrow" v-if="isSidebarOpen">{{ utilityManagementOpen ? '▼' : '▶' }}</span>
              <div class="sub-nav" v-if="utilityManagementOpen && isSidebarOpen">
                <router-link to="/admin/utility/meters" class="sub-nav-item">水电表具管理</router-link>
                <router-link to="/admin/utility/usage" class="sub-nav-item">用量数据监控</router-link>
                <router-link to="/admin/utility/alerts" class="sub-nav-item">异常预警处理</router-link>
              </div>
            </div>
            <router-link to="/admin/payment" class="nav-item" active-class="active">
              <span class="nav-icon">💳</span>
              <span class="nav-text" v-if="isSidebarOpen">费用缴纳管理</span>
            </router-link>
            <router-link to="/admin/parking" class="nav-item" active-class="active">
              <span class="nav-icon">🚗</span>
              <span class="nav-text" v-if="isSidebarOpen">智能停车管理</span>
            </router-link>
            <router-link to="/admin/locker" class="nav-item" active-class="active">
              <span class="nav-icon">📦</span>
              <span class="nav-text" v-if="isSidebarOpen">快递柜管理</span>
            </router-link>
            <router-link to="/admin/visitor" class="nav-item" active-class="active">
              <span class="nav-icon">👤</span>
              <span class="nav-text" v-if="isSidebarOpen">访客管理</span>
            </router-link>
            <router-link to="/admin/complaint" class="nav-item" active-class="active">
              <span class="nav-icon">💬</span>
              <span class="nav-text" v-if="isSidebarOpen">投诉建议管理</span>
            </router-link>
            <router-link to="/admin/monitoring" class="nav-item" active-class="active">
              <span class="nav-icon">📹</span>
              <span class="nav-text" v-if="isSidebarOpen">监控管理</span>
            </router-link>
            <router-link to="/admin/activity" class="nav-item" active-class="active">
              <span class="nav-icon">🎉</span>
              <span class="nav-text" v-if="isSidebarOpen">社区活动管理</span>
            </router-link>
          </div>
        </div>
        
        <div class="nav-section">
          <div class="section-title" v-if="isSidebarOpen">系统设置</div>
          <div class="nav-items">
            <router-link to="/admin/settings" class="nav-item" active-class="active">
              <span class="nav-icon">⚙️</span>
              <span class="nav-text" v-if="isSidebarOpen">设置</span>
            </router-link>
            <router-link to="/" class="nav-item">
              <span class="nav-icon">🏠</span>
              <span class="nav-text" v-if="isSidebarOpen">返回前台</span>
            </router-link>
            <a href="#" class="nav-item" @click="logout">
              <span class="nav-icon">🚪</span>
              <span class="nav-text" v-if="isSidebarOpen">退出登录</span>
            </a>
          </div>
        </div>
      </nav>
    </aside>
    
    <!-- 右侧内容区 -->
    <main class="admin-content" :class="{ expanded: !isSidebarOpen }">
      <!-- 顶部导航栏 -->
      <header class="content-header">
        <div class="header-left">
          <button class="toggle-btn" @click="toggleSidebar">
            <span class="toggle-icon">{{ isSidebarOpen ? '☰' : '☰' }}</span>
          </button>
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="header-actions">
            <div class="user-dropdown">
              <button class="user-btn">
                <div class="user-avatar">{{ userInfo.nickname?.charAt(0) || '管' }}</div>
                <span v-if="isSidebarOpen" class="user-name">{{ userInfo.nickname || '管理员' }}</span>
                <span class="dropdown-arrow">▼</span>
              </button>
            </div>
          </div>
        </div>
      </header>
      
      <!-- 内容区域 -->
      <div class="content-body">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const userInfo = ref({})
const isSidebarOpen = ref(true)
const notificationCount = ref(3) // 示例数据
const greenEnergyOpen = ref(false)
const smartCommunityOpen = ref(false)
const repairManagementOpen = ref(false)
const utilityManagementOpen = ref(false)

const pageTitle = computed(() => {
  const titles = {
    '/admin': '仪表盘',
    '/admin/users': '用户管理',
    '/admin/buildings': '楼栋管理',
    '/admin/garbage/classification': 'AI垃圾分类',
    '/admin/garbage/records': '分类记录',
    '/admin/garbage/statistics': '分类统计',
    '/admin/carbon-footprint': '碳足迹管理',
    '/admin/green-forum': '绿色论坛管理',
    '/admin/environment': '环保数据监测',
    '/admin/green-points': '绿色积分管理',
    '/admin/ai-tips': 'AI生活建议',
    '/admin/green-travel': '绿色出行规划',
    '/admin/energy-optimization': '家居节能优化',
    '/admin/health': '健康管理',
    '/admin/diet': '饮食养生',
    '/admin/knowledge': '养生知识库',
    '/admin/settings': '系统设置',
    // 智慧社区管理
    '/admin/access-control/devices': '门禁设备管理',
    '/admin/access-control/permissions': '门禁权限管理',
    '/admin/access-control/records': '进出记录查询',
    '/admin/repair/orders': '报修工单管理',
    '/admin/repair/technicians': '维修人员管理',
    '/admin/repair/statistics': '报修统计分析',
    '/admin/notices': '公告通知管理',
    '/admin/utility/meters': '水电表具管理',
    '/admin/utility/usage': '用量数据监控',
    '/admin/utility/alerts': '异常预警处理',
    '/admin/payment': '费用缴纳管理',
    '/admin/parking': '智能停车管理',
    '/admin/locker': '快递柜管理',
    '/admin/visitor': '访客管理',
    '/admin/complaint': '投诉建议管理',
    '/admin/monitoring': '监控管理',
    '/admin/activity': '社区活动管理'
  }
  return titles[route.path] || '管理中心'
})

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const toggleGreenEnergy = () => {
  greenEnergyOpen.value = !greenEnergyOpen.value
}

const toggleSmartCommunity = () => {
  smartCommunityOpen.value = !smartCommunityOpen.value
}

const toggleRepairManagement = () => {
  repairManagementOpen.value = !repairManagementOpen.value
}

const toggleUtilityManagement = () => {
  utilityManagementOpen.value = !utilityManagementOpen.value
}

const goToHome = () => {
  router.push('/')
}

const logout = () => {
  if (confirm('确定要退出登录吗？')) {
    userStore.logout()
    router.push('/login')
  }
}

const loadStats = async () => {
  try {
    const response = await fetch('/api/v1/admin/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      pendingMerchantCount.value = result.data?.pendingMerchantCount || 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(() => {
  userInfo.value = userStore.userInfo || {}
  loadStats()
  
  // 响应式处理
  window.addEventListener('resize', handleResize)
  handleResize()
})

const handleResize = () => {
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false
  }
}

// 监听路由变化，重新加载统计数据
watch(() => route.path, () => {
  loadStats()
  // 关闭所有展开的菜单
  greenEnergyOpen.value = false
  smartCommunityOpen.value = false
  repairManagementOpen.value = false
  utilityManagementOpen.value = false
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

/* 左侧导航栏 */
.admin-sidebar {
  width: 280px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transition: all 0.3s ease;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow-y: auto;
  z-index: 1000;
}

.admin-sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
}

.logo h1 {
  margin: 0 0 20px 0;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.admin-sidebar.collapsed .avatar {
  margin: 0 auto;
}

.info .name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}

.info .role {
  font-size: 12px;
  opacity: 0.8;
}

.sidebar-nav {
  padding: 20px 0;
}

.nav-section {
  margin-bottom: 30px;
}

.section-title {
  padding: 0 20px 10px;
  font-size: 14px;
  font-weight: 500;
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  border-left: 4px solid #ffd700;
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.nav-text {
  flex: 1;
  font-size: 16px;
  transition: all 0.3s ease;
}

.nav-arrow {
  font-size: 12px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.badge {
  background: #f56c6c;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: bold;
  min-width: 20px;
  text-align: center;
  flex-shrink: 0;
}

/* 子导航 */
.sub-nav {
  background: rgba(255, 255, 255, 0.1);
  margin: 0 10px 5px;
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.sub-nav-item {
  display: block;
  padding: 10px 20px 10px 45px;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 14px;
}

.sub-nav-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(3px);
}

/* 右侧内容区 */
.admin-content {
  flex: 1;
  margin-left: 280px;
  transition: all 0.3s ease;
}

.admin-content.expanded {
  margin-left: 80px;
}

.content-header {
  background: white;
  padding: 0 30px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  color: #667eea;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 搜索框 */
.search-box {
  position: relative;
  width: 300px;
}

.search-input {
  width: 100%;
  padding: 8px 40px 8px 15px;
  border: 1px solid #dcdfe6;
  border-radius: 20px;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #909399;
  font-size: 16px;
}

/* 头部操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.action-btn {
  position: relative;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #606266;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.action-btn:hover {
  background: #f5f7fa;
  color: #667eea;
}

.action-btn .badge {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(25%, -25%);
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  font-size: 11px;
  padding: 0 6px;
}

/* 用户下拉 */
.user-dropdown {
  position: relative;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #303133;
}

.user-btn:hover {
  background: #f5f7fa;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

.user-name {
  font-weight: 500;
  transition: all 0.3s ease;
}

.dropdown-arrow {
  font-size: 12px;
  color: #909399;
  transition: all 0.3s ease;
}

.content-body {
  padding: 30px;
  min-height: calc(100vh - 70px);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .admin-sidebar {
    width: 240px;
  }
  
  .admin-content {
    margin-left: 240px;
  }
  
  .search-box {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }
  
  .admin-sidebar.open {
    transform: translateX(0);
  }
  
  .admin-content {
    margin-left: 0;
  }
  
  .content-header {
    padding: 0 20px;
  }
  
  .content-body {
    padding: 20px;
  }
  
  .admin-info {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .info .name {
    font-size: 14px;
  }
  
  .nav-item {
    padding: 12px 15px;
  }
  
  .nav-text {
    font-size: 14px;
  }
  
  .search-box {
    display: none;
  }
  
  .user-name {
    display: none;
  }
}

@media (max-width: 480px) {
  .content-header {
    height: 60px;
  }
  
  .page-title {
    font-size: 16px;
  }
  
  .content-body {
    padding: 15px;
  }
  
  .header-actions {
    gap: 10px;
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }
}
</style>
