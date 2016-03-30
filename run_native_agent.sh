adb shell cp /sdcard/appbench/native_agent /data/local/tmp/
adb shell chmod 777 /data/local/tmp/native_agent
adb shell cp /sdcard/appbench/perf /data/local/tmp/
adb shell chmod 777 /data/local/tmp/perf
adb shell cp /sdcard/appbench/screencap /data/local/tmp/
adb shell chmod 777 /data/local/tmp/screencap
adb shell /data/local/tmp/native_agent > agent_log.txt &

