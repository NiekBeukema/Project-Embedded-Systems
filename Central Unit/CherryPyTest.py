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
        if percentage:
            self.controller.rollOut(percentage)

        # convert int to str for display reasons
        self.lightValue = "30"#str(self.controller.getLight())
        self.tempValue = "23"#str(self.controller.getTemp())

        return '''
        <html>
            <head>
                <title>Zeng Home | Project 2.1</title>
                <script type="Javascript" src="/vis.min.js"></script>
                <link rel="stylesheet" href="/metro.min.css">
                <link rel="stylesheet" href="/metro-responsive.min.css"
                <link rel="stylesheet" href="/vis.min.css">
                <script type="Javascript" src="/jquery-3.1.1.min.js"></script>
                <script type="Javascript" src="/metro.min.js"></script>

            </head>
            <body>
                <div class="grid">
                    <div class="row">
                        <div class="cell">is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</div>
                        <div class="cell">is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</div>
                    </div>
                    <div class="row">
                        <div id="visualization1" class="cell">
                            <div class="tile">
                                <div class="tile-content iconic">
                                    <icon/>
                                </div>
                            </div>
                        </div>
                        <div id="visualization2" class="cell"></div>
                    </div>
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
            </head>
            <body>
                <h2>Program Settings</h2>
                <div>
                    <form method="post">
                        <label for="lightThreshold">LightThreshold: </label>
                        <input type="text" size="5" name="lightThreshold" placeholder="Threshold"/>
                        <br/>
                        <br/>
                        <label for="tempThreshold">TempThreshold: </label>
                        <input type="text" size="5" name="tempThreshold" placeholder="Threshold"/>
                        <br/>
                        <br/>
                        <button type="submit">Save Settings</button>
                    </form>
                </div>
            </body>
        </html>
        '''

if __name__ == '__main__':
    # start cherrypy server
    cherrypy.quickstart(HelloWorld(), '/', 'CherryPyTest.config')


