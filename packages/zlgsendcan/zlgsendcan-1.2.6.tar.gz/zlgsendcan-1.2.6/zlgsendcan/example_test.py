from zlgsendcan.zlgserver import *
"""---------------------第一步初始化周立功设备,具体参数含义请进入这个类查看------------------"""
zlg_init = MessageDate('can', 0, {'zcy': '500kbps 80%', 'sjy': '2Mbps 80%'})

"""---------------------第二步获取dbc文件解析的db对象做成全局变量调用----------------------"""
dbcpath = 'D:\***\***.dbc'
get_dbc_db(dbcpath)

"""------------------第三步组装报文数据和发送信号------------------ 
    注意点：
        1、报文里面cycle_time如果不传，将自动获取dbc定义的周期时间，is_crc为0是不经过crc校验，1则经过，不传则默认为0，但crc涉及到机密，请结合本安装包自行在自己的工程里做crc脚本校验
        2、ZlgSend发送can信号会启动守护线程去发，主线程停止信号即停止发送
"""
# 多个报文发送组装数据格式及发送方式
def send_many_msg():
    many_msg_data = {
        "GW_BCS_2_B": {"GW_BCS_2_B": {"BCS_VehSpdVD": 1, "BCS_VehSpd": 120}, "send_num": '-1', "cycle_time": 100,
                       'is_crc': '0'},
        "GW_BCS_2_BB": {"GW_BCS_2_BB": {"BCS_VehSpdVD": 1, "BCS_VehSpd": 120}, "send_num": '-1', "cycle_time": 100,
                        'is_crc': '0'}}
    for k, v in many_msg_data.items():
        ZlgSend(zlg_init, v, dbcpath)


# 单个报文发送组装数据格式及发送方式
def send_single_msg():
    sig_msg_data = {
        "GW_BCS_2_B": {"BCS_VehSpdVD": 1, "BCS_VehSpd": 120},
        "send_num": '-1', "cycle_time": 100, 'is_crc': '0'}
    ZlgSend(zlg_init, sig_msg_data, dbcpath)


# 等差发送格式（信号值变化）
def send_change_msg():
    singnal_change = {"GW_EMS_1_B": {
        "GW_EMS_1_B": {"EMS_EngSt": 1, "EMS_FuelPulse": {"步长": '1000', "最大值": '65535', "最小值": '0'}},
        "send_num": '300', "cycle_time": 100, 'is_crc': '0'}}
    ZlgSend(zlg_init, singnal_change, dbcpath)


if __name__ == '__main__':
    send_many_msg()
    # send_single_msg()
    # send_change_msg()
