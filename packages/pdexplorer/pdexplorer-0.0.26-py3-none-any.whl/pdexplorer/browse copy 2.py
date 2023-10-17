from ._dataset import current

# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Pandas.py
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Browser_Paned.py
import PySimpleGUI as sg
import pandas as pd
import time
import threading


window = sg.Window("Table", [[]], grab_anywhere=False, resizable=True)


def display_dataframe_plus(notify_event):
    """Function to display the DataFrame using PySimpleGUI Table"""
    previous_df = current.df.copy()
    first_run = True

    while not notify_event.is_set():  # Check the event flag
        current_df = current.df.copy()
        if not current_df.equals(previous_df) or first_run:
            print("DataFrame has changed:")
            sg.set_options(auto_size_buttons=True)
            data = []
            header_list = []
            data = (
                current_df.values.tolist()
            )  # read everything else into a list of rows
            header_list = current_df.columns.tolist()

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
            # event, values = window.read(timeout=1000)
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                notify_event.set()  # Set the exit event to signal the thread to exit
                window.close()
                break
            print(event)
            print(values)

            previous_df = current_df.copy()
        first_run = False
        time.sleep(1)
    print("end display")


def browse():
    # global first_run
    global browse_notify_event
    global browse_thread
    # first_run = True
    # # Create an Event to notify the display thread of changes #
    # window.close()
    browse_notify_event = threading.Event()

    # Create a separate thread to display the DataFrame when changes occur #
    # browse_thread = threading.Thread(target=display_dataframe, args=(browse_notify_event,))
    browse_thread = threading.Thread(
        target=display_dataframe_plus, args=(browse_notify_event,)
    )
    browse_thread.start()
    # browse_thread.join()
    print("end browse")


###########################################################################
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
