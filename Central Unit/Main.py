from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()
while(1):
    print(controller.getDistance())
    msg = controller.waitForMessage();
    if(msg != None):
        print(msg)


