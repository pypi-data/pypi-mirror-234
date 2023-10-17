import cantools
import binascii
import re


class get_signal_data1(object):

    # data1 = {'GW_SRS_2_B': {'SRS_AirbagFaultSt': '1'}}
    def __init__(self, DBC_file=None):
        self.DBC_File = DBC_file
        self.db = cantools.database.load_file(self.DBC_File, strict=False)


class DbcInit:
    def __init__(self, msgname=None, data: dict = None, db_obj=None):
        self.crc = False
        self.pro_name = None
        self.six_data = None
        self.data = data
        self.db = db_obj
        self.msg_name = msgname
        if self.msg_name is not None:
            self.example_message = self.db.get_message_by_name(self.msg_name)
        # self.msg_id =self.example_message.__dict__['_frame_id']

    @staticmethod
    def deal_(x):
        a = {}
        a[x] = 0
        return a

    def init_dbc_parser(self, data=None):
        try:
            # sig_l = self.example_message.signal_tree
            # if type(sig_l[0]) == dict:
            #     for s_1 in sig_l:
            #         if type(s_1) == dict:
            #             for i1, i3 in s_1.items():
            #                 if type(i3) == dict:
            #                     for sk, sv in self.data.items():
            #                         # s_list = list(i1.values())
            #                         for k1, v1 in i3.items():
            #                             if sk == i1 and k1 == int(sv):
            #                                 # for i2 in list(i1.values())[idx]:
            #                                 sig_value[sk] = int(sv)
            #                                 sig_value[v1[0]] = 0
            #                                 break
            #                         else:
            #                             sig_value[sk] = int(sv)
            #
            #         else:
            #             for sk, sv in self.data.items():
            #                 if s_1 == sk:
            #                     sig_value[sk] = int(sv)
            #                 else:
            #                     sig_value[s_1] = 0
            # else:
            # 遍历每个信号
            # 兼容多路复用
            sig_value = {}
            multiplexer_value = None
            for signal in self.example_message.signals:
                si = self.example_message.get_signal_by_name(signal.name)
                if signal.is_multiplexer:
                    for k, v in self.data.items():
                        if k == signal.name:
                            multiplexer_value = int(v)
                    sig_value[signal.name] = 0 if si.minimum is None else si.minimum
                    continue  # 忽略多路复用信号本身

                # 检查信号的多路复用标识符是否与给定的值匹配
                if signal.multiplexer_ids is None:
                    sig_value[signal.name] = 0 if si.minimum is None else si.minimum
                elif signal.multiplexer_ids == [multiplexer_value]:
                    # 解析与多路复用信号关联的信号
                    sig_value[signal.name] = 0 if si.minimum is None else si.minimum
            sig_data = self.data

            # {'SRS_DriverSeatBeltSt': '0'}
            if data is not None:
                for i, i1 in data.items():
                    sig_value[i] = int(i1)
            else:
                for i, i1 in sig_data.items():
                    sig_value[i] = int(i1)

            sig_data1 = self.example_message.encode(sig_value, scaling=True, strict=True)
            a = binascii.b2a_hex(sig_data1)
            # 16进制
            self.six_data = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", a.decode('utf8')).split()
        except Exception as e:
            print('dbc解析错误', e)
            return

    def dbc_parser(self, data=None):
        self.init_dbc_parser(data)
        result = [int(i, 16) for i in self.six_data]
        return result

    def DBC_decoder(self, name, data):
        data_decoder = self.db.decode_message(name, data)
        return data_decoder

    @property
    def message_name(self):
        return self.Message_Name

    @property
    def message_length(self):
        return self.example_message.length

    @property
    def message_cycle_time(self):
        return self.example_message.cycle_time

    @property
    def message_frame_id(self):
        return self.example_message.frame_id

    @property
    def message_signas(self):
        return self.example_message.signals


class GlobleValue:
    thread_obj = {}
    global_msg = {}
    global_msg2 = {}
    global_msg3 = {}
    can_conf = {'can_type': 'can', 'chan': 0, 'zcy': None, 'sjy': None}
    zlginit = None
    dbc_path = None
    thread_run = False
    flag_trace = False
    thread_sigchange_flag = False
    data_log = []
    sql_flag = False
    dbc_init = None


if __name__ == '__main__':
    data1 = {'CCO_Active': '2'}
    a = get_signal_data1(
        'D:\data\P05-001-020MM01 C_Matrix for HEV SC_CANFD_V5.0_HEV.dbc').db
    ob = DbcInit('ESP8', data1, db_obj=a)
    print(ob.dbc_parser())
    print(ob.example_message.__dict__)
