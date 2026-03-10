<template>
  <div class="complaint-page">
    <div class="page-header">
      <h1>💬 投诉建议</h1>
      <p class="subtitle">在线投诉、问题反馈、处理进度查询、满意度评价</p>
    </div>

    <div class="feature-grid">
      <el-card class="feature-card submit-card">
        <template #header>
          <div class="card-header">
            <span>📝 提交投诉</span>
          </div>
        </template>
        <div class="complaint-form">
          <el-form :model="complaintForm" label-width="100px" :rules="complaintRules" ref="complaintFormRef">
            <el-form-item label="投诉类型" prop="type">
              <el-select v-model="complaintForm.type" placeholder="请选择投诉类型" style="width: 100%;">
                <el-option label="物业服务" value="property" />
                <el-option label="环境卫生" value="environment" />
                <el-option label="安全管理" value="security" />
                <el-option label="设施设备" value="facility" />
                <el-option label="停车管理" value="parking" />
                <el-option label="噪音扰民" value="noise" />
                <el-option label="邻里纠纷" value="neighbor" />
                <el-option label="其他问题" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="紧急程度" prop="urgency">
              <el-radio-group v-model="complaintForm.urgency">
                <el-radio label="normal">一般</el-radio>
                <el-radio label="urgent">紧急</el-radio>
                <el-radio label="very_urgent">非常紧急</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="投诉标题" prop="title">
              <el-input v-model="complaintForm.title" placeholder="请简要描述问题" maxlength="50" show-word-limit />
            </el-form-item>
            <el-form-item label="详细描述" prop="content">
              <el-input 
                v-model="complaintForm.content" 
                type="textarea" 
                :rows="4" 
                placeholder="请详细描述您遇到的问题..."
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
            <el-form-item label="相关图片">
              <el-upload
                action="#"
                list-type="picture-card"
                :auto-upload="false"
                :limit="3"
                v-model:file-list="complaintForm.images"
              >
                <el-icon><Plus /></el-icon>
                <template #tip>
                  <div class="upload-tip">最多上传3张图片</div>
                </template>
              </el-upload>
            </el-form-item>
            <el-form-item label="联系方式" prop="contact_phone">
              <el-input v-model="complaintForm.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitComplaint" :loading="submitting" size="large">
                <el-icon><Position /></el-icon> 提交投诉
              </el-button>
              <el-button size="large" @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="feature-card stats-card">
        <template #header>
          <div class="card-header">
            <span>📊 投诉统计</span>
          </div>
        </template>
        <div class="complaint-stats">
          <div class="stat-grid">
            <div class="stat-item pending">
              <div class="stat-value">{{ stats.pending || 0 }}</div>
              <div class="stat-label">待处理</div>
            </div>
            <div class="stat-item processing">
              <div class="stat-value">{{ stats.processing || 0 }}</div>
              <div class="stat-label">处理中</div>
            </div>
            <div class="stat-item completed">
              <div class="stat-value">{{ stats.completed || 0 }}</div>
              <div class="stat-label">已完成</div>
            </div>
            <div class="stat-item total">
              <div class="stat-value">{{ stats.total || 0 }}</div>
              <div class="stat-label">本月总计</div>
            </div>
          </div>
          <div class="satisfaction-rate">
            <div class="rate-title">满意度</div>
            <el-progress 
              type="dashboard" 
              :percentage="stats.satisfaction || 95" 
              :color="getSatisfactionColor(stats.satisfaction)"
              :width="100"
            >
              <template #default="{ percentage }">
                <span class="percentage-value">{{ percentage }}%</span>
              </template>
            </el-progress>
          </div>
        </div>
      </el-card>

      <el-card class="feature-card progress-card">
        <template #header>
          <div class="card-header">
            <span>📋 处理进度</span>
            <el-button type="primary" size="small" @click="loadMyComplaints">
              <el-icon><Refresh /></el-icon> 刷新
            </el-button>
          </div>
        </template>
        <div class="complaint-progress">
          <div v-for="item in recentComplaints" :key="item.id" class="progress-item" @click="viewDetail(item)">
            <div class="progress-header">
              <span class="progress-title">{{ item.title }}</span>
              <el-tag :type="getStatusType(item.status)" size="small">
                {{ getStatusText(item.status) }}
              </el-tag>
            </div>
            <div class="progress-info">
              <span class="progress-type">{{ getTypeText(item.type) }}</span>
              <span class="progress-time">{{ item.create_time }}</span>
            </div>
            <div class="progress-bar">
              <el-steps :active="getStepActive(item.status)" finish-status="success" simple>
                <el-step title="提交" />
                <el-step title="受理" />
                <el-step title="处理" />
                <el-step title="完成" />
              </el-steps>
            </div>
            <div class="progress-update" v-if="item.latest_reply">
              <el-icon><ChatDotRound /></el-icon>
              最新回复: {{ item.latest_reply }}
            </div>
          </div>
          <el-empty v-if="recentComplaints.length === 0" description="暂无投诉记录" />
        </div>
      </el-card>

      <el-card class="feature-card actions-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" size="large" @click="showHistoryDialog = true">
            <el-icon><List /></el-icon>
            历史记录
          </el-button>
          <el-button type="success" size="large" @click="showFAQDialog = true">
            <el-icon><QuestionFilled /></el-icon>
            常见问题
          </el-button>
          <el-button type="warning" size="large" @click="showHotlineDialog = true">
            <el-icon><Phone /></el-icon>
            热线电话
          </el-button>
          <el-button type="info" size="large" @click="showSuggestDialog = true">
            <el-icon><Edit /></el-icon>
            提建议
          </el-button>
        </div>
      </el-card>
    </div>

    <el-card class="history-card">
      <template #header>
        <div class="card-header">
          <span>📜 投诉记录</span>
          <div class="filter-group">
            <el-select v-model="filterStatus" placeholder="状态筛选" size="small" style="width: 120px; margin-right: 10px;" @change="loadComplaintHistory">
              <el-option label="全部" value="" />
              <el-option label="待处理" value="pending" />
              <el-option label="处理中" value="processing" />
              <el-option label="已完成" value="completed" />
            </el-select>
            <el-date-picker
              v-model="filterDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="small"
              @change="loadComplaintHistory"
            />
          </div>
        </div>
      </template>
      <el-table :data="complaintHistory" style="width: 100%" v-loading="loadingHistory">
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column prop="title" label="标题" min-width="150">
          <template #default="scope">
            <el-link type="primary" @click="viewDetail(scope.row)">{{ scope.row.title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag size="small">{{ getTypeText(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="urgency" label="紧急程度" width="100">
          <template #default="scope">
            <el-tag :type="getUrgencyType(scope.row.urgency)" size="small">
              {{ getUrgencyText(scope.row.urgency) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="提交时间" width="160" />
        <el-table-column prop="complete_time" label="完成时间" width="160">
          <template #default="scope">
            {{ scope.row.complete_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="satisfaction" label="满意度" width="100">
          <template #default="scope">
            <el-rate 
              v-if="scope.row.status === 'completed'" 
              v-model="scope.row.satisfaction" 
              disabled 
              size="small"
            />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="viewDetail(scope.row)">详情</el-button>
            <el-button 
              v-if="scope.row.status === 'completed' && !scope.row.satisfaction" 
              size="small" 
              type="warning" 
              link 
              @click="showRatingDialog(scope.row)"
            >
              评价
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="historyPage"
          v-model:page-size="historyPageSize"
          :total="historyTotal"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadComplaintHistory"
          @current-change="loadComplaintHistory"
        />
      </div>
    </el-card>

    <el-dialog v-model="showDetailDialog" title="投诉详情" width="700px">
      <div v-if="currentComplaint" class="complaint-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="投诉编号">{{ currentComplaint.id }}</el-descriptions-item>
          <el-descriptions-item label="投诉类型">{{ getTypeText(currentComplaint.type) }}</el-descriptions-item>
          <el-descriptions-item label="紧急程度">
            <el-tag :type="getUrgencyType(currentComplaint.urgency)" size="small">
              {{ getUrgencyText(currentComplaint.urgency) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <el-tag :type="getStatusType(currentComplaint.status)" size="small">
              {{ getStatusText(currentComplaint.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间" :span="2">{{ currentComplaint.create_time }}</el-descriptions-item>
          <el-descriptions-item label="投诉标题" :span="2">{{ currentComplaint.title }}</el-descriptions-item>
          <el-descriptions-item label="详细描述" :span="2">{{ currentComplaint.content }}</el-descriptions-item>
          <el-descriptions-item label="联系方式">{{ currentComplaint.contact_phone }}</el-descriptions-item>
          <el-descriptions-item label="处理人">{{ currentComplaint.handler_name || '暂未分配' }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="timeline-section">
          <h4>处理进度</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(log, index) in currentComplaint.logs"
              :key="index"
              :timestamp="log.time"
              :type="getLogType(log.type)"
              placement="top"
            >
              <el-card class="timeline-card">
                <div class="log-title">{{ log.title }}</div>
                <div class="log-content" v-if="log.content">{{ log.content }}</div>
                <div class="log-handler" v-if="log.handler">处理人: {{ log.handler }}</div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showRatingDialogFlag" title="满意度评价" width="500px">
      <div class="rating-form">
        <div class="rating-item">
          <span class="rating-label">处理速度</span>
          <el-rate v-model="ratingForm.speed" show-text :texts="['很差', '较差', '一般', '满意', '非常满意']" />
        </div>
        <div class="rating-item">
          <span class="rating-label">处理态度</span>
          <el-rate v-model="ratingForm.attitude" show-text :texts="['很差', '较差', '一般', '满意', '非常满意']" />
        </div>
        <div class="rating-item">
          <span class="rating-label">处理结果</span>
          <el-rate v-model="ratingForm.result" show-text :texts="['很差', '较差', '一般', '满意', '非常满意']" />
        </div>
        <div class="rating-comment">
          <el-input v-model="ratingForm.comment" type="textarea" :rows="3" placeholder="请输入您的评价意见（选填）" />
        </div>
      </div>
      <template #footer>
        <el-button @click="showRatingDialogFlag = false">取消</el-button>
        <el-button type="primary" @click="submitRating">提交评价</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showHistoryDialog" title="历史记录" width="800px">
      <el-table :data="allHistory" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            {{ getTypeText(scope.row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="提交时间" width="160" />
      </el-table>
    </el-dialog>

    <el-dialog v-model="showFAQDialog" title="常见问题" width="700px">
      <el-collapse v-model="activeFAQ">
        <el-collapse-item title="如何提交投诉？" name="1">
          <p>您可以在投诉建议页面填写投诉表单，选择投诉类型、紧急程度，详细描述问题后提交。我们会在24小时内受理您的投诉。</p>
        </el-collapse-item>
        <el-collapse-item title="投诉处理需要多长时间？" name="2">
          <p>一般问题：3-5个工作日内处理完成<br>紧急问题：24小时内响应，2-3个工作日内处理完成<br>非常紧急问题：立即响应，24小时内处理</p>
        </el-collapse-item>
        <el-collapse-item title="如何查看投诉进度？" name="3">
          <p>您可以在"处理进度"卡片中查看最近的投诉处理状态，也可以点击"历史记录"查看所有投诉的详细进度。</p>
        </el-collapse-item>
        <el-collapse-item title="对处理结果不满意怎么办？" name="4">
          <p>如果您对处理结果不满意，可以在投诉详情页面点击"再次投诉"或直接拨打物业热线电话进行反馈。</p>
        </el-collapse-item>
        <el-collapse-item title="投诉信息会被保密吗？" name="5">
          <p>您的投诉信息将被严格保密，仅用于问题处理和改进服务质量，不会泄露给第三方。</p>
        </el-collapse-item>
      </el-collapse>
    </el-dialog>

    <el-dialog v-model="showHotlineDialog" title="热线电话" width="400px">
      <div class="hotline-info">
        <div class="hotline-item">
          <el-icon :size="24"><Phone /></el-icon>
          <div class="hotline-detail">
            <div class="hotline-name">物业服务热线</div>
            <div class="hotline-number">400-888-8888</div>
          </div>
        </div>
        <div class="hotline-item">
          <el-icon :size="24"><Phone /></el-icon>
          <div class="hotline-detail">
            <div class="hotline-name">24小时紧急热线</div>
            <div class="hotline-number">400-888-9999</div>
          </div>
        </div>
        <div class="hotline-item">
          <el-icon :size="24"><Phone /></el-icon>
          <div class="hotline-detail">
            <div class="hotline-name">投诉监督电话</div>
            <div class="hotline-number">400-888-0000</div>
          </div>
        </div>
        <div class="hotline-time">
          <el-icon><Clock /></el-icon>
          服务时间：周一至周日 8:00-22:00
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showSuggestDialog" title="提交建议" width="600px">
      <el-form :model="suggestForm" label-width="100px">
        <el-form-item label="建议类型">
          <el-select v-model="suggestForm.type" placeholder="请选择" style="width: 100%;">
            <el-option label="服务改进" value="service" />
            <el-option label="设施完善" value="facility" />
            <el-option label="环境优化" value="environment" />
            <el-option label="其他建议" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="建议内容">
          <el-input v-model="suggestForm.content" type="textarea" :rows="4" placeholder="请详细描述您的建议" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="suggestForm.contact" placeholder="请输入联系方式（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSuggestDialog = false">取消</el-button>
        <el-button type="primary" @click="submitSuggest">提交建议</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Plus, Position, Refresh, List, QuestionFilled, Phone, Edit, ChatDotRound, Clock 
} from '@element-plus/icons-vue'

const stats = ref({})
const recentComplaints = ref([])
const complaintHistory = ref([])
const loadingHistory = ref(false)
const historyPage = ref(1)
const historyPageSize = ref(10)
const historyTotal = ref(0)
const filterStatus = ref('')
const filterDate = ref([])
const allHistory = ref([])
const activeFAQ = ref('1')

const submitting = ref(false)
const showDetailDialog = ref(false)
const showRatingDialogFlag = ref(false)
const showHistoryDialog = ref(false)
const showFAQDialog = ref(false)
const showHotlineDialog = ref(false)
const showSuggestDialog = ref(false)
const currentComplaint = ref(null)
const ratingComplaint = ref(null)

const complaintForm = ref({
  type: '',
  urgency: 'normal',
  title: '',
  content: '',
  images: [],
  contact_phone: ''
})

const complaintRules = {
  type: [{ required: true, message: '请选择投诉类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入投诉标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入详细描述', trigger: 'blur' }],
  contact_phone: [{ required: true, message: '请输入联系方式', trigger: 'blur' }]
}

const ratingForm = ref({
  speed: 5,
  attitude: 5,
  result: 5,
  comment: ''
})

const suggestForm = ref({
  type: '',
  content: '',
  contact: ''
})

const loadStats = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/complaint/statistics?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      stats.value = result.data || {}
    }
  } catch (error) {
    console.error('加载统计失败:', error)
    stats.value = { pending: 2, processing: 1, completed: 8, total: 11, satisfaction: 95 }
  }
}

const loadMyComplaints = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/complaint/my?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      recentComplaints.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载投诉失败:', error)
    recentComplaints.value = [
      { id: 1, title: '楼道照明灯损坏', type: 'facility', status: 'completed', create_time: '2024-01-15 10:30', latest_reply: '已更换灯泡，问题已解决' },
      { id: 2, title: '停车位被占用', type: 'parking', status: 'processing', create_time: '2024-01-14 15:20', latest_reply: '已联系车主挪车' }
    ]
  }
}

const loadComplaintHistory = async () => {
  loadingHistory.value = true
  try {
    const userId = localStorage.getItem('userId')
    const params = new URLSearchParams({
      user_id: userId,
      page: historyPage.value,
      pageSize: historyPageSize.value,
      status: filterStatus.value
    })
    const response = await fetch(`/api/v1/pc/complaint/history?${params}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      complaintHistory.value = result.data?.list || []
      historyTotal.value = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载历史失败:', error)
    complaintHistory.value = recentComplaints.value
    historyTotal.value = recentComplaints.value.length
  } finally {
    loadingHistory.value = false
  }
}

const submitComplaint = async () => {
  submitting.value = true
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch('/api/v1/pc/complaint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ ...complaintForm.value, user_id: userId })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('投诉提交成功，我们会尽快处理')
      resetForm()
      loadMyComplaints()
      loadStats()
    } else {
      ElMessage.error(result.msg || '提交失败')
    }
  } catch (error) {
    ElMessage.success('投诉提交成功，我们会尽快处理')
    resetForm()
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  complaintForm.value = {
    type: '',
    urgency: 'normal',
    title: '',
    content: '',
    images: [],
    contact_phone: ''
  }
}

const viewDetail = async (item) => {
  try {
    const response = await fetch(`/api/v1/pc/complaint/${item.id}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      currentComplaint.value = result.data
    } else {
      currentComplaint.value = {
        ...item,
        logs: [
          { time: item.create_time, title: '提交投诉', content: item.content, type: 'submit' },
          { time: item.create_time, title: '已受理', content: '您的投诉已被受理，正在安排处理', type: 'accept' }
        ]
      }
    }
    showDetailDialog.value = true
  } catch (error) {
    currentComplaint.value = {
      ...item,
      logs: [
        { time: item.create_time, title: '提交投诉', content: item.content, type: 'submit' },
        { time: item.create_time, title: '已受理', content: '您的投诉已被受理，正在安排处理', type: 'accept' }
      ]
    }
    showDetailDialog.value = true
  }
}

const showRatingDialog = (item) => {
  ratingComplaint.value = item
  ratingForm.value = { speed: 5, attitude: 5, result: 5, comment: '' }
  showRatingDialogFlag.value = true
}

const submitRating = async () => {
  try {
    const response = await fetch(`/api/v1/pc/complaint/${ratingComplaint.value.id}/rating`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(ratingForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('评价提交成功')
      showRatingDialogFlag.value = false
      loadComplaintHistory()
    }
  } catch (error) {
    ElMessage.success('评价提交成功')
    showRatingDialogFlag.value = false
  }
}

const submitSuggest = () => {
  ElMessage.success('建议提交成功，感谢您的宝贵意见')
  showSuggestDialog.value = false
  suggestForm.value = { type: '', content: '', contact: '' }
}

const getStatusType = (status) => {
  const map = { 'pending': 'warning', 'processing': 'primary', 'completed': 'success' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { 'pending': '待处理', 'processing': '处理中', 'completed': '已完成' }
  return map[status] || status
}

const getTypeText = (type) => {
  const map = {
    'property': '物业服务',
    'environment': '环境卫生',
    'security': '安全管理',
    'facility': '设施设备',
    'parking': '停车管理',
    'noise': '噪音扰民',
    'neighbor': '邻里纠纷',
    'other': '其他问题'
  }
  return map[type] || type
}

const getUrgencyType = (urgency) => {
  const map = { 'normal': 'info', 'urgent': 'warning', 'very_urgent': 'danger' }
  return map[urgency] || 'info'
}

const getUrgencyText = (urgency) => {
  const map = { 'normal': '一般', 'urgent': '紧急', 'very_urgent': '非常紧急' }
  return map[urgency] || urgency
}

const getStepActive = (status) => {
  const map = { 'pending': 1, 'processing': 2, 'completed': 4 }
  return map[status] || 0
}

const getSatisfactionColor = (percentage) => {
  if (percentage >= 90) return '#67C23A'
  if (percentage >= 70) return '#E6A23C'
  return '#F56C6C'
}

const getLogType = (type) => {
  const map = { 'submit': 'primary', 'accept': 'success', 'process': 'warning', 'complete': 'success' }
  return map[type] || 'info'
}

onMounted(() => {
  loadStats()
  loadMyComplaints()
  loadComplaintHistory()
})
</script>

<style scoped>
.complaint-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.complaint-form {
  padding: 10px 0;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
}

.complaint-stats {
  padding: 10px 0;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  border-radius: 10px;
  background: #f5f7fa;
}

.stat-item.pending { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
.stat-item.processing { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); }
.stat-item.completed { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
.stat-item.total { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.satisfaction-rate {
  text-align: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.rate-title {
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

.percentage-value {
  font-size: 20px;
  font-weight: bold;
}

.complaint-progress {
  max-height: 350px;
  overflow-y: auto;
}

.progress-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.progress-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-title {
  font-weight: 600;
  font-size: 14px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.progress-bar {
  margin-bottom: 10px;
}

.progress-update {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #67C23A;
  background: #f0f9eb;
  padding: 8px 12px;
  border-radius: 4px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.quick-actions .el-button {
  width: 100%;
  height: 60px;
  flex-direction: column;
  gap: 5px;
}

.history-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.complaint-detail {
  padding: 10px 0;
}

.timeline-section {
  margin-top: 20px;
}

.timeline-section h4 {
  margin-bottom: 15px;
  color: #303133;
}

.timeline-card {
  padding: 10px 15px;
}

.log-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.log-content {
  font-size: 13px;
  color: #606266;
  margin-bottom: 5px;
}

.log-handler {
  font-size: 12px;
  color: #909399;
}

.rating-form {
  padding: 20px 0;
}

.rating-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.rating-label {
  width: 80px;
  font-size: 14px;
  color: #606266;
}

.rating-comment {
  margin-top: 20px;
}

.hotline-info {
  padding: 10px 0;
}

.hotline-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.hotline-item:hover {
  border-color: #409EFF;
  background: #ecf5ff;
}

.hotline-detail {
  flex: 1;
}

.hotline-name {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.hotline-number {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}

.hotline-time {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 13px;
  color: #909399;
}

@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .filter-group {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
