<template>
  <view class="container">
    <!-- 头像信息卡 -->
    <view class="profile-header">
      <view class="avatar">{{ (patient.name || '?')[0] }}</view>
      <text class="profile-name">{{ patient.name || '-' }}</text>
      <text class="profile-phone">{{ patient.phone || '' }}</text>
    </view>

    <!-- 个人信息 -->
    <view class="card">
      <view class="section-title">👤 个人信息</view>
      <view v-if="!editing">
        <view class="info-row"><text class="info-label">姓名</text><text class="info-val">{{ patient.name || '-' }}</text></view>
        <view class="info-row"><text class="info-label">性别</text><text class="info-val">{{ genderLabel(patient.gender) }}</text></view>
        <view class="info-row"><text class="info-label">年龄</text><text class="info-val">{{ patient.age ? patient.age + ' 岁' : '-' }}</text></view>
        <view class="info-row"><text class="info-label">手机号</text><text class="info-val">{{ patient.phone || '-' }}</text></view>
        <view class="info-row"><text class="info-label">地址</text><text class="info-val">{{ patient.address || '-' }}</text></view>
        <view class="info-row"><text class="info-label">糖尿病类型</text><text class="info-val">{{ patient.diabetes_type || '-' }}</text></view>
        <button class="btn-edit" @click="startEdit">✏️ 编辑信息</button>
      </view>

      <!-- 编辑表单 -->
      <view v-else>
        <view class="form-item">
          <text class="form-label">姓名</text>
          <input v-model="form.name" class="form-input" placeholder="请输入姓名" />
        </view>
        <view class="form-item">
          <text class="form-label">性别</text>
          <picker :range="genderOptions" :range-key="'label'" @change="onGenderChange">
            <view class="picker-view">{{ selectedGenderLabel || '请选择性别' }}</view>
          </picker>
        </view>
        <view class="form-item">
          <text class="form-label">年龄</text>
          <input v-model="form.age" class="form-input" type="number" placeholder="请输入年龄" />
        </view>
        <view class="form-item">
          <text class="form-label">手机号</text>
          <input v-model="form.phone" class="form-input" type="number" placeholder="请输入手机号" />
        </view>
        <view class="form-item">
          <text class="form-label">地址</text>
          <input v-model="form.address" class="form-input" placeholder="请输入地址" />
        </view>
        <view class="form-item">
          <text class="form-label">糖尿病类型</text>
          <input v-model="form.diabetes_type" class="form-input" placeholder="如：2型糖尿病" />
        </view>
        <view class="btn-row">
          <button class="btn-cancel" @click="editing = false">取消</button>
          <button class="btn-save" :disabled="saving" @click="saveProfile">
            {{ saving ? '保存中...' : '保 存' }}
          </button>
        </view>
      </view>
    </view>

    <!-- 快捷功能 -->
    <view class="card">
      <view class="section-title">🔧 功能</view>
      <view class="menu-item" @click="goFamily">
        <text>👨‍👩‍👧 家属绑定管理</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @click="goReminders">
        <text>🔔 健康提醒列表</text>
        <text class="arrow">›</text>
      </view>
    </view>

    <!-- 退出 -->
    <button class="btn-logout" @click="logout">退出登录</button>
  </view>
</template>

<script>
import { get, put } from '@/utils/request.js';

