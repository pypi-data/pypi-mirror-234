function getCookie (key) {
  let value = ''
  document.cookie.split(';').forEach((e)=>{
     if(e.includes(key)) {
        value = e.split('=')[1]
     }
  })
return value
}