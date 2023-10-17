from ._dataset import current

# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Pandas.py
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Browser_Paned.py
import PySimpleGUI as sg

window = sg.Window("Table", [[]], grab_anywhere=False, resizable=True)
window.close_destroys_window = True


def guify(df):
    global window
    # df = current.df

    sg.set_options(auto_size_buttons=True)
    data = []
    header_list = []
    data = df.values.tolist()  # read everything else into a list of rows
    header_list = df.columns.tolist()

    layout = [
        [
            sg.Table(
                values=data,
                headings=header_list,
                display_row_numbers=True,
                auto_size_columns=False,
                num_rows=min(47, len(data)),
            )
        ]
    ]

    window = sg.Window("Table", layout, grab_anywhere=False, resizable=True)
    event, values = window.read(timeout=1000)
    print(event)
    print(values)


import pandas as pd
import time
import threading


def display_dataframe(notify_event):
    """Function to display the DataFrame when changes occur"""
    previous_df = current.df.copy()

    while not notify_event.is_set():  # Check the event flag
        current_df = current.df.copy()
        if not current_df.equals(previous_df):
            print("DataFrame has changed:")
            print(current_df)
            previous_df = current_df.copy()
        time.sleep(1)


def display_dataframe_plus(notify_event):
    """Function to display the DataFrame using PySimpleGUI Table"""
    previous_df = current.df.copy()

    while not notify_event.is_set():  # Check the event flag
        current_df = current.df.copy()
        if not current_df.equals(previous_df):
            print("DataFrame has changed:")

            # print(current_df)
            window.close()
            from time import sleep

            # sleep(5)
            guify(current_df)

            previous_df = current_df.copy()
        time.sleep(1)


# # Create an Event to notify the display thread of changes #
browse_notify_event = threading.Event()


# Create a separate thread to display the DataFrame when changes occur #
# browse_thread = threading.Thread(target=display_dataframe, args=(browse_notify_event,))
browse_thread = threading.Thread(
    target=display_dataframe_plus, args=(browse_notify_event,)
)
browse_thread.start()


def browse():
    pass


# atexit.register doesn't work to clean up the thread... but this does: #
# https://stackoverflow.com/questions/58910372/script-stuck-on-exit-when-using-atexit-to-terminate-threads #
def monitor_thread():
    main_thread = threading.main_thread()
    main_thread.join()
    browse_notify_event.set()
    browse_thread.join()


monitor = threading.Thread(target=monitor_thread)
monitor.daemon = True
monitor.start()
