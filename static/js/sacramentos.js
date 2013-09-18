$(document).on('ready', inicio);
document.write('<script src="/static/js/tablas.js" type="text/javascript"></script>');

function inicio(){
	crear_padre($('#id_form_crear_padre'), '#id_padre','#id_crear_padre', 'm');
	crear_padre($('#id_form_crear_madre'), '#id_madre','#id_crear_madre', 'f');
	crear_secretaria('#id_form_crear_secretaria', '#id_persona','#id_crear_secretaria');
	// crear_nota($('#id_form_crear_nota'), '#id_fecha','#id_descripcion', '#id_crear_nota');
	autocomplete('#id_padre');
	asignar_padre();
	// usuarioCreate();
	crear_nota_marginal($('#id_form_crear_nota'),'#id_crear_nota','/api/nota/add/');
	crear_nota_marginal($('#id_form_crear_nota_matrimonio'),'#id_crear_nota_matrimonio','/api/nota_matrimonio/add/');
	tablas_estilo_bootstrap();

	modelo_tablas('#id_table_secretaria, #id_table_libro,#id_table_asignar_parroquia,#id_table_log, #id_table_feligres, #id_table_matrimonio,#id_table_bautismo,#id_table_eucaristia,#id_table_confirmacion, #id_table_group, #id_table_parroquia, #id_table_provincia, #id_table_canton, #id_table_parroquia_civil, #id_table_sacerdotes');
	campos_con_fechas();
	radio_button();
	radio_button_sacerdotes();
	deshabilitar_campos('#id_form_padre input:text, #id_form_padre select');
	deshabilitar_campos('#id_form_bautizado input:text, #id_form_bautizado select');
	cargar_tabla_usuarios_en_modal();
	cargar_tabla_sacerdotes_en_modal();
	verificar_select_seleccionado();
	seleccionar_cantones('#id_provincia');
	seleccionar_parroquias('#id_canton');
	crear_direccion('#id_form_direccion');
	seleccionar_hora();
	controles_sacramentos();
	controles_feligres();	
	controles_reportes();
	controles_intenciones();
	controles_provincias();
}


function tables(){

	console.log('entre al tables');
	var oTable = $('#id_table_libro').dataTable({
        // ...
        "bProcessing": true,
        "bServerSide": true,
        "sAjaxSource": "{% url libro_json %}",
        "sPaginationType": "bootstrap",

        // "sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",

    });
}
// FUNCIONES PARA USAR CON JQUERY VALIDATE


// function validacion_reporte_sacramentos(){
	

// 	$('#id_form_anio').validate({

// 		rules:{
// 			anio:{required:true}
// 		},

// 		messages:{
// 			anio:{required:'Campo Año Obligatorio'}
// 		},
// 		errorElement:'div'
// 	});
// }

// function validacion_sacramentos(){
// 	$('#id_form_bautismo').validate({

// 		rules:{
// 			pagina:{required:true},
// 			numero_acta:{required:true},
// 			fecha_sacramento:{required:true},
// 			bautizado:{required:true},
// 			lugar_sacramento:{required:true},
// 			iglesia:{required:true},
// 			celebrante:{required:true},

// 		},

// 		messages:{
// 			pagina:{required:'Campo pagina obligatorio'},
// 			numero_acta:{required:'Campo numero acta obligatorio'},
// 			fecha_sacramento:{required:'Campo fecha sacramento obligatorio'},
// 			bautizado:{required:'Campo bautizado obligatorio'},
// 			lugar_sacramento:{required:'Campo lugar sacramento obligatorio'},
// 			iglesia:{required:'Campo iglesia obligatorio'},
// 			celebrante:{required:'Campo celebrante obligatorio'},
// 			// fecha_sacramento:{required:'Campo fecha sacramento Obligatorio'}
// 		},
// 		errorElement:'div'
// 	});

// 	$('#id_form_comunion').validate({

// 		rules:{
// 			pagina:{required:true},
// 			numero_acta:{required:true},
// 			fecha_sacramento:{required:true},
// 			feligres:{required:true},
// 			lugar_sacramento:{required:true},
// 			iglesia:{required:true},
// 			celebrante:{required:true},

