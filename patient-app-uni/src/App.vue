<script>
export default {
  onLaunch() {
    const token = uni.getStorageSync('token');
    if (!token) {
      uni.reLaunch({ url: '/pages/login/index' });
    }
  },
  onShow() {},
  onHide() {},
};
</script>

<style lang="scss">
@import './uni.scss';

page {
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.container {
  padding: 20rpx;
}

.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.btn-primary {
  background: #4caf50;
  color: #fff;
  border-radius: 12rpx;
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: 600;
  width: 100%;
  border: none;
}

.btn-danger {
  background: #f44336;
  color: #fff;
  border-radius: 12rpx;
  padding: 12rpx 28rpx;
  font-size: 26rpx;
  border: none;
}

.btn-outline {
  background: transparent;
  color: #4caf50;
  border: 2rpx solid #4caf50;
  border-radius: 12rpx;
  padding: 12rpx 28rpx;
  font-size: 26rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  margin-bottom: 20rpx;
}

.empty-tip {
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  padding: 60rpx 0;
}
</style>
