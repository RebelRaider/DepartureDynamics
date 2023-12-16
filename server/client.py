from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

client = APIRouter()
templates = Jinja2Templates(directory="templates")

@client.get('/ping')
async def pong(request: Request):
    """
    Обработчик запроса для эндпоинта '/ping'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: Ответ с рендеренным HTML-шаблоном 'pong.html'.
    """
    return templates.TemplateResponse('pong.html', {'request': request})


@client.get('/docs/app')
@client.get('/docs/app.html')
async def app(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/app'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'app.html'.
    """
    return HTMLResponse(open('templates/docs/app.html').read())



@client.get('/docs/db')
@client.get('/docs/db.html')
async def db(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/db'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'db.html'.
    """
    return HTMLResponse(open('templates/docs/db.html').read())


@client.get('/docs/client')
@client.get('/docs/client.html')
async def clients(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/client'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'client.html'.
    """
    return HTMLResponse(open('templates/docs/client.html').read())


@client.get('/docs/api/controller')
@client.get('/docs/api/controller.html')
async def controller(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/controller'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'controller.html'.
    """
    return HTMLResponse(open('templates/docs/api/controller.html').read())
    


@client.get('/docs/api/exceptions')
@client.get('/docs/api/exceptions.html')
async def exceptions(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/exceptions'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'exceptions.html'.
    """
    return HTMLResponse(open('templates/docs/api/exceptions.html').read())
    


@client.get('/docs/api/index')
@client.get('/docs/api/index.html')
async def index(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/index'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'index.html'.
    """
    return HTMLResponse(open('templates/docs/api/index.html').read())


@client.get('/docs/api/models')
@client.get('/docs/api/models.html')
async def models(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/models'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'models.html'.
    """
    return HTMLResponse(open('templates/docs/api/models.html').read())


@client.get('/docs/api/schemas')
@client.get('/docs/api/schemas.html')
async def schemas(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/schemas'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'schemas.html'.
    """
    return HTMLResponse(open('templates/docs/api/schemas.html').read())


@client.get('/docs/api/service')
@client.get('/docs/api/service.html')
async def service(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/service'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'service.html'.
    """
    return HTMLResponse(open('templates/docs/api/service.html').read())


@client.get('/docs/api/utils')
@client.get('/docs/api/utils.html')
async def utils(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/utils'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'utils.html'.
    """
    return HTMLResponse(open('templates/docs/api/utils.html').read())


@client.get('/docs/api/mail_parse')
@client.get('/docs/api/mail_parse.html')
async def mail_parse(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/mail_parse'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'mail_parse.html'.
    """
    return HTMLResponse(open('templates/docs/api/mail_parse.html').read())


@client.get('/docs/api/inference_catboost')
@client.get('/docs/api/inference_catboost.html')
async def inference_catboost(request: Request):
    """
    Обработчик запроса для эндпоинта '/docs/api/inference_catboost'.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HTMLResponse: Ответ с содержимым HTML-шаблона 'inference_catboost.html'.
    """
    return HTMLResponse(open('templates/docs/api/inference_catboost.html').read())
