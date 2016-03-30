from chrome_fps import chrome_fps 
from test import test_launch_time
from common import dev_sn
from common import kill_process
import time
import os

class contacts_launch_time(test_launch_time):
    def load_resource(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/%s/Contacts_100.vcf /sdcard/Contacts_100.vcf"%(self.dev_sn,self.app_package_name))
        self.launch_app("Contacts")
        if self.device(text="Import contacts").exists:
            self.locate("Import contacts",self.DIR_NONE)
            self.locate("Import from storage",self.DIR_NONE)
        time.sleep(5)
        os.system("adb -s %s shell am force-stop %s"%(self.dev_sn,self.app_package_name))

class gallery_launch_time(test_launch_time):
    def load_resource(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/%s/objects /sdcard/objects"%(self.dev_sn,self.app_package_name))

class message_launch_time(test_launch_time):
    def load_resource(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/%s/Messaging_50send_50receive.db /data/data/com.android.providers.telephony/databases/mmssms.db"%(self.dev_sn,self.app_package_name))

music_sum = 0

os.system("adb -s %s root"%dev_sn)
time.sleep(3)
os.system("adb wait-for-device")
kill_process(dev_sn,"native_agent")

np_music = ["Music","","com.android.music"] #null
np_chrome = ["Chrome","./res/com.android.chrome/Chrome_M42.apk","com.android.chrome"] #null
np_contacts = ["Contacts","","com.android.contacts"]
np_dialer = ["Phone","","com.android.dialer"] #null
np_gallery = ["Gallery","","com.android.gallery3d"]
np_message = ["Messaging","","com.android.mms"]


music_launch_time_test = test_launch_time(dev_sn,np_music)
chrome_launch_time_test = test_launch_time(dev_sn,np_chrome)
contacts_launch_time_test = contacts_launch_time(dev_sn,np_contacts)
dialer_launch_time_test = test_launch_time(dev_sn,np_dialer)
gallery_launch_time_test = gallery_launch_time(dev_sn,np_gallery)
message_launch_time_test = message_launch_time(dev_sn,np_message)

for i in range(5):
    os.system("adb -s %s reboot"%dev_sn)
    os.system("adb wait-for-device")
    time.sleep(60)
    os.system("adb -s %s root"%dev_sn)
    time.sleep(3)

    music_launch_time_test.exec_test()
    print("result of music_launch_time_test is %sms"%music_launch_time_test.result)
    
    chrome_launch_time_test.exec_test()
    print("result of chrome_launch_time_test is %sms"%chrome_launch_time_test.result)
    
    contacts_launch_time_test.exec_test()
    print("result of contacts_launch_time_test is %sms"%contacts_launch_time_test.result)
    
    dialer_launch_time_test.exec_test()
    print("result of dialer_launch_time_test is %sms"%dialer_launch_time_test.result)
    
    gallery_launch_time_test.exec_test()
    print("result of gallery_launch_time_test is %sms"%gallery_launch_time_test.result)
    
    message_launch_time_test.exec_test()
    print("result of message_launch_time_test is %sms"%message_launch_time_test.result)

print("result of music_launch_time_test is %sms"%music_launch_time_test.result)
print("result of chrome_launch_time_test is %sms"%chrome_launch_time_test.result)
print("result of contacts_launch_time_test is %sms"%contacts_launch_time_test.result)
print("result of dialer_launch_time_test is %sms"%dialer_launch_time_test.result)
print("result of gallery_launch_time_test is %sms"%gallery_launch_time_test.result)
print("result of message_launch_time_test is %sms"%message_launch_time_test.result)
