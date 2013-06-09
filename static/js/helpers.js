var sort_by = function(field, reverse, primer) {
   var key = function (x) {return primer ? primer(x[field]) : x[field]};

   return function (a,b) {
	  var A = key(a), B = key(b);
	  return ( (A < B) ? -1 : ((A > B) ? 1 : 0) ) * [-1,1][+!!reverse];                  
   }
}

function div()   { return $(document.createElement('div'));   }
function span()  { return $(document.createElement('span'));   }
function h(i)    { return $(document.createElement('h'+i));   }
function label() { return $(document.createElement('label')); }
function a()     { return $(document.createElement('a'));     }
function radio() { return $(document.createElement('input')).attr({type: 'radio' }); }
function input() { return $(document.createElement('input')).attr({type: 'text' }); }