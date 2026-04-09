# Фаза 0: Инженерная инфраструктура проекта

## Что это и зачем

Перед началом любой аналитической работы (до фазы 1) нужно настроить «кухню» — инструменты, структуру, правила. Это делается один раз и используется на всех фазах.

**Источник:** не из CRISP-DM (он описывает только аналитическую работу). Из практик Software Engineering, MLOps, и реальных требований к DS-портфолио и вакансиям 2024-2025. Отсутствие этой фазы — причина, по которой технически сильные проекты выглядят как «ещё один Jupyter Notebook» на GitHub.

**Когда делаем:** до начала фазы 1 (Project Brief). Занимает 2-4 часа.

---

## Задача 0.1: Git-репозиторий

### Что делаем
- `git init` или создать репо на GitHub/GitLab
- Настроить .gitignore (данные, кэши, виртуальное окружение, IDE-файлы)
- Первый commit: пустая структура + README
- Определить branching strategy

### Правила Git для проекта

#### Commits
- Осмысленные сообщения, не «fix» или «update»
- Формат: `<тип>: <что сделано>` — примеры:
  - `init: project structure and README`
  - `docs: add Project Brief v1.0`
  - `eda: add distribution analysis for T_return`
  - `feat: add lag features (1h-24h) for T_return`
  - `fix: correct data leakage in walk-forward split`
  - `test: add leakage check for feature pipeline`
- Типы: init, docs, eda, feat, fix, test, refactor, config

#### Branches
Для пет-проекта достаточно простой модели:
- `main` — стабильная версия, только через merge
- `feature/<name>` — для каждой задачи (feature/lag-features, feature/eda-dashboard)
- Merge через Pull Request (даже для себя — привычка и документация)

#### .gitignore (шаблон для DS-проекта)
```
# Data (tracked by DVC)
data/raw/
data/processed/
data/interim/
*.csv
*.parquet
*.pkl
!data/.gitkeep

# DVC
/storage

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# MLflow
mlruns/

# Profiling reports
*.html
!docs/*.html
```

### Чеклист готовности
- [ ] Репозиторий создан (GitHub/GitLab)
- [ ] .gitignore настроен по шаблону выше
- [ ] Первый commit сделан с осмысленным сообщением
- [ ] README.md создан (пока минимальный — название, описание, автор)
- [ ] Решено: public или private репо

---

## Задача 0.2: Структура проекта

### Что делаем
Создать стандартную структуру на основе Cookiecutter Data Science (де-факто стандарт).

### Структура

```
heatwin/
│
├── README.md                    ← Главная страница проекта
├── LICENSE
├── requirements.txt             ← Зависимости Python
├── Makefile                     ← Команды: make data, make eda, make features
├── Dockerfile                   ← Воспроизводимость среды (опционально)
├── setup.py или pyproject.toml  ← Если оформляем как пакет (опционально)
│
├── configs/                     ← Конфигурации и параметры
│   ├── params.yaml              ← Параметры pipeline (horizon, lags, windows)
│   └── logging.yaml             ← Настройки логирования
│
├── data/                        ← Данные (НЕ в Git — через DVC)
│   ├── raw/                     ← Исходные данные (XAI4HEAT CSV)
│   ├── interim/                 ← Промежуточные (после очистки)
│   ├── processed/               ← Финальные (после feature engineering)
│   └── .gitkeep                 ← Чтобы Git сохранил пустые папки
│
├── docs/                        ← Документация
│   ├── project_brief.md         ← Project Brief (фаза 1)
│   ├── eda_summary_report.pdf   ← EDA Summary для клиента (фаза 2)
│   ├── gate_review.md           ← Gate Review (между ф.2 и ф.3)
│   ├── feature_dictionary.md    ← Словарь признаков (фаза 3)
│   └── literature.md            ← Список литературы
│
├── notebooks/                   ← Jupyter Notebooks (exploration)
│   ├── 01_data_collection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation.ipynb
│
├── src/                         ← Исходный код (production-ready)
│   ├── __init__.py
│   ├── data/                    ← Загрузка и очистка
│   │   ├── __init__.py
│   │   ├── load.py              ← Загрузка XAI4HEAT CSV
│   │   ├── clean.py             ← Очистка (пропуски, выбросы)
│   │   └── validate.py          ← Pandera-схемы валидации
│   ├── features/                ← Feature engineering
│   │   ├── __init__.py
│   │   ├── build_features.py    ← Основной pipeline
│   │   ├── lags.py              ← Лаговые features
│   │   ├── calendar.py          ← Календарные features
│   │   └── climate.py           ← Климатическая память (HDD)
│   ├── models/                  ← Обучение и inference
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   └── visualization/           ← Графики для отчётов
│       ├── __init__.py
│       └── plots.py
│
├── tests/                       ← Тесты
│   ├── test_data_validation.py  ← Тесты Pandera-схем
│   ├── test_features.py         ← Тесты на leakage, NaN
│   └── test_pipeline.py         ← Интеграционные тесты pipeline
│
├── dashboard/                   ← Streamlit EDA-дашборд
│   ├── app.py                   ← Главная страница
│   └── pages/                   ← Multipage app
│       ├── 01_overview.py
│       ├── 02_distributions.py
│       ├── 03_correlations.py
│       ├── 04_temporal.py
│       └── 05_executive.py
│
└── dvc.yaml                     ← DVC pipeline definition (опционально)
```