// 		},

// 		messages:{
// 			pagina:{required:'Campo pagina obligatorio'},
// 			numero_acta:{required:'Campo numero acta obligatorio'},
// 			fecha_sacramento:{required:'Campo fecha sacramento obligatorio'},
// 			feligres:{required:'Campo feligres obligatorio'},
// 			lugar_sacramento:{required:'Campo lugar sacramento obligatorio'},
// 			iglesia:{required:'Campo iglesia obligatorio'},
// 			celebrante:{required:'Campo celebrante obligatorio'},
// 			// fecha_sacramento:{required:'Campo fecha sacramento Obligatorio'}
// 		},
// 		errorElement:'div'
// 	});

// 	$('#id_form_confirmacion').validate({

// 		rules:{
// 			pagina:{required:true},
// 			numero_acta:{required:true},
// 			fecha_sacramento:{required:true},
// 			confirmado:{required:true},
// 			lugar_sacramento:{required:true},
// 			iglesia:{required:true},
// 			celebrante:{required:true},

// 		},

// 		messages:{
// 			pagina:{required:'Campo pagina obligatorio'},
// 			numero_acta:{required:'Campo numero acta obligatorio'},
// 			fecha_sacramento:{required:'Campo fecha sacramento obligatorio'},
// 			confirmado:{required:'Campo confirmado obligatorio'},
// 			lugar_sacramento:{required:'Campo lugar sacramento obligatorio'},
// 			iglesia:{required:'Campo iglesia obligatorio'},
// 			celebrante:{required:'Campo celebrante obligatorio'},
// 			// fecha_sacramento:{required:'Campo fecha sacramento Obligatorio'}
// 		},
// 		errorElement:'div'
// 	});

// 	$('#id_form_matrimonio').validate({

// 		rules:{
// 			pagina:{required:true},
// 			numero_acta:{required:true},
// 			fecha_sacramento:{required:true},
// 			tipo_matrimonio:{required:true},
// 			novio:{required:true},
// 			novia:{required:true},
// 			lugar_sacramento:{required:true},
// 			iglesia:{required:true},
// 			celebrante:{required:true},
// 			testigo_novio:{required:true},
// 			testigo_novia:{required:true},

// 		},

// 		messages:{
// 			pagina:{required:'Campo pagina obligatorio'},
// 			numero_acta:{required:'Campo numero acta obligatorio'},
// 			fecha_sacramento:{required:'Campo fecha sacramento obligatorio'},
// 			tipo_matrimonio:{required:'Seleccione un valor'},
// 			novio:{required:'Campo novio obligatorio'},
// 			novia:{required:'Campo novia obligatorio'},
// 			lugar_sacramento:{required:'Campo lugar sacramento obligatorio'},
// 			iglesia:{required:'Campo iglesia obligatorio'},
// 			celebrante:{required:'Campo celebrante obligatorio'},
// 			testigo_novio:{required:'Campo testigo obligatorio'},
// 			testigo_novia:{required:'Campo testiga obligatorio'},
// 			// fecha_sacramento:{required:'Campo fecha sacramento Obligatorio'}
// 		},
// 		errorElement:'div'
// 	});

// }
// Función para añadir el widget multiselect
function widget_multiselect(identificador){
	$(identificador).multiSelect({
		selectableHeader: "<div style='background:#006dcc; color:white'>Permisos disponibles</div>",
		selectionHeader: "<div style='background:#006dcc; color:white'>Permisos elegidos</div>"
	});
	
	$('#id_select_all').click(function(){
		$(identificador).multiSelect('select_all');
		return false;
	});
	$('#id_delete_all').click(function(){
		$(identificador).multiSelect('deselect_all');
		return false;
	});
}

function mostrar_nota_marginal(idFieldSet){
	var v=$('#id_hidden').val();
	if(v!=0 & v>0){
		mostrar_html(idFieldSet);
	}

}  


