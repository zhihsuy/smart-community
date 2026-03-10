<template>
  <div class="green-forum">
    <div class="page-header">
      <h1>🌱 绿色社区论坛</h1>
      <p>分享绿色生活经验，共同建设美好社区</p>
    </div>

    <div class="content-section">
      <!-- 发布新帖子 -->
      <div class="post-create-card">
        <h3>📝 发布新帖子</h3>
        <div class="post-form">
          <el-input
            v-model="newPost.title"
            placeholder="请输入帖子标题"
            class="mb-3"
          />
          <el-select
            v-model="newPost.category"
            placeholder="请选择话题分类"
            class="mb-3 w-full"
          >
            <el-option label="绿色生活" value="green-life" />
            <el-option label="环保知识" value="eco-knowledge" />
            <el-option label="节能技巧" value="energy-saving" />
            <el-option label="垃圾分类" value="garbage-classification" />
            <el-option label="社区活动" value="community-activity" />
            <el-option label="其他" value="other" />
          </el-select>
          <el-input
            v-model="newPost.content"
            type="textarea"
            :rows="4"
            placeholder="请输入帖子内容"
            class="mb-3"
          />
          <div class="form-actions">
            <el-button type="primary" @click="createPost">
              <el-icon><Plus /></el-icon>
              发布帖子
            </el-button>
          </div>
        </div>
      </div>

      <!-- 论坛功能区 -->
      <div class="forum-functions">
        <div class="search-bar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索帖子"
            prefix-icon="Search"
            @keyup.enter="searchPosts"
          >
            <template #append>
              <el-button @click="searchPosts">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
        <div class="category-filter">
          <el-select
            v-model="selectedCategory"
            placeholder="按分类筛选"
            @change="filterPosts"
          >
            <el-option label="全部" value="all" />
            <el-option label="绿色生活" value="green-life" />
            <el-option label="环保知识" value="eco-knowledge" />
            <el-option label="节能技巧" value="energy-saving" />
            <el-option label="垃圾分类" value="garbage-classification" />
            <el-option label="社区活动" value="community-activity" />
            <el-option label="其他" value="other" />
          </el-select>
        </div>
      </div>

      <!-- 帖子列表 -->
      <div class="posts-list">
        <div 
          v-for="post in filteredPosts" 
          :key="post.id"
          class="post-card"
          @click="viewPostDetail(post)"
        >
          <div class="post-header">
            <div class="post-author">
              <div class="author-avatar">{{ post.author.charAt(0) }}</div>
              <div class="author-info">
                <div class="author-name">{{ post.author }}</div>
                <div class="post-time">{{ formatDate(post.createdAt) }}</div>
              </div>
            </div>
            <div class="post-category" :class="post.category">
              {{ getCategoryName(post.category) }}
            </div>
          </div>
          <div class="post-content">
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-excerpt">{{ post.content.substring(0, 100) }}...</p>
          </div>
          <div class="post-footer">
            <div class="post-stats">
              <span class="stat-item">
                <el-icon><ChatDotRound /></el-icon>
                {{ post.comments.length }}
              </span>
              <span class="stat-item">
                <el-icon><Star /></el-icon>
                {{ post.likes }}
              </span>
              <span class="stat-item">
                <el-icon><View /></el-icon>
                {{ post.views }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 帖子详情对话框 -->
      <el-dialog
        v-model="showPostDetail"
        :title="selectedPost.title"
        width="800px"
      >
        <div class="post-detail">
          <div class="post-detail-header">
            <div class="post-author">
              <div class="author-avatar">{{ selectedPost.author?.charAt(0) }}</div>
              <div class="author-info">
                <div class="author-name">{{ selectedPost.author }}</div>
                <div class="post-time">{{ formatDate(selectedPost.createdAt) }}</div>
              </div>
            </div>
            <div class="post-category" :class="selectedPost.category">
              {{ getCategoryName(selectedPost.category) }}
            </div>
          </div>
          <div class="post-detail-content">
            {{ selectedPost.content }}
          </div>
          <div class="post-detail-footer">
            <div class="post-stats">
              <span class="stat-item">
                <el-icon><View /></el-icon>
                {{ selectedPost.views }}
              </span>
              <span class="stat-item">
                <el-icon :class="{ active: selectedPost.liked }" @click="toggleLike">
                  <Star />
                </el-icon>
                {{ selectedPost.likes }}
              </span>
            </div>
          </div>
        </div>

        <div class="comments-section">
          <h3>💬 评论</h3>
          <div class="comment-form">
            <el-input
              v-model="newComment"
              type="textarea"
              :rows="3"
              placeholder="写下你的评论..."
              class="mb-3"
            />
            <el-button type="primary" @click="addComment">
              <el-icon><ChatLineRound /></el-icon>
              发表评论
            </el-button>
          </div>
          <div class="comments-list">
            <div 
              v-for="comment in selectedPost.comments" 
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-author">
                <div class="author-avatar">{{ comment.author.charAt(0) }}</div>
                <div class="author-info">
                  <div class="author-name">{{ comment.author }}</div>
                  <div class="comment-time">{{ formatDate(comment.createdAt) }}</div>
                </div>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Search, ChatDotRound, Star, View, ChatLineRound } from '@element-plus/icons-vue'

