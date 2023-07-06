# Deepfake API

API предоставляет возможность генерации deepfake видео на основе загружаемых фотографий и видео.
____

## Методы API

### 1. Создание задачи по генерации deepfake

<span style="font-size: 12px; color:blue; border: 2px solid blue; border-radius: 5px; padding: 4px; font-weight: bold;">POST</span> `/task/create/`

#### Описание:

Создает новую задачу по генерации deepfake видео. В качестве параметров принимает файлы фотографии и видео. Проверяет
расширения файлов и сохраняет их в директории задачи. Добавляет задачу в очередь.

#### Параметры:

- `photo` : `bytes` - Фото с лицом (`JPEG`, `JPG`)
- `video` : `bytes` - Видео в котором будут заменяться лица (`MP4`)

#### Возвращаемые значения

Возвращает информацию о созданной задаче.

```python
# json
{
    "id": "string",
    "status": "pending",
    "created": "string"
}
```

#### Ошибки

- `NotVideoFileError` : Если файл видео не является видео файлом.
- `NotImageFileError` : Если файл фото не является фото файлом.
- `VideoExtensionError` : Если расширение файла видео запрещено.
- `PhotoExtensionError` : Если расширение файла фото запрещено.
- `ValidationError` - тип данных не верный.

#### Пример кода на Python:

```python
import requests

url = "http://localhost:8000/task/create/"
files = {
    "photo": open("path_to_your_photo.jpg", "rb"),
    "video": open("path_to_your_video.mp4", "rb"),
}

response = requests.post(url, files=files)
print(response.json())
```

____

### 2. Получение статуса задачи

<span style="font-size: 12px; color:green; border: 2px solid green; border-radius: 5px; padding: 4px; font-weight: bold;">GET</span>  `/task/status/`

#### Описание:

Создает новую задачу по генерации deepfake видео. В качестве параметров принимает файлы фотографии и видео. Проверяет
расширения файлов и сохраняет их в директории задачи. Добавляет задачу в очередь.

#### Параметры:

- `task_id` : `str` - `id` задачи.

#### Возвращаемые значения

Возвращает информацию о задаче.

```python
# json
{
    "id": "string",
    "status": "pending",
    "created": "string",
    "error": "string"
}
```

#### Ошибки

- `NotFoundTaskError` - задача с указанным id не найдена.
- `ValidationError` - тип данных не верный.

#### Пример кода на Python:

```python
import requests

task_id = "your_task_id"
url = f"http://localhost:8000/task/status/?task_id={task_id}"

response = requests.get(url)
print(response.json())
```

____

### 3. Скачивание сгенерированного видео

<span style="font-size: 12px; color:green; border: 2px solid green; border-radius: 5px; padding: 4px; font-weight: bold;">GET</span>  `/task/download/`

#### Описание:

Позволяет скачать видео-результат задачи по её id

#### Параметры:

- `task_id` : `str` - `id` задачи.

#### Возвращаемые значения

Возвращает файл видео-результат с замененными лицами в формате `MP4`.

#### Ошибки

- `NotFoundTaskError` - задача с указанным id не найдена.
- `NotFoundFileError` - видео-результат задачи не найден.
- `ValidationError` - тип данных не верный.

**Пример кода на Python:**

```python
import requests

task_id = "your_task_id"
url = f"http://localhost:8000/task/download/?task_id={task_id}"
response = requests.get(url)

with open("path_to_save_video.mp4", "wb") as f:
    f.write(response.content)
```
____
## Статусы задач:
 В системе задачи могут иметь следующие статусы:
 - `pending` - Задача ожидает обработки.
 - `in_progress` - Задача в процессе выполнения.
 - `completed` - Задача успешно выполнена.
 - `failed` - Задачу не удалось выполнить.
____
## Ошибки:

#### `NotVideoFileError` - файл видео не является видео файлом.

- Status Code: `400`

```python
# json
{
    "detail": "File is not a video."
}
```

____

#### `NotImageFileError` - файл фото не является фото файлом.

- Status Code: `400`

```python
# json
{
    "detail": "File is not an image."
}
```

____

#### `VideoExtensionError` - расширение файла видео запрещено.

- Status Code: `400`

```python
# json
{
    "detail": "Unsupported video extension."
}
```

____

#### `PhotoExtensionError` - расширение файла фото запрещено.

- Status Code: `400`

```python
# json
{
    "detail": "Unsupported photo extension."
}
```

____

#### `NotFoundTaskError` - задача с указанным id не найдена.

- Status Code: `404`

```python
# json
{
    "detail": "Task not found."
}
```

____


#### `NotFoundFileError` - видео-результат задачи не найден.

- Status Code: `404`

```python
# json
{
    "detail": "File not found."
}
```

____


#### `ValidationError` - тип данных не верный.

- Status Code: `422`

```python
# json
{
    "detail": [
        {
            "loc": [
                "string",
                0
            ],
            "msg": "string",
            "type": "string"
        }
    ]
}
```
____

# Установка

Положить в папку `/neural_processing/` файл [`inswapper_128.onnx`](https://drive.google.com/file/d/1ZIuqBh8BacV1uMkabjCAzEUt1qrY-T-W/view?usp=sharing)

###Репозиторий нейросети 
[`https://github.com/s0md3v/roop`](https://github.com/s0md3v/roop)
    

