from django.core.management.base import BaseCommand
from talleres.models import Categoria, Lugar

class Command(BaseCommand):
    help = 'Carga categorías y lugares iniciales según los Anexos'

    def handle(self, *args, **kwargs):
        categorias = [
            (1, 'Aire Libre', 'Actividades que se realizan al exterior, como yoga, caminatas o deporte.'),
            (2, 'Arte', 'Talleres de pintura, dibujo, manualidades, escultura, mosaico, etc.'),
            (3, 'Música', 'Talleres de guitarra, canto, instrumentos, folclore o ensamble.'),
            (4, 'Salud', 'Actividades relacionadas con bienestar físico o mental: meditación, autocuidado, etc.'),
            (5, 'Tecnología', 'Capacitación en herramientas digitales, alfabetización digital, computación básica.'),
            (6, 'Oficios', 'Actividades orientadas al emprendimiento: costura, panadería, carpintería, etc.'),
            (7, 'Educación', 'Apoyo escolar, alfabetización, talleres de idiomas, matemáticas, etc.'),
            (8, 'Medioambiente', 'Huertos urbanos, reciclaje, compostaje, educación ambiental.'),
            (9, 'Comunidad y Liderazgo', 'Formación ciudadana, liderazgo, gestión vecinal, resolución de conflictos.'),
            (10, 'Recreación', 'Juegos, dinámicas grupales, talleres lúdicos para todas las edades.'),
        ]

        lugares = [
            (1, 'Jardín Botánico', 'Av. del Parque 123, Villa Verde'),
            (2, 'Playa El Encanto', 'Costanera Sur s/n, Sector Costero'),
            (3, 'Biblioteca Municipal', 'Calle Los Libros 45, Centro Cívico'),
            (4, 'Centro Cultural Villa Verde', 'Av. Patrimonio 567, Barrio Histórico'),
            (5, 'Gimnasio Municipal', 'Av. Deportes 789, Villa Deportiva'),
            (6, 'Sede Junta Vecinal N°5', 'Pasaje Los Almendros 321, Sector Norte'),
            (7, 'Sede Junta Vecinal N°12', 'Calle La Esperanza 876, Sector Sur'),
            (8, 'Parque Comunal', 'Camino Verde km 2, Acceso Norte'),
            (9, 'Salón Multiuso Municipal', 'Edificio Consistorial, 2° piso'),
            (10, 'Escuela Básica Villa Verde', 'Calle Educación 234, Sector Escolar'),
        ]

        for id, nombre, descripcion in categorias:
            Categoria.objects.update_or_create(id=id, defaults={'nombre': nombre, 'descripcion': descripcion})
        self.stdout.write(self.style.SUCCESS("Categorías cargadas."))

        for id, nombre, direccion in lugares:
            Lugar.objects.update_or_create(id=id, defaults={'nombre': nombre, 'direccion': direccion})
        self.stdout.write(self.style.SUCCESS("Lugares cargados."))