function crear_nota_marginal(id_form,id_modal,url_rest){
	$(id_form).on('submit', function(e){
		e.preventDefault();
		var id=$('#id_hidden').val();
		var url = url_rest;
		var json = $(this).serialize()+"&id="+id+"";
		$.post(url, json, function(data){
			if(data.respuesta){
				$(id_modal).modal('hide');
				$('tbody tr').remove();
				$.each(data.tabla,function(index,element){
					$('tbody').append(element.tabla);
					habilitar_campos('#id_href');
				});
			} else{
				var mensaje = '<div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> Uno o más datos son invalidos </div>';
				$('#id_mensaje_nota').html(mensaje);
				$.each(data.errores_nota, function(index, element){
					// $("#id_"+index).addClass('invalid');
					// console.log("#id_"+index);
					// console.log("#id_"+element);
					var mensajes_error = '<span>' + element+ '</span>';
					// console.log("Hay errores en nota: " + mensajes_error);
					$("#id_errors_"+index).append(mensajes_error);

				});
				
				
			}
		});
	})
}



$(document).ajaxStart(function(){
	$('#spinner').show();
}).ajaxStop(function(){
	$('#spinner').hide();
});



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
function deshabilitar_campos2(campos){
	$(campos).prop('enabled', true);
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
		console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres').removeClass('btn btn-primary');
			$('#id_button_nombres').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_nombres').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres, #id_query_apellidos'); 
		}
		if ($(this).attr('id')=='id_button_nombres'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula').removeClass('btn btn-primary');
			$('#id_button_cedula').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_cedula').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula'); 
		}
	});

}

function radio_button_sacerdotes(){

	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula_s'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres_s').removeClass('btn btn-primary');
			$('#id_button_nombres_s').addClass('btn');
			$('#id_div_form_buscar_s').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula_s').attr('style', 'display:inline-block');
			$('#id_div_mensaje_sacerdote').attr('style', 'display:none');
			$('#id_div_busqueda_nombres_s').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s'); 
		}
		if ($(this).attr('id')=='id_button_nombres_s'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula_s').removeClass('btn btn-primary');
			$('#id_button_cedula_s').addClass('btn');
			$('#id_div_form_buscar_s').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres_s').attr('style', 'display:inline-block');
			$('#id_div_mensaje_sacerdote').attr('style', 'display:none');
			$('#id_div_busqueda_cedula_s').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula_s'); 
		}
	});

}


// function crear_nota(identificador, idnota,idnota2, idmodal){
// 	$(identificador).on('submit', function(e){
// 		e.preventDefault();
// 		var url = '/api/nota/add/';
// 		var json = $(this).serialize();
// 		$.post(url, json , function(data){
// 			if(!data.respuesta){
// 				console.log(data.errores_nota);
// 			}else{
// 				$(idnota).html('< value="'+ data.fecha+'">'+'>');
// 				$(idnota2).html('< value="'+ data.descripcion+'">');
// 				$(idmodal).modal('hide');
// 			}

// 		});
// 	});
// }

function campos_con_fechas(){
	// $('#id_fecha_sacramento').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	// $('#id_form_libro #id_fecha_apertura').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	// $('#id_fecha_cierre').attr('data-date-format', 'dd/mm/yyyy').datepicker();
	
}

// function usuarioCreate(){
// 	$('#id_form_usuario_create').on('submit', function(e){
// 		e.preventDefault();
// 		json = $('#id_form_usuario_create').serialize();
// 		url = '/usuario/add/';
// 		$.post(url, json, function(data, status, jqXHR){
// 			if(data.valido){
// 				// $('#id_confirm_usuario_create').modal('show');
// 				var mensaje = '<div class="alert alert-success">' + 
// 				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
// 				'<img src="/static/img/success.png" alt=""> Usuario Creado exitosamente </div>';
// 				$('#id_mensaje').html(mensaje);
// 			} else {
// 				var mensaje = '<div class="alert alert-error">' + 
// 				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
// 				'<img src="/static/img/error.png" alt=""> Uno o más datos no son correctos </div>';
// 				$('#id_mensaje').html(mensaje);
// 				console.log(data.errores_usuario);
// 				console.log(data.errores_perfil);
// 				$.each(data.errores_usuario, function(index, element){
// 					$("#id_"+index).addClass('invalid');
// 					console.log("#id_"+index);
// 					console.log("#id_"+element);
// 					var mensajes_error = '<span>' + element+ '</span>';
// 					console.log(mensajes_error);
// 					$("#id_errors_"+index).append(mensajes_error);
// 				});
// 				console.log(data.errores_perfil);
// 				$.each(data.errores_perfil, function(index, element){
// 					$("#id_"+index).addClass('invalid');
// 					console.log("#id_"+index);
// 					console.log("#id_"+element);
// 					var mensajes_error = '<span>' + element+ '</span>';
// 					console.log(mensajes_error);
// 					$("#id_errors_"+index).append(mensajes_error);
// 				});
// 			}
// 		});
// });
// }


