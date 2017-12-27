Monkey = {
    # 基础参数
    'head':
        {
            '-p': 'com.sixty.nidoneClient',   # 待测应用包名
            '--throttle': '5',    # 按键操作间隔，单位毫秒
            '-s': '',     # 指定产生随机事件种子值，相同的种子值产生相同的事件序列。如： -s 200
            },
    # 发送的事件类型
    'event_type':
        {
            '--pct-touch': '',    # 指定触摸事件的百分比
            '--pct-motion': '',   # 滑动事件
            '--pct-trackball': '',    # 轨迹球事件
            '--pct-nav': '',  # 导航事件 up/down/left/right
            '--pct-majornav': '',     # 主要导航事件 back key 、 menu key
            '--pct-syskeys': '',      # 系统按键事件 Home 、Back 、startCall 、 endCall 、 volumeControl
            '--pct-anyevent': '',     # 任意事件
            '--pct-appswitch': ''     # activity之间的切换
            },
    # 调试选项
    'debug_option':
        {
            '--dbg-no-events': False,    # 初始化启动的activity，但是不产生任何事件。
            '--hprof': False,   # 指定该项后在事件序列发送前后会立即生成分析报告  —— 一般建议指定该项
            '--ignore-crashes': True,  # 忽略崩溃
            '--ignore-timeouts': True,     # 忽略超时
            '--1gnore-security-exceptions': False,  # 忽略安全异常
            '--kill-process-after-error': False,    # 发生错误后直接杀掉进程
            '--monitor-native-crashes': True,      # 跟踪本地方法的崩溃问题
            '--wait-dbg': False,    # 知道连接了调试器才执行monkey测试。
            '-v': False,    # 缺省值，仅提供启动提示、测试完成和最终结果等少量信息
            '-v -v': False,     # 提供较为详细的日志，包括每个发送到Activity的事件信息
            '-v -v -v': True    # 最详细的日志，包括了测试中选中/未选中的Activity信息
            },
    'time': '50000'   # 事件个数
}


Mky = ['monkey', ]


def monkey_config():
    for i in Monkey['head']:
        if Monkey['head'][i]:
            Mky.append(i)
            Mky.append(Monkey['head'][i])
    for j in Monkey['event_type']:
        if Monkey['event_type'][j]:
            Mky.append(j)
    for m in Monkey['debug_option']:
        if Monkey['debug_option'][m]:
            Mky.append(m)
    Mky.append(Monkey['time'])
    monkey = ' '.join(Mky)
    return Monkey['head']['-p'], monkey
