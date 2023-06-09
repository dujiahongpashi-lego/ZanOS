# 赞OS / ZanOS
- 运行于 LEGO HUB NO6 (Spike Prime Hub)
- 使用前需对hub刷固件，所有代码全都是针对刷固件后的HUB进行开发的
- 上传所有文件，并只上传文件夹apps，即可使用

### ZanOS操作
- 任何时候按下HOME/WIN回主屏菜单
- 回车 进入功能/按键透传（透传指的是在APP内也可使用此按键）
- ESC 离开功能
- CAPSLOCK 开启后英文变大写，保持状态（显示图标）
- 左右 切换菜单/按键透传
- 单字符 直接透传
- 上下 直接透传
- F1 尝试连接蓝牙键盘，并显示debug信息
- F2 清除所有Debug信息
- WIFI：需在wifi APP代码内预设好WIFI的SSID和密码，请用明文代替***部分
- WIFI：连接成功后系统将显示WIFI图标
- WIFI：APP内，F5刷新连接状态。F6切换图标显示状态（不影响实际连接）


### 刷固件
- 不刷固件无法解锁UART能力。也无法使用GPIO读取输入电平触发的中断,因此只能单向使用GPIO输出。即：不刷固件只能使用OLED和LCD，无法使用键盘和ESP外设。
- 使用Micropython的官方固件 https://www.micropython.org/
- 在HUBNO6页面查看当前新版固件 https://www.micropython.org/download/LEGO_HUB_NO6/
- 亲测尝试过此页面上各种固件包安装方式，都未能成功。所以最终采用了源码编译后安装的方式 https://github.com/micropython/micropython/tree/master/ports/stm32/boards/LEGO_HUB_NO6
- 下载源码并进入Linux系统，用usb线连接hub
- 按照固件源码页面的操作流程操作
- 提示：自行刷固件有风险，自行刷固件有风险，自行刷固件有风险

### 刷回原固件
- 建议使用Pybricks提供的在线刷固件工具，刷回乐高原版固件
- https://code.pybricks.com/ 选 Restore official LEGO® Firmware，再按提示操作

### 接线
- 运行前须将各外设接线，HUB上6个接口没有区别，都可使用
- 位于main.py定义接线，可在代码中更改接口
- 默认使用PORT B D F，分别连接LCD、PS2键盘、ESP32
- PORT C默认可连接OLED作为副屏
- 更改接口可参考文档《STM32 LEGO HUB PORT Mapping.csv》中的接口定义

### ESP32
- esp32-py-firmware/中代码在ESP32上运行，device.py是入口代码
- 4根线分别接在ESP32的3v3 GND和UART2(即G16 G17)

### 中文支持
- 乐高内部python库不支持GBK编码，只支持UTF8
- LCD12864内置中文字库，仅支持GBK，需要乐高侧硬编码才能正确显示汉字
- 拼音输入法字库，取自开源拼音输入法 Rime https://rime.im/

### PC端服务
- others\ChatGPT and Bili Summary JS Server 启动PC端WEB服务，用于预处理和ChatGPT的交互
- 从乐高过来的数据中，服务将中文GBK转为更为通用的UTF8
- 代替乐高转发请求后，回来的信息中的中文，将UTF8转回GBK传回乐高
- 没有使用魔法上网，在PC端中调用的ChatGPT服务均为国内开放的ChatGPT镜像工具站的接口。接口的更新频率高，且有下线风险。代码中的接口都是亲测可用的，但可能仅限测试之当时可用，后续的可用性不保证。
- PC服务引用了开源项目 BibiGPT 的部分代码，感谢 BibiGPT https://github.com/JimmyLv/BibiGPT

### 拼搭图纸
- 见io文件
- 为保证模型牢固，拼搭中的反牛顿之处请见谅

### 外设
- LCD12864 3.3V 版，支持中文字库
- OLED 基于芯片SSD1306
- ESP32 WROM1
- 蓝牙键盘 杂牌PDD版
- PS2键盘 2007年买的版

### ZanOS 二次开发指南
- APP代码文件放入apps/
- APPS.reg中注册文件名和入口Class名，ZanOS将通过反射方式加载APP
- 可继承Program类
- 定义title title_cn icon，分别是英文中文显示名和图标
- 图标生成可使用 others\additional\像素图标转数组.py 生成图标数组数据
- 用device.send方法发送请求(HTTP)，device.add_listener来注册响应方法回调
- 使用device对象是，scope定义详见 others\additional\设备间互发消息.txt
- 可使用screen对象以及Article类控制显示
- 可使用event对象读取到键盘输入