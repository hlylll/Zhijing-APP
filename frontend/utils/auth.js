// utils/auth.js
export const auth = {
  // 检查是否已登录
  isLoggedIn() {
    const token = uni.getStorageSync('token')
    const isLoggedIn = uni.getStorageSync('isLoggedIn')
    return !!(token && isLoggedIn)
  },
  
  // 获取token
  getToken() {
    return uni.getStorageSync('token')
  },
  
  // 获取用户信息
  getUser() {
    return uni.getStorageSync('user')
  },
  
  // 退出登录
  logout() {
    uni.removeStorageSync('token')
    uni.removeStorageSync('user')
    uni.removeStorageSync('isLoggedIn')
    uni.removeStorageSync('userInfo')
    
    uni.reLaunch({
      url: '/pages/login/login'
    })
  },
  
  // 跳转到登录页（如果需要）
  requireAuth() {
    if (!this.isLoggedIn()) {
      uni.reLaunch({
        url: '/pages/login/login'
      })
      return false
    }
    return true
  }
}