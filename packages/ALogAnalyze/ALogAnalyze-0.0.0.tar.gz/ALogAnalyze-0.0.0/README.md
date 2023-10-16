# README

Android Log Analyze

# UI

![0000_UI.png](/docs/images/0000_UI.png)

# 说明

* X Axis:
  * 获取的正则表达式groups中的数据索引，和Data Index数组共同作用
  * 空：使用自增整数作为索引，从0开始
  * Data Index中索引: 从Data Index获取索引作为X轴，一般是0
    * 如果X Axis和Data Index相同，那么Y轴采用自增索引，便于区分
* Data Index:
  * 获取的正则表达式groups中的数据索引，和X Axis数组共同作用
  * 绘图索引，和X Axis相同的索引会绘制垂线

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0001 | [Data3D](docs/0001_Data3D.md) | 获取加速度计数据
