define(function() {
	return {
		sort_by: function(field, reverse, primer) {
			var key = function (x) { return primer ? primer(x[field]) : x[field]; };

			return function (a,b) {
				var A = key(a), B = key(b);
				return ( (A < B) ? -1 : ((A > B) ? 1 : 0) ) * [-1,1][+!!reverse];					 
			};
		},

		/*br:function(){ return $(document.createElement('br'));},
		div:function(){ return $(document.createElement('div'));},
		span:function(){ return $(document.createElement('span'));},
		h:function(i){ return $(document.createElement('h' + i));},
		label:function(){ return $(document.createElement('label'));},
		a:function(){ return $(document.createElement('a'));},
		ul:function(){ return $(document.createElement('ul'));},
		li:function(){ return $(document.createElement('li'));},
		select:function(){ return $(document.createElement('select'));},
		option:function(text, value){ return $(document.createElement('option')).attr({value: value}).text(text);},
		radio:function(){ return $(document.createElement('input')).attr({type: 'radio' });},
		inputtext:function(){ return $(document.createElement('input')).attr({type: 'text' });},
		checkbx:function(checked){
			return $(document.createElement('input')).attr({type: 'checkbox' }).prop('checked', checked);
		},
		dropdown: function(data) {
			var buffer = $.map(data, function(val) {
				var splits = val.split('|');
				return option(splits[1] || val, splits[0]);
			});
			return select().append(buffer);
		},*/

		mapSorted: function(map, worker) {
			var keys = Object.keys(map).sort(),
				key, i;

			map = [];
			for (i = 0; i < keys.length; i++) {
				key = keys[i];
				map.push(worker(key, map[key]));
			}
			return map;
		},

		selectFirstDropdown: function($select) {
			$select.prop('selectedIndex',0).trigger('change');
		},

		setDropdownFromText: function($select, lookFor) {
			$select.children('option').each(function() {
				if ($(this).text() == lookFor) {
					$(this).attr('selected', 'selected').trigger('change');
				}
			});
		},

		getHash: function() {
			return window.location.hash.substring(1);
		},

		getValue: function(input) {
			if (input.attr('type') == 'checkbox')
				return input.is(':checked');
			else
				return input.val();
		}
	};
});