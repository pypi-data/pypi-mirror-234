import sys
import re
import time
import os

class KlogTime2UTC:
    """
    将内核log时间转换为UTC时间

    @input(template/kernel_log_6__2021_1118_154505): klog log文件
    """

    def __init__(self, kwargs):
        self.kernel_to_utc(kwargs["input"])

    def kernel_to_utc(self, klog):
        line = 0
        line_timestamp = []
        diff_timestamp = []
        debug_enable = False

        llog = klog + ".UTC.converted"

        with open(klog, mode="r", encoding='ISO-8859-1') as fh:
            with open(llog, mode="w", encoding='UTF-8') as fhout:

                _re_utc_time = re.compile(r"[^\[]*?\[[ ]*(\d+?\.\d+)\].*?(\d+-\d+-\d+ \d+:\d+:\d+)(\.\d+) UTC")

                for linebuf in fh:
                    line = line + 1

                    if "UTC" not in str(linebuf):
                        continue

                    m = _re_utc_time.match(str(linebuf))
                    if m:
                        (ktime, atime, usec) = m.group(1,2,3)
                        time_sec_int = time.mktime(time.strptime(atime, "%Y-%m-%d %H:%M:%S"))
                        time_sec = time_sec_int + float(usec) - float(ktime)

                        if (debug_enable):
                            print("*")
                            print(linebuf)
                            print(ktime, atime, usec)

                        line_timestamp.append(line)
                        diff_timestamp.append(time_sec)


                # second pass
                fh.seek(0, os.SEEK_SET)

                if debug_enable:
                    print(len(line_timestamp),",",len(diff_timestamp))
                    print(line_timestamp)
                    print(diff_timestamp)

                line_ts_ref = -1
                diff_ts_ref = 0

                # in case no timestamp exist
                if line_timestamp:
                    line_ts_ref = line_timestamp[0]
                    diff_ts_ref = diff_timestamp[0]

                # _re_ktime = re.compile(r"^[ ]*?<[^>]+>\[[ ]*?(\d+?\.\d+?)\]")
                _re_ktime = re.compile(r"^[^\[]*?\[[ ]*?(\d+?\.\d+?)\]")

                line = 0
                for linebuf in fh:
                    diff_ts = -1
                    line = line + 1

                    m = _re_ktime.match(str(linebuf))
                    if m:
                        diff_ts = float(m.group(1))

                    if line == line_ts_ref:
                        line_timestamp.pop(0)
                        line_ts_ref = line_timestamp[0] if line_timestamp else sys.maxsize
                        diff_ts_ref = diff_timestamp.pop(0)

                        if debug_enable: print("diff_ts_ref: ", diff_ts_ref)

                    if diff_ts != -1:
                        if line_ts_ref != -1:
                            android_time = diff_ts + diff_ts_ref
                            android_time_int = int(android_time)
                            android_time_frac = android_time - android_time_int

                            ts = time.localtime(android_time_int)

                            fhout.write(time.strftime("%Y-%m-%d %H:%M:%S", ts) + ("%.6f " % android_time_frac)[1:])
                        else:
                            fhout.write("??-?? ??:??:??.?????? ")

                    # print(linebuf.strip())
                    fhout.write(linebuf)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], " <kernel log>")
        sys.exit()
    else:
        KlogTime2UTC({"input": sys.argv[1], "output": "output/" + os.path.basename(sys.argv[1])+".utc"})

    sys.exit()
