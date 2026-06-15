<template>
	<scroll-view
	  class="mine-page"
	  scroll-y
	  refresher-enabled
	  :refresher-triggered="refreshing"
	  @refresherrefresh="onRefresh"
	>
  <div class="mine-page">
    <!-- 个人信息大卡片 -->
    <div class="profile-card" @click="goToEdit">
      <div class="profile-content">
        <!-- 左侧头像 -->
        <div class="avatar-wrapper">
          <img 
            src="/static/bg/touxiang.jpg" 
            alt="头像" 
            class="avatar"
          />
          <div class="edit-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
              <path d="m15 5 4 4"/>
            </svg>
          </div>
        </div>

        <!-- 右侧信息 -->
        <div class="user-info">
          <h2 class="user-name">{{ userInfo.name || '测试用户' }}</h2>
          <p class="user-detail">{{ userInfo.major || '软件工程' }} / {{ userInfo.grade || '大三' }}</p>
          <p class="user-detail">目标：{{ userInfo.target || '前端工程师' }}</p>
          <div class="mood-tag" :style="{ backgroundColor: currentMood.bgColor }">
            {{ currentMood.text }}
          </div>
        </div>
      </div>

      <!-- 底部进度环 -->
      <div class="progress-section">
        <div class="progress-ring-container">
          <svg class="progress-ring" width="80" height="80">
            <circle
              class="progress-ring-bg"
              cx="40"
              cy="40"
              r="32"
              fill="none"
              stroke="#FFE4D4"
              stroke-width="6"
            />
            <circle
              class="progress-ring-fill"
              cx="40"
              cy="40"
              r="32"
              fill="none"
              stroke="#F98C53"
              stroke-width="6"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="progressOffset"
              transform="rotate(-90 40 40)"
            />
          </svg>
          <div class="progress-text">{{ userProgress.toFixed(1) }}%</div>
        </div>
        <div class="progress-label">
          <div class="progress-title">当前路径进度</div>
          <div class="progress-subtitle">已完成 {{ completedSteps }}/{{ totalSteps }} 步</div>
          <div class="progress-prediction">预计2周后完成此阶段</div>
        </div>
      </div>
	 
    </div>

    <!-- 数据可视化区 -->
    <div class="data-section">
      <!-- 情绪曲线卡片 - 强化多模态感知 -->
      <div class="data-card mood-card">
        <div class="card-header">
          <h3 class="card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ABD7FB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
              <path d="M3 3v18h18"/>
              <path d="m19 9-5 5-4-4-3 3"/>
            </svg>
            多模态情感感知
          </h3>
          <div class="time-filter">
            <button 
              :class="['filter-btn', { active: timeRange === 7 }]"
              @click="timeRange = 7"
            >
              近7天
            </button>
            <button 
              :class="['filter-btn', { active: timeRange === 30 }]"
              @click="timeRange = 30"
            >
              近30天
            </button>
          </div>
        </div>
        
        <!-- 感知来源标签 -->
        <div class="sensor-tags">
          <span class="sensor-tag">
            <span class="sensor-dot text"></span>
            文本情绪（日记分析）
          </span>
          <span class="sensor-tag">
            <span class="sensor-dot behavior"></span>
            行为特征（深夜活跃）
          </span>
          <span class="sensor-tag" @click="goToDiary">
            <span class="sensor-dot fusion"></span>
            多模态融合结果
            <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </span>
        </div>

        <!-- 情绪曲线可视化（可点击查看详情） -->
        <div class="mood-chart" @click="goToEmotionDetail">
          <div class="chart-line">
            <svg viewBox="0 0 300 100" class="line-chart">
              <polyline
                :points="moodChartPoints"
                fill="none"
                stroke="#ABD7FB"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <circle 
                v-for="(point, index) in moodData" 
                :key="index"
                :cx="point.x" 
                :cy="point.y" 
                r="4" 
                fill="#ABD7FB"
                class="chart-point"
                @click.stop="showMoodDetail(index)"
              />
            </svg>
          </div>
          <div class="chart-labels">
            <span v-for="(label, index) in chartLabels" :key="index">{{ label }}</span>
          </div>
        </div>

        <div class="mood-summary" :class="moodSummaryClass">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" :stroke="moodSummaryColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
            <circle cx="12" cy="12" r="10"/>
            <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
            <line x1="9" x2="9.01" y1="9" y2="9"/>
            <line x1="15" x2="15.01" y1="9" y2="9"/>
          </svg>
          {{ moodSummary }}
          <span class="summary-source">基于近3天日记 + 深夜活跃度分析</span>
        </div>
      </div>

      <!-- 路径进度卡片 - 强化个性化发展 -->
      <div class="data-card path-card">
        <div class="card-header">
          <h3 class="card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F98C53" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
              <path d="M12 2v20M2 12l10-10 10 10"/>
            </svg>
            我的成长路径
          </h3>
          <button class="detail-btn" @click="goToPath">
            查看完整路径
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" style="margin-left: 4px;">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
        </div>

        <!-- 情感适配提示 -->
        <div class="emotion-fit-tip" @click="goToPath">
          <span class="fit-icon">🌱</span>
          <span class="fit-text">根据你当前情绪状态，系统为你调整了任务难度</span>
          <span class="fit-badge">轻度压力模式</span>
        </div>

        <!-- 水平进度条 -->
        <div class="horizontal-progress">
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: userProgress + '%' }"></div>
          </div>
          <div class="progress-info">{{ completedSteps }}/{{ totalSteps }} 已完成</div>
        </div>

        <!-- 最近步骤列表（带情绪适配标签） -->
        <div class="steps-list">
          <div 
            v-for="step in recentSteps" 
            :key="step.id"
            class="step-item"
            @click="goToStepDetail(step.id)"
          >
            <div class="step-icon" :class="step.status">
              <svg v-if="step.status === 'completed'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <svg v-else-if="step.status === 'ongoing'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="1"/>
              </svg>
            </div>
            <div class="step-content">
              <div class="step-title">{{ step.title }}</div>
              <div class="step-meta">
                <span class="step-status-text" :class="step.status">
                  {{ getStatusText(step.status) }}
                </span>
                <span v-if="step.moodFit" class="step-mood-fit">
                  <span class="fit-icon">{{ step.moodFit.icon }}</span>
                  {{ step.moodFit.text }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速查看全部任务 -->
        <div class="view-all-tasks" @click="goToPath">
          查看全部 {{ totalSteps }} 个任务
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F98C53" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 情绪日记快捷入口（新增） -->
    <div class="quick-diary" @click="goToDiary">
      <div class="diary-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
          <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
        </svg>
      </div>
      <div class="diary-content">
        <div class="diary-title">记录今日心情</div>
        <div class="diary-subtitle">帮助系统更懂你</div>
      </div>
      <div class="diary-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F98C53" stroke-width="2">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </div>
    </div>

    <!-- 功能列表区 -->
    <div class="function-section">
      <h3 class="section-title">更多功能</h3>
      <div class="function-list">
        <div 
          v-for="func in functionList" 
          :key="func.id"
          class="function-item"
          :class="{ logout: func.id === 'logout' }"
          @click="handleFunction(func.id)"
        >
          <div class="function-left">
            <component :is="func.icon" :color="func.color" class="function-icon" />
            <span class="function-text">{{ func.label }}</span>
          </div>
          <svg v-if="func.id !== 'logout'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 底部留白 -->
    <div class="bottom-spacer"></div>
  </div>
  </scroll-view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
 
// ========== API 配置 ==========
const API_BASE_URL = 'http://127.0.0.1:8000'

// ========== 页面路径常量 ==========
const PAGE_PATHS = {
  edit: '/pages/mine/edit',
  path: '/pages/path2/path2',
  pathDetail: '/pages/path/detail',
  emotionDetail: '/pages/diary/EmotionGarden/EmotionGarden',
  diary: '/pages/diary/diary',
  stepDetail: '/pages/path2/path2',
  favorite: '/pages/mine/favorite',
  square: '/pages/square/square',
  help: '/pages/help/help',
  settings: '/pages/settings/settings',
  login: '/pages/login/login'
}

// ========== 用户信息 ==========
const userInfo = ref({
  name: '',
  avatar: '',
  major: '',
  grade: '',
  target: ''
})

// ========== 路径进度 ==========
const userProgress = ref(0)
const completedSteps = ref(0)
const totalSteps = ref(0)
const currentPathId = ref(null)
const recentSteps = ref([])

// ========== 情绪数据 ==========
const emotionData = ref({
  currentMood: { text: '加载中...', bgColor: '#E0E0E0' },
  chartData: [],
  summary: '正在加载情绪数据...',
  summaryClass: 'neutral',
  summaryColor: '#999',
  recentDays: [],
  diaryCount: 0,
  hasTodayDiary: false
})

// 情绪映射
const moodMap = {
  1: { emoji: '☀️', name: '闪闪发光', text: '开心', bgColor: '#D2E0AA', summary: '近一周情绪积极向上，充满能量', summaryClass: 'positive', summaryColor: '#52c41a' },
  2: { emoji: '🌱', name: '温暖生长', text: '平静', bgColor: '#ABD7FB', summary: '近一周情绪平稳，心态平和', summaryClass: 'positive', summaryColor: '#52c41a' },
  3: { emoji: '🍃', name: '微风思绪', text: '思考', bgColor: '#C4A0E5', summary: '近一周处于思考状态，思绪活跃', summaryClass: 'positive', summaryColor: '#52c41a' },
  4: { emoji: '🌧️', name: '雨滴心情', text: '低落', bgColor: '#FFB3BA', summary: '近一周情绪偏低，需要注意调节', summaryClass: 'warning', summaryColor: '#faad14' },
  5: { emoji: '✨', name: '马戏团日', text: '兴奋', bgColor: '#FFD966', summary: '近一周精力充沛，热情高涨', summaryClass: 'positive', summaryColor: '#52c41a' },
  6: { emoji: '🫧', name: '拼图时刻', text: '困惑', bgColor: '#C4A0E5', summary: '近一周处于探索状态', summaryClass: 'neutral', summaryColor: '#999' }
}

// ========== 时间范围 ==========
const timeRange = ref(7)

// ========== 刷新状态 ==========
const refreshing = ref(false)
const lastUpdateTime = ref('')

// ========== 本地存储 key ==========
const PATH_STORAGE_KEY = 'user_path_tasks'

// ========== 从本地加载用户信息 ==========
const loadFromLocal = () => {
  try {
    const localInfo = uni.getStorageSync('userInfo')
    if (localInfo) {
      userInfo.value = localInfo
      console.log('从本地加载用户信息:', userInfo.value)
    }
  } catch (e) {
    console.error('加载本地数据失败:', e)
  }
}

// ========== 检查登录状态 ==========
const checkLoginStatus = () => {
  const token = uni.getStorageSync('token')
  const isLoggedIn = uni.getStorageSync('isLoggedIn')
  if (token && isLoggedIn) return true
  uni.reLaunch({ url: '/pages/login/login' })
  return false
}

// ========== 获取用户信息 ==========
const fetchUserInfo = () => {
  if (!checkLoginStatus()) return Promise.reject('未登录')
  uni.showLoading({ title: '加载中...' })
  return new Promise((resolve, reject) => {
    uni.request({
      url: API_BASE_URL + '/user/profile',
      method: 'POST',
      header: { 'Authorization': 'Bearer ' + uni.getStorageSync('token') },
      success: (res) => {
        if (res.data && res.data.code === 200) {
          const data = res.data.data
          let avatarUrl = data.avatar || ''
          if (!avatarUrl || avatarUrl.startsWith('blob:')) {
            avatarUrl = 'https://images.unsplash.com/photo-1621962366578-7364ccb3352b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=200'
          }
          userInfo.value = {
            name: data.nickname || '知径用户',
            avatar: avatarUrl,
            major: data.major || '未设置',
            grade: data.grade || '未设置',
            target: data.target_career || '未设置'
          }
          const now = new Date()
          lastUpdateTime.value = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`
          uni.setStorageSync('userInfo', userInfo.value)
          resolve(userInfo.value)
        } else if (res.data && res.data.code === 401) {
          uni.removeStorageSync('token')
          uni.removeStorageSync('userInfo')
          const pages = getCurrentPages()
          if (pages[pages.length - 1].route !== 'pages/mine/edit') {
            uni.reLaunch({ url: '/pages/login/login' })
          }
          reject('token无效')
        } else {
          loadFromLocal()
          resolve(userInfo.value)
        }
      },
      fail: (err) => {
        console.error('获取用户信息失败:', err)
        loadFromLocal()
        reject(err)
      },
      complete: () => uni.hideLoading()
    })
  })
}

// ========== 从本地存储加载路径进度 ==========
const loadPathProgressFromStorage = () => {
  const saved = uni.getStorageSync(PATH_STORAGE_KEY)
  if (saved) {
    try {
      const data = JSON.parse(saved)
      const tasks = data.tasks || []
      totalSteps.value = data.totalSteps || tasks.length
      completedSteps.value = data.completedSteps || tasks.filter(t => t.completed).length
      userProgress.value = totalSteps.value === 0 ? 0 : (completedSteps.value / totalSteps.value) * 100
      recentSteps.value = tasks.slice(0, 3).map(task => ({
        id: task.id,
        title: task.title,
        status: task.completed ? 'completed' : (task.current ? 'ongoing' : 'pending'),
        moodFit: task.current ? { icon: '🌱', text: '进行中' } : null
      }))
      console.log('从本地存储加载路径进度成功')
      return true
    } catch (e) {
      console.error('解析本地路径进度失败', e)
    }
  }
  return false
}

// ========== 获取用户当前路径（后端接口）==========
const fetchUserCurrentPath = () => {
  uni.request({
    url: API_BASE_URL + '/api/user/current-path/1',
    method: 'GET',
    success: (res) => {
      if (res.data && res.data.code === 200 && res.data.data) {
        const pathData = res.data.data
        currentPathId.value = pathData.path_id
        userProgress.value = pathData.progress || 0
        fetchPathDetail(pathData.path_id)
      } else {
        setDefaultPathData()
      }
    },
    fail: () => setDefaultPathData()
  })
}

const fetchPathDetail = (pathId) => {
  uni.request({
    url: API_BASE_URL + `/api/path/${pathId}`,
    method: 'GET',
    data: { user_id: 1 },
    success: (res) => {
      if (res.data && res.data.code === 200) {
        const data = res.data.data
        const tasks = data.tasks || []
        totalSteps.value = tasks.length
        completedSteps.value = tasks.filter(t => t.completed).length
        userProgress.value = totalSteps.value === 0 ? 0 : (completedSteps.value / totalSteps.value) * 100
        recentSteps.value = tasks.slice(0, 3).map(task => ({
          id: task.id,
          title: task.title,
          status: task.completed ? 'completed' : (task.current ? 'ongoing' : 'pending'),
          moodFit: task.current ? { icon: '🌱', text: '进行中' } : null
        }))
        // 存入本地存储
        const progressData = {
          tasks: tasks,
          totalSteps: totalSteps.value,
          completedSteps: completedSteps.value,
          progressPercent: userProgress.value,
          lastUpdate: Date.now()
        }
        uni.setStorageSync(PATH_STORAGE_KEY, JSON.stringify(progressData))
      } else {
        setDefaultPathData()
      }
    },
    fail: () => setDefaultPathData()
  })
}

// ========== 设置默认路径数据 ==========
const setDefaultPathData = () => {
  totalSteps.value = 8
  completedSteps.value = 3
  userProgress.value = 37
  recentSteps.value = [
    { id: 1, title: '学习 Flex 布局', status: 'ongoing', moodFit: { icon: '🌱', text: '进行中' } },
    { id: 2, title: '完成项目实战', status: 'pending', moodFit: { icon: '⏳', text: '待开始' } },
    { id: 3, title: 'JavaScript 基础复习', status: 'completed', moodFit: null }
  ]
  // 保存默认数据到本地存储
  const defaultTasks = recentSteps.value.map((step, idx) => ({
    id: step.id,
    title: step.title,
    completed: step.status === 'completed',
    current: step.status === 'ongoing'
  }))
  const progressData = {
    tasks: defaultTasks,
    totalSteps: totalSteps.value,
    completedSteps: completedSteps.value,
    progressPercent: userProgress.value,
    lastUpdate: Date.now()
  }
  uni.setStorageSync(PATH_STORAGE_KEY, JSON.stringify(progressData))
}

// ========== 获取真实情绪数据 ==========
const fetchRealMoodData = () => {
  try {
    const diaries = uni.getStorageSync('infog-mood-diaries')
    if (diaries) {
      const diaryList = JSON.parse(diaries)
      const today = new Date().toDateString()
      const sortedDiaries = [...diaryList].sort((a, b) => new Date(b.date) - new Date(a.date))
      const todayDiary = sortedDiaries.find(d => new Date(d.date).toDateString() === today)
      const last7Days = []
      const chartData = []
      for (let i = 6; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        const dateStr = date.toDateString()
        const diary = sortedDiaries.find(d => new Date(d.date).toDateString() === dateStr)
        if (diary) {
          const moodId = diary.predicted_mood || diary.manual_mood || 2
          const moodScore = { 1: 85, 2: 75, 3: 65, 4: 45, 5: 80, 6: 55 }[moodId] || 60
          chartData.push(moodScore)
          last7Days.push({
            date: date,
            moodId: moodId,
            moodInfo: moodMap[moodId],
            text: diary.text ? diary.text.substring(0, 20) + '...' : '心情记录'
          })
        } else {
          chartData.push(50)
          last7Days.push({ date: date, moodId: null, moodInfo: null, text: '无记录' })
        }
      }
      const validMoods = last7Days.filter(d => d.moodId).map(d => d.moodId)
      const avgMoodId = validMoods.length > 0 ? Math.round(validMoods.reduce((a, b) => a + b, 0) / validMoods.length) : 2
      const avgMoodInfo = moodMap[avgMoodId] || moodMap[2]
      let summary = ''
      if (todayDiary) {
        const todayMoodId = todayDiary.predicted_mood || todayDiary.manual_mood || 2
        const todayMoodInfo = moodMap[todayMoodId]
        summary = `今天心情：${todayMoodInfo.text}。`
        if (validMoods.length > 3) {
          summary += ` 近一周整体${avgMoodInfo.text}，`
          summary += todayMoodId >= 4 ? '建议适当放松，照顾好自己～' : '状态不错，继续保持！'
        }
      } else {
        summary = '今天还没有记录心情，点击下方按钮开始记录吧～'
      }
      emotionData.value = {
        currentMood: todayDiary ? {
          text: moodMap[todayDiary.predicted_mood || todayDiary.manual_mood || 2].text,
          bgColor: moodMap[todayDiary.predicted_mood || todayDiary.manual_mood || 2].bgColor
        } : { text: '暂无记录', bgColor: '#E0E0E0' },
        chartData: chartData,
        summary: summary,
        summaryClass: avgMoodId >= 4 ? 'warning' : 'positive',
        summaryColor: avgMoodId >= 4 ? '#faad14' : '#52c41a',
        recentDays: last7Days,
        diaryCount: diaryList.length,
        hasTodayDiary: !!todayDiary
      }
    } else {
      emotionData.value = {
        currentMood: { text: '暂无记录', bgColor: '#E0E0E0' },
        chartData: [50, 50, 50, 50, 50, 50, 50],
        summary: '还没有记录过心情日记，点击下方按钮开始记录吧～',
        summaryClass: 'neutral',
        summaryColor: '#999',
        recentDays: [],
        diaryCount: 0,
        hasTodayDiary: false
      }
    }
  } catch (error) {
    console.error('获取情绪数据失败:', error)
  }
}

// ========== 刷新所有数据 ==========
const refreshAllData = () => {
  refreshing.value = true
  Promise.all([fetchUserInfo(), fetchRealMoodData()])
    .finally(() => {
      setTimeout(() => {
        refreshing.value = false
        uni.showToast({ title: '刷新成功', icon: 'success' })
      }, 500)
    })
}

// ========== 下拉刷新 ==========
const onRefresh = () => refreshAllData()

// ========== 情绪数据计算 ==========
const moodData = computed(() => {
  const data = emotionData.value.chartData
  if (!data.length) return []
  return data.map((value, index) => ({
    x: (index / (data.length - 1)) * 300,
    y: 100 - value * 0.8,
    value: value,
    day: index + 1
  }))
})

const moodChartPoints = computed(() => moodData.value.map(p => `${p.x},${p.y}`).join(' '))

const chartLabels = computed(() => {
  if (timeRange.value === 7) {
    const labels = []
    for (let i = 6; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      labels.push(`${date.getMonth()+1}/${date.getDate()}`)
    }
    return labels
  }
  return ['1号', '8号', '15号', '22号', '30号']
})

const currentMood = computed(() => emotionData.value.currentMood)
const moodSummary = computed(() => emotionData.value.summary)
const moodSummaryColor = computed(() => emotionData.value.summaryColor)
const moodSummaryClass = computed(() => emotionData.value.summaryClass)

// ========== 进度环计算 ==========
const circumference = 2 * Math.PI * 32
const progressOffset = computed(() => circumference - (userProgress.value / 100) * circumference)

// ========== 工具函数 ==========
const getStatusText = (status) => {
  const map = { completed: '已完成', ongoing: '进行中', pending: '待开始' }
  return map[status]
}

// ========== 功能图标组件 ==========
const StarIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>` }
const BookIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path></svg>` }
const GridIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"></rect><rect width="7" height="7" x="14" y="3" rx="1"></rect><rect width="7" height="7" x="14" y="14" rx="1"></rect><rect width="7" height="7" x="3" y="14" rx="1"></rect></svg>` }
const HelpIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><path d="M12 17h.01"></path></svg>` }
const SettingsIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>` }
const LogoutIcon = { props: ['color'], template: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" x2="9" y1="12" y2="12"></line></svg>` }

const functionList = [
  { id: 'favorite', label: '我的收藏', icon: StarIcon, color: '#FFD700', path: PAGE_PATHS.favorite },
  { id: 'diary', label: '情绪日记', icon: BookIcon, color: '#ABD7FB', path: PAGE_PATHS.diary },
  { id: 'square', label: '信息广场', icon: GridIcon, color: '#D2E0AA', path: PAGE_PATHS.square },
  { id: 'help', label: '帮助与反馈', icon: HelpIcon, color: '#999', path: PAGE_PATHS.help },
  { id: 'settings', label: '设置', icon: SettingsIcon, color: '#666', path: PAGE_PATHS.settings },
  { id: 'logout', label: '退出登录', icon: LogoutIcon, color: '#ff4d4f' }
]

// ========== 跳转方法 ==========
const goToEdit = () => uni.navigateTo({ url: PAGE_PATHS.edit })
const goToPath = () => uni.switchTab({ url: PAGE_PATHS.path })
const goToPathDetail = (pathId) => uni.navigateTo({ url: `${PAGE_PATHS.pathDetail}?id=${pathId || currentPathId.value || 1}` })
const goToEmotionDetail = () => uni.navigateTo({ url: PAGE_PATHS.emotionDetail })
const goToDiary = () => uni.navigateTo({ url: PAGE_PATHS.diary })
const goToStepDetail = (stepId) => uni.navigateTo({ url: `${PAGE_PATHS.stepDetail}?id=${stepId}` })

const showMoodDetail = (index) => {
  const day = emotionData.value.recentDays[index]
  if (day && day.moodId) {
    uni.showModal({
      title: `${chartLabels.value[index]}情绪`,
      content: `心情：${day.moodInfo.text}\n${day.text || ''}`,
      showCancel: false,
      confirmText: '知道了'
    })
  } else {
    uni.showToast({ title: '当天无记录', icon: 'none' })
  }
}

const handleFunction = (id) => {
  if (id === 'logout') {
    uni.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          uni.removeStorageSync('token')
          uni.removeStorageSync('userInfo')
          uni.removeStorageSync(PATH_STORAGE_KEY)
          uni.removeStorageSync('needRefreshMinePage')
          uni.reLaunch({ url: PAGE_PATHS.login })
        }
      }
    })
    return
  }
  const func = functionList.find(f => f.id === id)
  if (func && func.path) {
    const tabBarPages = ['square']
    if (tabBarPages.includes(id)) uni.switchTab({ url: func.path })
    else uni.navigateTo({ url: func.path })
  }
}

// ========== 生命周期 ==========
onMounted(() => {
  if (checkLoginStatus()) {
    fetchUserInfo()
    fetchRealMoodData()
	 loadPathProgressFromStorage()
    // 优先从本地加载路径进度，若无则从后端获取
    if (!loadPathProgressFromStorage()) {
      fetchUserCurrentPath()
    }
  }
})

// 页面显示时刷新（监听 onShow）
if (typeof onShow !== 'undefined') {
  onShow(() => {
    const needRefresh = uni.getStorageSync('needRefreshMinePage')
    if (needRefresh) {
      console.log('检测到路径进度更新，刷新我的页面')
      uni.removeStorageSync('needRefreshMinePage')
      loadPathProgressFromStorage()
    } else {
      // 无刷新标志，但为了确保数据最新，也尝试加载一次（可选）
      // 如果不想每次都加载，可以去掉这行
      loadPathProgressFromStorage()
    }
    // 同时刷新用户信息和情绪数据
    if (checkLoginStatus()) {
      fetchUserInfo()
      fetchRealMoodData()
    }
  })
}
</script>
<!-- 模板部分保持不变 -->

<style scoped>
.mine-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #FFFFFF 0%, #FFF8F3 100%);
  padding-bottom: 80px;
}

/* 个人信息大卡片 - 渐变色 */
.profile-card {
  background: linear-gradient(135deg, #FFF9E6, #FFF3D4);
  margin: 20px;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 8px 24px rgba(249, 140, 83, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
}


.profile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(249, 140, 83, 0.12);
}

.profile-content {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid #F98C53;
  object-fit: cover;
}

.edit-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 26px;
  height: 26px;
  background: #F98C53;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.user-detail {
  font-size: 14px;
  color: #666;
  margin: 4px 0;
}

.mood-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #333;
  margin-top: 8px;
}

