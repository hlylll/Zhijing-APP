<template>
  <div class="diary-container">
    <!-- 顶部Tab导航 -->
    <div class="tab-nav">
      <div 
        class="tab-item" 
        :class="{ active: activeTab === 'diary' }"
        @click="switchTab('diary')"
      >
        <div class="tab-icon">📝</div>
        <div class="tab-text">今日日记</div>
      </div>
      <div 
        class="tab-item" 
        :class="{ active: activeTab === 'insight' }"
        @click="switchTab('insight')"
      >
        <div class="tab-icon">📊</div>
        <div class="tab-text">情绪洞察</div>
      </div>
    </div>

    <!-- 今日日记标签页 -->
    <div v-if="activeTab === 'diary'" class="diary-page">
      <!-- 顶部区域 -->
      <div class="diary-header">
        <div class="date-section">
          <div class="current-date">{{ currentDate }}</div>
          <div class="date-greeting">今天心情如何？选个表情记录吧~</div>
        </div>
        <div class="privacy-badge">
          <div class="lock-icon">🔒</div>
          <div class="privacy-text">私密日记</div>
        </div>
      </div>

      <!-- 情绪选择轮盘 -->
      <div class="mood-wheel">
        <div class="wheel-title">选择当前情绪</div>
        <div class="wheel-container">
          <div 
            v-for="mood in moods" 
            :key="mood.id"
            class="mood-item"
            :class="{ selected: selectedMood === mood.id, [mood.type]: true }"
            @click="selectMood(mood.id)"
          >
            <div class="mood-emoji">{{ mood.emoji }}</div>
            <div class="mood-text">{{ mood.text }}</div>
          </div>
        </div>
        <div class="mood-hint" v-if="selectedMoodHint">
          {{ selectedMoodHint }}
        </div>
      </div>

      <!-- 日记输入区域 -->
      <div class="diary-input-section">
        <div class="input-header">
          <div class="input-title">写下今天的经历和感受</div>
          <div class="word-count">{{ diaryText.length }}/500</div>
        </div>
        <textarea
          v-model="diaryText"
          class="diary-textarea"
          placeholder="今天发生了什么呢？有什么想对自己说的？"
          maxlength="500"
          @focus="animateTextarea"
          @input="handleTextInput"
        ></textarea>
        <div class="input-tips">
          <div class="tip-item">💡 记录真实感受有助于情绪分析</div>
          <div class="tip-item">✨ 系统会根据内容提供个性化建议</div>
        </div>
      </div>

      <!-- 匿名树洞开关 -->
      <div class="treehole-section">
        <div class="treehole-header">
          <div class="treehole-title">树洞留言</div>
          <div class="treehole-switch" @click="toggleTreehole">
            <div class="switch-track" :class="{ active: isTreeholeActive }">
              <div class="switch-thumb" :class="{ active: isTreeholeActive }"></div>
            </div>
          </div>
        </div>
        <div class="treehole-desc">
          开启后，你的日记将以匿名形式分享到树洞社区，获得温暖回应
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="submit-section">
        <button 
          class="submit-button" 
          :class="{ saving: isSaving }"
          @click="submitDiary"
          :disabled="isSaving || !diaryText.trim()"
        >
          <div class="button-content">
            <span class="button-icon" v-if="!isSaving">💾</span>
            <div class="loading-spinner" v-if="isSaving"></div>
            <span class="button-text">
              {{ isSaving ? '分析中...' : '保存并分析' }}
            </span>
          </div>
        </button>
        <div class="submit-tip">系统将分析你的情绪并提供成长建议</div>
      </div>
    </div>

    <!-- 情绪洞察标签页 -->
    <div v-if="activeTab === 'insight'" class="insight-page">
      <!-- 日历视图 -->
      <div class="calendar-section">
        <div class="section-header">
          <div class="section-title">
            <div class="title-decoration"></div>
            <h3>心情日历</h3>
          </div>
          <div class="calendar-nav">
            <div class="nav-btn" @click="prevMonth">←</div>
            <div class="current-month">{{ currentMonth }}</div>
            <div class="nav-btn" @click="nextMonth">→</div>
          </div>
        </div>
        
        <div class="calendar-grid">
          <div class="weekday-header" v-for="day in weekdays" :key="day">
            {{ day }}
          </div>
          <div 
            v-for="day in calendarDays"
            :key="day.date"
            class="calendar-day"
            :class="{ 
              today: day.isToday,
              'has-entry': day.hasEntry,
              [day.moodType]: day.moodType
            }"
            @click="selectDate(day)"
          >
            <div class="day-number">{{ day.day }}</div>
            <div class="day-mood" v-if="day.moodEmoji">
              {{ day.moodEmoji }}
            </div>
          </div>
        </div>
        
        <div class="calendar-legend">
          <div class="legend-item">
            <div class="legend-color positive"></div>
            <div class="legend-text">积极</div>
          </div>
          <div class="legend-item">
            <div class="legend-color neutral"></div>
            <div class="legend-text">中性</div>
          </div>
          <div class="legend-item">
            <div class="legend-color negative"></div>
            <div class="legend-text">需关注</div>
          </div>
        </div>
      </div>

      <!-- 心情图表 -->
      <div class="chart-section">
        <div class="section-header">
          <div class="section-title">
            <div class="title-decoration"></div>
            <h3>心情趋势</h3>
          </div>
          <div class="chart-filter">
            <div 
              class="filter-item"
              :class="{ active: chartRange === 'week' }"
              @click="chartRange = 'week'"
            >
              本周
            </div>
            <div 
              class="filter-item"
              :class="{ active: chartRange === 'month' }"
              @click="chartRange = 'month'"
            >
              本月
            </div>
          </div>
        </div>
        
        <!-- 仪表盘图表 -->
        <div class="gauge-chart">
          <div class="gauge-title">平均心情分数</div>
          <div class="gauge-container">
            <div class="gauge-background">
              <div class="gauge-arc"></div>
              <div 
                class="gauge-fill"
                :style="{ transform: `rotate(${averageMoodScore * 1.8 - 90}deg)` }"
              ></div>
              <div class="gauge-pointer"></div>
              <div class="gauge-center"></div>
            </div>
            <div class="gauge-score">
              <div class="score-value">{{ averageMoodScore }}</div>
              <div class="score-label">/100</div>
            </div>
          </div>
          <div class="gauge-labels">
            <div class="label-item">0</div>
            <div class="label-item">50</div>
            <div class="label-item">100</div>
          </div>
          <div class="gauge-status">
            <div class="status-text" :class="getMoodStatus(averageMoodScore).class">
              {{ getMoodStatus(averageMoodScore).text }}
            </div>
          </div>
        </div>
        
        <!-- 柱状图 -->
        <div class="bar-chart">
          <div class="chart-title">情绪分布</div>
          <div class="chart-bars">
            <div 
              v-for="item in moodDistribution"
              :key="item.mood"
              class="bar-item"
            >
              <div class="bar-label">
                <div class="bar-emoji">{{ item.emoji }}</div>
                <div class="bar-text">{{ item.mood }}</div>
              </div>
              <div class="bar-container">
                <div 
                  class="bar-fill"
                  :style="{ width: `${item.percentage}%` }"
                  :class="item.type"
                ></div>
                <div class="bar-value">{{ item.percentage }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 洞察总结 -->
      <div class="insight-section">
        <div class="section-header">
          <div class="section-title">
            <div class="title-decoration"></div>
            <h3>洞察总结</h3>
          </div>
          <div class="insight-update">更新于 {{ lastUpdate }}</div>
        </div>
        
        <div class="insight-cards">
          <div class="insight-card positive">
            <div class="card-icon">😊</div>
            <div class="card-content">
              <div class="card-title">开心天数</div>
              <div class="card-value">{{ positiveDays }} 天</div>
              <div class="card-desc">本月有{{ positiveDays }}天心情积极</div>
            </div>
          </div>
          
          <div class="insight-card warning">
            <div class="card-icon">😔</div>
            <div class="card-content">
              <div class="card-title">压力来源</div>
              <div class="card-value">{{ pressurePercentage }}%</div>
              <div class="card-desc">peer pressure 占比 {{ pressurePercentage }}%</div>
            </div>
          </div>
        </div>
        
        <!-- 趋势预警 -->
        <div class="trend-alert" v-if="showTrendAlert">
          <div class="alert-icon">⚠️</div>
          <div class="alert-content">
            <div class="alert-title">检测到情绪趋势下降</div>
            <div class="alert-desc">最近7天平均分下降15%，建议查看个性化建议</div>
            <button class="alert-button" @click="showRecommendations">
              查看建议
            </button>
          </div>
        </div>
        
        <!-- 个性化建议 -->
        <div class="recommendation-card">
          <div class="rec-icon">💡</div>
          <div class="rec-content">
            <div class="rec-title">数字化导师建议</div>
            <div class="rec-text">
              根据你的情绪模式，建议：
              {{ recommendationText }}
            </div>
            <div class="rec-actions">
              <button class="rec-button primary" @click="viewPathTemplate">
                查看路径模板
              </button>
              <button class="rec-button secondary" @click="viewArticle">
                阅读相关文章
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 日期详情弹窗 -->
    <div class="date-modal" v-if="selectedDate" @click="closeDateModal">
      <div class="modal-overlay"></div>
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <div class="modal-date">{{ selectedDate.date }}</div>
          <div class="modal-close" @click="closeDateModal">×</div>
        </div>
        
        <div class="modal-body">
          <div class="mood-summary">
            <div class="mood-display">
              <div class="mood-emoji-large">{{ selectedDate.moodEmoji }}</div>
              <div class="mood-info">
                <div class="mood-text-large">{{ selectedDate.moodText }}</div>
                <div class="mood-score">心情分数: {{ selectedDate.score }}/100</div>
              </div>
            </div>
          </div>
          
          <div class="diary-preview" v-if="selectedDate.hasEntry">
            <div class="preview-title">当日记录</div>
            <div class="preview-text">{{ selectedDate.diaryPreview }}</div>
            <div class="preview-time">记录于 {{ selectedDate.time }}</div>
          </div>
          
          <div class="analysis-result">
            <div class="analysis-title">情绪分析</div>
            <div class="analysis-text">{{ selectedDate.analysis }}</div>
            <div class="analysis-tags">
              <span 
                v-for="tag in selectedDate.tags"
                :key="tag"
                class="analysis-tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提交成功弹窗 -->
    <div class="success-modal" v-if="showSuccessModal" @click="closeSuccessModal">
      <div class="modal-overlay"></div>
      <div class="modal-content" @click.stop>
        <div class="modal-icon">🎉</div>
        <div class="modal-title">日记已保存</div>
        <div class="modal-subtitle">情绪分析完成</div>
        
        <div class="modal-analysis">
          <div class="analysis-mood">
            <div class="analysis-emoji">{{ selectedMoodEmoji }}</div>
            <div class="analysis-text">{{ selectedMoodText }}</div>
          </div>
          <div class="analysis-score">
            <div class="score-value">{{ analysisScore }}</div>
            <div class="score-label">心情分数</div>
          </div>
        </div>
        
        <div class="modal-insight">
          <div class="insight-title">分析洞察</div>
          <div class="insight-text">{{ analysisInsight }}</div>
        </div>
        
        <div class="modal-recommendation">
          <div class="rec-title">个性化建议</div>
          <div class="rec-text">{{ analysisRecommendation }}</div>
        </div>
        
        <div class="modal-actions">
          <button class="modal-button" @click="closeSuccessModal">好的</button>
          <button class="modal-button primary" @click="viewMoreRecommendations">
            查看更多建议
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

// 当前激活的标签页
const activeTab = ref('diary')

// 切换标签页
const switchTab = (tab) => {
  activeTab.value = tab
}

// 今日日记页面的数据
const currentDate = ref('')
const moods = ref([
  { id: 1, emoji: '😊', text: '开心', type: 'positive', hint: '今天是个好日子！继续保持积极心态～' },
  { id: 2, emoji: '😄', text: '兴奋', type: 'positive', hint: '充满能量的一天！有什么好消息吗？' },
  { id: 3, emoji: '😌', text: '平静', type: 'neutral', hint: '平静的时光也很珍贵，享受当下' },
  { id: 4, emoji: '🤔', text: '思考', type: 'neutral', hint: '思考是成长的开始，有什么新发现？' },
  { id: 5, emoji: '😔', text: '迷茫', type: 'negative', hint: '感到迷茫是正常的，让我们聊聊吧' },
  { id: 6, emoji: '😰', text: '焦虑', type: 'negative', hint: '压力山大了吗？深呼吸，慢慢来' },
  { id: 7, emoji: '😡', text: '压力', type: 'negative', hint: 'peer pressure有点大？分享出来会好些' },
  { id: 8, emoji: '🎃', text: '自定义', type: 'custom', hint: '今天有点特别？写下你的独特感受' }
])

const selectedMood = ref(1)
const selectedMoodHint = ref('')
const diaryText = ref('')
const isTreeholeActive = ref(false)
const isSaving = ref(false)

// 情绪洞察页面的数据
const currentMonth = ref('')
const calendarDays = ref([])
const selectedDate = ref(null)
const chartRange = ref('week')
const averageMoodScore = ref(72)
const moodDistribution = ref([
  { mood: '开心', emoji: '😊', percentage: 40, type: 'positive' },
  { mood: '平静', emoji: '😌', percentage: 25, type: 'neutral' },
  { mood: '思考', emoji: '🤔', percentage: 15, type: 'neutral' },
  { mood: '迷茫', emoji: '😔', percentage: 12, type: 'negative' },
  { mood: '压力', emoji: '😡', percentage: 8, type: 'negative' }
])
const positiveDays = ref(20)
const pressurePercentage = ref(30)
const lastUpdate = ref('')
const showTrendAlert = ref(true)

// 弹窗相关
const showSuccessModal = ref(false)
const analysisScore = ref(0)
const analysisInsight = ref('')
const analysisRecommendation = ref('')

// 星期数组
const weekdays = ['日', '一', '二', '三', '四', '五', '六']

// 计算选中的表情emoji和文本
const selectedMoodEmoji = computed(() => {
  const mood = moods.value.find(m => m.id === selectedMood.value)
  return mood ? mood.emoji : ''
})

const selectedMoodText = computed(() => {
  const mood = moods.value.find(m => m.id === selectedMood.value)
  return mood ? mood.text : ''
})

// 初始化日期
const initDate = () => {
  const now = new Date()
  currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
  currentMonth.value = `${now.getFullYear()}年${now.getMonth() + 1}月`
  lastUpdate.value = `${now.getMonth() + 1}月${now.getDate()}日 ${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`
}

// 生成日历
const generateCalendar = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth()
  
  // 获取当月第一天
  const firstDay = new Date(year, month, 1)
  // 获取当月最后一天
  const lastDay = new Date(year, month + 1, 0)
  // 获取当月天数
  const daysInMonth = lastDay.getDate()
  // 获取第一天是星期几 (0-6, 0代表周日)
  const firstDayOfWeek = firstDay.getDay()
  
  calendarDays.value = []
  
  // 添加上个月的最后几天
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    calendarDays.value.push({
      day: prevMonthLastDay - i,
      date: '',
      isToday: false,
      hasEntry: false,
      moodType: '',
      moodEmoji: ''
    })
  }
  
  // 添加当月日期
  const today = now.getDate()
  for (let i = 1; i <= daysInMonth; i++) {
    const hasEntry = Math.random() > 0.3 // 模拟有记录的日期
    const moodTypes = ['positive', 'neutral', 'negative']
    const moodType = hasEntry ? moodTypes[Math.floor(Math.random() * moodTypes.length)] : ''
    const moodEmojis = { positive: '😊', neutral: '😌', negative: '😔' }
    const moodEmoji = hasEntry ? moodEmojis[moodType] : ''
    
    calendarDays.value.push({
      day: i,
      date: `${year}年${month + 1}月${i}日`,
      isToday: i === today,
      hasEntry: hasEntry,
      moodType: moodType,
      moodEmoji: moodEmoji,
      score: hasEntry ? Math.floor(Math.random() * 40) + 60 : 0,
      moodText: hasEntry ? (moodType === 'positive' ? '开心' : moodType === 'neutral' ? '平静' : '需关注') : '',
      diaryPreview: hasEntry ? '今天过得还不错，完成了一些工作，也抽时间放松了一下。' : '',
      time: hasEntry ? '20:30' : '',
      analysis: hasEntry ? '情绪稳定，工作学习状态良好，建议继续保持当前节奏。' : '',
      tags: hasEntry ? ['工作', '学习', '放松'] : []
    })
  }
  
  // 添加下个月的前几天，使日历完整
  const totalCells = 42 // 6行 * 7列
  const nextMonthDays = totalCells - calendarDays.value.length
  for (let i = 1; i <= nextMonthDays; i++) {
    calendarDays.value.push({
      day: i,
      date: '',
      isToday: false,
      hasEntry: false,
      moodType: '',
      moodEmoji: ''
    })
  }
}

