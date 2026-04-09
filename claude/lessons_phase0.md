# Уроки фазы 0: Git, Структура проекта, DVC, Pandera

## Как устроены уроки
Каждый урок:
1. **Теория** — полное объяснение с нуля, без предположений о предыдущих знаниях
2. **Упражнения** — от простого к сложному, каждое следующее опирается на предыдущее
3. **Финальное задание** — применение к HeatWin (реальное действие из фазы 0)

Порядок уроков обязателен: Git → Структура → DVC → Pandera.

---
---

# Урок 1: Git — версионирование кода

## 1.1 Теория: зачем нужен Git

### Проблема без Git
Представьте: вы работаете над EDA. Файлы выглядят так:
```
eda_v1.py
eda_v2.py
eda_v2_fix.py
eda_v2_fix_FINAL.py
eda_v2_fix_FINAL_real.py
```
Через месяц вы не помните: что изменилось между v1 и v2? Какой fix был в fix_FINAL? А если нужно вернуться к v1, потому что v2 сломала всё?

### Что такое Git
Git — система контроля версий. Вместо копий файлов Git хранит **историю изменений**. Каждое сохранение (commit) — это снимок всего проекта в конкретный момент. Вы можете:
- Посмотреть что изменилось между любыми двумя моментами
- Вернуться к любому моменту в прошлом
- Работать над несколькими идеями параллельно (branches)
- Делиться кодом через GitHub/GitLab

### Ключевые концепции

**Repository (репозиторий, repo)** — папка проекта, в которой Git отслеживает изменения. Создаётся через `git init`.

**Commit (коммит)** — сохранение текущего состояния. Каждый commit имеет:
- Уникальный ID (хэш, например `a1b2c3d`)
- Сообщение (описание: что и зачем изменили)
- Автора
- Дату
- Ссылку на предыдущий commit (история)

**Staging area (индекс)** — промежуточная зона. Прежде чем сделать commit, вы выбираете какие именно изменения включить. Это позволяет делать коммиты логически целостными:
```
Изменили 5 файлов → добавили 3 из них в staging → commit
                  → добавили оставшиеся 2 в staging → другой commit
```

**Три состояния файла:**
```
Working Directory → Staging Area → Repository
  (файлы на диске)   (git add)     (git commit)
```

**Branch (ветка)** — параллельная линия разработки. Основная ветка — `main`. Создаёте ветку `feature/eda`, работаете там, потом сливаете (merge) обратно в `main`.

**Remote (удалённый репозиторий)** — копия на GitHub/GitLab. Команды:
- `git push` — отправить свои коммиты на remote
- `git pull` — получить коммиты с remote

**.gitignore** — файл со списком того, что Git должен игнорировать (данные, кэши, виртуальное окружение).

### Основные команды

```bash
# Создание
git init                          # инициализировать Git в текущей папке
git clone <url>                   # скопировать существующий репозиторий

# Просмотр
git status                        # что изменено? что в staging?
git log                           # история коммитов
git log --oneline                 # компактная история
git diff                          # что изменилось в файлах (не в staging)
git diff --staged                 # что в staging (будет в следующем commit)

# Основной цикл
git add <файл>                    # добавить файл в staging
git add .                         # добавить ВСЕ изменения в staging
git commit -m "сообщение"         # сделать коммит
git commit -am "сообщение"        # add + commit для уже отслеживаемых файлов

# Ветки
git branch                        # список веток
git branch <имя>                  # создать ветку
git checkout <имя>                # переключиться на ветку
git checkout -b <имя>             # создать И переключиться
git merge <имя>                   # слить ветку в текущую

# Remote
git remote add origin <url>       # привязать remote
git push -u origin main           # отправить main на remote
git push                          # отправить текущую ветку
git pull                          # получить обновления с remote
```

### Правила хороших коммитов

**Формат сообщения:** `<тип>: <что сделано>`

Типы:
- `init` — начало проекта, настройка
- `docs` — документация
- `feat` — новая функциональность
- `fix` — исправление ошибки
- `test` — тесты
- `refactor` — переработка кода без изменения поведения
- `config` — конфигурация, зависимости
- `eda` — исследовательский анализ данных
- `model` — моделирование

**Примеры хороших:**
```
init: project structure and README
docs: add Project Brief v1.0
feat: add lag features for T_return (1h-24h)
fix: correct data leakage in walk-forward split
test: add validation check for T_return < T_supply
config: add requirements.txt with pandas 2.1
eda: add distribution analysis for energy_kWh
```

**Примеры плохих:**
```
update            ← что обновлено?
fix               ← что исправлено?
changes           ← какие изменения?
asdfgh            ← без комментариев
WIP               ← не коммитьте незаконченное в main
```

### .gitignore

Файл в корне репозитория. Каждая строка — шаблон для игнорирования:
```
# Комментарий

# Конкретный файл
secret.txt

# Расширение
*.csv
*.pkl

# Папка
data/
__pycache__/
.venv/

# Исключение из игнорирования (! = НЕ игнорировать)
!data/.gitkeep
```

`.gitkeep` — пустой файл-маркер. Git не отслеживает пустые папки. Если хотите, чтобы папка `data/` существовала в репо (но без содержимого) — кладёте `.gitkeep` внутрь и добавляете `!data/.gitkeep` в .gitignore.

---

## 1.2 Упражнения

### Упражнение 1.1: Первый репозиторий (базовое)

**Задание:**
1. Создайте папку `git-practice/`
2. Инициализируйте Git
3. Создайте файл `hello.py` с содержимым `print("Hello, Git!")`
4. Посмотрите статус (`git status`) — файл должен быть untracked
5. Добавьте в staging (`git add`)
6. Посмотрите статус снова — файл должен быть в staging
7. Сделайте коммит: `init: add hello.py`
8. Посмотрите лог — должен быть 1 коммит

**Ожидаемый результат:**
```
$ git log --oneline
a1b2c3d init: add hello.py
```

### Упражнение 1.2: Цикл изменений (add → commit)

**Задание:**
1. Измените `hello.py`: добавьте вторую строку `print("Learning Git")`
2. Создайте файл `notes.txt` с текстом `Git lesson 1`
3. Посмотрите `git diff` — увидите изменения в hello.py
4. Добавьте **только** hello.py в staging: `git add hello.py`
5. Посмотрите `git status` — hello.py в staging, notes.txt нет
6. Коммит: `feat: add second print statement`
7. Теперь добавьте notes.txt и коммит: `docs: add study notes`
8. Посмотрите лог — должно быть 3 коммита

**Чему учит:** staging позволяет делать коммиты логически целостными. Каждый коммит — одна задача.

### Упражнение 1.3: .gitignore

**Задание:**
1. Создайте файлы: `data.csv`, `model.pkl`, `config.yaml`
2. Создайте папку `__pycache__/` с файлом `module.pyc` внутри
3. Сейчас `git status` покажет их все как untracked
4. Создайте `.gitignore`:
```
*.csv
*.pkl
__pycache__/
```
5. Снова `git status` — data.csv, model.pkl, __pycache__ исчезли, но config.yaml и .gitignore видны
6. Добавьте оба и коммит: `config: add .gitignore and config.yaml`

**Чему учит:** .gitignore защищает от случайного коммита данных и мусора.

### Упражнение 1.4: Ветки и merge (ключевое)

