from test import test_fps 
from common import dev_sn
from common import kill_process
import os
import time

class contacts_fps(test_fps):
    def load_resource(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/Contacts/Contacts_100.vcf /sdcard/"%self.dev_sn)

    def measure(self):
        self.logout(self.my_func_name(),"...")
        if self.device(text="Import contacts").exists:
            self.locate("Import contacts",self.DIR_NONE)
            self.locate("Import from storage",self.DIR_NONE)
        time.sleep(3)
        self.icon_click()
        self.swipe_vert(5,self.SWIPE_DIR_UP)
        #self.swipe_vert(5,self.SWIPE_DIR_DOWN)
        self.icon_click()

if __name__=="__main__": 
    os.system("adb -s %s root"%dev_sn)
    kill_process(dev_sn,"native_agent")
    np_contacts = ["Contacts","","com.android.contacts"]
    contacts_fps_test = contacts_fps(dev_sn,np_contacts)
    contacts_fps_test.exec_test()
    print("result of contacts_fps_test is %sfps"%contacts_fps_test.result)
