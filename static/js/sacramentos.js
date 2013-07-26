$(document).on('ready', inicio);
document.write('<script src="/static/js/acta.js" type="text/javascript"></script>');
 
function inicio(){
	usuarioCreate();

	modelo_tablas('#id_table_libro, #id_table_feligres,#id_table_matrimonio,#id_table_bautismo,#id_table_eucaristia,#id_table_confirmacion');
	// modelo_tablas('#id_table_libro');
	campos_con_fechas();


}

function campos_con_fechas(){
	$('#id_fecha_nacimiento').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_form_sacramento #id_fecha_sacramento').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_form_libro #id_fecha_apertura').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_fecha_cierre').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	
}

function usuarioCreate(){

	$('#id_form_usuario_create').on('submit', function(e){
		e.preventDefault();
		json = $('#id_form_usuario_create').serialize()
		url = '/usuario/add/';
		$.post(url, json, function(data, status, jqXHR){
			if(data.valido){
				// $('#id_confirm_usuario_create').modal('show');
				var mensaje = '<div class="alert alert-success">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/success.png" alt=""> Usuario Creado exitosamente </div>';
				$('#id_mensaje').html(mensaje);
			} else {
				var mensaje = '<div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> Uno o más datos no son correctos </div>';
				$('#id_mensaje').html(mensaje);
				console.log(data.errores_usuario);
				console.log(data.errores_perfil);
				$.each(data.errores_usuario, function(index, element){
					$("#id_"+index).addClass('invalid');
					console.log("#id_"+index);
					console.log("#id_"+element);
					var mensajes_error = '<span>' + element+ '</span>';
					console.log(mensajes_error);
					$("#id_errors_"+index).append(mensajes_error);
				});
				console.log(data.errores_perfil);
				$.each(data.errores_perfil, function(index, element){
					$("#id_"+index).addClass('invalid');
					console.log("#id_"+index);
					console.log("#id_"+element);
					var mensajes_error = '<span>' + element+ '</span>';
					console.log(mensajes_error);
					$("#id_errors_"+index).append(mensajes_error);
				});
			}
		});

$('#id_aceptar').on('click',function(e){
	e.preventDefault();
	$('#id_confirm_usuario_create').modal('hide');
});

});

}