### Зачем именно такая структура
- `data/` отделена от `src/` — данные не в Git (через DVC)
- `notebooks/` отделены от `src/` — notebooks для исследования, src для production кода
- `docs/` — все документы проекта в одном месте (Project Brief, Gate Review, литература)
- `tests/` — привычка писать тесты, даже минимальные
- `dashboard/` — отдельно от notebooks, потому что это deployable приложение
- Нумерация notebooks (01_, 02_) — порядок выполнения очевиден

### Чеклист готовности
- [ ] Все папки созданы (пустые — с .gitkeep)
- [ ] README.md содержит: название, описание, структуру, как запустить
- [ ] requirements.txt создан (пока базовый: pandas, numpy, matplotlib, seaborn, scipy)
- [ ] Commit: `init: project structure and README`

---

## Задача 0.3: Виртуальное окружение и requirements.txt

### Что делаем
- Создать виртуальное окружение (venv или conda)
- Установить базовые библиотеки
- Зафиксировать версии в requirements.txt

### requirements.txt (стартовый)
```
# Data
pandas>=2.1
numpy>=1.24
pyarrow>=14.0

# Visualization
matplotlib>=3.8
seaborn>=0.13
plotly>=5.18

# Statistics
scipy>=1.11

# Profiling
ydata-profiling>=4.6

# Validation
pandera>=0.18

# Dashboard
streamlit>=1.29

# Notebook
jupyter>=1.0
ipykernel>=6.27

# ML (добавится в фазе 3-4)
# scikit-learn>=1.3
# lightgbm>=4.1
# xgboost>=2.0
# shap>=0.44
# optuna>=3.4

# Experiment tracking (добавится в фазе 3)
# mlflow>=2.9

# Data versioning (опционально)
# dvc>=3.30
```

### Чеклист готовности
- [ ] Виртуальное окружение создано (python -m venv .venv или conda create)
- [ ] Базовые библиотеки установлены
- [ ] requirements.txt зафиксирован с версиями
- [ ] Commit: `config: add requirements.txt`

---

## Задача 0.4: DVC — версионирование данных (рекомендуется)

### Что делаем
- `dvc init` внутри Git-репозитория
- Настроить remote storage (для пет-проекта — локальная папка или Google Drive)
- `dvc add data/raw/` — отслеживать исходные данные
- Commit .dvc файлы в Git

### Базовые команды
```bash
# Инициализация
dvc init
git add .dvc .dvcignore
git commit -m "config: initialize DVC"

# Добавить данные
dvc add data/raw/xai4heat_scada_L4.csv
dvc add data/raw/xai4heat_scada_L8.csv
# ...
git add data/raw/*.dvc data/raw/.gitignore
git commit -m "data: add raw XAI4HEAT SCADA files (DVC tracked)"

# Remote (для шаринга — опционально)
dvc remote add -d storage /path/to/dvc-storage
dvc push
```

### Когда использовать dvc add в проекте
| Момент | Что добавляем | Команда |
|---|---|---|
| Фаза 0 (сейчас) | Пустая структура | `dvc init` |
| Фаза 2 (EDA) | Raw data (XAI4HEAT CSV) | `dvc add data/raw/` |
| Фаза 3 (Prep) | Processed data (после cleaning + FE) | `dvc add data/processed/` |
| Фаза 4 (Model) | Модели (pickle/joblib) | `dvc add models/` |

### Чеклист готовности
- [ ] `dvc init` выполнен
- [ ] .dvc и .dvcignore закоммичены
- [ ] Remote настроен (хотя бы локальный)
- [ ] Понимаю: dvc add → .dvc файл в Git → данные в storage

---

## Задача 0.5: Makefile (рекомендуется)

### Что делаем
Создать Makefile с командами для каждого этапа работы.

