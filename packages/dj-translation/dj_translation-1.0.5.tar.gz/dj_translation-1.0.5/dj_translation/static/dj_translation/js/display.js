class DJTDisplay {
    defaultOptions = {bidi: null, key: null, value: ""}

    constructor(element, options) {
        this.options = DJTUtils.deepExtend({}, this.defaultOptions, options)
        this.element = element
        this.setValue(this.options)
    }

    setValue(options) {
        var {key, bidi, value} = options
        this.element.setAttribute('lang', key)
        this.element.setAttribute('dir', bidi ? 'rtl' : 'ltr')
        this.element.innerHTML = value || ""
    }
}