<template>
  <view class="page-container">
    <!-- 魔法星星背景 -->
    <view class="stars-container">
      <view 
        v-for="(star, index) in stars" 
        :key="index"
        class="star"
        :style="{
          left: star.left + 'px',
          top: star.top + 'px',
          width: star.size + 'px',
          height: star.size + 'px',
          opacity: star.opacity,
          animationDelay: star.delay + 's',
          animationDuration: star.duration + 's'
        }"
      ></view>
    </view>

    <!-- 主内容区 -->
    <view class="main-content">
      <!-- 头部区域 -->
      <view class="header" :style="{ paddingTop: statusBarHeight + 'px' }">
        <view class="streak-card">
          <view class="streak-icon">🔥</view>
          <view class="streak-content">
            <text class="streak-number" :style="{ backgroundImage: streakGradient }">{{ streakDays }}</text>
            <text class="streak-label">天连续浇灌</text>
          </view>
        </view>
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
      </view>

      <!-- 标题区域 -->
      <view class="title-section">
        <text class="main-title">情绪魔法花园</text>
        <text class="sub-title">记录此刻，种下心愿</text>
        <view class="stats-cards">
          <view class="stat-card">
            <text class="stat-number">{{ currentMonthRecords }}</text>
            <text class="stat-label">本月花朵</text>
          </view>
          <view class="stat-card highlight">
            <text class="stat-number">{{ totalFlowers }}</text>
            <text class="stat-label">总共花朵</text>
          </view>
          <view class="stat-card">
            <text class="stat-number">{{ gardenLevel }}</text>
            <text class="stat-label">花园等级</text>
          </view>
        </view>
      </view>

      <!-- 月份切换 -->
      <view class="month-switcher">
        <view class="month-btn" @click="prevMonth">
          <text class="btn-icon">←</text>
        </view>
        <view class="month-display">
          <text class="current-month">{{ currentYear }}年 {{ currentMonth + 1 }}月</text>
          <text class="month-summary">收集了 {{ currentMonthRecords }} 朵情绪花</text>
        </view>
        <view class="month-btn" @click="nextMonth">
          <text class="btn-icon">→</text>
        </view>
      </view>

      <!-- 日历网格 -->
      <view class="calendar-container">
        <!-- 星期栏 -->
        <view class="weekdays">
          <text 
            v-for="day in weekdays" 
            :key="day"
            class="weekday"
            :class="{ weekend: day === '六' || day === '日' }"
          >
            {{ day }}
          </text>
        </view>
        
        <!-- 日期网格 -->
        <view class="days-grid">
          <view 
            v-for="(day, index) in calendarDays" 
            :key="index"
            class="day-cell"
            @click="day.hasRecord && showDetail(day)"
            :class="{
              'empty-day': !day.hasRecord,
              'today': day.isToday,
              'has-record': day.hasRecord
            }"
          >
            <!-- 有记录的日子 -->
            <view v-if="day.hasRecord" class="flower-container">
              <!-- 花朵右上角的日期数字 -->
              <text class="flower-date" :class="{ 'today-date': day.isToday }">
                {{ getDayNumber(day) }}
              </text>
              
              <!-- 花朵emoji -->
              <view 
                class="flower-emoji"
                :style="{
                  background: getFlowerGradient(day.score),
                  boxShadow: getFlowerGlow(day.score)
                }"
              >
                {{ day.emoji }}
              </view>
              
              <!-- 花名 -->
              <text class="flower-badge" :style="{ color: getMoodColor(day.score) }">
                {{ day.moodLabel }}
              </text>
            </view>
            
            <!-- 无记录的日子 -->
            <view v-else class="empty-day-container">
              <view class="empty-indicator">
                <view class="dot"></view>
              </view>
              <text class="day-number" :class="{ 'today-number': day.isToday }">
                {{ day.date }}
              </text>
            </view>
          </view>
        </view>
      </view>
    
      <!-- 月度总结卡片 -->
      <view class="summary-card">
        <view class="summary-header">
          <text class="summary-icon">🌱</text>
          <text class="summary-title">本月花园总结</text>
        </view>
        <text class="summary-text">{{ monthlySummary }}</text>
        
        <!-- 情绪分布小统计 -->
        <view class="mood-distribution" v-if="moodDistribution.length > 0">
          <view 
            v-for="(mood, index) in moodDistribution" 
            :key="index"
            class="mood-tag"
            :style="{ background: mood.color + '20' }"
          >
            <text class="mood-emoji">{{ mood.emoji }}</text>
            <text class="mood-count">{{ mood.count }}</text>
          </view>
        </view>
        
        <text class="summary-tip">继续记录，让花园越来越梦幻哦～ ✨</text>
      </view>
    </view>

    <!-- 日记详情弹窗 -->
    <view class="modal-overlay" v-if="showModal" @click="closeModal">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-date">{{ selectedDate }}</text>
          <view 
            class="modal-emoji"
            :style="{
              background: getFlowerGradient(selectedDay.score),
              boxShadow: getFlowerGlow(selectedDay.score)
            }"
          >
            {{ selectedDay.emoji }}
          </view>
          <view class="modal-close" @click="closeModal">×</view>
        </view>
        
        <scroll-view class="modal-body" scroll-y>
          <text class="modal-diary">{{ selectedDay.diary }}</text>
          
          <view class="modal-meta">
            <text class="meta-label">心情花朵：{{ selectedDay.moodLabel }}</text>
            <text class="meta-label">种植时间：{{ selectedDay.plantTime || selectedDate }}</text>
          </view>
          
          <view class="mood-energy">
            <text class="energy-label">心情能量值</text>
            <view class="energy-bar">
              <view 
                class="energy-fill"
                :style="{
                  width: selectedDay.score * 10 + '%',
                  background: getEnergyGradient(selectedDay.score)
                }"
              ></view>
            </view>
            <text class="energy-value">{{ selectedDay.score * 10 }}%</text>
          </view>
        </scroll-view>
        
        <view class="modal-footer">
          <view class="modal-btn" @click="closeModal">
            <text class="btn-text">回到花园 🌸</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 状态栏高度
      statusBarHeight: 44,
      
      // 魔法星星
      stars: [],
      
      // 花园数据
      gardenData: null,
      flowers: [],
      stats: {
        total: 0,
        byMood: {},
        byMonth: {}
      },
      growthLevel: 1,
      flowerStyles: {},
      
      // 当前月份
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth(),
      
      // 星期显示
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],
      
      // 日历数据
      calendarDays: [],
      
      // 弹窗相关
      showModal: false,
      selectedDay: {},
      
      // 用户ID
      userId: 'test_user'
    }
  },
  
  computed: {
    // 连续记录渐变背景
    streakGradient() {
      return 'linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 50%, #FAD0C4 100%)'
    },
    
    // 连续记录天数
    streakDays() {
      return this.gardenData?.streakDays || 0
    },
    
    // 总花朵数
    totalFlowers() {
      return this.stats.total || 0
    },
    
    // 花园等级
    gardenLevel() {
      return this.growthLevel || 1
    },
    
    // 当前月份记录数
    currentMonthRecords() {
      const monthStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}`
      return this.stats.byMonth?.[monthStr] || 0
    },
    
    // 情绪分布（用于月度总结）
    moodDistribution() {
      const distribution = []
      const monthStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}`
      const monthFlowers = this.flowers.filter(f => 
        f.date && f.date.startsWith(monthStr)
      )
      
      const countByMood = {}
      monthFlowers.forEach(f => {
        const moodId = f.moodId
        countByMood[moodId] = (countByMood[moodId] || 0) + 1
      })
      
      Object.keys(countByMood).forEach(moodId => {
        const style = this.flowerStyles[moodId] || { emoji: '🌸', color: '#9370DB', name: '心情花' }
        distribution.push({
          moodId,
          emoji: style.emoji,
          name: style.name,
          count: countByMood[moodId],
          color: style.color
        })
      })
      
      return distribution.sort((a, b) => b.count - a.count)
    },
    
    // 月度总结文案
    monthlySummary() {
      const monthFlowers = this.flowers.filter(f => 
        f.date && f.date.startsWith(`${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}`)
      )
      
      if (monthFlowers.length === 0) {
        return '本月还没有种下花朵，开始记录心情吧～'
      }
      
      const avgScore = this.calculateAverageScore(monthFlowers)
      const mostMood = this.moodDistribution[0]
      
      if (avgScore >= 8) {
        return `本月的花园阳光明媚，充满了快乐的能量！你最喜欢种下${mostMood?.emoji}${mostMood?.name}，你的积极心情像阳光一样温暖了整个花园。`
      } else if (avgScore >= 6) {
        return `本月的花园有晴有雨，但总体平和美好。你最喜欢种下${mostMood?.emoji}${mostMood?.name}，每一种情绪都是花园里独特的花朵。`
      } else {
        return `本月的花园经历了一些风雨，但每一朵花都在努力生长。你最喜欢种下${mostMood?.emoji}${mostMood?.name}，继续浇灌，春天总会到来。`
      }
    },
    
    // 弹窗显示的日期
    selectedDate() {
      if (this.selectedDay.fullDate) {
        const date = new Date(this.selectedDay.fullDate)
        return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
      }
      return ''
    }
  },
  
  onLoad(options) {
    // 获取状态栏高度
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight
    } catch (e) {
      console.error('获取状态栏高度失败', e)
    }
    
    // 获取用户ID
    try {
      const userInfo = uni.getStorageSync('user')
      if (userInfo) {
        this.userId = userInfo.id || userInfo.phone || 'test_user'
      }
    } catch (e) {
      console.error('获取用户ID失败', e)
    }
    
    // 生成魔法星星
    this.generateStars()
    
    // 初始化花朵样式（保持原样）
    this.flowerStyles = {
      1: { name: '向日葵', emoji: '🌻', color: '#FFD93D', type: 'happy' },
      2: { name: '云朵花', emoji: '☁️', color: '#B5B9FF', type: 'peaceful' },
      3: { name: '星星花', emoji: '✨', color: '#FFE55C', type: 'thoughtful' },
      4: { name: '雨滴花', emoji: '💧', color: '#6BCB77', type: 'sad' },
      5: { name: '彩虹花', emoji: '🌈', color: '#FF6B6B', type: 'excited' },
      6: { name: '拼图花', emoji: '🧩', color: '#845EC2', type: 'confused' }
    }
    
    // 加载花园数据
    this.loadGardenData()
  },
  
  methods: {
    // 加载花园数据
    async loadGardenData() {
      // 优先从数据库加载
      const success = await this.loadFromDatabase()
      
      // 如果数据库加载失败，从本地加载
      if (!success) {
        this.loadFromLocal()
      }
      
      // 生成日历
      this.generateCalendar()
      
      console.log('当前花朵数据:', this.flowers)
      console.log('当前月份记录数:', this.currentMonthRecords)
    },
    
    // 从数据库加载
    async loadFromDatabase() {
      try {
        const year = this.currentYear
        const month = this.currentMonth + 1
        
        const response = await fetch(
          `http://localhost:8000/api/garden-data/${this.userId}?year=${year}&month=${month}`
        )
        const result = await response.json()
        
        if (result.success && result.flowers) {
          console.log('从数据库加载成功')
          
          // 转换为花园需要的格式（保持原有的数据结构）
          this.flowers = result.flowers.map(f => ({
            date: f.date,
            text: f.text || '心情记录',
            moodId: f.moodId,
            growth: f.growth || 0.7,
            flowerStyle: this.flowerStyles[f.moodId] || {
              emoji: '🌸',
              name: '心情花',
              color: '#9370DB'
            }
          }))
          
          this.stats = result.stats || { total: 0, byMood: {}, byMonth: {} }
          this.growthLevel = result.growthLevel || 1
          this.gardenData = { streakDays: result.streakDays || 0 }
          
          return true
        }
        return false
      } catch (error) {
        console.error('从数据库加载失败:', error)
        return false
      }
    },
    
    // 从本地加载（保持原有的加载方式）
    loadFromLocal() {
      try {
        // 读取日记数据
        const diaries = uni.getStorageSync('infog-mood-diaries')
        console.log('从本地加载日记数据')
        
        if (diaries) {
          const diaryList = JSON.parse(diaries)
          
          // 转换为花朵格式（保持原有的转换逻辑）
          this.flowers = diaryList.map(diary => {
            const moodId = diary.predicted_mood || diary.manual_mood || diary.mood
            
            return {
              date: diary.date,
              text: diary.text || diary.diary_text || '心情记录',
              moodId: moodId,
              growth: 0.7 + Math.random() * 0.3,
              flowerStyle: this.flowerStyles[moodId] || { 
                emoji: '🌸', 
                name: '心情花',
                color: '#9370DB'
              }
            }
          }).filter(flower => flower.moodId)
          
          // 更新统计
          this.stats.total = this.flowers.length
          this.stats.byMood = {}
          this.stats.byMonth = {}
          
          this.flowers.forEach(flower => {
            const moodId = flower.moodId
            this.stats.byMood[moodId] = (this.stats.byMood[moodId] || 0) + 1
            
            if (flower.date) {
              const month = flower.date.substring(0, 7)
              this.stats.byMonth[month] = (this.stats.byMonth[month] || 0) + 1
            }
          })
          
          this.growthLevel = Math.floor(this.stats.total / 10) + 1
          this.gardenData = {
            streakDays: this.calculateStreak(diaryList)
          }
        }
      } catch (e) {
        console.error('从本地加载失败', e)
      }
    },
    
    // 计算连续天数（保持原样）
    calculateStreak(diaries) {
      if (!diaries || diaries.length === 0) return 0
      
      const sorted = [...diaries].sort((a, b) => 
        new Date(b.date) - new Date(a.date)
      )
      
      let streak = 1
      const oneDay = 24 * 60 * 60 * 1000
      
      for (let i = 0; i < sorted.length - 1; i++) {
        const current = new Date(sorted[i].date).setHours(0, 0, 0, 0)
        const next = new Date(sorted[i + 1].date).setHours(0, 0, 0, 0)
        
        if (current - next === oneDay) {
          streak++
        } else {
          break
        }
      }
      
      return streak
    },
    
    // 生成魔法星星（保持原样）
    generateStars() {
      const stars = []
      const starCount = 20
      
      for (let i = 0; i < starCount; i++) {
        stars.push({
          left: Math.random() * 100,
          top: -Math.random() * 100,
          size: 2 + Math.random() * 4,
          opacity: 0.3 + Math.random() * 0.7,
          delay: Math.random() * 5,
          duration: 10 + Math.random() * 20
        })
      }
      
      this.stars = stars
    },
    
    // 生成日历（保持原有的渲染逻辑）
    generateCalendar() {
      const year = this.currentYear
      const month = this.currentMonth
      const today = new Date()
      
      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)
      const firstDayWeekday = firstDay.getDay()
      const daysInMonth = lastDay.getDate()
      
      const calendarDays = []
      
      for (let i = 0; i < firstDayWeekday; i++) {
        calendarDays.push({
          date: '',
          hasRecord: false,
          isToday: false
        })
      }
      
      for (let i = 1; i <= daysInMonth; i++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
        const isToday = 
          today.getFullYear() === year &&
          today.getMonth() === month &&
          today.getDate() === i
        
        const flowerEntry = this.flowers.find(item => item.date && item.date.startsWith(dateStr))
        
        if (flowerEntry) {
          const style = this.flowerStyles[flowerEntry.moodId] || { 
            emoji: '🌸', 
            name: '心情花',
            color: '#9370DB'
          }
          
          calendarDays.push({
            date: i,
            fullDate: dateStr,
            hasRecord: true,
            isToday,
            emoji: flowerEntry.flowerStyle?.emoji || style.emoji,
            score: Math.floor(flowerEntry.growth * 10) || 7,
            moodLabel: flowerEntry.flowerStyle?.name || style.name,
            diary: flowerEntry.text || '今天的心情记录',
            moodId: flowerEntry.moodId,
            plantTime: this.formatDate(flowerEntry.date)
          })
        } else {
          calendarDays.push({
            date: i,
            fullDate: dateStr,
            hasRecord: false,
            isToday
          })
        }
      }
      
      this.calendarDays = calendarDays
    },
    
    // 以下所有方法都保持原样，不做任何修改
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
    },
    
    getDayNumber(day) {
      if (typeof day.date === 'string') {
        const match = day.date.match(/\d{4}-\d{2}-(\d{2})/)
        return match ? parseInt(match[1], 10) : day.date
      }
      return day.date
    },
    
    calculateAverageScore(flowers) {
      if (flowers.length === 0) return 0
      
      const totalScore = flowers.reduce((sum, flower) => {
        return sum + (flower.growth * 10 || 5)
      }, 0)
      return totalScore / flowers.length
    },
    
    getFlowerGradient(score) {
      if (score >= 9) {
        return 'linear-gradient(135deg, #FFD700 0%, #FF8C00 50%, #FF1493 100%)'
      } else if (score >= 7) {
        return 'linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 50%, #A18CD1 100%)'
      } else if (score >= 5) {
        return 'linear-gradient(135deg, #A1C4FD 0%, #C2E9FB 50%, #D4FC79 100%)'
      } else {
        return 'linear-gradient(135deg, #89F7FE 0%, #66A6FF 50%, #8EC5FC 100%)'
      }
    },
    
    getFlowerGlow(score) {
      const intensity = score * 1.5
      const spread = score * 1.2
      const color = score >= 9 ? 'rgba(255, 215, 0, 0.4)' :
                   score >= 7 ? 'rgba(255, 182, 193, 0.3)' :
                   score >= 5 ? 'rgba(173, 216, 230, 0.25)' :
                   'rgba(135, 206, 250, 0.2)'
      
      return `0 0 ${spread}px ${intensity}px ${color}`
    },
    
    getEnergyGradient(score) {
      if (score >= 9) {
        return 'linear-gradient(90deg, #FF9A9E 0%, #FECFEF 50%, #FAD0C4 100%)'
      } else if (score >= 7) {
        return 'linear-gradient(90deg, #A1C4FD 0%, #C2E9FB 50%, #D4FC79 100%)'
      } else if (score >= 5) {
        return 'linear-gradient(90deg, #89F7FE 0%, #66A6FF 50%, #8EC5FC 100%)'
      } else {
        return 'linear-gradient(90deg, #89F7FE 0%, #66A6FF 100%)'
      }
    },
    
    getMoodColor(score) {
      if (score >= 9) return '#FF1493'
      if (score >= 7) return '#FF69B4'
      if (score >= 5) return '#9370DB'
      return '#87CEEB'
    },
    
    prevMonth() {
      if (this.currentMonth === 0) {
        this.currentYear--
        this.currentMonth = 11
      } else {
        this.currentMonth--
      }
      this.loadGardenData()
    },
    
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentYear++
        this.currentMonth = 0
      } else {
        this.currentMonth++
      }
      this.loadGardenData()
    },
    
    showDetail(day) {
      if (!day.hasRecord) return
      this.selectedDay = { ...day }
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
    },
    
    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background: radial-gradient(circle at 20% 80%, rgba(255, 182, 193, 0.3), transparent 40%),
              radial-gradient(circle at 80% 20%, rgba(216, 191, 216, 0.3), transparent 40%),
              radial-gradient(circle at 40% 40%, rgba(255, 250, 205, 0.4), transparent 50%),
              linear-gradient(135deg, #FFF5F5 0%, #F8F8FF 50%, #F5F5DC 100%);
  position: relative;
  overflow: hidden;
}

