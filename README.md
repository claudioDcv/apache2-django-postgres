### Sistema de administracion para veterinarias

# apache2-django-postgres
Vetadmin System

### Link
- mail: claudio.dcv@gmail.com
- [Trello](https://trello.com/b/YnwxnTuA/vetadmin)
- [Admin](http://45.56.93.71/admin/)

### Recipe Debian 8

- Install `apache2/stable,now 2.4.10-10+deb8u8 amd64`
- Install `libapache2-mod-wsgi-py3/stable,now 4.3.0-1 amd64`

- Install psql (PostgreSQL) 9.6.2
- Install Python 3.4.2
- in location `/var/www/vetadmin`
  - Create virtualenv name `venv`
  - Active virtualenv `source /var /www/vetadmin/venv/bin/activate`
  - install requirements `pip -r requirements.txt`

### Postgress Config

- Create Database
```sql
ALTER USER "postgres" WITH PASSWORD '1234567890';
CREATE DATABASE vetadmin;
```

- Exit databese
```shell
\q
```

### Config in DEV
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vetadmin',
        'USER': 'postgres',
        'PASSWORD': '1234567890',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Migrations

```shell
./manage.py makemigrations

./manage.py migrate

./manage.py runserver
```
--------------------------------

### Create super user
```shell
./manage.py createsuperuser
```


 ### Config Apache 2
 - in `/etc/apache2/sites-available`

 ```apacheconf
 <VirtualHost *:80>

        Alias /static/ /var/www/vetadminweb/vetadminproject/static/

        <Directory /var/www/vetadminweb/vetadminproject/static>
                Require all granted
        </Directory>

        WSGIDaemonProcess vetadminproject python-path=/var/www/vetadminweb/vetadminproject:/var/www/vetadminweb/venv/lib/python3.4/site-packages
        WSGIProcessGroup vetadminproject

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

#### Vistas
- Login
  - Recuperación de contraseña
- Vademecum
  - Listar
  - Crear
  - Actualizar
  - Eliminar
- Pacientes
  - Listar
  - Crear
  - Actualizar
  - Eliminar
- Controles Medicos
  - Listar
  - Crear
  - Actualizar
  - Eliminar
- Clientes
  - Listar
  - Crear
  - Actualizar
  - Eliminar
- Metricas
  - Listar
  - Filtrar
    - Paciente <> Cliente
    - Paciente <> Medico
- Veterinario
  - Listar
  - Crear
  - Actualizar
  - Eliminar















|                                     | REQUISITOS FUNCIONALES                                                                                                                                                                                                                                                                                                  | REQUISITOS NO FUNCIONALES                                                                                                                                                                                                                                                                                                                            |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Login de Usuario                    | el sistema muestra una vista con campos usuario y contraseña, y un boton para ingresar al sistema, ademas mostrara feedback en caso de error                                                                                                                                                                            | Que al ingresar al sistema o al iniciar sesion me demore mas de 5 segundos y que me muestre la clave encriptada.                                                                                                                                                                                                                                     |
| Host Web                            | Servidor activo permamentemente                                                                                                                                                                                                                                                                                         | mantiene sesiones activas, herramienta de analisis de comportamiento de servidor, con alertas en caso de error y auto reinicio en caso de caida del sistema                                                                                                                                                                                          |
| Sistema toma de horas               | mostrar un formulario para agendar horas, mostrar una vista con horarios ordenados de 00 a 23:59                                                                                                                                                                                                                        | validacion de horarios no permiendo tomar horas en dias distintos, validacion que usuario permiendo solo usuarios tipo veterinario realicen esta accion, validar que campo, paciente asignado a hora, no posea una hora ya asignada en el mismo horario                                                                                              |
| Vademecum                           | desplegar un listado de medicamientos con datos atingentes a los mismos, como valor, fecha de caducidad, existencias actuales, mostrar en el header del sistema alertas de medicamentos con problemas, opcion para agregar medicamentos con un formulario donde un usuario puede agregar alertas para cada medicamento. | al ingresar a la seccion de medicamientos, el sistema evaluael tipo de usuario, y de ser un usuario administrador de farmacia, debe activarce la opcion de administracion de esta, sistema valida que datos sean consistentes, no permitiendo fechas fuera de rrango, valores menores a 0.                                                           |
| Generacion de historial medico      | despliegue de boton en vista paciente, que presionando sobre este genere un documento con historial medido de paciente, logo de la empresa, fotografias del proceso dentro de empresa (veterinaria)                                                                                                                     | recoleccion de fotografias grabadas en el servidor estatico y modificar su tamaño para incluirlo dentro de un documento tamaño carta, validacion de perfil de usuario.                                                                                                                                                                               |
| Crud para consultar medicas         | medico ingresa opcion nueva consulta y podra editar un formulario que despliega el sistema donde con distintos controles, tendra la opción de vincular un paciente, agregar fotografias, descriptores de consulta, vinculación de medicamientos existentes en facmacia                                                  | cada vez que se da clic en nueva consulta, sistema genera un registro vacio, para poder editarce a la vez en otro dispositivo, el sistema validar controles anteriores a 1 mes vacios y los elimina, sistema carga la informacion para llenado de consulta segun medico hace clic sobre los controles para mantener el sistema lo mas fluido posible |
| Crear api rest                      | pagina web con un listado de todos los servicios que puede consultar un tercero que decee extender el sistema                                                                                                                                                                                                           | validacion de perfil de usuario, entregando solo ciertas acciones dependiendo del mismo                                                                                                                                                                                                                                                              |
| estadisticas de atencion            | una seccion con campos de busqueda y filtro por determinados criterios que muestra graficos y tablas dependiend de los criterios ingresados, para ver el estado del sistema                                                                                                                                             | generacion de graficos a partir de consultas sql que librerias javascript transforman en objecos visibles en la interfaz                                                                                                                                                                                                                             |
| app para gestionar los pagos        | formulario para agregar pagos / editarlo / eliminarlos, con campos cliente, paciente atendido, medico que realiza atencion, costo total, horario de realizacion, para cliente nuevos el sistema permite el ingreso de nuevos cliente en el mismo formulario, ademas de realizar el ingreso de nuevos pacientes.         | cada ver que se presiona un determinado control, el sistema se encarga de cargar la data solicitada, validando datos como, existe el cliente o de otro modo retornando false                                                                                                                                                                         |
| sistema de fidelizacion de clientes | boton para agregar fechas importantes de clientes, formualrio creacion de promociones, boton para enviar email a clientes con saludos de: cumpleaños, santo, u otros dias atingentes a un cliente previamente ingresado en el sistema, boton que abre formulario para enviar a clientes promociones.                    | sistema valida perfil de usuario que debe ser admin, para crear promociones u otra accion. validacion de fecha actual para retornar clientes con fecha importante cercana a 10 dias de la fecha actual. y un flag para clientes con fecha importante en el mimo dia                                                                                  |
| dashboard para clientes             | vista con opcion para ver sus mascotas, y estados de pagos realizados.                                                                                                                                                                                                                                                  | el sistema valida usuario tipo cliente, y solo retorna informacion de sus mascotas, no incluyendo datos personales de los medicos ademas de: nombre, apellido, especialidad                                                                                                                                                                          |
|                                     |                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                                                                                      |
|                                     |                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                                                                                      |
|                                     |                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                                                                                      |
