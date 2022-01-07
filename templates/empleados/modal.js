$(function(){
     $("#news").on("submit", function(e){
         e.preventDefault();
         var f = $(this);
         var formData = new FormData(document.getElementById("news"));
         formData.append("dato", "valor");

         //una ves se presione el boton y antes de enviar por ajax
         if ($("#nombre").val().trim() != '') {
            if ($("#email").val().trim() != '') {
              //aqui tu codigo si todo es correcto
            }else{
              alert('email vacio');
            }
         }else{
          alert('nombre vacio');
         }

     });
});