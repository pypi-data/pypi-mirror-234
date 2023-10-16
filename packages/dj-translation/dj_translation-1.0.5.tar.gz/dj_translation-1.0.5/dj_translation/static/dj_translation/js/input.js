class BaseInput extends ClassEvent{
    defaultOptions = {};

    constructor(element, options) {
        super();
        this.options = DJTUtils.deepExtend({}, this.defaultOptions, options)
        this.element = element
    }
}


BaseInput.prototype.dispatchEvent = function (eventName, eventData) {
    var customEvent = new CustomEvent(eventName, {
        detail: eventData,
        bubbles: true,
        cancelable: true
    });

    this.element.dispatchEvent(customEvent);
}


BaseInput.prototype.addEventListener = function (eventName, callback) {
    this.element.addEventListener(eventName, callback);
};


BaseInput.prototype.create = function () {
}


BaseInput.prototype.setValue = function (value) {

}


/*
* issues:
* 1- ckeditor
* 2- event leaks
*
* solutions
* 1- events outting from this element exactly
* 2- replace djtinput with ckeditor and text input
* */


class RichText extends BaseInput {
    defaultOptions = {};
    editor = null

    constructor(element, options) {
        super(element, options);
    }


}


RichText.prototype.create = function () {
    var richText = this
    return new Promise(function (resolve, reject) {
        ClassicEditor
            .create(document.querySelector(`#${richText.options.name}-language-input`), {
                toolbar: JSON.parse(
                    richText.element.getAttribute('data-djt-richtext-config')
                ),
                language: richText.options.key
            })
            .then(function (editor) {
                richText.editor = editor;
                richText.editor.setData(richText.options.value)

                richText.editor.model.document.on('change:data', function () {
                    richText.emit('update:value', richText.editor.getData())
                })
                resolve()
            })
            .catch(function (error) {
                console.error(error);
                reject()
            })
    })

}

RichText.prototype.initialize = async function () {
    await this.create()
}


RichText.prototype.setValue = async function (options) {
    this.options = DJTUtils.deepExtend({}, this.options, options);
    var self = this;
    // this.editor.setData(options.value)

    // Check if editor exists and destroy it
    if (this.editor) {
        this.editor.destroy()
            .then(async function () {
                await self.create();
            })
            .catch(function (error) {
                console.error(error);
            });
    } else {
        // If editor doesn't exist, simply create it
        await this.create();
    }
};

class TextInput extends BaseInput {
    constructor(element, options) {
        super(element, options)
        this.editor = this
    }
}


TextInput.prototype.create = function () {
    this.element.setAttribute('lang', this.options.key)
    this.element.setAttribute('dir', this.options.bidi ? 'rtl' : 'ltr')
    this.element.value = this.options.value
    var self = this
    this.element.addEventListener('input', function (e) {
        self.dispatchEvent('text-input:change', {
            data: e.target.value,
        })
        self.emit('update:value', e.target.value)
    })
}


TextInput.prototype.setValue = async function (options) {
    this.element.value = options.value
    this.element.setAttribute('lang', options.key)
    this.element.setAttribute('dir', options.bidi ? 'rtl' : 'ltr')
}


TextInput.prototype.initialize = function () {
    this.create()
}


var EditorFactory = function (element, options) {
    // return new Promise(async function (resolve, reject) {

    var EditorClass = element.getAttribute('data-djt-richtext') === "true" ? RichText : TextInput
    return new EditorClass(element, options)

    // resolve(editor)
    // })
}