const newPost = ref({
  title: '',
  content: '',
  category: 'green-life'
})

const searchQuery = ref('')
const selectedCategory = ref('all')
const showPostDetail = ref(false)
const selectedPost = ref({})
const newComment = ref('')

const posts = ref([
  {
    id: 1,
    title: '如何在日常生活中减少碳排放',
    content: '在日常生活中，我们可以通过多种方式减少碳排放。首先，尽量选择公共交通、自行车或步行出行，减少私家车的使用。其次，在饮食方面，减少肉类消费，增加素食比例，选择本地、当季的食材。此外，在能源使用方面，使用LED灯泡，关闭不使用的电器，合理设置空调温度。最后，减少一次性用品的使用，积极参与垃圾分类和回收。这些小习惯的改变，都能为减少碳排放做出贡献。',
    author: '绿色生活爱好者',
    category: 'green-life',
    createdAt: '2026-03-01T10:00:00',
    likes: 25,
    views: 150,
    comments: [
      {
        id: 1,
        author: '环保达人',
        content: '非常实用的建议！我已经开始实践了，效果不错。',
        createdAt: '2026-03-01T11:00:00'
      },
      {
        id: 2,
        author: '新手学习者',
        content: '请问如何计算自己的碳足迹呢？',
        createdAt: '2026-03-01T12:00:00'
      }
    ],
    liked: false
  },
  {
    id: 2,
    title: '垃圾分类小知识',
    content: '垃圾分类是一项非常重要的环保举措。正确的垃圾分类可以减少环境污染，提高资源利用效率。在日常生活中，我们需要将垃圾分为可回收物、有害垃圾、厨余垃圾和其他垃圾四类。可回收物包括废纸、塑料、玻璃、金属等；有害垃圾包括废电池、过期药品、废油漆等；厨余垃圾包括剩菜剩饭、果皮、蛋壳等；其他垃圾包括卫生纸、尿不湿、一次性餐具等。通过正确的垃圾分类，我们可以为环境保护做出自己的贡献。',
    author: '环保志愿者',
    category: 'garbage-classification',
    createdAt: '2026-02-28T14:00:00',
    likes: 18,
    views: 120,
    comments: [
      {
        id: 1,
        author: '社区居民',
        content: '垃圾分类确实很重要，我们社区已经开始实施了。',
        createdAt: '2026-02-28T15:00:00'
      }
    ],
    liked: true
  },
  {
    id: 3,
    title: '节能家电选购指南',
    content: '选择节能家电不仅可以减少能源消耗，还可以节省电费。在选购家电时，我们可以关注能效等级，选择能效等级高的产品。例如，冰箱、空调、洗衣机等家电都有能效等级标识，等级越高，能源消耗越低。此外，我们还可以选择智能家电，通过手机APP控制家电的使用，避免不必要的能源浪费。在使用家电时，也要注意正确的使用方法，比如冰箱不要放得太满，空调温度设置合理等。',
    author: '节能专家',
    category: 'energy-saving',
    createdAt: '2026-02-25T09:00:00',
    likes: 32,
    views: 180,
    comments: [],
    liked: false
  },
  {
    id: 4,
    title: '社区绿化活动招募',
    content: '我们社区计划在本周末开展绿化活动，需要招募志愿者一起参与。活动内容包括植树、种花、清理绿化带等。希望大家积极参与，为我们的社区增添绿色，改善环境。活动时间：本周六上午9点，集合地点：社区中心广场。请有意参加的居民在下方留言报名。',
    author: '社区委员会',
    category: 'community-activity',
    createdAt: '2026-02-20T16:00:00',
    likes: 45,
    views: 200,
    comments: [
      {
        id: 1,
        author: '热心居民',
        content: '我报名参加！',
        createdAt: '2026-02-20T17:00:00'
      },
      {
        id: 2,
        author: '环保爱好者',
        content: '算我一个，我会带工具过去。',
        createdAt: '2026-02-20T18:00:00'
      }
    ],
    liked: false
  }
])

