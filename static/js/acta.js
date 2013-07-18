$(document).on('ready', modelo_tablas(valor));
	/* API method to get paging information */

function modelo_tablas(valor){
	$('th').each(function(){ 
	if($(this).text() != ''){
		$(this).append('  <img src="/static/img/black-unsorted.gif"></img>');
	}
});
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



$(valor).dataTable({
	// '<"top"lfit><"bottom"p><"clear">'
	// "<'row'<'span5'l><'span5'f>r>t<'row'<'span8'i><'span8'p>>

	// "sDom": "<'top' <'row' <'span5' l><'span5 form-search search-query' f>>>t<'bottom' p>",
	"iDisplayStart": 5,
	"aLengthMenu": [[5, 10, 25, 50, 100, -1], [5, 10, 25, 50, 100, 'Todos']],
	"sPaginationType": "bootstrap",
	"iDisplayLength": 5,
	'bsort': true,
	"oLanguage": {
		"sInfo": "Mostrando _END_ de _TOTAL_  Elementos",
		"sLengthMenu": "Mostrar _MENU_ registros",
		"sSearch": "Buscar:",
		"sEmptyTable": "No existen datos disponibles en la tabla",
		"sInfoFiltered": " (Filtrado de _MAX_ Elementos)",
		"sZeroRecords": "No existen registros con ese criterio de búsqueda",

		"oPaginate": {
			"sFirst": "",
			"sLast": "",
			"sNext": "Siguiente",
			"sPrevious": "Anterior",


		}

	}
	
	
    
});
console.log('ejecutando datatables');



}
	
