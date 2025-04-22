from django.urls import path
from app.views import *
from app.views.administrador.views import *
from app.views.operador.views import *
from app.views.terminal.views import *
from app.views.area.views import *
from app.views.marca.views import *
from app.views.agente.views import *
from app.views.activo.views import *
from app.views.movimiento.views import *
from backups.views import BackupDatabaseView, RestoreDatabaseView, DeleteBackupView, BackupListView

app_name = 'app'
urlpatterns = [
    ### CRUD ADMINISTRADOR ###
    path('administrador/listar/', AdministradorListView.as_view(), name='administrador_lista'),
    path('administrador/crear/', AdministradorCreateView.as_view(), name='administrador_crear'),
    path('administrador/editar/<int:pk>/', AdministradorUpdateView.as_view(), name='administrador_editar'),
    path('administrador/eliminar/<int:pk>/', AdministradorDeleteView.as_view(), name='administrador_eliminar'),

    ### CRUD OPERADOR ###
    path('operador/listar/', OperadorListView.as_view(), name='operador_lista'),
    path('operador/crear/', OperadorCreateView.as_view(), name='operador_crear'),
    path('operador/editar/<int:pk>/', OperadorUpdateView.as_view(), name='operador_editar'),
    path('operador/eliminar/<int:pk>/', OperadorDeleteView.as_view(), name='operador_eliminar'),

    ### COPIA DE SEGURIDAD DE BASE DE DATOS ###
    path('gestionar_backups/', BackupDatabaseView.as_view(), name='gestionar_backups'),
    path('restaurar_backup/', RestoreDatabaseView.as_view(), name='restaurar_backup'),
    path('eliminar-backup/', DeleteBackupView.as_view(), name='eliminar_backup'),
    path('backup_list/', BackupListView.as_view(), name='backup_list'),

    ### CRUD TERMINAL ###
    path('terminal/listar/', TerminalListView.as_view(), name='terminal_lista'),
    path('terminal /crear/', TerminalCreateView.as_view(), name='terminal_crear'),
    path('terminal/editar/<int:pk>/', TerminalUpdateView.as_view(), name='terminal_editar'),
    path('terminal/eliminar/<int:pk>/', TerminalDeleteView.as_view(), name='terminal_eliminar'),

    ### CRUD AREA ###
    path('area/listar/', AreaListView.as_view(), name='area_lista'),
    path('area /crear/', AreaCreateView.as_view(), name='area_crear'),
    path('area/editar/<int:pk>/',AreaUpdateView.as_view(), name='area_editar'),
    path('area/eliminar/<int:pk>/', AreaDeleteView.as_view(), name='area_eliminar'),

    ### CRUD MARCA ###
    path('marca/listar/', MarcaListView.as_view(), name='marca_lista'),
    path('marca/crear/', MarcaCreateView.as_view(), name='marca_crear'),
    path('marca/editar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_editar'),
    path('marca/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_eliminar'),

    ### CRUD AGENTE ###
    path('agente/listar/', AgenteListView.as_view(), name='agente_lista'),
    path('agente/crear/', AgenteCreateView.as_view(), name='agente_crear'),
    path('agente/editar/<int:pk>/', AgenteUpdateView.as_view(), name='agente_editar'),
    path('agente/eliminar/<int:pk>/', AgenteDeleteView.as_view(), name='agente_eliminar'),

    ### CRUD ACTIVO ###
    path('activo/listar/', ActivoListView.as_view(), name='activo_lista'),
    path('activo/crear/', ActivoCreateView.as_view(), name='activo_crear'),
    path('activo/editar/<int:pk>/', ActivoUpdateView.as_view(), name='activo_editar'),
    path('activo/eliminar/<int:pk>/', ActivoDeleteView.as_view(), name='activo_eliminar'),

    ### CRUD MOVIMIENTO ###
    path('movimiento/listar/', MovimientoListView.as_view(), name='movimiento_lista'),
    path('movimiento/crear/', MovimientoCreateView.as_view(), name='movimiento_crear'),
    path('movimiento/editar/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_editar'),
    path('movimiento/eliminar/<int:pk>/', MovimientoDeleteView.as_view(), name='movimiento_eliminar'),

    ### API'S ###
    path('movimiento/terminal_api/', TerminalAPI.as_view(), name='terminal_api'),
    path('movimiento/activo_api/', ActivoAPI.as_view(), name='activo_api'),
]
