<template>
  <view class="container">
    <view class="card">
      <view class="section-title">👨‍👩‍👧 已绑定家属</view>
      <view v-if="members.length === 0" class="empty-tip">暂无家属信息</view>
      <view v-for="m in members" :key="m.id" class="member-item">
        <view class="member-info">
          <text class="member-name">{{ m.name }}</text>
          <text class="member-detail">{{ m.relation || '关系未填' }} · {{ m.phone || '电话未填' }}</text>
        </view>
        <button class="btn-del" @click="deleteMember(m)">删除</button>
      </view>
    </view>

    <!-- 添加表单 -->
    <view class="card">
      <view class="section-title">➕ 添加家属</view>
      <view class="form-item">
        <text class="form-label">姓名 *</text>
        <input v-model="form.name" class="form-input" placeholder="请输入家属姓名" />
      </view>
      <view class="form-item">
        <text class="form-label">关系</text>
        <input v-model="form.relation" class="form-input" placeholder="如：配偶、子女、父母" />
      </view>
      <view class="form-item">
        <text class="form-label">手机号</text>
        <input v-model="form.phone" class="form-input" type="number" placeholder="请输入手机号" />
      </view>
      <button class="btn-add" :disabled="adding" @click="addMember">
        {{ adding ? '添加中...' : '✅ 添加家属' }}
      </button>
    </view>
  </view>
</template>

<script>
import { get, post, del } from '@/utils/request.js';

export default {
  data() {
    return {
      members: [],
      form: { name: '', relation: '', phone: '' },
      adding: false,
    };
  },
  onLoad() {
    this.loadMembers();
  },
  onShow() {
    this.loadMembers();
  },
  methods: {
    async loadMembers() {
      try {
        const res = await get('/family');
        this.members = res.items || [];
      } catch (e) {}
    },
    async addMember() {
      if (!this.form.name.trim()) {
        uni.showToast({ title: '请填写家属姓名', icon: 'none' });
        return;
      }
      this.adding = true;
      try {
        await post('/family', {
          name: this.form.name.trim(),
          relation: this.form.relation.trim() || null,
          phone: this.form.phone.trim() || null,
        });
        uni.showToast({ title: '家属已添加', icon: 'success' });
        this.form = { name: '', relation: '', phone: '' };
        await this.loadMembers();
      } catch (e) {
      } finally {
        this.adding = false;
      }
    },
    deleteMember(m) {
      uni.showModal({
        title: '确认删除',
        content: `确定删除家属「${m.name}」吗？`,
        success: async (res) => {
          if (res.confirm) {
            try {
              await del(`/family/${m.id}`);
              uni.showToast({ title: '已删除', icon: 'success' });
              await this.loadMembers();
            } catch (e) {}
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

.empty-tip {
  display: block;
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  padding: 30rpx 0;
}

.member-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  .member-info {
    flex: 1;

    .member-name {
      display: block;
      font-size: 30rpx;
      font-weight: 600;
      color: #333;
    }

    .member-detail {
      display: block;
      font-size: 24rpx;
      color: #aaa;
      margin-top: 6rpx;
    }
  }

  .btn-del {
    background: #fff;
    color: #f44336;
    border: 2rpx solid #f44336;
    border-radius: 30rpx;
    padding: 8rpx 24rpx;
    font-size: 24rpx;
    height: auto;
    line-height: 1.6;
  }
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
}

.btn-add {
  background: #4caf50;
  color: #fff;
  border-radius: 44rpx;
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  font-size: 30rpx;
  font-weight: 600;
  width: 100%;
  border: none;
}
</style>
