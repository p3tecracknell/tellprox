define(['durandal/composition', 'knockout'], function(composition, ko) {
    return function() {
		this.buttons = [];
		this.buttonWidth;
		this.selectedValue;
		
		function ButtonViewModel(text, value) {
			this.text = text;
			this.value = value;
		}
		
		this.isActive = function(data) {
			return data.value == ko.unwrap(this.selectedValue());
		}.bind(this);
		
		this.setItem = function(parent) {
			parent.selectedValue(this.value);
		};
		
		this.activate = function(settings) {
			this.selectedValue = settings.selectedValue;
			this.numItems = settings.numItems;
			this.buttonWidth = (100 / this.numItems) + '%';
			
			if (this.numItems > 2) {
				for (var value = 0; value < this.numItems; value++) {
					var text = Math.round(100 * value / (this.numItems - 1)) + '%';
					this.buttons.push(new ButtonViewModel(text, value));
				}
			} else {
				this.buttons.push(new ButtonViewModel('On', 1));
				this.buttons.push(new ButtonViewModel('Off', 0));
			}
		};
	}
});