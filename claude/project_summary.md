# Саммари проекта HeatWin — точка фиксации

## Дата: 27 марта 2026
## Автор проекта: IvanovMS (gromli@bk.ru)
## GitHub: https://github.com/gromli66/heatwin

---

## 1. Что за проект

**HeatWin** — ML-система прогнозирования температуры обратной воды (T_return) на 6–24 часа вперёд для оптимизации теплоснабжения. Пет-проект для портфолио DS/MLE.

**Бизнес-контекст:** ООО «АТЭС-Полярные Зори», Мурманская область. Электрокотельная 48.16 Гкал/ч + мазутная 79.7 Гкал/ч, 33.7 км сетей, температурный график 115/70°С. Цель — 5-15% экономии через прогнозное управление вместо реактивного.

**Данные:** XAI4HEAT SCADA Dataset (Cvetković et al., 2025, Mendeley DOI: 10.17632/2mwc6x6kwb.1) — 5 подстанций г. Ниш (Сербия), 5 отопительных сезонов (2019–2024), часовая дискретизация.

**Стек:** Python + LightGBM/XGBoost + MLflow + Pandera + FastAPI + Streamlit + DVC + Docker.

---

## 2. Что спланировали (проектные документы)

Полный план проекта от `git init` до `docker-compose up` по методологии CRISP-DM + MLOps + A/B testing + причинный анализ.

### Созданные документы (14 файлов, 6685 строк)

| # | Документ | Строк | Фаза | Содержание |
|---|---|---|---|---|
| 1 | phase0_infrastructure.md | 564 | 0 | Git, cookiecutter-структура, DVC, Makefile, Docker, README |
| 2 | Project_Brief_Template_v2.docx | — | 1 | Шаблон 9 разделов + Приложение А + Б |
| 3 | project_brief_supplement.md | 145 | 1 | Дополнения из CRISP-DM + Нетбай: Current Solution, Risks, Terminology, Costs, формальная постановка |
| 4 | phase2_data_understanding.md | 559 | 2 | 6 задач: EDA + измерение инерционности (2.3.7) |
| 5 | gate_review_2_to_3.md | 201 | 2→3 | 6 шагов: сверка допущений, решение GO/STOP |
| 6 | phase3_data_preparation.md | 454 | 3 | 7 задач + Rationale for Inclusion/Exclusion + стратегия объединения подстанций |
| 7 | phase4_modeling.md | 697 | 4 | 8 задач + post-processing (сглаживание из Нетбая) |
| 8 | phase5_6_eval_deploy.md | 749 | 5+6 | Backtesting + попериодный анализ + FINDINGS + A/B + Deploy |
| 9 | literature.md | 253 | сквозной | 23 источника с точными страницами и чеклистами |
| 10 | lessons_phase0.md | 1921 | обучение | 4 урока, 28 упражнений |
| 11 | conspect_crispdm_netbay.md | 482 | конспект | Исчерпывающий конспект CRISP-DM (91 стр.) + Нетбай (10 стр.) |
| 12 | validate.py | 393 | код | Pandera-схема с документированными диапазонами + диагностика |
| 13 | project_summary.md | 267 | сводка | Полное саммари проекта на точку фиксации |
| 14 | HeatWin_Research_Report.docx | — | предварительный | Аналитическая записка 20+ стр. (из предыдущей сессии) |

### Покрытие роадмапы по статистике для DS

Все 14 блоков закрыты (кроме 11.2 survival — не релевантен):
- Блоки 3 (EDA), 4 (распределения), 5 (MLE/MoM) → фаза 2
- Блоки 6 (CI, conformal), 7 (гипотезы), 9 (OLS, диагностика) → фаза 4
- Блоки 8 (A/B), 10 (DAG, DiD), 14 (алгоритм) → фаза 5
- Блоки 11 (TS), 12 (тесты: GoF, Kruskal-Wallis, CUSUM, корреляция) → фазы 2–4

### Ключевые архитектурные решения

- **Фаза 0** добавлена перед CRISP-DM — инженерная инфраструктура (Git, DVC, Pandera, Makefile)
- **Пирамида моделей:** naive → seasonal naive → ARIMA → OLS → Ridge/Lasso → LightGBM → XGBoost → LSTM (опц.)
- **Шаблон 14.1:** формальный H₀/H₁/α/тест/решение перед КАЖДЫМ статистическим тестом
- **Cross-column checks вынесены в диагностику**, не в строгую валидацию (физика переходных режимов)
- **Три выхода каждой фазы:** notebook (техн.), summary report (бизнес), дашборд (оба)

---

## 3. Что изучили (уроки фазы 0)