//Muestra una tabla en un modal con los datos de feligreses después de una búsqueda
function cargar_tabla_usuarios_en_modal(){
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
			devolver_campos_de_lista(map,'#id_padre','#id_madre');
			devolver_campos_de_lista(map,'#id_novio','#id_novia');
			devolver_campos_a_sacramento(map,'#id_bautizado');
			devolver_campos_a_sacramento(map,'#id_feligres');
			devolver_campos_a_sacramento(map,'#id_confirmado');
			devolver_campos_a_secretaria(map, '#id_persona');


			
		});
	});
}

function cargar_tabla_sacerdotes_en_modal(){
	$('#id_form_busqueda_sacerdotes').on('submit', function(e){
		e.preventDefault();
		var url= '/api/sacerdote/';
		var nombres = $('#id_query_nombres_s').val();
		var apellidos = $('#id_query_apellidos_s').val();
		var cedula = $('#id_query_cedula_s').val();
		mostrar_html("#id_table_busqueda_sacerdotes");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula};
		var columnas = [
		{ "mData" : "link", "bSortable": true},
		{ "mData" : "apellidos", "bSortable": true},
		{ "mData" : "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			tablas_busqueda_ajax("#id_table_busqueda_sacerdotes", columnas, data.perfiles);
			var map = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_a_sacerdote(map,'#id_celebrante');

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


// Funcion para buscar y asignar usuarios a Matrimonio 
// todavia no vale para aignar padre y madre
function devolver_campos_de_lista(map,id_male,id_female){
	$('a#id_click').on('click', function(e){
		// alert('estoy aqui');
		e.preventDefault();
		$("#id_buscar_padre").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		if(objeto.sexo =='m'){
			$(id_male+' option').remove();
			$(id_male).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.nombres+" "+objeto.apellidos+'</option>')
		} 
		if (objeto.sexo =='f') {
			$(id_female+' option').remove();
			$(id_female).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.nombres+" "+objeto.apellidos+'</option>')
		}
	});
}

function devolver_campos_a_sacerdote(map, id_sacerdote){
	$('a#id_click').on('click', function(e){
		// alert('estoy aqui');
		e.preventDefault();
		$("#id_buscar_sacerdotes").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		$(id_sacerdote+' option').remove();
		$(id_sacerdote).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.nombres+" "+objeto.apellidos+'</option>')

	});
}

function devolver_campos_a_secretaria(map, id_persona){
	$('a#id_click').on('click', function(e){
		e.preventDefault();
		$("#id_buscar_secretaria").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		$(id_persona+' option').remove();
		$(id_persona).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.nombres + " " + objeto.apellidos+'</option>')
		
	});
}


// function devolver_campos_a_matrimonio(map,id_male,id_female){
// 	$('a#id_click').on('click', function(e){
// 		// alert('estoy aqui');
// 		e.preventDefault();
// 		$("#id_buscar_padre").modal('hide');  		
// 		var id =  $(this).parents('tr').attr('id');
// 		var objeto = map[id];
// 		console.log(objeto.sexo);
// 		if(objeto.sexo =='m'){
// 			$(id_male+' option').remove();
// 			$(id_male).append('<option value='+objeto.id+'>'+ objeto.nombres+" "+objeto.apellidos+'</option>')
// 		} 
// 		if (objeto.sexo =='f') {
// 			$(id_female+' option').remove();
// 			$(id_female).append('<option value='+objeto.id+'>'+ objeto.nombres+" "+objeto.apellidos+'</option>')
// 		}
// 	});
// }