// 选择情绪
const selectMood = (moodId) => {
  selectedMood.value = moodId
  const mood = moods.value.find(m => m.id === moodId)
  selectedMoodHint.value = mood.hint
  
  // 自动填充一些示例文本
  if (!diaryText.value) {
    if (moodId === 7) { // 压力
      diaryText.value = '今天peer pressure有点大，看着同学们都在进步，感觉自己落后了...'
    } else if (moodId === 5) { // 迷茫
      diaryText.value = '对未来感到迷茫，不知道该选择哪条路，考研还是工作...'
    } else if (moodId === 1) { // 开心
      diaryText.value = '今天完成了一个重要的项目，感觉很有成就感！'
    }
  }
}

// 文本输入处理
const handleTextInput = () => {
  // 可以在这里添加实时分析逻辑
}

// 文本区域动画
const animateTextarea = () => {
  // 可以添加动画效果
}

// 切换树洞开关
const toggleTreehole = () => {
  isTreeholeActive.value = !isTreeholeActive.value
}

// 提交日记
const submitDiary = () => {
  if (!diaryText.value.trim()) return
  
  isSaving.value = true
  
  // 模拟API调用
  setTimeout(() => {
    // 分析情绪分数（基于文本和选择的情绪）
    const baseScore = {
      positive: 80,
      neutral: 60,
      negative: 40,
      custom: 50
    }
    
    const moodType = moods.value.find(m => m.id === selectedMood.value).type
    analysisScore.value = baseScore[moodType] + Math.floor(Math.random() * 20) - 10
    
    // 生成分析洞察
    if (analysisScore.value >= 70) {
      analysisInsight.value = '平均心情：Good！检测到积极情绪占主导，继续保持！'
    } else if (analysisScore.value >= 50) {
      analysisInsight.value = '平均心情：平稳。检测到轻度压力，建议适当放松。'
    } else {
      analysisInsight.value = '检测到情绪波动，但这是成长的一部分。推荐阅读情绪管理文章。'
    }
    
    // 生成建议
    if (selectedMood.value === 7) { // 压力
      analysisRecommendation.value = '检测到peer pressure，推荐阅读"如何建立自己的成长节奏"'
    } else if (selectedMood.value === 5) { // 迷茫
      analysisRecommendation.value = '感到迷茫时，建议尝试"职业兴趣探索"路径'
    } else {
      analysisRecommendation.value = '保持当前状态，推荐"高效学习策略"文章'
    }
    
    isSaving.value = false
    showSuccessModal.value = true
    
    // 保存到本地存储
    const diaryEntry = {
      date: new Date().toISOString(),
      mood: selectedMood.value,
      text: diaryText.value,
      isTreehole: isTreeholeActive.value,
      score: analysisScore.value
    }
    
    const diaries = JSON.parse(localStorage.getItem('infog-diaries') || '[]')
    diaries.push(diaryEntry)
    localStorage.setItem('infog-diaries', JSON.stringify(diaries))
    
    // 清空表单
    diaryText.value = ''
    selectedMood.value = 1
    selectedMoodHint.value = ''
    
  }, 1500)
}

