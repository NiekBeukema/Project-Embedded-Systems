from UnoNetworking import UnoNetworkController
import cherrypy
# import os.path
from random import randint
import time


class Default(object):

    def __init__(self):
        # establish connection with Arduino
        self.controller = UnoNetworkController()
        self.test = 0
        self.controller.connect()

    # cherrypy.expose exposes a def as a webpage
    @cherrypy.expose
    def index(self, percentage=0):

        # convert int to str for display reasons
        lightValue = str(self.controller.getLight())
        tempValue = str(self.controller.getTemp())

        return '''
        <html>
            <head>
                <title>Zeng Home | Project 2.1</title>

                <!-- JS Scripts -->
                <script type="text/javascript" src="/static/js/jquery-3.1.1.min.js"></script>
                <!-- <script type="Javascript" src="https://code.jquery.com/jquery-3.1.1.js"></script> -->

                <!-- when loading visjs from disk i get a "vis is not defined" error.
                     I don't get this error when using a cdn.
                     i suspect this is somehow due to the load time of the visjs file -->

                <!-- <script type="javascript" src="/static/js/vis.min.js"></script> -->
                <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.17.0/vis.min.js"></script>
                <script type="Javascript" src="/static/js/metro.min.js"></script>

                <!-- StyleSheets -->
                <link rel="stylesheet" href="/static/css/vis.css" type="text/css" />
                <link rel="stylesheet" href="/static/css/metro.min.css" type="text/css">
                <link rel="stylesheet" href="/static/css/metro-responsive.min.css" type="text/css" />

            </head>
            <body>
                <div class="grid">
                    <div class="row cells2">
                        <div class="cell">
                            <!-- <label>Light Threshold</label><br>
                            <div class="input-control text">
                                <input type="text" placeholder="Enter light threshold value...">
                            </div><br>
                            <label>Temperature Threshold</label><br>
                            <div class="input-control text">
                                <input type="text" placeholder="Enter temperature threshold value...">
                            </div><br> -->
                            <a href="settings">Settings Are Here</a>
                            <br/>
                            <br/>
                            <div id="values">
                                <label>Current Temperature: </label><div id="currenttemp">''' + tempValue + '''</div><br>
                                <label>Current Light: </label><div id="currentlight">''' + lightValue + '''</div><br>
                            </div>
                        </div>
                        <div class="cell">
                            is simply dummy text of the printing and typesetting industry.
                            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
                            when an unknown printer took a galley of type and scrambled it to make a type specimen book.
                            It has survived not only five centuries, but also the leap into electronic typesetting,
                            remaining essentially unchanged.
                            It was popularised in the 1960s with the release of Letraset sheets containing
                            Lorem Ipsum passages,
                            and more recently with desktop publishing software like Aldus PageMaker including
                            versions of Lorem Ipsum
                        </div>
                    </div>
                </div>
                <div class="row cells2">
                    <div id="visualization1" class="cell"></div>

                    <div id="visualization2" class="cell"></div>
                </div>

                <script type="text/javascript">

                    $(document).ready(function() {
                        var container1 = document.getElementById('visualization1');
                        var container2 = document.getElementById('visualization2');
                        var getTime = new Date();
                        var getTimePlus = new Date(getTime);
                        getTimePlus.setMinutes(getTime.getMinutes() + 5 )
                        var items = [
                            {x: getTime.getTime(), y: 0}
                        ];
                        var graph2d1data = new vis.DataSet(items);
                        var graph2d2data = new vis.DataSet(items);
                        var options = {
                            start: getTime.getTime(),
                            end: getTimePlus.getTime()
                        };
                        var graph2d1 = new vis.Graph2d(container1, graph2d1data, options);
                        var graph2d2 = new vis.Graph2d(container2, graph2d2data, options);
                        setInterval(function() {
                            // console.log("calling..");
                            console.log($('#values').load("values"));
                            $.ajax({
                            url : 'values',
                            type : 'POST',
                            dataType : 'json',
                            success : function (result) {
                            console.log(result);
                                var getTime = new Date();
                                graph2d1data.update({x: getTime.getTime(), y: result['tempValue']});
                                graph2d2data.update({x: getTime.getTime(), y: result['lightValue']});
                                $("#gputempbadge").text(result['gpu1']);
                                $("#cputempbadge").text(result['cpu']);
                            },
                            error : function (obj, ovj, error) {
                                console.log(obj);
                                console.log(ovj);
                                console.log(error);
                            }
                        })
                        }, 1000);
                    });
                </script>

            </body>
        </html>'''

    @cherrypy.expose
    # settings page for various variables
    def settings(self, lightThreshold=0, tempThreshold=0):

        if lightThreshold:
            print("i got " + str(lightThreshold) + " as a light value")
            # self.controller.setLightThreshold(lightThreshold)
        if tempThreshold:
            print("i got " + str(tempThreshold) + " as a temp value")
            # self.controller.setTempThreshold(tempThreshold)

        # self.currentLightThreshold = str(self.controller.getLightThreshold())

        # debug for use without arduino connected
        currentLightThreshold = str(randint(10, 50))

        # self.currentTempThreshold = str(self.controller.getTempThreshold())

        # debug for use without arduino connected
        currentTempThreshold = str(randint(10, 50))

        return '''
        <html>
            <head>
                <title>Settings | Project 2.1</title>
                <link rel="stylesheet" href="/static/css/metro.min.css" type="text/css">
                <link rel="stylesheet" href="/static/css/metro-responsive.min.css" type="text/css" />
                <script type="Javascript" src="/static/js/jquery-3.1.1.min.js"></script>
                <script type="Javascript" src="/static/js/metro.min.js"></script>
                <script src="/static/js/vis.js"></script>
                <link href="/static/css/vis.css" rel="stylesheet" type="text/css" />
            </head>
            <body>
                <div class="grid">
                    <div class="row cells10">
                        <div class="cell offset1 colspan4">
                            <h2>Program Settings</h2>
                        </div>
                    </div>
                    <div class="row cells10">
                        <div class="cell offset1 colspan4">
                            <form method="post">
                                <label>Current lightThreshold is: ''' + currentLightThreshold + '''</label>
                                <br/>
                                <label for="lightThreshold">LightThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" size="5" name="lightThreshold" value="''' + currentLightThreshold + '''"
                                    placeholder="Threshold"/>
                                </div>
                                <br/>
                                <br/>
                                <label>Current tempThreshold is: ''' + currentTempThreshold + '''</label>
                                <br/>
                                <label for="tempThreshold">TempThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" size="5" name="tempThreshold"
                                    value="''' + currentTempThreshold + '''" placeholder="Threshold"/>
                                </div>
                                <br/>
                                <br/>
                                <input type="submit" value="Save Settings">
                            </form>
                        </div>
                    </div>
                </div>
            </body>
        </html>'''

    # small page to load the temp and light values from
    @cherrypy.expose()

    def values(self):
        # for debug purposes without arduino connected
        lightValue = self.controller.getLight()
        tempValue = self.controller.getTemp()
        return '''{"tempValue":''' + str(tempValue) + ''', "lightValue":''' + str(lightValue) + '''}'''


if __name__ == '__main__':
    # start cherrypy server
    cherrypy.quickstart(Default(), '/', 'CherryPyTest.config')



