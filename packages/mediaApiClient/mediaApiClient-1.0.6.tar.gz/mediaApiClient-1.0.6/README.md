# mediaApiClient

Публичная библиотека для работы c MediAPI ContentApiGate, написанная на PYTHON.

## MediAPI

MediAPI - контент-платформа Медиатек, предназначенная для доставки контента от правообладателей к операторам.

Для получения токена доступа production и staging-среды обратитесь к вашему менеджеру или свяжитесь с нами: sales@mediatech.by

## Установка

Установка последней версии mediaApiClient с ресурса [PyPI](https://pypi.org/project/mediaApiClient/):

```bash
pip install mediaApiClient
```

## Документация по отдельным контроллерам

* Контроллеры

  * [Работа с Content Controller](docs/content.md)
  * [Работа с Stream Controller](docs/stream.md)
  * [Работа с Service Controller](docs/service.md)
  * [Работа с Account Controller](docs/account.md)
  * [Работа с Compilation Controller](docs/compilation.md)

Так же, [MediAPI Swagger](https://mediapi.mediatech.by/swagger-ui) поможет вам в изучении структуры API.

### Основные концепции MediAPI

* `Client`: клиент MediAPI, как правило - OTT/IPTV-оператор.
* `Service`: библиотека контента, как правило сформированная одним поставщиком контента.
* `Account`: аккаунт конечного пользователя услуги, как правило подписчик OTT/IPTV-оператора.
* `Content`: сам контент, фильмы, сериалы и др.
* `Stream`: уникальная ссылка для каждой еденицы `Content`, сгенерированная для `Account`
* `Compilation`: коллекция контента, может объеденять в себе контент из разных сервисов, доступных клиенту. Зачастую это тематические подборки.


## Лицензия

[BSD 3-Clause License](LICENSE)