### Makefile (стартовый)
```makefile
.PHONY: setup data eda features split profile test dashboard clean

## Setup environment
setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

## Download / load raw data
data:
	python src/data/load.py

## Run EDA notebook (non-interactive)
eda:
	jupyter nbconvert --execute notebooks/02_eda.ipynb --to html --output-dir=docs/

## Generate auto-profile
profile-raw:
	python -c "import ydata_profiling; import pandas as pd; \
	df = pd.read_csv('data/raw/xai4heat_scada_L4.csv'); \
	df.profile_report().to_file('docs/profile_raw.html')"

## Run feature engineering
features:
	python src/features/build_features.py --config configs/params.yaml

## Train/test split
split:
	python src/data/split.py --config configs/params.yaml

## Profile after feature engineering
profile-features:
	python -c "import ydata_profiling; import pandas as pd; \
	df = pd.read_parquet('data/processed/features.parquet'); \
	df.profile_report().to_file('docs/profile_features.html')"

## Run tests
test:
	python -m pytest tests/ -v

## Run Streamlit dashboard
dashboard:
	streamlit run dashboard/app.py

## Validate data with Pandera
validate:
	python src/data/validate.py

## Clean generated files
clean:
	rm -rf data/interim/* data/processed/*
	rm -rf docs/profile_*.html
	rm -rf mlruns/

## Full pipeline: data → clean → features → split → validate
pipeline: data features split validate
	@echo "Pipeline complete."
```

### Зачем
- `make setup` — новый человек клонирует репо и за 1 команду получает рабочее окружение
- `make pipeline` — пересобрать данные от начала до конца одной командой
- `make test` — проверить что ничего не сломалось
- `make dashboard` — запустить дашборд

### Чеклист готовности
- [ ] Makefile создан с базовыми командами
- [ ] `make setup` работает (создаёт venv, ставит зависимости)
- [ ] Commit: `config: add Makefile`

---

## Задача 0.6: Docker (senior-уровень, опционально)

### Что делаем
Dockerfile для воспроизводимости среды — «у меня работает» больше не проблема.

### Dockerfile (минимальный)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY configs/ configs/
COPY Makefile .

CMD ["make", "pipeline"]
```

### docker-compose.yml (для дашборда)
```yaml
version: "3.8"
services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./dashboard:/app/dashboard
    command: streamlit run dashboard/app.py --server.port 8501
```

### Чеклист готовности
- [ ] Dockerfile создан
- [ ] `docker build -t heatwin .` собирается без ошибок
- [ ] docker-compose.yml для дашборда (опционально)
- [ ] Commit: `config: add Dockerfile`

---

## Задача 0.7: README.md (живой документ)

### Что делаем
README — визитная карточка проекта. Первое, что видит рецензент/hiring manager.

### Структура README
```markdown
# HeatWin: прогнозирование температуры обратной воды в системе теплоснабжения

> Пет-проект по прогнозному управлению теплоснабжением.
> ML-модель прогнозирует T_return на 6 часов вперёд для оптимизации уставки T_supply.

## Бизнес-контекст
Кратко: проблема, цель, ожидаемый эффект (5-15% экономии).

