import BASE_URL from './config.js';

/**
 * 统一请求封装
 * - 自动附加 Authorization: Bearer <token> 头
 * - 401 时自动跳转登录页
 */
function request(options) {
  const token = uni.getStorageSync('token');
  const header = {
    'Content-Type': 'application/json',
    ...(options.header || {}),
  };
  if (token) {
    header['Authorization'] = `Bearer ${token}`;
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header,
      success(res) {
        if (res.statusCode === 401) {
          uni.removeStorageSync('token');
          uni.removeStorageSync('patient');
          uni.reLaunch({ url: '/pages/login/index' });
          return reject(new Error('未授权，请重新登录'));
        }
        if (res.statusCode >= 200 && res.statusCode < 300) {
          return resolve(res.data);
        }
        const msg = (res.data && res.data.message) || `请求失败(${res.statusCode})`;
        uni.showToast({ title: msg, icon: 'none' });
        return reject(new Error(msg));
      },
      fail(err) {
        uni.showToast({ title: '网络错误，请检查连接', icon: 'none' });
        reject(err);
      },
    });
  });
}

export const get = (url, data) => request({ url, method: 'GET', data });
export const post = (url, data) => request({ url, method: 'POST', data });
export const put = (url, data) => request({ url, method: 'PUT', data });
export const del = (url) => request({ url, method: 'DELETE' });

export default request;
