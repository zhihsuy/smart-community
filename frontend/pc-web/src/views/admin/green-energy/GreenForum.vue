<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>绿色论坛管理</h1>
        <p>管理绿色社区论坛的帖子、评论和版块</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalPosts || 0 }}</div>
          <div class="stat-label">帖子总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalComments || 0 }}</div>
          <div class="stat-label">评论总数</div>
        </el-card>
      </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
          <div class="stat-label">活跃用户</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.todayPosts || 0 }}</div>
          <div class="stat-label">今日发帖</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="帖子管理" name="posts">
          <div class="filter-bar">
            <el-select v-model="filterCategory" placeholder="帖子分类" clearable style="width: 150px;" @change="loadPosts">
              <el-option label="环保知识" value="knowledge" />
              <el-option label="低碳生活" value="low-carbon" />
              <el-option label="绿色出行" value="travel" />
              <el-option label="节能技巧" value="energy" />
              <el-option label="其他" value="other" />
            </el-select>
            <el-select v-model="filterStatus" placeholder="状态" clearable style="width: 120px; margin-left: 10px;" @change="loadPosts">
              <el-option label="已发布" value="published" />
              <el-option label="待审核" value="pending" />
              <el-option label="已下架" value="removed" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索帖子标题或内容" style="width: 200px; margin-left: 10px;" clearable @keyup.enter="loadPosts">
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" style="margin-left: 10px;" @click="loadPosts">查询</el-button>
          </div>

          <el-table :data="posts" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="标题" min-width="200">
              <template #default="scope">
                <el-link type="primary" @click="viewPost(scope.row)">{{ scope.row.title }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="author_name" label="作者" width="100" />
            <el-table-column prop="category" label="分类" width="100">
              <template #default="scope">
                <el-tag size="small">{{ getCategoryName(scope.row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="likes" label="点赞" width="80" />
            <el-table-column prop="comments" label="评论" width="80" />
            <el-table-column prop="views" label="浏览" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)" size="small">
                  {{ getStatusName(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="发布时间" width="160" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewPost(scope.row)">查看</el-button>
                <el-button size="small" type="success" link @click="approvePost(scope.row)" v-if="scope.row.status === 'pending'">通过</el-button>
                <el-button size="small" type="warning" link @click="removePost(scope.row)" v-if="scope.row.status === 'published'">下架</el-button>
                <el-button size="small" type="danger" link @click="deletePost(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next"
              @size-change="loadPosts"
              @current-change="loadPosts"
            />
          </div>
        </el-tab-pane>

        <el-tab-pane label="评论管理" name="comments">
          <div class="filter-bar">
            <el-input v-model="commentSearchKeyword" placeholder="搜索评论内容" style="width: 200px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadComments">查询</el-button>
          </div>

          <el-table :data="comments" style="width: 100%" v-loading="loadingComments">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="评论者" width="100" />
            <el-table-column prop="post_title" label="所属帖子" min-width="150">
              <template #default="scope">
                <el-link type="primary">{{ scope.row.post_title }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="评论内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="likes" label="点赞" width="80" />
            <el-table-column prop="create_time" label="评论时间" width="160" />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button size="small" type="danger" link @click="deleteComment(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="版块管理" name="categories">
          <div class="category-header">
            <h4>论坛版块</h4>
            <el-button type="primary" @click="showAddCategoryDialog = true">
              <el-icon><Plus /></el-icon> 添加版块
            </el-button>
          </div>

          <el-table :data="categories" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="版块名称" width="150" />
            <el-table-column prop="description" label="描述" min-width="200" />
            <el-table-column prop="post_count" label="帖子数" width="100" />
            <el-table-column prop="sort_order" label="排序" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleCategoryStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editCategory(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteCategory(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="举报处理" name="reports">
          <el-table :data="reports" style="width: 100%" v-loading="loadingReports">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="reporter_name" label="举报人" width="100" />
            <el-table-column prop="type" label="举报类型" width="100">
              <template #default="scope">
                <el-tag size="small">{{ scope.row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="target_title" label="被举报内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="reason" label="举报原因" min-width="150" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'pending' ? 'warning' : 'success'" size="small">
                  {{ scope.row.status === 'pending' ? '待处理' : '已处理' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="举报时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="handleReport(scope.row)" v-if="scope.row.status === 'pending'">处理</el-button>
                <el-button size="small" type="info" link @click="viewReport(scope.row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showPostDialog" title="帖子详情" width="700px">
      <div v-if="currentPost" class="post-detail">
        <h3>{{ currentPost.title }}</h3>
        <div class="post-meta">
          <span>作者: {{ currentPost.author_name }}</span>
          <span>发布时间: {{ currentPost.create_time }}</span>
          <span>浏览: {{ currentPost.views }}</span>
        </div>
        <div class="post-content">
          {{ currentPost.content }}
        </div>
        <div class="post-images" v-if="currentPost.images?.length">
          <el-image v-for="(img, index) in currentPost.images" :key="index" :src="img" style="width: 100px; height: 100px; margin-right: 10px;" fit="cover" />
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showAddCategoryDialog" title="添加版块" width="400px">
      <el-form :model="categoryForm" label-width="80px">
        <el-form-item label="版块名称">
          <el-input v-model="categoryForm.name" placeholder="请输入版块名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="categoryForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="categoryForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddCategoryDialog = false">取消</el-button>
        <el-button type="primary" @click="saveCategory">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('posts')
const loading = ref(false)
const loadingComments = ref(false)
const loadingReports = ref(false)
const filterCategory = ref('')
const filterStatus = ref('')
const searchKeyword = ref('')
const commentSearchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showPostDialog = ref(false)
const showAddCategoryDialog = ref(false)
const currentPost = ref(null)

const stats = ref({
  totalPosts: 1256,
  totalComments: 5680,
  activeUsers: 890,
  todayPosts: 23
})

const posts = ref([])
const comments = ref([])
const categories = ref([])
const reports = ref([])
const categoryForm = ref({ name: '', description: '', sort_order: 0 })

const loadPosts = () => {
  loading.value = true
  setTimeout(() => {
    posts.value = [
      { id: 1, title: '分享我的低碳生活经验', author_name: '张三', category: 'low-carbon', likes: 128, comments: 45, views: 890, status: 'published', create_time: '2024-01-15 10:30:00' },
      { id: 2, title: '如何正确进行垃圾分类', author_name: '李四', category: 'knowledge', likes: 256, comments: 78, views: 1560, status: 'published', create_time: '2024-01-14 15:20:00' },
      { id: 3, title: '绿色出行的好处', author_name: '王五', category: 'travel', likes: 89, comments: 23, views: 450, status: 'pending', create_time: '2024-01-14 09:10:00' }
    ]
    total.value = 3
    loading.value = false
  }, 500)
}

const loadComments = () => {
  comments.value = [
    { id: 1, user_name: '赵六', post_title: '分享我的低碳生活经验', content: '写得很好，学习了！', likes: 15, create_time: '2024-01-15 11:00:00' },
    { id: 2, user_name: '钱七', post_title: '如何正确进行垃圾分类', content: '这个分类方法很实用', likes: 23, create_time: '2024-01-14 16:00:00' }
  ]
}

const loadCategories = () => {
  categories.value = [
    { id: 1, name: '环保知识', description: '分享环保知识和技巧', post_count: 256, sort_order: 1, status: true },
    { id: 2, name: '低碳生活', description: '低碳生活方式分享', post_count: 189, sort_order: 2, status: true },
    { id: 3, name: '绿色出行', description: '绿色出行经验交流', post_count: 145, sort_order: 3, status: true }
  ]
}

const loadReports = () => {
  reports.value = [
    { id: 1, reporter_name: '张三', type: '垃圾广告', target_title: '分享我的低碳生活经验', reason: '内容涉嫌广告推广', status: 'pending', create_time: '2024-01-15 12:00:00' },
    { id: 2, reporter_name: '李四', type: '不当内容', target_title: '绿色出行的好处', reason: '内容包含敏感信息', status: 'processed', create_time: '2024-01-14 18:00:00' }
  ]
}

const viewPost = (post) => {
  currentPost.value = { ...post, content: '这是帖子的详细内容...', images: [] }
  showPostDialog.value = true
}

const approvePost = (post) => {
  ElMessage.success('帖子已通过审核')
  post.status = 'published'
}

const removePost = (post) => {
  ElMessage.warning('帖子已下架')
  post.status = 'removed'
}

const deletePost = async (post) => {
  try {
    await ElMessageBox.confirm('确定要删除该帖子吗？', '提示', { type: 'warning' })
    ElMessage.success('帖子已删除')
    loadPosts()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const deleteComment = async (comment) => {
  try {
    await ElMessageBox.confirm('确定要删除该评论吗？', '提示', { type: 'warning' })
    ElMessage.success('评论已删除')
    loadComments()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const saveCategory = () => {
  ElMessage.success('版块保存成功')
  showAddCategoryDialog.value = false
  loadCategories()
}

const editCategory = (category) => {
  categoryForm.value = { ...category }
  showAddCategoryDialog.value = true
}

const deleteCategory = async (category) => {
  try {
    await ElMessageBox.confirm('确定要删除该版块吗？', '提示', { type: 'warning' })
    ElMessage.success('版块已删除')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const toggleCategoryStatus = (category) => {
  ElMessage.success(`版块已${category.status ? '启用' : '禁用'}`)
}

const handleReport = (report) => {
  ElMessage.success('举报已处理')
  report.status = 'processed'
}

const viewReport = (report) => {
  ElMessage.info('查看举报详情')
}

const getCategoryName = (category) => {
  const map = { 'knowledge': '环保知识', 'low-carbon': '低碳生活', 'travel': '绿色出行', 'energy': '节能技巧', 'other': '其他' }
  return map[category] || category
}

const getStatusType = (status) => {
  const map = { 'published': 'success', 'pending': 'warning', 'removed': 'danger' }
  return map[status] || 'info'
}

const getStatusName = (status) => {
  const map = { 'published': '已发布', 'pending': '待审核', 'removed': '已下架' }
  return map[status] || status
}

onMounted(() => {
  loadPosts()
  loadComments()
  loadCategories()
  loadReports()
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

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  border-radius: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.main-card {
  border-radius: 12px;
}

.filter-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.category-header h4 {
  margin: 0;
  font-size: 16px;
}

.post-detail h3 {
  margin: 0 0 15px 0;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 13px;
  margin-bottom: 15px;
}

.post-content {
  line-height: 1.8;
  color: #606266;
}

.post-images {
  margin-top: 15px;
}
</style>
