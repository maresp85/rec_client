fetch('http://l2.io/ip.js?var=myip', {
   headers: {
      'Accept': 'application/json'
   }
})
   .then(response => response.text())
   .then(text => document.getElementById('ip_address').value = text)