const filteredPosts = computed(() => {
  let result = [...posts.value]
  
  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    result = result.filter(post => post.category === selectedCategory.value)
  }
  
  // 按搜索关键词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(post => 
      post.title.toLowerCase().includes(query) || 
      post.content.toLowerCase().includes(query) ||
      post.author.toLowerCase().includes(query)
    )
  }
  
  // 按创建时间倒序排序
  result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  
  return result
})

const createPost = () => {
  if (!newPost.value.title || !newPost.value.content) {
    return
  }
  
  const newPostObj = {
    id: posts.value.length + 1,
    title: newPost.value.title,
    content: newPost.value.content,
    author: '当前用户',
    category: newPost.value.category,
    createdAt: new Date().toISOString(),
    likes: 0,
    views: 0,
    comments: [],
    liked: false
  }
  
  posts.value.unshift(newPostObj)
  
  // 重置表单
  newPost.value = {
    title: '',
    content: '',
    category: 'green-life'
  }
}

const viewPostDetail = (post) => {
  selectedPost.value = { ...post }
  // 增加浏览量
  selectedPost.value.views++
  // 更新原帖子的浏览量
  const index = posts.value.findIndex(p => p.id === post.id)
  if (index !== -1) {
    posts.value[index].views++
  }
  showPostDetail.value = true
}

const toggleLike = () => {
  selectedPost.value.liked = !selectedPost.value.liked
  if (selectedPost.value.liked) {
    selectedPost.value.likes++
  } else {
    selectedPost.value.likes--
  }
  // 更新原帖子的点赞状态
  const index = posts.value.findIndex(p => p.id === selectedPost.value.id)
  if (index !== -1) {
    posts.value[index].liked = selectedPost.value.liked
    posts.value[index].likes = selectedPost.value.likes
  }
}

const addComment = () => {
  if (!newComment.value) {
    return
  }
  
  const newCommentObj = {
    id: selectedPost.value.comments.length + 1,
    author: '当前用户',
    content: newComment.value,
    createdAt: new Date().toISOString()
  }
  
  selectedPost.value.comments.push(newCommentObj)
  
  // 更新原帖子的评论
  const index = posts.value.findIndex(p => p.id === selectedPost.value.id)
  if (index !== -1) {
    posts.value[index].comments = [...selectedPost.value.comments]
  }
  
  // 重置评论表单
  newComment.value = ''
}

const searchPosts = () => {
  // 搜索逻辑已在computed属性中处理
}

const filterPosts = () => {
  // 筛选逻辑已在computed属性中处理
}

const getCategoryName = (category) => {
  const categoryMap = {
    'green-life': '绿色生活',
    'eco-knowledge': '环保知识',
    'energy-saving': '节能技巧',
    'garbage-classification': '垃圾分类',
    'community-activity': '社区活动',
    'other': '其他'
  }
  return categoryMap[category] || '其他'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.green-forum {
  min-height: 100vh;
  background: #f8fafc;
}

.page-header {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 10px;
  font-weight: 600;
}

.page-header p {
  font-size: 18px;
  opacity: 0.9;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.post-create-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

.post-create-card h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 20px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.forum-functions {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.search-bar {
  flex: 1;
  min-width: 300px;
}

.category-filter {
  min-width: 200px;
}

.posts-list {
  display: grid;
  gap: 20px;
}

.post-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #10b981;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.post-time {
  font-size: 12px;
  color: #999;
}

.post-category {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.post-category.green-life {
  background: #10b981;
}

.post-category.eco-knowledge {
  background: #3b82f6;
}

.post-category.energy-saving {
  background: #f59e0b;
}

.post-category.garbage-classification {
  background: #8b5cf6;
}

.post-category.community-activity {
  background: #ef4444;
}

.post-category.other {
  background: #6b7280;
}

.post-content {
  margin-bottom: 15px;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.post-excerpt {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.post-footer {
  border-top: 1px solid #e5e7eb;
  padding-top: 15px;
}

.post-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stat-item:hover {
  color: #10b981;
}

.stat-item .el-icon.active {
  color: #f59e0b;
}

.post-detail {
  margin-bottom: 30px;
}

.post-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.post-detail-content {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 20px;
}

.post-detail-footer {
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.comments-section {
  margin-top: 30px;
}

.comments-section h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.comment-form {
  margin-bottom: 30px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}

.comment-author {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.comment-content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 20px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .content-section {
    padding: 20px;
  }
  
  .post-create-card {
    padding: 20px;
  }
  
  .forum-functions {
    flex-direction: column;
  }
  
  .search-bar {
    min-width: 100%;
  }
  
  .category-filter {
    min-width: 100%;
  }
  
  .post-card {
    padding: 20px;
  }
  
  .post-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .post-detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>