import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/activities',
      name: 'activities',
      component: () => import('../views/Activities.vue')
    },
    {
      path: '/activities/detail/:id',
      name: 'activityDetail',
      component: () => import('../views/ActivityDetail.vue')
    },
    {
      path: '/services',
      name: 'services',
      component: () => import('../views/Services.vue')
    },
    {
      path: '/government',
      name: 'government',
      component: () => import('../views/Government.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/admin',
      name: 'adminDashboard',
      component: () => import('../views/admin/Dashboard.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/users',
      name: 'adminUserManage',
      component: () => import('../views/admin/UserManage.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/buildings',
      name: 'adminBuildingManage',
      component: () => import('../views/admin/BuildingManage.vue'),
      meta: { requiresAdmin: true }
    },
    // ==================== 智慧社区管理 ====================
    // 智能门禁管理
    {
      path: '/admin/access-control/devices',
      name: 'adminAccessDevices',
      component: () => import('../views/admin/smart-community/AccessControlDevices.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/access-control/permissions',
      name: 'adminAccessPermissions',
      component: () => import('../views/admin/smart-community/AccessControlPermissions.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/access-control/records',
      name: 'adminAccessRecords',
      component: () => import('../views/admin/smart-community/AccessControlRecords.vue'),
      meta: { requiresAdmin: true }
    },
    // 物业报修管理
    {
      path: '/admin/repair/orders',
      name: 'adminRepairOrders',
      component: () => import('../views/admin/smart-community/RepairOrders.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/repair/technicians',
      name: 'adminRepairTechnicians',
      component: () => import('../views/admin/smart-community/RepairTechnicians.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/repair/statistics',
      name: 'adminRepairStatistics',
      component: () => import('../views/admin/smart-community/RepairStatistics.vue'),
      meta: { requiresAdmin: true }
    },
    // 公告通知管理
    {
      path: '/admin/notices',
      name: 'adminNotices',
      component: () => import('../views/admin/smart-community/Notices.vue'),
      meta: { requiresAdmin: true }
    },
    // 智能水电管理
    {
      path: '/admin/utility/meters',
      name: 'adminUtilityMeters',
      component: () => import('../views/admin/smart-community/UtilityMeters.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/utility/usage',
      name: 'adminUtilityUsage',
      component: () => import('../views/admin/smart-community/UtilityUsage.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/utility/alerts',
      name: 'adminUtilityAlerts',
      component: () => import('../views/admin/smart-community/UtilityAlerts.vue'),
      meta: { requiresAdmin: true }
    },
    // 费用缴纳管理
    {
      path: '/admin/payment',
      name: 'adminPayment',
      component: () => import('../views/admin/smart-community/Payment.vue'),
      meta: { requiresAdmin: true }
    },
    // 智能停车管理
    {
      path: '/admin/parking',
      name: 'adminParking',
      component: () => import('../views/admin/smart-community/Parking.vue'),
      meta: { requiresAdmin: true }
    },
    // 快递柜管理
    {
      path: '/admin/locker',
      name: 'adminLocker',
      component: () => import('../views/admin/smart-community/Locker.vue'),
      meta: { requiresAdmin: true }
    },
    // 访客管理
    {
      path: '/admin/visitor',
      name: 'adminVisitor',
      component: () => import('../views/admin/smart-community/Visitor.vue'),
      meta: { requiresAdmin: true }
    },
    // 投诉建议管理
    {
      path: '/admin/complaint',
      name: 'adminComplaint',
      component: () => import('../views/admin/smart-community/Complaints.vue'),
      meta: { requiresAdmin: true }
    },
    // 监控管理
    {
      path: '/admin/monitoring',
      name: 'adminMonitoring',
      component: () => import('../views/admin/smart-community/Monitoring.vue'),
      meta: { requiresAdmin: true }
    },
    // 社区活动管理
    {
      path: '/admin/activity',
      name: 'adminActivity',
      component: () => import('../views/admin/smart-community/Activity.vue'),
      meta: { requiresAdmin: true }
    },

    // ==================== 绿色能源管理 ====================
    // AI垃圾分类管理
    {
      path: '/admin/garbage/classification',
      name: 'adminGarbageClassification',
      component: () => import('../views/admin/green-energy/GarbageClassification.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/garbage/records',
      name: 'adminGarbageRecords',
      component: () => import('../views/admin/green-energy/GarbageRecords.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/garbage/statistics',
      name: 'adminGarbageStatistics',
      component: () => import('../views/admin/green-energy/GarbageStatistics.vue'),
      meta: { requiresAdmin: true }
    },
    // 碳足迹管理
    {
      path: '/admin/carbon-footprint',
      name: 'adminCarbonFootprint',
      component: () => import('../views/admin/green-energy/CarbonFootprint.vue'),
      meta: { requiresAdmin: true }
    },
    // 绿色论坛管理
    {
      path: '/admin/green-forum',
      name: 'adminGreenForum',
      component: () => import('../views/admin/green-energy/GreenForum.vue'),
      meta: { requiresAdmin: true }
    },
    // 环保数据监测
    {
      path: '/admin/environment',
      name: 'adminEnvironment',
      component: () => import('../views/admin/green-energy/Environment.vue'),
      meta: { requiresAdmin: true }
    },
    // 绿色积分管理
    {
      path: '/admin/green-points',
      name: 'adminGreenPoints',
      component: () => import('../views/admin/green-energy/GreenPoints.vue'),
      meta: { requiresAdmin: true }
    },
    // AI生活建议管理
    {
      path: '/admin/ai-tips',
      name: 'adminAITips',
      component: () => import('../views/admin/green-energy/AITips.vue'),
      meta: { requiresAdmin: true }
    },
    // 绿色出行规划
    {
      path: '/admin/green-travel',
      name: 'adminGreenTravel',
      component: () => import('../views/admin/green-energy/GreenTravel.vue'),
      meta: { requiresAdmin: true }
    },
    // 家居节能优化
    {
      path: '/admin/energy-optimization',
      name: 'adminEnergyOptimization',
      component: () => import('../views/admin/green-energy/EnergyOptimization.vue'),
      meta: { requiresAdmin: true }
    },
    // 健康管理
    {
      path: '/admin/health',
      name: 'adminHealth',
      component: () => import('../views/admin/green-energy/Health.vue'),
      meta: { requiresAdmin: true }
    },
    // 饮食养生
    {
      path: '/admin/diet',
      name: 'adminDiet',
      component: () => import('../views/admin/green-energy/Diet.vue'),
      meta: { requiresAdmin: true }
    },
    // 养生知识库
    {
      path: '/admin/knowledge',
      name: 'adminKnowledge',
      component: () => import('../views/admin/green-energy/Knowledge.vue'),
      meta: { requiresAdmin: true }
    },
    // 系统设置
    {
      path: '/admin/settings',
      name: 'adminSettings',
      component: () => import('../views/admin/Settings.vue'),
      meta: { requiresAdmin: true }
    },
    // 评价管理
    {
      path: '/admin/reviews',
      name: 'adminReviews',
      component: () => import('../views/admin/ReviewManage.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/op/users',
      name: 'opUserManage',
      component: () => import('../views/op/UserManage.vue'),
      meta: { requiresOp: true }
    },
    {
      path: '/op/buildings',
      name: 'opBuildingManage',
      component: () => import('../views/op/BuildingManage.vue'),
      meta: { requiresOp: true }
    },
    {
      path: '/green-energy',
      name: 'greenEnergy',
      component: () => import('../views/GreenEnergy.vue')
    },
    {
      path: '/green-energy/knowledge',
      name: 'greenKnowledge',
      component: () => import('../views/green-energy/Knowledge.vue')
    },
    {
      path: '/green-energy/garbage',
      name: 'greenGarbage',
      component: () => import('../views/green-energy/GarbageClassification.vue')
    },
    {
      path: '/green-energy/health',
      name: 'greenHealth',
      component: () => import('../views/green-energy/Health.vue')
    },
    {
      path: '/green-energy/diet',
      name: 'greenDiet',
      component: () => import('../views/green-energy/Diet.vue')
    },
    {
      path: '/green-energy/carbon-footprint',
      name: 'carbonFootprint',
      component: () => import('../views/green-energy/CarbonFootprint.vue')
    },
    {
      path: '/green-energy/forum',
      name: 'greenForum',
      component: () => import('../views/green-energy/GreenForum.vue')
    },
    {
      path: '/green-energy/environment',
      name: 'communityEnvironment',
      component: () => import('../views/green-energy/CommunityEnvironment.vue')
    },
    {
      path: '/green-energy/energy-tips',
      name: 'energyTips',
      component: () => import('../views/green-energy/EnergyTips.vue')
    },
    {
      path: '/green-energy/points',
      name: 'greenPoints',
      component: () => import('../views/green-energy/GreenPoints.vue')
    },
    {
      path: '/green-energy/ai-tips',
      name: 'aiGreenTips',
      component: () => import('../views/green-energy/AIGreenTips.vue')
    },
    {
      path: '/green-energy/travel',
      name: 'greenTravel',
      component: () => import('../views/green-energy/GreenTravel.vue')
    },
    {
      path: '/green-energy/home-energy',
      name: 'homeEnergyOptimization',
      component: () => import('../views/green-energy/HomeEnergyOptimization.vue')
    },
    // ==================== 智慧社区基础功能 ====================
    // 智能门禁
    {
      path: '/access-control',
      name: 'accessControl',
      component: () => import('../views/smart-community/AccessControl.vue')
    },
    {
      path: '/access-control/records',
      name: 'accessRecords',
      component: () => import('../views/smart-community/AccessRecords.vue')
    },
    // 物业报修
    {
      path: '/repair',
      name: 'repair',
      component: () => import('../views/smart-community/Repair.vue')
    },
    {
      path: '/repair/my-orders',
      name: 'myRepairOrders',
      component: () => import('../views/smart-community/MyRepairOrders.vue')
    },
    // 公告通知
    {
      path: '/notices',
      name: 'notices',
      component: () => import('../views/smart-community/Notices.vue')
    },
    {
      path: '/notices/:id',
      name: 'noticeDetail',
      component: () => import('../views/smart-community/NoticeDetail.vue')
    },
    // 智能水电
    {
      path: '/utility',
      name: 'utility',
      component: () => import('../views/smart-community/Utility.vue')
    },
    {
      path: '/utility/usage',
      name: 'utilityUsage',
      component: () => import('../views/smart-community/UtilityUsage.vue')
    },
    // 费用缴纳
    {
      path: '/payment',
      name: 'payment',
      component: () => import('../views/smart-community/Payment.vue')
    },
    {
      path: '/payment/bills',
      name: 'myBills',
      component: () => import('../views/smart-community/MyBills.vue')
    },
    // 智能停车
    {
      path: '/parking',
      name: 'parking',
      component: () => import('../views/smart-community/Parking.vue')
    },
    {
      path: '/parking/my-vehicles',
      name: 'myVehicles',
      component: () => import('../views/smart-community/MyVehicles.vue')
    },
    // 快递柜
    {
      path: '/locker',
      name: 'locker',
      component: () => import('../views/smart-community/Locker.vue')
    },
    {
      path: '/locker/my-packages',
      name: 'myPackages',
      component: () => import('../views/smart-community/MyPackages.vue')
    },
    // 访客管理
    {
      path: '/visitor',
      name: 'visitor',
      component: () => import('../views/smart-community/Visitor.vue')
    },
    {
          path: '/visitor/appointments',
          name: 'visitorAppointments',
          component: () => import('../views/smart-community/VisitorAppointments.vue')
        },
        {
          path: '/visitor/records',
          name: 'visitorRecords',
          component: () => import('../views/smart-community/VisitorRecords.vue')
        },
    // 投诉建议
    {
      path: '/complaint',
      name: 'complaint',
      component: () => import('../views/smart-community/Complaint.vue')
    },
    {
      path: '/complaint/my-complaints',
      name: 'myComplaints',
      component: () => import('../views/smart-community/MyComplaints.vue')
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  console.log('路由守卫:', from.path, '->', to.path)
  const isLoggedIn = localStorage.getItem('token')
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
  const userRole = userInfo.role || '居民'
  
  // 需要登录的页面
  const requireAuth = ['profile']
  
  // 需要管理员权限的页面
  const requiresAdmin = to.meta.requiresAdmin
  
  // 需要运营权限的页面
  const requiresOp = to.meta.requiresOp
  
  if (requiresAdmin) {
    if (!isLoggedIn) {
      console.log('需要管理员权限，未登录')
      next('/login')
    } else if (userRole !== '管理员') {
      console.log('需要管理员权限，无权限')
      next('/')
    } else {
      next()
    }
  } else if (requiresOp) {
    if (!isLoggedIn) {
      console.log('需要运营权限，未登录')
      next('/login')
    } else if (!['运营', '管理员'].includes(userRole)) {
      console.log('需要运营权限，无权限')
      next('/')
    } else {
      next()
    }
  } else if (requireAuth.includes(to.name) && !isLoggedIn) {
    console.log('需要登录')
    next('/login')
  } else {
    console.log('允许导航')
    next()
  }
})

router.afterEach((to, from) => {
  console.log('导航完成:', to.path)
})

export default router