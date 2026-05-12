# Day 2: 上拉电阻 + 中断 + PWM + I2C 代码深化

> 日期: 2026-05-12

## 1. 上拉/下拉电阻

### 1.1 浮空状态是什么

GPIO的一种物理状态，电压不确定，数字随机读取（可能是0也可能是1，因为现实世界充满电磁干扰）

### 1.2 上拉电阻原理(自己画图或描述)

```text
       3.3V
        │
       [10kΩ]    ← 上拉电阻
        │
ESP32 GPIO 4 ──[按钮]── GND
```

当按钮按下时，GPIO直接接到GND,故GPIO直接读取到LOW
当按钮断开时，GPIO间接接到3.3V，故GPIO直接读取到HIGH

```text
       3.3V
        │
       [按钮]
        │
ESP32 GPIO 4
        │
       [10kΩ]    ← 下拉电阻
        │
       GND
```

当按钮按下时，GPIO直接接到3.3V，故GPIO直接读取到HIGH
当按钮断开时，GPIO间接接到GND，故GPIO直接读取到LOW

### 1.3 上拉 vs 下拉对比表

| 维度 | 上拉 | 下拉 |
|---|---|---|
| 电阻接 | 3.3V | GND |
| 默认电平 | HIGH | LOW |
| 按钮另一端接 | GND | 3.3V |

### 1.4 ESP32 内置上拉/下拉的代码用法

```c
pinMode(BUTTON_PIN, INPUT_PULLUP);    // 启用内置上拉
pinMode(BUTTON_PIN, INPUT_PULLDOWN);  // 启用内置下拉
```

## 2. 中断(Interrupt)

### 2.1 中断代码核心解释
- Serial.begin(115200)串口通信，波特率115200
- volatile表示这个变量随时可改
-  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN),buttonPressed, FALLING);

- 1.  digitalPinToInterrupt(BUTTON_PIN)把引脚号转成中断号
 - 2.  buttonPressed 不带括号，当中断触发时，自动运行的函数名
 - 3.  FALLING 从HIGH变成LOW(下降沿)时，实现了按下瞬间触发

### 2.2 中断的三条铁律
中断函数三条规则:
1. 修改的变量必须加 volatile
2. 函数体要尽量短(< 几毫秒)
3. 不要在中断里用 delay() 或 Serial.println()


### 2.3 标准代码模板

```c
const int BUTTON_PIN = 4;
volatile int counter = 0;

void buttonPressed() {
  counter++;
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN),buttonPressed, FALLING);
}

void loop() {
  Serial.println(counter);
  delay(1000);
}
```

### 2.4 触发模式选择(RISING / FALLING / CHANGE)
- `RISING`: 低→高
- `FALLING`: 高→低
- `CHANGE`: 任何变化
- `LOW`: 持续低电平

## 3. ESP32 PWM(ledc)

### 3.1 三个核心参数
- **通道(Channel)**: 0-15,共16个独立通道
- **频率(Frequency)**: 通常 5kHz 适合 LED
- **分辨率(Resolution)**: 8 位 = 0-255 级

### 3.2 参数权衡(分辨率 vs 频率)
分辨率越高,频率上限越低。8 位+5kHz 是 LED 最佳组合

### 3.3 标准代码模板

```c
const int LED_PIN = 2;
const int PWM_CHANNEL = 0;
const int PWM_FREQ = 5000;
const int PWM_RESOLUTION = 8;

void setup() {
  ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(LED_PIN, PWM_CHANNEL);
}

void loop() {
  for (int i = 0; i < 256; i++) {
    ledcWrite(PWM_CHANNEL, i);  // 设置占空比
    delay(10);
  }
}
```

### 3.4 与 Arduino UNO PWM 的差异
- Arduino UNO: `analogWrite()` 直接用,但只有 6 个固定 PWM 引脚
- ESP32: 用 `ledcSetup()` + `ledcWrite()`,任意 GPIO 可分配到 16 个通道


## 4. I2C 通信(Wire 库)

### 4.1 核心要点
- 2 根线:SDA(数据)+ SCL(时钟)
- 多设备通过 7 位地址区分
- ESP32 默认: SDA=GPIO21, SCL=GPIO22

### 4.2 标准代码模板

```c
#include <Wire.h>

void setup() {
  Wire.begin();                      // 初始化
  Wire.beginTransmission(0x3C);      // 指定设备地址(OLED)
  Wire.write(0x00);                  // 发送数据
  Wire.endTransmission();            // 结束通信
}
```

### 4.3 为什么需要 Wire 库(封装意义)
封装的价值:我只用关心业务逻辑,底层时序由库处理


## 5. 昨日问题回答
- 1. GPIO在ESP32比Arduino能做更多
- 2. digitalWrite()芯片底层逻辑：代码->机器指令->CPU改写寄存器->GPIO电路控制晶体管动作->物理电压变化（仅了解）
- 3. I2C具体原理(仅了解)：SDA传输实际0和1；SCL提供同步节拍，告诉“什么时候读取SDA”
>> **Note** :今日思考题明日总结

---

*Last updated: 2026-05-12*