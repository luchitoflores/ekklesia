function principal() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == "POST") {
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});
}


function cargarDatosConPost() {

	$(function() {
		$('#id_form').on('submit', function(e) {

			e.preventDefault();

			url = '/loginajax/';
			console.log('soy la url: ', url);
			archivojson = $('#id_form').serialize();
			console.log('soy el archivo json: ' + archivojson);

			var spinner = $('#id_carga').data('spinner', new Spinner({
				radius: 5,
				width: 2,
				height: 2,
				lenght: 4
			}).spin(this));

			$.post(url, archivojson, function(response, estado, jqXHR) {
				console.log('respuesta del servidor: ' + response);
				console.log('estado del servidor: ' + estado);
				console.log('jqXHR del servidor: ' + jqXHR);
				spinner.stop().hide();

			});

		});

	});

}


function cargarDatosConAjax() {
	$(function() {
		$('#id_form').on('submit', function(e) {

			e.preventDefault();
			$.ajax({
				beforeSend: function() {
					var opts = {
						lines: 13, // The number of lines to draw
						length: 4, // The length of each line
						width: 2, // The line thickness
						radius: 3, // The radius of the inner circle
						corners: 1, // Corner roundness (0..1)
						rotate: 0, // The rotation offset
						direction: 1, // 1: clockwise, -1: counterclockwise
						color: '#000', // #rgb or #rrggbb
						speed: 1, // Rounds per second
						trail: 60, // Afterglow percentage
						shadow: false, // Whether to render a shadow
						hwaccel: false, // Whether to use hardware acceleration
						className: 'spinner', // The CSS class to assign to the spinner
						zIndex: 2e9, // The z-index (defaults to 2000000000)
						top: 'auto', // Top position relative to parent in px
						left: 'relative',

					};
					var target = document.getElementById('id_carga');
					var spinner = new Spinner(opts).spin(target);
				},

				url: $('#id_form').attr('action'),
				type: $('#id_form').attr('method'),
				data: $('#id_form').serialize(),
				success: function(response) {
					console.log(response);
					$('#id_carga').html('<p>Todo está correcto</p>')

				},
				error: function(jqXHR, estado, error) {
					console.log(jqXHR);
					console.log(estado);
					console.log(error);
				},
				complete: function(jqXHR, estado) {
					console.log(jqXHR);
					console.log(estado);
				},
				timeout: 15000,
			});

});
});

}


function cargarDatosConGet() {

	$(function() {

		$('#prueba').click(function() {
			$.get('/feligres/ajax', function(data) {
				console.log(data);

			});
		});

	});
}