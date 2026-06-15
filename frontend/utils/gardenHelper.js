import dayjs from 'dayjs'

// 生成月份数据
export function generateMonthData(yearMonth) {
  const [year, month] = yearMonth.split('-').map(Number)
  const daysInMonth = dayjs(`${year}-${month}`).daysInMonth()
  const firstDay = dayjs(`${year}-${month}-01`).day()
  
  const days = []
  
  // 获取实际数据（这里从本地存储或API获取）
  const diaryData = getDiaryDataForMonth(yearMonth)
  
  // 生成每一天的数据
  for (let i = 1; i <= daysInMonth; i++) {
    const date = `${year}-${month.toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`
    const diary = diaryData.find(d => d.date === date)
    
    days.push({
      date,
      day: i,
      mood: diary?.mood || 'neutral',
      intensity: diary?.intensity || 0.5,
      diary: diary?.content || '',
      hasEntry: !!diary,
      isToday: date === dayjs().format('YYYY-MM-DD'),
      diaryLength: diary?.content?.length || 0,
      flowerType: getFlowerType(diary?.mood)
    })
  }
  
  return {
    yearMonth,
    startDay: firstDay,
    days
  }
}

// 根据情绪获取花朵类型
function getFlowerType(mood) {
  const mapping = {
    happy: 'sunflower',
    peaceful: 'cloud',
    sad: 'raindrop',
    excited: 'fire',
    thoughtful: 'moon',
    neutral: 'default'
  }
  return mapping[mood] || 'default'
}

// 从本地存储获取日记数据
function getDiaryDataForMonth(yearMonth) {
  try {
    const diaries = JSON.parse(localStorage.getItem('infog-diaries') || '[]')
    return diaries.filter(diary => diary.date.startsWith(yearMonth))
  } catch (error) {
    console.error('读取日记数据失败:', error)
    return []
  }
}

// 计算连续记录天数
export function calculateStreak() {
  const diaries = JSON.parse(localStorage.getItem('infog-diaries') || '[]')
  if (diaries.length === 0) return 0
  
  const sortedDates = diaries
    .map(d => d.date)
    .sort()
    .reverse()
  
  let streak = 1
  let currentDate = dayjs(sortedDates[0])
  
  for (let i = 1; i < sortedDates.length; i++) {
    const prevDate = dayjs(sortedDates[i])
    const diff = currentDate.diff(prevDate, 'day')
    
    if (diff === 1) {
      streak++
      currentDate = prevDate
    } else {
      break
    }
  }
  
  return streak
}

// 获取本周统计
export function getWeekStats(days) {
  const stats = {
    happy: 0,
    peaceful: 0,
    sad: 0,
    excited: 0,
    thoughtful: 0
  }
  
  const thisWeek = days.filter(day => {
    const dayDate = dayjs(day.date)
    const weekStart = dayjs().startOf('week')
    const weekEnd = dayjs().endOf('week')
    return dayDate.isBetween(weekStart, weekEnd, null, '[]')
  })
  
  thisWeek.forEach(day => {
    if (stats[day.mood] !== undefined) {
      stats[day.mood]++
    }
  })
  
  // 转换为文本：开心3天 | 平静2天...
  return Object.entries(stats)
    .filter(([_, count]) => count > 0)
    .map(([mood, count]) => `${getMoodName(mood)}${count}天`)
    .join(' | ')
}

// 获取情绪中文名
function getMoodName(mood) {
  const names = {
    happy: '开心',
    peaceful: '平静',
    sad: '难过',
    excited: '兴奋',
    thoughtful: '思考'
  }
  return names[mood] || mood
}
// 添加模拟数据生成函数
function generateMockData(yearMonth) {
  const [year, month] = yearMonth.split('-').map(Number)
  const daysInMonth = dayjs(`${year}-${month}`).daysInMonth()
  
  const emotions = ['happy', 'peaceful', 'sad', 'excited', 'thoughtful', 'neutral']
  const mockColors = {
    happy: '#FFD700',
    peaceful: '#87CEEB',
    sad: '#4682B4',
    excited: '#FF69B4',
    thoughtful: '#9370DB',
    neutral: '#D3D3D3'
  }
  
  const mockData = []
  
  for (let i = 1; i <= daysInMonth; i++) {
    const date = `${year}-${month.toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`
    const emotionIndex = Math.floor(Math.random() * emotions.length)
    const mood = emotions[emotionIndex]
    
    // 随机决定是否有日记（30%的几率）
    const hasEntry = Math.random() > 0.7
    
    mockData.push({
      date: date,
      mood: mood,
      intensity: Math.random().toFixed(2),
      content: hasEntry ? `这是${date}的模拟日记内容...` : '',
      color: mockColors[mood]
    })
  }
  
  return mockData
}

// 修改 getDiaryDataForMonth 函数
function getDiaryDataForMonth(yearMonth) {
  try {
    const diaries = JSON.parse(localStorage.getItem('infog-diaries') || '[]')
    
    // 如果没有数据，返回模拟数据
    if (diaries.length === 0) {
      console.log('没有本地数据，使用模拟数据')
      return generateMockData(yearMonth)
    }
    
    return diaries.filter(diary => diary.date.startsWith(yearMonth))
  } catch (error) {
    console.error('读取日记数据失败，使用模拟数据:', error)
    return generateMockData(yearMonth)
  }
  }