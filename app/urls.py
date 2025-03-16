from django.urls import path
from app.views import *
from app.views.administrador.views import *
from app.views.operador.views import *
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
]
