from StringIO import StringIO
from string import Template
css = """

body {
    font-family: Verdana, Tahoma;
}

div#allselectors {
    display: block;
    overflow: auto;
    margin: 0;
    margin-bottom: 1em;
    padding: 0.5em; 
    background-color: #ddf;
}

div.box {
    display: block;
    float: left;
    margin-right: 1em;
}    

#status {
    clear: both; font-weight: bold; font-size: small;
}

#error { color: red; font-weight: bold; }


#topbar {margin:0;  height: 9%; padding: 1em; display: block; }
#window {margin:0;  width: 95%; height: 90%;border: 0;}



"""

scriptb = """


String.prototype.format = function(args) {
        var formatted = this;
        for (arg in args) {
            formatted = formatted.replace("{" + arg + "}", args[arg]);
        }
        return formatted;
};


function update_gui() {
    var data_id = get_data_id();

    var src = data_id + '.html';
    
    $('#window').attr("src", src); 

    message = (
    '<span><a target="_blank" '+
    'href="{data_id}.html">Open {title} in a new tab.</a>. ') .format(
                           { 'title': data_id, 
                           'data_id': data_id});
        
    $('#status').html(message);
}


$(document).ready( function () {
    $('select').change(update_gui);
    
    update_gui(); /* will call slide() value */
});
 
"""
page = """
<html>
    <head>
        <title> Saccade analysis GUI </title>
        <style type="text/css">${css}</style>
        <script type="text/javascript" src="images/static/jquery/jquery.js"></script>   
        <script type="text/javascript">                                         
          ${script}                                        
        </script>      
        <script type="text/javascript">                                         
          ${scriptb}                                        
        </script>      
        <script type="text/javascript" src="images/static/jquery/jquery.ui.js"></script>   
        
        <!-- Image zoom -->
        <script type="text/javascript" src="images/static/jquery/jquery.imageZoom.js"></script>
        <link rel="stylesheet" href="images/static/jquery/jquery.imageZoom.css"/>
        
        <link rel="stylesheet" href="images/static/jquery/ui-lightness/jquery-ui-1.8.5.custom.css"/>
        
        <script type="text/javascript"> 
            $$(document).ready( function () {
                $$('.zoomable').imageZoom();
            });       
        </script>

    </head>
<body>
<div id="container>
<div id="topbar">
    ${topbar}
    <p id="status">?</p>
</div>
<iframe  name="window"  src="#" id="window">
No iframes supported.
</iframe>
</div>
</body>
</html>
"""

def create_gui(filename, menus):
    f = open(filename, 'w')
   
    script = StringIO()
    
    topbar = StringIO()

    script.write("""
function get_data_id() {
        var s = "";
    """)    
    for i, menu in enumerate(menus):
        label, choices = menu
        name = 'var%d' % i
        choices = map(lambda x: (x,x), choices)
        
    
        write_select_box(topbar, label, name, choices)
        
        if i != 0:
            script.write("""
        s = s + ".";
            """)
        script.write("""
        var%d = $('#var%d').val();
        s = s + var%d;
        """ % (i,i,i) )
        
    script.write("""
    return s;
}
    """)    

    
    f.write(Template(page).substitute(css=css, script=script.getvalue(),
                                      scriptb=scriptb, 
                                        topbar=topbar.getvalue()))
    
    
     

def write_select(f, name, choices, onchange=""):
    '''Writes the <select> element to f. choices is a tuple of (value, desc).''' 
    f.write('<select id="%s" name="%s">\n' % (name, name))
    for i, choice in enumerate(choices):
        value = choice[0]
        desc = choice[1]
        selected = 'selected="selected"' if i == 0 else ""
        f.write('\t<option value="%s" %s>%s</option>\n' % 
                (value, selected, desc))
              
    f.write('</select>\n\n')    


def write_select_box(f, desc, name, choices):
    f.write('<div class="box" id="box-%s">\n' % name)
    f.write('<span>%s</span>\n' % desc)
    write_select(f, name, choices)
    f.write('</div>\n\n')
    
    
    
def create_main_gui(filename):
    f = open(filename, 'w')
    f.write("""
<html>
    <head>
        <title> Saccade analysis GUI </title>
        <style type="text/css">${css}
        
body {
    font-family: Verdana, Tahoma;
    font-weight: bold;
}

#topbar {
    height: 5%;
    border: 0;
}
#topbar a {
    font-weight: bold;
    margin-right: 2em;
}
#window {
    border: 0;
    height: 90%;
    width: 100%;
}
        </style>
</head>
<body>
<div id="topbar">
    <a href="expdata_plots.html" target="window">Raw data stats</a>
    <a href="group_plots.html" target="window">Groups stats</a>
    <a href="saccade_plots.html" target="window">Single sample stats</a>
</div>
<iframe src="expdata_plots.html" name="window" id="window">
No iframes supported.
</iframe>
</body>
</html>
""")
    
    
    
    
    
    
    