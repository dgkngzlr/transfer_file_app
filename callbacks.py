import dearpygui.dearpygui as dpg

from util import *

FILE_NAME = ""
FILE_PATH = ""


def save_button_callback(sender, app_data, user_data):
    ip = dpg.get_value("ip_text")

    if ip != "":
        with open("./states/ip.txt", "a") as f:
            f.write(ip + "\n")


def select_button_callback(sender, app_data, user_data):
    dpg.set_value("ip_text", dpg.get_value("ip_list_box"))


def browse_button_callback(sender, app_data, user_data):
    dpg.show_item("file_dialog")


def browse_button_1_callback(sender, app_data, user_data):
    dpg.show_item("file_dialog_1")


def file_dialog_callback(sender, app_data, user_data):
    global FILE_NAME, FILE_PATH
    file_name = list(app_data['selections'].keys())[0]
    file_path = list(app_data['selections'].values())[0]

    dpg.set_value("path_text", file_path)

    FILE_NAME = file_name
    FILE_PATH = file_path


def file_dialog_1_callback(sender, app_data, user_data):
    file_path = app_data['file_path_name']
    dpg.set_value("destination_text", file_path)


def transmit_button_callback(sender, app_data, user_data):
    dpg.configure_item("modal_id", show=True)


def about_callback(sender, app_data, user_data):
    dpg.configure_item("modal_about", show=True)


# Transmit operation here
def continue_transmitting_callback(sender, app_data, user_data):
    dpg.configure_item("modal_id", show=False)
    if FILE_NAME.strip() != "" and dpg.get_value('ip_text').strip() != "":
        Logger.write("transmitter_log", f"File : {FILE_NAME.strip()}")
        Logger.write("transmitter_log", f"Destination : {dpg.get_value('ip_text').strip()}")
        Logger.write("transmitter_log", "File is transmitting, please wait ...")
        dpg.configure_item("transmit_button", enabled=False)
        Sender.send_file(file_path=FILE_PATH, dest_ip=dpg.get_value("ip_text").strip())
        Logger.write("transmitter_log", "File is transmitted")
    else:
        Logger.write("transmitter_log", "Fill in the fields above !", level="error")


# Receive operation here
def receive_button_callback(sender, app_data, user_data):
    if dpg.get_value("destination_text") != "":
        Logger.write("receiver_log", "File is receiving, please wait ...")
        dpg.configure_item("receive_button", enabled=False)
        Receiver.receive_file(dest_direct=dpg.get_value("destination_text"))
        Logger.write("receiver_log", "File is received !")
    else:
        Logger.write("receiver_log", "Fill in the fields above !", level="error")
