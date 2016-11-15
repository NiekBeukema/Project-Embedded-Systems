from UnoNetworking import UnoNetworkController
import cherrypy
# import os.path
from random import randint
import time


class Default(object):

    def __init__(self):
        # establish connection with Arduino
        self.controller = UnoNetworkController()
        self.controller.connect()

    # cherrypy.expose exposes a def as a webpage
    @cherrypy.expose
    def index(self, control=""):

        if control == "rollIn":
            print("Rollin In...")
            self.controller.rollOut(0)
        if control == "rollOut":
            print("Rollin Out...")
            self.controller.rollOut(1)

        # convert int to str for display reasons
        lightValue = str(self.controller.getLight())
        tempValue = str(self.controller.getTemp())
        rolledOutValue = str(self.controller.getRolledOut())

        # debug values
        # lightValue = str(randint(10,30))
        # tempValue = str(randint(10,30))
        # rolledOutValue = str(1)

        return '''
        <html>
            <head>
                <title>Zeng Home | Project 2.1</title>

                <!-- JS Scripts -->
                <script type="text/javascript" src="/static/js/jquery-3.1.1.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.17.0/vis.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

                <!-- Stylesheets -->
                <link rel="stylesheet" href="/static/css/vis.css" type="text/css" />
                <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
            </head>

            <body>
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <a href="settings">Settings Are Here</a>
                            <form method="post">
                                <div class="radio">
                                    <label>
                                        <input type="radio" name="control" value="rollIn" checked>Inrollen
                                    </label>
                                </div>
                                <div class="radio">
                                    <label>
                                        <input type="radio" name="control" value="rollOut">Uitrollen
                                    </label>
                                </div>
                                <button type="submit" class="btn btn-default">Uitvoeren</button>
                            </form>
                            <br/>
                            <br/>
                            <div id="values">
                                <label>Current Temperature: </label>
                                <div id="currenttemp">''' + tempValue + ''' Cº</div><br>
                                <label>Current Light: </label>
                                <div id="currentlight">''' + lightValue + ''' Lx</div><br>
                                <label>Status: </label>
                                <div id="currentstatus">''' + rolledOutValue + '''</div><br>
                            </div>
                        </div>
                        <div class="col-md-8">
                            is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not
                            only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing
                            software like Aldus PageMaker including versions of Lorem Ipsum
                        </div>
                        </div>
                        <div class="row">&nbsp;</div>
                        <div class="row">
                            <div class="col-md-5">
                                <div id="tempGraph"></div>
                            </div>
                            <div class="col-md-5 col-md-offset-1">
                                <div id="lightGraph"></div>
                        </div>
                    </div>
                </div>

                <script type="text/javascript">
                function ajax1() {
                    return $.ajax({
                        url : 'values',
                        type : 'POST',
                        dataType : 'json'
                      })
                }

                  $(document).ready(function() {

                    var tempContainer = document.getElementById('tempGraph');
                    var lightContainer = document.getElementById('lightGraph');
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
                      end: getTimePlus.getTime(),
                      autoResize: true
                    };
                    var graph2d1 = new vis.Graph2d(tempContainer, graph2d1data, options);
                    var graph2d2 = new vis.Graph2d(lightContainer, graph2d2data, options);
                    function updateGraph() {
                      $.when(ajax1()).done(function(result) {
                        console.log("Request Completed");
                        var getTime = new Date();
                        graph2d1data.update({x: getTime.getTime(), y: result['tempValue']});
                            graph2d2data.update({x: getTime.getTime(), y: result['lightValue']});
                            $("#currenttemp").html(result['tempValue'] + "Cº");
                            $("#currentlight").html(result['lightValue'] + "Lx");
                            $("#currentstatus").html(result['rolledOutValue']);
                        setTimeout(updateGraph(), 3000);
                      })
                    }
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
        print("Update values")
        lightValue = self.controller.getLight()
        tempValue = self.controller.getTemp()
        rolledOutValue = self.controller.getRolledOut()
        print(lightValue)
        print(tempValue)
        print(rolledOutValue)
        return '''{"tempValue":''' + str(tempValue) + ''', "lightValue":''' + str(lightValue) + ''', "rolledOutValue":''' + str(rolledOutValue) + '''}'''


if __name__ == '__main__':
    # start cherrypy server
    cherrypy.quickstart(Default(), '/', 'CherryPyTest.config')



