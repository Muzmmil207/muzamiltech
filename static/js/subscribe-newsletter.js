const subscribeForm = document.getElementById('subscribe-form')
subscribeForm.addEventListener('submit', (e) => {
    e.preventDefault()
    var email = document.getElementById('subscribe-form-input').value

    fetch('/subscribe-handler', {
        method: "POST",
        headers: {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'email': email })
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            let div = subscribeForm.parentNode
            div.removeChild(subscribeForm)
            var thanksMessage = document.createElement('p')
            thanksMessage.innerText = data
            div.appendChild(thanksMessage)
        })

})
