/* $(document).ready(function(){ 
    $("form").submit(function(){
      alert("Submitted");
    });
    $("#bot").click(function(){
      var SendInfo={
      "Precio Fabrica":document.getElementById("Precio Fabrica").value,
      "Almacenamiento":document.getElementById("Almacenamiento").value,
      "Bateria":document.getElementById("Bateria").value,
      "Tiene Memoria Adicional":document.getElementById("Tiene Memoria Adicional").value,
      "Camara":document.getElementById("Camara").value,
      "Camara Video":document.getElementById("Camara Video").value,
      "Selfie":document.getElementById("Selfie").value,
      "Selfie Video":document.getElementById("Selfie Video").value,
      "Procesamiento":document.getElementById("Procesamiento").value,
      "RAM":document.getElementById("RAM").value,
      "Resolucion":document.getElementById("Resolucion").value,
      "Tamanio":document.getElementById("Tamanio").value,
      "Tiene Lector Huella":document.getElementById("Tiene Lector Huella").value,
      "Reconocimiento Rostro":document.getElementById("Reconocimiento Rostro").value,
      "Reciente":document.getElementById("Reciente").value,
      "Tiene Audifonos":document.getElementById("Tiene Audifonos").value,
      "Tiene Bluetooth":document.getElementById("Tiene Bluetooth").value,
      "Tiene Radio":document.getElementById("Tiene Radio").value,
      "Tiene Localizacion":document.getElementById("Tiene Localizacion").value,
      "Tiene NFC":document.getElementById("Tiene NFC").value,
      "Tiene SIM":document.getElementById("Tiene SIM").value};
      console.log(SendInfo);

      $.ajax({
        type: 'POST',
        url: '/product',
        data: JSON.stringify(SendInfo),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function (data) {
            console.log("Response: ", data);
            if(data['result']=='success'){
              location.replace("product.html")
            }
        }    
    }); 
    });
  }); */

