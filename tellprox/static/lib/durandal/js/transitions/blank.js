define(['durandal/system'], function(system) {
    return function(context) {
        return system.defer(function(dfd) {
            if (context.activeView) {
                $(context.activeView).hide();
            }
            $(context.child).show();

            dfd.resolve();
        }).promise();
    };
});
