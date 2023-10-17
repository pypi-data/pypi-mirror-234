# Назначение
Это обычный logging, но с более широкими настройками

# Применение
```
from dsutp_custom_logger import Logging
log = Logging().get_logger()
log.info('Test my logs')
```
# Описание параметров класса Logging
1. log_file_enabled - запись логов в файл. Принимает булево значение True/False. Default = True
2. log_console_enabled - запись логов в консоль. Принимает булево значение True/False. Default = True
3. log_httpsink_enabled - отправка логов в удаленный http. Принимает булево значение True/False. Default = False
4. log_httpsink_url - http ссылка до удаленого лог приемника. Принимает строковое значение ссылки. Default = None
5. log_level - уровень логгирования. Принимает строковое значение DEBUG/INFO/WARNINGS ... .Default = INFO
6. log_buffer_size_file - размер файла в байтах. Принимает целочисленное значение. Default = 5 * 10**7 (50 Мб)
7. backupCount - число файлов с историей. Принимает целочисленное значение. Default = 1
8. stream - потоки. Принимает список кастомных потоков. Default = []
9. log_location - место файлов для логов. Принимает строкове значение. Default = log.log
10. base_json_fields - "системные" поля для логов. Принимает словарь. Default = None
11. custon_json_fields - кастомные поля для логов. Принимает словарь. Default = None
12. log_structured_datetimeformat - формат даты. Принимает строковое значение. Default = '%Y-%m-%d %H:%M:%S'

## Подбробное описание
### log_httpsink_enabled и log_httpsink_url
Если log_httpsink_enabled = True и указана log_httpsink_url ссылка, то в зависимости от выставленного порога log_level будет отправлять тело запроса с полями {'level': '', 'message': ''}.

### stream
Вы можете определить свой stream. Для этого нужно:

```
from dsutp_custom_logger import Stream, Logging

class YourCustomStream(Stream):
    def write(self, msg: str) -> None:
        do_something

log = Logging(stream = [YourCustomStream()]).get_logger()
```

### base_json_fields
Словарь с базовыми полям, ключи можно изменять, а ключи статичный.
Данные поля заполняются системными данными.
```
{"level": "levelname", 
"message": "message", 
"loggerName": "name", 
"processName": "processName",
"processID": "process", 
"threadName": "threadName", 
"threadID": "thread",
"timestamp": "asctime",
"filename":"filename",
"module":"module",
"pathname":"pathname"}
```

### custon_json_fields
Можно задать свои кастомные поля с уже заполнеными данными
```
{""RequestID":"123",
"Span":"344",
...}
```

# Тесты

В папке tests находятся тесты с результатми