.progress-section {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.progress-ring-container {
  position: relative;
  width: 80px;
  height: 80px;
}

.progress-ring-fill {
  transition: stroke-dashoffset 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  font-weight: bold;
  color: #F98C53;
}

.progress-label {
  flex: 1;
}

.progress-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.progress-subtitle {
  font-size: 14px;
  color: #999;
  margin-bottom: 4px;
}

.progress-prediction {
  font-size: 12px;
  color: #F98C53;
  background: rgba(249, 140, 83, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
  display: inline-block;
}

/* 数据可视化区 */
.data-section {
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.data-card {
  background: white;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.data-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
}

.mood-card {
  background: linear-gradient(135deg, #E3F2FD 0%, #ffffff 100%);
}

.path-card {
  background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.time-filter {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 6px 12px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn.active {
  background: #ABD7FB;
  color: white;
  border-color: #ABD7FB;
}

/* 感知来源标签 */
.sensor-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.sensor-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #666;
  background: rgba(255, 255, 255, 0.7);
  padding: 4px 10px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.sensor-tag:hover {
  background: white;
}

.sensor-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.sensor-dot.text {
  background: #ABD7FB;
}

.sensor-dot.behavior {
  background: #F98C53;
}

.sensor-dot.fusion {
  background: linear-gradient(135deg, #ABD7FB, #F98C53);
}

.arrow-icon {
  margin-left: 2px;
}

/* 情绪图表 */
.mood-chart {
  margin: 16px 0;
  cursor: pointer;
}

.chart-line {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 8px;
}

.line-chart {
  width: 100%;
  height: 100px;
}

.chart-point {
  cursor: pointer;
  transition: r 0.2s;
}

.chart-point:hover {
  r: 6;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #999;
  padding: 0 20px;
}

.mood-summary {
  font-size: 14px;
  padding: 12px;
  background: #f6ffed;
  border-radius: 8px;
  border: 1px solid #b7eb8f;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mood-summary.warning {
  background: #fff7e6;
  border-color: #ffe58f;
}

.summary-source {
  font-size: 12px;
  color: #999;
  background: rgba(255, 255, 255, 0.7);
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
  width: fit-content;
}

/* 情感适配提示 */
.emotion-fit-tip {
  background: rgba(249, 140, 83, 0.08);
  border-left: 4px solid #F98C53;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.emotion-fit-tip:hover {
  background: rgba(249, 140, 83, 0.12);
}

.fit-icon {
  font-size: 20px;
}

.fit-text {
  flex: 1;
  font-size: 14px;
  color: #333;
}

.fit-badge {
  background: #F98C53;
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.detail-btn {
  display: flex;
  align-items: center;
  background: linear-gradient(90deg, #F98C53, #FFAA6B);
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 30px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 140, 83, 0.3);
}

/* 水平进度条 */
.horizontal-progress {
  margin: 16px 0;
}

.progress-bar-bg {
  height: 12px;
  background: #FFE4D4;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #F98C53 0%, #FFB347 100%);
  border-radius: 6px;
  transition: width 0.5s ease;
}

.progress-info {
  font-size: 12px;
  color: #999;
  text-align: right;
}

/* 步骤列表 */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 16px 0;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px;
  border-radius: 12px;
  transition: background 0.2s;
}

.step-item:hover {
  background: rgba(0, 0, 0, 0.02);
}

.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-icon.completed {
  background: #52c41a;
}

.step-icon.ongoing {
  background: #F98C53;
}

.step-icon.pending {
  background: #d9d9d9;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.step-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.step-status-text {
  font-size: 12px;
}

.step-status-text.completed {
  color: #52c41a;
}

.step-status-text.ongoing {
  color: #F98C53;
}

.step-status-text.pending {
  color: #999;
}

.step-mood-fit {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #F98C53;
  background: rgba(249, 140, 83, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
}

.view-all-tasks {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(249, 140, 83, 0.05);
  border-radius: 12px;
  font-size: 14px;
  color: #F98C53;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-tasks:hover {
  background: rgba(249, 140, 83, 0.1);
}

/* 情绪日记快捷入口 */
.quick-diary {
  margin: 16px 20px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #F98C53, #FFAA6B);
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(249, 140, 83, 0.25);
}

.quick-diary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(249, 140, 83, 0.35);
}

.diary-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.diary-content {
  flex: 1;
}

.diary-title {
  font-size: 18px;
  font-weight: bold;
  color: white;
  margin-bottom: 4px;
}

.diary-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
}

.diary-arrow {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 功能列表区 */
.function-section {
  padding: 0 20px;
  margin-top: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 16px 0;
}

.function-list {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.function-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
}

.function-item:last-child {
  border-bottom: none;
}

.function-item:hover {
  background: #fafafa;
}

.function-item:active {
  transform: scale(0.98);
}

.function-item.logout {
  color: #ff4d4f;
}

.function-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.function-icon {
  width: 22px;
  height: 22px;
}

.function-text {
  font-size: 15px;
  color: #333;
}

.function-item.logout .function-text {
  color: #ff4d4f;
}

.bottom-spacer {
  height: 40px;
}

/* 响应式 */
@media (min-width: 768px) {
  .data-section {
    flex-direction: row;
  }

  .data-card {
    flex: 1;
  }
}

/* 动画效果 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.progress-ring-fill {
  transition: stroke-dashoffset 0.5s ease;
}

/* 自定义滚动条（可选） */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-thumb {
  background: #F98C53;
  border-radius: 4px;
}

::-webkit-scrollbar-track {
  background: #f0f0f0;
}
</style>