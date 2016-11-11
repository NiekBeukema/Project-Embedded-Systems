from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()
controller.rollOut(0)
while(1):
    msg = controller.waitForMessage();
    if(msg != None):
        print(msg)


