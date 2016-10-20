import PyCmdMessenger
import serial.tools.list_ports
import time

class UnoNetworkController(object):
    commands = [["roll_out", "i"],
                ["get_temp", ""],
                ["get_length", ""],
                ["error", "s"],
                ["temp_is", "i"],
                ["rollout_done", "s"],
                ["length_is", "i"],
                ["get_light", ""],
                ["light_is", "i"],
                ["set_temp_threshold", "i"],
                ["set_light_threshold", "i"],
                ["timer_runtime_end", "s"]]

    arduino = 0#PyCmdMessenger.ArduinoBoard("COM3", baud_rate=9600)
    messenger = 0#PyCmdMessenger.CmdMessenger(arduino, commands)
    isConnected = 0;

    def UnoNetworkController(self, isConnected):
        self.isConnected = isConnected;

    def connect(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if("Uno" in str(p)):
                port = str(p).split(" ")[0]
                self.arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=9600)
                self.messenger = PyCmdMessenger.CmdMessenger(self.arduino, self.commands)
                print("Connected succesfully")
        return True

    def connectWithPort(self, port):
        self.arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=9600)
        self.messenger = PyCmdMessenger.CmdMessenger(self.arduino, self.commands)
        print("Connected succesfully")
        return True

    def rollOut(self, percentage):
        self.messenger.send("roll_out", percentage)
        time.sleep(3)
        msg = self.messenger.receive("s")
        return str(msg)

    def getTemp(self):
        self.messenger.send("get_temp")
        msg = self.messenger.receive("s")
        return int(str(msg[1][0]).split(".")[0])


    def getLight(self):
        self.messenger.send("get_light")
        msg = self.messenger.receive("s")
        return int(str(msg[1][0]))


    def getLength(self):
        self.messenger.send("get_length")
        msg = self.messenger.receive("s")
        return int(str(msg[1][0]).split(".")[0])

    def forceError(self):
        self.messenger.send("force_error")
        msg = self.messenger.receive("s")
        return msg

    def waitForMessage(self):
        msg = self.messenger.receive("s")
        return msg;