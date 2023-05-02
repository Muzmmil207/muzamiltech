/**
* Easy selector helper function
*/
const select = (el, all = false) => {
    el = el.trim()
    if (all) {
        return [...document.querySelectorAll(el)]
    } else {
        return document.querySelector(el)
    }
}

/**
* Easy event listener function
*/
const on = (type, el, listener, all = false) => {
    if (all) {
        select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
        select(el, all).addEventListener(type, listener)
    }
}

/**
 * Easy on scroll event listener 
 */
const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
}

let homeDevices = null
let phonesDevices = select('phones-devices')
const appendDevices = () => {
    console.log(homeDevices)
    if (phonesDevices) {
        if (homeDevices === null) {
            homeDevices = []
        }
    }
    console.log(homeDevices)
}
window.addEventListener('load', appendDevices)
onscroll(document, appendDevices)

