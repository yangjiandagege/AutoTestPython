from test import test_fps
from common import dev_sn
from common import kill_process
import os
import time

class chrome_fps(test_fps):
    def load_resource(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/Browser/1.html /sdcard/"%self.dev_sn)

    def do_app_settings(self):
        self.logout(self.my_func_name(),"...")
        self.locate("Accept & continue",self.DIR_NONE)
        self.locate("Next",self.DIR_NONE)

    def measure(self):
        self.logout(self.my_func_name(),"...")
        self.locate("Search or type URL",self.DIR_NONE)
        os.system("adb -s %s shell input text file:///sdcard/1.html"%self.dev_sn)
        self.device.press.enter()
        time.sleep(3)
        self.icon_click()
        time.sleep(3)
        self.swipe_vert(5,self.SWIPE_DIR_UP)
        self.swipe_vert(5,self.SWIPE_DIR_DOWN)
        self.icon_click()

if __name__=="__main__": 
    os.system("adb -s %s root"%dev_sn)
    kill_process(dev_sn,"native_agent")
    np_chrome = ["Chrome","./res/Browser/Chrome_M42.apk",""]
    chrome_fps_test = chrome_fps(dev_sn,np_chrome)
    chrome_fps_test.exec_test()
    print("result of chrome_fps_test is %sfps"%chrome_fps_test.result)
