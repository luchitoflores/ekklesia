$(document).on('ready', inicio);


function inicio(){
	usuarioCreate();
}


function usuarioCreate(){

	$('#id_form_usuario_create').on('submit', function(e){
		e.preventDefault();
		json = $('#id_form_usuario_create').serialize()
		url = '/usuario/add/';
		$.post(url, json, function(respuesta, estado, jqXHR){
			console.log(respuesta.respuesta);
			$('#id_confirm_usuario_create').modal('show');

		});
		$('#id_aceptar').on('click',function(e){
			e.preventDefault();
			$('#id_confirm_usuario_create').modal('hide');


		});

	});
	
}
