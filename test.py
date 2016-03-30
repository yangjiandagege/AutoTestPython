import os
import time
import re
import inspect
import logging
from uiautomator import Device

class test(object):
    dev_sn = ""
    dev_displayHeight = 0
    dev_displayWidth = 0
    icon_x = 0
    icon_y = 0
    app_name = ""
    app_path = ""
    app_package_name = ""
    class_name = ""
    result = ""
    install_time = ""
    device = Device();

    DIR_VERT, DIR_HORIZ ,DIR_NONE = range(3)
    SWIPE_DIR_UP, SWIPE_DIR_DOWN, SWIPE_DIR_LEFT, SWIPE_DIR_RIGHT = range(4)

    def __init__(self,sn,app):
        self.dev_sn = sn
        self.device = Device(self.dev_sn)
        self.dev_displayHeight = self.device.info['displayHeight']
        self.dev_displayWidth = self.device.info['displayWidth']
        self.icon_x = self.dev_displayWidth * 12 / 100
        self.icon_y = self.dev_displayHeight * 52 / 100
        self.is_app_settings_done = False
        if len(app) > 0 and app[0] != '':
            self.app_name = app[0]
        if len(app) > 1 and app[1] != '':
            self.app_path = app[1]
            self.app_package_name = self.get_package_name()
            self.install_app()
        if len(app) > 2 and app[2] != '':
            self.app_package_name = app[2]
        else:
            self.app_package_name = os.popen("adb -s %s shell pm list package | grep -i %s | awk -F ':' '{print$2}'"%(self.dev_sn,self.app_name)).read().strip("\r\n")
        self.set_app_settings_done_flag()
        self.clean_result()
        self.load_resource()

    def get_package_name(self):
        p = re.compile(r"package: name=\'([\w+.]*)\'")
        s = os.popen("./aapt dump badging  %s | grep -i package"%(self.app_path)).read()
        package_name = re.findall(p,s)
        return ''.join(package_name)

    def icon_click(self):
        os.system("adb -s %s shell input tap %s %s"%(self.dev_sn,self.icon_x,self.icon_y))

    def my_func_name(self):
        return inspect.stack()[1][3]

    def logout(self,function_name,log):
        print ">>> (%s) [%s.%s] :"%(self.app_name, self.__class__.__name__, function_name)+log

    def is_AppBench_root_page(self):
        if self.device(text="AppBench").exists and self.device(text="Tutorial").exists:
            return True
        else:
            return False

    def wait_for_fps_result(self):
        self.logout(self.my_func_name(),"...")
        while True:
            if self.is_AppBench_root_page() == False:
                if self.device(text="AppBench").exists:
                    return True
                else:
                    continue
            else:
                return False

    def swipe_vert(self,swipe_times,direction):
        if direction == self.SWIPE_DIR_UP:
            src_x = self.dev_displayWidth / 2
            src_y = self.dev_displayHeight * 4 / 5
            des_x = self.dev_displayWidth / 2
            des_y = self.dev_displayHeight * 1 / 5
        elif direction == self.SWIPE_DIR_DOWN:
            src_x = self.dev_displayWidth / 2
            src_y = self.dev_displayHeight * 1 / 5
            des_x = self.dev_displayWidth / 2
            des_y = self.dev_displayHeight * 4 / 5
        else:
            self.logout(self.my_func_name(),"direction is error...")
            return False
        for i in range(swipe_times):
            self.device.swipe(src_x,src_y,des_x,des_y,steps=20)
        return True


    def swipe_horiz(self,swipe_times,direction):
        if direction == self.SWIPE_DIR_RIGHT:
            src_x = self.dev_displayWidth  * 1 / 5
            src_y = self.dev_displayHeight / 3
            des_x = self.dev_displayWidth * 4 / 5
            des_y = self.dev_displayHeight  / 2
        elif direction == self.SWIPE_DIR_LEFT:
            src_x = self.dev_displayWidth  * 4 / 5
            src_y = self.dev_displayHeight / 3
            des_x = self.dev_displayWidth * 1 / 5
            des_y = self.dev_displayHeight  / 3
        else: 
            self.logout(self.my_func_name(),"direction is error...")
            return False
        for i in range(swipe_times):
            self.device.swipe(src_x,src_y,des_x,des_y,steps=20)
        return True

    def set_app_settings_done_flag(self):
        if "1" in os.popen("adb -s %s shell ls /data/data/%s | grep -c shared_prefs"%(self.dev_sn,self.app_package_name)).read(): 
            self.is_app_settings_done = True
        else:
            self.is_app_settings_done = False

    def back_to_AppBench_root_page(self):
        for i in range(10):
            if self.is_AppBench_root_page() == True:
                break
            else:
                self.device.press.back()
                time.sleep(1)

    def locate(self,option_name,direction):
        if direction == self.DIR_VERT:
            self.device(scrollable=True).scroll.vert.to(text=option_name)
            self.device(text=option_name).click.wait()
        elif direction == self.DIR_HORIZ:
            self.device(scrollable=True).scroll.horiz.to(text=option_name) 
            self.device(text=option_name).click.wait()
        else:
            self.device(text=option_name).click.wait()
 
    def start_native_agent(self):
        self.logout(self.my_func_name(),"...")
        cmds = ["cp /sdcard/appbench/native_agent /data/local/tmp/",
                "chmod 777 /data/local/tmp/native_agent",
                "cp /sdcard/appbench/perf /data/local/tmp/",
                "chmod 777 /data/local/tmp/perf",
                "cp /sdcard/appbench/screencap /data/local/tmp/",
                "chmod 777 /data/local/tmp/screencap",
                "/data/local/tmp/native_agent > agent_log.txt &"
                ]
        if "0" in os.popen("adb -s %s shell ps | grep -c native_agent"%self.dev_sn).read():
            self.logout(self.my_func_name(),"start native_agent now")
            for cmd in cmds:
                os.system("adb -s %s shell "%self.dev_sn+cmd)
        else:
            self.logout(self.my_func_name(),"native_agent is running")

    def load_resource(self):
        self.logout(self.my_func_name(),"...")

    def install_app(self):
        if "1" in os.popen("adb -s %s shell ls /data/data | grep -c "%self.dev_sn+self.app_package_name).read():
            self.logout(self.my_func_name(),"%s app has been installed."%self.app_name)
        else:
            self.logout(self.my_func_name(),"app %s is installing now."%self.app_name)
            time_start = time.time()
            os.system("adb -s %s install "%self.dev_sn+self.app_path)
            time_end = time.time()
            self.install_time = time_end - time_start

    def launch_app(self,app_name):
        self.logout(self.my_func_name(),"...")
        if self.device.screen == "off":
            os.system("adb -s %s shell input keyevent 82"%self.dev_sn)
        else:
            os.system("adb -s %s shell input keyevent 26"%self.dev_sn)
            time.sleep(3)
            os.system("adb -s %s shell input keyevent 82"%self.dev_sn)
        time.sleep(3)
        self.device.press.home()
        self.device(description='Apps').click.wait()
        self.locate("Apps",self.DIR_NONE)
        self.locate(app_name,self.DIR_HORIZ)

    def select_test_mode(self):
        self.logout(self.my_func_name(),"...")

    def start_app_from_AppBench(self):
        self.logout(self.my_func_name(),"...")
        self.back_to_AppBench_root_page()
        self.locate(self.app_package_name,self.DIR_VERT)
        self.locate("Measure",self.DIR_NONE)
        time.sleep(1)
        if "0" in os.popen("adb -s %s shell ps | grep -c native_agent"%self.dev_sn).read():
            return False
        return True

    def do_app_settings(self):
        self.logout(self.my_func_name(),"...")
        
    def measure(self):
        self.logout(self.my_func_name(),"...")

    def clean_result(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s shell rm -rf /sdcard/appbench/%s"%(self.dev_sn,self.app_package_name))
        time.sleep(3)

    def collect_result(self):
        self.logout(self.my_func_name(),"...")

    def stop_app(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s shell am force-stop %s"%(self.dev_sn,self.app_package_name))

    def stop_appbench(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s shell am force-stop com.intel.appbench"%self.dev_sn)

    def exec_test(self):
        self.logout(self.my_func_name(),"...")

class test_fps(test):
    def select_test_mode(self):
        self.logout(self.my_func_name(),"...")
        self.back_to_AppBench_root_page()
        self.device(description="More options").click.wait()
        self.locate("Settings",self.DIR_NONE)
        self.locate("Metric Options",self.DIR_NONE)
        self.locate("Basic Metric",self.DIR_NONE)
        self.logout(self.my_func_name(),"Basic Metric...")
        self.device.press.back()

    def collect_result(self):
        self.logout(self.my_func_name(),"...")
        result_path = os.popen("adb -s %s shell find /sdcard/appbench/%s -name summary.data"%(self.dev_sn,self.app_package_name)).read().strip("\r\n")
        self.logout(self.my_func_name(),"result path is %s"%result_path)
        p = re.compile(r"AvgFPS=([\d+.]*)fps") 
        result_content = os.popen("adb -s %s shell cat %s"%(self.dev_sn,result_path)).read()
        self.result = ''.join(re.findall(p,result_content))

    def exec_test(self):
        self.start_native_agent()
        if self.is_AppBench_root_page() == False:
            self.launch_app("AppBench")
        self.select_test_mode()
        while self.start_app_from_AppBench() == False:
            self.stop_app()
            self.stop_appbench()
            time.sleep(3)
            self.start_native_agent()
            time.sleep(3)
            self.launch_app("AppBench")
        if self.is_app_settings_done == False:
            self.do_app_settings()
        self.measure()
        self.wait_for_fps_result()
        self.back_to_AppBench_root_page()
        if self.app_package_name != "com.android.launcher":
            self.stop_app()
        self.collect_result()


class test_launch_time(test):
    def __init__(self,sn,app):
        super(test_launch_time,self).__init__(sn,app)
        self.load_png_for_launch_time()

    def load_png_for_launch_time(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s push ./res/%s/%s.bin /sdcard/appbench/%s/%s.bin"%(self.dev_sn,self.app_package_name,self.app_package_name,self.app_package_name,self.app_package_name))

    def select_test_mode(self):
        self.logout(self.my_func_name(),"...")
        self.back_to_AppBench_root_page()
        self.device(description="More options").click.wait()
        self.locate("Settings",self.DIR_NONE)
        self.locate("Metric Options",self.DIR_NONE)
        self.locate("Launch Time",self.DIR_NONE)
        self.logout(self.my_func_name(),"Launch Time...")
        self.device.press.back()

    def collect_result(self):
        self.logout(self.my_func_name(),"...")
        os.system("adb -s %s pull /sdcard/appbench/%s/launchtime/launch_time.txt ./"%(self.dev_sn,self.app_package_name))
        result_log = open('launch_time.txt')
        results = result_log.read()
        all_results = re.findall("(\d+)ms",results)
        sum_result=0
        for result in all_results:
            int_result = int(result)
            sum_result = sum_result + int_result
        os.system("rm launch_time.txt")
        self.result = sum_result/len(all_results)
    
    def get_agent_log_line_number(self):
        result = os.popen("awk '{print NR}' agent_log.txt | tail -n1").read().strip("\r\n")
        return result

    def is_get_launch_time_done(self,from_line_number):
        if "0" in os.popen("sed -n '%s,$p' agent_log.txt | grep -c 'I: launch time '"%from_line_number).read():
            return False
        else:
            return True

    def measure(self):
        self.logout(self.my_func_name(),"...")
        log_line_number = 1
        timeout = 90
        while self.is_get_launch_time_done(log_line_number) == False:
            log_line_number = self.get_agent_log_line_number()
            time.sleep(3)
            timeout = timeout - 3
            if timeout <= 0:
                break
        self.icon_click()

    def exec_test(self):
        self.start_native_agent()
        if self.is_AppBench_root_page() == False:
            self.launch_app("AppBench")
        self.select_test_mode()
        while self.start_app_from_AppBench() == False:
            self.stop_app()
            self.stop_appbench()
            time.sleep(3)
            self.start_native_agent()
            time.sleep(3)
            self.launch_app("AppBench")
        if self.is_app_settings_done == False:
            self.do_app_settings()
        self.measure()
        self.stop_appbench()
        if self.app_package_name != "com.android.launcher":
            self.stop_app()
        self.collect_result()