**Задание:**
1. Убедитесь что вы на ветке `main` (`git branch`)
2. Создайте ветку: `git checkout -b feature/add-functions`
3. Создайте файл `utils.py`:
```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```
4. Коммит: `feat: add math utility functions`
5. Переключитесь на main: `git checkout main`
6. Обратите внимание: `utils.py` исчез! Он существует только в ветке feature/add-functions
7. Слейте ветку: `git merge feature/add-functions`
8. Теперь `utils.py` появился в main
9. Посмотрите лог — видна история из обеих веток

**Чему учит:** ветки изолируют работу. Пока вы экспериментируете в feature-ветке, main остаётся стабильной.

### Упражнение 1.5: Remote (GitHub)

**Задание:**
1. Создайте пустой репозиторий на GitHub (без README, без .gitignore)
2. В вашем локальном репо:
```bash
git remote add origin https://github.com/<ваш-username>/git-practice.git
git push -u origin main
```
3. Откройте GitHub в браузере — все файлы и история коммитов видны
4. Измените hello.py локально, коммит, `git push`
5. Обновите страницу на GitHub — изменения видны

**Чему учит:** GitHub — это remote-копия. Push отправляет, pull получает.

### Упражнение 1.6: Полный workflow (интеграционное)

**Задание:** Симулировать реальный рабочий процесс.
1. На ветке main создайте `README.md`: `# Git Practice\nLearning Git step by step.`
2. Коммит: `docs: add README`
3. Создайте ветку `feature/analysis`
4. В ней создайте `analysis.py`:
```python
import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def describe_data(df):
    return df.describe()
```
5. Коммит: `feat: add data analysis functions`
6. Добавьте в analysis.py функцию:
```python
def count_missing(df):
    return df.isna().sum()
```
7. Коммит: `feat: add missing values counter`
8. Переключитесь на main, merge feature/analysis
9. Push всё на GitHub
10. Посмотрите историю: `git log --oneline --graph`

**Ожидаемый результат:** чистая история с осмысленными сообщениями, merge из feature-ветки.

---

## 1.3 Финальное задание: Git для HeatWin

**Сделать после всех упражнений:**
1. Создать репозиторий `heatwin` на GitHub (public)
2. Локально: `git init`, создать .gitignore по шаблону из phase0_infrastructure.md
3. Коммит: `init: create repository with .gitignore`
4. Push на GitHub
5. Проверить: на GitHub видна чистая история с 1 осмысленным коммитом

→ Это действие из задачи 0.1 нашего phase0_infrastructure.md.

---
---

# Урок 2: Структура DS-проекта

## 2.1 Теория: зачем нужна структура

### Проблема без структуры
```
heatwin/
├── analysis.ipynb
├── analysis_v2.ipynb
├── clean_data.py
├── data.csv
├── features.py
├── model.pkl
├── plots.py
├── test.py
├── train.py
└── utils.py
```
10 файлов в одной папке. Где raw data? Где processed? clean_data.py — это для запуска или для импорта? test.py — это unit-тест или тестовый скрипт?

### Принцип: analysis is a DAG

DAG = Directed Acyclic Graph (направленный ациклический граф). Каждый шаг вашего анализа зависит от предыдущего:

```
raw data → clean data → features → train/test → model → predictions
```

Структура папок должна отражать этот граф. Если raw data в той же папке что predictions — непонятно что от чего зависит.

### Принципы Cookiecutter Data Science

1. **Данные иммутабельны.** Raw data никогда не меняется. Очистка создаёт НОВЫЙ файл в другой папке.
2. **Notebooks для exploration, src для production.** Notebook = черновик, скрипт = чистовик. Notebooks не вызываются из скриптов.
3. **Среда воспроизводима.** requirements.txt или environment.yml — любой может воссоздать окружение.
4. **Тесты рядом с кодом.** Каждая функция может быть проверена.

### Стандартная структура

```
project_name/
│
├── README.md              ← Что это за проект? Как запустить?
├── requirements.txt       ← Зависимости Python
├── Makefile               ← Команды: make data, make train
├── .gitignore             ← Что не отслеживать
│
├── data/                  ← ВСЕ данные (НЕ в Git)
│   ├── raw/               ← Исходные, неизменяемые
│   ├── interim/           ← После очистки (промежуточные)
│   └── processed/         ← Финальные, для моделирования
│
├── notebooks/             ← Jupyter notebooks (exploration)
│   ├── 01_eda.ipynb
│   └── 02_modeling.ipynb
│
├── src/                   ← Python-модули (production code)
│   ├── __init__.py
│   ├── data/              ← Загрузка и очистка
│   │   ├── __init__.py
│   │   └── load.py
│   ├── features/          ← Feature engineering
│   │   ├── __init__.py
│   │   └── build.py
│   └── models/            ← Обучение и предсказание
│       ├── __init__.py
│       └── train.py
│
├── tests/                 ← Тесты
│   └── test_features.py
│
├── configs/               ← Параметры
│   └── params.yaml
│
└── docs/                  ← Документация
    └── project_brief.md
```

### Зачем что

| Папка | Зачем | Что внутри | В Git? |
|---|---|---|---|
| data/raw/ | Неизменяемый источник | CSV, парquet от клиента | Нет (DVC) |
| data/interim/ | Промежуточные результаты | После очистки | Нет (DVC) |
| data/processed/ | Финальные данные | train.parquet, test.parquet | Нет (DVC) |
| notebooks/ | Исследование, визуализации | Jupyter notebooks | Да |
| src/ | Production-ready код | .py модули с функциями | Да |
| tests/ | Проверки | pytest файлы | Да |
| configs/ | Параметры | YAML/JSON конфигурации | Да |
| docs/ | Документация | Markdown, PDF | Да |

### __init__.py

Пустой файл (или с импортами) в каждой подпапке src/. Делает папку Python-пакетом, позволяя:
```python
from src.features.build import create_lag_features
```

Без __init__.py Python не «видит» папку как пакет.

### Makefile (основы)

Makefile — набор команд с именами. Вместо запоминания длинных команд:
```makefile
.PHONY: data clean test

data:
	python src/data/load.py

clean:
	rm -rf data/interim/* data/processed/*

test:
	python -m pytest tests/ -v
```

Запуск: `make data`, `make test`, `make clean`.

`.PHONY` — говорит Make, что это не файлы, а команды.

**Важно:** в Makefile отступы — это TAB, не пробелы. Это частая ошибка.

---

## 2.2 Упражнения

### Упражнение 2.1: Создать структуру вручную

**Задание:**
1. В репозитории `git-practice` (из урока 1) создайте полную структуру:
```bash
mkdir -p data/raw data/interim data/processed
mkdir -p src/data src/features src/models
mkdir -p notebooks tests configs docs
```
2. Создайте .gitkeep в каждой папке data/:
```bash
touch data/raw/.gitkeep data/interim/.gitkeep data/processed/.gitkeep
```
3. Создайте __init__.py в каждой подпапке src/:
```bash
touch src/__init__.py src/data/__init__.py src/features/__init__.py src/models/__init__.py
```
4. Коммит: `init: create project directory structure`

### Упражнение 2.2: Разложить код по папкам

**Задание:** У вас есть один файл `messy_project.py` (создайте его):

