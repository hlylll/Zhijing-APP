<template>
  <view class="rednote-container">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-box">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          placeholder="搜竞赛、实习、考研资料..."
          v-model="searchKeyword"
          confirm-type="search"
          :focus="searchFocus"
          @focus="onSearchFocus"
          @blur="onSearchBlur"
          @confirm="doSearch"
        />
      </view>
    </view>

    <!-- 分类标签（横向滑动） -->
    <scroll-view scroll-x class="category-scroll" show-scrollbar="false">
      <view class="category-wrapper">
        <view 
          v-for="tab in tabs" 
          :key="tab"
          class="category-item"
          :class="{ active: currentTab === tab }"
          @tap="switchTab(tab)"
        >
          <text>{{ tab }}</text>
          <view class="active-line" v-if="currentTab === tab"></view>
        </view>
      </view>
    </scroll-view>

    <!-- 双列瀑布流卡片 -->
    <view class="waterfall-container">
      <!-- 左列 -->
      <view class="waterfall-column">
        <view 
          v-for="(item, index) in leftColumnCards" 
          :key="'left-' + item.id"
          class="feed-card"
          @tap="goDetail(item.id)"
        >
          <view class="card-image-wrapper">
            <image 
              :src="item.image" 
              mode="aspectFill" 
              class="card-image"
              :style="{ height: getImageHeight(index) }"
            />
            <view class="card-badge" v-if="item.badge">{{ item.badge }}</view>
          </view>
          
          <view class="card-info">
            <text class="card-title">{{ item.title }}</text>
            <text class="card-desc">{{ item.subtitle }}</text>
            
            <view class="card-meta">
              <view class="tags">
                <text class="tag" v-for="tag in item.tags.slice(0,2)" :key="tag">#{{ tag }}</text>
              </view>
              <view class="stats">
                <text class="stat">👤 {{ item.participants }}</text>
                <text class="stat">⭐ {{ item.rating }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 右列 -->
      <view class="waterfall-column">
        <view 
          v-for="(item, index) in rightColumnCards" 
          :key="'right-' + item.id"
          class="feed-card"
          @tap="goDetail(item.id)"
        >
          <view class="card-image-wrapper">
            <image 
              :src="item.image" 
              mode="aspectFill" 
              class="card-image"
              :style="{ height: getImageHeight(index + 5) }"
            />
            <view class="card-badge" v-if="item.badge">{{ item.badge }}</view>
          </view>
          
          <view class="card-info">
            <text class="card-title">{{ item.title }}</text>
            <text class="card-desc">{{ item.subtitle }}</text>
            
            <view class="card-meta">
              <view class="tags">
                <text class="tag" v-for="tag in item.tags.slice(0,2)" :key="tag">#{{ tag }}</text>
              </view>
              <view class="stats">
                <text class="stat">👤 {{ item.participants }}</text>
                <text class="stat">⭐ {{ item.rating }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more" v-if="loading">
      <text>加载中...</text>
    </view>
    <view class="load-more" v-else-if="!hasMore">
      <text>已经到底啦～</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 搜索相关
const searchKeyword = ref('')
const searchFocus = ref(false)

// 分类标签
const tabs = ref(['全部', '竞赛', '实习', '考研', '路径', '心理', '生活实践'])
const currentTab = ref('全部')

// 数据相关
const allCards = ref([])
const loading = ref(false)
const hasMore = ref(true)
const page = ref(1)

// 计算左右两列的数据
const leftColumnCards = computed(() => {
  return allCards.value.filter((_, index) => index % 2 === 0)
})

const rightColumnCards = computed(() => {
  return allCards.value.filter((_, index) => index % 2 === 1)
})

// 随机生成图片高度（模拟不同尺寸的图片）
const getImageHeight = (index) => {
  const heights = ['320rpx', '380rpx', '280rpx', '420rpx', '360rpx', '300rpx']
  return heights[index % heights.length]
}

// 获取推荐卡片数据
const fetchRecommendCards = async (category = '全部', loadMore = false) => {
  if (loading.value) return
  
  loading.value = true
  try {
    let url = `http://127.0.0.1:8000/api/recommend-cards?page=${page.value}&page_size=10`
    if (category && category !== '全部') {
      url += `&category=${encodeURIComponent(category)}`
    }
    
    const res = await uni.request({
      url: url,
      method: 'GET'
    })
    
    console.log('推荐卡片数据:', res.data)
    
    // 处理后端返回的数据
    let newData = []
    if (res.data && res.data.data) {
      newData = res.data.data
    } else if (Array.isArray(res.data)) {
      newData = res.data
    }
    
    if (loadMore) {
      allCards.value = [...allCards.value, ...newData]
    } else {
      allCards.value = newData
    }
    
    // 判断是否还有更多数据
    hasMore.value = newData.length === 10
    
  } catch (error) {
    console.error('获取推荐卡片失败:', error)
    // 如果后端获取失败，使用模拟数据
   
    
    if (category === '全部') {
      allCards.value = mockData
    } else {
      allCards.value = mockData.filter(item => item.category === category)
    }
  } finally {
    loading.value = false
  }
}

// 切换标签
const switchTab = (tab) => {
  currentTab.value = tab
  page.value = 1
  fetchRecommendCards(tab)
}

// 加载更多
const loadMore = () => {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchRecommendCards(currentTab.value, true)
  }
}

// 跳转详情
const goDetail = (id) => {
  uni.navigateTo({
    url: `/pages/info/detail?id=${id}`
  })
}

// 搜索相关函数
const focusSearch = () => {
  searchFocus.value = true
}

const onSearchFocus = () => {
  searchFocus.value = true
}

const onSearchBlur = () => {
  console.log('搜索框失焦')
}

const doSearch = () => {
  if (!searchKeyword.value.trim()) {
    uni.showToast({ title: '请输入搜索内容', icon: 'none' })
    return
  }
  console.log('执行搜索：', searchKeyword.value)
  uni.showToast({ title: `搜索：${searchKeyword.value}`, icon: 'none' })
}

// 页面加载
onLoad((options) => {
  console.log('推荐页面加载完成', options)
  fetchRecommendCards('全部')
})

// 监听滚动到底部
onMounted(() => {
  // 使用 UniApp 的页面滚动监听
  uni.onReachBottom && uni.onReachBottom(() => {
    loadMore()
  })
})
</script>

<style scoped>
.rednote-container {
  min-height: 100vh;
  background-color: #f8f8f8;
  padding: 24rpx 24rpx 40rpx;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* 搜索栏 */
.search-section {
  margin-bottom: 30rpx;
}

.search-box {
  background: white;
  height: 80rpx;
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.03);
}

.search-icon {
  font-size: 32rpx;
  color: #999;
  margin-right: 16rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

/* 分类标签 */
.category-scroll {
  margin-bottom: 30rpx;
  white-space: nowrap;
  width: 100%;
}

.category-wrapper {
  display: flex;
  flex-direction: row;
  gap: 40rpx;
  padding: 0 8rpx;
}

.category-item {
  position: relative;
  font-size: 32rpx;
  color: #666;
  padding: 12rpx 0;
  font-weight: 500;
  flex-shrink: 0;
  white-space: nowrap;
}

.category-item.active {
  color: #FF6B6B;
  font-weight: 600;
}

.active-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background: #FF6B6B;
  border-radius: 2rpx;
}

/* 瀑布流容器 */
.waterfall-container {
  display: flex;
  gap: 24rpx;
}

.waterfall-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

/* 卡片样式 */
.feed-card {
  background: white;
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  width: 100%;
}

.feed-card:active {
  transform: scale(0.98);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.card-image {
  width: 100%;
  display: block;
  transition: transform 0.3s ease;
}

.feed-card:hover .card-image {
  transform: scale(1.05);
}

.card-badge {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  background: #FF6B6B;
  color: white;
  font-size: 24rpx;
  font-weight: 600;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  z-index: 2;
}

.card-info {
  padding: 24rpx 20rpx 20rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 8rpx;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 16rpx;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  margin-top: 8rpx;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-bottom: 12rpx;
}

.tag {
  font-size: 22rpx;
  color: #FF6B6B;
  background: rgba(255, 107, 107, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 16rpx;
}

.stats {
  display: flex;
  gap: 16rpx;
}

.stat {
  font-size: 24rpx;
  color: #666;
}

/* 加载更多 */
.load-more {
  text-align: center;
  padding: 40rpx;
  color: #999;
  font-size: 28rpx;
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feed-card {
  animation: fadeInUp 0.5s ease;
}

.feed-card:nth-child(2n) {
  animation-delay: 0.1s;
}

.feed-card:nth-child(3n) {
  animation-delay: 0.2s;
}
</style>