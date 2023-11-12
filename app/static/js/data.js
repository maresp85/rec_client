fetch('https://api.ipify.org?format=json', {
   headers: {
      'Accept': 'application/json'
   }
})
   .then(response => response.json())
   .then(text => document.getElementById('ip_address').value = text.ip)