# Day 7: ESP32 HTTP 客户端 + JSON 解析

> 学习日期: 2026-05-19  
> 核心: HTTP 协议入门 + HTTPClient 库 + JSON 数据格式 + ArduinoJson 解析

---

## 1. HTTP 是什么? 【必懂】

### 1.1 一个生活类比
浏览器访问网页背后的协议:
```
客户端 → 服务器: GET /xxx
服务器 → 客户端: 200 OK + 数据
```

### 1.2 ESP32 也能当客户端
- 物联网核心: ESP32 向云端 API 拿数据 / 上报数据
- 应用: 天气、新闻、定位、设备控制

---

## 2. HTTP 请求方法 【必懂】
| 方法 | 用途 | 例子 |
|---|---|---|
| GET | 从服务器拿数据 | 拿天气、拿新闻 |
| POST | 向服务器送数据 | 上传读数、发评论 |
| PUT | 更新数据【了解】 | 修改用户信息 |
| DELETE | 删除数据【了解】 | 删除记录 |

M1 阶段只用 GET 和 POST。

---

## 3. HTTP 状态码 【必背:reasoning - 200/401 必懂含义】
| 状态码 | 含义 | 处理 |
|---|---|---|
| 200 | 成功 | 处理数据 |
| 301/302 | 重定向 | 跟随新 URL |
| 400 | 请求格式错 | 检查你的代码 |
| **401** | **未授权** | **API Key 错或没传** |
| 404 | 找不到 URL | 检查 URL |
| 500 | 服务器错 | 不是你的锅 |

**核心思维: 看到状态码立刻反推问题层级**。

---

## 4. HTTPClient 五件套 【必懂】

```cpp
#include <HTTPClient.h>

HTTPClient http;                       // ① 创建对象
http.begin(client, url);               // ② 设置 URL (HTTPS 要传 client)
http.addHeader("Key 头名", "Key 值");  // ③ 加请求头 (按需,99% API 要)
int code = http.GET();                 // ④ 发请求,返回状态码
String payload = http.getString();     // ⑤ 拿响应
http.end();                            // ⑥ 释放! 必须!
```

**⚠️ 致命坑: 忘 http.end() 会内存泄漏, 几分钟就崩**。

---

## 5. JSON 数据格式 【必懂】

### 5.1 长什么样
```json
{
  "city": "武汉",
  "temperature": 25,
  "weather": "晴",
  "humidity": 60
}
```

### 5.2 嵌套结构
```json
{
  "now": {
    "temp": 25
  },
  "hourly": [
    {"hour": 12, "temp": 26},
    {"hour": 13, "temp": 27}
  ]
}
```

- `{}` 对象, 用 key 访问
- `[]` 数组, 用 index 访问
- 跨语言通用 (Python/JS/C++ 都用)

---

## 6. ArduinoJson 解析三步 【必懂】

```cpp
#include <ArduinoJson.h>

JsonDocument doc;                              // ① 创建文档
deserializeJson(doc, payload);                 // ② 解析字符串
int temp = doc["temp"];                        // ③ 像字典一样访问
```

### 嵌套访问 (剥洋葱) 【必背思路】
```cpp
const char* val = doc["data"][0]["items"][0]["value"];
//                     ↑    ↑       ↑        ↑
//                  对象  数组   嵌套数组  嵌套对象
```

### 解析失败处理
```cpp
DeserializationError error = deserializeJson(doc, payload);
if (error) {
  Serial.printf("解析失败: %s\n", error.c_str());
} else {
  // 提取数据
}
```

**核心思维: 网络请求成功 ≠ JSON 合法。服务器可能返回 HTML 错误页, 必须双重检查**。

---

## 7. HTTPS 注意事项 【了解】

```cpp
WiFiClientSecure client;
client.setInsecure();              // 学习阶段: 不验证证书
HTTPClient http;
http.begin(client, "https://...");
```

⚠️ 生产环境不能 setInsecure(), 要配 CA 证书。M1 不深入。

---

