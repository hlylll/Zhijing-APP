<!-- pages/login/login.vue （或 index/index.vue，根据你的页面路径） -->
<template>
  <view class="login-container">
    <view class="login-content">
		<div class="logo">
		         <h1>知径</h1>
		       </div>
		       <div class="slogan">
		         <p>知你所感</p>
		         <p>径你所向</p>
		       </div>
		       <div class="subtitle">
		         <p>成长有知，前路有径</p>
		       </div>

      <!-- 账号输入 -->
      <view class="input-group">
        <input 
          class="input-field" 
          type="number" 
          placeholder="请输入手机号" 
          v-model="phone"
        />
      </view>

      <!-- 验证码输入 -->
      <view class="input-group">
        <view class="code-wrapper">
          <input 
            class="input-field code-input" 
            type="number" 
            placeholder="请输入验证码" 
            v-model="code"
          />
          <button 
            class="get-code-btn" 
            :disabled="countdown > 0"
            @click="getCode"
          >
            {{ countdown > 0 ? countdown + 's' : '获取验证码' }}
          </button>
        </view>
      </view>

      <!-- 登录按钮 -->
      <button 
        class="login-btn" 
        @click="startJourney"
      >
        开始我的成长旅程
      </button>

      <!-- 用户协议 checkbox -->
      <view class="agreement">
      <view class="agreement" @click="toggleAgree">
          <view class="custom-checkbox" :class="{ checked: agreed }">
            <text v-if="agreed" class="checkmark">✓</text>
          </view>
          <text class="agreement-text">我已阅读并同意《用户协议》</text>
        </view>
      </view>

      <!-- 第三方登录 -->
      <view class="third-party">
        <text class="third-title">第三方登录</text>
        <view class="icons">
          <image class="icon" src="/static/icons/wechat.png" mode="aspectFit" />
          <image class="icon" src="/static/icons/qq.png" mode="aspectFit" />
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const phone = ref('')
const code = ref('')
const countdown = ref(0)
const agreed = ref(false)

const API_BASE = 'http://localhost:8000'

const getCode = async () => {
  if (!phone.value || phone.value.length !== 11 || !/^1[3-9]\d{9}$/.test(phone.value)) {
    uni.showToast({ title: '请输入正确的11位手机号', icon: 'none' })
    return
  }
  
  if (!agreed.value) {
    uni.showToast({ title: '请先同意用户协议', icon: 'none' })
    return
  }
  
  try {
    // 修改请求方式，不使用数组解构
    const res = await uni.request({
      url: `${API_BASE}/api/send-code`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: { phone: phone.value }
    })
    
    console.log('验证码响应：', res) // 添加日志
    
    // 注意：res 是一个对象，包含 statusCode、data 等属性
    if (res.statusCode === 200 && res.data && res.data.success) {
      uni.showToast({ title: '验证码已发送', icon: 'success' })
      code.value = res.data.debug_code || ''
      countdown.value = 60
      const timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) clearInterval(timer)
      }, 1000)
    } else {
      uni.showToast({ 
        title: res.data?.message || `发送失败（${res.statusCode}）`, 
        icon: 'none' 
      })
    }
  } catch (error) {
    console.error('验证码请求错误：', error)
    uni.showToast({ title: '网络错误', icon: 'none' })
  }
}

const toggleAgree = (e) => {
  console.log('checkbox change event:', e)
  
  if (typeof e.detail.value === 'boolean') {
    agreed.value = e.detail.value
  } else if (Array.isArray(e.detail.value)) {
    agreed.value = e.detail.value.length > 0
  } else {
    agreed.value = !agreed.value
  }
  
  console.log('协议状态更新为：', agreed.value)
}

