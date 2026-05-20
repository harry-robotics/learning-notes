# Day 6: NTP 时间同步 + OLED 真实时钟

> 学习日期: 2026-05-18  
> 核心: NTP 协议入门 + time.h 标准库 + struct tm + strftime + WiFi/OLED 整合

---

## 1. 为什么需要 NTP?

### 1.1 ESP32 没有"时间"概念
回顾 Day 4 的 OLED 时钟用 `millis()` 计时:
- 每次重启时间归零, 显示的是"开机 1234 秒"而不是真实时间
- 没有日期概念, 做不了"今天 8 点开灯"
- 长时间运行有累积误差, 一周可能差 10 多秒

### 1.2 三种时间方案对比
| 方案 | 原理 | 优点 | 缺点 |
|---|---|---|---|
| RTC 芯片 | DS3231 等带电池芯片硬件计时 | 准, 断电也跑 | 要硬件成本 |
| **NTP** | 联网从时间服务器拿当前时间 | **零硬件成本** | 断网就废 |
| 手动设置 | 启动时输入时间 | — | 弱智, 没人用 |

ESP32 自带 WiFi → **NTP 是最优解**。

### 1.3 NTP 是什么 (简要)
- 全称: **Network Time Protocol**, 网络时间协议
- 工作原理: ESP32 向时间服务器发请求, 服务器返回 UTC 时间戳
- 我只需要懂的部分: **调用 configTime 一行配好**, 底层全自动

---

## 2. ESP32 时间相关 API

### 2.1 configTime() — 一行配置 NTP
```cpp
configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
```

| 参数 | 含义 | 中国的值 |
|---|---|---|
| gmtOffset_sec | 时区偏移(秒) | 8 * 3600 = 28800 (东8区) |
| daylightOffset_sec | 夏令时偏移 | 0 (中国不用) |
| ntpServer | 服务器地址 | "ntp.aliyun.com" |

### 2.2 time_t 与 Unix 时间戳
- **Unix 时间戳**: 从 1970-01-01 00:00:00 UTC 算起的总秒数
- 本质类型: `long` (64 位 8 字节)
- 为什么用这种格式: 跨语言通用、计算简单(直接相减)、单个整数表示所有时间

### 2.3 struct tm 结构体 (两大坑!)
| 字段 | 范围 | 注意点 |
|---|---|---|
| tm_sec | 0-59 | 秒 |
| tm_min | 0-59 | 分 |
| tm_hour | 0-23 | 时 |
| tm_mday | 1-31 | 日 |
| **tm_mon** | **0-11** | **⚠️ 月份从 0 开始, 5 月 = 4!** |
| **tm_year** | 年-1900 | **⚠️ 2026 年存的是 126!** |
| tm_wday | 0-6 | 0=Sunday |
| tm_yday | 0-365 | 一年第几天 |

这两个坑是 C 标准库 1972 年定的, 改不动了, **全世界程序员都骂过**。

### 2.4 getLocalTime(&timeinfo) — 输出参数模式
```cpp
struct tm timeinfo;
if (getLocalTime(&timeinfo)) {
  // 成功, timeinfo 已被填充
}
```
- `&timeinfo` 是**取地址**, 传指针进去
- 函数内部**通过指针修改你的结构体**
- 这是 C 语言"输出参数"模式: 想返回复杂数据时, 让你先声明再传地址

### 2.5 strftime() 常用格式符
```cpp
char buf[64];
strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &timeinfo);
// 结果: "2026-05-18 15:30:45"
```

| 格式符 | 含义 | 示例 |
|---|---|---|
| %Y | 4位年 | 2026 |
| %m | 2位月 | 05 |
| %d | 2位日 | 18 |
| %H | 24小时制 | 15 |
| %M | 分 | 30 |
| %S | 秒 | 45 |
| %A | 完整星期名 | Monday |
| %a | 缩写星期 | Mon |

好处: 自动处理"补零"、"月份+1"、"年份+1900" 这些坑。

---

## 3. 指针知识入门 (Day 6 专项)

### 3.1 输出参数模式
```cpp
struct tm timeinfo;          // 声明空结构体
getLocalTime(&timeinfo);     // 传地址,函数填充
strftime(buf, 64, "%Y", &timeinfo);  // 同理
```
**为什么不直接 return 结构体**: 复制开销大, C 语言习惯传指针。

### 3.2 -> 与 (*ptr). 关系
- `指针->成员` 等价于 `(*指针).成员`
- 比如函数内部: `ptr->tm_year = 126;`

### 3.3 const char* 字符串数组
```cpp
const char* WEEKDAYS[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
```
- 7 个元素, 每个是一个字符串指针
- `WEEKDAYS[1]` 返回 "Mon" 的地址

---

## 4. Day 6 完整代码