## 8. Day 7 完整代码 (天气获取)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "你的WiFi名";
const char* WIFI_PASSWORD = "你的WiFi密码";
const unsigned long WIFI_TIMEOUT = 10000;

const char* WEATHER_URL = "https://wttr.in/Wuhan?format=j1";
const unsigned long FETCH_INTERVAL = 10 * 60 * 1000;

unsigned long lastFetch = 0;

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

void fetchWeather() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[HTTP] WiFi 未连接, 跳过");
    return;
  }
  
  WiFiClientSecure client;
  client.setInsecure();
  
  HTTPClient http;
  http.begin(client, WEATHER_URL);
  
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (error) {
      Serial.printf("[JSON] 解析失败: %s\n", error.c_str());
    } else {
      const char* temp_C = doc["current_condition"][0]["temp_C"];
      const char* humidity = doc["current_condition"][0]["humidity"];
      const char* weather = doc["current_condition"][0]["weatherDesc"][0]["value"];
      
      Serial.println("====== 武汉天气 ======");
      Serial.printf("温度: %s°C\n", temp_C);
      Serial.printf("湿度: %s%%\n", humidity);
      Serial.printf("天气: %s\n", weather);
      Serial.println("======================");
    }
  } else {
    Serial.printf("[HTTP] 请求失败, 状态码: %d\n", httpCode);
  }
  
  http.end();  // ⚠️ 必须!
}

void setup() {
  Serial.begin(115200);
  delay(100);
  
  if (!connectWiFi()) return;
  fetchWeather();
  lastFetch = millis();
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastFetch >= FETCH_INTERVAL) {
    lastFetch = currentMillis;
    fetchWeather();
  }
}
```

---

## 9. 思考题闭环

### Q1: HTTP 401 错误怎么处理?
**两个排查方向**:
- 方向 1: 没传 API Key → 用 `http.addHeader("Key 头名", "Key 值")` 加上
- 方向 2: 传了但 Key 错了 → 重新复制 Key, 检查空格/截断/过期

**核心**: 401 是"授权层"问题, 不要瞎猜代码层。

### Q2: 内存泄漏修复
```cpp
void loop() {
  HTTPClient http;
  http.begin("http://example.com");
  int code = http.GET();
  if (code == 200) {
    String data = http.getString();
    Serial.println(data);
  }
  http.end();   // ✅ 加这行!
  delay(1000);
}
```
忘了 end() 每秒泄漏 1-2KB, **2.7 分钟内存耗尽崩溃**。

---

## 10. 易错点

| 坑 | 后果 |
|---|---|
| 忘 http.end() | 几分钟崩 |
| HTTPS 不用 WiFiClientSecure | 连不上 |
| 直接用 payload 不检查状态码 | 拿到错误页当成功 |
| JSON 解析不检查 error | 拿到 null 指针 |
| JSON 嵌套层级写错 | 拿到空值 |

---

## 11. 智能车应用场景
- **远程调 PID 参数**: 把参数放云端, ESP32 启动时 HTTP GET 拿配置
- **上报跑圈数据**: 比赛时 POST 圈速到服务器
- **接收上位机指令**: 拉云端的运行模式 (训练 / 比赛 / 调试)
- **拉取赛道信息**: 不同赛道不同算法参数

---

## 12. Day 7 四象限知识分类

### 🧠 重点记忆 (核心思维)
- HTTP 状态码反推问题层级 (200/401/404/500)
- begin 必有 end (资源配对纪律)
- 请求成功 ≠ 数据合法 (双重检查)
- JSON 剥洋葱访问思路

### 🔧 必懂代码模式
- HTTPClient 六件套
- ArduinoJson 解析三步
- 嵌套 JSON 访问

### 📚 必识 (用时查)
- 完整 HTTP 状态码表
- HTTPClient 所有方法
- ArduinoJson 6.x vs 7.x 语法
- HTTPS / TLS 协议细节

---

## 13. 我踩的坑 / 我的疑问 / 我的心得
<!-- 自己填: 
- 编译时遇到什么报错?
- 哪个 API 第一次没用对?
- 对 HTTP/JSON 还有什么不清楚?
-->
*Last updated: 2026-5-24*