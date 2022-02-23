import dearpygui.dearpygui as dpg

from callbacks import *
from util import *

dpg.create_context()

with dpg.window(tag="main_window"):
    with dpg.menu_bar():
        dpg.add_menu_item(label="About", callback=about_callback)

    # Create tab context
    with dpg.tab_bar():
        # Transmit File tab context
        with dpg.tab(label="Transmit File"):
            dpg.add_text(default_value="IP Address :")

            # Set horizontal layout of input text and button
            with dpg.group(horizontal=True):
                ip_text = dpg.add_input_text(tag="ip_text", scientific=True, hint="Enter destination IP Address")
                save_button = dpg.add_button(label="Save", width=100, callback=save_button_callback)

            dpg.add_text(default_value="Saved IPs :")

            # Set horizontal layout of list box and button
            with dpg.group(horizontal=True):
                ip_list_box = dpg.add_listbox(tag="ip_list_box")
                select_button = dpg.add_button(label="Select", width=100, callback=select_button_callback)

            dpg.add_text(default_value="\nFile :")

            # Set horizontal layout of input text and button
            with dpg.group(horizontal=True):
                path_text = dpg.add_input_text(tag="path_text", hint="Enter file path")
                browse_button = dpg.add_button(label="Browse", width=100, callback=browse_button_callback)

            dpg.add_text(default_value="\n\n")

            # Make responsive the button
            # Set grid layout to locate the button
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text(default_value="")
                    transmit_button = dpg.add_button(tag="transmit_button", label="Transmit", width=-1,
                                                     callback=transmit_button_callback)
                    dpg.add_text(default_value="")

            dpg.add_text(default_value="\n")
            dpg.add_separator()
            dpg.add_text(default_value="\n")

            # Create progress bar context
            with dpg.group(horizontal=True):
                dpg.add_text(default_value="Progress :")
                progress_bar = dpg.add_progress_bar(tag="pb", default_value=0.0)

            # Create log window item
            dpg.add_text(default_value="\n")
            dpg.add_text(default_value="Log :")
            dpg.add_input_text(tag="transmitter_log", width=-1, height=-1, multiline=True, readonly=True)

        # Receive File tab context
        with dpg.tab(label="Receive File"):
            dpg.add_text(default_value=f"Host IP : {get_host_ip()}")
            dpg.add_text(default_value="\n")
            dpg.add_text(default_value="Destination Directory :")

            with dpg.group(horizontal=True):
                destination_text = dpg.add_input_text(tag="destination_text", hint="Enter destination directory")
                browse_button_1 = dpg.add_button(label="Browse", width=100, callback=browse_button_1_callback)

            dpg.add_text(default_value="\n")

            # Make responsive the button
            # Set grid layout to locate the button
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text(default_value="")
                    receive_button = dpg.add_button(tag="receive_button", label="Receive", width=-1,
                                                    callback=receive_button_callback)
                    dpg.add_text(default_value="")

            dpg.add_text(default_value="\n")
            dpg.add_separator()
            dpg.add_text(default_value="\n")

            # Create progress bar context
            with dpg.group(horizontal=True):
                dpg.add_text(default_value="Progress :")
                progress_bar_1 = dpg.add_progress_bar(tag="pb_1", default_value=0.0)

            # Create log window item
            dpg.add_text(default_value="\n")
            dpg.add_text(default_value="Log :")
            dpg.add_input_text(tag="receiver_log", width=-1, height=-1, multiline=True, readonly=True)

with dpg.file_dialog(directory_selector=False, show=False, id="file_dialog", callback=file_dialog_callback, height=400):
    dpg.add_file_extension(".*", color=(150, 255, 150, 255))

with dpg.file_dialog(directory_selector=True, show=False, id="file_dialog_1", callback=file_dialog_1_callback,
                     height=400):
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.window(label="Reminder", modal=True, show=False, id="modal_id"):
    dpg.add_text("Please start receiving operation!")
    dpg.add_separator()

    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():
            dpg.add_button(label="Continue", width=100, callback=continue_transmitting_callback)
            dpg.add_button(label="Cancel", width=100, callback=lambda: dpg.configure_item("modal_id", show=False))

with dpg.window(label="About", modal=True, show=False, id="modal_about", width=380):
    dpg.add_text("Version : v0.1")
    dpg.add_text("Author : dgkngzlr")
    dpg.add_separator()

    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_text(default_value="")
            dpg.add_button(label="Close", width=100, callback=lambda: dpg.configure_item("modal_about", show=False))
            dpg.add_text(default_value="")

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [129, 133, 137])

with dpg.font_registry():
    default_font = dpg.add_font("./fonts/UbuntuMono-Regular.ttf", 15)

dpg.bind_theme(global_theme)
dpg.bind_font(default_font)

if __name__ == "__main__":
    fetch_saved_ips()

    dpg.set_primary_window("main_window", True)
    dpg.create_viewport(title="Transfer File", width=400, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
