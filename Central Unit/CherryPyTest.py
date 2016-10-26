from UnoNetworking import UnoNetworkController
import cherrypy
import os.path

class HelloWorld(object):

    def __init__(self):
        # establish connection with Arduino
        self.controller = UnoNetworkController()

    # cherrypy.expose exposes a def as a webpage
    @cherrypy.expose
    def index(self, percentage=0):
        self.controller.connect()

        # self.controller.rollOut(88)

        if percentage:
            self.controller.rollOut(percentage)

        # convert int to str for display reasons
        self.lightValue = "30" #str(self.controller.getLight())
        self.tempValue = "23" #str(self.controller.getTemp())

        return '''
        <html>
            <head>
                <title>Zeng Home | Project 2.1</title>
                <link rel="stylesheet" href="/static/css/metro.min.css" type="text/css">
                <link rel="stylesheet" href="/static/css/metro-responsive.min.css" type="text/css" />
                <script type="Javascript" src="/static/js/jquery-3.1.1.min.js"></script>
                <script type="Javascript" src="/static/js/metro.min.js"></script>
                <script src="/static/js/vis.js"></script>
                <link href="/static/css/vis.css" rel="stylesheet" type="text/css" />
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
                            <label>Current Temperature: </label><div id="currenttemp">''' + self.tempValue + '''</div><br>
                            <label>Current Light: </label><div id="currentlight">''' + self.lightValue + '''</div><br>
                        </div>
	                    <div class="cell">
	                        is simply dummy text of the printing and typesetting industry.
	                        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer
	                        took a galley of type and scrambled it to make a type specimen book.
	                        It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
	                        It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
	                        and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum
	                    </div>
                    </div>
                </div>
                <div class="row cells2">
                    <div id="visualization1" class="cell"></div>

                    <div id="visualization2" class="cell"></div>
                </div>
                <script type="text/javascript">
                    var container1 = document.getElementById('visualization1');
                    var container2 = document.getElementById('visualization2');
                    var items = [
                        {x: '2014-06-11', y: 10},
                        {x: '2014-06-12', y: 25},
                        {x: '2014-06-13', y: 30},
                        {x: '2014-06-14', y: 10},
                        {x: '2014-06-15', y: 15},
                        {x: '2014-06-16', y: 30}
                    ];
                    var dataset = new vis.DataSet(items);
                    var options = {
                        start: '2014-06-10',
                        end: '2014-06-18'
                    };
                    var graph2d1 = new vis.Graph2d(container1, dataset, options);
                    var graph2d2 = new vis.Graph2d(container2, dataset, options);
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
                                <label for="lightThreshold">LightThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" size="5" name="lightThreshold" placeholder="Threshold"/>
                                </div>
                                <br/>
                                <br/>
                                <label for="tempThreshold">TempThreshold: </label>
                                <div class="input-control text">
                                    <input type="text" size="5" name="tempThreshold" placeholder="Threshold"/>
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

if __name__ == '__main__':
    # start cherrypy server
    cherrypy.quickstart(HelloWorld(), '/', 'CherryPyTest.config')


