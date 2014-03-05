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
function ul()    { return $(document.createElement('ul'));     }
function li()    { return $(document.createElement('li'));     }
function select(){ return $(document.createElement('select'));     }
function option(text, value){ return $(document.createElement('option')).attr({value: value}).text(text); }
function radio() { return $(document.createElement('input')).attr({type: 'radio' }); }
function inputtext() { return $(document.createElement('input')).attr({type: 'text' }); }
function checkbx(checked) {
	return $(document.createElement('input')).attr({type: 'checkbox' }).prop('checked', checked);
}
function dropdown(data) {
	var buffer = $.map(data, function(val) {
		var splits = val.split('|');
		return option(splits[1] || val, splits[0]);
	});
	return select().append(buffer);
}

function mapSorted(map, worker) {
    var keys = Object.keys(map).sort(),
		key, i;

	var map = [];
    for (i = 0; i < keys.length; i++) {
		key = keys[i];
        map.push(worker(key, map[key]));
    }
	return map;
}

function selectFirstDropdown($select) {
	$select.prop('selectedIndex',0).trigger('change');
}

function setDropdownFromText($select, lookFor) {
	$select.children('option').each(function() {
		if ($(this).text() == lookFor) {
			$(this).attr('selected', 'selected').trigger('change');            
		}
	});
}

function getHash() {
	return window.location.hash.substring(1);
}

function getValue(input) {
	if (input.attr('type') == 'checkbox')
		return input.is(':checked');
	else
		return input.val();
}