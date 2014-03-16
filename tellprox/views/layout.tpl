<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>TellProx{{' ' + title if title else ''}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="static/css/bootstrap.min.css" rel="stylesheet">
	<link href="static/css/bootstrap-switch.css" rel="stylesheet">
	<link href="static/css/bootstrap-select.min.css" rel="stylesheet">
	<link href="static/css/flat-ui.css" rel="stylesheet">
	<link href="static/css/jquery.toast.min.css" rel="stylesheet">
	<link href="static/css/site.css" rel="stylesheet">
  </head>

  <body>
  <!-- Fixed navbar -->
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <img src="static/images/logo.png" id="logo" class="hidden-xs"/>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
			<li 
			%if name == 'devices':
				class="active"\\
			%end
			><a href="devices">Devices</a></li>
			<li 
			%if name == 'scheduler':
				class="active"\\
			%end
			><!--a href="scheduler">Scheduler</a></li>
			<li 
			%if name == 'config':
				class="active"\\
			%end
			--><a href="config">Config</a></li>
			<li 
			%if name == 'api':
				class="active"\\
			%end
			><a href="api">API</a></li>
		  </ul>
		  %if password:
          <ul class="nav navbar-nav navbar-right">
            <li><a href="logout">Logout</a></li>
          </ul>	
		  %end
        </div><!--/.nav-collapse -->
      </div>
    </div>
	
	%if debug:
	<script src="static/js/jquery-2.1.0.min.js"></script>
	<script src="static/js/jquery.toast.min.js"></script>
	<script src="static/js/bootstrap.min.js"></script>
	<script src="static/js/bootstrap-switch.js"></script>
	<script src="static/js/bootstrap-select.min.js"></script>
	<script src="static/js/helpers.js"></script>
	<script>{{!jsAPI}}</script>
	%else:
	<script src="static/compiled.js"></script>
	%end
	<script>
	var api = new tellproxAPI('{{apikey}}');
	</script>

    <div class="container">
	  %include
	</div>
  </body>
</html>
