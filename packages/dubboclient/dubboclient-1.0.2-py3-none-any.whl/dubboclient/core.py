import json
import telnetlib
import logging


class DubboClient:

    def __init__(self, host, port):
        """
        实例化dubbo客户端对象
        :param host: dubbo服务地址
        :param port: dubbo服务端口
        """
        self.telnet = telnetlib.Telnet(host, port)

    def invoke(self, service_name, method_name, *args):
        """
        调用接口
        :param service_name: 服务名称
        :param method_name: 方法名称
        :param args: 方法参数列表
        :return: 接口响应数据
        """
        # 处理参数
        new_args = self._deal_args(args)
        logging.info(f"new_args=={new_args}")

        # 调用接口
        command = "invoke {}.{}({})\n".format(service_name, method_name, new_args)
        logging.info(f"command=={command}")
        self.telnet.write(command.encode())

        # 读取响应数据
        response_data = self.telnet.read_until("dubbo>".encode())
        logging.info(f"response_data=={response_data}")

        # 处理响应数据
        data = self._deal_response_data(response_data)
        return data

    @staticmethod
    def _deal_response_data(response_data):
        """处理响应数据"""
        all_data = response_data.decode()
        # 成功
        if "result:" in all_data:
            for line in all_data.split("\r\n"):
                if line.startswith("result:"):
                    data = line[8:]
                    return json.loads(data)
        else:
            return all_data

    @staticmethod
    def _deal_args(args):
        """处理参数"""
        args_str = ""
        for arg in args:
            args_str += json.dumps(arg) + ","
        return args_str[:-1]

    def close(self):
        """关闭连接对象"""
        if self.telnet:
            self.telnet.close()
            self.telnet = None

    def __del__(self):
        """销毁对象时，自动关闭连接"""
        self.close()
