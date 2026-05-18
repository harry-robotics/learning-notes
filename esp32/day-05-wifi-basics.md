# Day 5: ESP32 WiFi 入门 (STA 模式)

> 学习日期: 2026-05-18  
> 核心内容: WiFi 网络基础 + STA 连接 + 非阻塞编程 + 工程超时降级思维

---

## 0. WiFi 基础概念 (网络扫盲)

### SSID (WiFi 名字)
- **定义**: Service Set Identifier, WiFi 的"名字", 最长 32 字符
- **命名注意**:
  - 强烈不建议中文 SSID, 嵌入式设备兼容性差
  - 双频路由器通常有两个 SSID (如 `Home` 和 `Home_5G`)
  - **ESP32 只支持 2.4GHz**, 必须连接 2.4G 那个 SSID
- **隐藏 SSID**: 路由器可设置不广播 SSID, 但知道名字仍可连

### 密码 (WiFi Password)
- **加密协议主流**: WPA2-PSK (ESP32 完美支持)
- **WPA3**: ESP32 部分支持, 可能有兼容问题
- **工程安全**: 不要 push 明文密码到 GitHub!
  - 短期: 写在代码里, push 前改成假密码
  - 长期: 用 `secrets.h` + `.gitignore` (M2 学)

### IP 地址
- **公网 IP**: 路由器对外的地址, 全网唯一
- **内网 IP**: 路由器分给家里设备的地址 (如 `192.168.1.105`)
- **DHCP**: 路由器自动分配 IP 的机制
- **关键点**: `WiFi.localIP()` 必须在连上之后调用, 因为连上之前没分到 IP
- **工程坑**: IP 默认每次连接可能变化, 重要设备建议路由器绑定固定 IP

### MAC 地址 (硬件地址)
- **格式**: 6 段两位十六进制 (如 `A4:CF:12:34:56:78`)
- **特性**: 出厂烧死, 永远不变, 全球唯一
- **与 IP 的本质区别**:
  - MAC = 身份证号 (永远不变)
  - IP = 临时门牌号 (可能变化)
- **工程用途**:
  - 区分多台同型号设备
  - 路由器 MAC 绑定固定 IP
  - 设备唯一标识 (上报云端用)

---

## 1. WiFi 三种工作模式

| 模式 | 角色 | 典型场景 |
|---|---|---|
| **STA (Station)** | 客户端, 连别人的路由器 | 99% 物联网场景 |
| AP (Access Point) | 自己当热点 | 配网模式 |
| AP+STA | 两者同时 | 高级应用 |

---

## 2. WiFi 库核心 API

```cpp
#include <WiFi.h>  // ESP32 自带, 不需要装第三方库
```

| API | 作用 | 阻塞性 | 备注 |
|---|---|---|---|
| `WiFi.mode(WIFI_STA)` | 设置工作模式 | 非阻塞 | 显式声明好习惯 |
| `WiFi.begin(ssid, pwd)` | 发起连接 | **非阻塞!** | 立即返回, 后台连接 |
| `WiFi.status()` | 查询连接状态 | 非阻塞 | 返回状态码 |
| `WiFi.localIP()` | 获取分到的 IP | 非阻塞 | 连上才有效 |
| `WiFi.RSSI()` | 信号强度 (dBm) | 非阻塞 | 负数, 越接近 0 越强 |
| `WiFi.macAddress()` | 本机 MAC | 非阻塞 | 字符串形式 |
| `WiFi.reconnect()` | 重连 | 非阻塞 | 必须先 begin 过 |
| `WiFi.disconnect()` | 主动断开 | 非阻塞 | |

---

## 3. 核心认知: WiFi.begin() 的非阻塞特性

### 什么是非阻塞?
```cpp
WiFi.begin("MyWiFi", "password");  // 这一行 1ms 内返回
Serial.println("已发起连接");        // 立刻执行, 这时候还没连上!
```

调用 `WiFi.begin()` 后立即返回, 真正的连接握手在**后台**进行, 一般需要 2-10 秒。

### 为什么 ESP32 能做到后台连接? (回顾 Day 3)
- **Core 0 (PRO)**: 跑 WiFi/蓝牙协议栈, 默默处理连接
- **Core 1 (APP)**: 跑你的 Arduino 代码 (setup + loop)
- 真双核并行, 不是任务切片

这就是 ESP32 相比 Arduino UNO 的核心优势——**单核 UNO 做 WiFi 会卡死主程序, ESP32 不会**。

### 这对编程的影响
- 不能 `WiFi.begin()` 之后立刻用 `WiFi.localIP()`, 因为还没连上
- 必须**轮询** `WiFi.status()` 等待连接完成
- 必须设计**超时机制**, 防止永远卡死

---

## 4. WiFi 状态机

