<template>
  <AdminLayout>
    <div class="review-manage">
      <div class="page-header">
        <h2 class="page-title">⭐ 评价管理</h2>
        <div class="header-actions">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索评价内容/用户"
            style="width: 300px; margin-right: 10px"
            @keyup.enter="loadReviews"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select
            v-model="status"
            placeholder="选择状态"
            style="width: 120px; margin-right: 10px"
            @change="loadReviews"
          >
            <el-option label="全部" value="" />
            <el-option label="正常" value="normal" />
            <el-option label="违规" value="blocked" />
          </el-select>
          <el-button type="primary" @click="loadReviews">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button type="warning" @click="runAICheck">
            <el-icon><Refresh /></el-icon>
            AI违规检测
          </el-button>
        </div>
      </div>

      <div class="review-table">
        <el-table :data="reviews" style="width: 100%">
          <el-table-column prop="id" label="评价ID" width="80" />
          <el-table-column prop="user_nickname" label="用户" width="120" />
          <el-table-column prop="goods_name" label="商品" width="180" />
          <el-table-column prop="rating" label="评分" width="80">
            <template #default="scope">
              <div class="rating">
                <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= scope.row.rating }">
                  ★
                </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="评价内容" min-width="200" />
          <el-table-column label="图片" width="120">
            <template #default="scope">
              <el-image
                v-if="scope.row.images && scope.row.images.length > 0"
                :src="scope.row.images[0]"
                fit="cover"
                style="width: 80px; height: 80px"
                :preview-src-list="scope.row.images"
              />
              <span v-else>无</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'normal' ? 'success' : 'danger'">
                {{ scope.row.status === 'normal' ? '正常' : '违规' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="评价时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="replyReview(scope.row)"
                style="margin-right: 5px"
              >
                回复
              </el-button>
              <el-button
                size="small"
                :type="scope.row.status === 'normal' ? 'danger' : 'success'"
                @click="toggleStatus(scope.row)"
              >
                {{ scope.row.status === 'normal' ? '屏蔽' : '解除屏蔽' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination" style="margin-top: 20px">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 回复对话框 -->
      <el-dialog
        v-model="replyVisible"
        title="回复评价"
        width="500px"
      >
        <el-form :model="replyForm" label-width="100px">
          <el-form-item label="评价内容">
            <el-input
              v-model="replyForm.content"
              type="textarea"
              rows="4"
              placeholder="请输入回复内容"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="replyVisible = false">取消</el-button>
            <el-button type="primary" @click="saveReply">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const reviews = ref([])
const searchKeyword = ref('')
const status = ref('')
const replyVisible = ref(false)
const replyForm = ref({})
const currentReview = ref(null)

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const loadReviews = async () => {
  try {
    const response = await fetch(`/api/v1/admin/reviews?page=${pagination.value.currentPage}&pageSize=${pagination.value.pageSize}&keyword=${searchKeyword.value}&status=${status.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      reviews.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载评价列表失败:', error)
    ElMessage.error('加载评价列表失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadReviews()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadReviews()
}

const replyReview = (review) => {
  currentReview.value = review
  replyForm.value = {
    content: review.reply || ''
  }
  replyVisible.value = true
}

const saveReply = async () => {
  if (!currentReview.value) return
  
  try {
    const response = await fetch(`/api/v1/admin/reviews/${currentReview.value.id}/reply`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ reply: replyForm.value.content })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('回复成功')
      replyVisible.value = false
      loadReviews()
    } else {
      ElMessage.error(result.msg || '回复失败')
    }
  } catch (error) {
    console.error('回复评价失败:', error)
    ElMessage.error('回复失败')
  }
}

const toggleStatus = async (review) => {
  try {
    const response = await fetch(`/api/v1/admin/reviews/${review.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ status: review.status === 'normal' ? 'blocked' : 'normal' })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('操作成功')
      loadReviews()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('切换状态失败:', error)
    ElMessage.error('操作失败')
  }
}

const runAICheck = async () => {
  try {
    const response = await fetch('/api/v1/admin/reviews/ai-check', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success(`AI检测完成，发现${result.data?.blockedCount || 0}条违规评价`)
      loadReviews()
    } else {
      ElMessage.error(result.msg || '检测失败')
    }
  } catch (error) {
    console.error('AI检测失败:', error)
    ElMessage.error('检测失败')
  }
}

onMounted(() => {
  loadReviews()
})
</script>

<style scoped>
.review-manage {
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
  flex-wrap: wrap;
  gap: 15px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.review-table {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.rating {
  display: flex;
  align-items: center;
}

.star {
  color: #e4e7ed;
  font-size: 16px;
  margin-right: 2px;
}

.star.active {
  color: #f7ba2a;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .el-input {
    flex: 1;
  }
  
  .review-table {
    padding: 10px;
  }
  
  .pagination {
    justify-content: center;
  }
}
</style>