```python
import pandas as pd
import numpy as np

# --- Data loading ---
def load_csv(path):
    return pd.read_csv(path, parse_dates=['timestamp'])

# --- Cleaning ---
def remove_duplicates(df):
    return df.drop_duplicates()

def fill_missing(df, column, method='ffill'):
    df[column] = df[column].fillna(method=method)
    return df

# --- Features ---
def add_lag(df, column, lag=1):
    df[f'{column}_lag_{lag}'] = df[column].shift(lag)
    return df

def add_rolling_mean(df, column, window=3):
    df[f'{column}_rolling_{window}'] = df[column].rolling(window).mean()
    return df

# --- Model ---
def train_model(X, y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    return model
```

Разложите по файлам:
- `src/data/load.py` — load_csv
- `src/data/clean.py` — remove_duplicates, fill_missing
- `src/features/build.py` — add_lag, add_rolling_mean
- `src/models/train.py` — train_model

Каждый коммит — один файл:
```
feat: add data loading module
feat: add data cleaning functions
feat: add feature engineering functions
feat: add model training module
```

### Упражнение 2.3: Notebook vs src

**Задание:**
1. Создайте `notebooks/01_exploration.ipynb` (или .py если нет Jupyter)
2. В нём импортируйте функции из src:
```python
from src.data.load import load_csv
from src.features.build import add_lag, add_rolling_mean
```
3. Покажите, что notebook использует src/, а не дублирует код

**Чему учит:** notebook вызывает production-код, а не содержит его.

### Упражнение 2.4: Makefile

**Задание:**
1. Создайте `Makefile` (файл без расширения, в корне проекта):
```makefile
.PHONY: setup test clean structure

setup:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

clean:
	rm -rf data/interim/* data/processed/*
	find . -type d -name __pycache__ -exec rm -rf {} +

structure:
	@echo "Project structure:"
	@find . -type f -not -path './.git/*' -not -path './.venv/*' | sort
```
2. Создайте `requirements.txt`:
```
pandas>=2.1
numpy>=1.24
pytest>=7.0
```
3. Запустите: `make structure` — должно вывести дерево файлов
4. Коммит: `config: add Makefile and requirements.txt`

---

---

## 2.2b Теория: logging, .env, type hints

### Python logging — замена print()

**Проблема с print():**
```python
print("Loading data...")          # где это выводится?
print(f"Rows: {len(df)}")         # в production это мусор в stdout
print("WARNING: 50 missing!")     # не отличить от обычного вывода
```

В production print() бесполезен: его нельзя отключить, нельзя перенаправить в файл, нельзя фильтровать по важности.

**Решение — модуль logging:**
```python
import logging

# Настройка (один раз в начале скрипта)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)
```

**Уровни важности (от низшего к высшему):**
```python
logger.debug("Loaded 1000 rows")       # детали для отладки (обычно выключено)
logger.info("Pipeline started")         # нормальная работа
logger.warning("50 missing values")     # проблема, но работаем дальше
logger.error("File not found: x.csv")   # ошибка, шаг не выполнен
logger.critical("Database down")        # всё сломалось
```

`level=logging.INFO` означает: показывать INFO и выше (INFO, WARNING, ERROR, CRITICAL). DEBUG — скрыт. Для отладки меняете на `level=logging.DEBUG`.

**Логирование в файл:**
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),   # в файл
        logging.StreamHandler()                      # и в консоль
    ]
)
```

**Паттерн для DS-pipeline:**
```python
logger = logging.getLogger(__name__)

def load_data(path):
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    
    missing = df.isna().sum().sum()
    if missing > 0:
        logger.warning(f"Found {missing} missing values")
    
    return df
```

Вывод:
```
2024-01-15 10:30:01 | INFO | src.data.load | Loading data from data/raw/heat.csv
2024-01-15 10:30:02 | INFO | src.data.load | Loaded 47232 rows, 9 columns
2024-01-15 10:30:02 | WARNING | src.data.load | Found 150 missing values
```

### .env и python-dotenv — конфигурация окружения

**Проблема с хардкодом:**
```python
df = pd.read_csv("/home/ivan/projects/heatwin/data/raw/data.csv")  # ← ваш путь
API_KEY = "sk-abc123..."                                             # ← секрет в коде!
```

Другой человек клонирует репо — пути не работают. Секрет утёк на GitHub.

**Решение — файл .env:**
```bash
# .env (в корне проекта, НЕ в Git!)
DATA_DIR=data/raw
PROCESSED_DIR=data/processed
MLFLOW_TRACKING_URI=http://localhost:5000
API_KEY=sk-abc123...
```

**.env добавляется в .gitignore:**
```
# .gitignore
.env
```

**Загрузка в Python:**
```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # загружает переменные из .env

data_dir = os.getenv("DATA_DIR", "data/raw")   # второй аргумент = значение по умолчанию
api_key = os.getenv("API_KEY")
```

**Паттерн: .env + .env.example**
```bash
# .env.example (в Git — шаблон без секретов)
DATA_DIR=data/raw
PROCESSED_DIR=data/processed
MLFLOW_TRACKING_URI=http://localhost:5000
API_KEY=<your-api-key-here>
```

Новый человек: копирует `.env.example` → `.env`, заполняет свои значения.

### Type hints — аннотации типов

**Проблема без типов:**
```python
def add_lag(df, column, lag):
    # df — это что? DataFrame? dict? 
    # column — str? int? list?
    # lag — int? float?
    # Что возвращает?
```

**Решение — type hints:**
```python
import pandas as pd

def add_lag(df: pd.DataFrame, column: str, lag: int = 1) -> pd.DataFrame:
    """Add lagged feature to DataFrame."""
    df[f"{column}_lag_{lag}"] = df[column].shift(lag)
    return df
```

Теперь IDE (PyCharm, VSCode) знает:
- `df` — DataFrame → подсказывает методы `.head()`, `.describe()`
- `column` — str → подсвечивает если передали int
- Возвращает DataFrame → следующая функция в цепочке знает тип

**Основные типы:**
```python
from typing import Optional, List, Dict, Tuple, Union

def load_data(path: str) -> pd.DataFrame: ...
def get_columns(df: pd.DataFrame) -> List[str]: ...
def split_data(df: pd.DataFrame, ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]: ...
def find_value(data: Dict[str, float], key: str) -> Optional[float]: ...  # может вернуть None
def process(value: Union[int, float]) -> float: ...  # принимает int ИЛИ float
```

**Type hints НЕ проверяются Python при запуске!** Это подсказки для IDE и разработчика. Для проверки нужен `mypy`:
```bash
pip install mypy
mypy src/  # проверит типы во всех файлах src/
```

**Для DS — минимальный набор:**
```python
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple

def clean_data(
    df: pd.DataFrame, 
    columns: List[str], 
    threshold: float = 0.05
) -> pd.DataFrame:
    """Remove columns with more than threshold fraction of missing values."""
    ...