// 日历导航
const prevMonth = () => {
  // 实现上个月逻辑
  console.log('上一月')
}

const nextMonth = () => {
  // 实现下个月逻辑
  console.log('下一月')
}

// 选择日期
const selectDate = (day) => {
  if (day.hasEntry) {
    selectedDate.value = day
  }
}

// 关闭日期弹窗
const closeDateModal = () => {
  selectedDate.value = null
}

// 获取心情状态
const getMoodStatus = (score) => {
  if (score >= 70) return { text: '积极', class: 'positive' }
  if (score >= 50) return { text: '平稳', class: 'neutral' }
  return { text: '需关注', class: 'negative' }
}

// 查看建议
const showRecommendations = () => {
  activeTab.value = 'diary'
}

// 查看路径模板
const viewPathTemplate = () => {
  console.log('查看路径模板')
  // 实际项目中应该跳转到相应页面
}

// 查看文章
const viewArticle = () => {
  console.log('阅读文章')
  // 实际项目中应该跳转到相应页面
}

// 推荐文本
const recommendationText = computed(() => {
  if (averageMoodScore.value >= 70) {
    return '继续保持当前节奏，可以尝试挑战更高难度的学习目标。'
  } else if (averageMoodScore.value >= 50) {
    return '适当调整学习计划，增加休息时间，避免过度疲劳。'
  } else {
    return '考虑调整成长路径，减少压力源，寻找适合自己的节奏。'
  }
})