// Funcion para buscar y asignar usuarios a Bautismo,Feligres,
// Confirmacion
function devolver_campos_a_sacramento(map,id_feligres){
	$('a#id_click').on('click', function(e){
		// alert('estoy aqui');
		e.preventDefault();
		$("#id_buscar_padre").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		$(id_feligres+' option').remove();
		$(id_feligres).append('<option value='+objeto.id+'>'+ objeto.nombres + " " + objeto.apellidos+'</option>')
		
	});
}


function asignar_padre(){
	$('#id_form_padre').on('submit', function(e){
		e.preventDefault();
		//obtener id del feligres
		//obtener id del padre
		var idfeligres = $('#id_perfil').val();
		var idpadre = $('#id_padre').val();
		console.log('padre' + idpadre);
		console.log('feligres'+idfeligres);
		var ctx = {'idfeligres': idfeligres, 'idpadre': idpadre};
		var url = '/api/asignarpadre/';
		$.post(url , ctx, function(data){
			if(data.bandera==true){
				console.log(data.bandera);
				$(location).attr('href','/usuario/');
			}else{
				console.log(data.bandera);
			}
		});

	});
}

function autocomplete(identificador){
	var labels = [];
	var datos = {};
	$(identificador).typeahead({
		source: function(query, process){
			labels = [];
			datos = {};
			var ctx = {'q': query};
			var url = '/api/usuario/';
			$.get(url, ctx, function(data){
				$.each(data.perfiles, function(index, element){

					labels.push(element.nombres);
					console.log(element.nombres);
					datos[element.nombres] = element;
					console.log(datos);
				});
				process(labels);
			});

		},
		minLength:3,
		highlighter: function(item){
			var p = datos[item];
			var itm = ''
			+ "<div class='typeahead_wrapper'>"
			+ "<div class='typeahead_labels'>"
			+ "<div class='typeahead_primary'>" + p.nombres + ' '+ p.apellidos +"</div>"
			+ "<div class='typeahead_secondary'>" + p.dni + '/' + p.lugar_nacimiento + "</div>"
			+ "</div>"
			+ "</div>";
			return itm;
		}
	});
}


//  Esta función llama a un modal para crear un padre para un feligrés
function crear_padre(identificador, idpadre, idmodal, sexo){
	$(identificador).on('submit', function(e){
		e.preventDefault();
		var url = '/api/padre/add/';
		var json = $(this).serialize()+'&sexo='+sexo;
		$.post(url, json , function(data){
			if(!data.respuesta){
				console.log(data.errores_usuario);
				console.log(data.errores_perfil);
			}else{
				$(idpadre).html('<option value="">-- Seleccione --</option><option value="'+ data.id+'" selected>'+data.full_name+'</option>');
				$(idmodal).modal('hide');
			}

		});
	});
}


//  Esta función llama a un modal para crear una secretaria
function crear_secretaria(identificador, idsecretaria, idmodal){
	$(identificador).on('submit', function(e){
		e.preventDefault();
		var url = '/api/secretaria/add/';
		var json = $(this).serialize();
		$.post(url, json , function(data){
			if(!data.respuesta){
				console.log(data.errores_usuario);
				console.log(data.errores_perfil);
			}else{
				$(idsecretaria).html('<option value="">-- Seleccione --</option><option value="'+ data.id+'" selected>'+data.full_name+'</option>');
				$(idmodal).modal('hide');
			}

		});
	});
}


//Permite crear via ajax una direccion
function crear_direccion(identificador){
	$(identificador).on('submit', function(e){
		e.preventDefault();
		var url = '/ciudades/direccion/add/'
		var json = $(this).serialize()
		$.post(url, json, function(data){
			if(data.respuesta){
				$('#id_modal_direccion').modal('hide');
			} else{
				console.log('Existen errores');
				console.log(data.errores);
			}
		});
	})
}