def train_test_split(
    df: pd.DataFrame, 
    test_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    ...
```

---

## 2.2c Упражнения: logging, .env, type hints

### Упражнение 2.5: Logging в pipeline

**Задание:**
1. Создайте `configs/logging.yaml` (или настройте в коде)
2. Перепишите `src/data/load.py` из упражнения 2.2 с logging:
```python
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def load_csv(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path, parse_dates=['timestamp'])
    logger.info(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    
    missing = df.isna().sum().sum()
    if missing > 0:
        logger.warning(f"Found {missing} missing values across all columns")
    else:
        logger.info("No missing values found")
    
    return df
```
3. Перепишите `src/data/clean.py` с logging:
```python
logger = logging.getLogger(__name__)

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        logger.warning(f"Removed {removed} duplicate rows")
    else:
        logger.info("No duplicates found")
    return df
```
4. Коммит: `refactor: add logging to data modules`

### Упражнение 2.6: .env для путей

**Задание:**
1. Создайте `.env`:
```
DATA_RAW_DIR=data/raw
DATA_PROCESSED_DIR=data/processed
LOG_LEVEL=INFO
```
2. Создайте `.env.example` (копия без секретов — для Git)
3. Добавьте `.env` в `.gitignore`
4. Обновите `src/data/load.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DATA_RAW_DIR = os.getenv("DATA_RAW_DIR", "data/raw")

def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_RAW_DIR, filename)
    logger.info(f"Loading from {path}")
    return pd.read_csv(path)
```
5. Коммит: `config: add .env support with python-dotenv`

### Упражнение 2.7: Type hints

**Задание:**
1. Добавьте type hints ко ВСЕМ функциям в src/:
   - `src/data/load.py`
   - `src/data/clean.py`
   - `src/features/build.py`
   - `src/models/train.py`
2. Пример для features:
```python
import pandas as pd

def add_lag(df: pd.DataFrame, column: str, lag: int = 1) -> pd.DataFrame:
    df[f"{column}_lag_{lag}"] = df[column].shift(lag)
    return df

def add_rolling_mean(df: pd.DataFrame, column: str, window: int = 3) -> pd.DataFrame:
    df[f"{column}_rolling_{window}"] = df[column].rolling(window).mean()
    return df
```
3. Опционально: запустите `mypy src/` и исправьте предупреждения
4. Коммит: `refactor: add type hints to all modules`

---

## 2.3 Финальное задание: Структура HeatWin

**Сделать после всех упражнений:**
1. В репозитории `heatwin` (из урока 1) создать полную структуру по шаблону из phase0_infrastructure.md (задача 0.2)
2. Включая: data/, src/, notebooks/, tests/, configs/, docs/, dashboard/
3. .gitkeep в пустых папках, __init__.py в src/
4. requirements.txt (стартовый набор из phase0_infrastructure.md задача 0.3)
5. Makefile (стартовый из phase0_infrastructure.md задача 0.5)
6. README.md (минимальный: название, описание, структура)
7. Каждое действие — отдельный коммит на ветке `feature/project-structure`
8. Merge в main
9. Push на GitHub

→ Это задачи 0.2, 0.3, 0.5, 0.7 из phase0_infrastructure.md.

---
---

# Урок 3: DVC — версионирование данных

## 3.1 Теория: зачем DVC

### Проблема
Git отлично хранит код (текстовые файлы до ~100 КБ). Но данные:
- Большие (CSV 500 МБ, parquet 1 ГБ)
- Бинарные (Git не может показать diff)
- Не должны быть публичными (приватные данные клиента)

GitHub ограничивает: максимум 100 МБ на файл, 1 ГБ на репо. Ваш dataset не влезет.

### Решение: DVC

DVC = Data Version Control. Принцип:
- **Данные** хранятся в отдельном storage (локальная папка, S3, Google Drive)
- **Метаданные** (.dvc файлы) хранятся в Git
- .dvc файл = маленький текстовый файл с хэшем данных

```
Git repo:                    DVC storage:
  data/raw/data.csv.dvc  →    /storage/ab/cd1234...  (сам файл)
  (200 байт, текст)           (500 МБ, бинарный)
```

Когда кто-то клонирует ваш репо, он получает .dvc файлы. Потом `dvc pull` скачивает данные из storage.

### Как работает

```
1. dvc init              ← инициализация (один раз)
2. dvc add data/raw/     ← DVC начинает отслеживать папку
   → создаёт data/raw.dvc (метаданные)
   → создаёт data/raw/.gitignore (чтобы Git игнорировал данные)
3. git add data/raw.dvc data/raw/.gitignore
   git commit -m "data: track raw data with DVC"
4. dvc push              ← отправить данные в storage
```

При получении:
```
git clone <repo>
dvc pull                 ← скачать данные из storage
```

### DVC remote storage

Remote — где физически лежат данные:
```bash
# Локальная папка (для обучения)
dvc remote add -d storage /path/to/dvc-storage

# Google Drive (для шаринга)
dvc remote add -d gdrive gdrive://folder_id

# Amazon S3
dvc remote add -d s3 s3://my-bucket/data
```

Для пет-проекта достаточно локальной папки.

### Что DVC отслеживает vs Git

| Что | Где хранится | Команда |
|---|---|---|
| .py файлы | Git | git add, git commit |
| .ipynb файлы | Git | git add, git commit |
| requirements.txt | Git | git add, git commit |
| data/raw/*.csv | DVC storage | dvc add, dvc push |
| data/processed/*.parquet | DVC storage | dvc add, dvc push |
| models/*.pkl | DVC storage | dvc add, dvc push |
| .dvc файлы | Git | git add, git commit |

---

## 3.2 Упражнения

### Подготовка данных для упражнений

**Создайте тестовый CSV файл** (или попросите меня подготовить):

```python
# create_test_data.py
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=n, freq='h'),
    'temperature': np.random.normal(20, 5, n),
    'humidity': np.random.normal(60, 10, n),
    'energy': np.abs(np.random.normal(100, 30, n))
})
df.to_csv('data/raw/sensor_data.csv', index=False)
print(f"Created: {len(df)} rows, {df.shape[1]} columns")
```

### Упражнение 3.1: Инициализация DVC

**Задание:**
1. В репозитории из урока 2 (с готовой структурой):
```bash
dvc init
```
2. Посмотрите что создалось: `ls -la .dvc/`
3. Обратите внимание: появились `.dvc/` и `.dvcignore`
4. Коммит в Git:
```bash
git add .dvc .dvcignore
git commit -m "config: initialize DVC"
```

### Упражнение 3.2: Отслеживание данных

**Задание:**
1. Создайте тестовый CSV (скрипт выше) в `data/raw/`
2. Проверьте размер: `ls -lh data/raw/sensor_data.csv`
3. Добавьте в DVC:
```bash
dvc add data/raw/sensor_data.csv
```
4. Посмотрите что создалось:
   - `data/raw/sensor_data.csv.dvc` — метаданные (откройте, посмотрите содержимое)
   - `data/raw/.gitignore` — автоматически добавлен CSV в ignore
5. Коммит метаданных в Git:
```bash
git add data/raw/sensor_data.csv.dvc data/raw/.gitignore
git commit -m "data: add raw sensor data (DVC tracked)"
```

### Упражнение 3.3: Remote storage

**Задание:**
1. Создайте локальный storage:
```bash
mkdir -p /tmp/dvc-storage
dvc remote add -d local_storage /tmp/dvc-storage
```
2. Push данных в storage:
```bash
dvc push
```
3. Проверьте storage: `ls /tmp/dvc-storage/` — появились файлы с хэш-именами
4. Коммит:
```bash
git add .dvc/config
git commit -m "config: add DVC remote storage"
```

### Упражнение 3.4: Воспроизводимость (ключевое)

**Задание:** Проверить что DVC работает для другого человека.
1. Удалите CSV из рабочей папки (имитация клона):
```bash
rm data/raw/sensor_data.csv
ls data/raw/  # файла нет!
```
2. Восстановите из DVC:
```bash
dvc pull
ls data/raw/  # файл вернулся!
```

**Чему учит:** клонирование репо + dvc pull = полное воспроизведение проекта.

### Упражнение 3.5: Обновление данных

**Задание:**
1. Модифицируйте данные (добавьте строки в CSV):
```python
import pandas as pd
df = pd.read_csv('data/raw/sensor_data.csv')
new_row = pd.DataFrame({'timestamp': ['2023-02-11 00:00:00'], 
                         'temperature': [25.0], 'humidity': [55.0], 'energy': [120.0]})
