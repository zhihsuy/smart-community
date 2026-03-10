<template>
  <div class="register-container">
    <div class="register-form-wrapper">
      <div class="register-header">
        <h2>用户注册</h2>
        <p>加入智慧社区，享受便捷服务</p>
      </div>
      
      <form class="register-form" @submit.prevent="handleRegister">
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
        
        <!-- 验证码 -->
        <div class="form-item">
          <label for="verificationCode">验证码</label>
          <div class="code-input">
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
        
        <!-- 密码 -->
        <div class="form-item">
          <label for="password">密码</label>
          <div class="password-input">
            <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="form.password"
                placeholder="请设置密码（6-20位）"
                minlength="6"
                maxlength="20"
                required
              />
            <button type="button" class="toggle-password" @click="showPassword = !showPassword">
              {{ showPassword ? '👁️' : '👁️‍🗨️' }}
            </button>
          </div>
        </div>
        
        <!-- 确认密码 -->
        <div class="form-item">
          <label for="confirmPassword">确认密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="form.confirmPassword"
            placeholder="请再次输入密码"
            minlength="6"
            maxlength="20"
            required
          />
        </div>
        
        <!-- 用户名/昵称 -->
        <div class="form-item">
          <label for="nickname">用户名（选填）</label>
          <input
            type="text"
            id="nickname"
            v-model="form.nickname"
            placeholder="不填则随机生成用户名"
            maxlength="20"
          />
          <small class="field-hint">留空将为您自动生成一个随机用户名</small>
        </div>
        
        <!-- 家庭结构 -->
        <div class="form-item">
          <label>家庭结构</label>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" v-model="form.familyStructure" value="老人" />
              <span>老人</span>
            </label>
            <label class="radio-label">
              <input type="radio" v-model="form.familyStructure" value="宝妈" />
              <span>宝妈</span>
            </label>
            <label class="radio-label">
              <input type="radio" v-model="form.familyStructure" value="普通居民" />
              <span>普通居民</span>
            </label>
          </div>
        </div>
        
        <!-- 居住楼栋 -->
        <div class="form-item">
          <label for="buildingId">居住楼栋</label>
          <select id="buildingId" v-model="form.buildingId" required>
            <option value="">请选择楼栋</option>
            <option value="1">1号楼</option>
            <option value="2">2号楼</option>
            <option value="3">3号楼</option>
            <option value="4">4号楼</option>
            <option value="5">5号楼</option>
          </select>
        </div>
        
        <!-- 同意协议 -->
        <div class="form-agreement">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.agreeTerms" required />
            <span>我已阅读并同意</span>
            <a href="#" class="agreement-link">《用户服务协议》</a>
            <span>和</span>
            <a href="#" class="agreement-link">《隐私政策》</a>
          </label>
        </div>
        
        <!-- 注册按钮 -->
        <button type="submit" class="register-btn" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <!-- 登录链接 -->
      <div class="login-link">
        已有账号？
        <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/request'

// 状态
const showPassword = ref(false)
const countdown = ref(0)
const isLoading = ref(false)
const router = useRouter()

// 表单数据
const form = reactive({
  phone: '',
  verificationCode: '',
  password: '',
  confirmPassword: '',
  nickname: '',
  familyStructure: '普通居民',
  buildingId: '',
  agreeTerms: false
})

// 生成随机用户名
const generateRandomNickname = () => {
  const prefixes = ['快乐', '开心', '幸运', '阳光', '智慧', '勇敢', '温柔', '可爱', '活力', '梦想']
  const suffixes = ['小熊', '猫咪', '狗狗', '兔子', '小鸟', '鱼儿', '小鹿', '小马', '小羊', '小猪']
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)]
  const suffix = suffixes[Math.floor(Math.random() * suffixes.length)]
  const randomNum = Math.floor(Math.random() * 1000)
  return `${prefix}${suffix}${randomNum}`
}

// 方法
const sendVerificationCode = async () => {
  if (!form.phone || form.phone.length !== 11) {
    alert('请输入正确的手机号')
    return
  }
  
  try {
    // 调用后端发送验证码API
    const response = await axios.post('/v1/pc/auth/send-code', {
      phone: form.phone
    })
    
    if (response.data.code === 0) {
      alert('验证码已发送')
      // 开始倒计时
      countdown.value = 60
      const timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    } else {
      alert(response.data.msg || '验证码发送失败')
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    alert('验证码发送失败，请重试')
  }
}

const handleRegister = async () => {
  // 表单验证
  if (form.password !== form.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  if (!form.agreeTerms) {
    alert('请阅读并同意用户协议')
    return
  }
  
  isLoading.value = true
  
  try {
    // 如果没有填写昵称，生成随机昵称
    const nickname = form.nickname.trim() || generateRandomNickname()
    
    // 调用后端注册API
    const registerData = {
      phone: form.phone,
      password: form.password,
      code: form.verificationCode,
      nickname: nickname,
      platformType: 'pc'
    }
    
    console.log('注册请求:', registerData)
    
    const response = await axios.post('/v1/pc/auth/register', registerData)
    
    if (response.data.code === 0) {
      alert('注册成功！请登录')
      // 跳转到登录页面
      router.push('/login')
    } else {
      alert(response.data.msg || '注册失败，请重试')
    }
  } catch (error) {
    console.error('注册失败:', error)
    if (error.response && error.response.data) {
      alert(error.response.data.msg || '注册失败，请重试')
    } else {
      alert('注册失败，请检查网络连接')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-form-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  margin: 0 0 10px;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.register-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
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

.form-item input,
.form-item select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-item input:focus,
.form-item select:focus {
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

.radio-group {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #666;
  font-size: 14px;
}

.radio-label input[type="radio"] {
  width: auto;
}

.form-agreement {
  margin: 24px 0;
  font-size: 12px;
  line-height: 1.5;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  cursor: pointer;
  color: #666;
}

.checkbox-label input[type="checkbox"] {
  margin-top: 2px;
  width: auto;
}

.agreement-link {
  color: #2196F3;
  text-decoration: none;
  transition: color 0.3s;
}

.agreement-link:hover {
  color: #1976D2;
  text-decoration: underline;
}

.register-btn {
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
  margin-bottom: 20px;
}

.register-btn:hover:not(:disabled) {
  background: #1976D2;
}

.register-btn:disabled {
  background: #90CAF9;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-link router-link {
  color: #2196F3;
  text-decoration: none;
  margin-left: 4px;
  transition: color 0.3s;
}

.login-link router-link:hover {
  color: #1976D2;
}

.field-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-form-wrapper {
    padding: 30px 20px;
  }
  
  .register-header h2 {
    font-size: 20px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 12px;
  }
}
</style>