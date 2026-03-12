<template>
  <div class="home-page">
    <!-- 轮播横幅 -->
    <section class="banner-section">
      <div class="banner-slider">
        <div 
          v-for="(banner, index) in banners" 
          :key="banner.id"
          v-show="currentBannerIndex === index"
          class="banner-slide"
        >
          <div class="banner-content">
            <h2>{{ banner.title }}</h2>
            <p>{{ banner.subtitle }}</p>
            <el-button type="primary" size="large" @click="handleBannerClick(banner)">
              {{ banner.buttonText }}
            </el-button>
          </div>
        </div>
        <div class="banner-dots">
          <span 
            v-for="(banner, index) in banners" 
            :key="banner.id"
            class="dot"
            :class="{ active: currentBannerIndex === index }"
            @click="currentBannerIndex = index"
          ></span>
        </div>
      </div>
    </section>

    <!-- 公告通知区 -->
    <section class="notices-section">
      <div class="section-header">
        <h2 class="section-title">
          <el-icon><i-ep-message /></el-icon>
          最新公告
        </h2>
        <el-button link @click="$router.push('/notices')">查看全部</el-button>
      </div>
      <div class="notices-grid">
        <div 
          v-for="notice in latestNotices" 
          :key="notice.id" 
          class="notice-card"
          @click="goToNoticeDetail(notice.id)"
        >
          <div class="notice-header">
            <h3 class="notice-title">{{ notice.title }}</h3>
            <span class="notice-date">{{ formatDate(notice.publish_time) }}</span>
          </div>
          <p class="notice-content">{{ truncateContent(notice.content, 100) }}</p>
          <div class="notice-footer">
            <span class="notice-author">{{ notice.author }}</span>
            <el-tag :type="getStatusTag(notice.status)" size="small">{{ getStatusText(notice.status) }}</el-tag>
          </div>
        </div>
        <div v-if="latestNotices.length === 0" class="no-notices">
          <el-empty description="暂无公告" />
        </div>
      </div>
    </section>

    <!-- AI推荐区 -->
    <section class="recommend-section">
      <div class="section-header">
        <h2 class="section-title">
          <el-icon><Star /></el-icon>
          为你推荐
        </h2>
        <el-button link @click="refreshRecommendations">换一批</el-button>
      </div>
      <div class="recommend-grid">
        <div 
          v-for="item in recommendations" 
          :key="item.item_id" 
          class="recommend-card"
          @click="goToDetail(item)"
        >
          <div class="card-image">
            <img :src="item.image || '/images/default-goods.jpg'" :alt="item.name">
            <div class="card-tags">
              <el-tag v-for="tag in item.tags" :key="tag" size="small" effect="plain">
                {{ tag }}
              </el-tag>
            </div>
          </div>
          <div class="card-content">
            <h3>{{ item.name }}</h3>
            <p class="card-price">¥{{ item.price }}</p>
            <p class="card-reason">{{ item.reason }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心服务模块 -->
    <section class="services-section">
      <h2 class="section-title">智慧社区</h2>
      <div class="services-grid">
        <div class="service-card" @click="$router.push('/access-control')">
          <el-icon class="service-icon" :size="48">
            <i-ep-lock />
          </el-icon>
          <h3>智能门禁</h3>
          <p>人脸识别、门禁记录、权限管理</p>
        </div>
        <div class="service-card" @click="$router.push('/repair')">
          <el-icon class="service-icon" :size="48">
            <i-ep-wrench />
          </el-icon>
          <h3>物业报修</h3>
          <p>在线报修、进度查询、维修评价</p>
        </div>
        <div class="service-card" @click="$router.push('/notices')">
          <el-icon class="service-icon" :size="48">
            <i-ep-message />
          </el-icon>
          <h3>公告通知</h3>
          <p>社区公告、活动通知、重要提醒</p>
        </div>
        <div class="service-card" @click="$router.push('/utility')">
          <el-icon class="service-icon" :size="48">
            <i-ep-light />
          </el-icon>
          <h3>智能水电</h3>
          <p>用量监控、异常预警、费用查询</p>
        </div>
        <div class="service-card" @click="$router.push('/payment')">
          <el-icon class="service-icon" :size="48">
            <i-ep-credit-card />
          </el-icon>
          <h3>费用缴纳</h3>
          <p>物业费、水电费、停车费缴纳</p>
        </div>
        <div class="service-card" @click="$router.push('/parking')">
          <el-icon class="service-icon" :size="48">
            <i-ep-car />
          </el-icon>
          <h3>智能停车</h3>
          <p>车位管理、车辆登记、停车缴费</p>
        </div>
        <div class="service-card" @click="$router.push('/locker')">
          <el-icon class="service-icon" :size="48">
            <i-ep-box />
          </el-icon>
          <h3>快递柜</h3>
          <p>包裹管理、取件通知、异常处理</p>
        </div>
        <div class="service-card" @click="$router.push('/visitor')">
          <el-icon class="service-icon" :size="48">
            <i-ep-user />
          </el-icon>
          <h3>访客管理</h3>
          <p>访客预约、临时门禁、进出记录</p>
        </div>
        <div class="service-card" @click="$router.push('/complaint')">
          <el-icon class="service-icon" :size="48">
            <i-ep-chat-line-round />
          </el-icon>
          <h3>投诉建议</h3>
          <p>在线投诉、处理进度、满意度评价</p>
        </div>
      </div>
    </section>

    <!-- AI垃圾分类 -->
    <section class="ai-garbage-section">
      <div class="ai-garbage-content">
        <div class="ai-garbage-text">
          <h2>AI垃圾分类识别</h2>
          <p>拍照识别垃圾类型，获取投放建议</p>
          <p class="ai-stats">已识别 <span class="highlight">10,000+</span> 次</p>
          <el-button type="primary" size="large" @click="showGarbageModal = true">
            立即体验
          </el-button>
        </div>
        <div class="ai-garbage-demo">
          <div class="demo-image">
            <el-image src="/images/garbage-demo.jpg" fit="cover" />
          </div>
        </div>
      </div>
    </section>

    <!-- 数据统计区 -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-item">
          <el-statistic :value="12800" title="社区用户" />
          <p class="stat-label">注册用户</p>
          <p class="stat-trend">+12% 本月新增</p>
        </div>
        <div class="stat-item">
          <el-statistic :value="5600" title="团购订单" />
          <p class="stat-label">本月订单</p>
          <p class="stat-trend">+8% 环比增长</p>
        </div>
        <div class="stat-item">
          <el-statistic :value="320" title="社区活动" />
          <p class="stat-label">累计活动</p>
          <p class="stat-trend">+25 本月新增</p>
        </div>
        <div class="stat-item">
          <el-statistic :value="98" title="满意度" suffix="%" />
          <p class="stat-label">用户满意度</p>
          <p class="stat-trend">持续提升中</p>
        </div>
      </div>
    </section>

    <!-- 垃圾分类弹窗 -->
    <el-dialog
      v-model="showGarbageModal"
      title="AI垃圾分类识别"
      width="500px"
      destroy-on-close
    >
      <div class="garbage-modal-content">
        <el-upload
          class="garbage-uploader"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleGarbageImageChange"
          drag
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            拖拽图片到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 jpg/png 格式，文件大小不超过 5MB
            </div>
          </template>
        </el-upload>

        <div v-if="garbageResult" class="garbage-result">
          <el-divider />
          <h4>识别结果</h4>
          <div class="result-item">
            <span class="result-label">垃圾类型：</span>
            <el-tag :type="getGarbageTagType(garbageResult.category)" size="large">
              {{ garbageResult.category }}
            </el-tag>
          </div>
          <div class="result-item">
            <span class="result-label">置信度：</span>
            <el-progress :percentage="garbageResult.confidence * 100" :format="format" />
          </div>
          <div class="result-item">
            <span class="result-label">投放建议：</span>
            <p>{{ garbageResult.disposal_method }}</p>
          </div>
          <div v-if="garbageResult.recommended_activities.length > 0" class="result-item">
            <span class="result-label">推荐活动：</span>
            <div class="activity-tags">
              <el-tag 
                v-for="activity in garbageResult.recommended_activities" 
                :key="activity"
                type="success"
                effect="plain"
              >
                {{ activity }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Star, ShoppingCart, Calendar, Service, OfficeBuilding, UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

// 当前轮播图索引
const currentBannerIndex = ref(0)

// 轮播图数据
const banners = ref([
  {
    id: 1,
    title: '智慧社区，美好生活',
    subtitle: '一站式社区服务平台，让生活更便捷',
    buttonText: '了解更多',
    link: '/services'
  },
  {
    id: 2,
    title: '智能门禁，安全守护',
    subtitle: '人脸识别、远程开门，保障社区安全',
    buttonText: '查看详情',
    link: '/services'
  },
  {
    id: 3,
    title: '精彩活动，等你来参与',
    subtitle: '亲子互动、文化娱乐、公益活动',
    buttonText: '查看活动',
    link: '/activities'
  },
  {
    id: 4,
    title: '智慧绿能，节能环保',
    subtitle: '智能水电管理，绿色生活从社区开始',
    buttonText: '了解更多',
    link: '/green-energy'
  },
  {
    id: 5,
    title: '智能停车，便捷出行',
    subtitle: '车位预约、智能导航，让停车更简单',
    buttonText: '查看详情',
    link: '/services'
  },
  {
    id: 6,
    title: '政务服务，一键办理',
    subtitle: '在线办理各类政务，足不出户轻松搞定',
    buttonText: '立即办理',
    link: '/government'
  }
])

// 推荐数据
const recommendations = ref([])

// 最新公告
const latestNotices = ref([])

// 垃圾分类
const showGarbageModal = ref(false)
const garbageResult = ref(null)

// 方法
const handleBannerClick = (banner) => {
  router.push(banner.link)
}

const fetchRecommendations = async () => {
  try {
    const userId = localStorage.getItem('userId') || 1
    const response = await axios.post('/api/v1/ai/recommend', {
      user_id: parseInt(userId),
      platform_type: 'pc',
      scene: 'home',
      limit: 8
    })
    
    if (response.data.code === 0) {
      recommendations.value = response.data.data.recommendations
    }
  } catch (error) {
    console.error('获取推荐失败:', error)
    // 使用默认数据
    recommendations.value = [
      { item_id: 1, name: '新鲜水果套餐', price: 99, tags: ['新鲜', '健康'], reason: '基于您的兴趣推荐', image: '/images/fruit.jpg' },
      { item_id: 2, name: '社区健身卡', price: 199, tags: ['运动', '健康'], reason: '热门商品', image: '/images/gym.jpg' },
      { item_id: 3, name: '亲子活动门票', price: 120, tags: ['亲子', '教育'], reason: '新用户专享', image: '/images/family.jpg' },
      { item_id: 4, name: '有机蔬菜包', price: 68, tags: ['有机', '健康'], reason: '限时优惠', image: '/images/vegetable.jpg' }
    ]
  }
}

const fetchLatestNotices = async () => {
  try {
    const response = await axios.get('/api/v1/pc/notices', {
      params: {
        page: 1,
        pageSize: 3,
        status: 'published'
      }
    })
    
    if (response.data.code === 0) {
      latestNotices.value = response.data.data.list
    }
  } catch (error) {
    console.error('获取最新公告失败:', error)
    // 使用默认数据
    latestNotices.value = [
      {
        id: 1,
        title: '社区停水通知',
        content: '因管道维修，本周末将暂停供水，请各位业主提前做好储水准备。具体停水时间：周六上午9:00至下午18:00。给您带来不便，敬请谅解。',
        author: '物业管理员',
        publish_time: new Date().toISOString(),
        status: 'published'
      },
      {
        id: 2,
        title: '小区活动通知',
        content: '本周末将在社区中心举办亲子活动，欢迎各位业主带着孩子参加。活动内容包括手工制作、游戏互动等，还有小礼品赠送。',
        author: '活动组',
        publish_time: new Date(Date.now() - 86400000).toISOString(),
        status: 'published'
      }
    ]
  }
}

const refreshRecommendations = () => {
  fetchRecommendations()
}

const goToDetail = (item) => {
  if (item.item_type === 'goods') {
    router.push(`/group-buy/detail/${item.item_id}`)
  } else {
    router.push(`/activities/detail/${item.item_id}`)
  }
}

const goToNoticeDetail = (noticeId) => {
  router.push(`/notices/detail/${noticeId}`)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const truncateContent = (content, length) => {
  if (!content) return ''
  // 移除HTML标签
  const plainText = content.replace(/<[^>]*>/g, '')
  return plainText.length > length ? plainText.substring(0, length) + '...' : plainText
}

const getStatusText = (status) => {
  const statuses = {
    'published': '已发布',
    'draft': '草稿',
    'expired': '已过期'
  }
  return statuses[status] || status
}

const getStatusTag = (status) => {
  const tags = {
    'published': 'success',
    'draft': 'info',
    'expired': 'danger'
  }
  return tags[status] || 'default'
}

const handleGarbageImageChange = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file.raw)
    
    const response = await axios.post('/api/v1/ai/garbage/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data.code === 0) {
      garbageResult.value = response.data.data.result
    }
  } catch (error) {
    console.error('垃圾分类识别失败:', error)
    // 模拟结果
    garbageResult.value = {
      category: '可回收物',
      confidence: 0.92,
      disposal_method: '清洁干燥后投放至可回收物收集容器',
      recommended_activities: ['社区回收日活动', '旧物改造手工课']
    }
  }
}

