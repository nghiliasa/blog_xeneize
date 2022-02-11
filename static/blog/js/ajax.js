/*..............................................................................................
... PARA VALIDAR LOS DATOS .....................................................
.............................................................................................*/
var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method){
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/*..............................................................................................
... TODOS LOS CURSOS .............................................................
............................................................................................. */
$( "#boton_prod" ).click(function(){
	valor = $( "#id_querycom" ).val();
	respuestabusqueda(valor)
});

function respuestabusqueda(valor){
    $.ajax({
        beforeSend : function(xhr, settings){
			if(!csrfSafeMethod(settings.type) && !this.crossDomain){
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		url : "/datos/",
		type : "GET",
		data : { valor : valor,},
		success : function(json){

            valor_retornado2 = "<i class='fa fa-play' aria-hidden='true'></i>"
            valor_retornado3 = "<img class='img-fluid rounded border' src='/media/"+json[0].imagen+"' alt='Imagen'/>"
            valor_retornado4 = "<em>"+json[0].titulo+" ("+json[0].agno+")</em>"
            imagen = "<img class='img-fluid rounded border mb-2' src='/media/"+json[0].imagen+"' alt='#'/>"
            titulo = ""+json[0].titulo+""
            titulo_original = ""+json[0].titulo_original+""
            pais = ""+json[0].pais+""
            agno = ""+json[0].agno+""
            genero = ""+json[0].genero+""
            puntaje = ""+json[0].puntaje+""
            duracion = ""+json[0].duracion+" minutos"
            director = ""+json[0].director+""
            reparto = ""+json[0].reparto+""
            sinopsis = ""+json[0].sinopsis+""
            link = "<IFRAME SRC='"+json[0].link+"' FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=300 HEIGHT=200 allowfullscreen></IFRAME>"



            $('#contenedor_filtrado').html(valor_retornado2);

            $('#contenedor_filtrado2').html(valor_retornado3);

            $('#contenedor_filtrado3').html(valor_retornado4);

            $('#imagen').html(imagen);

            $('#titulo').html(titulo);

            $('#titulo_original').html(titulo_original);

            $('#pais').html(pais);

            $('#agno').html(agno);

            $('#genero').html(genero);

            $('#puntaje').html(puntaje);

            $('#duracion').html(duracion);

            $('#director').html(director);

            $('#reparto').html(reparto);

            $('#sinopsis').html(sinopsis);

            $('#link').html(link);

		},
		error : function(xhr, errmsg, err){
			console.log('Error en carga de respuesta');
		},
    });
}
