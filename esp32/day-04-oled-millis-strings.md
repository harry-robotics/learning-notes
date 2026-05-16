# Day 4: OLED 显示 + millis() 非阻塞 + 字符串处理

> 日期: 2026-05-13
> 主题: 综合性项目入门,真正学会"嵌入式多任务编程"

## 1. OLED 0.96" SSD1306

### 1.1 硬件参数
- 分辨率: 128 × 64 像素
- 驱动芯片: SSD1306
- 通信: I2C (默认地址 0x3C)
- 工作电压: 3.3V (兼容 5V,但 ESP32 用 3.3V 更安全)

### 1.2 接线方案 (ESP32)

```text
OLED       →    ESP32
VCC        →    3.3V
GND        →    GND
SDA        →    GPIO 21  (ESP32 默认 I2C SDA)
SCL        →    GPIO 22  (ESP32 默认 I2C SCL)
```

### 1.3 库的选择
入门用 Adafruit_SSD1306 + Adafruit_GFX (简单稳定)。
进阶 (中文显示等) 用 U8g2。

## 2. OLED 编程模板

### 2.1 标准初始化

```c
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED init failed!");
    while (1);  // 死循环,防御性编程
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
}
```

### 2.2 显示文字的 4 步流程

1. `display.clearDisplay()` 清空缓冲区
2. `display.setTextSize()` / `setTextColor()` / `setCursor()` 设置属性(字号大小，字颜色，光标位置)
3. `display.println()` / `print()` 写入缓冲区
4. **`display.display()`** ← 真正显示,易忘!

### 2.3 关键 API

| 函数 | 作用 |
|---|---|
| `setTextSize(n)` | 字号,1=最小 (6x8) |
| `setCursor(x, y)` | 光标位置 (左上角 = 0,0) |
| `setTextColor(SSD1306_WHITE)` | 文字颜色 (OLED 只有亮/灭) |
| `clearDisplay()` | 清空缓冲区 |
| `display()` | 实际把缓冲区刷到屏幕 |

## 3. millis() 非阻塞编程 (核心)

### 3.1 delay() 的致命缺陷
`delay(1000)` 期间 CPU 完全卡死,任何按钮、传感器、串口数据都不响应。
导致多任务场景下整个程序卡顿。

### 3.2 millis() 是什么
返回芯片启动到现在过去的毫秒数 (`unsigned long`)。
**调用本身不阻塞**,49.7 天后溢出回 0。

### 3.3 非阻塞公式 (背下来)

```c
unsigned long previousMillis = 0;
const unsigned long interval = 1000;

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    // 执行任务
  }
  
  // 其他代码继续运行,不被阻塞
}
```

### 3.4 多任务并行模板

```c
unsigned long lastTask1 = 0;
unsigned long lastTask2 = 0;
unsigned long lastTask3 = 0;

const unsigned long interval1 = 500;
const unsigned long interval2 = 1000;
const unsigned long interval3 = 5000;

void loop() {
  unsigned long now = millis();
  
  if (now - lastTask1 >= interval1) {
    lastTask1 = now;
    task1();
  }
  
  if (now - lastTask2 >= interval2) {
    lastTask2 = now;
    task2();
  }
  
  if (now - lastTask3 >= interval3) {
    lastTask3 = now;
    task3();
  }
}
```

### 3.5 溢出陷阱 (深入)

`(now - last >= interval)` **减法形式**利用 unsigned long 溢出特性,溢出时自动绕回,**计算正确**。

`(now >= last + interval)` **加法形式**在溢出附近会出 bug,**禁用**。

工程师法则:**永远用减法,不用加法**。

### 3.6 millis() 法则
- 写新代码本能用 millis() 不用 delay()
- 简单 LED 闪烁也用 millis(),养成习惯

## 4. String 类的坑

### 4.1 内存碎片问题
String 每次拼接都重新分配内存,长期跑会导致内存碎片化,最终崩溃。速度也慢。(malloc/free动态分配释放内存) 

### 4.2 替代方案: char[] + sprintf

```c
char buffer[32];
sprintf(buffer, "Temp: %d C", temperature);
Serial.println(buffer);
```

优势:内存固定、速度快、嵌入式标准。

### 4.3 常用格式符

| 格式符 | 含义 | 例子 |
|---|---|---|
| `%d` | int 整数 | "42" |
| `%lu` | unsigned long | "12345" |
| `%.1f` | 1位小数浮点 | "3.1" |
| `%s` | 字符串 | "Hi" |
| `%c` | 单字符 | "A" |
| `%02d` | 不足 2 位补 0 | "05" |

### 4.4 嵌入式法则
能用 char[] 替代 String 时,**永远选 char[]**。

## 5. 中断 vs 轮询 (按钮场景判断)

判断标准:**事件突发 + 必须立即响应 → 中断**

| 场景 | 选择 | 理由 |
|---|---|---|
| 急停按钮 (工业) | 中断 | 必须毫秒级响应 |
| 普通开关按钮 | 轮询 (50ms) | 用户感觉不到延迟 |
| 编码器读数 | 中断 | 高速事件,轮询会漏 |
| 定时读温湿度 | 轮询 | 周期性任务,不突发 |

## 6. 代码项目清单

本日完成的项目 (本地 E:\code\):
- `esp32_oled_hello`: OLED 显示静态文字
- `esp32_oled_clock`: OLED + millis() 实时显示运行时间
- `esp32_oled_multitask`: LED + OLED + 串口三任务并行

---

*Last updated: 2026-05-13*