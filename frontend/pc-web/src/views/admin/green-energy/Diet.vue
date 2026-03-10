<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>饮食养生</h1>
        <p>管理健康食谱、营养建议和饮食数据</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalRecipes || 0 }}</div>
          <div class="stat-label">健康食谱</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalNutritionTips || 0 }}</div>
          <div class="stat-label">营养建议</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalMealPlans || 0 }}</div>
          <div class="stat-label">膳食计划</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
          <div class="stat-label">活跃用户</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="健康食谱" name="recipes">
          <div class="filter-bar">
            <el-select v-model="filterRecipeType" placeholder="食谱类型" clearable style="width: 150px;" @change="loadRecipes">
              <el-option label="早餐" value="breakfast" />
              <el-option label="午餐" value="lunch" />
              <el-option label="晚餐" value="dinner" />
              <el-option label="加餐" value="snack" />
            </el-select>
            <el-select v-model="filterDifficulty" placeholder="难度" clearable style="width: 120px; margin-left: 10px;" @change="loadRecipes">
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="复杂" value="hard" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索食谱" style="width: 200px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadRecipes">查询</el-button>
            <el-button type="success" @click="showAddRecipeDialog = true">
              <el-icon><Plus /></el-icon> 添加食谱
            </el-button>
          </div>

          <el-table :data="recipes" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="食谱名称" min-width="200" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="scope">
                <el-tag size="small">{{ getRecipeTypeName(scope.row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="scope">
                <el-tag :type="getDifficultyType(scope.row.difficulty)" size="small">
                  {{ getDifficultyName(scope.row.difficulty) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="cooking_time" label="烹饪时间" width="120">
              <template #default="scope">
                {{ scope.row.cooking_time }}分钟
              </template>
            </el-table-column>
            <el-table-column prop="calories" label="热量" width="100">
              <template #default="scope">
                {{ scope.row.calories }} kcal
              </template>
            </el-table-column>
            <el-table-column prop="view_count" label="查看次数" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewRecipe(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editRecipe(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteRecipe(scope.row)">删除</el-button>
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

        <el-tab-pane label="营养建议" name="nutrition">
          <div class="nutrition-header">
            <h4>营养建议管理</h4>
            <el-button type="primary" @click="showAddNutritionDialog = true">
              <el-icon><Plus /></el-icon> 添加建议
            </el-button>
          </div>

          <el-table :data="nutritionTips" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="建议标题" min-width="200" />
            <el-table-column prop="category" label="分类" width="120">
              <template #default="scope">
                <el-tag size="small">{{ getCategoryName(scope.row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="target_audience" label="适用人群" min-width="150" />
            <el-table-column prop="view_count" label="查看次数" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewNutritionTip(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editNutritionTip(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteNutritionTip(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="膳食计划" name="meal-plans">
          <div class="meal-plan-header">
            <h4>膳食计划管理</h4>
            <el-button type="primary" @click="showAddMealPlanDialog = true">
              <el-icon><Plus /></el-icon> 添加计划
            </el-button>
          </div>

          <el-table :data="mealPlans" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="计划名称" width="180" />
            <el-table-column prop="type" label="计划类型" width="120">
              <template #default="scope">
                <el-tag :type="getMealPlanType(scope.row.type)" size="small">
                  {{ getMealPlanTypeName(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="duration" label="周期" width="100">
              <template #default="scope">
                {{ scope.row.duration }}天
              </template>
            </el-table-column>
            <el-table-column prop="target_audience" label="适用人群" min-width="150" />
            <el-table-column prop="calories_per_day" label="每日热量" width="120">
              <template #default="scope">
                {{ scope.row.calories_per_day }} kcal
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewMealPlan(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editMealPlan(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteMealPlan(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="饮食统计" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>食谱类型分布</span>
                </template>
                <div class="recipe-distribution">
                  <div v-for="item in recipeDistribution" :key="item.type" class="recipe-item">
                    <div class="recipe-info">
                      <span class="recipe-name">{{ getRecipeTypeName(item.type) }}</span>
                      <span class="recipe-value">{{ item.count }}个</span>
                    </div>
                    <el-progress :percentage="item.percentage" :stroke-width="10" />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>营养摄入趋势</span>
                </template>
                <div class="trend-chart">
                  <div class="chart-bars">
                    <div v-for="(item, index) in nutritionTrend" :key="index" class="bar-item">
                      <div class="bar" :style="{ height: getBarHeight(item.calories) + '%' }">
                        <span class="bar-value">{{ item.calories }} kcal</span>
                      </div>
                      <span class="bar-label">{{ item.week }}</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddRecipeDialog" title="添加健康食谱" width="500px">
      <el-form :model="recipeForm" label-width="100px">
        <el-form-item label="食谱名称">
          <el-input v-model="recipeForm.name" placeholder="请输入食谱名称" />
        </el-form-item>
        <el-form-item label="食谱类型">
          <el-select v-model="recipeForm.type" style="width: 100%;">
            <el-option label="早餐" value="breakfast" />
            <el-option label="午餐" value="lunch" />
            <el-option label="晚餐" value="dinner" />
            <el-option label="加餐" value="snack" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="recipeForm.difficulty" style="width: 100%;">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="复杂" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="烹饪时间">
          <el-input-number v-model="recipeForm.cooking_time" :min="1" />
          <span style="margin-left: 10px;">分钟</span>
        </el-form-item>
        <el-form-item label="热量">
          <el-input-number v-model="recipeForm.calories" :min="0" />
          <span style="margin-left: 10px;">kcal</span>
        </el-form-item>
        <el-form-item label="食材">
          <el-input v-model="recipeForm.ingredients" type="textarea" rows="3" placeholder="请输入食材清单" />
        </el-form-item>
        <el-form-item label="做法">
          <el-input v-model="recipeForm.instructions" type="textarea" rows="4" placeholder="请输入烹饪步骤" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRecipeDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRecipe">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAddNutritionDialog" title="添加营养建议" width="500px">
      <el-form :model="nutritionForm" label-width="100px">
        <el-form-item label="建议标题">
          <el-input v-model="nutritionForm.title" placeholder="请输入建议标题" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="nutritionForm.category" style="width: 100%;">
            <el-option label="蛋白质" value="protein" />
            <el-option label="碳水化合物" value="carbs" />
            <el-option label="脂肪" value="fat" />
            <el-option label="维生素" value="vitamin" />
            <el-option label="矿物质" value="mineral" />
          </el-select>
        </el-form-item>
        <el-form-item label="适用人群">
          <el-input v-model="nutritionForm.target_audience" placeholder="请输入适用人群" />
        </el-form-item>
        <el-form-item label="建议内容">
          <el-input v-model="nutritionForm.content" type="textarea" rows="4" placeholder="请输入建议详细内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddNutritionDialog = false">取消</el-button>
        <el-button type="primary" @click="saveNutritionTip">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAddMealPlanDialog" title="添加膳食计划" width="500px">
      <el-form :model="mealPlanForm" label-width="100px">
        <el-form-item label="计划名称">
          <el-input v-model="mealPlanForm.name" placeholder="请输入计划名称" />
        </el-form-item>
        <el-form-item label="计划类型">
          <el-select v-model="mealPlanForm.type" style="width: 100%;">
            <el-option label="减重" value="weight_loss" />
            <el-option label="增肌" value="muscle_gain" />
            <el-option label="维持" value="maintenance" />
            <el-option label="特殊人群" value="special" />
          </el-select>
        </el-form-item>
        <el-form-item label="周期">
          <el-input-number v-model="mealPlanForm.duration" :min="1" />
          <span style="margin-left: 10px;">天</span>
        </el-form-item>
        <el-form-item label="适用人群">
          <el-input v-model="mealPlanForm.target_audience" placeholder="请输入适用人群" />
        </el-form-item>
        <el-form-item label="每日热量">
          <el-input-number v-model="mealPlanForm.calories_per_day" :min="0" />
          <span style="margin-left: 10px;">kcal</span>
        </el-form-item>
        <el-form-item label="计划描述">
          <el-input v-model="mealPlanForm.description" type="textarea" rows="4" placeholder="请输入计划详细描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddMealPlanDialog = false">取消</el-button>
        <el-button type="primary" @click="saveMealPlan">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('recipes')
const loading = ref(false)
const filterRecipeType = ref('')
const filterDifficulty = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddRecipeDialog = ref(false)
const showAddNutritionDialog = ref(false)
const showAddMealPlanDialog = ref(false)

const stats = ref({
  totalRecipes: 128,
  totalNutritionTips: 89,
  totalMealPlans: 45,
  activeUsers: 1256
})

const recipes = ref([])
const nutritionTips = ref([])
const mealPlans = ref([])
const recipeDistribution = ref([])
const nutritionTrend = ref([])
const recipeForm = ref({ name: '', type: 'breakfast', difficulty: 'easy', cooking_time: 0, calories: 0, ingredients: '', instructions: '' })
const nutritionForm = ref({ title: '', category: 'protein', target_audience: '', content: '' })
const mealPlanForm = ref({ name: '', type: 'weight_loss', duration: 7, target_audience: '', calories_per_day: 0, description: '' })

const loadRecipes = () => {
  recipes.value = [
    { id: 1, name: '全麦三明治', type: 'breakfast', difficulty: 'easy', cooking_time: 10, calories: 350, view_count: 1256, create_time: '2024-01-15 10:00:00', ingredients: '全麦面包、鸡蛋、生菜、番茄', instructions: '1. 煎鸡蛋 2. 组装三明治' },
    { id: 2, name: '清蒸鱼', type: 'dinner', difficulty: 'medium', cooking_time: 20, calories: 450, view_count: 890, create_time: '2024-01-14 15:00:00', ingredients: '鱼、姜、葱、料酒', instructions: '1. 鱼处理干净 2. 清蒸15分钟' },
    { id: 3, name: '蔬菜沙拉', type: 'lunch', difficulty: 'easy', cooking_time: 5, calories: 250, view_count: 654, create_time: '2024-01-13 09:00:00', ingredients: '生菜、黄瓜、番茄、橄榄油', instructions: '1. 切菜 2. 混合调味' }
  ]
  total.value = 3
}

const loadNutritionTips = () => {
  nutritionTips.value = [
    { id: 1, title: '蛋白质摄入建议', category: 'protein', target_audience: '所有人群', view_count: 1256, create_time: '2024-01-15 10:00:00', content: '建议每天摄入体重(kg)×1.2-1.6g的蛋白质' },
    { id: 2, title: '碳水化合物选择', category: 'carbs', target_audience: '健身人群', view_count: 890, create_time: '2024-01-14 15:00:00', content: '优先选择复杂碳水化合物，如全麦、糙米等' },
    { id: 3, title: '维生素C的重要性', category: 'vitamin', target_audience: '所有人群', view_count: 654, create_time: '2024-01-13 09:00:00', content: '维生素C有助于增强免疫力，建议多吃新鲜水果' }
  ]
}

const loadMealPlans = () => {
  mealPlans.value = [
    { id: 1, name: '7天减重计划', type: 'weight_loss', duration: 7, target_audience: '需要减重的人群', calories_per_day: 1500, description: '低热量、高纤维的膳食计划' },
    { id: 2, name: '增肌营养计划', type: 'muscle_gain', duration: 30, target_audience: '健身人群', calories_per_day: 3000, description: '高蛋白质、适量碳水的膳食计划' },
    { id: 3, name: '孕妇营养计划', type: 'special', duration: 280, target_audience: '孕妇', calories_per_day: 2200, description: '均衡营养的孕期膳食计划' }
  ]
}

const loadStatistics = () => {
  recipeDistribution.value = [
    { type: 'breakfast', count: 45, percentage: 35 },
    { type: 'lunch', count: 35, percentage: 27 },
    { type: 'dinner', count: 30, percentage: 23 },
    { type: 'snack', count: 18, percentage: 15 }
  ]
  nutritionTrend.value = [
    { week: '第1周', calories: 2000 },
    { week: '第2周', calories: 1900 },
    { week: '第3周', calories: 1800 },
    { week: '第4周', calories: 1700 },
    { week: '第5周', calories: 1600 },
    { week: '第6周', calories: 1500 }
  ]
}

const viewRecipe = (recipe) => {
  ElMessage.info('查看食谱详情')
}

const saveRecipe = () => {
  ElMessage.success('食谱保存成功')
  showAddRecipeDialog.value = false
  loadRecipes()
}

const editRecipe = (recipe) => {
  recipeForm.value = { ...recipe }
  showAddRecipeDialog.value = true
}

const deleteRecipe = async (recipe) => {
  try {
    await ElMessageBox.confirm('确定要删除该食谱吗？', '提示', { type: 'warning' })
    ElMessage.success('食谱删除成功')
    loadRecipes()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const viewNutritionTip = (tip) => {
  ElMessage.info('查看营养建议详情')
}

const saveNutritionTip = () => {
  ElMessage.success('营养建议保存成功')
  showAddNutritionDialog.value = false
  loadNutritionTips()
}

const editNutritionTip = (tip) => {
  nutritionForm.value = { ...tip }
  showAddNutritionDialog.value = true
}

const deleteNutritionTip = async (tip) => {
  try {
    await ElMessageBox.confirm('确定要删除该营养建议吗？', '提示', { type: 'warning' })
    ElMessage.success('营养建议删除成功')
    loadNutritionTips()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const viewMealPlan = (plan) => {
  ElMessage.info('查看膳食计划详情')
}

const saveMealPlan = () => {
  ElMessage.success('膳食计划保存成功')
  showAddMealPlanDialog.value = false
  loadMealPlans()
}

const editMealPlan = (plan) => {
  mealPlanForm.value = { ...plan }
  showAddMealPlanDialog.value = true
}

const deleteMealPlan = async (plan) => {
  try {
    await ElMessageBox.confirm('确定要删除该膳食计划吗？', '提示', { type: 'warning' })
    ElMessage.success('膳食计划删除成功')
    loadMealPlans()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const getRecipeTypeName = (type) => {
  const map = { 'breakfast': '早餐', 'lunch': '午餐', 'dinner': '晚餐', 'snack': '加餐' }
  return map[type] || type
}

const getDifficultyType = (difficulty) => {
  const map = { 'easy': 'success', 'medium': 'warning', 'hard': 'danger' }
  return map[difficulty] || 'info'
}

const getDifficultyName = (difficulty) => {
  const map = { 'easy': '简单', 'medium': '中等', 'hard': '复杂' }
  return map[difficulty] || difficulty
}

const getCategoryName = (category) => {
  const map = { 'protein': '蛋白质', 'carbs': '碳水化合物', 'fat': '脂肪', 'vitamin': '维生素', 'mineral': '矿物质' }
  return map[category] || category
}

const getMealPlanType = (type) => {
  const map = { 'weight_loss': 'success', 'muscle_gain': 'primary', 'maintenance': 'warning', 'special': 'info' }
  return map[type] || 'info'
}

const getMealPlanTypeName = (type) => {
  const map = { 'weight_loss': '减重', 'muscle_gain': '增肌', 'maintenance': '维持', 'special': '特殊人群' }
  return map[type] || type
}

const getBarHeight = (calories) => {
  const max = Math.max(...nutritionTrend.value.map(t => t.calories), 1)
  return (calories / max) * 100
}

onMounted(() => {
  loadRecipes()
  loadNutritionTips()
  loadMealPlans()
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

.nutrition-header, .meal-plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.nutrition-header h4, .meal-plan-header h4 {
  margin: 0;
  font-size: 16px;
}

.recipe-distribution {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
}

.recipe-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recipe-info {
  display: flex;
  justify-content: space-between;
}

.recipe-name {
  font-size: 14px;
  color: #606266;
}

.recipe-value {
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
  background: linear-gradient(180deg, #E6A23C 0%, #f5d399 100%);
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