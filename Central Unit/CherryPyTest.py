from UnoNetworking import UnoNetworkController
import cherrypy
from random import randint
import time

class Default(object):

    def __init__(self):
        # Create a new instance of UnoNetworkingController
        self.controller = UnoNetworkController()
        # Establish connection with Arduino
        self.controller.connect()

    # cherrypy.expose tells CherryPy
    @cherrypy.expose
    def index(self):

        # convert int to str for display reasons
        lightValue = str(self.controller.getLight())
        tempValue = str(self.controller.getTemp())
        rolledOutValue = str(self.controller.getRolledOut())


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
                <link href="/static/css/style.css" rel="stylesheet"/>
            </head>
            <body>

                <nav class="navbar navbar-inverse navbar-fixed-top">
                    <div class="container">
                        <div class="navbar-header">
                            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                                <span class="sr-only">Toggle navigation</span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                            </button>
                            <a class="navbar-brand" href="#">Zeng ltd.</a>
                        </div>
                        <div id="navbar" class="collapse navbar-collapse">
                            <ul class="nav navbar-nav">
                                <li class="active"><a href="/">Home</a></li>
                                <li><a href="settings">Instellingen</a></li>
                                <li><a href="values">Debug</a></li>
                            </ul>
                        </div><!--/.nav-collapse -->
                    </div>
                </nav>

                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <a href="settings">Settings Are Here</a>
                            <button id="rollinbut" onclick="rollIn()" class="btn btn-default disabled">Rol in</button>
                            <button id="rolloutbut" onclick="rollOut()" class="btn btn-default disabled">Rol uit</button>
                            <button id="toggleautobut" onclick="toggleAuto()" class="btn btn-default">Naar handmatig</button>
                            <br/>
                            <br/>
                            <div id="values">
                                <label>Huidige temperatuur: </label>
                                <div id="currenttemp">''' + tempValue + '''  Cº</div><br>
                                <label>Lichtintensiteit: </label>
                                <div id="currentlight">''' + lightValue + '''  Lx</div><br>
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
                    var auto = true;
                    var avgTemp = 0;
                    var avgLight = 0;
                    var tempCount = 0;
                    var lightCount = 0;
                    function rollIn() {
                        var request = $.ajax({
                            url: "rollin",
                            type: "POST",
                            dataType: "text"
                        });
                        request.done(function(msg) {
                            console.log("succes");
                        });
                        request.fail(function(jqXHR, textStatus) {
                            alert( "Request failed: " + textStatus );
                        });
                    }

                    function rollOut() {
                        var request = $.ajax({
                            url: "rollout",
                            type: "POST",
                            dataType: "text"
                        });
                        request.done(function(msg) {
                            console.log("succes");
                        });
                        request.fail(function(jqXHR, textStatus) {
                            alert( "Request failed: " + textStatus );
                        });
                    }

                    function toggleAuto() {
                        var request = $.ajax({
                            url: "toggleauto",
                            type: "POST",
                            dataType: "text"
                        });
                        request.done(function(msg) {
                            if(auto) {
                                $("#rollinbut").toggleClass("disabled");
                                $("#rolloutbut").toggleClass("disabled");
                                $("#toggleautobut").html("Naar automatisch");
                                auto = false
                            }

                            else {
                                $("#rollinbut").toggleClass("disabled");
                                $("#rolloutbut").toggleClass("disabled");
                                $("#toggleautobut").html("Naar handmatig");
                                auto = true;
                            }

                        });
                        request.fail(function(jqXHR, textStatus) {
                            alert( "Request failed: " + textStatus );
                        });
                    }

                    function ajax1() {
                        return $.ajax({
                            url : 'values',
                            type : 'POST',
                            dataType : 'json'
                          })
                    }

                    function wait(ms) {
                        var start = new Date().getTime();
                        var end = start;
                        while(end < start + ms) {
                            end = new Date().getTime();
                        }
                    }
                      $(document).ready(function() {
                        //$("#rollinbut").bind("click", rollIn());
                        //$("#rolloutbut").bind("click", rollOut())
                        //$(document).delay(1000);
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
                          autoResize: true,
                          drawPoints: false
                        };
                        var graph2d1 = new vis.Graph2d(tempContainer, graph2d1data, options);
                        var graph2d2 = new vis.Graph2d(lightContainer, graph2d2data, options);
                        function updateData() {
                          $.when(ajax1()).done(function(result) {
                                lightCount++;
                                tempCount++;
                                avgTemp = (avgTemp + result['tempValue']);
                                avgLight = (avgLight + result['lightValue']);
                                $("#currenttemp").html(result['tempValue'] + " Cº");
                                $("#currentlight").html(result['lightValue'] + " Lx");
                                $("#currentstatus").html(result['rolledOutValue']);
                                wait(1000);
                                updateData();
                          })
                        }

                        function updateGraph() {
                            var getTime = new Date();
                            graph2d1data.update({x: getTime.getTime(), y: (avgTemp / tempCount)});
                            graph2d2data.update({x: getTime.getTime(), y: (avgLight / lightCount)});

                        }
                     console.log("First execution");
                     setInterval(updateGraph, 10000);
                     updateData();

                      });
    </script>
            </body>
        </html>'''

    @cherrypy.expose
    # settings page for various variables
    def settings(self, lightThreshold=0, tempThreshold=0):

        settingsSaved = ""

        if lightThreshold:
            # debug
            print("light value is: " + str(lightThreshold))
            self.controller.setLightThreshold(lightThreshold)
        if tempThreshold:
            # debug
            print("temp value is: " + str(tempThreshold))
            self.controller.setTempThreshold(tempThreshold)

        if lightThreshold or tempThreshold:
            settingsSaved = '<br/><br/><div class="alert alert-success" role="alert">Instellingen opgeslagen</div>'

        currentLightThreshold = str(self.controller.getLightThreshold())
        currentTempThreshold = str(self.controller.getTempThreshold())

        # debug for use without arduino connected
        # currentLightThreshold = str(randint(10, 50))
        # currentTempThreshold = str(randint(10, 50))

        return '''
        <html>
            <head>
                <title>Settings | Project 2.1</title>
                <!-- JS Scripts -->
                <script type="text/javascript" src="/static/js/jquery-3.1.1.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.17.0/vis.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
                <!-- Stylesheets -->
                <link rel="stylesheet" href="/static/css/vis.css" type="text/css" />
                <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
                <link href="/static/css/style.css" rel="stylesheet"/>
            </head>
            <body>
                <nav class="navbar navbar-inverse navbar-fixed-top">
                    <div class="container">
                        <div class="navbar-header">
                            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                                <span class="sr-only">Toggle navigation</span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                            </button>
                            <a class="navbar-brand" href="#">Zeng ltd.</a>
                        </div>
                        <div id="navbar" class="collapse navbar-collapse">
                            <ul class="nav navbar-nav">
                                <li><a href="/">Home</a></li>
                                <li class="active"><a href="settings">Instellingen</a></li>
                                <li><a href="values">Debug</a></li>
                            </ul>
                        </div><!--/.nav-collapse -->
                    </div>
                </nav>

                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <h2>Program Settings</h2>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <form method="post">
                                <label>Current lightThreshold is: ''' + currentLightThreshold + '''</label>
                                <br/>
                                <label for="lightThreshold">LightThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" class="form-control" name="lightThreshold" value="''' + currentLightThreshold + '''"
                                    placeholder="Threshold"/>
                                </div>
                                <br/>
                                <label>Current tempThreshold is: ''' + currentTempThreshold + '''</label>
                                <br/>
                                <label for="tempThreshold">TempThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" class="form-control" name="tempThreshold"
                                    value="''' + currentTempThreshold + '''" placeholder="Threshold"/>
                                </div>
                                <br/>
                                <button type="submit" class="btn btn-default">Opslaan</button>
                                ''' + settingsSaved + ''''
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
        return '''{"tempValue":''' + str(tempValue) + ''', "lightValue":''' + str(lightValue) + ''', "rolledOutValue":''' + str(rolledOutValue) + '''}'''

    @cherrypy.expose()
    def rollin(self):
        print("Rolling in")
        self.controller.rollOut(0)

    @cherrypy.expose()
    def rollout(self):
        print("Rolling out")
        self.controller.rollOut(1)

    @cherrypy.expose()
    def toggleauto(self):
        self.controller.toggleauto()
        print("toggling modes")


if __name__ == '__main__':
    # start cherrypy server
    cherrypy.quickstart(Default(), '/', 'CherryPyTest.config')
