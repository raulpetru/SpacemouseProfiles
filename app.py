from pyexpat.errors import messages
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.reactive import reactive
from textual.widgets import Static, Label, Input, Select, Button, Header, Footer
import win32gui
import win32process
import psutil
import json
import serial
import serial.tools.list_ports

loaded_profiles = dict()
active_window = str()
selected_port = str()


def send_values_to_mouse(self):
    # Open serial
    ser = serial.Serial(selected_port, 25000, timeout=1)
    send_list = []
    for widget in self.app.query(NewInput):
        if active_window in loaded_profiles:
            if widget.id in loaded_profiles[active_window]:
                widget.value = loaded_profiles[active_window][widget.id]
        else:
            widget.value = widget.initial_value
        send_list.append(f'{widget.id}={widget.value},')
    # Remove last comma
    send_list[-1] = send_list[-1][:-1]
    send_list.append('\n')
    message = ''.join(send_list)
    ser.write(message.encode('utf-8'))
    # Close serial
    ser.close()


def load_json():
    try:
        with open("profiles.json", "r") as profiles:
            return json.load(profiles)
    except FileNotFoundError:
        # If there is no json file, make one
        with open('profiles.json', 'w') as profiles:
            json.dump({}, profiles)
            return {}


def save_json(profiles_to_save):
    with open("profiles.json", "w") as profiles:
        json.dump(profiles_to_save, profiles)


class ActiveApp(Static):
    """A widget to monitor active window app in order to update Spacemouse profiles"""

    active_window = reactive(str('None'))
    last_window = reactive(str('None'))

    def on_mount(self) -> None:
        global loaded_profiles
        loaded_profiles = load_json()
        if not loaded_profiles:
            loaded_profiles = dict()
        self.active_window = self.set_interval(0.2, self.get_active_window)

    def get_active_window(self):
        current_window = win32gui.GetForegroundWindow()
        if current_window != self.last_window:
            _, pid = win32process.GetWindowThreadProcessId(current_window)
            # Sometimes can't get the process PID so we continue and try again
            global active_window
            try:
                process = psutil.Process(pid)
                if process.name() in ('WindowsTerminal.exe', 'explorer.exe', 'cmd.exe'):
                    if self.last_window == 'None':
                        self.active_window = 'None'
                        active_window = self.active_window
                else:
                    self.active_window = process.name()
                    active_window = self.app.sub_title = self.active_window
                    self.last_window = current_window
                    send_values_to_mouse(self)
            except:
                pass


class NewInput(Input):
    def __init__(self, in_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_value = in_value


class InputSensitivity(Static):
    def __init__(self, in_label, in_value):
        super().__init__()
        self.in_label = in_label
        self.in_value = in_value

    def get_input_initial_value(self):
        return self.in_value

    def compose(self) -> ComposeResult:
        yield Label(f'{self.in_label} (default:{self.in_value})')
        yield NewInput(placeholder=self.in_label, type='number', value=self.in_value, in_value=self.in_value,
                       id=self.in_label, classes='input')

    def on_input_changed(self, event: NewInput.Changed) -> None:
        global loaded_profiles
        input_id = event.input.id
        if active_window != '' and active_window != 'None':
            if active_window in loaded_profiles:
                loaded_profiles[active_window][input_id] = event.input.value
            else:
                loaded_profiles[active_window] = {input_id: event.input.value}
        save_json(loaded_profiles)


class SpacemouseProfiles(App):
    ports = [p.device for p in list(serial.tools.list_ports.comports())]
    ports = [(line, line) for line in ports]

    BINDINGS = [("q", 'quit', "Close app")]

    CSS_PATH = 'app.tcss'

    def compose(self) -> ComposeResult:
        yield Header(name='test')
        yield Center(ActiveApp())
        yield Label(f'Select COM port:')
        yield Select(self.ports, value=self.ports[0][1])
        yield Center(InputSensitivity('TRANSX_SENSITIVITY', str(5)))
        yield Center(InputSensitivity('TRANSY_SENSITIVITY', str(5)))
        yield Center(InputSensitivity('POS_TRANSZ_SENSITIVITY', str(5)))
        yield Center(InputSensitivity('NEG_TRANSZ_SENSITIVITY', str(5)))
        yield Center(InputSensitivity('GATE_NEG_TRANSZ', str(15)))
        yield Center(InputSensitivity('GATE_ROTX', str(15)))
        yield Center(InputSensitivity('GATE_ROTY', str(15)))
        yield Center(InputSensitivity('GATE_ROTZ', str(15)))
        yield Center(InputSensitivity('ROTX_SENSITIVITY', str(1.5)))
        yield Center(InputSensitivity('ROTY_SENSITIVITY', str(1.5)))
        yield Center(InputSensitivity('ROTZ_SENSITIVITY', str(5)))
        yield Center(Button.success("Save"))
        yield Footer()

    def on_mount(self):
        global selected_port

        selected_port = self.query_one(Select).value

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        global selected_port

        selected_port = str(event.value)

    @on(Button.Pressed)
    def button_pressed(self) -> None:
        send_values_to_mouse(self)


if __name__ == "__main__":
    app = SpacemouseProfiles()
    app.run()
