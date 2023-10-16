#!/usr/bin/env python3

import re
from matplotlib import pyplot as plt
from VisualLog.MatplotlibZoom import figure_pan_and_zoom

class Bootprof:

    """
    可视化两个版本的Android bootprof

    @first(template/bootprof_ref_20230804.txt): 第一个文件，对比机
    @second(template/bootprof_go_20230804.txt): 第二个文件，自己的机器
    @mode(all): 输出分析曲线类型，all、kernel
    """

    def __init__(self, kwargs):

        # 对比机
        first = kwargs["first"]
        # 自己的机器
        second = kwargs["second"]
        # 只显示内核，或者全部显示
        mode = kwargs["mode"]
        bootprof_keys = []

        # 加载对比机数据
        first_keys = self.load_keys(first, mode)
        # 加载自己机器数据
        second_keys = self.load_keys(second, mode)

        # 剔除不需要的key
        for first_key in second_keys:
            if first_key.startswith("TEEI") or first_key.startswith("ccci") or "deferred_probe_initcall" in first_key:
                continue

            if first_key in first_keys:
                bootprof_keys.append(first_key)
        
        # 基于bootprof_keys来生成数据
        bootprof_arrays = []
        for filename in [first, second]:

            # 生成数组
            items = [None] * len(bootprof_keys)

            with open(filename, mode="r", encoding='UTF-8') as fd:
                for line in fd:
                    lineSplits = line.strip().split(" : ")

                    if len(lineSplits) == 3:
                        if len(lineSplits[2].strip("")) == 0:
                            continue

                        # 组合当前字符串
                        concat_keys = self.log_key_str(lineSplits[2])
                        if concat_keys in bootprof_keys :
                            # print(lineSplits[0] + " : " + lineSplits[2] + " : " + str(bootprof_keys.index(concat_keys)))
                            if items[bootprof_keys.index(concat_keys)] == None:
                                items[bootprof_keys.index(concat_keys)] = (float(lineSplits[0].strip()) / 1000)

            # 对于有些没有的数据，用前面的数据进行填充
            for index in range(len(items)):
                if items[index] == None:
                    if index == 0:
                        items[index] = 0
                    else:
                        items[index] = items[index - 1]

            bootprof_arrays.append(items)
            # print(bootprof_arrays)

        print("------------------------------------")

        # 支持鼠标中间缩放，左键移动
        fig = figure_pan_and_zoom()
        ax1 = fig.add_subplot(1, 1, 1)

        # 绘制点
        for file_index in range(2):
            items = bootprof_arrays[file_index]
            for item_index in range(len(bootprof_keys)):
                ax1.plot(item_index, items[item_index], 'o')
                ax1.plot([item_index, item_index], [0, items[item_index]], color="gray")
        # 绘制text
        items = bootprof_arrays[file_index]
        for item_index in range(len(bootprof_keys)):
            ax1.text(item_index - 0.15, items[item_index] + 0.4, bootprof_keys[item_index], fontsize=7, rotation=90)

        # 绘制曲线
        X1 = list(range(len(bootprof_keys)))
        for index in range(2):
            curve_name = "Reference Machine"
            if index == 1:
                curve_name = "Own Machine"
            line, = ax1.plot(X1, bootprof_arrays[index], label=curve_name)

        # 计算差值
        items = [None] * len(bootprof_keys)
        items_diff = [None] * len(bootprof_keys)
        items_diff[0] = 0
        for item_index in range(len(bootprof_keys)):
            items[item_index] = bootprof_arrays[1][item_index] - bootprof_arrays[0][item_index]
            if item_index != 0:
                # items_diff[item_index] = abs(items[item_index] - items[item_index - 1])
                items_diff[item_index] = items[item_index] - items[item_index - 1]
        ax1.plot(X1, items, label='Relative Increment')
        ax1.plot(X1, items_diff, color="red", label='Diff Increment')

        ax1.plot([0, len(bootprof_keys)], [0, 0], marker='o')

        ax1.set_xlabel("X Bootprof Keys Index")
        ax1.set_ylabel("Y Bootprof Time")
        ax1.set_title("/proc/bootprof")

        plt.legend(loc='best')
        plt.show()
    
    def log_key_str(self, line):
        keys = line.strip("").split()
        concat_keys = ""

        for key in keys:
            # key = key.strip().replace(":", "")
            key = key.strip()
            if "(0x" in key:
                key = key.split("(0x")[0]

            matchObj = re.match(r'^\d*\.*\d*ms$', key, re.M | re.I)
            if matchObj:
                continue

            if key.isnumeric():
                continue

            # matchObj = re.match(r'.*(pid\d+)', key, re.M | re.I)
            matchObj = re.match(r'.*(pid:\d+)', key, re.M | re.I)
            if matchObj:
                print(key)
                key = key.replace(matchObj.group(1), "")

            # print(key)
            concat_keys += key + ":"
        
        return concat_keys[:-1]

    def load_keys(self, file, mode):
        keys = []
        with open(file, mode="r", encoding='UTF-8') as fd:
            for line in fd:
                lineSplits = line.strip().split(" : ")
                if len(lineSplits) == 3:
                    # print(lineSplits[2])

                    if len(lineSplits[2].strip("")) == 0:
                        continue

                    # 只处理kernel相关部分的数据，也就是不显示那么多数据
                    if mode == "kernel":
                        if "swapper/0" in lineSplits[1] or "kworker/0:1" in lineSplits[1]:
                            concat_keys = self.log_key_str(lineSplits[2])
                            keys.append(concat_keys)
                    else:
                        concat_keys = self.log_key_str(lineSplits[2])
                        keys.append(concat_keys)
        
        return keys

if __name__ == "__main__" :
    print("main")
