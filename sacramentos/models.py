# -*- coding:utf-8 -*-
import re
from datetime import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.conf import settings


from ciudades.models import Direccion 
from sacramentos.managers import LibroManager, PersonaManager,BautismoManager
# Create your models here.

def user_new_unicode(self):
    return self.username if self.get_full_name() == '' else self.get_full_name()

# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode 


class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Libro(TimeStampedModel):
	TIPO_LIBRO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio')
                     
    	)

	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	numero_libro=models.PositiveIntegerField()
	tipo_libro=models.CharField(max_length=200, choices=TIPO_LIBRO_CHOICES)
	fecha_apertura=models.DateField(help_text='Ingrese una fecha Ej:22/07/2010')
	fecha_cierre=models.DateField(null=True,blank=True,help_text='Ingrese una fecha Ej:22/07/2010')
	estado=models.CharField(max_length=20,choices=ESTADO_CHOICES)
	numero_maximo_actas=models.PositiveIntegerField()
	parroquia = models.ForeignKey('Parroquia', related_name='parroquia', help_text='Seleccione una parroquia')


	def __unicode__(self):
		return '%d %s' %(self.numero_libro,self.tipo_libro)

class PerfilUsuario(TimeStampedModel):
	# p.f00_size
	# p.get_foo_size_display()
    SEXO_CHOICES = (
		('m', 'Masculino'), 
		('f','Femenino')
        )
        
    ESTADO_CIVIL_CHOICES = (
        ('s','Soltero/a'),
        ('c','Casado/a'),
        ('d','Divorciado/a'),
        ('v','Viudo/a')
        )

    NACIONALIDAD_CHOICES = (
                    ('EC', 'Ecuador'),
                    ('AF', 'Afganistán'), 
                    ('AL', 'Albania'), 
                    ('DE', 'Alemania'), 
                    ('AD', 'Andorra'), 
                    ('AO', 'Angola'),
                    ('AI', 'Anguilla'),
                    ('AQ', 'Antártida'),
                    ('AG', 'Antigua y Barbuda'),
                    ('AN', 'Antillas Holandesas'),
                    ('SA', 'Arabia Saudí'),
                    ('DZ', 'Argelia'),
                    ('AR', 'Argentina'),
                    ('AM', 'Armenia'),
                    ('AW', 'Aruba'),
                    ('AU', 'Australia'),
                    ('AT', 'Austria'), 
                    ('AZ', 'Azerbaiyán'), 
                    ('BS', 'Bahamas'), 
                    ('BH', 'Bahrein'), 
                    ('BD', 'Bangladesh'), 
                    ('BB', 'Barbados'), 
                    ('BE', 'Bélgica'), 
                    ('BZ', 'Belice'), 
                    ('BJ', 'Benin'), 
                    ('BM', 'Bermudas'), 
                    ('BY', 'Bielorrusia'), 
                    ('MM', 'Birmania'), 
                    ('BO', 'Bolivia'), 
                    ('BA', 'Bosnia y Herzegovina'), 
                    ('BW', 'Botswana'), 
                    ('BR', 'Brasil'), 
                    ('BN', 'Brunei'), 
                    ('BG', 'Bulgaria'), 
                    ('BF', 'Burkina Faso'), 
                    ('BI', 'Burundi'), 
                    ('BT', 'Bután'), 
                    ('CV', 'Cabo Verde'), 
                    ('KH', 'Camboya'), 
                    ('CM', 'Camerún'), 
                    ('CA', 'Canadá'), 
                    ('TD', 'Chad'), 
                    ('CL', 'Chile'), 
                    ('CN', 'China'), 
                    ('CY', 'Chipre'), 
                    ('VA', 'Ciudad del Vaticano (Santa Sede)'), 
                    ('CO', 'Colombia'), 
                    ('KM', 'Comores'), 
                    ('CG', 'Congo'), 
                    ('CD', 'Congo, República Democrática del'), 
                    ('KR', 'Corea'), 
                    ('KP', 'Corea del Norte'), 
                    ('CI', 'Costa de Marfíl'), 
                    ('CR', 'Costa Rica'), 
                    ('HR', 'Croacia (Hrvatska)'), 
                    ('CU', 'Cuba'), 
                    ('DK', 'Dinamarca'), 
                    ('DJ', 'Djibouti'),
                    ('DM', 'Dominica'),
                    ('EG', 'Egipto'),
                    ('SV', 'El Salvador'), 
                    ('AE', 'Emiratos Árabes Unidos'),
                    ('ER', 'Eritrea'),
                    ('SI', 'Eslovenia'),
                    ('ES', 'España'),
                    ('GM', 'Gambia'),
                    ('GE', 'Georgia'),
                    ('GH', 'Ghana'),
                    ('GI', 'Gibraltar'),
                    ('GD', 'Granada'),
                    ('GR', 'Grecia'), 
                    ('GL', 'Groenlandia'), 
                    ('GP', 'Guadalupe'), 
                    ('GU', 'Guam'), 
                    ('GT', 'Guatemala'),
                    ('GY', 'Guayana'),
                    ('GF', 'Guayana Francesa'),
                    ('GN', 'Guinea'),
                    ('GQ', 'Guinea Ecuatorial'),
                    ('GW', 'Guinea-Bissau'),
                    ('HT', 'Haití'), 
                    ('HN', 'Honduras'), 
                    ('HU', 'Hungría'), 
                    ('IN', 'India'), 
                    ('ID', 'Indonesia'), 
                    ('IQ', 'Irak'), 
                    ('IR', 'Irán'), 
                    ('IE', 'Irlanda'), 
                    ('BV', 'Isla Bouvet'), 
                    ('CX', 'Isla de Christmas'), 
                    ('IS', 'Islandia'), 
                    ('KY', 'Islas Caimán'), 
                    ('CK', 'Islas Cook'), 
                    ('CC', 'Islas de Cocos o Keeling'), 
                    ('FO', 'Islas Faroe'), 
                    ('HM', 'Islas Heard y McDonald'), 
                    ('FK', 'Islas Malvinas'), 
                    ('MP', 'Islas Marianas del Norte'), 
                    ('MH', 'Islas Marshall'), 
                    ('UM', 'Islas menores de Estados Unidos'), 
                    ('PW', 'Islas Palau'), 
                    ('SB', 'Islas Salomón'), 
                    ('SJ', 'Islas Svalbard y Jan Mayen'), 
                    ('TK', 'Islas Tokelau'), 
                    ('TC', 'Islas Turks y Caicos'), 
                    ('VI', 'Islas Vírgenes (EE.UU.)'), 
                    ('VG', 'Islas Vírgenes (Reino Unido)'), 
                    ('WF', 'Islas Wallis y Futuna'), 
                    ('IL', 'Israel'), 
                    ('IT', 'Italia'), 
                    ('JM', 'Jamaica'), 
                    ('JP', 'Japón'), 
                    ('JO', 'Jordania'), 
                    ('KZ', 'Kazajistán'), 
                    ('KE', 'Kenia'), 
                    ('KG', 'Kirguizistán'), 
                    ('KI', 'Kiribati'), 
                    ('KW', 'Kuwait'), 
                    ('LA', 'Laos'), 
                    ('LS', 'Lesotho'), 
                    ('LV', 'Letonia'), 
                    ('LB', 'Líbano'), 
                    ('LR', 'Liberia'), 
                    ('LY', 'Libia'), 
                    ('LI', 'Liechtenstein'), 
                    ('LT', 'Lituania'), 
                    ('LU', 'Luxemburgo'), 
                    ('MK', 'Macedonia'), 
                    ('MG', 'Madagascar'), 
                    ('MY', 'Malasia'), 
                    ('MW', 'Malawi'), 
                    ('MV', 'Maldivas'), 
                    ('ML', 'Malí'), 
                    ('MT', 'Malta'), 
                    ('MA', 'Marruecos'), 
                    ('MQ', 'Martinica'), 
                    ('MU', 'Mauricio'), 
                    ('MR', 'Mauritania'), 
                    ('YT', 'Mayotte'), 
                    ('MX', 'México'), 
                    ('FM', 'Micronesia'), 
                    ('MD', 'Moldavia'), 
                    ('MC', 'Mónaco'), 
                    ('MN', 'Mongolia'), 
                    ('MS', 'Montserrat'), 
                    ('MZ', 'Mozambique'), 
                    ('NA', 'Namibia'), 
                    ('NR', 'Nauru'), 
                    ('NP', 'Nepal'), 
                    ('NI', 'Nicaragua'), 
                    ('NE', 'Níger'), 
                    ('NG', 'Nigeria'), 
                    ('NU', 'Niue'), 
                    ('NF', 'Norfolk'), 
                    ('NO', 'Noruega'), 
                    ('NC', 'Nueva Caledonia'), 
                    ('NZ', 'Nueva Zelanda'), 
                    ('OM', 'Omán'), 
                    ('NL', 'Países Bajos'), 
                    ('PA', 'Panamá'), 
                    ('PG', 'Papúa Nueva Guinea'), 
                    ('PK', 'Paquistán'), 
                    ('PY', 'Paraguay'), 
                    ('PE', 'Perú'), 
                    ('PN', 'Pitcairn'), 
                    ('PF', 'Polinesia Francesa'), 
                    ('PL', 'Polonia'), 
                    ('PT', 'Portugal'), 
                    ('PR', 'Puerto Rico'), 
                    ('QA', 'Qatar'), 
                    ('UK', 'Reino Unido'), 
                    ('CF', 'República Centroafricana'), 
                    ('CZ', 'República Checa'), 
                    ('ZA', 'República de Sudáfrica'), 
                    ('DO', 'República Dominicana'), 
                    ('SK', 'República Eslovaca'), 
                    ('RE', 'Reunión'), 
                    ('RW', 'Ruanda'), 
                    ('RO', 'Rumania'), 
                    ('RU', 'Rusia'), 
                    ('EH', 'Sahara Occidental'), 
                    ('KN', 'Saint Kitts y Nevis'), 
                    ('WS', 'Samoa'), 
                    ('AS', 'Samoa Americana'), 
                    ('SM', 'San Marino'), 
                    ('VC', 'San Vicente y Granadinas'), 
                    ('SH', 'Santa Helena'), 
                    ('LC', 'Santa Lucía'), 
                    ('ST', 'Santo Tomé y Príncipe'), 
                    ('SN', 'Senegal'), 
                    ('SC', 'Seychelles'), 
                    ('SL', 'Sierra Leona'), 
                    ('SG', 'Singapur'), 
                    ('SY', 'Siria'), 
                    ('SO', 'Somalia'), 
                    ('LK', 'Sri Lanka'), 
                    ('PM', 'St. Pierre y Miquelon'), 
                    ('SZ', 'Suazilandia'), 
                    ('SD', 'Sudán'), 
                    ('SE', 'Suecia'), 
                    ('CH', 'Suiza'), 
                    ('SR', 'Surinam'), 
                    ('TH', 'Tailandia'), 
                    ('TW', 'Taiwán'), 
                    ('TZ', 'Tanzania'), 
                    ('TJ', 'Tayikistán'), 
                    ('TF', 'Territorios franceses del Sur'), 
                    ('TP', 'Timor Oriental'), 
                    ('TG', 'Togo'), 
                    ('TO', 'Tonga'), 
                    ('TT', 'Trinidad y Tobago'), 
                    ('TN', 'Túnez'), 
                    ('TM', 'Turkmenistán'), 
                    ('TR', 'Turquía'), 
                    ('TV', 'Tuvalu'), 
                    ('UA', 'Ucrania'), 
                    ('UG', 'Uganda'), 
                    ('UY', 'Uruguay'), 
                    ('UZ', 'Uzbekistán'), 
                    ('VU', 'Vanuatu'), 
                    ('VE', 'Venezuela'), 
                    ('VN', 'Vietnam'), 
                    ('YE', 'Yemen'), 
                    ('YU', 'Yugoslavia'), 
                    ('ZM', 'Zambia'), 
                    ('ZW', 'Zimbabue')
                    )


    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Usuario', null=True, blank=True)
    dni = models.CharField('Cédula/Pasaporte', max_length=20, null=True, blank=True, help_text='Ingrese un numero de cedula ej:1104688617')
    nacionalidad = models.CharField(max_length=2, help_text='Escoja la nacionalidad. Ej: Ecuador', choices=NACIONALIDAD_CHOICES)
    padre = models.ForeignKey('PerfilUsuario', related_name='Padre', null=True, blank=True, limit_choices_to={'sexo':'m'}, help_text='Presione buscar, si no está en la lista, presione crear')
    madre = models.ForeignKey('PerfilUsuario', related_name='Madre', null=True, blank=True, limit_choices_to={'sexo':'f'}, help_text='Presione buscar, si no está en la lista, presione crear')
    fecha_nacimiento = models.DateField(null=True, blank=True, 
        help_text='Ingrese la fecha de nacimiento Ej: dd/mm/yyyy')
    lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True, help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza')
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES,
		help_text='Elija el sexo de la persona. Ej: Masculino')
    estado_civil = models.CharField(max_length=10, choices=ESTADO_CIVIL_CHOICES, null=True, blank=True, help_text='Elija el estado civil. Ej: Soltero/a')
    profesion = models.CharField(max_length=50, null=True, blank=True, help_text='Ingrese la profesión de la persona')
    celular=models.CharField(max_length=10, blank=True, null=True, help_text='Ingrese su número celular. Ej: 0986522754')
    parroquias = models.ManyToManyField('Parroquia', null=True, blank=True, through='AsignacionParroquia') 

    objects = PersonaManager()


    def __unicode__(self):
        if self.user.first_name == None and self.user.last_name == None:
            return self.user.username 
	else:
            return '%s.- %s %s' %(self.id, self.user.first_name, self.user.last_name) 

    def get_absolute_url_sacerdote(self):
	return u'/sacerdote/%i' % self.id
    

    def crear_username(self, nombres, apellidos):
        import unicodedata
        nombres = ''.join((c for c in unicodedata.normalize('NFD', unicode(nombres)) if unicodedata.category(c) != 'Mn'))
        apellidos = ''.join((c for c in unicodedata.normalize('NFD', unicode(apellidos)) if unicodedata.category(c) != 'Mn'))
        nombres = nombres.lower().split()
        apellidos = apellidos.lower().split()
        # s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
        username = u'%s%s'% (nombres[0][0],apellidos[0])
            # username = u'%s%s'% (nombres,apellidos)
    	print username
    	user_name = PerfilUsuario.objects.username_disponible(username)

    	if user_name == True:
    		return username
    	else:
    		personas = PerfilUsuario.objects.filter(user__username__startswith=username).latest('user__date_joined')
                ultimo_username = personas.user.username
                digitos = ''
                for d in ultimo_username:
                    if re.match('[0-9]+', d):
                        digitos += d
                if digitos == '':
                    username = username + str(1)
                else:
                    digitos = int(digitos) + 1
                    username = username + str(digitos)
                return username

