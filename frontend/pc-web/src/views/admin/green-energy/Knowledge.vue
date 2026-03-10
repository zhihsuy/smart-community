<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>养生知识库</h1>
        <p>管理养生知识文章、分类和标签</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalArticles || 0 }}</div>
          <div class="stat-label">知识文章</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalCategories || 0 }}</div>
          <div class="stat-label">文章分类</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalTags || 0 }}</div>
          <div class="stat-label">标签数量</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalViews || 0 }}</div>
          <div class="stat-label">总浏览量</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="知识文章" name="articles">
          <div class="filter-bar">
            <el-select v-model="filterCategory" placeholder="文章分类" clearable style="width: 150px;" @change="loadArticles">
              <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索文章" style="width: 200px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadArticles">查询</el-button>
            <el-button type="success" @click="showAddArticleDialog = true">
              <el-icon><Plus /></el-icon> 添加文章
            </el-button>
          </div>

          <el-table :data="articles" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="文章标题" min-width="250" />
            <el-table-column prop="category_name" label="分类" width="120">
              <template #default="scope">
                <el-tag size="small">{{ scope.row.category_name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="tags" label="标签" min-width="150">
              <template #default="scope">
                <el-tag v-for="tag in scope.row.tags" :key="tag" size="small" style="margin-right: 5px;">
                  {{ tag }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="author" label="作者" width="100" />
            <el-table-column prop="view_count" label="浏览量" width="100" />
            <el-table-column prop="create_time" label="发布时间" width="160" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleArticleStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewArticle(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editArticle(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteArticle(scope.row)">删除</el-button>
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
            />
          </div>
        </el-tab-pane>

        <el-tab-pane label="分类管理" name="categories">
          <div class="category-header">
            <h4>文章分类管理</h4>
            <el-button type="primary" @click="showAddCategoryDialog = true">
              <el-icon><Plus /></el-icon> 添加分类
            </el-button>
          </div>

          <el-table :data="categories" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="分类名称" width="180" />
            <el-table-column prop="description" label="分类描述" min-width="200" />
            <el-table-column prop="article_count" label="文章数量" width="100" />
            <el-table-column prop="sort_order" label="排序" width="80" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editCategory(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteCategory(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="标签管理" name="tags">
          <div class="tag-header">
            <h4>标签管理</h4>
            <el-button type="primary" @click="showAddTagDialog = true">
              <el-icon><Plus /></el-icon> 添加标签
            </el-button>
          </div>

          <el-table :data="tags" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="标签名称" width="150" />
            <el-table-column prop="article_count" label="使用次数" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editTag(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteTag(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="统计分析" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>分类文章分布</span>
                </template>
                <div class="category-distribution">
                  <div v-for="item in categoryDistribution" :key="item.category_id" class="category-item">
                    <div class="category-info">
                      <span class="category-name">{{ item.category_name }}</span>
                      <span class="category-value">{{ item.count }}篇</span>
                    </div>
                    <el-progress :percentage="item.percentage" :stroke-width="10" />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>文章浏览趋势</span>
                </template>
                <div class="trend-chart">
                  <div class="chart-bars">
                    <div v-for="(item, index) in viewTrend" :key="index" class="bar-item">
                      <div class="bar" :style="{ height: getBarHeight(item.views) + '%' }">
                        <span class="bar-value">{{ item.views }}</span>
                      </div>
                      <span class="bar-label">{{ item.month }}</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddArticleDialog" title="添加知识文章" width="600px">
      <el-form :model="articleForm" label-width="100px">
        <el-form-item label="文章标题">
          <el-input v-model="articleForm.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="文章分类">
          <el-select v-model="articleForm.category_id" style="width: 100%;">
            <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="articleForm.tags" multiple style="width: 100%;" placeholder="请选择标签">
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="articleForm.author" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="文章内容">
          <el-input v-model="articleForm.content" type="textarea" rows="10" placeholder="请输入文章详细内容" />
        </el-form-item>
        <el-form-item label="封面图片">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="handleImageChange"
            :file-list="articleForm.cover_image"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon> 选择图片
            </el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddArticleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveArticle">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAddCategoryDialog" title="添加分类" width="400px">
      <el-form :model="categoryForm" label-width="100px">
        <el-form-item label="分类名称">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="分类描述">
          <el-input v-model="categoryForm.description" type="textarea" rows="3" placeholder="请输入分类描述" />
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

    <el-dialog v-model="showAddTagDialog" title="添加标签" width="400px">
      <el-form :model="tagForm" label-width="100px">
        <el-form-item label="标签名称">
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddTagDialog = false">取消</el-button>
        <el-button type="primary" @click="saveTag">保存</el-button>
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

const activeTab = ref('articles')
const loading = ref(false)
const filterCategory = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddArticleDialog = ref(false)
const showAddCategoryDialog = ref(false)
const showAddTagDialog = ref(false)

const stats = ref({
  totalArticles: 256,
  totalCategories: 12,
  totalTags: 89,
  totalViews: 12560
})

const articles = ref([])
const categories = ref([])
const tags = ref([])
const categoryDistribution = ref([])
const viewTrend = ref([])
const articleForm = ref({ title: '', category_id: '', tags: [], author: '', content: '', cover_image: [] })
const categoryForm = ref({ name: '', description: '', sort_order: 0 })
const tagForm = ref({ name: '' })

const loadArticles = () => {
  articles.value = [
    { id: 1, title: '春季养生小知识', category_id: 1, category_name: '四季养生', tags: ['春季', '养生', '健康'], author: '管理员', view_count: 1256, status: true, create_time: '2024-01-15 10:00:00', content: '春季是养生的好时节...' },
    { id: 2, title: '夏季防暑降温技巧', category_id: 1, category_name: '四季养生', tags: ['夏季', '防暑', '降温'], author: '管理员', view_count: 890, status: true, create_time: '2024-01-14 15:00:00', content: '夏季高温天气...' },
    { id: 3, title: '秋季润燥食谱', category_id: 1, category_name: '四季养生', tags: ['秋季', '润燥', '食谱'], author: '管理员', view_count: 654, status: false, create_time: '2024-01-13 09:00:00', content: '秋季气候干燥...' }
  ]
  total.value = 3
}

const loadCategories = () => {
  categories.value = [
    { id: 1, name: '四季养生', description: '四季养生相关知识', article_count: 45, sort_order: 1 },
    { id: 2, name: '饮食养生', description: '饮食养生相关知识', article_count: 38, sort_order: 2 },
    { id: 3, name: '运动养生', description: '运动养生相关知识', article_count: 25, sort_order: 3 },
    { id: 4, name: '情志养生', description: '情志养生相关知识', article_count: 18, sort_order: 4 }
  ]
}

const loadTags = () => {
  tags.value = [
    { id: 1, name: '春季', article_count: 25, create_time: '2024-01-01 00:00:00' },
    { id: 2, name: '夏季', article_count: 20, create_time: '2024-01-01 00:00:00' },
    { id: 3, name: '秋季', article_count: 18, create_time: '2024-01-01 00:00:00' },
    { id: 4, name: '冬季', article_count: 22, create_time: '2024-01-01 00:00:00' },
    { id: 5, name: '养生', article_count: 89, create_time: '2024-01-01 00:00:00' },
    { id: 6, name: '健康', article_count: 76, create_time: '2024-01-01 00:00:00' }
  ]
}

const loadStatistics = () => {
  categoryDistribution.value = [
    { category_id: 1, category_name: '四季养生', count: 45, percentage: 45 },
    { category_id: 2, category_name: '饮食养生', count: 38, percentage: 38 },
    { category_id: 3, category_name: '运动养生', count: 25, percentage: 25 },
    { category_id: 4, category_name: '情志养生', count: 18, percentage: 18 }
  ]
  viewTrend.value = [
    { month: '1月', views: 1200 },
    { month: '2月', views: 1100 },
    { month: '3月', views: 1300 },
    { month: '4月', views: 1500 },
    { month: '5月', views: 1400 },
    { month: '6月', views: 1600 }
  ]
}

const handleImageChange = (file) => {
  articleForm.value.cover_image = [file]
}

const viewArticle = (article) => {
  ElMessage.info('查看文章详情')
}

const saveArticle = () => {
  ElMessage.success('文章保存成功')
  showAddArticleDialog.value = false
  loadArticles()
}

const editArticle = (article) => {
  articleForm.value = { ...article }
  showAddArticleDialog.value = true
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', { type: 'warning' })
    ElMessage.success('文章删除成功')
    loadArticles()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const toggleArticleStatus = (article) => {
  ElMessage.success(`文章已${article.status ? '发布' : '下架'}`)
}

const saveCategory = () => {
  ElMessage.success('分类保存成功')
  showAddCategoryDialog.value = false
  loadCategories()
}

const editCategory = (category) => {
  categoryForm.value = { ...category }
  showAddCategoryDialog.value = true
}

const deleteCategory = async (category) => {
  try {
    await ElMessageBox.confirm('确定要删除该分类吗？', '提示', { type: 'warning' })
    ElMessage.success('分类删除成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const saveTag = () => {
  ElMessage.success('标签保存成功')
  showAddTagDialog.value = false
  loadTags()
}

const editTag = (tag) => {
  tagForm.value = { ...tag }
  showAddTagDialog.value = true
}

const deleteTag = async (tag) => {
  try {
    await ElMessageBox.confirm('确定要删除该标签吗？', '提示', { type: 'warning' })
    ElMessage.success('标签删除成功')
    loadTags()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const getBarHeight = (views) => {
  const max = Math.max(...viewTrend.value.map(t => t.views), 1)
  return (views / max) * 100
}

onMounted(() => {
  loadArticles()
  loadCategories()
  loadTags()
  loadStatistics()
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
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.category-header, .tag-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.category-header h4, .tag-header h4 {
  margin: 0;
  font-size: 16px;
}

.category-distribution {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
}

.category-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-info {
  display: flex;
  justify-content: space-between;
}

.category-name {
  font-size: 14px;
  color: #606266;
}

.category-value {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
}

.trend-chart {
  height: 200px;
  padding: 20px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 150px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bar {
  width: 30px;
  background: linear-gradient(180deg, #909399 0%, #c0c4cc 100%);
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 5px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #606266;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}
</style>