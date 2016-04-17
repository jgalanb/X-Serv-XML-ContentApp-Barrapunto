from django.shortcuts import render
from django.http import HttpResponse
from models import Pages
from django.views.decorators.csrf import csrf_exempt
from parser_barrapunto import obtener_titulares

# Create your views here.

def actualizar_titulares(request):
    titulares_Barrapunto = obtener_titulares()
    return HttpResponse("<h3>Los titulares han sido actualizados en " +\
                        "estos momentos!</h3>" + titulares_Barrapunto)

@csrf_exempt
def id_to_page(request, identificador):
    metodo = request.method
    if metodo == "GET":
        try:
            elementos = Pages.objects.get(id=int(identificador))
            http_Resp = elementos.page
        except Pages.DoesNotExist:
            http_Error = "<h3><font color='red'>Error! El indice introducido no " +\
                        "corresponde con ningun elemento de la tabla!</font></h3>"
    elif metodo == "PUT":
        http_Error = "<h3><font color='red'>Error! Cuando se introduce un " +\
                    "identificador, el unico metodo valido es GET.</font></h3>"
    else:
        http_Error = "<h3><font color='red'>Error! Metodo no valido</font></h3>"
    try:
        html_Barrapunto = obtener_titulares()
        return HttpResponse(http_Resp + html_Barrapunto)
    except UnboundLocalError:
        return HttpResponse(http_Error)

@csrf_exempt
def name_to_page(request, recurso):
    metodo = request.method
    if metodo == "GET":
        try:
            elementos = Pages.objects.get(name=recurso)
            http_Resp = elementos.page
        except Pages.DoesNotExist:
            http_Error = "<h3><font color='red'>Error! El recurso introducido no " +\
                        "corresponde con ningun elemento de la tabla!</font></h3>"
    elif metodo == "PUT":
        try:
            elementos = Pages.objects.get(name=recurso)
            http_Error = "Cuidado! Este recurso ya esta en la base de datos!"
        except Pages.DoesNotExist:
            cuerpo = request.body
            new_page = Pages(name=recurso, page=cuerpo)
            new_page.save()
            http_Resp = "<p>Se ha introducido el recurso " + recurso +\
                        " en la base de datos.</p>" +\
                        "<p>Accede a la lista de a traves de /pages</p>"
    else:
        http_Error = "<h3><font color='red'>Error! Metodo no valido</font></h3>"

    try:
        html_Barrapunto = obtener_titulares()
        return HttpResponse(http_Resp + html_Barrapunto)
    except UnboundLocalError:
        return HttpResponse(http_Error)

def obtener_lista_pages(request):
    http_inicial = "<h3>Lista de Pages actualmente en la base de datos:</h3>"
    try:
        elementos = Pages.objects.all()
        http_Resp = '<ol>'
        for elemento in elementos:
            http_Resp += '<li><a href="/' + str(elemento.id) + '">' + \
                        str(elemento.name) + '</a>'
        http_Resp += '</ol>'
    except Pages.DoesNotExist:
        http_Error = "<h3><font color='red'>Error! No existe el modelo " +\
                    "Pages!</font></h3>"
                    
    try:
        html_Barrapunto = obtener_titulares()
        return HttpResponse(http_inicial + http_Resp + html_Barrapunto)
    except UnboundLocalError:
        return HttpResponse(http_Error)