const getGarbageTagType = (category) => {
  const types = {
    '可回收物': 'success',
    '有害垃圾': 'danger',
    '厨余垃圾': 'warning',
    '其他垃圾': 'info'
  }
  return types[category] || 'info'
}

const format = (percentage) => `${percentage.toFixed(1)}%`

onMounted(() => {
  fetchRecommendations()
  fetchLatestNotices()
  
  // 自动轮播
  setInterval(() => {
    currentBannerIndex.value = (currentBannerIndex.value + 1) % banners.value.length
  }, 5000)
})
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 轮播区域 */
.banner-section {
  margin-bottom: 40px;
}

.banner-slider {
  position: relative;
  height: 400px;
  overflow: hidden;
  border-radius: 8px;
}

.banner-slide {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transition: all 0.5s ease;
}

/* 轮播图背景颜色 */
.banner-slide:nth-child(1) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.banner-slide:nth-child(2) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.banner-slide:nth-child(3) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.banner-slide:nth-child(4) {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.banner-slide:nth-child(5) {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.banner-slide:nth-child(6) {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.banner-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 2;
}

.banner-dots .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.3s;
}

.banner-dots .dot.active {
  background: white;
}

.banner-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.banner-content h2 {
  font-size: 36px;
  margin-bottom: 16px;
}

.banner-content p {
  font-size: 18px;
  margin-bottom: 24px;
}

/* 推荐区域 */
.recommend-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 24px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.recommend-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.recommend-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-image {
  height: 160px;
  position: relative;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-tags {
  position: absolute;
  bottom: 8px;
  left: 8px;
  display: flex;
  gap: 4px;
}

.card-content {
  padding: 12px;
}

.card-content h3 {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-price {
  font-size: 18px;
  color: #FF9800;
  font-weight: bold;
  margin-bottom: 4px;
}

.card-reason {
  font-size: 12px;
  color: #999;
}

/* 服务区域 */
.services-section {
  margin-bottom: 40px;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.service-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.service-icon {
  color: #2196F3;
  margin-bottom: 16px;
}

.service-card h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 8px;
}

.service-card p {
  font-size: 14px;
  color: #666;
}

/* AI垃圾分类区域 */
.ai-garbage-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 40px;
  margin-bottom: 40px;
  color: white;
}

.ai-garbage-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ai-garbage-text {
  flex: 1;
}

.ai-garbage-text h2 {
  font-size: 28px;
  margin-bottom: 16px;
}

.ai-garbage-text p {
  font-size: 16px;
  margin-bottom: 12px;
  opacity: 0.9;
}

.ai-stats {
  font-size: 14px;
  margin-bottom: 20px;
}

.highlight {
  color: #FF9800;
  font-weight: bold;
  font-size: 20px;
}

.ai-garbage-demo {
  flex: 0 0 300px;
}

.demo-image {
  width: 280px;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

/* 统计区域 */
.stats-section {
  margin-bottom: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-item {
  background: white;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.stat-trend {
  font-size: 12px;
  color: #52c41a;
  margin-top: 4px;
}

/* 垃圾分类弹窗 */
.garbage-modal-content {
  padding: 20px 0;
}

.garbage-uploader {
  text-align: center;
}

.garbage-result {
  margin-top: 20px;
}

.result-item {
  margin-bottom: 16px;
}

.result-label {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  display: block;
}

.activity-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 公告通知区域 */
.notices-section {
  margin-bottom: 40px;
}

.notices-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.notice-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.notice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.notice-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
  flex: 1;
  margin-right: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notice-date {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
}

.notice-content {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.notice-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notice-author {
  font-size: 12px;
  color: #999;
}

.no-notices {
  grid-column: 1 / -1;
  padding: 40px 0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .recommend-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .services-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .notices-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .recommend-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .notices-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-garbage-content {
    flex-direction: column;
    text-align: center;
  }
  
  .ai-garbage-demo {
    margin-top: 20px;
  }
}
</style>