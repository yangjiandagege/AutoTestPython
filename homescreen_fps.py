from test import test_fps 
from common import dev_sn
from common import kill_process
import os
import time

class homescreen_fps(test_fps):
    def measure(self):
        self.logout(self.my_func_name(),"...")
        time.sleep(3)
        self.icon_click()
        self.swipe_horiz(3,self.SWIPE_DIR_LEFT)
        self.swipe_horiz(3,self.SWIPE_DIR_RIGHT)
        self.device(description='Apps').click()
        self.swipe_horiz(5,self.SWIPE_DIR_LEFT)
        self.swipe_horiz(5,self.SWIPE_DIR_RIGHT)
        self.icon_click()

if __name__=="__main__": 
    os.system("adb -s %s root"%dev_sn)
    kill_process(dev_sn,"native_agent")
    np_homescreen = ["Launcher","","com.android.launcher"]
    homescreen_fps_test = homescreen_fps(dev_sn,np_homescreen)
    homescreen_fps_test.exec_test()
    print("result of homescreen_fps_test is %sfps"%homescreen_fps_test.result)