| 状态常量 | 数值 | 含义 |
|---|---|---|
| `WL_IDLE_STATUS` | 0 | 空闲 |
| `WL_NO_SSID_AVAIL` | 1 | 找不到 SSID |
| `WL_SCAN_COMPLETED` | 2 | 扫描完成 |
| `WL_CONNECTED` | 3 | ✅ 已连接 |
| `WL_CONNECT_FAILED` | 4 | 连接失败 (一般密码错) |
| `WL_CONNECTION_LOST` | 5 | 连接丢失 |
| `WL_DISCONNECTED` | 6 | 已断开 |

**工程实践重点**: 只关注 `WL_CONNECTED`, 其他都归类为"还没连上"。

---

## 5. RSSI 信号强度

| RSSI 范围 (dBm) | 信号质量 | 体验 |
|---|---|---|
| -30 ~ -50 | 极强 | 紧贴路由器 |
| -50 ~ -60 | 强 | 同一房间 |
| -60 ~ -70 | 中 | 隔一堵墙 |
| -70 ~ -80 | 弱 | 开始丢包 |
| < -80 | 极弱 | 频繁断连 |

**工程用途**: 提示用户"信号太弱", 优化设备摆放位置。

---

## 6. 工程思维: 超时处理

### 新手错误写法 ❌
```cpp
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.print(".");
}
```
**问题**:
- 路由器宕机/密码错/信号弱 → ESP32 永远卡死
- 看门狗可能复位芯片, 进入复位死循环
- 用户体验灾难: 开机后无响应

### 工程师正确写法 ✅
```cpp
WiFi.begin(ssid, password);
unsigned long startTime = millis();
const unsigned long TIMEOUT = 10000;  // 10 秒

while (WiFi.status() != WL_CONNECTED) {
  if (millis() - startTime >= TIMEOUT) {
    Serial.println("\n[WiFi] 连接超时, 进入离线模式");
    return;
  }
  delay(500);
  Serial.print(".");
}
```
**关键点**:
- `millis() - startTime`: Day 4 学的**减法形式**, 溢出安全
- 超时后**降级运行**, 不卡死
- loop 里再定期重连

---

## 7. 离线降级策略

### 为什么需要降级
- 网络不可靠 (路由器重启/WiFi 拥塞/信号波动)
- 嵌入式设备必须保证**基础功能不依赖网络**
- 用户体验: 离线时仍能感知设备状态

### 常见降级策略
| 场景 | 在线行为 | 离线降级 |
|---|---|---|
| 温湿度上报 | MQTT 推云端 | 本地 OLED 显示 + SD 卡缓存 |
| 智能开关 | App 远程控制 | 物理按钮仍可用 |
| 智能门铃 | 推送手机 | 本地蜂鸣器响 |

**核心思想**: 网络是锦上添花, 不是雪中送炭。

---

## 8. Day 5 完整代码

```cpp
/*
 * esp32_wifi_basic - Day 5 ESP32 WiFi STA 模式入门
 * 演示:
 *   1. 非阻塞 WiFi 连接 + 超时降级
 *   2. WiFi 状态机检查
 *   3. 心跳检测 + 自动重连
 *   4. 工程师标准结构
 */

#include <WiFi.h>

// ============== 配置区 (按你家 WiFi 修改) ==============
const char* WIFI_SSID     = "你的WiFi名";
const char* WIFI_PASSWORD = "你的WiFi密码";

const unsigned long WIFI_TIMEOUT       = 10000;  // 10 秒连接超时
const unsigned long HEARTBEAT_INTERVAL = 5000;   // 5 秒心跳

// ============== 全局变量 ==============
unsigned long lastHeartbeat = 0;
bool wifiOk = false;

// ============== WiFi 连接函数 ==============
bool connectWiFi() {
  Serial.printf("\n[WiFi] 连接到 %s ...\n", WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime >= WIFI_TIMEOUT) {
      Serial.println("\n[WiFi] 连接超时");
      return false;
    }
    delay(500);
    Serial.print(".");
  }
  
  Serial.println();
  Serial.printf("[WiFi] 已连接\n");
  Serial.printf("[WiFi] IP 地址: %s\n", WiFi.localIP().toString().c_str());
  Serial.printf("[WiFi] MAC 地址: %s\n", WiFi.macAddress().c_str());
  Serial.printf("[WiFi] 信号强度: %d dBm\n", WiFi.RSSI());
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(100);
  
  wifiOk = connectWiFi();
  
  if (!wifiOk) {
    Serial.println("[Main] WiFi 失败, 进入离线模式 (功能降级)");
  } else {
    Serial.println("[Main] WiFi 成功, 进入在线模式");
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastHeartbeat >= HEARTBEAT_INTERVAL) {
    lastHeartbeat = currentMillis;
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.printf("[心跳] 在线, RSSI: %d dBm\n", WiFi.RSSI());
      wifiOk = true;
    } else {
      Serial.println("[心跳] 离线, 尝试重连...");
      wifiOk = false;
      WiFi.reconnect();
    }
  }
}
```