class Sacramento(TimeStampedModel):
    TIPO_SACRAMENTO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio')           
    	)
    numero_acta = models.PositiveIntegerField(help_text='Ingrese el numero de acta ej:3,78')
    pagina = models.PositiveIntegerField(help_text='Numero de pagina ej:1,3')
    tipo_sacramento = models.CharField(max_length=50, 
    	choices=TIPO_SACRAMENTO_CHOICES,help_text='Elija un tipo de sacramento')
    fecha_sacramento = models.DateField(help_text='Elija una fecha ej:dd/mm/yyyy')
    celebrante = models.ForeignKey(PerfilUsuario, related_name='Sacerdote',
        help_text='Nombre del Celebrante ej: Ob Julio Parrilla')
    lugar_sacramento = models.CharField(max_length=50,
    	help_text='Ingrese el lugar ej: Loja,San Pedro')
    padrino = models.CharField(max_length= 200,null=True,blank=True,
    	help_text='Ingrese el nombre de padrino ej:Jose Rivera')
    madrina = models.CharField(max_length= 200,null=True,blank=True,
    	help_text='Ingrese el nombre de madrina ej:Luisa Mera')
    iglesia = models.CharField(max_length=50,help_text='Nombre de iglesia ej:Catedral')
    libro=models.ForeignKey(Libro, related_name='Libro',
    	help_text='Seleccione un libro')
    parroquia = models.ForeignKey('Parroquia', related_name='Parroquia')

    
