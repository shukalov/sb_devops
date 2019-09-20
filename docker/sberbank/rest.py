import logging
import re
import aiohttp
from aiomisc.service.aiohttp import AIOHTTPService
from lib.state import env

log = logging.getLogger(__name__)


async def create_task(request):
    """Добавляет задачу в очередь."""
    try:
        log.info('Получен запрос на выполнение задачи')

        uuid = await get_task_from_api()
        log.info(f'От внешней системы получен uuid={uuid}')

        env.task_queue.put_nowait(uuid)
        log.info(f'Задача с uuid={uuid} добавлена в очередь')

        return aiohttp.web.Response(text=uuid)

    except Exception as e:
        log.error(e)

        return aiohttp.web.HTTPInternalServerError()


async def get_task_from_api():
    """Забирает uuid с внешнего api"""
    async with aiohttp.ClientSession() as session:
        async with session.get(env.config['task_uid_api']) as resp:
            uuid = await resp.text()
            uuid = re.sub('[\n\t\r]', '', uuid)

            return uuid


async def result(request):
    """Возвращаем результат по uuid"""
    uuid = request.match_info.get('uuid')
    if uuid not in env.results:
        return aiohttp.web.HTTPNotFound()
    result = env.results[uuid]

    return aiohttp.web.Response(text=result)


class REST(AIOHTTPService):
    """Сервис REST"""
    async def create_application(self):
        app = aiohttp.web.Application()

        app.add_routes([
            aiohttp.web.get('/add_task', create_task),
            aiohttp.web.get('/result/{uuid}', result),
        ])

        return app
