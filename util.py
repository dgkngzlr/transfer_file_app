import dearpygui.dearpygui as dpg
import socket
import os


def fetch_saved_ips():
    """
        Fetch saved ips from /states/ip.txt. Then update ip_list_box.
    :return:
    """
    with open("./states/ip.txt", "r") as f:
        ip_list = f.readlines()

    dpg.configure_item("ip_list_box", items=ip_list)


def get_host_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_addr = s.getsockname()[0]

    return local_ip_addr


class Logger:

    @staticmethod
    def write(dest, msg, level="info"):
        if level == "info":
            dpg.set_value(dest, f"{dpg.get_value(dest)}INFO> {msg}\n")

        elif level == "warning":
            dpg.set_value(dest, f"{dpg.get_value(dest)}WARN> {msg}\n")

        elif level == "error":
            dpg.set_value(dest, f"{dpg.get_value(dest)}ERROR> {msg}\n")

        else:
            assert True, "Logger level error"

    @staticmethod
    def clean(dest):
        dpg.set_value(dest, "")


class Sender:

    @classmethod
    def send_msg(cls, msg, ip="127.0.0.1"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(60)

            s.bind((ip, 55055))
            s.listen()

            conn, addr = s.accept()
            conn.send(msg.encode())

    @classmethod
    def send_file(cls, file_path, ip="127.0.0.1"):
        file_name: str
        file_size = os.path.getsize(file_path)

        if os.name == "nt":
            file_name = file_path.split("\\")[-1]
        else:
            file_name = file_path.split("/")[-1]

        Sender.send_msg(file_name, ip=ip)
        Sender.send_msg(f"{file_size}", ip=ip)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(60)

            s.bind((ip, 55055))
            s.listen()

            conn, addr = s.accept()
            sent_size = 0
            dpg.configure_item('pb', default_value=sent_size / file_size)
            with open(file_path, "rb") as f:
                while sent_size < file_size:
                    bytes_ = f.read(1024)
                    conn.send(bytes_)
                    sent_size += 1024
                    dpg.configure_item('pb', default_value=sent_size / file_size)
            dpg.configure_item("transmit_button", enabled=True)
            dpg.configure_item('pb', default_value=0.0)
            Logger.write("transmitter_log", "File successfully transmitted !")


class Receiver:

    @classmethod
    def receive_msg(cls, from_="127.0.0.1") -> str:
        flag = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            while flag:
                try:
                    s.connect((from_, 55055))
                    flag = False
                except Exception as e:
                    pass

            msg = s.recv(1024)

        return msg.decode("utf-8")

    @classmethod
    def receive_file(cls, dest_direct, from_="127.0.0.1"):

        file_name = Receiver.receive_msg(from_)
        file_size = int(Receiver.receive_msg(from_))
        dest_path: str
        Logger.write("receiver_log", f"File : {file_name}")

        if os.name == "nt":
            dest_path = dest_direct + f"\\{file_name}"
        else:
            dest_path = dest_direct + f"/{file_name}"

        flag = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            while flag:
                try:
                    s.connect((from_, 55055))
                    flag = False
                except Exception as e:
                    pass

            received_size = 0

            dpg.configure_item('pb_1', default_value=received_size / file_size)
            with open(dest_path, "wb") as f:

                while received_size < file_size:
                    bytes_ = s.recv(1024)
                    f.write(bytes_)
                    received_size += 1024
                    dpg.configure_item('pb_1', default_value=received_size / file_size)
            dpg.configure_item('pb_1', default_value=0.0)
            dpg.configure_item("receive_button", enabled=True)
            Logger.write("receiver_log", "File successfully received !")


if __name__ == "__main__":
    pass