## Результаты
- MAE = X°C на тестовом сезоне
- Conformal PI coverage = Y%
- [Ссылка на EDA-дашборд](https://heatwin.streamlit.app)

## Архитектурная диаграмма
[Вставить диаграмму pipeline: raw → clean → features → model → predict]

## Структура проекта
[Дерево папок]

## Быстрый старт
```bash
git clone https://github.com/username/heatwin.git
cd heatwin
make setup
make pipeline
make dashboard
```

## Данные
Датасет: XAI4HEAT SCADA Dataset 2024 (Mendeley, DOI: 10.17632/2mwc6x6kwb.1)

## Методология
CRISP-DM + роадмапа по статистике для DS. Подробности: docs/

## Стек
Python, pandas, LightGBM, MLflow, Pandera, Streamlit, DVC

## Автор
[Имя, контакты, LinkedIn]
```

### Когда обновляем README
| Фаза | Что добавляем |
|---|---|
| Фаза 0 (сейчас) | Название, описание, структура, быстрый старт |
| Фаза 2 | Ссылка на EDA-дашборд, скриншот |
| Фаза 4 | Результаты модели (MAE, R²) |
| Фаза 6 | Архитектурная диаграмма, ссылка на API |

### Чеклист готовности
- [ ] README содержит: название, описание, структуру, быстрый старт
- [ ] README содержит: стек технологий, ссылку на данные
- [ ] Commit: `docs: add detailed README`

---

## Gate criteria: переход к фазе 1

- [ ] Git-репозиторий создан и опубликован
- [ ] Структура проекта создана по шаблону
- [ ] .gitignore настроен
- [ ] requirements.txt с версиями
- [ ] Виртуальное окружение работает
- [ ] Makefile с базовыми командами (setup, clean)
- [ ] README.md с названием, описанием, структурой
- [ ] DVC инициализирован (рекомендуется)
- [ ] Dockerfile создан (опционально)
- [ ] Первые 3+ осмысленных commit в истории

---

## Литература для фазы 0

### Обязательно

#### Л.1: Cookiecutter Data Science — документация
- **Доступ:** бесплатно — https://drivendata.github.io/cookiecutter-data-science/
- **Что читать:** Opinions (5 мин), Directory Structure (5 мин)
- **Для чего:** стандартная структура проекта

**Чеклист понимания:**
- [ ] Понимаю, зачем разделять notebooks/ и src/ (exploration vs production)
- [ ] Понимаю, зачем data/ вне Git (размер, безопасность)
- [ ] Могу объяснить, зачем нумеровать notebooks (01_, 02_)
- [ ] Знаю принцип «analysis is a DAG» — каждый шаг зависит от предыдущего

#### Л.2: Git — базовый workflow
- **Доступ:** бесплатно — https://git-scm.com/book/en/v2 (главы 1-3)
- **Что читать:** Chapter 1 (Getting Started), Chapter 2 (Git Basics), Chapter 3 (Branching)
- **Для чего:** осмысленные commits, branches, .gitignore

**Чеклист понимания:**
- [ ] Могу сделать: init, add, commit, push, pull, branch, checkout, merge
- [ ] Понимаю .gitignore — зачем и как работает
- [ ] Могу написать осмысленный commit message (тип: описание)
- [ ] Понимаю feature branch workflow: main → feature/X → PR → merge

### Рекомендуется

#### Л.3: DVC — Get Started
- **Доступ:** бесплатно — https://dvc.org/doc/start
- **Что читать:** Get Started (20 мин)
- **Для чего:** версионирование данных

**Чеклист понимания:**
- [ ] Понимаю: DVC = «Git для данных» — .dvc файлы в Git, данные в storage
- [ ] Могу выполнить: dvc init, dvc add, dvc push, dvc pull
- [ ] Понимаю remote storage — где лежат данные (local / S3 / GDrive)

#### Л.4: Pandera — Getting Started
- **Доступ:** бесплатно — https://pandera.readthedocs.io/en/stable/
- **Что читать:** Getting Started (15 мин), DataFrameSchema (10 мин)
- **Для чего:** декларативная валидация данных

**Чеклист понимания:**
- [ ] Могу создать DataFrameSchema с типами колонок и ограничениями (T_return > 0, T_return < T_supply)
- [ ] Понимаю разницу между Pandera (лёгкий, для pandas) и Great Expectations (тяжёлый, для production)
- [ ] Могу подключить Pandera-валидацию в pipeline (validate на входе и выходе каждого шага)

#### Л.5: Makefile для DS — примеры
- **Доступ:** бесплатно — в документации Cookiecutter Data Science
- **Что читать:** пример Makefile из шаблона (5 мин)
- **Для чего:** автоматизация команд проекта

**Чеклист понимания:**
- [ ] Понимаю синтаксис Makefile: target, dependencies, commands
- [ ] Могу написать: make setup, make data, make test, make clean
- [ ] Понимаю .PHONY и зачем он нужен

---

## Маппинг на роадмапу

Фаза 0 не маппится на блоки роадмапы напрямую — это инженерная обвязка, не статистика. Но она критична для:
- **Портфолио:** структурированный проект vs «набор файлов» — первое нанимают
- **Воспроизводимости:** любой человек может клонировать и запустить
- **Масштабируемости:** когда в фазе 4 начнутся эксперименты — инфраструктура уже готова

## Полный список артефактов фазы 0

| # | Артефакт | Файл | Статус |
|---|---|---|---|
| 1 | Git-репозиторий | GitHub URL | обязательно |
| 2 | .gitignore | .gitignore | обязательно |
| 3 | Структура проекта | папки + .gitkeep | обязательно |
| 4 | requirements.txt | requirements.txt | обязательно |
| 5 | Виртуальное окружение | .venv/ | обязательно |
| 6 | README.md (v0) | README.md | обязательно |
| 7 | Makefile | Makefile | рекомендуется |
| 8 | DVC init | .dvc/, .dvcignore | рекомендуется |
| 9 | Dockerfile | Dockerfile | опционально |
| 10 | docker-compose.yml | docker-compose.yml | опционально |
