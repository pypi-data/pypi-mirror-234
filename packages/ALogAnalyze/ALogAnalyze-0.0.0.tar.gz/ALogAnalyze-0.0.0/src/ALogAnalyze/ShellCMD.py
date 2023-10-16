import subprocess

def Shell(*cmd):
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = out.stdout.read()
    if data != None:
        return data.decode('utf-8').strip()
    else:
        return ""

if __name__ == "__main__" :
    print(Shell("adb", "devices"))
    print(Shell("adb", "root"))
    print(Shell("adb", "shell", "cat /proc/bootprof"))
