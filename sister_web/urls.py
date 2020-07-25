from django.urls import path
from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html')

def kelas(request):
    return render(request, 'kelas_index.html')

def kelas_absensi(request):
    return render(request, 'absensi_index.html')

def kelas_absensi_create(request):
    return render(request, 'absensi_change.html')

def kelas_rentangnilai_change(request):
    return render(request, 'rentangnilai_change.html')

def matapelajaran_bobotpenilaian_change(request):
    return render(request, 'rentangnilai_change.html')

urlpatterns = [
    path('', homepage, name='homepage'),
    path('kelas/', kelas, name='kelas'),
    path('kelas/absensi/', kelas_absensi, name='kelas_absensi'),
    path('kelas/absensi/create', kelas_absensi_create, name='kelas_absensi_create'),
    path('kelas/rentangnilai/change', kelas_rentangnilai_change, name='kelas_rentangnilai_change'),
    path('matapelajaran/bobotpenilaian/change', matapelajaran_bobotpenilaian_change, name='matapelajaran_bobotpenilaian_change'),
]