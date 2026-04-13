<template>
  <view class="login-page">
    <!-- 顶部品牌区 -->
    <view class="brand-area">
      <view class="brand-icon">🩺</view>
      <text class="brand-title">糖尿病管理</text>
      <text class="brand-sub">患者健康管理平台</text>
    </view>

    <!-- 登录表单 -->
    <view class="form-card">
      <view class="form-title">患者登录</view>

      <view class="form-item">
        <text class="form-label">手机号</text>
        <input
          v-model="phone"
          class="form-input"
          type="number"
          placeholder="请输入手机号"
          maxlength="11"
        />
      </view>

      <view class="form-item">
        <text class="form-label">密码</text>
        <input
          v-model="password"
          class="form-input"
          type="password"
          placeholder="请输入密码"
        />
      </view>

      <button class="btn-login" :disabled="loading" @click="handleLogin">
        {{ loading ? '登录中...' : '登 录' }}
      </button>
    </view>
  </view>
</template>

<script>
import { post } from '@/utils/request.js';

export default {
  data() {
    return {
      phone: '',
      password: '',
      loading: false,
    };
  },
  onLoad() {
    // 已登录则直接跳首页
    const token = uni.getStorageSync('token');
    if (token) {
      uni.switchTab({ url: '/pages/home/index' });
    }
  },
  methods: {
    async handleLogin() {
      if (!this.phone || !this.password) {
        uni.showToast({ title: '请填写手机号和密码', icon: 'none' });
        return;
      }
      this.loading = true;
      try {
        const res = await post('/login', { phone: this.phone, password: this.password });
        uni.setStorageSync('token', res.token);
        uni.setStorageSync('patient', JSON.stringify(res.patient));
        uni.switchTab({ url: '/pages/home/index' });
      } catch (e) {
        // 错误已在 request.js 中 showToast
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="scss">
.login-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #43a047 0%, #a5d6a7 60%, #f5f5f5 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 120rpx;
}

.brand-area {
  text-align: center;
  margin-bottom: 60rpx;

  .brand-icon {
    font-size: 100rpx;
    display: block;
  }

  .brand-title {
    display: block;
    font-size: 48rpx;
    font-weight: 700;
    color: #fff;
    margin-top: 20rpx;
  }

  .brand-sub {
    display: block;
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.85);
    margin-top: 10rpx;
  }
}

.form-card {
  width: 680rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 50rpx 40rpx;
  box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.12);

  .form-title {
    font-size: 36rpx;
    font-weight: 700;
    color: #333;
    margin-bottom: 40rpx;
    text-align: center;
  }

  .form-item {
    margin-bottom: 30rpx;

    .form-label {
      display: block;
      font-size: 28rpx;
      color: #666;
      margin-bottom: 12rpx;
    }

    .form-input {
      width: 100%;
      height: 88rpx;
      border: 2rpx solid #e0e0e0;
      border-radius: 12rpx;
      padding: 0 24rpx;
      font-size: 30rpx;
      color: #333;
      box-sizing: border-box;
    }
  }

  .btn-login {
    margin-top: 40rpx;
    background: #4caf50;
    color: #fff;
    border-radius: 44rpx;
    height: 96rpx;
    line-height: 96rpx;
    text-align: center;
    font-size: 34rpx;
    font-weight: 600;
    width: 100%;
    border: none;
    letter-spacing: 4rpx;
  }
}
</style>
