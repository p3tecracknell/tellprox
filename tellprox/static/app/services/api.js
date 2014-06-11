define(['jquery'], function ($) {
    return {
        auth: { key: apiKey },
        group : {
            remove: function(id, onComplete) { return $.post('json/group/remove', $.extend(this.auth, { id: id }), onComplete); }
        },
        sensor : {
            info: function(id, onComplete) { return $.post('json/sensor/info', $.extend(this.auth, { id: id }), onComplete); }
        , setname: function(id, name, onComplete) { return $.post('json/sensor/setname', $.extend(this.auth, { id: id, name: name }), onComplete); }
        , setignore: function(id, ignore, onComplete) { return $.post('json/sensor/setignore', $.extend(this.auth, { id: id, ignore: ignore }), onComplete); }
        },
        clients : {
            list: function(extras, onComplete) { return $.post('json/clients/list', $.extend(this.auth, { extras: extras }), onComplete); }
        },
        devices : {
            list: function(supportedMethods, onComplete) { return $.post('json/devices/list', $.extend(this.auth, { supportedMethods: supportedMethods }), onComplete); }
        },
        client : {
            info: function(id, onComplete) { return $.post('json/client/info', $.extend(this.auth, { id: id }), onComplete); }
        },
        api : {
            install: function(onComplete) { return $.post('json/api/install', this.auth, onComplete); }
        , list: function(onComplete) { return $.post('json/api/list', this.auth, onComplete); }
        , shutdown: function(onComplete) { return $.post('json/api/shutdown', this.auth, onComplete); }
        , restart: function(onComplete) { return $.post('json/api/restart', this.auth, onComplete); }
        },
        scheduler : {
            removejob: function(id, onComplete) { return $.post('json/scheduler/removejob', $.extend(this.auth, { id: id }), onComplete); }
        , jobinfo: function(id, onComplete) { return $.post('json/scheduler/jobinfo', $.extend(this.auth, { id: id }), onComplete); }
        , joblist: function(onComplete) { return $.post('json/scheduler/joblist', this.auth, onComplete); }
        , setjob: function(id, deviceId, method, methodValue, type, hour, minute, offset, randomInterval, retries, retryInterval, reps, active, weekdays, onComplete) { return $.post('json/scheduler/setjob', $.extend(this.auth, { id: id, deviceId: deviceId, method: method, methodValue: methodValue, type: type, hour: hour, minute: minute, offset: offset, randomInterval: randomInterval, retries: retries, retryInterval: retryInterval, reps: reps, active: active, weekdays: weekdays }), onComplete); }
        },
        device : {
            info: function(id, supportedMethods, onComplete) { return $.post('json/device/info', $.extend(this.auth, { id: id, supportedMethods: supportedMethods }), onComplete); }
        , dim: function(id, level, onComplete) { return $.post('json/device/dim', $.extend(this.auth, { id: id, level: level }), onComplete); }
        , toggle: function(id, onComplete) { return $.post('json/device/toggle', $.extend(this.auth, { id: id }), onComplete); }
        , learn: function(id, onComplete) { return $.post('json/device/learn', $.extend(this.auth, { id: id }), onComplete); }
        , setname: function(id, name, onComplete) { return $.post('json/device/setname', $.extend(this.auth, { id: id, name: name }), onComplete); }
        , setprotocol: function(id, protocol, onComplete) { return $.post('json/device/setprotocol', $.extend(this.auth, { id: id, protocol: protocol }), onComplete); }
        , bell: function(id, onComplete) { return $.post('json/device/bell', $.extend(this.auth, { id: id }), onComplete); }
        , stop: function(id, onComplete) { return $.post('json/device/stop', $.extend(this.auth, { id: id }), onComplete); }
        , up: function(id, onComplete) { return $.post('json/device/up', $.extend(this.auth, { id: id }), onComplete); }
        , remove: function(id, onComplete) { return $.post('json/device/remove', $.extend(this.auth, { id: id }), onComplete); }
        , down: function(id, onComplete) { return $.post('json/device/down', $.extend(this.auth, { id: id }), onComplete); }
        , add: function(clientId, name, protocol, model, onComplete) { return $.post('json/device/add', $.extend(this.auth, { clientId: clientId, name: name, protocol: protocol, model: model }), onComplete); }
        , turnoff: function(id, onComplete) { return $.post('json/device/turnoff', $.extend(this.auth, { id: id }), onComplete); }
        , command: function(id, value, method, onComplete) { return $.post('json/device/command', $.extend(this.auth, { id: id, value: value, method: method }), onComplete); }
        , execute: function(id, onComplete) { return $.post('json/device/execute', $.extend(this.auth, { id: id }), onComplete); }
        , setmodel: function(id, model, onComplete) { return $.post('json/device/setmodel', $.extend(this.auth, { id: id, model: model }), onComplete); }
        , turnon: function(id, onComplete) { return $.post('json/device/turnon', $.extend(this.auth, { id: id }), onComplete); }
        , setparameter: function(id, parameter, value, onComplete) { return $.post('json/device/setparameter', $.extend(this.auth, { id: id, parameter: parameter, value: value }), onComplete); }
        },
        sensors : {
            list: function(includeignored, onComplete) { return $.post('json/sensors/list', $.extend(this.auth, { includeignored: includeignored }), onComplete); }
        },
        config : {
            getall: function(onComplete) { return $.post('json/config/getall', this.auth, onComplete); }
        , set: function(item, value, onComplete) { return $.post('json/config/set', $.extend(this.auth, { item: item, value: value }), onComplete); }
        , get: function(item, onComplete) { return $.post('json/config/get', $.extend(this.auth, { item: item }), onComplete); }
        }
    }
});