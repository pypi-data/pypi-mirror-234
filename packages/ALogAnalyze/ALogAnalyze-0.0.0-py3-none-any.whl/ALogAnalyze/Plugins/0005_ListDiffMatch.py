#!/usr/bin/env python3

import re
import difflib

class ListDiffMatch:

    """
    可视化两个版本的Android bootprof

    @data(default/UDiskMount.txt): U盘挂载数据
    """

    def __init__(self, kwargs):

        # 对比机
        data = kwargs["data"]
        data1_keys = [
            "USB Mass Storage device detected",
            "USB Mass Storage device detected",
            "scsi host0: usb-storage 1-1:1.0",
            "Direct-Access",
            "Attached SCSI removable disk",
            "/system/bin/sgdisk",
            "Disk::readPartitions",
            "Disk::createPublicVolume",
            "FAT-fs"
        ]

        data2_keys = [
            "scsi host0: usb-storage 1-1:1.0",
            "USB Mass Storage device detected",
            "Direct-Access",
            "Attached SCSI removable disk",
            "/system/bin/sgdisk",
            "Disk::readPartitions",
            "FAT-fs",
            "Disk::createPublicVolume",
        ]

        diff = difflib.Differ()
        print("new +++")
        print("old ---")
        print("\n".join(list(diff.compare(data1_keys, data2_keys))))

        print("--------------")

        for line in list(diff.compare(data1_keys, data2_keys)):

            matchObj = re.match(r'^([\+\- ]) ', line, re.M | re.I)
            if matchObj:
                print(line)

                match = matchObj.group(1)
                if match == " ":
                    print("normal")
                elif match == "+":
                    print("add")
                elif match == "-":
                    print("del")
                else:
                    print("not found")
    
if __name__ == "__main__" :
    print("main")