export default {
  data() {
    return {
      patient: {},
      editing: false,
      saving: false,
      form: {},
      genderOptions: [
        { label: '男', value: 'male' },
        { label: '女', value: 'female' },
        { label: '其他', value: 'other' },
      ],
      selectedGenderLabel: '',
    };
  },
  onLoad() {
    this.loadProfile();
  },
  onShow() {
    this.loadProfile();
  },
  methods: {
    async loadProfile() {
      try {
        const cached = uni.getStorageSync('patient');
        if (cached) this.patient = JSON.parse(cached);
        const res = await get('/me');
        this.patient = res;
        uni.setStorageSync('patient', JSON.stringify(res));
      } catch (e) {}
    },
    startEdit() {
      this.form = { ...this.patient };
      const g = this.genderOptions.find(o => o.value === this.patient.gender);
      this.selectedGenderLabel = g ? g.label : '';
      this.editing = true;
    },
    onGenderChange(e) {
      const idx = e.detail.value;
      this.form.gender = this.genderOptions[idx].value;
      this.selectedGenderLabel = this.genderOptions[idx].label;
    },
    async saveProfile() {
      this.saving = true;
      try {
        const payload = {
          name: this.form.name,
          gender: this.form.gender,
          age: this.form.age ? parseInt(this.form.age) : null,
          phone: this.form.phone,
          address: this.form.address,
          diabetes_type: this.form.diabetes_type,
        };
        const res = await put('/me', payload);
        this.patient = res;
        uni.setStorageSync('patient', JSON.stringify(res));
        this.editing = false;
        uni.showToast({ title: '个人信息已更新', icon: 'success' });
      } catch (e) {
      } finally {
        this.saving = false;
      }
    },
    genderLabel(g) {
      const map = { male: '男', female: '女', other: '其他' };
      return map[g] || '-';
    },
    goFamily() {
      uni.navigateTo({ url: '/pages/family/index' });
    },
    goReminders() {
      uni.navigateTo({ url: '/pages/reminders/index' });
    },
    logout() {
      uni.showModal({
        title: '确认退出',
        content: '确定要退出登录吗？',
        success(res) {
          if (res.confirm) {
            uni.removeStorageSync('token');
            uni.removeStorageSync('patient');
            uni.reLaunch({ url: '/pages/login/index' });
          }
        },
      });
    },
  },
};
</script>

<style lang="scss">
.container {
  padding: 20rpx;
}

.profile-header {
  background: linear-gradient(135deg, #4caf50, #81c784);
  border-radius: 20rpx;
  padding: 40rpx 30rpx;
  text-align: center;
  margin-bottom: 20rpx;

  .avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56rpx;
    color: #fff;
    font-weight: 700;
    margin: 0 auto 16rpx;
  }

  .profile-name {
    display: block;
    font-size: 36rpx;
    font-weight: 700;
    color: #fff;
  }

  .profile-phone {
    display: block;
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.85);
    margin-top: 8rpx;
  }
}

.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  margin-bottom: 20rpx;
}

.info-row {
  display: flex;
  padding: 18rpx 0;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-of-type {
    border-bottom: none;
  }

  .info-label {
    width: 160rpx;
    font-size: 28rpx;
    color: #999;
  }

  .info-val {
    flex: 1;
    font-size: 28rpx;
    color: #333;
  }
}

.btn-edit {
  margin-top: 24rpx;
  background: #e8f5e9;
  color: #4caf50;
  border: 2rpx solid #4caf50;
  border-radius: 44rpx;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 28rpx;
  width: 100%;
}

.form-item {
  margin-bottom: 20rpx;

  .form-label {
    display: block;
    font-size: 26rpx;
    color: #666;
    margin-bottom: 8rpx;
  }

  .form-input {
    width: 100%;
    height: 80rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 10rpx;
    padding: 0 20rpx;
    font-size: 28rpx;
    color: #333;
    box-sizing: border-box;
  }

  .picker-view {
    height: 80rpx;
    line-height: 80rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 10rpx;
    padding: 0 20rpx;
    font-size: 28rpx;
    color: #999;
  }
}

.btn-row {
  display: flex;
  gap: 20rpx;
  margin-top: 20rpx;

  .btn-cancel {
    flex: 1;
    height: 80rpx;
    line-height: 80rpx;
    background: #f5f5f5;
    color: #666;
    border-radius: 44rpx;
    font-size: 28rpx;
    border: none;
  }

  .btn-save {
    flex: 1;
    height: 80rpx;
    line-height: 80rpx;
    background: #4caf50;
    color: #fff;
    border-radius: 44rpx;
    font-size: 28rpx;
    border: none;
  }
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
  font-size: 30rpx;
  color: #333;

  &:last-child {
    border-bottom: none;
  }

  .arrow {
    color: #aaa;
    font-size: 36rpx;
  }
}

.btn-logout {
  background: #fff;
  color: #f44336;
  border: 2rpx solid #f44336;
  border-radius: 44rpx;
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  font-size: 30rpx;
  width: 100%;
  margin-top: 10rpx;
}
</style>
