"""A standalone GUI utility offering Perforce users the ability to check out files.

While this ability is available out of the box by directly using the official Perforce visual 
client (p4v), it's convenient to integrate it into the user's IDE. Most popular IDEs have 
an official Perforce plugin, but those that don't can use this utility to easily check out 
files before editing them.

Source:
    https://github.com/Dvd848/p4checkout

License:
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from typing import Optional, List, Tuple, Union, Callable, Dict
from collections.abc import Iterator
from collections import namedtuple
from pathlib import Path
from tkinter import ttk, messagebox

import importlib.resources
import tkinter as tk
import threading
import traceback
import argparse
import logging
import queue
import sys
import os
import re

import P4

VERSION = "0.1.0"

ChangeList = namedtuple("ChangeList", "id description")

class PerforceCheckout:
    CL_ID_NEW = -1
    CL_ID_DEFAULT = 0

    def __init__(self, file_path: str, **kwargs) -> None:
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(type(self).__name__)
        self.p4 = None
        self.p4args = {}

        allowed_kwargs = ["port", "client", "host", "user"]
        for k, v in kwargs.items():
            if k in allowed_kwargs:
                self.p4args[k] = v

        self._changelists = None
        self.connected = False

        if (not self.file_path.exists()):
            raise FileNotFoundError(f"File '{self.file_path}' does not exist!")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        if exc_type is not None:
            info = (exc_type, exc_val, exc_tb)
            self.logger.log(logging.ERROR, "Exception occurred", exc_info=info)
            if self.p4 is not None:
                for e in self.p4.errors:
                    self.logger.log(logging.ERROR, str(e))

    def connect(self) -> None:
        self.p4 = P4.P4()        
        for k, v in self.p4args.items():
            if v is not None:
                self.logger.info(f"Setting p4.{k} to {v}")
                setattr(self.p4, k, v)

        self.p4.connect()

        self.logger.info(f"P4 connected to {self.p4.port}, user = {self.p4.user}")
        self.connected = True

        if not "client" in self.p4args or self.p4args["client"] is None:
            self._set_client_by_file_path(self.file_path)

    def disconnect(self) -> None:
        if self.p4 is not None and self.connected:
            self.p4.disconnect()
            self.connected = False
            self.logger.info(f"P4 disconnected from {self.p4.port}")
    
    def is_connected(self) -> bool:
        return self.connected

    def _get_file_metadata(self, file_path: os.PathLike) -> Optional[P4.Spec]:
        try:
            file_metadata = self.p4.run_fstat(file_path)
            if len(file_metadata) == 1:
                # File was added in the past
                self.logger.debug("File exists in workspace")
                return file_metadata[0]
        except P4.P4Exception:
            if file_path.is_relative_to(self.p4.fetch_client(self.p4.client)["Root"]):
                # File is new
                self.logger.debug("File does not exist in workspace but is located under it")
                return None

        raise RuntimeError("Provided path is not under current client")
    
    @property
    def file_metadata(self) -> Optional[P4.Spec]:
        if not self.is_connected():
            raise RuntimeError("Must be connected in order to read metadata")
        return self._get_file_metadata(self.file_path)

    @property
    def _clients(self) -> Iterator[P4.Spec]:
        return self.p4.iterate_clients(["-u", self.p4.user])

    def _set_client_by_file_path(self, file_path: os.PathLike) -> None:
        self.logger.info(f"Locating client for '{file_path}'")

        for client in self._clients:
            self.p4.client = client["Client"]

            try:
                self._get_file_metadata(file_path)
                self.logger.info(f"Client identified as '{self.p4.client}'")
                return
            except RuntimeError:
                pass
        
        raise RuntimeError("Provided path is not under any known client")
        
    @property
    def changelists(self) -> Iterator[ChangeList]:
        if self._changelists is None:
            changelists = []
            changelists.append(ChangeList(self.CL_ID_NEW, "New"))
            changelists.append(ChangeList(self.CL_ID_DEFAULT, "default"))

            for cl in self.p4.iterate_changes(["-u", self.p4.user, "-c", self.p4.client]):
                assert(cl["Client"] == self.p4.client)
                assert(cl["User"] == self.p4.user)
                if cl["Status"] == "pending":
                    changelists.append(ChangeList(cl["Change"], cl["Description"]))
            self._changelists = tuple(changelists)
        return self._changelists
    
    def checkout(self, changelist_id: int, changelist_description: str) -> str:
        target_changelist = ""

        if changelist_id == self.CL_ID_NEW:
            if changelist_description == "":
                raise ValueError("New changelist description cannot be empty")
            changespec = {'Change': 'new', 'Description': changelist_description}
            changelist_result = self.p4.save_change(changespec)[0]
            self.logger.debug(f"New CL creation: Change spec: {changespec}, result: {changelist_result}")
            match = re.search(r'\bChange (\d+) created.', changelist_result)
            if not match:
                raise RuntimeError("Error checking out file")
            
            target_changelist = match.group(1)
            self.logger.info(f"New changelist created with id {target_changelist}")
        elif changelist_id == self.CL_ID_DEFAULT:
            target_changelist = "default"
        else:
            target_changelist = str(changelist_id)

        file_metadata = self._get_file_metadata(self.file_path)
        self.logger.debug(f"File metadata: {file_metadata}")
        if file_metadata is None:
            # New file - add it
            add_result = self.p4.run_add(f"-c{target_changelist}", self.file_path)
            self.logger.debug(f"Adding file: Target changelist: {target_changelist}, result: {add_result}")
        else:
            if "change" in file_metadata:
                raise RuntimeError(f"Error: File is already checked out in changelist '{file_metadata['change']}'")
            edit_result = self.p4.run_edit(f"-c{target_changelist}", self.file_path)
            self.logger.debug(f"Editing file: Target changelist: {target_changelist}, result: {edit_result}")
        self.logger.info(f"Done checking out file, CL: {target_changelist}")

        return target_changelist

class PerforceCheckoutGui:
    def __init__(self, file_path: str, p4args: Dict[str, str]) -> None:
        
        self.p4checkout = None
        self.logger = logging.getLogger(type(self).__name__)

        self.initialize_gui()
        self.initialize_state(file_path, p4args)

    def initialize_gui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Select Pending Changelist")
        self.root.geometry("320x300")
        self.load_icon()
        #self.root.attributes('-toolwindow', True)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        cl_select_label = tk.Label(self.main_frame, text="Add files to pending changelist:", 
                                   anchor=tk.W, justify=tk.LEFT)
        cl_select_label.grid(row=0, column=0, sticky=tk.W)
        
        self.select_box = ttk.Combobox(self.main_frame, values=[], state="readonly")
        self.select_box.grid(row=1, column=0, padx=5, pady=2, sticky=tk.E + tk.W)
        self.select_box.bind("<<ComboboxSelected>>", self.on_select)

        cl_desc_label = tk.Label(self.main_frame, text="Changelist description:", 
                                   anchor=tk.W, justify=tk.LEFT)
        cl_desc_label.grid(row=2, column=0, pady=2, sticky=tk.W)

        text_frame = tk.Frame(self.main_frame)
        text_frame.grid(row=3, column=0, padx=5, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.text_box = tk.Text(text_frame, state=tk.DISABLED)
        self.text_box.pack(fill="both", expand=True)

        footer_frame = tk.Frame(self.main_frame)
        footer_frame.grid(row=4, column=0, pady=(10, 0), padx=2, sticky=tk.E + tk.W)
        footer_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(footer_frame, orient='horizontal', mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, padx=5, sticky=tk.E + tk.W, columnspan=2)
        self.progress_bar_start()

        self.ok_button = tk.Button(footer_frame, text="OK", width="10", command=self.on_ok_button_click)
        self.ok_button.grid(row=1, column=0, padx=5, pady=(10, 0), sticky=tk.E)
        self.ok_button.config(state=tk.DISABLED)

        cancel_button = tk.Button(footer_frame, text="Cancel", width="10", command=self.on_cancel_button_click)
        cancel_button.grid(row=1, column=1, padx=5, pady=(10, 0), sticky=tk.E)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_icon(self) -> None:
        try:
            self.root.iconbitmap(Path(__file__).parent / "icon.ico")
            self.logger.debug("Loaded icon as iconbitmap using path")
            return
        except Exception:
            pass

        try:
            icon = tk.PhotoImage(file = Path(__file__).parent / "icon.gif")
            self.root.call('wm', 'iconphoto', self.root._w, icon)
            self.logger.debug("Loaded icon as iconphoto using path")
            return
        except Exception:
            pass

        try:
            with importlib.resources.path(f"{__package__}", "icon.ico") as icon_path:
                self.root.iconbitmap(default = icon_path)
                self.logger.debug("Loaded icon as iconbitmap using importlib")
                return
        except Exception:
            pass

        try:
            with importlib.resources.path(f"{__package__}", "icon.gif") as icon_path:
                icon = tk.PhotoImage(file = icon_path)
                self.root.call('wm', 'iconphoto', self.root._w, icon)
                self.logger.debug("Loaded icon as iconphoto using importlib")
                return
        except Exception:
            pass
    
        self.logger.debug("Could not load icon")
        # No icon for you

    def handle_worker_results(self) -> None:
        timeout = 100

        try:
            result, callback = self.worker2main_queue.get_nowait()
            callback(result)
        except queue.Empty:
            pass
        self.root.after(timeout, self.handle_worker_results)

    def submit_to_worker(self, function: Callable[[Optional[Tuple]], None], 
                         function_args: Tuple, 
                         callback: Callable[[Union[Tuple, Exception]], None]) -> None:
        self.main2worker_queue.put((function, function_args, callback))

    @staticmethod
    def worker_thread(input_queue: queue.Queue, output_queue: queue.Queue) -> None:
        while True:
            job = input_queue.get()

            if job is None:
                break

            func, args, callback = job
            try:
                result = func(args)
            except Exception as e:
                result = e
            output_queue.put((result, callback))

    def initialize_state(self, file_path: str, p4args: Dict[str, str]) -> None:
        assert(self.p4checkout is None)

        self.main2worker_queue = queue.Queue()
        self.worker2main_queue = queue.Queue()

        self.worker = threading.Thread(target=self.worker_thread, args=(self.main2worker_queue, self.worker2main_queue))
        self.worker.daemon = True
        self.worker.start()
        self.handle_worker_results()
        
        try:
            self.p4checkout = PerforceCheckout(file_path, **p4args)
            self.submit_to_worker(self.get_changelist_details, None, self.update_options_in_ui)
        except Exception as e:
            self.log_exception(e)
            messagebox.showerror("Error", str(e))
            raise e

    def on_closing(self) -> None:
        if self.p4checkout is not None:
            self.p4checkout.disconnect()
        self.root.destroy()

    def progress_bar_start(self) -> None:
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()

    def progress_bar_stop(self) -> None:
        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate")
        self.progress_bar["value"] = 0

    def get_changelist_details(self, args: Optional[Tuple]) -> Tuple[List[ChangeList], int]:
        if not self.p4checkout.is_connected():
            self.p4checkout.connect()
        res = []
        default_index = None
        for i, cl in enumerate(self.p4checkout.changelists):
            if cl.id in [self.p4checkout.CL_ID_NEW, self.p4checkout.CL_ID_DEFAULT]:
                res.append(cl.description)
                if cl.id == self.p4checkout.CL_ID_DEFAULT:
                    default_index = i
            else:
                res.append(f"{cl.id} {cl.description.rstrip()}")
        return (res, default_index)
    
    def update_options_in_ui(self, result: Union[Tuple[List[str], int], Exception]) -> None:
        if isinstance(result, Exception):
            self.log_exception(result)
            messagebox.showerror("Error", str(result))
            self.root.destroy()
        else:
            options, default_index = result
            options = [s.replace('\n', ' ') for s in options]
            self.select_box['values'] = options
            self.select_box.set(options[default_index])
            self.progress_bar_stop()
            self.ok_button.config(state=tk.NORMAL)
            self.submit_to_worker(self.check_file_metadata, None, 
                                  self.handle_file_metadata )
            
    def check_file_metadata(self, args: Optional[Tuple]) -> Optional[P4.Spec]:
        metadata = self.p4checkout.file_metadata
        if metadata is None:
            return None
        if "change" in metadata:
            raise RuntimeError(f"Error: File is already checked out in changelist '{metadata['change']}'")
        return metadata
        
    def handle_file_metadata(self, result: Union[P4.Spec, Exception]) -> None:
        if isinstance(result, Exception):
            self.log_exception(result)
            messagebox.showerror("Error", str(result))
            self.root.destroy()

    def on_select(self, event) -> None:
        selected_index = self.select_box.current()
        changelist = self.p4checkout.changelists[selected_index]
        
        content = ""
        self.text_box.config(state="normal")
        if changelist.id not in [self.p4checkout.CL_ID_DEFAULT, self.p4checkout.CL_ID_NEW]:
            content = changelist.description
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", content)

        if changelist.id != self.p4checkout.CL_ID_NEW:
            self.text_box.config(state="disabled")

    def on_ok_button_click(self) -> None:
        self.progress_bar_start()
        self.ok_button.config(state=tk.DISABLED)
        selected_index = self.select_box.current()
        changelist = self.p4checkout.changelists[selected_index]
        description = self.text_box.get("1.0",tk.END+"-1c") # Ignore redundant newline added by text widget

        def on_checkout(result: Union[str, Exception]) -> None:
            self.progress_bar_stop()
            if isinstance(result, str):
                messagebox.showinfo("Checked out", f"Successfully checked out to changelist '{result}'")
                self.root.destroy()
            elif isinstance(result, Exception):
                self.log_exception(result)
                self.ok_button.config(state=tk.NORMAL)
                messagebox.showerror("Error", str(result))
            else:
                raise ValueError(f"Unexpected result: {result}")

        def checkout(args: Optional[Tuple]) -> Union[str, Exception]:
            try:
                new_changelist = self.p4checkout.checkout(changelist.id, description)
                return new_changelist
            except Exception as e:
                return e

        self.submit_to_worker(checkout, None, on_checkout)
        
    def on_cancel_button_click(self) -> None:
        self.root.destroy()

    def log_exception(self, ex: BaseException) -> None:
        self.logger.error(''.join(traceback.TracebackException.from_exception(ex).format()))

    def run(self) -> None:
        self.root.mainloop()
        

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("path", help="Path to file to check out")

    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=VERSION))

    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc.)")

    parser.add_argument("-p", "--port", action="store", help="P4 port (e.g. 'ssl:localhost:1666')")
    parser.add_argument("-c", "--client", action="store", help="P4 client")
    parser.add_argument("-s", "--host", action="store", help="P4 host")
    parser.add_argument("-u", "--user", action="store", help="P4 user")
    
    args = parser.parse_args()

    logging.basicConfig(level={0: logging.CRITICAL, 
                               1: logging.ERROR, 
                               2: logging.INFO, 
                               3: logging.DEBUG}.get(args.verbose, logging.DEBUG),
                        format='%(name)-12s %(levelname)-8s %(message)s',)    

    try:
        p4args = {}
        for arg in ["port", "client", "host", "user"]:
            if hasattr(args, arg):
                p4args[arg] = getattr(args, arg)
        gui = PerforceCheckoutGui(args.path, p4args)
        gui.run()
    except Exception as e:
        sys.exit(f"Failed: {str(e)}")

if __name__ == "__main__":
    main()

