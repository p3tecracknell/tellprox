requirejs.config({
    paths: {
        'text': '../lib/require/text',
        'durandal':'../lib/durandal/js',
        'plugins' : '../lib/durandal/js/plugins',
        'transitions' : '../lib/durandal/js/transitions',
        'knockout': '../lib/knockout/knockout-2.3.0',
        'bootstrap': '../lib/bootstrap/js/bootstrap',
		'bootstrap-select': '../lib/bootstrap/js/bootstrap-select.min',
        'jquery': '../lib/jquery/jquery-1.9.1'
    },
    shim: {
        'bootstrap': {
            deps: ['jquery'],
            exports: 'jQuery'
       }
    }
});

define(['durandal/system', 'durandal/app', 'durandal/viewLocator', 'knockout', 'services/api'],  function (system, app, viewLocator, ko, api) {
	var debug = true;
	
    //>>excludeStart("build", true);
    system.debug(debug);
    //>>excludeEnd("build");
	
	var ErrorHandlingBindingProvider = function() {
		var original = new ko.bindingProvider(); 

		//determine if an element has any bindings
		this.nodeHasBindings = original.nodeHasBindings;

		//return the bindings given a node and the bindingContext
		this.getBindings = function(node, bindingContext) {
			var result;
			try {
				result = original.getBindings(node, bindingContext);
			}
			catch (e) {
				if (console && console.log) {
					console.log("Error in binding: " + e.message);   
				}
			}

			return result;
		};
	};

	if (debug) ko.bindingProvider.instance = new ErrorHandlingBindingProvider();

    app.title = 'Tellprox';

    app.configurePlugins({
        router: true,
        dialog: true,
        widget: true,
        dialog: true
    });

    app.start().then(function() {
        // Replace 'viewmodels' in the moduleId with 'views' to locate the view.
        // Look for partial views in a 'views' folder in the root.
        viewLocator.useConvention();

        // Show the app by setting the root view model for our application with a transition.
        app.setRoot('viewmodels/shell', 'blank');
    });
});