### 代码工程亮点
| 设计 | 体现的工程思维 |
|---|---|
| 配置区集中放顶部 | 改 SSID/密码只改一处 |
| 用 `const` 修饰配置 | 防止意外修改 |
| 封装成 `connectWiFi()` | 复用 + 可读性 |
| 函数返回 `bool` | 调用方能决策 |
| 超时 `return` 不死等 | 系统鲁棒性 |
| 心跳持续检测+重连 | 长时间运行稳定性 |
| 用 `wifiOk` 标志位 | 在线/离线成为一等概念 |

---

## 9. 指针知识补充 (C 基础薄弱专项)

### `const char*` 是什么?
```cpp
const char* WIFI_SSID = "Harry";
```
- `char*` = 指向 char 的指针 (字符串本质)
- `const` = 内容只读, 不允许修改
- 字符串实际存在程序的**只读内存区**
- 指针存的是字符串第一个字符的**地址**

### 内存示意
```
地址:  0x100  0x101  0x102  0x103  0x104  0x105
值:    [ H ] [ a ] [ r ] [ r ] [ y ] [ \0 ]
        ↑
        WIFI_SSID 指向这里 (0x100)
```

### `printf("%s", ...)` 必须传 char*
```cpp
Serial.printf("%s", WiFi.localIP().toString().c_str());
//                                            ↑↑↑↑↑↑↑
//                              把 String 对象转成 const char*
```
- `WiFi.localIP()` → 返回 `IPAddress` 对象
- `.toString()` → 转 `String` 对象
- `.c_str()` → 转 `const char*` (C 风格字符串)

### 指针先记五点
1. `&变量` 取地址
2. `*指针` 取值 (解引用)
3. `char*` 用来指向字符串
4. `printf` 的 `%s` 要 `char*`, `String` 对象要 `.c_str()` 转换
5. 指针就是地址, 大小固定 (64 位系统 8 字节)

---

## 10. 关键易错点

| 坑 | 现象 | 解决 |
|---|---|---|
| 连 5GHz WiFi | 永远 `WL_NO_SSID_AVAIL` | 改连 2.4G SSID |
| `reconnect()` 没 begin 过 | 静默失败, 永不连接 | 首次必须 `begin()` |
| `localIP()` 在连上前调用 | 返回 `0.0.0.0` | 等 `WL_CONNECTED` 后调用 |
| while 死等连接 | 路由器挂了就死机 | 用 millis 超时降级 |
| 明文密码 push GitHub | 安全泄露 | 改假密码再 push |

---

## 11. 思考题闭环

### Q1: WiFi.mode(WIFI_STA) 能不能删?
- 能, ESP32 默认就是 STA
- 但显式声明是工程师好习惯: 意图清晰 / 防御性 / 可移植性

### Q2: setup 超时返回后 reconnect 会怎样?
- 第一问: `WiFi.status()` 返回非 `WL_CONNECTED` 状态 (常见 `WL_DISCONNECTED`)
- 第二问关键: **只要 begin 过一次, reconnect 就能用** (即使 begin 后没连上, 凭证已缓存)
- **真实 bug 场景**: 从来没 begin 直接 reconnect → 永远连不上

### Q3: 常驻 vs 唤醒+断开?
- 功耗: A >> B (差 8-10 倍数量级)
- 延迟: A < 1s, B 最坏 5min
- 云控: A 实时, B 几乎不可用
- **决策**: 电池供电必须 B, USB 供电必须 A

---

## 12. Day 5 四象限知识分类

### 🔧 操作 - 必须熟练 (高频反复用)
| 操作 | 频率 |
|---|---|
| 写 `WiFi.begin()` 三件套 (mode + begin + status 轮询) | 几乎每个 IoT 项目 |
| 用 `millis()` 减法形式写非阻塞超时 | 巨高频 |
| `Serial.printf` 格式化打印调试 | 巨高频 |
| 烧录后开串口监视器 (115200) | 每次烧录 |

### 🛠️ 操作 - 跟一遍即可 (低频/一次性)
- 进路由器后台查设备列表
- MAC 绑定固定 IP 的路由器设置
- `WiFi.config()` 静态 IP 配置
- 切换 2.4G/5G 的路由器配置

### 🧠 知识 - 重点记忆 (理论核心)
- `WiFi.begin()` 是非阻塞的
- Core 0 跑 WiFi 协议栈, Core 1 跑你的代码
- 超时降级的工程思维 (不能 while 死等)
- MAC vs IP 的本质区别 (身份证 vs 门牌号)
- DHCP 分配 IP 的机制
- ESP32 只支持 2.4GHz WiFi
- 明文密码 push GitHub 的安全隐患

### 📚 知识 - 不必死记 (百度即得)
- WiFi.status() 的 6 个状态数值
- RSSI 具体数值范围细节
- WPA2/WPA3 加密协议技术细节
- WiFi 库所有 API 列表
- 2.4GHz / 5GHz 频段技术差异
- IPv4 / IPv6 格式细节

---

*Last updated: 2026-5-18*

