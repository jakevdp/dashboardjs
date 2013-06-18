from IPython.display import HTML
import urlparse


EMBED_SOURCE = r"""
<div style="border-color:black;border-style:solid;border-width:1px;padding:10px;width:400px;">
<button onclick="test_func()">Send Message</button><input type="text" id="messageBox">
<br><br>

Messages Received:<br>
<input type="text" id="domain_name">
<input type="text" id="message_name">
</div>
<br>
<iframe id="embedded" src="{target}" width="{width}" height="{height}" style="border-color:black;border-style:solid;border-width:1px;"></iframe>
<br>

<script language="text/Javascript">
function test_func(){{
  var message = document.getElementById("messageBox").value;
  var windowRef = document.getElementById("embedded").contentWindow;
  windowRef.postMessage(message, "{target}");
}}

window.addEventListener("message", receiveMessage, false);

function receiveMessage(event)
{{
  document.getElementById("domain_name").value = event.origin;
  if(event.origin === "{target}"){{
    if (typeof event.data == 'string' || event.data instanceof String){{
       document.getElementById("message_name").value = event.data;
    }}else{{
       var kernel = IPython.notebook.kernel;
       var code = 'import numpy as np\n'
       code += 'data=dict()\n'

       // Would it be better to pass a JSON rep and have python convert it?
       for(var k in event.data[0]){{
          if(k == "id" || k == "visible") continue;
          code += 'data["' + k + '"] = np.array([';
          for (var i = 0; i < event.data.length; i++){{
             if(typeof event.data[i][k] == 'string' || event.data instanceof String){{
               code += "'" + event.data[i][k] + "', ";
             }}else{{
               code += event.data[i][k] + ', ';
             }}
          }}
          code += '])\n';
       }}
       kernel.execute(code);
       document.getElementById("message_name").value = "(data object)";
    }}
  }}else{{
    console.log("WARNING: received message from unrecognized origin: " + event.origin + ". Expected origin: " + "{target}");
    console.log(event.origin);
  }}
}}
</script>
"""


def embed(ascot_addr, width=1000, height=600):
    res = urlparse.urlparse(ascot_addr)
    return HTML(EMBED_SOURCE.format(target="{0}://{1}".format(*res),
                                    width=width, height=height))