class Bautismo(Sacramento):
	bautizado=models.OneToOneField(PerfilUsuario, related_name='Bautizado',
		help_text='Seleccione un feligres')
	abuelo_paterno = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuelo paterno ej:Jose Rivera')
	abuela_paterna = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuela paterna ej:Maria Gonzalez')
	abuelo_materno = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuelo materno ej:Jose Gonzalez')
	abuela_materna = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuela materna ej: Gloria Correa')
	vecinos_paternos = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de vecinos paternos ej:Jose Rivera')
	vecinos_maternos = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de vecinos maternos ej:Ana Vargas')
	objects=BautismoManager()



	def __unicode__(self):
		return '%s %s' %(self.bautizado.user.first_name,self.bautizado.user.last_name)

	


class Eucaristia(Sacramento):
	feligres=models.OneToOneField(PerfilUsuario, related_name='feligres',
		help_text='Seleccione un feligres')
	
	def __unicode__(self):
		return '%s %s' %(self.feligres.user.first_name,self.feligres.user.last_name)

	

class Confirmacion(Sacramento):
	confirmado=models.OneToOneField(PerfilUsuario, related_name='Confirmado',null=True,
		blank=True,help_text='Seleccione un feligres')
	

	def __unicode__(self):
		return '%s %s' %(self.confirmado.user.first_name,self.confirmado.user.last_name)


