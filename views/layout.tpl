<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>TellProx{{' ' + title if title else ''}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="static/css/bootstrap.css" rel="stylesheet">
	<link href="static/css/bootstrap-switch.css" rel="stylesheet">
	<link href="static/css/flat-ui-prev.css" rel="stylesheet">
    <link href="static/css/bootstrap-responsive.css" rel="stylesheet">
	<link href="static/css/site.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
	  <div class="navbar navbar-inverse">
		<div class="navbar-inner">
		  <ul class="nav">
			<li><img src="static/images/logo.png" id="logo" /></a>
			%if name == 'devices':
				<li class="active"><a href="devices">Devices</a></li>
			%else:
				<li><a href="devices">Devices</a></li>
			%end
			%if name == 'config':
				<li class="active"><a href="config">Config</a></li>
			%else:
				<li><a href="config">Config</a></li>
			%end
			%if name == 'api':
				<li class="active"><a href="api">API</a></li>
			%else:
				<li><a href="api">API</a></li>
			%end
		  </ul>
		</div>
	  </div>
	  
	  %include
  </body>
</html>