```cpp
#include <WiFi.h>
#include <time.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// WiFi 配置
const char* WIFI_SSID = "你的WiFi名";
const char* WIFI_PASSWORD = "你的WiFi密码";
const unsigned long WIFI_TIMEOUT = 10000;

// NTP 配置
const char* NTP_SERVER = "ntp.aliyun.com";
const long GMT_OFFSET_SEC = 8 * 3600;
const int DAYLIGHT_OFFSET_SEC = 0;

// OLED 配置
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long lastUpdate = 0;
const unsigned long UPDATE_INTERVAL = 1000;
const char* WEEKDAYS[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};

bool connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime >= WIFI_TIMEOUT) return false;
    delay(500);
  }
  Serial.printf("[WiFi] IP: %s\n", WiFi.localIP().toString().c_str());
  return true;
}

bool syncTimeFromNTP() {
  configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, NTP_SERVER);
  
  struct tm timeinfo;
  unsigned long startTime = millis();
  while (!getLocalTime(&timeinfo)) {
    if (millis() - startTime >= 10000) return false;
    delay(500);
  }
  
  char buf[64];
  strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S %A", &timeinfo);
  Serial.printf("[NTP] 同步成功: %s\n", buf);
  return true;
}

void displayTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Time NOT synced");
    display.display();
    return;
  }
  
  char dateBuf[16], timeBuf[16];
  strftime(dateBuf, sizeof(dateBuf), "%Y-%m-%d", &timeinfo);
  strftime(timeBuf, sizeof(timeBuf), "%H:%M:%S", &timeinfo);
  
  display.clearDisplay();
  display.setTextSize(1);  display.setCursor(0, 0);  display.println(dateBuf);
  display.setTextSize(2);  display.setCursor(0, 20); display.println(timeBuf);
  display.setTextSize(1);  display.setCursor(0, 50);
  display.print("Day: ");
  display.println(WEEKDAYS[timeinfo.tm_wday]);
  display.display();
}

void setup() {
  Serial.begin(115200);
  delay(100);
  
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("[OLED] 初始化失败");
    while (1);
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  
  if (!connectWiFi()) return;
  if (!syncTimeFromNTP()) return;
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = currentMillis;
    displayTime();
  }
}
```

### 代码工程亮点
| 设计 | 思想 |
|---|---|
| 配置区分块 (WiFi/NTP/OLED) | 改一处即可 |
| 把每个流程封装成函数 | 复用 + 可读 |
| 每步都有 fail 分支 | 鲁棒性 |
| OLED 显示错误状态 | 用户体验 |
| 每秒刷新 (millis 减法形式) | Day 4 模板 |

---

## 5. 工程整合: WiFi + NTP + OLED 启动流程
1. OLED 初始化 → 失败死循环报错
2. WiFi 连接 → 失败 return
3. NTP 同步 → 失败 return
4. 进入循环刷新

---

## 6. 易错点
| 坑 | 现象 | 解决 |
|---|---|---|
| tm_mon 当 1-12 月用 | 月份永远错 1 | 记住从 0 开始 |
| tm_year 当 2026 用 | 显示 3926 年 | 加 1900 才是真年份 |
| 忘记 #include <time.h> | 编译报 struct tm 找不到 | 必加 |
| 同步前调用 getLocalTime | 返回 1970 年 | 等同步成功 |
| 没设时区直接拿时间 | 拿到 UTC, 差 8 小时 | configTime 第一参数设对 |

---

## 7. 思考题闭环

### Q1: 指针专项
- 不能写 `getLocalTime(timeinfo)`: 编译报错, 类型不匹配
- `getLocalTime` 内部对 timeinfo: **写**(填充各字段)
- `strftime` 内部对 timeinfo: **读**(读出年月日格式化到 buf)

### Q2: NTP 失败时的鲁棒性
- 当前代码: setup return 后 loop 仍跑, 但 OLED 显示 "Time NOT synced"
- 不够理想: 没有重试机制
- 改进: loop 里定期尝试 syncTimeFromNTP(), 用 millis 减法

### Q3: Unix 时间戳粗算
- 2026-05-18 15:30:45 北京 = 2026-05-18 07:30:45 UTC
- 距 1970 约 56 年 × 365.25 × 86400 ≈ 17.7 亿秒
- tm_year = 126, tm_mon = 4
- printf 写法: `printf("%d-%02d-%02d", year+1900, mon+1, mday);`

---

## 8. Day 6 四象限知识分类

### 🔧 操作 - 必须熟练 (高频)
- `configTime(...)` 一行配 NTP
- `getLocalTime(&timeinfo)` 取时间
- `strftime(buf, size, fmt, &tm)` 格式化
- 输出参数模式 `func(&myStruct)`

### 🛠️ 操作 - 跟一遍即可 (低频)
- 切换不同 NTP 服务器 (阿里云/谷歌/苹果)
- 调试时手动设置时间
- 出国时改时区偏移

### 🧠 知识 - 重点记忆 (理论核心)
- **tm_mon 是 0-11, tm_year 是 -1900 偏移** ⚠️
- NTP 是 ESP32 拿真实时间的标准方法
- Unix 时间戳的本质 (1970 起秒数)
- 输出参数模式 (传地址让函数填)
- `->` 是指针访问成员

### 📚 知识 - 不必死记 (百度即得)
- NTP 协议底层 (UDP 端口 123 / SNTP)
- Stratum 1/2/3 层级
- 所有 strftime 格式符
- struct tm 其他字段
- 不同时区的具体偏移值

---

*Last updated: 2026-5-20*