# ns_asphalt9

![switch connect](https://github.com/codehai/ns_asphalt9/blob/main/images/ui.jpg?raw=true)

**ns-asphalt9是一个基于图像采集和蓝牙模拟手柄自动完成Asphalt9日常任务的工具。**

目前支持的功能如下：

* **模式设置** - 支持多人一、多人二、多人三、野兽年
* **任务设置** - 支持在循环模式中执行定时任务，支持的任务有免费抽卡、大奖赛抽卡、寻车、传奇寻车、自动重启、商店刷新通知
* **自动选车** - 多人一可以根据段位选车，可以配置不同段位所使用的车库等级以及所使用的车辆
* **自动扫描寻车位置** - 由于每日任务经常有新活动上架或者老活动下架导致寻车位置经常变动，当变动以后会自动扫描活动查找寻车活动位置
* **自动选路** - 根据地图自动选择路线
* **错误重进** - 支持识别系统错误、连接错误、服务错误等发生以后重新进入游戏
* **log追踪** - 完善log体系，可以追溯任何操作

这个工具是基于nxbt控制switch、v4l2图像采集、tesseract-ocr5识别图像开发的。因此使用前需要准备一些硬件并搭建一下环境。

推荐使用的系统环境为

* windows
* linux
* mac(全平台)

> NS狂野飙车9工具交流、历史兑换码、UnEdge前100俱乐部申请等请加vx: unedge或qq: 77686805

### 硬件依赖

硬件连线图参考如下:

![switch connect](https://github.com/codehai/ns_asphalt9/blob/main/images/switch_nxbt.png?raw=true)

1. **HDMI采集卡(必选)** - 用于switch画面输入到虚拟机
2. **USB蓝牙(必选)** - 用于模拟手柄向switch发消息,Linux环境下可用本机蓝牙，Mac，Windows，群晖虚拟机请买usb蓝牙，注意群晖请需要适用于群晖的免驱蓝牙。
3. **HDMI分配器一分二 一进二出(可选)** - 同时输出switch到显示器和采集卡，方便查看工具操作以及在工具和手柄间自有切换。

### 详细教程

[Wiki](https://docs.qq.com/aio/DWHFrVHlxV1ZVWU1p)

### 免责声明

ns_asphalt为python学习交流的开源非营利项目，仅作为程序员之间相互学交流之用，使用需严格遵守开源许可协议。严禁用于商业用途，禁止使用ns_asphalt进行任何盈利活动。对一切非法使用所产生的后果，我们概不负责。

### 许可证

![GitHub](https://img.shields.io/github/license/codehai/ns_asphalt9.svg)