class Matrimonio(Sacramento):

    TIPO_MATRIMONIO_CHOICES=(
        ('Catolico','Catolico'),
        ('Mixto','Mixto'),
        )
    novio=models.ForeignKey(PerfilUsuario, related_name='Novio',
		help_text='Seleccione un novio')
    novia=models.ForeignKey(PerfilUsuario, related_name='Novia',
		help_text='Seleccione una novia')
    testigo_novio = models.CharField(max_length=200,
		help_text='Nombre de testigo ej: Pablo Robles')
    testigo_novia = models.CharField(max_length=200,help_text='Nombre de testiga ej:Fernanda Pincay')
    vigente=models.BooleanField()
    tipo_matrimonio=models.CharField(max_length=100,choices=TIPO_MATRIMONIO_CHOICES)
    def __unicode__(self):
        return str(self.pagina)

    

class NotaMarginal(TimeStampedModel):
	fecha = models.DateField()
	descripcion = models.TextField(max_length=300,
		help_text='Descripcion ej:Saco para casarse') 
	bautismo= models.ForeignKey('Bautismo',related_name='Bautismo',null=True,blank=True)
	matrimonio=models.ForeignKey('Matrimonio',related_name='Matrimonio',null=True,
		blank=True)
	def __unicode__(self):
		return self.descripcion