df = pd.concat([df, new_row], ignore_index=True)
df.to_csv('data/raw/sensor_data.csv', index=False)
```
2. `dvc status` — покажет что файл изменился
3. Обновите DVC:
```bash
dvc add data/raw/sensor_data.csv
git add data/raw/sensor_data.csv.dvc
git commit -m "data: update sensor data with new records"
dvc push
```

**Чему учит:** при обновлении данных → dvc add → git commit → dvc push. Обе истории (кода и данных) синхронизированы.

---

---

## 3.2b Теория: DVC Pipelines (dvc.yaml, dvc repro)

### Проблема с Makefile для данных

Makefile знает: «если запустить `make features`, выполнится `python src/features/build.py`». Но Makefile НЕ знает:
- Изменились ли входные данные с прошлого запуска?
- Изменился ли код с прошлого запуска?
- Нужно ли пересобирать features, если raw data не менялся?

Вы запускаете `make pipeline` — он пересчитывает ВСЁ каждый раз, даже если ничего не изменилось. На больших данных это часы.

### Решение: DVC Pipelines

DVC pipeline = DAG из шагов (stages). Каждый шаг знает:
- **deps** (dependencies) — от чего зависит (данные + код)
- **cmd** — что запустить
- **outs** — что создаёт
- **metrics** — что измерять (MAE, RMSE)

DVC автоматически определяет: что изменилось → какие шаги нужно перезапустить → пропускает неизменившиеся.

### dvc.yaml — описание pipeline

```yaml
stages:
  clean:
    cmd: python src/data/clean.py
    deps:
      - src/data/clean.py          # если код изменится → пересчитать
      - data/raw/heat_data.csv     # если данные изменятся → пересчитать
    outs:
      - data/interim/clean.parquet # что создаёт этот шаг

  features:
    cmd: python src/features/build.py --config configs/params.yaml
    deps:
      - src/features/build.py
      - data/interim/clean.parquet  # зависит от выхода clean
      - configs/params.yaml         # если параметры изменятся → пересчитать
    outs:
      - data/processed/features.parquet

  split:
    cmd: python src/data/split.py
    deps:
      - src/data/split.py
      - data/processed/features.parquet
    outs:
      - data/processed/train.parquet
      - data/processed/test.parquet

  train:
    cmd: python src/models/train.py
    deps:
      - src/models/train.py
      - data/processed/train.parquet
    outs:
      - models/model.pkl
    metrics:
      - metrics/scores.json:
          cache: false              # метрики не кэшировать — всегда текстовые
```

### dvc repro — запуск pipeline

```bash
dvc repro              # запустить весь pipeline
```

DVC проверяет хэши всех deps и outs. Если ничего не изменилось — `Stage 'clean' didn't change, skipping`. Если изменился только `params.yaml` — пересчитает features, split, train, но не clean.

```bash
dvc repro train        # запустить только шаг train (и все его зависимости если изменились)
```

### dvc dag — визуализация pipeline

```bash
dvc dag
```
Выводит:
```
+-------+
| clean |
+-------+
     *
     *
+----------+
| features |
+----------+
     *
     *
+-------+
| split |
+-------+
     *
     *
+-------+
| train |
+-------+
```

### dvc params — управление параметрами

Файл `configs/params.yaml`:
```yaml
clean:
  outlier_method: iqr
  outlier_threshold: 1.5

features:
  horizon: 6
  lags: [1, 3, 6, 12, 24]
  rolling_windows: [3, 6, 12, 24]

split:
  test_ratio: 0.2
  
train:
  model: lightgbm
  n_estimators: 1000
  learning_rate: 0.05
```

В Python:
```python
import yaml

with open("configs/params.yaml") as f:
    params = yaml.safe_load(f)

horizon = params["features"]["horizon"]  # 6
lags = params["features"]["lags"]        # [1, 3, 6, 12, 24]
```

Если изменить `horizon: 6` → `horizon: 12` и запустить `dvc repro`, DVC пересчитает features → split → train, но не clean (clean не зависит от params).

### dvc metrics — отслеживание результатов

Шаг train записывает `metrics/scores.json`:
```json
{"mae": 1.73, "rmse": 2.41, "r2": 0.912}
```

```bash
dvc metrics show       # показать текущие метрики
dvc metrics diff       # сравнить с предыдущим запуском
```

Вывод `dvc metrics diff`:
```
Path                mae    rmse    r2
metrics/scores.json 1.73   2.41    0.912
                    (-0.2) (-0.3)  (+0.02)
```

### DVC pipeline vs Makefile

| | Makefile | DVC Pipeline |
|---|---|---|
| Знает об изменениях | Нет — пересчитывает всё | Да — пропускает неизменившееся |
| Отслеживает данные | Нет | Да (хэши файлов) |
| Метрики | Нет | dvc metrics show/diff |
| Параметры | Вручную | dvc params diff |
| Визуализация DAG | Нет | dvc dag |
| Сложность | Минимальная | Нужно описать dvc.yaml |

**Рекомендация для HeatWin:** начать с Makefile (фаза 0-2), перейти на DVC pipeline когда появится полный pipeline clean → features → train (фаза 3-4).

---

## 3.2c Упражнения: DVC Pipelines

### Упражнение 3.6: Простой pipeline из двух шагов

**Задание:**
1. Создайте два скрипта:

`src/data/clean.py`:
```python
import pandas as pd
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean(input_path: str, output_path: str) -> None:
    logger.info(f"Cleaning {input_path}")
    df = pd.read_csv(input_path)
    
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna()
    logger.info(f"Cleaned: {before} → {len(df)} rows")
    
    df.to_parquet(output_path, index=False)
    logger.info(f"Saved to {output_path}")

if __name__ == "__main__":
    clean("data/raw/sensor_data.csv", "data/interim/clean.parquet")
```

`src/features/build.py`:
```python
import pandas as pd
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_features(input_path: str, output_path: str, params_path: str) -> None:
    with open(params_path) as f:
        params = yaml.safe_load(f)
    
    df = pd.read_parquet(input_path)
    
    for lag in params["features"]["lags"]:
        df[f"temperature_lag_{lag}"] = df["temperature"].shift(lag)
        logger.info(f"Added lag {lag}")
    
    df = df.dropna()
    df.to_parquet(output_path, index=False)
    logger.info(f"Features built: {df.shape[1]} columns, {len(df)} rows → {output_path}")

if __name__ == "__main__":
    build_features("data/interim/clean.parquet", "data/processed/features.parquet", "configs/params.yaml")
```

2. Создайте `configs/params.yaml`:
```yaml
features:
  lags: [1, 3, 6, 12, 24]
```

3. Создайте `dvc.yaml`:
```yaml
stages:
  clean:
    cmd: python src/data/clean.py
    deps:
      - src/data/clean.py
      - data/raw/sensor_data.csv
    outs:
      - data/interim/clean.parquet

  features:
    cmd: python src/features/build.py
    deps:
      - src/features/build.py
      - data/interim/clean.parquet
      - configs/params.yaml
    outs:
      - data/processed/features.parquet
```