/* 魔法星星样式 */
.stars-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.star {
  position: absolute;
  background: linear-gradient(135deg, #FFFFFF 0%, #FFFACD 100%);
  border-radius: 50%;
  filter: blur(0.5px);
  animation: floatDown linear infinite;
}

@keyframes floatDown {
  0% {
    transform: translateY(-100px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}

/* 主内容区 */
.main-content {
  position: relative;
  z-index: 2;
  padding: 20rpx;
}

/* 头部区域 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  margin-bottom: 40rpx;
}

.streak-card {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 50rpx;
  padding: 16rpx 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(255, 182, 193, 0.2);
}

.streak-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.streak-content {
  display: flex;
  align-items: baseline;
}

.streak-number {
  font-size: 52rpx;
  font-weight: bold;
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  margin-right: 8rpx;
}

.streak-label {
  font-size: 24rpx;
  color: #666;
}

.back-btn {
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.back-icon {
  font-size: 40rpx;
  color: #666;
}

/* 标题区域 */
.title-section {
  text-align: center;
  margin-bottom: 60rpx;
}

.main-title {
  display: block;
  font-size: 56rpx;
  font-weight: bold;
  background: linear-gradient(135deg, #9370DB 0%, #FF69B4 50%, #FFD700 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  margin-bottom: 16rpx;
}

.sub-title {
  display: block;
  font-size: 28rpx;
  color: #888;
  margin-bottom: 40rpx;
}

.stats-cards {
  display: flex;
  justify-content: center;
  gap: 30rpx;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 40rpx;
  padding: 24rpx 32rpx;
  min-width: 180rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.stat-card.highlight {
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.9), rgba(216, 191, 216, 0.9));
}

.stat-number {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #666;
}

/* 月份切换 */
.month-switcher {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40rpx;
  padding: 0 20rpx;
}

.month-btn {
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.btn-icon {
  font-size: 36rpx;
  color: #666;
}

.month-display {
  text-align: center;
}

.current-month {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.month-summary {
  font-size: 24rpx;
  color: #888;
}

/* 日历网格 */
.calendar-container {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 40rpx;
  padding: 40rpx 20rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 8rpx 40rpx rgba(255, 182, 193, 0.2);
}

.weekdays {
  display: flex;
  margin-bottom: 30rpx;
}

.weekday {
  flex: 1;
  text-align: center;
  font-size: 28rpx;
  color: #666;
}

.weekday.weekend {
  color: #FF6B6B;
}

.days-grid {
  display: flex;
  flex-wrap: wrap;
}

.day-cell {
  width: calc(100% / 7);
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.flower-container {
  display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   width: 100%;
   height: 100%;
   padding: 10rpx;
   position: relative; /* 为绝对定位的日期数字做准备 */
}
.flower-date {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  font-size: 20rpx;
  color: rgba(102, 102, 102, 0.7);
  font-weight: 400;
  z-index: 2;
  background: rgba(255, 255, 255, 0.8);
  width: 28rpx;
  height: 28rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

/* 有花日期的今天数字 */
.flower-date.today-date {
  color: #FF6B6B;
  font-weight: 600;
  background: rgba(255, 107, 107, 0.1);
  border: 1rpx solid rgba(255, 107, 107, 0.3);
}

/* 花朵emoji */
.flower-emoji {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34rpx;
  margin-bottom: 6rpx;
  animation: breathe float infinite alternate;
  position: relative;
  z-index: 1;
}
@keyframes breathe {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5rpx);
  }
}

.flower-badge {
   font-size: 18rpx;
    background: rgba(255, 255, 255, 0.9);
    padding: 4rpx 10rpx;
    border-radius: 16rpx;
    backdrop-filter: blur(10px);
    text-align: center;
    max-width: 90%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #666;
    font-weight: 500;
    margin-top: 2rpx;
}
/* 空日期的容器 */
.empty-day-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 10rpx;
}
.empty-indicator .dot {
  width: 14rpx;
    height: 14rpx;
    background: rgba(221, 221, 221, 0.8);
    border-radius: 50%;
    margin-bottom: 12rpx;
}

.day-number {
  font-size: 28rpx;
    color: #888;
    font-weight: 400;
}

.day-cell.today .day-number {
  color: #FF6B6B;
    font-weight: bold;
    background: rgba(255, 107, 107, 0.1);
    padding: 4rpx 12rpx;
    border-radius: 20rpx;
}
/* 有花朵日期的悬停效果 */
.day-cell.has-record:active .flower-emoji {
  transform: scale(0.95);
  transition: transform 0.2s;
}
.day-cell.today::before {
  content: '';
  position: absolute;
  top: 5rpx;
  right: 5rpx;
  width: 12rpx;
  height: 12rpx;
  background: #FF6B6B;
  border-radius: 50%;
}

/* 月度总结卡片 */
.summary-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 40rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 40rpx rgba(255, 182, 193, 0.2);
}

.summary-header {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}

.summary-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.summary-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.summary-text {
  display: block;
  font-size: 28rpx;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20rpx;
}

.summary-tip {
  display: block;
  font-size: 24rpx;
  color: #888;
  text-align: center;
}

/* 详情弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 40rpx;
}

.modal-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 250, 240, 0.95));
  backdrop-filter: blur(30px);
  border-radius: 40rpx;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20rpx 80rpx rgba(255, 182, 193, 0.4);
  position: relative;
  overflow: hidden;
  
}

.modal-content::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: radial-gradient(circle at center, rgba(255, 215, 0, 0.1) 0%, transparent 70%);
  z-index: -1;
  
}

.modal-header {
  padding: 40rpx 40rpx 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.modal-date {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.modal-emoji {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
  animation: breathe 2s infinite alternate;
}

.modal-close {
  position: absolute;
  top: 40rpx;
  right: 40rpx;
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #666;
  
}

.modal-body {
  flex: 1;
  padding: 0 40rpx;
  overflow-y: auto;

}

.modal-diary {
  width:90%;
  display: block;
  font-size: 32rpx;
  line-height: 1.8;
  color: #333;
  margin-bottom: 40rpx;
  padding: 20rpx 10rpx;
  max-height: 400rpx;        /* 增加最大高度 */
  overflow-y: auto;           /* 允许内部滚动 */
  word-break: break-word;     /* 文字自动换行 */
  -webkit-overflow-scrolling: touch;  /* 平滑滚动 */
}

.mood-energy {
	
  padding: 30rpx;
  margin-right: 78rpx;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30rpx;
  margin-bottom: 20rpx;
}

.energy-label {
	width:90%;
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 16rpx;
}

.energy-bar {
  height: 24rpx;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 16rpx;
}

.energy-fill {
  height: 100%;
  border-radius: 12rpx;
  transition: width 0.8s ease;
}

.energy-value {
  display: block;
  text-align: right;
  font-size: 24rpx;
  color: #666;
}

.modal-footer {
  padding: 30rpx 40rpx 40rpx;
}

.modal-btn {
  background: linear-gradient(135deg, #FF9A9E, #FAD0C4);
  border-radius: 40rpx;
  padding: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-text {
  font-size: 32rpx;
  color: white;
  font-weight: bold;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .main-content {
    max-width: 750rpx;
    margin: 0 auto;
  }
}
.stats-cards {
  display: flex;
  justify-content: center;
  gap: 20rpx;
  flex-wrap: wrap;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 40rpx;
  padding: 20rpx 24rpx;
  min-width: 150rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.stat-number {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.stat-label {
  font-size: 22rpx;
  color: #666;
}

/* 情绪分布样式 */
.mood-distribution {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin: 30rpx 0 20rpx;
  padding: 20rpx;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30rpx;
}

.mood-tag {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 20rpx;
  border-radius: 30rpx;
  font-size: 24rpx;
}

.mood-emoji {
  font-size: 28rpx;
}

.mood-count {
  font-weight: 600;
  color: #333;
}

/* 弹窗元信息 */
.modal-meta {
  width: 82%;
  padding: 20rpx;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 20rpx;
  margin-bottom: 30rpx;
  
}

.meta-label {
  display: block;
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .main-content {
    max-width: 750rpx;
    margin: 0 auto;
  }
  
  .stats-cards {
    gap: 30rpx;
  }
  
  .stat-card {
    min-width: 180rpx;
    padding: 24rpx 32rpx;
  }
  
  .stat-number {
    font-size: 48rpx;
  }
  
  .stat-label {
    font-size: 24rpx;
  }
}
</style>