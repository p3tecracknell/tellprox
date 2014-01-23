var sort_by = function(field, reverse, primer) {
   var key = function (x) {return primer ? primer(x[field]) : x[field]};

   return function (a,b) {
	  var A = key(a), B = key(b);
	  return ( (A < B) ? -1 : ((A > B) ? 1 : 0) ) * [-1,1][+!!reverse];                  
   }
}

function br()    { return $(document.createElement('br'));   }
function div()   { return $(document.createElement('div'));   }
function span()  { return $(document.createElement('span'));   }
function h(i)    { return $(document.createElement('h' + i));   }
function label() { return $(document.createElement('label')); }
function a()     { return $(document.createElement('a'));     }
function radio() { return $(document.createElement('input')).attr({type: 'radio' }); }
function inputtext() { return $(document.createElement('input')).attr({type: 'text' }); }
function checkbx(checked) {
	return $(document.createElement('input')).attr({type: 'checkbox' }).prop('checked', checked);
}
function dropdown(data) {
	var s = $(document.createElement('select'));
	$.each(data, function(key, val) {
		var splits = val.split('|');
		$('<option />', {value: splits[0], text: splits[1] || val}).appendTo(s);
	});
	return s;
}