4. Запустите: `dvc repro`
5. Посмотрите DAG: `dvc dag`
6. Запустите ещё раз: `dvc repro` — оба шага будут пропущены (ничего не изменилось)
7. Измените `lags: [1, 3, 6, 12, 24]` → `lags: [1, 6, 24]` в params.yaml
8. Запустите `dvc repro` — clean пропущен, features пересчитан
9. Коммит:
```bash
git add dvc.yaml dvc.lock configs/params.yaml src/
git commit -m "feat: add DVC pipeline (clean → features)"
```

### Упражнение 3.7: Метрики

**Задание:**
1. Добавьте шаг `evaluate` в `dvc.yaml`:
```yaml
  evaluate:
    cmd: python src/models/evaluate.py
    deps:
      - src/models/evaluate.py
      - data/processed/features.parquet
    metrics:
      - metrics/scores.json:
          cache: false
```

2. Создайте `src/models/evaluate.py`:
```python
import pandas as pd
import json
import os

def evaluate(features_path: str, metrics_path: str) -> None:
    df = pd.read_parquet(features_path)
    
    # Простая "оценка" — описательные статистики как метрики
    scores = {
        "n_rows": int(len(df)),
        "n_features": int(df.shape[1]),
        "temperature_mean": round(float(df["temperature"].mean()), 2),
        "temperature_std": round(float(df["temperature"].std()), 2),
    }
    
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        json.dump(scores, f, indent=2)
    print(f"Metrics saved: {scores}")

if __name__ == "__main__":
    evaluate("data/processed/features.parquet", "metrics/scores.json")
```

3. Запустите `dvc repro`
4. Посмотрите метрики: `dvc metrics show`
5. Измените параметры → `dvc repro` → `dvc metrics diff`
6. Коммит: `feat: add metrics tracking to DVC pipeline`

---

## 3.3 Финальное задание: DVC для HeatWin

**Сделать после всех упражнений:**
1. В репозитории `heatwin`: `dvc init` + настроить local remote
2. Коммит: `config: initialize DVC`
3. Когда скачаете XAI4HEAT: `dvc add data/raw/` → коммит .dvc файлов

→ Это задача 0.4 из phase0_infrastructure.md.

---
---

# Урок 4: Pandera — валидация данных

## 4.1 Теория: зачем валидация

### Проблема
Вы написали feature pipeline. Он работает на тестовых данных. Через неделю приходят новые данные — и pipeline падает. Почему?
- Новый столбец пропущен (источник изменил формат)
- Temperature = -999 (датчик сломался)
- Energy отрицательный (ошибка знака)
- Дата в неправильном формате

Вы узнаёте об этом через 3 шага pipeline, когда модель выдаёт NaN. Дебаг: 2 часа.

### Решение: декларативная валидация

Вместо ручных проверок (`assert`, `if`) — описываете **схему** данных один раз. Pipeline проверяет данные автоматически на входе и выходе каждого шага.

### Pandera vs Great Expectations

| | Pandera | Great Expectations |
|---|---|---|
| Размер | Лёгкий, одна библиотека | Тяжёлый фреймворк |
| Для кого | DS, pandas-проекты | Data Engineering, production |
| API | Python-native (DataFrameSchema) | JSON-конфигурации |
| Интеграция | pip install pandera, готово | Настройка проекта, store, datasources |
| Когда | Пет-проект, пайплайн | Enterprise, сотни таблиц |

Для HeatWin — Pandera.

### Основные концепции

**DataFrameSchema** — описание структуры DataFrame:
- Какие колонки должны быть
- Какого типа каждая колонка
- Допустимые диапазоны значений
- Могут ли быть пропуски
- Любые кастомные проверки

**Column** — описание одной колонки:
```python
import pandera as pa

schema = pa.DataFrameSchema({
    "temperature": pa.Column(float, pa.Check.in_range(-50, 50)),
    "energy": pa.Column(float, pa.Check.ge(0)),  # >= 0
    "substation": pa.Column(str, pa.Check.isin(["L4", "L8", "L12"])),
})
```

**Check** — отдельная проверка:
```python
pa.Check.ge(0)              # >= 0
pa.Check.le(100)            # <= 100
pa.Check.in_range(0, 100)   # 0 <= x <= 100
pa.Check.isin(["A", "B"])   # одно из значений
pa.Check.str_matches(r"L\d+")  # regex
pa.Check(lambda s: s.mean() > 0, error="Mean must be positive")  # кастомная
```

**Валидация:**
```python
validated_df = schema.validate(df)  # бросает SchemaError если не проходит
```

Или мягкая валидация:
```python
schema.validate(df, lazy=True)  # собирает ВСЕ ошибки, не останавливается на первой
```

### Паттерн использования в pipeline

```python
# Схема для raw data
raw_schema = pa.DataFrameSchema({...})

# Схема для processed data (после feature engineering)
processed_schema = pa.DataFrameSchema({...})

def pipeline(raw_path, output_path):
    df = pd.read_csv(raw_path)
    df = raw_schema.validate(df)          # проверяем вход
    
    df = clean(df)
    df = build_features(df)
    
    df = processed_schema.validate(df)     # проверяем выход
    df.to_parquet(output_path)
```

Если данные не проходят валидацию — pipeline падает с понятной ошибкой **до** того, как испортит модель.

---

## 4.2 Упражнения

### Подготовка

```bash
pip install pandera
```

### Упражнение 4.1: Первая схема

**Задание:**
1. Создайте файл `src/data/validate.py`
2. Опишите схему для sensor_data.csv (из урока 3):

```python
import pandera as pa

sensor_schema = pa.DataFrameSchema({
    "timestamp": pa.Column(str),  # пока строка, позже datetime
    "temperature": pa.Column(float, [
        pa.Check.in_range(-50, 60, error="Temperature out of physical range")
    ]),
    "humidity": pa.Column(float, [
        pa.Check.in_range(0, 100, error="Humidity must be 0-100%")
    ]),
    "energy": pa.Column(float, [
        pa.Check.ge(0, error="Energy cannot be negative")
    ]),
})
```

3. Протестируйте на правильных данных:
```python
import pandas as pd
df = pd.read_csv("data/raw/sensor_data.csv")
validated = sensor_schema.validate(df)
print("Validation passed!")
```

4. Коммит: `feat: add data validation schema`

### Упражнение 4.2: Сломать и поймать

**Задание:**
1. Создайте «плохой» DataFrame:
```python
bad_df = pd.DataFrame({
    "timestamp": ["2023-01-01", "2023-01-02"],
    "temperature": [20.0, -999.0],    # ← ошибка датчика!
    "humidity": [60.0, 150.0],         # ← больше 100%!
    "energy": [100.0, -50.0],          # ← отрицательный!
})
```
2. Валидируйте с `lazy=True`:
```python
try:
    sensor_schema.validate(bad_df, lazy=True)
except pa.errors.SchemaErrors as err:
    print(err.failure_cases)
```
3. Вы увидите ВСЕ ошибки одновременно, а не по одной

**Чему учит:** lazy=True — отладка. Без lazy — production (падает на первой ошибке).

### Упражнение 4.3: Кастомные проверки

**Задание:** Добавьте проверку, которую нельзя выразить стандартными Check:

```python
# Проверка: температура не должна быть «замёрзшей» (std = 0 на окне 24 строк)
def check_not_frozen(series):
    rolling_std = series.rolling(24, min_periods=24).std()
    return rolling_std.dropna().gt(0).all()

enhanced_schema = pa.DataFrameSchema({
    "temperature": pa.Column(float, [
        pa.Check.in_range(-50, 60),
        pa.Check(check_not_frozen, error="Sensor appears frozen (std=0 for 24h)")
    ]),
    # ...остальные колонки
})
```