// Permite elegir los cantones de acuerdo a sus respectivas provincias
function seleccionar_cantones(identificador){
	$(identificador).on('change', function(e){
		$('#id_canton option').remove();
		$('#id_canton').prop('disabled', true);
		$('#id_parroquia option').remove();
		$('#id_parroquia').append('<option>---------</option>')
		$('#id_parroquia').prop('disabled', true);

		e.preventDefault();
		var url = '/api/ciudades/select/';
		var provincia = $(identificador + ' option:selected').text();
		var ctx = {'provincia': provincia}

		$.get(url, ctx, function(data){
			console.log(data.cantones)
			$.each(data.cantones, function(index, element){
				console.log(element);
				$('#id_canton').prop('disabled', false);
				$('#id_canton').append(element.option)
			});
		});
	})
}

// Permite elegir las parroquias de acuerdo a sus respectivos cantones
function seleccionar_parroquias(identificador){
	$(identificador).on('change', function(e){
		$('#id_parroquia option').remove();
		$('#id_parroquia').prop('disabled', true);
		e.preventDefault();
		var url = '/api/ciudades/select/';
		var canton = $(identificador + ' option:selected').text();
		var ctx = {'canton': canton}

		$.get(url, ctx, function(data){
			console.log(data.parroquias)
			$.each(data.parroquias, function(index, element){
				$('#id_parroquia').prop('disabled', false);
				$('#id_parroquia').append(element.option)
			});
		});
	})
}

// Permite verificar si un select tiene algun valor seleccionado
function verificar_select_seleccionado(){
	if($("#id_provincia option:selected").text()!= '-- Seleccione --'){
		$('#id_canton').prop('disabled', false);
		$('#id_parroquia').prop('disabled', false);
	}
}

function seleccionar_hora(){
	$('#id_tipo').on('change', function(e){
		
		console.log('Change de tipo')

		if ($('#id_tipo option:selected').text()=='Diario') {
			e.preventDefault();
			console.log('Entre al If de cambio');
			($('#id_div_hora')).css('display', 'inline-block');

			
		}else{
			($('#id_div_hora')).css('display', 'none');

		}
		
	});
}

function controles_sacramentos(){

	($('#id_pagina').numeric());
	($('#id_numero_acta').numeric());
	($('#id_numero_libro').numeric());
	($('#id_lugar_sacramento').alpha({allow:" "}));
	($('#id_iglesia').alpha({allow:" "}));
	($('#id_padrino').alpha({allow:" "}));
	($('#id_madrina').alpha({allow:" "}));
	($('#id_abuelo_paterno').alpha({allow:" "}));
	($('#id_abuela_paterna').alpha({allow:" "}));
	($('#id_abuelo_materno').alpha({allow:" "}));
	($('#id_abuela_materna').alpha({allow:" "}));
	($('#id_vecinos_paternos').alpha({allow:" "}));
	($('#id_vecinos_maternos').alpha({allow:" "}));
	// para nota marginal
	($('#id_descripcion').alpha({allow:" "}));

}

function controles_feligres(){

	($('#id_first_name').alpha({allow:" "}));
	($('#id_last_name').alpha({allow:" "}));
	($('#id_profesion').alpha({allow:" "}));
	($('#id_dni').numeric());
	($('#id_lugar_nacimiento').alpha({allow:" "}));
	($('#id_celular').numeric());
}
function controles_intenciones(){
	($('#id_intencion').alpha({allow:" "}));
	($('#id_oferente').alpha({allow:" "}));
	($('#id_ofrenda').numeric());

}
function controles_reportes(){
	($('#id_form_anio #id_anio').numeric());
}

function controles_provincias(){

	($('#id_nombre').alpha({allow:" "}));
	($('#id_abreviatura').alphanumeric({allow:"-"}));

	// para campo name de grupos

	($('#id_name').alpha({allow:" "}));


}

// function verificar_select_padre(id_etiqueta){
// 	if($(id_etiqueta + " option:selected").text()!= '-- Seleccione --'){
// 		$(id_etiqueta).prop('disabled', false);
// 	} else {
// 		$(id_etiqueta).prop('disabled', true);
// 	}
// }