// pages/login/login.vue
const startJourney = async () => {
  console.log('登录点击 - 协议状态:', agreed.value)
  
  if (!phone.value || !code.value) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' })
    return
  }
  
  if (!agreed.value) {
    uni.showToast({ title: '请同意用户协议', icon: 'none' })
    return
  }
  
  try {
    const res = await uni.request({
      url: `${API_BASE}/api/login/code`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: { 
        phone: phone.value.trim(),
        code: code.value.trim()
      }
    })
    
    console.log('登录响应完整对象：', res)
    
    if (res.statusCode === 200 && res.data && res.data.success) {
      // 🔴 重要：保存 token 和用户信息
      if (res.data.token) {
        uni.setStorageSync('token', res.data.token)
        console.log('token已保存:', res.data.token)
      }
      if (res.data.user) {
        uni.setStorageSync('user', res.data.user)
        console.log('用户信息已保存:', res.data.user)
      }
      
      // 同时保存一个登录状态标志
      uni.setStorageSync('isLoggedIn', true)
      
      uni.showToast({ title: '登录成功', icon: 'success' })
      
      // 延迟跳转到首页
      setTimeout(() => {
        uni.switchTab({ url: '/pages/home/home' })
      }, 1000)
    } else {
      const errorMsg = res.data?.message || 
                      (res.statusCode === 400 ? '验证码错误或已过期' : 
                       res.statusCode === 404 ? '用户不存在' : 
                       `请求失败（${res.statusCode}）`)
      uni.showToast({ 
        title: errorMsg, 
        icon: 'none',
        duration: 3000
      })
    }
  } catch (error) {
    console.error('登录请求失败详情：', error)
    uni.showToast({ 
      title: '网络连接失败，请检查服务器是否运行', 
      icon: 'none',
      duration: 3000
    })
  }
}
</script>

<style lang="scss">
.login-container {
  height: 100vh;
  background-image: url('/static/bg/bg4.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 40rpx;
  box-sizing: border-box;
}

.login-content {
  background-color: rgba(255, 255, 255, 0.65); /* 减小 alpha 值，增加透明度 */
   padding: 40px 50px;
   border-radius: 20px;
   box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
   text-align: center;
   width: 95%;
   height: 78%;
   max-width: 420px;
   box-sizing: border-box;
 
}
.logo h1 {
  font-size: 45px;
  font-family: "Times New Roman", "Songti SC", serif;
  color: #2c3e50;
  margin-bottom: 10px;
  letter-spacing: 2px;
  font-weight: 700;
}

.slogan {
}

.slogan p {
  font-size: 18px;
  line-height: 1.6;
  color: #34495e;
  margin: 5px 0;
  font-weight: 500;
  font-family:  "Microsoft YaHei";
}

.subtitle {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.subtitle p {
  font-size: 15px;
  color: #7f8c8d;
}

.input-group {
  width: 100%;
  margin-bottom: 40rpx;
}

.label {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.input-field {
  height: 100rpx;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 70rpx;
  padding: 0 40rpx;
  font-size: 28rpx;
  color: #333;
  box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
}

.code-wrapper {
  display: flex;
  align-items: center;
}

.code-input {
  flex: 1;
  margin-right: 20rpx;
  
}
.custom-checkbox {
  width: 36rpx;
  height: 36rpx;
  border: 2rpx solid #ccc;
  border-radius: 6rpx;
  margin-right: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-checkbox.checked {
  border-color: #f99337;
  background-color: #f99337;
}

.checkmark {
  color: white;
  font-size: 24rpx;
  font-weight: bold;
}

.agreement {
  display: flex;
  align-items: center;
  margin-bottom: 60rpx;
  font-size: 28rpx;
}



.get-code-btn {
  width: 180rpx;
  height: 100rpx;
  line-height: 100rpx;
  padding-left: 20rpx;
  background:#fffbf4 ;
  color:  #1aa6be;
  border: #565f60 5rpx;
  border-radius: 70rpx;
  font-size: 25rpx;
  text-align: left;
  
}

.login-btn {
  width: 80%;
  height: 100rpx;
  line-height: 100rpx;
  background: linear-gradient(to right, #f6c35b, #f99337);
  color: #fff;
  font-size: 33rpx;
  border-radius: 50rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 8rpx 20rpx rgba(108, 92, 231, 0.3);
}

.agreement {
  display: flex;
  align-items: center;
  margin-bottom: 60rpx;
  font-size: 28rpx;

}

.checkbox {
  margin-right: 20rpx;
  transform: scale(1.2);
  background-color: #eee;
  color: #333;
}

.agreement-text {
  color: #6f6f6f;
}

.third-party {
  width: 100%;
  text-align: center;

}

.third-title {
  font-size: 28rpx;
  color: #999;
  margin-top: 20rpx;
  margin-bottom: 10rpx;

}

.icons {
  position: absolute;
  bottom:250rpx;
  left: 36%;
  display: flex;
  justify-content: center;
  gap: 50rpx;
}

.icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.1);
}
</style>