### Упражнение 4.4: Схема для теплоснабжения (приближение к HeatWin)

**Задание:** Создайте схему для данных теплоснабжения.

Подготовьте данные (или попросите меня):
```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 500
T_outdoor = np.random.normal(-5, 10, n)
T_supply = 80 - 0.5 * T_outdoor + np.random.normal(0, 2, n)
T_return = T_supply - np.random.uniform(15, 25, n)
energy = np.maximum(0, (T_supply - T_return) * 10 + np.random.normal(0, 20, n))

heat_df = pd.DataFrame({
    'timestamp': pd.date_range('2023-10-01', periods=n, freq='h'),
    'substation': np.random.choice(['L4', 'L8', 'L12'], n),
    'T_supply_primary': T_supply,
    'T_return_primary': T_return,
    'T_outdoor': T_outdoor,
    'energy_kWh': energy,
})
heat_df.to_csv('data/raw/heat_data.csv', index=False)
```

Напишите схему:
```python
heat_schema = pa.DataFrameSchema({
    "timestamp": pa.Column(str),
    "substation": pa.Column(str, pa.Check.isin(["L4", "L8", "L12", "L17", "L22"])),
    "T_supply_primary": pa.Column(float, pa.Check.in_range(40, 130)),
    "T_return_primary": pa.Column(float, pa.Check.in_range(20, 100)),
    "T_outdoor": pa.Column(float, pa.Check.in_range(-50, 45)),
    "energy_kWh": pa.Column(float, pa.Check.ge(0)),
})

# Бонус: cross-column check — T_return < T_supply
heat_schema_with_cross = heat_schema.add_columns({}).update_columns({})
# Pandera позволяет добавить DataFrame-level check:
heat_schema_full = pa.DataFrameSchema(
    columns=heat_schema.columns,
    checks=[
        pa.Check(
            lambda df: (df["T_return_primary"] < df["T_supply_primary"]).all(),
            error="T_return must be less than T_supply"
        )
    ]
)
```

Протестируйте на правильных и неправильных данных.

### Упражнение 4.5: Интеграция в pipeline

**Задание:** Создайте мини-pipeline с валидацией на входе и выходе:

```python
# src/data/pipeline.py
import pandas as pd
from src.data.validate import raw_schema, processed_schema

def load_and_validate(path):
    df = pd.read_csv(path)
    return raw_schema.validate(df)

def add_features(df):
    df['T_delta'] = df['T_supply_primary'] - df['T_return_primary']
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    return df

def run_pipeline(input_path, output_path):
    df = load_and_validate(input_path)      # валидация входа
    df = add_features(df)
    df = processed_schema.validate(df)       # валидация выхода
    df.to_parquet(output_path)
    print(f"Pipeline complete: {len(df)} rows → {output_path}")
```

Добавьте `processed_schema` — расширение raw_schema с проверками новых колонок (T_delta > 0, hour in 0-23).

---

---

## 4.2b Теория: декораторы и schema inference

### Проблема с ручной валидацией

В упражнении 4.5 мы писали:
```python
def run_pipeline(input_path, output_path):
    df = load_and_validate(input_path)
    df = raw_schema.validate(df)        # ← вручную
    df = add_features(df)
    df = processed_schema.validate(df)   # ← вручную
    df.to_parquet(output_path)
```

Каждая функция должна помнить: «сначала валидируй». Если забыли — невалидные данные пойдут дальше. Если 10 функций в pipeline — 10 мест где можно забыть.

### Решение: декораторы @check_input / @check_output

Декоратор — это обёртка вокруг функции. Pandera добавляет валидацию автоматически:

```python
import pandera as pa

input_schema = pa.DataFrameSchema({
    "temperature": pa.Column(float, pa.Check.in_range(-50, 60)),
    "energy": pa.Column(float, pa.Check.ge(0)),
})

output_schema = pa.DataFrameSchema({
    "temperature": pa.Column(float, pa.Check.in_range(-50, 60)),
    "energy": pa.Column(float, pa.Check.ge(0)),
    "temp_lag_1": pa.Column(float, nullable=True),  # NaN допустим из-за shift
})

@pa.check_input(input_schema)
@pa.check_output(output_schema)
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df["temp_lag_1"] = df["temperature"].shift(1)
    return df
```

Теперь при каждом вызове `add_features(df)`:
1. Pandera сначала проверяет df по input_schema
2. Функция выполняется
3. Pandera проверяет результат по output_schema
4. Если что-то не проходит — SchemaError до того, как плохие данные пойдут дальше

**Вам не нужно помнить** про validate() — декоратор делает это за вас.

### Несколько аргументов

Если функция принимает несколько DataFrame:
```python
@pa.check_input(schema_a, "df_train")   # валидировать аргумент df_train
@pa.check_input(schema_b, "df_test")    # и аргумент df_test
def train_model(df_train: pd.DataFrame, df_test: pd.DataFrame, params: dict):
    ...
```

Второй аргумент декоратора — имя параметра функции, который нужно проверить.

### @pa.check_types — через аннотации типов

Более новый подход (Pandera >= 0.13):
```python
from pandera.typing import DataFrame

class InputSchema(pa.DataFrameModel):
    temperature: float = pa.Field(ge=-50, le=60)
    energy: float = pa.Field(ge=0)

class OutputSchema(pa.DataFrameModel):
    temperature: float = pa.Field(ge=-50, le=60)
    energy: float = pa.Field(ge=0)
    temp_lag_1: float = pa.Field(nullable=True)

@pa.check_types
def add_features(df: DataFrame[InputSchema]) -> DataFrame[OutputSchema]:
    df["temp_lag_1"] = df["temperature"].shift(1)
    return df
```

Здесь type hints **и** валидация в одном месте. IDE видит типы, Pandera проверяет данные.

### Schema inference — генерация схемы из данных

Вместо написания схемы вручную — Pandera анализирует DataFrame и генерирует схему автоматически:

```python
import pandera as pa
import pandas as pd

df = pd.read_csv("data/raw/heat_data.csv")
schema = pa.infer_schema(df)
print(schema)
```

Вывод:
```python
DataFrameSchema(
    columns={
        "timestamp": Column(dtype=object, ...),
        "substation": Column(dtype=object, checks=[Check.isin(["L4","L8","L12"])], ...),
        "T_supply_primary": Column(dtype=float64, checks=[Check.in_range(62.1, 98.7)], ...),
        "T_return_primary": Column(dtype=float64, checks=[Check.in_range(41.3, 78.2)], ...),
        ...
    }
)
```

Pandera выводит: типы колонок, диапазоны значений, допустимые категории. Но диапазоны берёт **из данных** — минимум и максимум текущего DataFrame. Это значит:
- Если в текущих данных T_outdoor от -20 до +15 — схема поставит этот диапазон
- Но в новых данных может быть -35 — и валидация упадёт

**Поэтому infer_schema — это СТАРТОВАЯ ТОЧКА, не финальная.** Процесс:
1. `schema = pa.infer_schema(df)` — получить автосхему
2. Сохранить: `schema.to_yaml("configs/raw_schema.yaml")` или записать как Python-код
3. Вручную отредактировать: расширить диапазоны до физически допустимых, добавить cross-column checks
4. Использовать отредактированную схему в pipeline

