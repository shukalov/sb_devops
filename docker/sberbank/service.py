import asyncio
import concurrent.futures
from aiomisc import entrypoint
from aiomisc.service import Service

import os
from random import randint
from time import sleep
import logging

from lib.state import env
from lib import config

from rest import REST


def cpu_bound(uuid):
    latency = randint(1, 10)
    sleep(latency)
    result = f'Задача с uuid={uuid} завершена на pid={os.getpid()} за {latency} секунд'
    return {
        'uuid': uuid,
        'result': result
    }


class SaveResultService(Service):
    """Сервис сохранения результатов, выполненных задач."""
    async def start(self):
        while True:
            task1 = await env.result_queue.get()
            completed, pending = await asyncio.wait({task1})
            result = [t.result() for t in completed]

            log.info(f'Получен результат задачи с uuid={result[0]["uuid"]}: {result[0]["result"]}')

            if result[0]["uuid"] in env.results:
                log.info(f'Результаты задачи с uuid={result[0]["uuid"]} будут перезаписаны (')

            env.results[result[0]['uuid']] = result[0]['result']


class ConsumerService(Service):
    """Сервис подписки на исполнение очереди задач."""
    async def start(self):

        while True:
            task1 = await env.task_queue.get()
            batch_tasks = [task1]
            max_workers = min(env.config['max_workers'], env.task_queue.qsize() + 1)
            for task in range(max_workers - 1):
                batch_tasks.append(await env.task_queue.get())
            log.info(f'Задачи на исполнение{batch_tasks}')

            loop = asyncio.get_event_loop()

            for t in batch_tasks:
                env.result_queue.put_nowait(loop.run_in_executor(env.executor, cpu_bound, t))


services = (
    REST(address=env.config['address'], port=env.config['port']),
    ConsumerService(),
    SaveResultService(),
)


if __name__ == '__main__':

    log = logging.getLogger('Service')

    loop = asyncio.get_event_loop()
    # очередь невыполненных задач
    env.task_queue = asyncio.Queue(loop=loop)
    # очередь запущенных или отработанных задач, результат которых не сохранён
    env.result_queue = asyncio.Queue(loop=loop)

    # устанавливаем максимальное количество воркеров для cpu bound задач из конфига или по числу ядер
    max_workers = env.config.get('max_workers', os.cpu_count())
    # cpu bound запускаем в отдельном процессе
    env.executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=max_workers,
    )

    env.results = {}

    with entrypoint(*services, loop=loop) as loop:
        loop.run_forever()
