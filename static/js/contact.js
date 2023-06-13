let contactForm = document.getElementById('contact-form')
contactForm.addEventListener('submit', contactFormSubmitHandler)

function contactFormSubmitHandler(e) {

    e.preventDefault()
    var name = document.getElementById('contact-name').value
    var email = document.getElementById('contact-email').value
    var message = document.getElementById('contact-message').value

    fetch('/contact-handler', {
        method: "POST",
        headers: {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'name': name, 'email': email, 'message': message })
    })
        .then((response) => response.json())
        .then((data) => {
            let div = contactForm.parentNode
            div.removeChild(contactForm)
            var thanksMessage = document.createElement('p')
            thanksMessage.innerHTML = data
            div.appendChild(thanksMessage)
        })
}