<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>绿色积分管理</h1>
        <p>管理绿色积分规则、兑换商品和积分记录</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalPoints || 0 }}</div>
          <div class="stat-label">总积分发放</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.usedPoints || 0 }}</div>
          <div class="stat-label">已兑换积分</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
          <div class="stat-label">参与用户</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.todayEarned || 0 }}</div>
          <div class="stat-label">今日获得</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="积分记录" name="records">
          <div class="filter-bar">
            <el-select v-model="filterType" placeholder="积分类型" clearable style="width: 150px;" @change="loadRecords">
              <el-option label="垃圾分类" value="garbage" />
              <el-option label="绿色出行" value="travel" />
              <el-option label="节能减碳" value="energy" />
              <el-option label="活动参与" value="activity" />
              <el-option label="积分兑换" value="exchange" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索用户" style="width: 180px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadRecords">查询</el-button>
          </div>

          <el-table :data="records" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="用户" width="120">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="24">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  <span style="margin-left: 8px;">{{ scope.row.user_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.points > 0 ? 'success' : 'danger'" size="small">
                  {{ getTypeName(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="points" label="积分变化" width="120">
              <template #default="scope">
                <span :class="scope.row.points > 0 ? 'points-add' : 'points-reduce'">
                  {{ scope.row.points > 0 ? '+' : '' }}{{ scope.row.points }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="balance" label="当前余额" width="100" />
            <el-table-column prop="description" label="描述" min-width="200" />
            <el-table-column prop="create_time" label="时间" width="160" />
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

        <el-tab-pane label="积分规则" name="rules">
          <div class="rule-header">
            <h4>积分获取规则</h4>
            <el-button type="primary" @click="showAddRuleDialog = true">
              <el-icon><Plus /></el-icon> 添加规则
            </el-button>
          </div>

          <el-table :data="rules" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="规则名称" width="150" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag size="small">{{ getTypeName(scope.row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="points" label="积分值" width="100" />
            <el-table-column prop="daily_limit" label="每日上限" width="100" />
            <el-table-column prop="description" label="描述" min-width="200" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleRuleStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editRule(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteRule(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="兑换商品" name="products">
          <div class="product-header">
            <h4>可兑换商品</h4>
            <el-button type="primary" @click="showAddProductDialog = true">
              <el-icon><Plus /></el-icon> 添加商品
            </el-button>
          </div>

          <el-row :gutter="20">
            <el-col :span="6" v-for="product in products" :key="product.id">
              <el-card class="product-card" shadow="hover">
                <div class="product-image">
                  <el-icon :size="48"><Present /></el-icon>
                </div>
                <div class="product-info">
                  <h4>{{ product.name }}</h4>
                  <p class="product-desc">{{ product.description }}</p>
                  <div class="product-points">
                    <el-icon><Coin /></el-icon>
                    <span>{{ product.points }} 积分</span>
                  </div>
                  <div class="product-stock">库存: {{ product.stock }}</div>
                  <div class="product-actions">
                    <el-button size="small" type="primary" @click="editProduct(product)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deleteProduct(product)">删除</el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="兑换记录" name="exchanges">
          <el-table :data="exchanges" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="用户" width="120" />
            <el-table-column prop="product_name" label="兑换商品" width="150" />
            <el-table-column prop="points" label="消耗积分" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getExchangeStatusType(scope.row.status)" size="small">
                  {{ getExchangeStatusName(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="兑换时间" width="160" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="success" link @click="completeExchange(scope.row)" v-if="scope.row.status === 'pending'">完成</el-button>
                <el-button size="small" type="danger" link @click="cancelExchange(scope.row)" v-if="scope.row.status === 'pending'">取消</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="排行榜" name="ranking">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>积分总榜</span>
                </template>
                <el-table :data="totalRanking" style="width: 100%">
                  <el-table-column type="index" label="排名" width="60">
                    <template #default="scope">
                      <span class="rank-badge" :class="'rank-' + (scope.$index + 1)">{{ scope.$index + 1 }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="user_name" label="用户" />
                  <el-table-column prop="total_points" label="总积分" />
                  <el-table-column prop="level" label="等级" />
                </el-table>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>本周活跃榜</span>
                </template>
                <el-table :data="weeklyRanking" style="width: 100%">
                  <el-table-column type="index" label="排名" width="60">
                    <template #default="scope">
                      <span class="rank-badge" :class="'rank-' + (scope.$index + 1)">{{ scope.$index + 1 }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="user_name" label="用户" />
                  <el-table-column prop="weekly_points" label="本周积分" />
                  <el-table-column prop="activities" label="参与活动" />
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddRuleDialog" title="添加积分规则" width="500px">
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="规则名称">
          <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="ruleForm.type" placeholder="请选择类型" style="width: 100%;">
            <el-option label="垃圾分类" value="garbage" />
            <el-option label="绿色出行" value="travel" />
            <el-option label="节能减碳" value="energy" />
            <el-option label="活动参与" value="activity" />
          </el-select>
        </el-form-item>
        <el-form-item label="积分值">
          <el-input-number v-model="ruleForm.points" :min="1" />
        </el-form-item>
        <el-form-item label="每日上限">
          <el-input-number v-model="ruleForm.daily_limit" :min="0" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="ruleForm.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRuleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRule">保存</el-button>
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

const activeTab = ref('records')
const loading = ref(false)
const filterType = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddRuleDialog = ref(false)
const showAddProductDialog = ref(false)

const stats = ref({
  totalPoints: 256800,
  usedPoints: 89500,
  activeUsers: 3256,
  todayEarned: 1250
})

const records = ref([])
const rules = ref([])
const products = ref([])
const exchanges = ref([])
const totalRanking = ref([])
const weeklyRanking = ref([])
const ruleForm = ref({ name: '', type: '', points: 10, daily_limit: 100, description: '' })

const loadRecords = () => {
  records.value = [
    { id: 1, user_name: '张三', type: 'garbage', points: 10, balance: 1250, description: '垃圾分类识别奖励', create_time: '2024-01-15 10:30:00' },
    { id: 2, user_name: '李四', type: 'travel', points: 20, balance: 890, description: '绿色出行奖励', create_time: '2024-01-15 09:20:00' },
    { id: 3, user_name: '王五', type: 'exchange', points: -100, balance: 560, description: '兑换环保袋', create_time: '2024-01-14 18:45:00' }
  ]
  total.value = 3
}

const loadRules = () => {
  rules.value = [
    { id: 1, name: '垃圾分类识别', type: 'garbage', points: 10, daily_limit: 100, description: '每次正确识别垃圾分类', status: true },
    { id: 2, name: '绿色出行', type: 'travel', points: 20, daily_limit: 60, description: '使用公共交通出行', status: true },
    { id: 3, name: '节能打卡', type: 'energy', points: 15, daily_limit: 45, description: '每日节能打卡', status: true }
  ]
}

const loadProducts = () => {
  products.value = [
    { id: 1, name: '环保购物袋', description: '可重复使用的环保购物袋', points: 100, stock: 50 },
    { id: 2, name: '绿植盆栽', description: '小型绿植盆栽', points: 200, stock: 30 },
    { id: 3, name: '节能灯泡', description: 'LED节能灯泡', points: 150, stock: 100 },
    { id: 4, name: '环保水杯', description: '不锈钢保温水杯', points: 300, stock: 25 }
  ]
}

const loadExchanges = () => {
  exchanges.value = [
    { id: 1, user_name: '张三', product_name: '环保购物袋', points: 100, status: 'completed', create_time: '2024-01-15 10:00:00' },
    { id: 2, user_name: '李四', product_name: '绿植盆栽', points: 200, status: 'pending', create_time: '2024-01-15 09:30:00' }
  ]
}

const loadRanking = () => {
  totalRanking.value = [
    { user_name: '张三', total_points: 12560, level: '环保达人' },
    { user_name: '李四', total_points: 9870, level: '绿色先锋' },
    { user_name: '王五', total_points: 8560, level: '绿色先锋' },
    { user_name: '赵六', total_points: 7230, level: '环保新手' },
    { user_name: '钱七', total_points: 6580, level: '环保新手' }
  ]
  weeklyRanking.value = [
    { user_name: '张三', weekly_points: 560, activities: 28 },
    { user_name: '李四', weekly_points: 450, activities: 22 },
    { user_name: '王五', weekly_points: 380, activities: 19 }
  ]
}

const saveRule = () => {
  ElMessage.success('规则保存成功')
  showAddRuleDialog.value = false
  loadRules()
}

const editRule = (rule) => {
  ruleForm.value = { ...rule }
  showAddRuleDialog.value = true
}

const deleteRule = async (rule) => {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？', '提示', { type: 'warning' })
    ElMessage.success('规则删除成功')
    loadRules()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const toggleRuleStatus = (rule) => {
  ElMessage.success(`规则已${rule.status ? '启用' : '禁用'}`)
}

const editProduct = (product) => {
  ElMessage.info(`编辑商品: ${product.name}`)
}

const deleteProduct = async (product) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', { type: 'warning' })
    ElMessage.success('商品删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const completeExchange = (exchange) => {
  ElMessage.success('兑换已完成')
  exchange.status = 'completed'
}

const cancelExchange = (exchange) => {
  ElMessage.warning('兑换已取消')
  exchange.status = 'cancelled'
}

const getTypeName = (type) => {
  const map = { 'garbage': '垃圾分类', 'travel': '绿色出行', 'energy': '节能减碳', 'activity': '活动参与', 'exchange': '积分兑换' }
  return map[type] || type
}

const getExchangeStatusType = (status) => {
  const map = { 'pending': 'warning', 'completed': 'success', 'cancelled': 'danger' }
  return map[status] || 'info'
}

const getExchangeStatusName = (status) => {
  const map = { 'pending': '待处理', 'completed': '已完成', 'cancelled': '已取消' }
  return map[status] || status
}

onMounted(() => {
  loadRecords()
  loadRules()
  loadProducts()
  loadExchanges()
  loadRanking()
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

.user-info {
  display: flex;
  align-items: center;
}

.points-add {
  color: #67C23A;
  font-weight: bold;
}

.points-reduce {
  color: #F56C6C;
  font-weight: bold;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.rule-header, .product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.rule-header h4, .product-header h4 {
  margin: 0;
  font-size: 16px;
}

.product-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.product-image {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #67C23A 0%, #95d475 100%);
  color: white;
  border-radius: 8px 8px 0 0;
}

.product-info {
  padding: 15px;
}

.product-info h4 {
  margin: 0 0 10px 0;
}

.product-desc {
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
}

.product-points {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #E6A23C;
  font-weight: bold;
  margin-bottom: 10px;
}

.product-stock {
  font-size: 13px;
  color: #606266;
  margin-bottom: 10px;
}

.product-actions {
  display: flex;
  gap: 10px;
}

.rank-badge {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 50%;
  background: #909399;
  color: white;
  font-size: 12px;
}

.rank-badge.rank-1 { background: #FFD700; }
.rank-badge.rank-2 { background: #C0C0C0; }
.rank-badge.rank-3 { background: #CD7F32; }
</style>
