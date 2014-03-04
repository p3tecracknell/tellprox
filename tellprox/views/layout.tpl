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
	<script>
	function authData(data) {
		return $.extend({ 'key': '{{apikey}}' }, data);
	}
	</script>
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
          <img src="static/images/logo.png" id="logo" />
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li>
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
		  %if password:
          <ul class="nav navbar-nav navbar-right">
            <li><a href="logout">Logout</a></li>
          </ul>	
		  %end
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">
	  %include
	</div>
  </body>
</html>
