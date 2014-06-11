<!DOCTYPE html>
<html>
    <head>
        <title>Tellprox</title>
        
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black" />
        <meta name="format-detection" content="telephone=no"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        
        <link rel="apple-touch-startup-image" href="lib/durandal/img/ios-startup-image-landscape.png" media="(orientation:landscape)" />
        <link rel="apple-touch-startup-image" href="lib/durandal/img/ios-startup-image-portrait.png" media="(orientation:portrait)" />
        <link rel="apple-touch-icon" href="lib/durandal/img/icon.png"/>
        
		<link rel="stylesheet" href="lib/bootstrap/css/bootstrap.min.css">
		<link rel="stylesheet" href="lib/bootstrap/css/bootstrap-switch.css">
		<link rel="stylesheet" href="lib/bootstrap/css/bootstrap-select.min.css">
		<link rel="stylesheet" href="css/flat-ui.css">
		<link rel="stylesheet" href="css/jquery.toast.min.css">
		<link rel="stylesheet" href="css/site.css">
	
        <link rel="stylesheet" href="lib/font-awesome/css/font-awesome.css" />
        <link rel="stylesheet" href="css/ie10mobile.css" />
        <link rel="stylesheet" href="lib/durandal/css/durandal.css" />
        <link rel="stylesheet" href="css/starterkit.css" />
        
        <script type="text/javascript">
            if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
                var msViewportStyle = document.createElement("style");
                var mq = "@@-ms-viewport{width:auto!important}";
                msViewportStyle.appendChild(document.createTextNode(mq));
                document.getElementsByTagName("head")[0].appendChild(msViewportStyle);
            }
        </script>
		<script>
		var apiKey = '{{apikey}}';
		</script>
    </head>
    <body>
        <div id="applicationHost">
            <div class="splash">
              <div class="message">
                  Tellprox
              </div>
              <i class="icon-spinner icon-2x icon-spin active"></i>
          </div>
        </div>
		%if debug:
        <script src="lib/require/require.js" data-main="app/main"></script>
		%else:
		<script type="text/javascript" src="app/main-built.js"></script>
		%end
    </body>
</html>