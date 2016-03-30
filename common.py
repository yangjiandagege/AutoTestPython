import os

#dev_sn = "004999010699998"
#dev_sn = "0123456789012345"
dev_sn = "YOGA1753ECE2"

def kill_process(sn,process_name):
    pid = os.popen("adb -s %s shell ps | grep -i %s |awk '{print $2}'"%(sn,process_name)).read()
    if pid!="":
        os.system("adb -s %s shell kill -9 %s"%(sn,pid))

def install_appbench(sn):
    os.system("adb -s %s install ./res/AppBench_3GR_new.apk"%(sn,pid))
