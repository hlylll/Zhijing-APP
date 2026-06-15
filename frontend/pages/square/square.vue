<template>
  <view class="help-square-container">
    <!-- 顶部导航 -->
    <view class="header">
      <text class="title">帮帮广场</text>
    </view>

    <!-- 三张卡片 - 左大右小布局 -->
    <view class="cards-container">
      <!-- 左侧：职场收获季（大卡片） -->
      <view class="left-card">
        <image class="card-bg" src="/static/bg/zhichang.png" mode="aspectFill"></image>
        <view class="card-overlay"></view>
        <view class="card-content">
          <text class="card-title">职场收获季</text>
          <text class="card-subtitle">分享你的求职感悟 赢取职Q创作金</text>
        </view>
      </view>

      <!-- 右侧：上下两张小卡片 -->
      <view class="right-cards">
        <!-- 右上：求职困惑墙 -->
        <view class="small-card">
          <image class="card-bg" src="/static/bg/kunhuo.jpeg" mode="aspectFill"></image>
          <view class="card-overlay"></view>
          <view class="card-content">
            <text class="small-card-title">求职困惑墙</text>
            <text class="small-card-subtitle">热门问题 邀你回答</text>
          </view>
        </view>

        <!-- 右下：生活小妙招 -->
        <view class="small-card">
          <image class="card-bg" src="/static/bg/life.png" mode="aspectFill"></image>
          <view class="card-overlay"></view>
          <view class="card-content">
            <text class="small-card-title">生活小妙招</text>
            <text class="small-card-subtitle">美好生活 技巧多多</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 热议榜 - 无限滚动版 -->
    <view class="hot-topic-section">
     <view class="section-header">
           <view class="title-wrapper">
             <text class="section-title">热议榜</text>
             <text class="fire-emoji">🔥</text>
             <text class="title-tag">HOT</text>
           </view>
           <view class="more-wrapper">
             <text class="section-more">TOP 5</text>
             <text class="arrow-icon">›</text>
           </view>
		</view>
      
      <!-- 滚动容器 -->
      <view 
        class="topic-list-container"
        @mouseenter="pauseRotation"   
        @mouseleave="resumeRotation"  
        @wheel="handleWheel"
      >
        <view 
          class="topic-list" 
          :class="{ 'scrolling': isScrolling }"
          :style="scrollStyle"
        >
          <view 
            class="topic-item" 
            v-for="(item, index) in scrollTopicsList" 
            :key="index"
          >
            <!-- 序号：基于当前显示的真实序号 -->
              <text class="topic-rank" :class="{ 'top-three': getRealIndex(index) < 3 }">
                      {{ getRealIndex(index) + 1 }}
            </text>
            <text class="topic-content">{{ item.content }}</text>
            <text class="topic-tag" v-if="item.tag">{{ item.tag }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 分类标签 -->
    <view class="category-tabs">
      <view 
        v-for="tab in categoryTabs" 
        :key="tab.name"
        class="tab-item"
        :class="{ active: activeTab === tab.name }"
        @tap="switchTab(tab.name)"
      >
        <text class="tab-name">{{ tab.name }}</text>
        <text class="tab-desc">{{ tab.desc }}</text>
      </view>
    </view>

    <!-- 竞赛专区 -->
    <view class="contest-card" v-if="activeTab === '竞赛'">
      <view class="contest-header">
        <text class="contest-title">2026年蓝桥杯大赛报名开启</text>
        <text class="contest-badge">热门</text>
      </view>
      <text class="contest-desc">含金量高的算法竞赛，适合计算机专业学生参加</text>
      <view class="contest-tags">
        <text class="tag">#算法</text>
        <text class="tag">#国家级</text>
      </view>
      <view class="contest-footer">
        <text class="deadline">68天后截止</text>
        <text class="detail-link">查看详情</text>
      </view>
    </view>

    <!-- 内容列表 -->
    <view class="content-list">
      <view class="post-card" v-for="(post, index) in allPosts" :key="index">
        <view class="post-header">
          <view class="user-info">
            <text class="user-name">{{ post.userName }}</text>
            <text class="user-meta">{{ post.userMeta }}</text>
          </view>
        </view>
        <text class="post-content">{{ post.content }}</text>
        <view class="post-footer">
          <view class="post-tags">
            <text v-for="tag in post.tags" :key="tag" class="mini-tag">{{ tag }}</text>
          </view>
          <view class="post-stats">
            <text class="stat">💬 {{ post.comments }}</text>
            <text class="stat">👍 {{ post.likes }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';

const hotTopics = ref([]);
const allPosts = ref([]);
const activeTab = ref('推荐');

// 轮换相关变量
let rotationTimer = null;
let scrollPosition = 0;
let isScrolling = ref(false);
const displayCount = 5; // 同时显示的条数
const itemHeight = 80; // 每个话题项的高度(rpx)
const currentPage = ref(0); // 当前显示的页码

// 计算滚动样式
const scrollStyle = computed(() => {
  return {
    transform: `translateY(-${scrollPosition * itemHeight}rpx)`,
    transition: isScrolling.value ? 'transform 0.5s ease' : 'none'
  };
});
const getRealIndex = (displayIndex) => {
  if (!hotTopics.value.length) return 0;
  // 返回原始数据中的真实索引（0-14）
  return displayIndex % hotTopics.value.length;
};
// 创建无限循环的列表 - 复制3份数据并保留原始索引
const scrollTopicsList = computed(() => {
  if (hotTopics.value.length === 0) return [];
  
  const copies = 3;
  const result = [];
  for (let i = 0; i < copies; i++) {
    hotTopics.value.forEach((item, idx) => {
      result.push({
        ...item,
        originalIndex: idx  // 保存原始索引（0-14）
      });
    });
  }
  return result;
});

// 计算原始数据长度
const originalLength = computed(() => hotTopics.value.length);

// 监听hotTopics变化，重置滚动位置
watch(hotTopics, () => {
  scrollPosition = 0;
  isScrolling.value = false;
  currentPage.value = 0;
  console.log('热议榜数据已更新，共', hotTopics.value.length, '条');
});

const categoryTabs = ref([
  { name: '推荐', desc: '为你精选' },
  { name: '职场', desc: '求职·经验' },
  { name: '竞赛', desc: '比赛·保研' },
  { name: '生活', desc: '日常·技巧' }
]);

// 转换热议榜数据格式
const transformHotTopics = (data) => {
  if (Array.isArray(data)) {
    // 按 sort_order 排序
    return data
      .sort((a, b) => (a.sort_order || a.id) - (b.sort_order || b.id))
      .map(item => ({
        content: item.content,
        tag: item.tag || ''
      }));
  }
  else if (data && data.data && Array.isArray(data.data)) {
    return data.data
      .sort((a, b) => (a.sort_order || a.id) - (b.sort_order || b.id))
      .map(item => ({
        content: item.content,
        tag: item.tag || ''
      }));
  }
  return [];
};

// 轮换显示下5条数据
const rotateTopics = () => {
  if (originalLength.value === 0) return;
  
  const totalItems = originalLength.value; // 15
  const totalPages = Math.ceil(totalItems / displayCount); // 3页 (15/5=3)
  const maxPage = totalPages - 1; // 2
  
  // 计算下一页
  let nextPage = currentPage.value + 1;
  if (nextPage > maxPage) {
    nextPage = 0; // 重置到第一页
  }
  
  // 计算要滚动到的位置
  const targetPosition = nextPage * displayCount;
  
  // 执行滚动动画
  scrollPosition = targetPosition;
  isScrolling.value = true;
  
  // 更新当前页码
  currentPage.value = nextPage;
  
  // 计算实际显示的记录范围
  const startIdx = nextPage * displayCount; // 0,5,10
  const endIdx = Math.min(startIdx + displayCount, totalItems); // 5,10,15
  
  console.log(`切换到第${nextPage + 1}页，显示第${startIdx + 1}-${endIdx}条`);
  console.log('当前滚动位置:', scrollPosition, '目标位置:', targetPosition);
  
  // 如果到达最后，动画结束后重置位置
  if (nextPage === 0) {
    setTimeout(() => {
      isScrolling.value = false;
      scrollPosition = 0;
    }, 500);
  }
};

// 开始自动轮换
const startAutoRotation = () => {
  if (rotationTimer) clearInterval(rotationTimer);
  if (originalLength.value > 0) {
    rotationTimer = setInterval(() => {
      rotateTopics();
    }, 10000);
    console.log('开始自动轮换，每10秒切换一次');
  }
};

// 暂停轮换
const pauseRotation = () => {
  if (rotationTimer) {
    clearInterval(rotationTimer);
    rotationTimer = null;
  }
};

// 恢复轮换
const resumeRotation = () => {
  startAutoRotation();
};

// 手动滚动处理
const handleWheel = () => {
  pauseRotation();
  setTimeout(() => {
    resumeRotation();
  }, 5000);
};

// 获取热议榜
const fetchHotTopics = async () => {
  try {
    const res = await uni.request({
      url: 'http://127.0.0.1:8000/api/hot-topics',
      method: 'GET'
    });
    
    console.log('热议榜原始响应:', res);
    console.log('热议榜数据:', res.data);
    
    // 转换数据
    let topics = transformHotTopics(res.data);
    console.log('转换后数据:', topics);
    
    if (topics.length === 0) {
      console.warn('没有获取到热议榜数据');
      return;
    }
    
    hotTopics.value = topics;
    console.log('最终热议榜数据:', hotTopics.value.length, '条');
    console.log('数据内容:', hotTopics.value);
    
    // 重置状态
    scrollPosition = 0;
    currentPage.value = 0;
    isScrolling.value = false;
    
    // 启动轮换定时器
    startAutoRotation();
  } catch (error) {
    console.error('获取热议榜失败:', error);
  }
};

// 获取帖子列表
const fetchPosts = async (category) => {
  try {
    let url = 'http://127.0.0.1:8000/api/posts';
    if (category && category !== '推荐') {
      url += `?category=${encodeURIComponent(category)}`;
    }
    const res = await uni.request({
      url: url,
      method: 'GET'
    });
    console.log('帖子数据:', res.data);
    allPosts.value = transformPosts(res.data);
  } catch (error) {
    console.error('获取帖子失败:', error);
  }
};

// 转换帖子数据格式
const transformPosts = (data) => {
  if (!data) return [];
  
  if (Array.isArray(data)) {
    return data.map(item => ({
      userName: item.user_name || '匿名用户',
      userMeta: item.user_meta || '',
      content: item.content || '',
      tags: item.tags || [],
      comments: item.comments || 0,
      likes: item.likes || 0
    }));
  }
  else if (data && data.data && Array.isArray(data.data)) {
    return data.data.map(item => ({
      userName: item.user_name || '匿名用户',
      userMeta: item.user_meta || '',
      content: item.content || '',
      tags: item.tags || [],
      comments: item.comments || 0,
      likes: item.likes || 0
    }));
  }
  return [];
};

// 切换标签
const switchTab = (tab) => {
  activeTab.value = tab;
  fetchPosts(tab);
};

onMounted(() => {
  fetchHotTopics();
  fetchPosts('推荐');
});

onUnmounted(() => {
  if (rotationTimer) {
    clearInterval(rotationTimer);
    rotationTimer = null;
  }
});
</script>

<style scoped>
.help-square-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f9ff 0%, #eef3fe 100%);
  padding: 40rpx 32rpx 60rpx;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* 顶部导航 */
.header {
  margin-bottom: 32rpx;
}

.title {
  font-size: 52rpx;
  font-weight: 700;
  color: #1a2b4c;
  letter-spacing: 2rpx;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 三张卡片 - 左大右小布局 */
.cards-container {
  display: flex;
  gap: 20rpx;
  margin-bottom: 40rpx;
  height: 360rpx;
}

/* 左侧大卡片 */
.left-card {
  flex: 1;
  position: relative;
  border-radius: 32rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 40rpx rgba(0, 0, 0, 0.1);
}

/* 右侧两张小卡片容器 */
.right-cards {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

/* 右侧小卡片 */
.small-card {
  flex: 1;
  position: relative;
  border-radius: 32rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 40rpx rgba(0, 0, 0, 0.1);
}

/* 卡片背景图片 */
.card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 卡片遮罩层 */
.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.left-card .card-overlay {
  background: linear-gradient(135deg, rgba(85, 170, 255, 0.7) 0%, rgba(0,0,0,0.3) 100%);
}

.small-card:nth-child(1) .card-overlay {
  background: linear-gradient(135deg, rgba(255, 170, 127, 0.7) 0%, rgba(0,0,0,0.3) 100%);
}

.small-card:nth-child(2) .card-overlay {
  background: linear-gradient(135deg, rgba(255, 170, 255, 0.7) 0%, rgba(0,0,0,0.3) 100%);
}

/* 卡片内容 */
.card-content {
  position: relative;
  z-index: 3;
  height: 100%;
  padding: 30rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

/* 大卡片文字 */
.card-title {
  font-size: 40rpx;
  font-weight: 700;
  color: #ffffff;
  display: block;
  margin-bottom: 35rpx;
  text-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.3);
}

.card-subtitle {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 50rpx;
  display: block;
  line-height: 1.5;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

/* 小卡片文字 */
.small-card-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #ffffff;
  display: block;
  margin-bottom: 8rpx;
  text-shadow: 0 4rpx 8rpx rg8(0, 0, 0, 0.3);
}

.small-card-subtitle {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.95);
  display: block;
  margin-bottom: 35rpx;
  line-height: 1.4;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}







/* 热议榜滚动容器 */
.hot-topic-section {
  margin: 30rpx 20rpx;
  background: linear-gradient(135deg, #fff5f0 0%, #ffffff 100%);
  border-radius: 24rpx;
  padding: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(255, 107, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
  padding: 0 10rpx;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 12rpx;
  position: relative;
}

.section-title {
  font-size: 40rpx;
  font-weight: 700;
  background: linear-gradient(135deg, #ff6b00 0%, #ff3300 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2rpx;
  text-shadow: 0 2rpx 10rpx rgba(255, 107, 0, 0.3);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -4rpx;
  left: 0;
  width: 100%;
  height: 6rpx;
  background: linear-gradient(90deg, #ff6b00, #ffaa00, #ff6b00);
  border-radius: 3rpx;
  opacity: 0.5;
}

.fire-emoji {
  font-size: 48rpx;
  animation: flameFlicker 1.5s ease-in-out infinite;
  transform-origin: center;
  filter: drop-shadow(0 0 6rpx rgba(255, 107, 0, 0.6));
}

@keyframes flameFlicker {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    filter: drop-shadow(0 0 6rpx rgba(255, 107, 0, 0.6));
  }
  25% {
    transform: scale(1.2) rotate(5deg);
    filter: drop-shadow(0 0 12rpx rgba(255, 107, 0, 0.9));
  }
  50% {
    transform: scale(1.1) rotate(-3deg);
    filter: drop-shadow(0 0 15rpx rgba(255, 68, 0, 1));
  }
  75% {
    transform: scale(1.15) rotate(2deg);
    filter: drop-shadow(0 0 10rpx rgba(255, 107, 0, 0.8));
  }
}

.title-tag {
  font-size: 24rpx;
  font-weight: 600;
  padding: 4rpx 12rpx;
  background: linear-gradient(135deg, #ff6b00, #ff3300);
  color: white;
  border-radius: 20rpx;
  margin-left: 8rpx;
  letter-spacing: 1rpx;
  box-shadow: 0 4rpx 10rpx rgba(255, 68, 0, 0.3);
  transform: rotate(2deg);
  animation: tagPulse 2s ease-in-out infinite;
}

@keyframes tagPulse {
  0%, 100% {
    transform: rotate(2deg) scale(1);
  }
  50% {
    transform: rotate(2deg) scale(1.05);
    box-shadow: 0 6rpx 15rpx rgba(255, 68, 0, 0.5);
  }
}

.more-wrapper {
  display: flex;
  align-items: center;
  gap: 8rpx;
  background: rgba(255, 107, 0, 0.1);
  padding: 8rpx 16rpx;
  border-radius: 30rpx;
  border: 1rpx solid rgba(255, 107, 0, 0.3);
  backdrop-filter: blur(5rpx);
}

.section-more {
  font-size: 28rpx;
  font-weight: 600;
  color: #ff6b00;
  letter-spacing: 1rpx;
  background: linear-gradient(135deg, #ff6b00, #ff3300);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.arrow-icon {
  font-size: 36rpx;
  color: #ff6b00;
  font-weight: 300;
  line-height: 1;
  transition: transform 0.3s ease;
}

.more-wrapper:active .arrow-icon {
  transform: translateX(4rpx);
}

/* 添加背景装饰 */
.hot-topic-section::before {
  content: '🔥';
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  font-size: 80rpx;
  opacity: 0.05;
  transform: rotate(15deg);
  pointer-events: none;
}

/* 添加微光效果 */
@keyframes shine {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.section-title {
  background: linear-gradient(135deg, #ff6b00 0%, #ff3300 50%, #ffaa00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: shine 3s linear infinite;
}

/* 滚动列表容器 */
.topic-list-container {
  height: 400rpx; /* 5行 * 80rpx = 400rpx */
  overflow: hidden;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20rpx);
  border-radius: 24rpx;
  border: 1px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.03);
}

/* 滚动列表 */
.topic-list {
  transition: transform 0.5s ease;
}

.topic-list.scrolling {
  box-shadow: 0 10rpx 30rpx rgba(74, 144, 226, 0.1);
}

/* 话题项 */
.topic-item {
  display: flex;
  align-items: center;
  padding: 16rpx 20rpx;
  height: 80rpx; /* 固定高度 */
  box-sizing: border-box;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
}

.topic-item:last-child {
  border-bottom: none;
}

.topic-rank {
  width: 48rpx;
  font-size: 26rpx;
  font-weight: 600;
  color: #aaa;
  text-align: center;
  margin-right: 16rpx;
}

.topic-rank.top-three {
  color: #ff9800;
}

.topic-content {
  flex: 1;
  font-size: 26rpx;
  color: #2c3e50;
  margin-right: 16rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topic-tag {
  font-size: 20rpx;
  color: #4a90e2;
  background: rgba(74, 144, 226, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 30rpx;
  white-space: nowrap;
}
@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    opacity: 1;
  }
}



/* 分类标签 */
.category-tabs {
  display: flex;
  gap: 16rpx;
  margin-bottom: 32rpx;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10rpx);
  border-radius: 60rpx;
  padding: 12rpx;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12rpx 0;
  border-radius: 48rpx;
  transition: all 0.3s ease;
}

.tab-item.active {
  background: white;
  box-shadow: 0 10rpx 30rpx rgba(74, 144, 226, 0.15);
}

.tab-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #5a6b7c;
  margin-bottom: 4rpx;
}

.tab-item.active .tab-name {
  color: #4a90e2;
}

.tab-desc {
  font-size: 18rpx;
  color: #8e9aa8;
}

.tab-item.active .tab-desc {
  color: #81d4fa;
}

/* 竞赛卡片 */
.contest-card {
  background: white;
  border-radius: 28rpx;
  padding: 28rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 20rpx 40rpx rgba(74, 144, 226, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.contest-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 12rpx;
}

.contest-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #1a2b4c;
  flex: 1;
}

.contest-badge {
  font-size: 20rpx;
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  padding: 4rpx 16rpx;
  border-radius: 30rpx;
}

.contest-desc {
  font-size: 24rpx;
  color: #5a6b7c;
  margin-bottom: 16rpx;
  line-height: 1.5;
}

.contest-tags {
  display: flex;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.tag {
  font-size: 20rpx;
  background: #f0f5ff;
  color: #4a90e2;
  padding: 4rpx 16rpx;
  border-radius: 30rpx;
}

.contest-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1px solid #f0f0f0;
}

.deadline {
  font-size: 22rpx;
  color: #ff6b6b;
  font-weight: 500;
}

.detail-link {
  font-size: 22rpx;
  color: #4a90e2;
}

/* 内容列表 */
.content-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.post-card {
  background: white;
  border-radius: 28rpx;
  padding: 28rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.post-header {
  margin-bottom: 16rpx;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.user-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3e50;
}

.user-meta {
  font-size: 22rpx;
  color: #8e9aa8;
}

.post-content {
  font-size: 26rpx;
  color: #2c3e50;
  line-height: 1.6;
  margin-bottom: 20rpx;
  display: block;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-tags {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.mini-tag {
  font-size: 20rpx;
  background: #f5f7fa;
  color: #6b7b8c;
  padding: 4rpx 16rpx;
  border-radius: 30rpx;
}

.post-stats {
  display: flex;
  gap: 20rpx;
}

.stat {
  font-size: 22rpx;
  color: #8e9aa8;
  display: flex;
  align-items: center;
}
</style>