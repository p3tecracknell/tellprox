<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>TellProx{{' ' + title if title else ''}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="static/css/bootstrap.css" rel="stylesheet">
	<link href="static/css/flat-ui.css" rel="stylesheet">
    <link href="static/css/bootstrap-responsive.css" rel="stylesheet">
	<link href="static/css/site.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
	  <div class="navbar navbar-inverse">
		<div class="navbar-inner">
		  <ul class="nav">
			<li><img src="static/images/logo.png" id="logo" /></a>
			<li class="active"><a href="devices">Devices</a></li>
			<li><a href="config">Config</a></li>
			<li><a href="api">API</a></li>
		  </ul>
		</div>
	  </div>
	  
	  %include
  </body>
</html>
