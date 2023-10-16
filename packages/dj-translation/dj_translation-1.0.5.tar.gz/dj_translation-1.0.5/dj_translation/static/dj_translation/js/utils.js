window.TranslationInputDataStore = {}
window.TranslationInputDataStoreID = 0
window.TranslationInputDelegatedEventHandlers = {}


var DJTUtils = function () {
    return {
        deepExtend(out) {
            out = out || {};

            for (var i = 1; i < arguments.length; i++) {
                var obj = arguments[i];
                if (!obj) continue;

                for (var key in obj) {
                    if (!obj.hasOwnProperty(key)) {
                        continue;
                    }

                    // based on https://javascriptweblog.wordpress.com/2011/08/08/fixing-the-javascript-typeof-operator/
                    if (Object.prototype.toString.call(obj[key]) === '[object Object]') {
                        out[key] = DJTUtils.deepExtend(out[key], obj[key]);
                        continue;
                    }

                    out[key] = obj[key];
                }
            }

            return out;
        },

        data(el) {
            return {
                set: function (name, data) {
                    if (!el) {
                        return;
                    }

                    if (el.customDataTag === undefined) {
                        window.TranslationInputDataStoreID++;
                        el.customDataTag = window.TranslationInputDataStoreID;
                    }

                    if (window.TranslationInputDataStore[el.customDataTag] === undefined) {
                        window.TranslationInputDataStore[el.customDataTag] = {};
                    }

                    window.TranslationInputDataStore[el.customDataTag][name] = data;
                },

                get: function (name) {
                    if (!el) {
                        return;
                    }

                    if (el.customDataTag === undefined) {
                        return null;
                    }

                    return this.has(name) ? window.TranslationInputDataStore[el.customDataTag][name] : null;
                },

                has: function (name) {
                    if (!el) {
                        return false;
                    }

                    if (el.customDataTag === undefined) {
                        return false;
                    }

                    return !!(window.TranslationInputDataStore[el.customDataTag] && window.TranslationInputDataStore[el.customDataTag][name]);
                },

                remove: function (name) {
                    if (el && this.has(name)) {
                        delete window.TranslationInputDataStore[el.customDataTag][name];
                    }
                }
            };

        },
        addEvent(el, type, handler, one) {
            if (typeof el !== 'undefined' && el !== null) {
                el.addEventListener(type, handler);
            }
        },
        getUniqueId(prefix) {
            return prefix + Math.floor(Math.random() * (new Date()).getTime());
        },
        on(element, selector, event, handler) {
            if (element === null) {
                return;
            }

            var eventId = DJTUtils.getUniqueId('event');

            window.TranslationInputDelegatedEventHandlers[eventId] = function (e) {
                var targets = element.querySelectorAll(selector);
                var target = e.target;

                while (target && target !== element) {
                    for (var i = 0, j = targets.length; i < j; i++) {
                        if (target === targets[i]) {
                            handler.call(target, e);
                        }
                    }

                    target = target.parentNode;
                }
            }

            DJTUtils.addEvent(element, event, window.TranslationInputDelegatedEventHandlers[eventId]);

            return eventId;
        },
    }
}()