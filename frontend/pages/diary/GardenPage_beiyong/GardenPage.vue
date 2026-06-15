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
            <text class="stat-label">朵情绪花</text>
          </view>
          <view class="stat-card highlight">
            <text class="stat-number">{{ moodIndex }}</text>
            <text class="stat-label">心情指数</text>
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
             <!-- 有记录的日子：显示花朵、花名和右上角日期 -->
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
                    boxShadow: getFlowerGlow(day.score),
                    animationDuration: (1 + day.score * 0.1) + 's'
                  }"
                >
                  {{ day.emoji }}
                </view>
                
                <!-- 花名 -->
                <text class="flower-badge" :style="{ color: getMoodColor(day.score) }">
                  {{ day.moodLabel }}
                </text>
              </view>
              
              <!-- 无记录的日子：显示点和日期数字（居中） -->
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
      // 状态栏高度（适配刘海屏）
      statusBarHeight: 44,
      
      // 魔法星星
      stars: [],
      
      // 连续记录天数
      streakDays: 8,
      
      // 当前月份数据
      currentYear: 2026,
      currentMonth: 0, // 0-11
      currentMonthRecords: 12,
      moodIndex: 78,
      
      // 星期显示
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],
      
      // 日历数据
      calendarDays: [],
      
      // 弹窗相关
      showModal: false,
      selectedDay: {},
      
      // 模拟的日记数据
      diaryData: [
        {
          date: '2026-01-03',
          emoji: '🌻',
          score: 9,
          moodLabel: '向日葵',
          diary: '今天阳光特别好，去公园散步看到了小松鼠！心情像向日葵一样绽放～'
        },
        {
          date: '2026-01-05',
          emoji: '☁️',
          score: 6,
          moodLabel: '云朵花',
          diary: '有点多云的一天，不过跟朋友聊了很久的电话，心里暖暖的。'
        },
        {
          date: '2026-01-08',
          emoji: '✨',
          score: 10,
          moodLabel: '星星花',
          diary: '完成了重要的项目！成就感满满，晚上奖励自己一杯奶茶，幸福指数爆表！✨'
        },
        {
          date: '2026-01-12',
          emoji: '🌧️',
          score: 4,
          moodLabel: '雨滴花',
          diary: '下雨天，心情有点低落。不过听了喜欢的音乐，慢慢平静下来了。'
        },
        {
          date: '2026-01-15',
          emoji: '🌸',
          score: 8,
          moodLabel: '樱花',
          diary: '跟好久不见的朋友见面了，聊了很多大学时候的趣事，樱花飘落的季节总是让人怀念。'
        },
        {
          date: '2026-01-18',
          emoji: '🌙',
          score: 7,
          moodLabel: '月光花',
          diary: '晚上看到超美的月亮，安静地思考了很多事情，内心很平和。'
        },
        {
          date: '2026-01-20',
          emoji: '🌈',
          score: 9,
          moodLabel: '彩虹花',
          diary: '雨后看到彩虹啦！果然风雨过后会有美丽的风景呢～'
        },
        {
          date: '2026-01-22',
          emoji: '☀️',
          score: 10,
          moodLabel: '太阳花',
          diary: '今天一切都特别顺利！早起运动、高效工作、晚上还学会了一道新菜，完美的一天！'
        },
        {
          date: '2026-01-25',
          emoji: '💫',
          score: 8,
          moodLabel: '彗星花',
          diary: '有了新的灵感，开始了一个有趣的小项目，期待能像彗星一样闪亮！'
        },
        {
          date: '2026-01-28',
          emoji: '🍃',
          score: 5,
          moodLabel: '绿叶花',
          diary: '普通的一天，但平凡中也有些小确幸，比如喝到了喜欢的抹茶拿铁。'
        },
        {
          date: '2026-01-30',
          emoji: '🌺',
          score: 9,
          moodLabel: '热带花',
          diary: '计划了期待已久的旅行！已经开始想象热带海岛的风光了～'
        }
      ]
    }
  },
  
  computed: {
    // 连续记录渐变背景
    streakGradient() {
      return 'linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 50%, #FAD0C4 100%)'
    },
    
    // 月度总结文案
    monthlySummary() {
      const avgScore = this.calculateAverageScore()
      if (avgScore >= 8) {
        return '本月的花园阳光明媚，充满了快乐的能量！你的积极心情像阳光一样温暖了整个花园。'
      } else if (avgScore >= 6) {
        return '本月的花园有晴有雨，但总体平和美好。每一种情绪都是花园里独特的花朵。'
      } else {
        return '本月的花园经历了一些风雨，但每一朵花都在努力生长。继续浇灌，春天总会到来。'
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
  
  onLoad() {
    // 获取状态栏高度（实际项目中需要调用uni.getSystemInfo）
    this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight
    
    // 生成魔法星星
    this.generateStars()
    
    // 初始化日历
    this.generateCalendar()
  },
  
  methods: {
    // 生成魔法星星
    generateStars() {
      const stars = []
      const starCount = 20 // 星星数量
      
      for (let i = 0; i < starCount; i++) {
        stars.push({
          left: Math.random() * 100, // 0-100% 宽度内的随机位置
          top: -Math.random() * 100, // 从屏幕上方开始
          size: 2 + Math.random() * 4, // 2-6px大小
          opacity: 0.3 + Math.random() * 0.7, // 0.3-1透明度
          delay: Math.random() * 5, // 0-5秒延迟开始
          duration: 10 + Math.random() * 20 // 10-30秒完成动画
        })
      }
      
      this.stars = stars
    },
    
    // 生成日历
    generateCalendar() {
      const year = this.currentYear
      const month = this.currentMonth
      const today = new Date()
      
      // 获取当月第一天
      const firstDay = new Date(year, month, 1)
      // 获取当月最后一天
      const lastDay = new Date(year, month + 1, 0)
      // 第一天是星期几（0-6，0代表周日）
      const firstDayWeekday = firstDay.getDay()
      // 当月天数
      const daysInMonth = lastDay.getDate()
      
      const calendarDays = []
      
      // 添加上个月的空格
      for (let i = 0; i < firstDayWeekday; i++) {
        calendarDays.push({
          date: '',
          hasRecord: false,
          isToday: false
        })
      }
      
      // 添加当月日期
      for (let i = 1; i <= daysInMonth; i++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
        const isToday = 
          today.getFullYear() === year &&
          today.getMonth() === month &&
          today.getDate() === i
        
        // 查找是否有当天的日记
        const diaryEntry = this.diaryData.find(item => item.date === dateStr)
        
        if (diaryEntry) {
          calendarDays.push({
            date: i,
            fullDate: dateStr,
            hasRecord: true,
            isToday,
            ...diaryEntry
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
    
    // 计算平均心情分数
    calculateAverageScore() {
      const records = this.calendarDays.filter(day => day.hasRecord)
      if (records.length === 0) return 0
      
      const totalScore = records.reduce((sum, day) => sum + day.score, 0)
      return totalScore / records.length
    },
    
    // 获取花朵渐变背景
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
    getDayNumber(day) {
      // 如果day.date是字符串，提取数字部分
      if (typeof day.date === 'string') {
        const match = day.date.match(/\d{4}-\d{2}-(\d{2})/)
        return match ? parseInt(match[1], 10) : day.date
      }
      // 如果是数字，直接返回
      return day.date
    },
    // 获取花朵发光效果
   getFlowerGlow(score) {
     const intensity = score * 1.5  // 稍微降低强度
     const spread = score * 1.2     // 稍微减小扩散范围
     const color = score >= 9 ? 'rgba(255, 215, 0, 0.4)' :  // 0.8 -> 0.4
                  score >= 7 ? 'rgba(255, 182, 193, 0.3)' :  // 0.6 -> 0.3
                  score >= 5 ? 'rgba(173, 216, 230, 0.25)' : // 0.5 -> 0.25
                  'rgba(135, 206, 250, 0.2)'                 // 0.4 -> 0.2
     
     return `0 0 ${spread}px ${intensity}px ${color}`
   },
    
    // 获取能量条渐变
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
    
    // 获取心情颜色
    getMoodColor(score) {
      if (score >= 9) return '#FF1493'
      if (score >= 7) return '#FF69B4'
      if (score >= 5) return '#9370DB'
      return '#87CEEB'
    },
    
    // 月份切换
    prevMonth() {
      if (this.currentMonth === 0) {
        this.currentYear--
        this.currentMonth = 11
      } else {
        this.currentMonth--
      }
      this.generateCalendar()
    },
    
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentYear++
        this.currentMonth = 0
      } else {
        this.currentMonth++
      }
      this.generateCalendar()
    },
    
    // 显示日记详情
    showDetail(day) {
      this.selectedDay = { ...day }
      this.showModal = true
    },
    
    // 关闭弹窗
    closeModal() {
      this.showModal = false
    },
    
    // 返回上一页
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
  display: block;
  font-size: 32rpx;
  line-height: 1.8;
  color: #333;
  margin-bottom: 40rpx;
  padding: 20rpx 0;
    
}

.mood-energy {
  padding: 30rpx;
  margin-right: 78rpx;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30rpx;
  margin-bottom: 20rpx;
}

.energy-label {
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
</style>
