$(document).on('ready', inicio);
document.write('<script src="/static/js/acta.js" type="text/javascript"></script>');

function inicio(){
	usuarioCreate();
	tablas_estilo_bootstrap();
	modelo_tablas('#id_table_libro, #id_table_feligres,#id_table_matrimonio,#id_table_bautismo,#id_table_eucaristia,#id_table_confirmacion');
	campos_con_fechas();
	radio_button();
	deshabilitar_campos('#id_form_padre input:text, #id_form_padre select');
	deshabilitar_campos('#id_form_bautizado input:text, #id_form_bautizado select');
	prueba();
}

function limpiar_campos(campos){
	$(campos).val('');
}

function habilitar_campos(campos){
	$(campos).prop('disabled', false);
}

function deshabilitar_campos(campos){
	$(campos).prop('disabled', true);
	// $(campos).attr('disabled', 'disabled');
}

function mostrar_html(identificadorhtml){
	$(identificadorhtml).attr('style', 'display:auto');
	// $(identificadorhtml).css('display', 'auto');
}

function ocultar_html(identificadorhtml){
	$(identificadorhtml).attr('style', 'display:none');
	// $(identificadorhtml).css('display', 'none');
}


function radio_button(){
	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		$(this).prop("checked", true);
		if($(this).is(":checked")){
			$(this).addClass('btn-primary');
		}
		if ($(this).attr('id')=='id_button_cedula'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres').removeClass('btn btn-primary').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_nombres').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres, #id_query_apellidos'); 
		}
		if ($(this).attr('id')=='id_button_nombres'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula').removeClass('btn btn-primary').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_cedula').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula'); 
		}
	});
}

function campos_con_fechas(){
	$('#id_fecha_nacimiento').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_fecha_sacramento').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_form_libro #id_fecha_apertura').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	$('#id_fecha_cierre').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	
}

function usuarioCreate(){
	$('#id_form_usuario_create').on('submit', function(e){
		e.preventDefault();
		json = $('#id_form_usuario_create').serialize();
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
});
}

function prueba(){
	$('#id_form_busqueda').on('submit', function(e){
		e.preventDefault();
		var url= '/api/usuario/';
		var nombres = $('#id_query_nombres').val();
		var apellidos = $('#id_query_apellidos').val();
		var cedula = $('#id_query_cedula').val();
		mostrar_html("#id_table_busqueda_usuarios");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula};
		var columnas = [
		{ "mData" : "link", "bSortable": true},
		{ "mData" : "apellidos", "bSortable": true},
		{ "mData" : "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			tablas_busqueda_ajax("#id_table_busqueda_usuarios", columnas, data.perfiles);
			var map = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_de_lista(map);
		});
	});
}

function almacenar_busqueda_en_map(lista){
	var map = {};
	$.each(lista, function(index, element){
		map[element.id] = element; 
	}); 
	return map;
}

function devolver_campos_de_lista(map){
	$('a#id_click').on('click', function(e){
		// alert('estoy aqui');
		e.preventDefault();
		$("#id_buscar_padre").modal('hide');  //$(this).parents("div:first").html(...);
		console.log('prueba: ' + $(this).parents('tr').attr('id'));
		var id =  $(this).parents('tr').attr('id');
		console.log(map[id]);
		var objeto = map[id];

		console.log(objeto.nombres);
		$('#id_form_padre #id_first_name').attr('value', objeto.nombres);
		$('#id_form_padre #id_last_name').attr('value', objeto.apellidos);
		$('#id_form_padre #id_dni').attr('value', objeto.dni);
		$('#id_form_padre #id_profesion').attr('value', objeto.profesion);
		$('#id_form_padre #id_lugar_nacimiento').attr('value', objeto.lugar_nacimiento);
		// $('#id_form_padre #id_estado_civil').attr('value', objeto.estado_civil);
		$('#id_form_padre #id_estado_civil option[value="'+objeto.estado_civil+'"]').prop('selected', true);
	});
}

function asignar_padre(identificadorform){
	$(identificadorform).on('click', function(e){
		e.preventDefault();
		//obtener id del feligres
		//obtener id del padre


	});
}



