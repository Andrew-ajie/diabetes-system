<template>
  <view class="chat-page">
    <!-- 消息列表 -->
    <scroll-view
      class="msg-list"
      scroll-y
      :scroll-top="scrollTop"
      scroll-with-animation
    >
      <view v-if="!messages.length" class="empty-tip">暂无消息，发送第一条消息吧～</view>
      <view
        v-for="msg in messages"
        :key="msg.id"
        class="msg-row"
        :class="msg.sender === 'patient' ? 'msg-right' : 'msg-left'"
      >
        <view v-if="msg.sender !== 'patient'" class="avatar avatar-doctor">👨‍⚕️</view>
        <view class="bubble-wrap">
          <view class="bubble" :class="msg.sender === 'patient' ? 'bubble-self' : 'bubble-other'">
            {{ msg.content }}
          </view>
          <text class="msg-time">{{ formatTime(msg.created_at) }}</text>
        </view>
        <view v-if="msg.sender === 'patient'" class="avatar avatar-patient">🙋</view>
      </view>
      <!-- 占位，确保最后一条消息不被输入框遮挡 -->
      <view style="height: 140rpx;" />
    </scroll-view>

    <!-- 输入区 -->
    <view class="input-bar">
      <input
        v-model="inputText"
        class="chat-input"
        placeholder="请输入消息..."
        confirm-type="send"
        @confirm="sendMsg"
      />
      <button class="send-btn" :disabled="sending" @click="sendMsg">发送</button>
    </view>
  </view>
</template>

<script>
import { get, post } from '@/utils/request.js';

export default {
  data() {
    return {
      messages: [],
      inputText: '',
      sending: false,
      scrollTop: 0,
      page: 1,
      total: 0,
    };
  },
  onLoad() {
    this.loadMessages();
  },
  onShow() {
    this.loadMessages();
  },
  methods: {
    async loadMessages() {
      try {
        const res = await get('/consultation?page=1&page_size=100');
        this.messages = res.items || [];
        this.total = res.total || 0;
        this.$nextTick(() => {
          this.scrollTop = 9999999;
        });
      } catch (e) {}
    },
    async sendMsg() {
      const content = this.inputText.trim();
      if (!content) return;
      if (this.sending) return;
      this.sending = true;
      try {
        await post('/consultation', { content });
        this.inputText = '';
        await this.loadMessages();
      } catch (e) {
      } finally {
        this.sending = false;
      }
    },
    formatTime(iso) {
      if (!iso) return '';
      return iso.replace('T', ' ').slice(0, 16);
    },
  },
};
</script>

<style lang="scss">
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f4f0;
}

.msg-list {
  flex: 1;
  padding: 20rpx;
  overflow-y: auto;
}

.empty-tip {
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  padding: 80rpx 0;
}

.msg-row {
  display: flex;
  align-items: flex-end;
  margin-bottom: 28rpx;

  &.msg-right {
    flex-direction: row-reverse;
  }

  &.msg-left {
    flex-direction: row;
  }
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: #e8f5e9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  flex-shrink: 0;

  &.avatar-doctor {
    background: #e3f2fd;
  }

  &.avatar-patient {
    background: #e8f5e9;
  }
}

.bubble-wrap {
  max-width: 64%;
  margin: 0 12rpx;

  .bubble {
    padding: 20rpx 28rpx;
    border-radius: 20rpx;
    font-size: 30rpx;
    line-height: 1.5;
    word-break: break-all;

    &.bubble-self {
      background: #4caf50;
      color: #fff;
      border-bottom-right-radius: 4rpx;
    }

    &.bubble-other {
      background: #fff;
      color: #333;
      border-bottom-left-radius: 4rpx;
    }
  }

  .msg-time {
    display: block;
    font-size: 20rpx;
    color: #aaa;
    text-align: right;
    margin-top: 6rpx;
  }
}

.input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16rpx 24rpx;
  background: #fff;
  border-top: 1rpx solid #eee;
  display: flex;
  align-items: center;
  gap: 16rpx;

  .chat-input {
    flex: 1;
    height: 80rpx;
    background: #f5f5f5;
    border-radius: 40rpx;
    padding: 0 24rpx;
    font-size: 28rpx;
    color: #333;
  }

  .send-btn {
    background: #4caf50;
    color: #fff;
    border-radius: 40rpx;
    height: 80rpx;
    line-height: 80rpx;
    padding: 0 32rpx;
    font-size: 28rpx;
    border: none;
    flex-shrink: 0;
  }
}
</style>
