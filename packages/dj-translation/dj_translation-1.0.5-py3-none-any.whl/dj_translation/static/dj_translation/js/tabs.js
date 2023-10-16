class Tabs extends ClassEvent{
    activeClass = 'djt-button--active'
    defaultOptions = {
        type: 'input',
        active: null,
    }

    constructor(element, options) {
        super();
        this.options = DJTUtils.deepExtend({}, this.defaultOptions, options)
        this.element = element
        this.tabs = this.element.querySelectorAll(`[data-djt-toggle="${this.options.type}-tab"]`)

        this.initializeTabs()

        this.activate(this.options.active)
    }

    /*
    * sets tabs events
    */
    initializeTabs() {
        var self = this;
        this.tabs.forEach((tab) => {
            tab.addEventListener('click', function () {
                var key = this.getAttribute('data-djt-key');
                self.activate(key);
                self.emit('tab:clicked', {key, group: self.options.type})
            });
        });
    }
}


Tabs.prototype.activate = function (key) {
    var currentActiveTabs = this.element.querySelectorAll(`[data-djt-toggle="${this.options.type}-tab"].${this.activeClass}`)
    if (currentActiveTabs) {
        for (var i = 0; i < currentActiveTabs.length; i++) {
            currentActiveTabs[i].classList.remove(this.activeClass)
        }
    }
    this.element.querySelector(`[data-djt-toggle="${this.options.type}-tab"][data-djt-key="${key}"]`).classList.add(this.activeClass)
}

//
// Tabs.prototype.dispatchEvent = function (eventName, eventData) {
//     var customEvent = new CustomEvent(eventName, {
//         detail: eventData,
//         bubbles: true,
//         cancelable: true
//     });
//
//     this.element.dispatchEvent(customEvent);
// }


Tabs.prototype.addEventListener = function (eventName, callback) {
    this.element.addEventListener(eventName, callback);
};

