from test import test_launch_time
from common import dev_sn
from common import kill_process
import os
import time

os.system("adb -s %s root"%dev_sn)
time.sleep(2)
os.system("adb wait-for-device")
kill_process(dev_sn,"native_agent")
np_chrome = ["Chrome","./res/Browser/Chrome_M42.apk","com.android.chrome"]
chrome_launch_time_test = test_launch_time(dev_sn,np_chrome)
chrome_launch_time_test.exec_test()
print("result of chrome_launch_time_test is %sms"%chrome_launch_time_test.result)