### Урок 1: Git — ПРОЙДЕН
- Теория: репозитории, commits, staging, branches, merge, remote, .gitignore
- Практика: 6 упражнений + финальное задание
- Репозиторий git-practice: https://github.com/gromli66/git-practice
- Репозиторий heatwin: https://github.com/gromli66/heatwin (первый коммит: `init: create repository with .gitignore`)

**Что усвоено:**
- Три состояния файла: working → staging → repository
- Формат коммитов: `тип: описание` (init, feat, fix, docs, config, eda, model, test, refactor)
- Feature branch workflow: main → feature/X → merge
- .gitignore: с DVC — по расширениям (*.csv), не по папкам (data/raw/)
- `git diff` — читать вывод (@@, +/-, контекст)
- Fast-forward merge vs merge-commit
- Tags для именования состояний pipeline

### Урок 2: Структура проекта + logging + .env + type hints — ПРОЙДЕН
- Cookiecutter Data Science структура создана в heatwin
- Принцип «analysis is a DAG», notebooks/ vs src/, __init__.py

**Что усвоено:**
- **logging:** basicConfig vs YAML, уровни (DEBUG→CRITICAL), `setup_logging()` один раз в main.py, `logging.getLogger(__name__)` в каждом модуле. Аналогия: настроить сеть (один раз) vs купить телефон (каждый модуль)
- **main.py** лежит в корне проекта
- **Для notebook:** `setup_logging()` в первой ячейке
- **.env + python-dotenv:** пути и конфиги, .env.example для Git
- **Type hints:** `def load_csv(path: str) -> pd.DataFrame`
- **mypy:** опционален, VSCode подсвечивает основные ошибки
- **Windows:** пути в Python через `/` не `\` (unicode escape ошибка)
- **`from src.module import func`** — нужен `__init__.py` в каждой подпапке src/
- **`ModuleNotFoundError: No module named 'src'`** → решение: `python -m tests.val_test` или `sys.path.insert(0, ".")`

### Урок 3: DVC — ПРОЙДЕН
- dvc init, dvc add, dvc.yaml pipeline (clean → features), dvc repro, dvc dag
- Pipeline работает, метрики отслеживаются

**Что усвоено:**
- DVC не имеет своих коммитов/веток — использует Git. Git = голова, DVC = тело
- `dvc push`/`dvc pull` нужны только для передачи по сети (другой компьютер, коллега). Локально достаточно `dvc add` + `dvc checkout`
- `dvc repro` читает `dvc.yaml`, проверяет хэши deps, пропускает неизменившееся
- Все состояния pipeline хранятся в `.dvc/cache/` по хэшам. Переключение: `git checkout <tag>` → `dvc checkout` (мгновенно из кэша)
- Git tags для именования состояний: `git tag v1-baseline-lags`
- .gitignore с DVC: игнорировать по расширениям (*.csv, *.parquet), НЕ по папкам (data/raw/ блокирует .dvc файлы)
- **parquet** = бинарный формат, 3-5× меньше CSV, 10× быстрее чтение, сохраняет типы. Нужен pyarrow

### Урок 4: Pandera — ПРОЙДЕН (на реальных данных HeatWin)
- Базовая схема, валидация на реальных XAI4HEAT данных (lazy=True), schema inference (infer_schema + to_script), диагностика cross-column
- Работает на heatwin, результаты в docs/data_diagnostics.json

**Что усвоено:**
- Pandera = валидация DataFrame, Pydantic = валидация Python-объектов (API input). Оба пригодятся: Pandera в фазах 2-4, Pydantic в фазе 6 (FastAPI)
- `import pandera.pandas as pa` (новый импорт, без FutureWarning)
- Cross-column check: `pa.Check(lambda df: (df["T_return"] < df["T_supply"]).all())` на уровне DataFrameSchema.checks
- infer_schema → to_script() → ручная правка диапазонов до физических
- Пути в Windows: использовать `/` вместо `\` (избежать unicode escape)

---

## 4. Что узнали о данных XAI4HEAT (до начала EDA)

### Источник и статья
- Cvetković S., Zdravković M., Ignjatović M. "Exploring district heating systems: A SCADA dataset for enhanced explainability", Data in Brief, 2025
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11815968/

### Структура данных (из Table 2 статьи)

| Колонка | Описание | Единица |
|---|---|---|
| datetime | Timestamp, часовой шаг, CET/CEST | — |
| t_amb | Наружная температура, датчик У ПОДСТАНЦИИ (не метеостанция) | °C |
| t_ref | **УСТАВКА** — целевая температура вторичной подачи из регулировочной кривой (расчётная, не измеренная) | °C |
| t_sup_prim | Подача первичного контура | °C |
| t_ret_prim | Обратка первичного контура | °C |
| t_sup_sec | Подача вторичного контура | °C |
| t_ret_sec | Обратка вторичного контура | °C |
| delta_e | Переданная энергия = разность показаний калориметра за час | кВтч |

### Ключевая находка: t_ref — это T_supply_setpoint

Колонка `t_ref` НЕ описана в Mendeley, но описана в статье (Table 2). Это **уставка** — целевая температура для вторичной подачи, рассчитанная по регулировочной кривой. В концепте HeatWin это `T_supply_setpoint`. Ценная переменная для: обнаружения перетопа (факт > уставки), feature engineering (отклонение от уставки), бизнес-анализа.

### Маппинг XAI4HEAT → концепт HeatWin

| Концепт HeatWin | XAI4HEAT | Есть? |
|---|---|---|
| T_supply (прямая) | t_sup_prim, t_sup_sec | ✓ |
| T_return (обратка) | t_ret_prim, t_ret_sec | ✓ |
| T_supply_setpoint (уставка) | t_ref | ✓ |
| air_temperature | t_amb | ✓ |
| energy | delta_e | ✓ |
| flow_rate, pressure, wind, humidity | — | ✗ |

### Результаты валидации (5 подстанций)

**Строгая валидация (Pandera):**
- L4, L8, L12, L17: **PASSED**
- L22: **FAILED** — датчик t_amb сломан (значения 55-90°C вместо наружной температуры)

**Диагностика (мягкие проверки):**

| Подстанция | Строк | Система откл. | ret>sup (prim) | ret>sup (sec) | Откл. от уставки (ср/макс) |
|---|---|---|---|---|---|
| L4 | 18101 | 32.1% | 0.15% | 4.62% | 2.5°C / 47.9°C |
| L8 | 10877 | 36.7% | 0.07% | 4.74% | 1.4°C / 42.2°C |
| L12 | 10877 | 36.9% | 0.04% | 0.83% | 1.4°C / 21.0°C |
| L17 | 18137 | 36.1% | 0.13% | 0.03% | 1.7°C / 45.2°C |
| L22 | 10877 | — | — | — | — (датчик сбой) |

**Интерпретация:**
- Система отключена 32-37% времени — подтверждает статью (>30%)
- Cross-column нарушения при работе: t_ret_sec > t_sup_sec в 0.03-4.74% — малая нагрузка + погрешность датчика (±0.3°C), не ошибка данных
- Отклонение от уставки: среднее 1.4-2.5°C (нормальное регулирование), максимум 42-48°C (пуск/останов)
- L22 — решение на фазе 2: использовать t_amb с другой подстанции или исключить из MVP

### Физические диапазоны (из отраслевой литературы)

| Колонка | Из данных | Отраслевой | Источник |
|---|---|---|---|
| t_amb | -11.8...24.3 | -25...45 | Климат Ниша |
| t_ref | 0...~65 | 0...85 | Уставка вторичной подачи |
| t_sup_prim | 0...101.5 | 0...115 | Swedish DH survey + Wikipedia |
| t_ret_prim | 0...72.2 | 0...75 | 142 Swedish systems (расширен по данным) |
| t_sup_sec | 0...94.8 | 0...100 | ScienceDirect (расширен из-за L22) |
| t_ret_sec | 0...93.9 | 0...100 | CIBSE (расширен из-за L22) |
| delta_e | 0...178360 | ≥0, без верх. лимита | Зависит от подстанции |

---

## 5. Среда разработки

- **ОС:** Windows, WSL (Ubuntu) доступен
- **Python:** 3.11.9
- **IDE:** VSCode (основная) + PyCharm (запасная)
- **Anaconda:** установлена, но НЕ используется для HeatWin — venv + pip
- **Git:** работает, GitHub авторизация настроена
- **Make:** установлен (GnuWin32, PATH: `C:\Program Files (x86)\GnuWin32\bin`)
- **Терминал:** PowerShell (основной) + Git Bash (для bash-команд)
- **Виртуальное окружение:** `.venv` в каждом проекте

---

## 6. Текущее состояние GitHub: https://github.com/gromli66/heatwin

### Структура (6 коммитов, ветка master)
```
.dvc/           ✓
configs/        ✓
data/           ✓ (с DVC tracking)
dashboard/      ✓ (.gitkeep)
docs/           ✓ (data_diagnostics.json)
notebooks/      ✓ (.gitkeep)
src/            ✓ (data/validate.py, logging_setup.py, __init__.py, features/, models/, visualization/)
tests/          ✓ (.gitkeep, __init__.py)
.dvcignore      ✓
.env.example    ✓
.gitignore      ✓
Makefile        ✓
README.md       ✓ (минимальный: "Проект HeatWin")
main.py         ✓
requirements.txt ✓
```

---

## 7. Литература — статус

### Прочитано / изучено
- [x] Pro Git Book — главы 1-3 (через уроки)
- [x] Cookiecutter Data Science — Opinions + Directory Structure (через уроки)
- [x] DVC — Get Started (через уроки)
- [x] Pandera — Getting Started (через уроки + реальные данные)
- [x] Cvetković et al. 2025 — статья по XAI4HEAT (Table 2, Limitations, Section 4.1)
- [x] CRISP-DM Guide — полный конспект 91 стр. → 350 строк (conspect_crispdm_netbay.md)
- [x] Нетбай и др. 2020 — полный конспект 10 стр. → 130 строк (conspect_crispdm_netbay.md)

### Следующее к прочтению (фаза 1)
- [ ] Data Science for Business (Provost) — только глава 2, стр. 19-42 (23 стр.)
- [ ] Designing ML Systems (Huyen) — только глава 2 (основной источник для framing)

### Полный каталог: 23 источника
- 16 бесплатных, 7 платных
- Provost локализован: 77 стр. из 414 (19%) — точные страницы по фазам
- Каждый источник с чеклистом понимания

---

## 8. Что дальше

### Ближайший шаг: чтение оставшейся литературы фазы 1 (~4-6 часов)
1. **Provost глава 2, стр. 19-42** (23 стр., требует перевода) — типы DS-задач, «think backwards»
2. **Huyen DMLS глава 2** (основной источник) — framing ML problems, business vs ML objectives

CRISP-DM и Нетбай уже законспектированы — можно перечитать конспект и задавать вопросы.

### После прочтения: заполнение Project Brief
- Шаблон готов (Project_Brief_Template_v2.docx)
- Дополнения готовы (project_brief_supplement.md) — вставить при заполнении
- Заполнять раздел за разделом, сверяясь с конспектом CRISP-DM

### Далее: фаза 2 (EDA)
- Чеклист готов (phase2_data_understanding.md)
- Данные XAI4HEAT скачаны и провалидированы
- Ключевая новая задача: измерить инерционность (2.3.7) → обосновать горизонт прогноза

---

## 9. Ключевые решения принятые по ходу работы

| Решение | Обоснование |
|---|---|
| Фаза 0 перед CRISP-DM | Инженерная обвязка нужна ДО аналитики — иначе «набор файлов» |
| XAI4HEAT вместо реальных данных ПЗ | Публичный SCADA dataset, 5 сезонов, документирован в статье |
| venv + pip, не Anaconda | Стандарт в вакансиях и open-source, совместимость с Docker |
| VSCode, не Colab | Git, DVC, Makefile, структура проекта — Colab не поддерживает |
| Pandera, не Great Expectations | Лёгкий, для pandas, достаточен для пет-проекта |
| Cross-column → диагностика, не валидация | t_ret > t_sup при отключении — физика, не ошибка |
| .gitignore по расширениям, не по папкам | DVC .dvc файлы лежат в data/ — папочный ignore блокирует их |
| t_ref = уставка (T_supply_setpoint) | Подтверждено статьёй Cvetković Table 2 — расчётная, не измеренная |
| L22 — проблемная подстанция | Датчик t_amb сбоит (55-90°C) — решить на фазе 2 |
| Provost: 77 из 414 стр. | Остальное покрыто ISLR/Huyen или не релевантно для HeatWin |

### Решения из анализа CRISP-DM + Нетбай (добавлены 30.03.2026)

| Решение | Куда добавлено |
|---|---|
| Формальная математическая постановка (как у Нетбая) | project_brief_supplement.md раздел 4.1 |
| Глоссарий бизнес + DS/ML терминов | project_brief_supplement.md раздел 2.5 |
| Current Solution (ручное управление каждые 2ч) | project_brief_supplement.md раздел 2.2 |
| Cost-benefit анализ проекта (200ч vs экономия 5-15%) | project_brief_supplement.md раздел 2.6 |
| Формальный список рисков (7 рисков + план B) | project_brief_supplement.md раздел 2.4 |
| Rationale for Inclusion/Exclusion (L22, t_ref, delta_e=0) | phase3 задача 3.1 |
| Стратегия объединения подстанций (3 варианта: одна/отдельные/кластерная) | phase3 задача 3.4 |
| Измерение инерционности (cross-correlation) → обоснование горизонта | phase2 задача 2.3.7 |
| Post-processing предсказаний (сглаживание из Нетбая) | phase4 задача 4.3.5 |
| Попериодный backtesting (по режимам: похолодание/оттепель/пуск) | phase5 задача 5.2.2 |
| FINDINGS = побочные находки (CRISP-DM: RESULTS = MODELS + FINDINGS) | phase5 задача 5.7 |
