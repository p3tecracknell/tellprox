<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>TellProx Login</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link href="static/css/bootstrap.min.css" rel="stylesheet">
	<link href="static/css/flat-ui.css" rel="stylesheet">
	<link href="static/css/site.css" rel="stylesheet">
</head>

<body>		
	<div class="main-login">
	<form method="post" action="postlogin">
		<div class="main-login-screen">
			<div class="login-icons">
				<h4>TellProx</h4>
			</div>

			<div class="main-login-form">
				<div class="form-group">
					<input type="text" class="form-control login-field" name="username"
						placeholder="Enter your name" id="login-name" />
					<label class="login-field-icon fui-user" for="login-name"></label>
				</div>

				<div class="form-group">
					<input type="password" class="form-control login-field" name="password"
						placeholder="Password" id="login-pass" />
					<label class="login-field-icon fui-lock" for="login-pass"></label>
				</div>

				<input type="submit" class="btn btn-primary btn-lg btn-block" value="login"></input>
			</div>
		</div>
	</form>
	</div>
</body>
</html>