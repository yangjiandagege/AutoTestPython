from test import test_launch_time
from common import dev_sn
from common import kill_process
import os


os.system("adb -s %s root"%dev_sn)
kill_process(dev_sn,"native_agent")
np_music = ["Music","","com.android.music"]
music_launch_time_test = test_launch_time(dev_sn,np_music)
music_launch_time_test.exec_test()
print("result of music_launch_time_test is %sms"%music_launch_time_test.result)
