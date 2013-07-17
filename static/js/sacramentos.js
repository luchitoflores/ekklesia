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


def addFeligres_view(request):
	logger.info('entré a añadir feligrés')
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = FeligresForm(request.POST)
			
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.INFO, 'Se añadió con éxito el feligres')
				return HttpResponseRedirect('/feligres')
			else:
				messages.add_message(request, messages.WARNING, 'Uno o más campos son incorrectos')
		else:
			form = FeligresForm()
			
			
		ctx = {'form': form}
		return render(request, 'feligres/addfeligres.html', ctx)
	else:

		return HttpResponseRedirect('/login')