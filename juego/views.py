
# Create your views here.
from django.shortcuts import render, redirect
from .models import Pregunta, Respuesta, Partida, Categoria
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def listar_preguntas(request):
    if request.method == "POST":
        resultado = 0
        for i in range(1,3):
            opcion = Respuesta.objects.get(pk=request.POST[str(i)])
            resultado += opcion.puntaje
        Partida.objects.create(usuario=request.user, fecha=datetime.now, resultado=resultado)
        return redirect("/")
    else:
        data = {}
        preguntas = Pregunta.objects.all().order_by('?')[:2]
        for item in preguntas:
            respuestas = Respuesta.objects.filter(id_pregunta=item.id)
            categoria = Categoria.objects.get(pk=item.id_categoria.id)
            #{pregunta: {opciones: [opcion1, opcion2, opcion3], categoria: categoria}
            data[item.pregunta]= {'opciones': respuestas, 'categoria': categoria}
        return render(request, 'juego/listar_preguntas.html', {"preguntas":preguntas,"data":data})



from .forms import PreguntaForm
def crear_pregunta(request):
    form = PreguntaForm()
    return render(request, 'juego/crear_pregunta.html', {'form': form})
