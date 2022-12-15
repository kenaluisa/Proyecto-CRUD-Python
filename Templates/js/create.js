function guardar() {
 
    let n = document.getElementById("txtNombre").value
    let p = document.getElementById("txtImagen").value
    let s = document.getElementById("txtDescripcion").value
 
    let receta = {
        nombre: n,
        imagen: p,
        descripcion: s
    }
    let url = "https://kenaluisa.pythonanywhere.com/recetas"
    var options = {
        body: JSON.stringify(receta),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
       // redirect: 'follow'
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
 
            // Handle response we get from the API
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar")
            console.error(err);
        })
    //window.location.href = "index.html";  //NUEVO    
    
}