### Сохранение и загрузка схемы

```python
# Сохранить в YAML
schema.to_yaml("configs/raw_schema.yaml")

# Загрузить из YAML
loaded_schema = pa.DataFrameSchema.from_yaml("configs/raw_schema.yaml")
```

Или в Python-скрипте:
```python
# Сохранить как Python-код
print(schema.to_script())
# → Выводит Python-код DataFrameSchema(...) который можно скопировать в validate.py
```

---

## 4.2c Упражнения: декораторы и inference

### Упражнение 4.6: Schema inference

**Задание:**
1. Загрузите heat_data.csv из упражнения 4.4
2. Инфератируйте схему:
```python
import pandera as pa
import pandas as pd

df = pd.read_csv("data/raw/heat_data.csv")
auto_schema = pa.infer_schema(df)
print(auto_schema)
```
3. Обратите внимание на диапазоны — они слишком узкие (только текущие данные)
4. Экспортируйте: `print(auto_schema.to_script())`
5. Скопируйте вывод в `src/data/validate.py`
6. Вручную отредактируйте:
   - T_supply_primary: расширить до `[40, 130]` (физический диапазон)
   - T_return_primary: расширить до `[20, 100]`
   - T_outdoor: расширить до `[-50, 45]`
   - Добавить cross-column check: T_return < T_supply
7. Коммит: `feat: generate and refine data schema with pandera inference`

### Упражнение 4.7: Декоратор @check_input

**Задание:**
1. Перепишите `src/features/build.py` с декоратором:
```python
import pandera as pa
import pandas as pd
from src.data.validate import heat_schema  # ваша отредактированная схема

feature_schema = pa.DataFrameSchema({
    **heat_schema.columns,  # все колонки из raw + новые:
    "T_delta": pa.Column(float, pa.Check.gt(0)),
    "hour": pa.Column(int, pa.Check.in_range(0, 23)),
})

@pa.check_input(heat_schema)       # проверить вход
@pa.check_output(feature_schema)   # проверить выход
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df["T_delta"] = df["T_supply_primary"] - df["T_return_primary"]
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    return df
```

2. Протестируйте: вызовите `add_features(df)` с правильным и неправильным DataFrame
3. Убедитесь: при неправильных данных ошибка происходит **при вызове функции**, не внутри pipeline
4. Коммит: `feat: add pandera decorators to feature pipeline`

### Упражнение 4.8: DataFrameModel (class-based schema)

**Задание:**
1. Перепишите схему в class-based стиле:
```python
import pandera as pa
from pandera.typing import DataFrame, Series

class HeatRawSchema(pa.DataFrameModel):
    timestamp: Series[str]
    substation: Series[str] = pa.Field(isin=["L4", "L8", "L12", "L17", "L22"])
    T_supply_primary: Series[float] = pa.Field(ge=40, le=130)
    T_return_primary: Series[float] = pa.Field(ge=20, le=100)
    T_outdoor: Series[float] = pa.Field(ge=-50, le=45)
    energy_kWh: Series[float] = pa.Field(ge=0)

    @pa.check("T_return_primary")
    def return_less_than_supply(cls, series: Series[float]) -> Series[bool]:
        # Для cross-column нужен доступ к другим колонкам — используем dataframe check:
        return True  # placeholder

    @pa.dataframe_check
    def return_less_than_supply_df(cls, df: pd.DataFrame) -> bool:
        return (df["T_return_primary"] < df["T_supply_primary"]).all()

class HeatFeaturesSchema(HeatRawSchema):  # наследует все проверки raw +
    T_delta: Series[float] = pa.Field(gt=0)
    hour: Series[int] = pa.Field(ge=0, le=23)
```

2. Используйте с `@pa.check_types`:
```python
@pa.check_types
def add_features(df: DataFrame[HeatRawSchema]) -> DataFrame[HeatFeaturesSchema]:
    df["T_delta"] = df["T_supply_primary"] - df["T_return_primary"]
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    return df
```

3. Оцените: чем class-based лучше? (Наследование, type hints + валидация в одном месте)
4. Коммит: `refactor: migrate to class-based Pandera schemas`

---

## 4.3 Финальное задание: Pandera для HeatWin

**Сделать после всех упражнений:**
1. В `heatwin/src/data/validate.py` — создать `raw_schema` для XAI4HEAT данных
2. Включить все проверки из phase2 задача 2.4: T_return < T_supply, energy >= 0, T_outdoor in [-50, 45], substations in [L4, L8, L12, L17, L22]
3. Добавить в Makefile: `make validate` → `python src/data/validate.py`
4. Коммит: `feat: add Pandera validation schema for raw data`

→ Это часть задач 0.4 и 2.4 из наших чеклистов.

---
---

# Итоговый чеклист: все 4 урока пройдены

## Урок 1: Git
- [ ] Упр. 1.1: первый репозиторий (init, add, commit)
- [ ] Упр. 1.2: цикл изменений (staging, два коммита)
- [ ] Упр. 1.3: .gitignore
- [ ] Упр. 1.4: ветки и merge
- [ ] Упр. 1.5: remote (GitHub)
- [ ] Упр. 1.6: полный workflow
- [ ] Финальное: heatwin repo создан на GitHub

## Урок 2: Структура проекта + logging + .env + type hints
- [ ] Упр. 2.1: создать структуру вручную
- [ ] Упр. 2.2: разложить код по папкам
- [ ] Упр. 2.3: notebook импортирует из src/
- [ ] Упр. 2.4: Makefile работает
- [ ] Упр. 2.5: logging в pipeline (замена print → logger)
- [ ] Упр. 2.6: .env для путей (dotenv + .env.example)
- [ ] Упр. 2.7: type hints для всех функций в src/
- [ ] Финальное: heatwin структура создана, push на GitHub

## Урок 3: DVC + Pipelines
- [ ] Упр. 3.1: dvc init
- [ ] Упр. 3.2: dvc add (отслеживание данных)
- [ ] Упр. 3.3: remote storage
- [ ] Упр. 3.4: воспроизводимость (удалить → dvc pull)
- [ ] Упр. 3.5: обновление данных
- [ ] Упр. 3.6: dvc.yaml pipeline из двух шагов (clean → features)
- [ ] Упр. 3.7: dvc metrics (scores.json, dvc metrics show/diff)
- [ ] Финальное: heatwin DVC настроен

## Урок 4: Pandera + декораторы + inference
- [ ] Упр. 4.1: первая схема
- [ ] Упр. 4.2: сломать и поймать (lazy=True)
- [ ] Упр. 4.3: кастомные проверки
- [ ] Упр. 4.4: схема для теплоснабжения
- [ ] Упр. 4.5: интеграция в pipeline
- [ ] Упр. 4.6: schema inference (infer → export → refine)
- [ ] Упр. 4.7: декоратор @check_input / @check_output
- [ ] Упр. 4.8: DataFrameModel (class-based + @check_types)
- [ ] Финальное: heatwin validate.py создан

## Результат после всех уроков
На GitHub в репозитории heatwin:
- Чистая commit history (15+ осмысленных коммитов)
- Полная структура проекта (cookiecutter)
- DVC инициализирован
- Pandera-схема для raw data
- Makefile с базовыми командами
- README.md
- .gitignore настроен

→ Фаза 0 из phase0_infrastructure.md **выполнена**. Можно переходить к фазе 1 (заполнение Project Brief).
