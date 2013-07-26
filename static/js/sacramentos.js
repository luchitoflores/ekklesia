$(document).on('ready', inicio);
document.write('<script src="/static/js/acta.js" type="text/javascript"></script>');
 
function inicio(){
	usuarioCreate();


	modelo_tablas('#id_table_libro, #id_table_feligres,#id_table_matrimonio,#id_table_bautismo,#id_table_eucaristia,#id_table_confirmacion');
	// modelo_tablas('#id_table_libro');

	// modelo_tablas('#id_table_feligres, #id_table_libro,#id_buscar_padre ,#id_table_busqueda_usuarios');
	//modelo_tablas('#id_table_feligres');

	campos_con_fechas();
	tabla_busqueda_usuarios();
	radio_button();
	deshabilitar_campos('#id_form_padre input:text, #id_form_padre select');
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

function tabla_busqueda_usuarios(){
	$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
	{
		return {
			"iStart":         oSettings._iDisplayStart,
			"iEnd":           oSettings.fnDisplayEnd(),
			"iLength":        oSettings._iDisplayLength,
			"iTotal":         oSettings.fnRecordsTotal(),
			"iFilteredTotal": oSettings.fnRecordsDisplay(),
			"iPage":          oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
			"iTotalPages":    oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
		};
	}

	$.extend( $.fn.dataTableExt.oStdClasses, {
		"sSortAsc": "header headerSortDown",
		"sSortDesc": "header headerSortUp",
		"sSortable": "header",
	});

	/* Bootstrap style pagination control */
	$.extend( $.fn.dataTableExt.oPagination, {
		"bootstrap": {
			"fnInit": function( oSettings, nPaging, fnDraw ) {
				var oLang = oSettings.oLanguage.oPaginate;
				var fnClickHandler = function ( e ) {
					e.preventDefault();
					if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
						fnDraw( oSettings );
					}
				};

				$(nPaging).addClass('pagination').append(
					'<ul>'+
					'<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
					'<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
					'</ul>'
					);
				var els = $('a', nPaging);
				$(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
				$(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
			},

			"fnUpdate": function ( oSettings, fnDraw ) {
				var iListLength = 5;
				var oPaging = oSettings.oInstance.fnPagingInfo();
				var an = oSettings.aanFeatures.p;
				var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

				if ( oPaging.iTotalPages < iListLength) {
					iStart = 1;
					iEnd = oPaging.iTotalPages;
				}
				else if ( oPaging.iPage <= iHalf ) {
					iStart = 1;
					iEnd = iListLength;
				} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
					iStart = oPaging.iTotalPages - iListLength + 1;
					iEnd = oPaging.iTotalPages;
				} else {
					iStart = oPaging.iPage - iHalf + 1;
					iEnd = iStart + iListLength - 1;
				}

				for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
                  // Remove the middle elements
                  $('li:gt(0)', an[i]).filter(':not(:last)').remove();

                  // Add the new list items and their event handlers
                  for ( j=iStart ; j<=iEnd ; j++ ) {
                  	sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
                  	$('<li '+sClass+'><a href="#">'+j+'</a></li>')
                  	.insertBefore( $('li:last', an[i])[0] )
                  	.bind('click', function (e) {
                  		e.preventDefault();
                  		oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
                  		fnDraw( oSettings );
                  	} );
                  }

                  // Add / remove disabled classes from the static elements
                  if ( oPaging.iPage === 0 ) {
                  	$('li:first', an[i]).addClass('disabled');
                  } else {
                  	$('li:first', an[i]).removeClass('disabled');
                  }

                  if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
                  	$('li:last', an[i]).addClass('disabled');
                  } else {
                  	$('li:last', an[i]).removeClass('disabled');
                  }
              }
          }
      }
  } );

$('#id_form_busqueda').on('submit', function(e){
	e.preventDefault();
	var url= '/api/usuario/';
	var nombres = $('#id_query_nombres').val();
	var apellidos = $('#id_query_apellidos').val();
	var cedula = $('#id_query_cedula').val();
	console.log(nombres);
	console.log(apellidos);
	console.log(cedula);
	mostrar_html("#id_table_busqueda_usuarios");
	
	var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula};
	$.get(url, ctx, function(data){
		console.log(data);
		// if (data.bandera){
			
			$("#id_table_busqueda_usuarios").dataTable({
				"sDom": "<'top't><'bottom'p><'clear'>",
				"sPaginationType": "bootstrap",
				// "iDisplayStart": 2,
				"iDisplayLength": 2,
				"bPaginate": true,
				"bInfo": true,
				"bSorted": true,
				"bFilter": true,
				"bLengthChange": true,
				"aLengthMenu": [[2, 5, 10, -1], [2, 5, 10, "Todos"]],
				"aaData": data.perfiles,
				"bDestroy": true,
				"aoColumns" : [
				{ "mData" : "nombres", "bSortable": true},
				{ "mData" : "apellidos", "bSortable": true},
				{ "mData" : "dni", "bSortable": true }],
				"oLanguage": {
					"sInfo": "Mostrando _END_ de _TOTAL_  Elementos",
					"sLengthMenu": "Mostrar _MENU_ registros",
					"sSearch": "Filtrar:",
					"sEmptyTable": "No existen datos disponibles en la tabla",
					"sInfoFiltered": " (Filtrado de _MAX_ Elementos)",
					"sZeroRecords": "No existen registros con ese criterio de búsqueda",

					"oPaginate": {
						"sFirst": "",
						"sLast": "",
						"sNext": "Siguiente",
						"sPrevious": "Anterior"}
					}
				}); 
		// } else {
		// 	ocultar_html('#id_table_busqueda_usuarios, #id_table_busqueda_usuarios_wrapper');
		// 	$('#id_div_mensaje_error').attr('style', 'display:auto');
		// 	$('#id_div_mensaje_error img').after('<p>'+data.perfiles+'</p>');
		// 	// $('#id_div_mensaje_error').slideDown(3000).delay(2000).slideToggle(2000, function(){
		// 	// 	$('#id_div_mensaje_error p').remove();
		// 	// });
		// 	// $('#id_div_mensaje_error p').remove();
		// 	// alert('No se encontraron Usuarios con ese criterio');
		// }

		
	});
});
}

