<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <div class="login-header">
        <h2>用户登录</h2>
        <p>欢迎回到智慧社区</p>
      </div>
      
      <div class="login-form">
        <div class="form-tabs">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'password' }"
            @click="activeTab = 'password'"
          >
            手机号+密码
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'code' }"
            @click="activeTab = 'code'"
          >
            手机号+验证码
          </button>
        </div>
        
        <form @submit.prevent="handleLogin">
          <!-- 手机号 -->
          <div class="form-item">
            <label for="phone">手机号</label>
            <input
              type="tel"
              id="phone"
              v-model="form.phone"
              placeholder="请输入手机号"
              maxlength="11"
              required
            />
          </div>
          
          <!-- 密码/验证码 -->
          <div class="form-item">
            <label v-if="activeTab === 'password'" for="password">密码</label>
            <label v-else for="verificationCode">验证码</label>
            
            <div class="password-input" v-if="activeTab === 'password'">
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="form.password"
                placeholder="请输入密码"
                required
              />
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
            
            <div class="code-input" v-else>
              <input
                type="text"
                id="verificationCode"
                v-model="form.verificationCode"
                placeholder="请输入验证码"
                maxlength="6"
                required
              />
              <button 
                type="button" 
                class="send-code-btn"
                :disabled="countdown > 0"
                @click="sendVerificationCode"
              >
                {{ countdown > 0 ? `${countdown}s` : '发送验证码' }}
              </button>
            </div>
          </div>
          
          <!-- 记住密码 -->
          <div class="form-options" v-if="activeTab === 'password'">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.rememberMe" />
              记住密码
            </label>
            <a href="#" class="forgot-password">忘记密码？</a>
          </div>
          
          <!-- 登录按钮 -->
          <button type="submit" class="login-btn" :disabled="isLoading">
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </form>
        
        <!-- 第三方登录 -->
        <div class="third-party-login">
          <div class="divider">
            <span>其他登录方式</span>
          </div>
          <div class="third-party-icons">
            <button class="third-party-btn wechat">
              <span>微信</span>
            </button>
            <button class="third-party-btn alipay">
              <span>支付宝</span>
            </button>
          </div>
        </div>
        
        <!-- 注册链接 -->
        <div class="register-link">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/request'

// 状态
const activeTab = ref('password')
const showPassword = ref(false)
const countdown = ref(0)
const isLoading = ref(false)
const router = useRouter()
const userStore = useUserStore()

// 表单数据
const form = reactive({
  phone: '',
  password: '',
  verificationCode: '',
  rememberMe: false
})

// 方法
const sendVerificationCode = async () => {
  if (!form.phone || form.phone.length !== 11) {
    alert('请输入正确的手机号')
    return
  }
  
  // 模拟发送验证码
  console.log('发送验证码到:', form.phone)
  
  // 开始倒计时
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const handleLogin = async () => {
  // 表单验证
  if (!form.phone) {
    alert('请输入手机号')
    return
  }
  
  if (activeTab.value === 'password' && !form.password) {
    alert('请输入密码')
    return
  }
  
  if (activeTab.value === 'code' && !form.verificationCode) {
    alert('请输入验证码')
    return
  }
  
  isLoading.value = true
  
  try {
    // 使用真实的后端登录接口
    console.log('使用真实登录')
    
    const response = await axios.post('/v1/pc/auth/login', {
      phone: form.phone,
      password: form.password,
      platformType: 'pc'
    })
    
    if (response.data.code === 0) {
      const { token, refreshToken, userInfo } = response.data.data
      console.log('登录成功，用户信息:', userInfo)
      
      // 保存用户信息和token
      userStore.token = token
      userStore.refreshToken = refreshToken
      userStore.userInfo = userInfo
      userStore.isLoggedIn = true
      
      // 存储到本地
      localStorage.setItem('token', token)
      localStorage.setItem('refreshToken', refreshToken)
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
      
      // 设置请求头
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      console.log('用户信息已保存，准备跳转')

      // 根据角色跳转到不同页面
      const userRole = userInfo.role || '居民'
      console.log('用户角色:', userRole)

      if (userRole === '管理员') {
        // 管理员跳转到管理员仪表盘
        await router.push('/admin')
        console.log('管理员跳转完成')
      } else if (userRole === '运营') {
        // 运营人员跳转到商品管理页面
        await router.push('/op/goods')
        console.log('运营人员跳转完成')
      } else if (userRole === '物业管理员') {
        // 物业管理员跳转到物业管理页面
        await router.push('/property/dashboard')
        console.log('物业管理员跳转完成')
      } else {
        // 普通用户跳转到首页
        await router.push('/')
        console.log('普通用户跳转完成')
      }
    } else {
      alert('登录失败: ' + response.data.msg)
    }
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查网络连接')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-form-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  margin: 0 0 10px;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.login-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.form-tabs {
  display: flex;
  margin-bottom: 24px;
  border-bottom: 1px solid #e8e8e8;
}

.tab-btn {
  flex: 1;
  padding: 12px 0;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  color: #2196F3;
  border-bottom-color: #2196F3;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-item input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-item input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.code-input {
  display: flex;
  gap: 12px;
}

.code-input input {
  flex: 1;
}

.send-code-btn {
  padding: 0 16px;
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.send-code-btn:hover:not(:disabled) {
  background: #e8e8e8;
}

.send-code-btn:disabled {
  color: #999;
  cursor: not-allowed;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #666;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

.forgot-password {
  color: #2196F3;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-password:hover {
  color: #1976D2;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
  margin-bottom: 24px;
}

.login-btn:hover:not(:disabled) {
  background: #1976D2;
}

.login-btn:disabled {
  background: #90CAF9;
  cursor: not-allowed;
}

.third-party-login {
  margin-bottom: 20px;
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
  color: #999;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e8e8e8;
}

.divider span {
  padding: 0 16px;
  white-space: nowrap;
}

.third-party-icons {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.third-party-btn {
  width: 48px;
  height: 48px;
  border: 1px solid #e8e8e8;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #666;
}

.third-party-btn:hover {
  border-color: #2196F3;
  color: #2196F3;
  transform: translateY(-2px);
}

.third-party-btn.wechat:hover {
  border-color: #07C160;
  color: #07C160;
}

.third-party-btn.alipay:hover {
  border-color: #1677FF;
  color: #1677FF;
}

.register-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-link router-link {
  color: #2196F3;
  text-decoration: none;
  margin-left: 4px;
  transition: color 0.3s;
}

.register-link router-link:hover {
  color: #1976D2;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-form-wrapper {
    padding: 30px 20px;
  }
  
  .login-header h2 {
    font-size: 20px;
  }
}
</style>