// 查看更多建议
const viewMoreRecommendations = () => {
  console.log('查看更多建议')
  showSuccessModal.value = false
  // 实际项目中可以跳转到建议页面
}

// 关闭成功弹窗
const closeSuccessModal = () => {
  showSuccessModal.value = false
}

// 组件挂载时初始化
onMounted(() => {
  initDate()
  generateCalendar()
})
</script>

<style scoped>
.diary-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #F8F9FA 0%, #FFF8F3 100%);
  padding-top: 20rpx;
  padding-bottom: 40rpx;
}

/* Tab导航样式 */
.tab-nav {
  display: flex;
  background: white;
  border-radius: 50rpx;
  margin: 0 32rpx 32rpx;
  padding: 8rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 0;
  border-radius: 40rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-item.active {
  background: linear-gradient(135deg, #D2E0AA, #E8F5E8);
  transform: translateY(-2rpx);
  box-shadow: 0 4rpx 16rpx rgba(210, 224, 170, 0.3);
}

.tab-icon {
  font-size: 40rpx;
  margin-bottom: 8rpx;
}

.tab-text {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
}

.tab-item.active .tab-text {
  color: #4CAF50;
}

/* 今日日记页面样式 */
.diary-page {
  padding: 0 32rpx;
}

.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40rpx;
}

.date-section {
  flex: 1;
}

.current-date {
  font-size: 44rpx;
  font-weight: 800;
  color: #333333;
  margin-bottom: 12rpx;
}

.date-greeting {
  font-size: 32rpx;
  color: #666666;
  opacity: 0.9;
}

.privacy-badge {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 20rpx;
  background: rgba(171, 215, 251, 0.2);
  border-radius: 25rpx;
}

.lock-icon {
  font-size: 24rpx;
}

.privacy-text {
  font-size: 24rpx;
  color: #2196F3;
  font-weight: 500;
}

/* 情绪选择轮盘 */
.mood-wheel {
  background: white;
  border-radius: 32rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.wheel-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 32rpx;
  text-align: center;
}

.wheel-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24rpx;
}

