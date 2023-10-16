# RabbitMQ transport for Domain-driven Design Misc

Пакет предоставляет транспортную надстройку на `MessageBus` пакета [`ddd-misc`](https://pypi.org/project/ddd-misc/)
для осуществления публикации событий и RPC-вызова команд посредством брокера RabbitMQ.

## Классы

**Классы объектов**
- `AsyncRMQEventTransport` - асинхронный класс транспорта выполняющий публикацию и подписку на события
- `SyncRMQEventTransport` - синхронный класс транспорта выполняющий публикацию и подписку на события


Сигнатура инициализации классов:

`AsyncRMQEventTransport(messagebus: AsyncMessageBus, url: t.Union[str, URL], service_name, *, 
publish_middlewares: t.Iterable[AbstractPublisherMiddleware] = (),
consume_middlewares: t.Iterable[AbstractConsumerMiddleware] = (),
**kwargs)`

`SyncRMQEventTransport(messagebus: MessageBus, url: t.Union[str, URL], service_name, *, 
publish_middlewares: t.Iterable[AbstractPublisherMiddleware] = (),
consume_middlewares: t.Iterable[AbstractConsumerMiddleware] = (),
**kwargs)`

- `messagebus` - инстанс класса шины сообщений используемой в сервисе
- `url` - урл подключения к брокеру RabbitMQ формата `amqps://user:password@broker-host/vhost`
- `service_name` - наименование микросервиса, используется: 
  - для формирования наименования exchange в который будет осуществляться публикация событий на основании шаблона `<service_name>_events`
  - используется в качестве наименования очереди для подписки на события по умолчанию
- `prefetch_count` - максимальное количество одновременно обрабатываемых событий
- `publish_middlewares` - middleware вызываемые при публикации событий
- `consume_middlewares` - middleware вызываемые при получении событий по подписке
- `**kwargs` - дополнительно возможные расширения параметризации класса транспорта

_свойства_
- `is_ready` - готовность класса принимать/отправлять события
- `service_name` - наименование сервиса заданное при ининциализации

_методы_
- `def register(events: *t.Type[DDDEvent])` - регистрация событий для публикации через брокер
  - `events` - классы событий
- `def consume_to_service(service_name: str, queue_name: str = None)` - метод подписки на все события публикуемые заданным микросервисом
  - `service_name` - наименование стороннего сервиса, на exchange которого будет осуществлена подписка
  - `queue_name` - специфичное наименование очереди. При передаче пустой строки будет осуществлена посредством временной очереди
- `def consume_to_domain(service_name: str, domain: str, queue_name: str = None)` - метод подписки на все события указанного домена, публикуемые заданным микросервисом
  - `service_name` - наименование стороннего сервиса, на exchange которого будет осуществлена подписка
  - `domain` - наименование домена на события которого будет осуществлена подписка
  - `queue_name` - специфичное наименование очереди. При передаче пустой строки будет осуществлена посредством временной очереди
- `def consume_to_event(service_name: str, event: t.Type[DDDEvent], queue_name: str = None)` - метод подписки на конкретное событие, публикуемое данным сервисом
  - `service_name` - наименование стороннего сервиса, на exchange которого будет осуществлена подписка
  - `event` - наименование домена на события которого будет осуществлена подписка
  - `queue_name` - специфичное наименование очереди. При передаче пустой строки будет осуществлена посредством временной очереди

_!!! Допускается подписка на события собственного сервиса при этом события полученные через брокер 
не будут повторно опубликованы в брокер сообщений_


## Примеры использования

**Пример использования для публикации событий**
```python
from sample_project.bootstap import messagebus
from sample_project.domain.events import CompleteEvent, SpecificEvent
from dddmisc_rmq import AsyncRMQEventTransport

transport = AsyncRMQEventTransport(messagebus, 'amqps://guest:guest@localhost/vhost', 'sample_project')
transport.register(CompleteEvent, SpecificEvent)
```

**Пример использования для подписки на события**
```python
from sample_project.bootstap import messagebus
from other_project.events import CompleteEvent, SpecificEvent
from dddmisc_rmq import AsyncRMQEventTransport

transport = AsyncRMQEventTransport(messagebus, 'amqps://guest:guest@localhost/vhost', 'sample_project')
transport.consume_to_event('other_project', CompleteEvent)  # Подписка на событие CompleteEvent через постоянную очередь sample_project
transport.consume_to_domain('other_project', 'other_domain', '')  # Экслюзивная подписка на события домена через временную очередь
transport.consume_to_service('other_project', 'sample-queue')  # Подписка на все события домена через постоянную очередь sample-queue

```

**Пример одновренменной подписки и публикации событий**
```python
from sample_project.bootstap import messagebus
from sample_project.events import SuccessEvent
from other_project.events import CompleteEvent, SpecificEvent
from dddmisc_rmq import AsyncRMQEventTransport

transport = AsyncRMQEventTransport(messagebus, 'amqps://guest:guest@localhost/vhost', 'sample_project')
transport.register(SuccessEvent)
transport.consume_to_event('other_project', CompleteEvent)  # Подписка на событие CompleteEvent через постоянную очередь sample_project
transport.consume_to_domain('other_project', 'other_domain', '')  # Экслюзивная подписка на события домена через временную очередь
transport.consume_to_service('other_project', 'sample-queue')  # Подписка на все события домена через постоянную очередь sample-queue

```


**Пример использования middleware**
```python
from sample_project.bootstap import messagebus
from sample_project.events import SuccessEvent
from other_project.events import CompleteEvent, SpecificEvent
import typing as t
from uuid import uuid4
import contextvars as cv
from dddmisc_rmq import AsyncRMQEventTransport, AbstractPublisherMiddleware, AbstractConsumerMiddleware
from aio_pika.abc import AbstractMessage, AbstractIncomingMessage


class PublisherMiddleware(AbstractPublisherMiddleware):

  async def __call__(self, message: AbstractMessage, routing_key: str,
                     publisher: t.Callable[[AbstractMessage, str], t.Coroutine]):
    message.correlation_id = str(cv.ContextVar('correlation_id').get(uuid4()))
    return await publisher(message, routing_key)


class ConsumeMiddleware(AbstractConsumerMiddleware):

  async def __call__(self, message: AbstractIncomingMessage,
                     consumer: t.Callable[[AbstractIncomingMessage], t.Coroutine]):
    cv.ContextVar('correlation_id').set(message.correlation_id or uuid4())
    return await consumer(message)


transport = AsyncRMQEventTransport(messagebus, 'amqps://guest:guest@localhost/vhost', 'sample_project',
                                   publish_middlewares=[PublisherMiddleware()],
                                   consume_middlewares=[ConsumeMiddleware()])
transport.register(SuccessEvent)
transport.consume_to_event('other_project', CompleteEvent)  # Подписка на событие CompleteEvent через постоянную очередь sample_project
transport.consume_to_domain('other_project', 'other_domain','')  # Экслюзивная подписка на события домена через временную очередь
transport.consume_to_service('other_project', 'sample-queue')  # Подписка на все события домена через постоянную очередь sample-queue

```


## Changelog 

**0.2.0** 
- Add support middlewares

**0.1.2**
- Add support ddd-misc version >=0.8.1 < 0.9.0

**0.1.1**

- Change exchange type from `Fanout` to `Topic`

**0.1.0**

- First release