class AsignacionParroquia(TimeStampedModel):
	persona = models.ForeignKey('PerfilUsuario')
	parroquia = models.ForeignKey('Parroquia')
	# periodo = models.ForeignKey('PeriodoAsignacionParroquia')
	
	def __unicode__(self):
		return u'Párroco: %s - Parroquia: %s' % (self.persona.user.get_full_name(), self.parroquia.nombre) 

        def get_absolute_url(self):
		return '/asignar/parroquia/parroco/%i' % self.id

    	# class Meta:
     #    	db_table = u'sacramentos_perfilusuario_parroquias'

class PeriodoAsignacionParroquia(TimeStampedModel):
    inicio = models.DateField(null=True, blank=True)
    fin = models.DateField(null=True, blank=True) 
    presente = models.BooleanField('Al presente', help_text='Marque la casilla para indicar que el periodo de asignación está vigente')  
    estado = models.BooleanField('Activo?', help_text='Marque la casilla activo para indicar que es el párroco actual')
    asignacion = models.ForeignKey('AsignacionParroquia')

    def __unicode__(self):
        return u'%s - %s : %s' % (self.asignacion.persona, self.asignacion.parroquia, self.estado)
        
class Intenciones(TimeStampedModel):
	intencion = models.CharField(max_length=200, 
		help_text='Ingrese la intención. Ej: Aniversario de fallecimiento')
	fecha = models.DateField(help_text=
        'Ingrese la fecha de la intención Ej: dd/mm/yyyy')
	hora = models.TimeField(help_text=
        'Ingrese la hora de celebración de la intención Ej: 17:00')
	oferente = models.CharField(max_length=200, 
        help_text='Ingrese quien ofrece la intención. Ej: La Flia Flores')
	ofrenda = models.PositiveIntegerField(
        help_text='Ingrese el valor de la ofrenda por la intención. Ej: 5')
	parroquia = models.ForeignKey('Parroquia')
	individual = models.BooleanField('Es única?', 
        help_text='Marque para indicar que la intención será la única en la misa')


	def __unicode__(self):
		return self.intencion

	def get_absolute_url(self):
		return u'/intencion/%i' % self.id


class Parroquia(TimeStampedModel):
	nombre=models.CharField('Nombre de Parroquia',max_length=100)
	direccion=models.ForeignKey(Direccion, related_name='direccion', verbose_name=u'Prueba')

	def __unicode__(self):
		return u'%s.- %s' % (self.id, self.nombre)

	def get_absolute_url(self):
		return '/parroquia/%s' %(self.id)

	class Meta:
		permissions = (
			('create', 'Puede crear parroquias'),
			('can_change', 'Puede actualizar parroquias'),
			('delete', 'Puede eliminar parroquias'),
			)


