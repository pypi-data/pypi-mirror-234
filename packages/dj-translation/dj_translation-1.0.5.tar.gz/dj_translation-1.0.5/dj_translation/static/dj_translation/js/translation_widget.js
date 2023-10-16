window.TranslationWidgetHandlersInitialized = false

class TranslationWidget {

    constructor(element) {
        if (typeof element === "undefined" || element === null) return;

        this.innerValue = {}
        this.activeKeys = {input: null, display: null}
        this.element = element
        this.name = this.element.getAttribute('data-djt-name')
        this.valueInput = this.element.querySelector(`#id_${this.name}`)

        this.displayToggle = this.element.querySelector('.djt-button.djt-button--display-toggle')

        this.initializeValue()
        this.setLanguages()
        this.setActiveKeys()

        // sets widget elements
        this.setTabsGroups()

        this.setDisplayArea()

        this.setTextInput()


        this.textInput.initialize()

        this.initHandlers()

        DJTUtils.data(this.element).set('translation-widget', this)
    }

    get value() {
        return this.innerValue
    }

    set value(value) {
        this.innerValue = value
        this.valueListener(value)
    }

    valueListener(value) {
        this.valueInput.value = JSON.stringify(value)
    }

    initializeValue() {
        this.value = JSON.parse(this.valueInput.value)
    }

    setLanguages() {
        this.languages = JSON.parse(this.element.getAttribute('data-djt-languages')) || []
    }

    setTabsGroups() {
        this.tabsGroups = {
            input: new Tabs(this.element.querySelector('[data-djt-group="input"]'), {
                type: 'input',
                active: this.activeKeys['input']
            }),
            display: new Tabs(this.element.querySelector('[data-djt-group="display"]'), {
                type: 'display',
                active: this.activeKeys['display']
            }),
        }
    }

    setDisplayArea() {
        var self = this
        var {code: key, bidi} = this.languages.find(function (lang) {
            return lang.code === self.activeKeys['display']
        })
        this.displayArea = new DJTDisplay(this.element.querySelector('[data-djt-toggle="display"]'), {
            bidi,
            key,
            value: self.value[key]
        })
    }

    setTextInput() {
        var self = this
        var {code: key, bidi} = this.languages.find(function (lang) {
            return lang.code === self.activeKeys['input']
        })
        this.textInput = EditorFactory(this.element.querySelector('[data-djt-toggle="input"]'), {
            bidi,
            key,
            name: self.name,
            value: self.value[key] || ''
        })
    }

    setActiveKeys(group = null, key = null) {
        var tabsGroup = group || 'input'
        var langKey = key || this.languages[0].code
        this.activeKeys[tabsGroup] = langKey

        for (var activeKey in this.activeKeys) {
            if (this.activeKeys.hasOwnProperty(activeKey)) {
                if (activeKey !== tabsGroup) {
                    if(this.activeKeys[tabsGroup] === langKey) {
                        this.activeKeys[activeKey] = this.languages.find(function (lang) {
                            return lang.code !== langKey
                        }).code
                    }
                }
            }
        }
    }


    initHandlers() {
        var self = this

        function getLanguageByKey(key) {
            return self.languages.find(function (lang) {
                return lang.code === key
            })
        }

        function activateTab(group) {
            for (var tabGroup in self.tabsGroups) {
                if (self.tabsGroups.hasOwnProperty(tabGroup)) {
                    if (tabGroup !== group) {
                        self.tabsGroups[tabGroup].activate(self.activeKeys[tabGroup])
                    }
                }
            }
        }

        function setDisplay() {
            var {code: key, bidi} = getLanguageByKey(self.activeKeys.display)
            self.displayArea.setValue({bidi, key, value: self.value[key] || ""})
        }

        function setInput() {
            var {code: key, bidi} = getLanguageByKey(self.activeKeys.input)
            self.textInput.setValue({bidi, key, value: self.value[key] || ""})
        }

        for (var tabGroup in this.tabsGroups) {
            if (this.tabsGroups.hasOwnProperty(tabGroup)) {
                this.tabsGroups[tabGroup].on('tab:clicked', function ({key, group}) {
                    self.setActiveKeys(group, key)
                    activateTab(group)
                    setDisplay()
                    setInput()
                })
            }
        }

        self.textInput.on('update:value', function (data) {
            var newValue = {...self.value}
            newValue[self.activeKeys.input] = data
            self.value = {...newValue}
        })

        this.displayToggle.addEventListener('click', function () {
            var display = self.element.querySelector('[data-djt-group="display-tab"].djt-container')
            if (display.classList.contains('djt-container--hidden')) {
                display.classList.remove('djt-container--hidden')
                self.element.classList.remove('djt--expanded')
            } else {
                display.classList.add('djt-container--hidden')
                self.element.classList.add('djt--expanded')
            }
        })
    }
}


TranslationWidget.getInstances = function (element) {
    if (!element) return null

    if (DJTUtils.data(element).has('translation-widget')) {
        return DJTUtils.data(element).get('translation-widget')
    }
    return null
}


TranslationWidget.createInstances = function (selector = '[data-toggle="dj-translation"]') {
    var elements = document.querySelectorAll(selector)
    if (elements && elements.length > 0) {
        for (var i = 0; i < elements.length; i++) {
            new TranslationWidget(elements[i])
        }
    }
}


TranslationWidget.init = function () {
    TranslationWidget.createInstances()

    if (window.TranslationWidgetHandlersInitialized === false) {
        window.TranslationWidgetHandlersInitialized = true
    }

}


// On document ready
if (document.readyState !== 'loading' && document.body) {
    TranslationWidget.init()
} else {
    document.addEventListener('DOMContentLoaded', TranslationWidget.init)
}