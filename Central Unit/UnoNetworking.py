import PyCmdMessenger
import serial.tools.list_ports

class UnoNetworkController(object):
    commands = [["roll_out", "i"],
                ["get_temp", ""],
                ["get_length", ""],
                ["get_type", ""],
                ["error", "s"],
                ["type_is", "s"],
                ["temp_is", "i"],
                ["rollout_done", "s"],
                ["length_is", "i"],
                ["force_error", ""]]

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

    def getType(self):
        self.messenger.send("get_type")
        msg = self.messenger.receive("s")
        return str(msg)

    def rollOut(self, percentage):
        self.messenger.send("roll_out", percentage)
        msg = self.messenger.receive()
        return str(msg)

    def getTemp(self):
        if self.getType() == "temp":
            self.messenger.send("get_temp")
            msg = self.messenger.receive("s")
            return int(msg[1][0])
        return "U"

    def getLight(self):
        if self.getType() == "light":
            self.messenger.send("get_light")
            msg = self.messenger.receive()
            return int(msg[1][0])
        return "U"

    def getLength(self):
        self.messenger.send("get_length")
        msg = self.messenger.receive("s")
        return int(msg[1][0])

    def forceError(self):
        self.messenger.send("force_error")
        msg = self.messenger.receive("s")
        return msg





