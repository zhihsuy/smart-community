<template>
  <div class="app-container">
    <!-- 顶部导航 - 在管理员页面隐藏 -->
    <header v-if="!isAdminPage" class="app-header">
      <div class="header-content">
        <div class="logo">
          <h1>智慧社区</h1>
        </div>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/green-energy" class="nav-item">智慧绿能</router-link>
          <router-link to="/activities" class="nav-item">活动</router-link>
          <router-link to="/services" class="nav-item">服务</router-link>
          <router-link to="/government" class="nav-item">政务</router-link>
        </nav>
        <div class="user-info">
          <template v-if="userStore.isLoggedIn">
            <div class="user-menu-container">
              <div class="user-dropdown-trigger" @click="toggleMenu">
                <img 
                  v-if="userStore.userInfo.avatar" 
                  :src="userStore.userInfo.avatar" 
                  class="user-avatar" 
                  alt="头像"
                />
                <div v-else class="user-avatar-placeholder">
                  {{ (userStore.userInfo.nickname || userStore.userInfo.phone || '用户').charAt(0) }}
                </div>
                <span class="user-name">{{ userStore.userInfo.nickname || userStore.userInfo.phone }}</span>
                <span class="dropdown-arrow" :class="{ 'is-open': showMenu }">▼</span>
              </div>
              <div class="user-dropdown-menu" v-if="showMenu">
                <div class="dropdown-item" @click="goToProfile">
                  <span class="item-icon">👤</span>
                  <span>个人中心</span>
                </div>
                <div class="dropdown-item" @click="goToOrders">
                  <span class="item-icon">📋</span>
                  <span>我的订单</span>
                </div>
                <div class="dropdown-item" v-if="userStore.userInfo.role === '管理员'" @click="goToAdmin">
                  <span class="item-icon">⚙️</span>
                  <span>管理后台</span>
                </div>
                <div class="dropdown-divider"></div>
                <div class="dropdown-item logout" @click="logout">
                  <span class="item-icon">🚪</span>
                  <span>退出登录</span>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">登录</router-link>
            <router-link to="/register" class="register-btn">注册</router-link>
          </template>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="app-main">
      <router-view />
    </main>

    <!-- 底部信息 - 在管理员页面隐藏 -->
    <footer v-if="!isAdminPage" class="app-footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于我们</h3>
          <p>智慧社区致力于为居民提供便捷的社区服务</p>
        </div>
        <div class="footer-section">
          <h3>联系我们</h3>
          <p>客服热线: 400-123-4567</p>
          <p>邮箱: service@smartcommunity.com</p>
        </div>
        <div class="footer-section">
          <h3>关注我们</h3>
          <div class="social-icons">
            <span class="icon">微信</span>
            <span class="icon">微博</span>
            <span class="icon">抖音</span>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 智慧社区 版权所有</p>
      </div>
    </footer>

    <!-- AI智能客服 - 在管理员页面隐藏 -->
    <div v-if="!isAdminPage" class="ai-assistant" @click="showAiAssistant = true">
      <button class="ai-btn">
        💬
      </button>
    </div>

    <!-- AI客服弹窗 -->
    <div v-if="showAiAssistant" class="ai-chat-modal">
      <div class="ai-chat-container">
        <div class="ai-chat-header">
          <h3>AI智能客服</h3>
          <button class="close-btn" @click="showAiAssistant = false">×</button>
        </div>
        <div class="chat-messages">
          <div class="message ai-message">
            <p>您好！我是智慧社区的AI客服，有什么可以帮助您的吗？</p>
          </div>
          <!-- 聊天记录 -->
        </div>
        <div class="chat-input">
          <input
            v-model="chatInput"
            placeholder="请输入您的问题..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from './stores/user'

// 状态
const showAiAssistant = ref(false)
const chatInput = ref('')
const showMenu = ref(false)
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// 判断是否为管理员页面
const isAdminPage = computed(() => {
  return route.path.startsWith('/admin') || route.path.startsWith('/op')
})

// 初始化登录状态
onMounted(() => {
  userStore.initLoginState()
  console.log('App mounted, isLoggedIn:', userStore.isLoggedIn)
  console.log('userInfo:', userStore.userInfo)
})

// 方法
const sendMessage = () => {
  if (chatInput.value.trim()) {
    console.log('发送消息:', chatInput.value)
    chatInput.value = ''
  }
}

const toggleMenu = () => {
  console.log('toggleMenu called, current state:', showMenu.value)
  showMenu.value = !showMenu.value
  console.log('new state:', showMenu.value)
}

const closeMenu = () => {
  showMenu.value = false
}

const goToProfile = () => {
  showMenu.value = false
  setTimeout(() => {
    router.push('/profile')
  }, 10)
}

const goToOrders = () => {
  showMenu.value = false
  setTimeout(() => {
    router.push('/orders')
  }, 10)
}

const goToAdmin = () => {
  showMenu.value = false
  setTimeout(() => {
    router.push('/admin')
  }, 10)
}

const logout = () => {
  showMenu.value = false
  userStore.logout()
  router.push('/')
}

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  // 只在菜单打开时处理
  if (!showMenu.value) return
  
  const userMenu = document.querySelector('.user-menu-container')
  if (userMenu && !userMenu.contains(event.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  // document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  // document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #2196F3;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo h1 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #FF9800;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: white;
  padding: 4px 8px;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.user-dropdown-trigger:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.user-avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: white;
  border: 2px solid white;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 10px;
  margin-left: 4px;
  transition: transform 0.3s;
}

.dropdown-arrow.is-open {
  transform: rotate(180deg);
}

.user-menu-container {
  position: relative;
}

.user-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 160px;
  z-index: 9999;
  overflow: hidden;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #333;
  font-size: 14px;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.dropdown-item.logout {
  color: #f56c6c;
}

.dropdown-item.logout:hover {
  background-color: #fef0f0;
}

.item-icon {
  font-size: 16px;
}

.dropdown-divider {
  height: 1px;
  background-color: #e4e7ed;
  margin: 4px 0;
}

.login-btn, .register-btn {
  padding: 6px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  border: 1px solid white;
}

.login-btn {
  color: white;
}

.register-btn {
  background: #FF9800;
  color: white;
  border: 1px solid #FF9800;
}

.app-main {
  flex: 1;
  padding: 20px 0;
}

.app-footer {
  background: #333;
  color: white;
  padding: 30px 0 20px;
  margin-top: 40px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 40px;
}

.footer-section {
  flex: 1;
  min-width: 200px;
}

.footer-section h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #FF9800;
}

.footer-section p {
  font-size: 14px;
  color: #ccc;
  margin: 5px 0;
}

.social-icons {
  display: flex;
  gap: 15px;
}

.icon {
  width: 36px;
  height: 36px;
  background: #444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.icon:hover {
  background: #FF9800;
}

.footer-bottom {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #555;
  font-size: 14px;
  color: #999;
}

.ai-assistant {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 999;
}

.ai-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #2196F3;
  color: white;
  border: none;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s;
}

.ai-btn:hover {
  transform: scale(1.1);
}

.ai-chat-modal {
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

.ai-chat-container {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.ai-chat-header {
  padding: 16px;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-chat-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  max-height: 300px;
}

.message {
  margin-bottom: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  max-width: 80%;
}

.ai-message {
  background: #f5f5f5;
  align-self: flex-start;
}

.user-message {
  background: #2196F3;
  color: white;
  align-self: flex-end;
  margin-left: auto;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e8e8e8;
  display: flex;
  gap: 8px;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  font-size: 14px;
}

.chat-input button {
  padding: 8px 16px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>