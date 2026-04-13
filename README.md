# 糖尿病管理系统 / Diabetes Management System

基于 Flask + MySQL 的糖尿病患者管理系统，支持医生、管理员角色（Web 端），以及患者端 uni-app（H5 + App）移动应用。

A Flask + MySQL diabetes patient management system with doctor/admin web roles and a patient-facing uni-app (H5 + App).

---

## 环境要求 / Requirements

- Python 3.9+
- MySQL 8.0+
- Node.js 18+（运行 uni-app 前端）

---

## 后端安装与启动 / Backend Setup

### 1. 克隆并进入项目目录

```bash
git clone <repository-url>
cd diabetes-system
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. 创建数据库

```sql
CREATE DATABASE diabetes_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际数据库连接信息和密钥
```

`.env` 示例:

```
SECRET_KEY=your-very-secret-key-change-this
DATABASE_URL=mysql+pymysql://root:password@localhost/diabetes_system
GLUCOSE_HIGH=11.1
GLUCOSE_LOW=3.9

# JWT 配置（移动端 API 使用）
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_EXPIRE_DAYS=7
```

> ⚠️ 生产环境请务必设置强随机密钥，不要使用默认值。

### 5. 初始化并填充数据库

```bash
python seed.py
```

### 6. 启动后端

```bash
python run.py
```

后端默认运行在 http://localhost:5000

---

## 患者端 uni-app 前端 / Patient uni-app Frontend

uni-app 项目位于 `patient-app-uni/` 目录，支持 H5（浏览器）和 App 打包。

### 1. 进入前端目录并安装依赖

```bash
cd patient-app-uni
npm install
```

### 2. 配置后端地址

编辑 `src/utils/config.js`，将 `BASE_URL` 修改为后端实际地址：

```js
// 本地开发
const BASE_URL = 'http://127.0.0.1:5000/api/patient';

// 生产环境示例
// const BASE_URL = 'https://your-domain.com/api/patient';
```

### 3. 运行 H5（浏览器中显示手机界面）

```bash
npm run dev:h5
```

浏览器打开 http://localhost:5173（或终端提示的端口），即可看到手机界面。

### 4. 打包 App（Android/iOS）

使用 [HBuilderX](https://www.dcloud.io/hbuilderx.html) 打开 `patient-app-uni/` 目录，选择「运行 → 运行到手机或模拟器」，或「发行 → 原生 App-云打包」。

---

## 患者端功能模块 / Patient App Features

| 模块         | 功能说明                         |
|--------------|----------------------------------|
| 🏠 首页      | 快捷入口、最近血糖、最新提醒      |
| 💬 在线咨询  | 与医生消息聊天（发送 + 历史记录） |
| 📊 数据统计  | 血糖/运动趋势图表 + 分页列表      |
| ✏️ 数据录入  | 血糖录入、运动录入                |
| 👤 我的      | 个人信息查看/编辑、家属绑定、提醒 |
| 👨‍👩‍👧 家属绑定 | 添加/删除家属信息                |
| 🔔 健康提醒  | 医生发布的提醒列表               |

患者默认密码由 `seed.py` 初始化（见演示账号表）。

---

## 患者端 JSON API / Patient JSON API

所有 API 前缀：`/api/patient`，除登录外均需 `Authorization: Bearer <token>` 请求头。

| 路径                          | 方法         | 说明               |
|-------------------------------|--------------|--------------------|
| `/api/patient/login`          | POST         | 手机号+密码登录     |
| `/api/patient/me`             | GET / PUT    | 获取/更新个人信息   |
| `/api/patient/glucose`        | GET / POST   | 血糖记录列表/新增   |
| `/api/patient/glucose/<id>`   | PUT / DELETE | 编辑/删除血糖记录   |
| `/api/patient/exercise`       | GET / POST   | 运动记录列表/新增   |
| `/api/patient/exercise/<id>`  | PUT / DELETE | 编辑/删除运动记录   |
| `/api/patient/reminders`      | GET          | 健康提醒列表        |
| `/api/patient/consultation`   | GET / POST   | 咨询消息列表/发送   |
| `/api/patient/family`         | GET / POST   | 家属列表/新增       |
| `/api/patient/family/<id>`    | DELETE       | 删除家属            |
| `/api/patient/stats/glucose`  | GET          | 血糖统计（周/月）   |
| `/api/patient/stats/exercise` | GET          | 运动统计（周/月）   |

---

## 演示账号 / Demo Accounts

| 角色   | 账号                   | 密码   |
|--------|------------------------|--------|
| 管理员 | admin@123.com          | 123456 |
| 医生1  | Doctor1@123.com        | 123456 |
| 医生2  | Doctor2@123.com        | 123456 |
| 患者   | 见 seed.py 初始化数据  | 123456 |

---

## 路由说明 / Web Routes

### 认证
| 路径       | 方法      | 说明     |
|------------|-----------|----------|
| /login     | GET/POST  | 登录页面 |
| /logout    | GET       | 退出登录 |

### 医生端 (需要登录，doctor 角色)
| 路径                                    | 方法      | 说明               |
|-----------------------------------------|-----------|---------------------|
| /doctor/dashboard                       | GET       | 医生仪表盘          |
| /doctor/patients                        | GET       | 我的患者列表        |
| /doctor/patients/\<id\>                 | GET/POST  | 患者详情及添加记录  |
| /doctor/patients/\<id\>/glucose_data    | GET       | 血糖图表JSON数据    |
| /doctor/reminders                       | GET/POST  | 提醒管理            |

### 管理员端 (需要登录，admin 角色)
| 路径                               | 方法      | 说明             |
|------------------------------------|-----------|------------------|
| /admin/dashboard                   | GET       | 管理员仪表盘     |
| /admin/dashboard/chart_data        | GET       | 图表JSON数据     |
| /admin/users                       | GET/POST  | 用户（医生）管理 |
| /admin/users/\<id\>/reset_password | POST      | 重置医生密码     |
| /admin/patients                    | GET/POST  | 全部患者管理     |
| /admin/patients/\<id\>/edit        | GET/POST  | 编辑患者信息     |

---

## 功能说明 / Features

- **医生端**：查看自己的患者列表，记录血糖和运动数据，通过 Chart.js 折线图查看趋势，创建患者提醒。
- **管理员端**：管理所有医生账号（添加、重置密码），管理所有患者（添加、编辑、分配医生），查看系统统计图表。
- **患者端 App**：uni-app 移动应用，支持 H5 预览和 App 打包，通过 JWT Token 认证调用 JSON API。
- **血糖预警**：血糖值 > 11.1 mmol/L 显示红色预警，< 3.9 mmol/L 显示黄色预警。

---

## 技术栈 / Tech Stack

- **后端**: Flask 3.0, Flask-SQLAlchemy, Flask-Cors, PyJWT, PyMySQL
- **Web前端**: Bootstrap 5, Chart.js 4, Bootstrap Icons
- **移动前端**: uni-app (Vue 3 + Vite)，兼容 H5 / Android / iOS
- **数据库**: MySQL 8.0