.mood-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 20rpx;
  border-radius: 24rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #F8F9FA;
  border: 2rpx solid transparent;
}

.mood-item:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
}

.mood-item.selected {
  transform: translateY(-6rpx);
  box-shadow: 0 12rpx 32rpx rgba(0, 0, 0, 0.12);
}

.mood-item.positive.selected {
  background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
  border-color: #4CAF50;
}

.mood-item.neutral.selected {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
  border-color: #FF9800;
}

.mood-item.negative.selected {
  background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
  border-color: #F44336;
}

.mood-item.custom.selected {
  background: linear-gradient(135deg, #F3E5F5, #E1BEE7);
  border-color: #9C27B0;
}

.mood-emoji {
  font-size: 48rpx;
  margin-bottom: 16rpx;
}

.mood-text {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
}

.mood-hint {
  margin-top: 32rpx;
  padding: 24rpx;
  background: linear-gradient(135deg, #FFF8F3, #FFE8D6);
  border-radius: 20rpx;
  font-size: 28rpx;
  color: #F98C53;
  text-align: center;
  font-weight: 500;
}

/* 日记输入区域 */
.diary-input-section {
  background: white;
  border-radius: 32rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.input-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
}

.word-count {
  font-size: 28rpx;
  color: #999999;
}

.diary-textarea {
  width: 87%;
  min-height: 300rpx;
  padding: 32rpx;
  font-size: 32rpx;
  color: #333333;
  border: 2rpx solid #E0E0E0;
  border-radius: 24rpx;
  outline: none;
  background: #F8F9FA;
  resize: vertical;
  transition: all 0.3s ease;
  line-height: 1.6;
}

.diary-textarea:focus {
  border-color: #F98C53;
  background: white;
  box-shadow: 0 0 0 4rpx rgba(249, 140, 83, 0.1);
}

.diary-textarea::placeholder {
  color: #999999;
}

.input-tips {
  margin-top: 24rpx;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.tip-item {
  font-size: 26rpx;
  color: #666666;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

/* 树洞开关 */
.treehole-section {
  background: white;
  border-radius: 32rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.treehole-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.treehole-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
}

.treehole-switch {
  cursor: pointer;
}

.switch-track {
  width: 80rpx;
  height: 40rpx;
  background: #E0E0E0;
  border-radius: 20rpx;
  position: relative;
  transition: background-color 0.3s ease;
}

.switch-track.active {
  background: #4CAF50;
}

.switch-thumb {
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  width: 32rpx;
  height: 32rpx;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
}

.switch-thumb.active {
  transform: translateX(40rpx);
}

.treehole-desc {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.5;
}

/* 提交按钮 */
.submit-section {
  margin-top: 48rpx;
}

.submit-button {
  width: 100%;
  padding: 36rpx;
  background: linear-gradient(to right, #F98C53, #FFAA6B);
  color: white;
  font-size: 36rpx;
  font-weight: 700;
  border: none;
  border-radius: 50rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.3);
}

.submit-button:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 12rpx 40rpx rgba(249, 140, 83, 0.4);
}

.submit-button:disabled {
  background: #CCCCCC;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.submit-button.saving {
  opacity: 0.8;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.button-icon {
  font-size: 40rpx;
}

.loading-spinner {
  width: 40rpx;
  height: 40rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.3);
  border-top: 4rpx solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.submit-tip {
  text-align: center;
  font-size: 26rpx;
  color: #666666;
  margin-top: 20rpx;
  opacity: 0.8;
}

/* 情绪洞察页面样式 */
.insight-page {
  padding: 0 32rpx;
}

/* 通用部分样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.title-decoration {
  width: 6rpx;
  height: 36rpx;
  background: #F98C53;
  border-radius: 3rpx;
}

.section-title h3 {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
  margin: 0;
}

/* 日历部分 */
.calendar-section {
  background: white;
  border-radius: 32rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.calendar-nav {
  display: flex;
  align-items: center;
  gap: 32rpx;
}

.nav-btn {
  font-size: 32rpx;
  color: #666666;
  cursor: pointer;
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  transition: background-color 0.3s ease;
}

.nav-btn:hover {
  background-color: #F5F5F5;
}

.current-month {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  min-width: 200rpx;
  text-align: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8rpx;
  margin-bottom: 32rpx;
}

.weekday-header {
  text-align: center;
  font-size: 28rpx;
  color: #666666;
  font-weight: 500;
  padding: 16rpx 0;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  background: #F8F9FA;
}

.calendar-day:hover {
  background: #F0F0F0;
}

.calendar-day.today {
  border: 2rpx solid #F98C53;
}

.calendar-day.has-entry {
  cursor: pointer;
}

.calendar-day.positive {
  background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
}

.calendar-day.neutral {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
}

.calendar-day.negative {
  background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
}

.day-number {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 4rpx;
}

.day-mood {
  font-size: 24rpx;
}

.calendar-legend {
  display: flex;
  justify-content: center;
  gap: 32rpx;
  margin-top: 24rpx;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.legend-color {
  width: 24rpx;
  height: 24rpx;
  border-radius: 6rpx;
}

.legend-color.positive {
  background: #C8E6C9;
}

.legend-color.neutral {
  background: #FFE0B2;
}

.legend-color.negative {
  background: #FFCDD2;
}

.legend-text {
  font-size: 24rpx;
  color: #666666;
}

/* 图表部分 */
.chart-section {
  background: white;
  border-radius: 32rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.chart-filter {
  display: flex;
  gap: 16rpx;
}

.filter-item {
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 28rpx;
  color: #666666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-item.active {
  background: #F98C53;
  color: white;
  font-weight: 600;
}

/* 仪表盘图表 */
.gauge-chart {
  background: #F8F9FA;
  border-radius: 24rpx;
  padding: 40rpx;
  margin: 32rpx 0;
  text-align: center;
}

.gauge-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 32rpx;
}

.gauge-container {
  position: relative;
  width: 300rpx;
  height: 150rpx;
  margin: 0 auto 48rpx;
}

.gauge-background {
  position: relative;
  width: 100%;
  height: 100%;
}

.gauge-arc {
  position: absolute;
  top: 0;
  left: 0;
  width: 300rpx;
  height: 150rpx;
  border: 20rpx solid #E0E0E0;
  border-top-left-radius: 300rpx;
  border-top-right-radius: 300rpx;
  border-bottom: 0;
  box-sizing: border-box;
}

.gauge-fill {
  position: absolute;
  top: 0;
  left: 0;
  width: 300rpx;
  height: 150rpx;
  border: 20rpx solid #F98C53;
  border-top-left-radius: 300rpx;
  border-top-right-radius: 300rpx;
  border-bottom: 0;
  box-sizing: border-box;
  transform-origin: 50% 100%;
  transition: transform 1s ease;
}

.gauge-pointer {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 4rpx;
  height: 80rpx;
  background: #333333;
  transform-origin: 50% 100%;
  transform: translateX(-50%);
}

.gauge-center {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 20rpx;
  height: 20rpx;
  background: #333333;
  border-radius: 50%;
  transform: translate(-50%, 50%);
}

.gauge-score {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-value {
  font-size: 60rpx;
  font-weight: 800;
  color: #333333;
  line-height: 1;
}

.score-label {
  font-size: 24rpx;
  color: #666666;
  margin-top: 4rpx;
}

.gauge-labels {
  display: flex;
  justify-content: space-between;
  margin-top: -20rpx;
  padding: 0 20rpx;
}

.label-item {
  font-size: 24rpx;
  color: #666666;
}

.gauge-status {
  margin-top: 24rpx;
}

.status-text {
  display: inline-block;
  padding: 12rpx 32rpx;
  border-radius: 25rpx;
  font-size: 28rpx;
  font-weight: 600;
}

.status-text.positive {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-text.neutral {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.status-text.negative {
  background: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

/* 柱状图 */
.bar-chart {
  margin-top: 48rpx;
}

.chart-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 32rpx;
}

.chart-bars {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.bar-label {
  display: flex;
  align-items: center;
  gap: 12rpx;
  width: 120rpx;
}

.bar-emoji {
  font-size: 32rpx;
}

.bar-text {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
}

.bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.bar-fill {
  height: 32rpx;
  border-radius: 16rpx;
  transition: width 1s ease;
}

.bar-fill.positive {
  background: linear-gradient(to right, #C8E6C9, #4CAF50);
}

.bar-fill.neutral {
  background: linear-gradient(to right, #FFE0B2, #FF9800);
}

.bar-fill.negative {
  background: linear-gradient(to right, #FFCDD2, #F44336);
}

.bar-value {
  font-size: 28rpx;
  color: #333333;
  font-weight: 600;
  min-width: 80rpx;
  text-align: right;
}

/* 洞察总结部分 */
.insight-section {
  background: white;
  border-radius: 32rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
}

.insight-update {
  font-size: 26rpx;
  color: #999999;
}

.insight-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
  margin: 32rpx 0;
}

.insight-card {
  background: #F8F9FA;
  border-radius: 24rpx;
  padding: 32rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.insight-card.positive {
  background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
}

.insight-card.warning {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
}

.card-icon {
  font-size: 48rpx;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 28rpx;
  color: #666666;
  margin-bottom: 8rpx;
}

.card-value {
  font-size: 40rpx;
  font-weight: 800;
  color: #333333;
  margin-bottom: 4rpx;
}

.card-desc {
  font-size: 24rpx;
  color: #999999;
}

/* 趋势预警 */
.trend-alert {
  background: linear-gradient(135deg, #FFF3E0, #FFECB3);
  border-radius: 24rpx;
  padding: 32rpx;
  margin: 32rpx 0;
  display: flex;
  align-items: flex-start;
  gap: 24rpx;
  border-left: 8rpx solid #FF9800;
}

.alert-icon {
  font-size: 48rpx;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 12rpx;
}

.alert-desc {
  font-size: 28rpx;
  color: #666666;
  margin-bottom: 24rpx;
  line-height: 1.5;
}

.alert-button {
  padding: 16rpx 32rpx;
  background: #FF9800;
  color: white;
  font-size: 28rpx;
  font-weight: 600;
  border: none;
  border-radius: 25rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.alert-button:hover {
  background: #F57C00;
  transform: translateY(-2rpx);
}

/* 个性化建议 */
.recommendation-card {
  background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-top: 32rpx;
  display: flex;
  align-items: flex-start;
  gap: 24rpx;
}

.rec-icon {
  font-size: 48rpx;
  flex-shrink: 0;
}

.rec-content {
  flex: 1;
}

.rec-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 16rpx;
}

.rec-text {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 24rpx;
}

.rec-actions {
  display: flex;
  gap: 16rpx;
}

.rec-button {
  padding: 16rpx 32rpx;
  font-size: 28rpx;
  font-weight: 600;
  border: none;
  border-radius: 25rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.rec-button.primary {
  margin-left: -40rpx;
  height: 100rpx;
  width: 250rpx;
  background: #2196F3;
  color: white;
}

.rec-button.primary:hover {
  background: #1976D2;
  transform: translateY(-2rpx);
}

.rec-button.secondary {
	height: 100rpx;
	width: 250rpx;
  background: white;
  color: #2196F3;
  border: 2rpx solid #2196F3;
}

.rec-button.secondary:hover {
  background: #E3F2FD;
}

/* 弹窗样式 */
.date-modal,
.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 600rpx;
  max-height: 80vh;
  overflow-y: auto;
  background: white;
  border-radius: 40rpx;
  padding: 48rpx;
  z-index: 10000;
  box-shadow: 0 20rpx 80rpx rgba(0, 0, 0, 0.2);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(40rpx) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.modal-date {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
}

.modal-close {
  font-size: 40rpx;
  color: #999999;
  cursor: pointer;
  padding: 8rpx 16rpx;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.modal-close:hover {
  background-color: #F5F5F5;
}

.mood-summary {
  background: #F8F9FA;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
}

.mood-display {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.mood-emoji-large {
  font-size: 60rpx;
}

.mood-info {
  flex: 1;
}

.mood-text-large {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 8rpx;
}

.mood-score {
  font-size: 28rpx;
  color: #666666;
}

.diary-preview {
  background: #FFF8F3;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
}

.preview-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16rpx;
}

.preview-text {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.preview-time {
  font-size: 24rpx;
  color: #999999;
  text-align: right;
}

.analysis-result {
  background: #F0F7FF;
  border-radius: 24rpx;
  padding: 32rpx;
}

.analysis-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16rpx;
}

.analysis-text {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 24rpx;
}

.analysis-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.analysis-tag {
  padding: 8rpx 16rpx;
  background: white;
  color: #2196F3;
  font-size: 24rpx;
  border-radius: 20rpx;
  border: 1rpx solid #2196F3;
}

/* 成功弹窗 */
.modal-icon {
  font-size: 80rpx;
  text-align: center;
  margin-bottom: 24rpx;
}

.modal-title {
  font-size: 40rpx;
  font-weight: 800;
  color: #333333;
  text-align: center;
  margin-bottom: 8rpx;
}

.modal-subtitle {
  font-size: 32rpx;
  color: #666666;
  text-align: center;
  margin-bottom: 40rpx;
}

.modal-analysis {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F8F9FA;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
}

.analysis-mood {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.analysis-emoji {
  font-size: 60rpx;
}

.analysis-text {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
}

.analysis-score {
  text-align: center;
}

.score-value {
  font-size: 48rpx;
  font-weight: 800;
  color: #F98C53;
  line-height: 1;
}

.score-label {
  font-size: 24rpx;
  color: #999999;
  margin-top: 4rpx;
}

.modal-insight {
  background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
}

.insight-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 12rpx;
}

.insight-text {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.5;
}

.modal-recommendation {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 40rpx;
}

.rec-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 12rpx;
}

.rec-text {
  font-size: 28rpx;
  color: #666666;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 24rpx;
}

.modal-button {
  flex: 1;
  padding: 24rpx;
  font-size: 32rpx;
  font-weight: 600;
  border: none;
  border-radius: 25rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-button {
  background: #F5F5F5;
  color: #666666;
}

.modal-button:hover {
  background: #E0E0E0;
}

.modal-button.primary {
  background: #F98C53;
  color: white;
}

.modal-button.primary:hover {
  background: #FF7C3A;
  transform: translateY(-2rpx);
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .calendar-grid {
    gap: 4rpx;
  }
  
  .wheel-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .insight-cards {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    padding: 40rpx 32rpx;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>