# А. ПРОМТ ДЛЯ НОВОГО ЧАТА
# Скопировать и вставить в начало разговора с Claude

---

## Как использовать:
## 1. Скопируйте весь блок между === НАЧАЛО ПРОМТА === и === КОНЕЦ ПРОМТА ===
## 2. Вставьте первым сообщением в новый чат
## 3. Приложите файлы которые нужны для текущего шага (см. навигатор ниже)
## 4. Напишите что конкретно делаете сейчас

---

=== НАЧАЛО ПРОМТА ===

# Контекст проекта HeatWin

Ты помогаешь мне вести DS-проект HeatWin. Это пет-проект для портфолио. Ниже полный контекст — все решения, прогресс, файлы. Не нужно ничего перепроверять или переспрашивать — просто продолжай работу с того места, где мы остановились.

## Проект
HeatWin — ML-система прогнозирования T_return (температура обратки) на 6–24ч для оптимизации теплоснабжения. Методология: CRISP-DM + MLOps + A/B + причинный анализ.

## Клиент (легенда)
ООО «АТЭС-Полярные Зори», Мурманская область. Электрокотельная 48.16 Гкал/ч + мазутная 79.7 Гкал/ч. Цель: экономия 5-15% топлива через прогнозное управление.

## Данные
XAI4HEAT SCADA Dataset (Cvetković et al., 2025, DOI: 10.17632/2mwc6x6kwb.1). 5 подстанций г. Ниш (Сербия), 5 сезонов (2019–2024), часовая дискретизация. Колонки: datetime, t_amb, t_ref (уставка!), t_sup_prim, t_ret_prim, t_sup_sec, t_ret_sec, delta_e (кВтч).

## Стек
Python 3.11 + LightGBM/XGBoost + MLflow + Pandera + FastAPI + Streamlit + DVC + Docker. IDE: VSCode. ОС: Windows + WSL. venv (не Anaconda).

## GitHub
https://github.com/gromli66/heatwin (master, структура cookiecutter, DVC init, Pandera validate.py)

## Ключевые находки из данных
- t_ref — НЕ измеренная температура, а УСТАВКА (из регулировочной кривой). Это T_supply_setpoint.
- L22 — сбой датчика t_amb (значения 55-90°C). Решение: исключить из MVP или заменить t_amb.
- Система отключена 32-37% времени (delta_e = 0). Подтверждено статьёй (>30%).
- Cross-column нарушения (ret > sup) в 0-5% при работе — физика переходных режимов, не ошибка.
- Отклонение от уставки: среднее 1.4-2.5°C, макс 42-48°C (пуск/останов).
- Инерционность теплосети: нужно измерить cross-correlation на EDA (задача 2.3.7).

## Ключевые решения
- Фаза 0 добавлена перед CRISP-DM (Git, DVC, Pandera, Makefile)
- Пирамида моделей: naive → seasonal naive → ARIMA → OLS → LightGBM → XGBoost → LSTM (опц.)
- Шаблон 14.1 (H₀/H₁/α/тест/решение) перед КАЖДЫМ стат. тестом
- Cross-column checks вынесены в диагностику (не строгая валидация)
- Модель только для отопительного сезона (ноябрь–апрель)
- Формальная математическая постановка: f: H(t) → T_ret_sec(t+h), h ∈ {6,12,24}, MAE < 2°C
- Одна модель на все подстанции (MVP) vs отдельные (сравнение)
- Итерация 4.5: ручной подбор гиперпараметров перед Optuna
- Digital Twin: lookup-симулятор теплосети для simulation backtesting (задача 5.2.3)

## Проектные документы (приложить нужные к сообщению)
1. phase0_infrastructure.md — фаза 0 чеклист
2. Project_Brief_Template_v2.docx — шаблон Brief
3. project_brief_supplement.md — дополнения Brief (Current Solution, Risks, Terminology, Costs, формальная постановка)
4. phase2_data_understanding.md — фаза 2 чеклист (EDA + инерционность)
5. gate_review_2_to_3.md — точка решения GO/STOP
6. phase3_data_preparation.md — фаза 3 чеклист (Rationale, интеграция подстанций, только отоп. сезон)
7. phase4_modeling.md — фаза 4 чеклист (пирамида, ручной подбор, post-processing)
8. phase5_6_eval_deploy.md — фазы 5+6 (попериодный backtesting, FINDINGS, A/B, deploy)
9. literature.md — 23 источника с чеклистами
10. lessons_phase0.md — 4 урока, 28 упражнений (пройдены)
11. conspect_crispdm_netbay.md — конспект CRISP-DM + Нетбай
12. validate.py — Pandera-схема XAI4HEAT
13. project_summary.md — полное саммари проекта
14. supplement_questions_risks_reports.md — вопросы User Guide + риски моделирования M1-M10 + шаблоны 8 отчётов

## Текущий прогресс
- [x] Фаза 0: инфраструктура — ЗАВЕРШЕНА (GitHub, Git, DVC, Pandera, Makefile, структура)
- [x] Уроки фазы 0: 4 урока, 28 упражнений — ПРОЙДЕНЫ
- [x] Валидация XAI4HEAT — 4/5 PASSED, L22 сбой задокументирован
- [x] Конспект CRISP-DM + Нетбай — ГОТОВ (482 строки)
- [ ] Чтение: Provost гл.2 (стр. 19-42) + Huyen DMLS гл.2
- [ ] Заполнение Project Brief
- [ ] Фаза 2: EDA
- [ ] Фаза 3: Data Preparation
- [ ] Фаза 4: Modeling
- [ ] Фаза 5: Evaluation
- [ ] Фаза 6: Deployment

## Среда
Windows, Python 3.11.9, VSCode, Git, GnuWin32 Make (PATH: C:\Program Files (x86)\GnuWin32\bin), Git Bash для bash-команд. Автор: IvanovMS, email: gromli@bk.ru.

## Стиль работы
- Говори прямо, без воды. Если не знаешь — скажи.
- Все цифры и факты — из документов, не выдумывай.
- Каждое решение — с обоснованием.
- Код: Python, type hints, logging вместо print, пути через / не \.
- Коммиты: тип: описание (init, feat, fix, docs, config, eda, model, test, refactor).

=== КОНЕЦ ПРОМТА ===

---
---

# Б. ПОШАГОВЫЙ ПЛАН-НАВИГАТОР
# Открывать когда нужно понять «что дальше» и «что приложить к чату»

---

## Как пользоваться навигатором:
## 1. Найдите текущий шаг (по прогрессу)
## 2. Прочитайте: что делать, какие файлы приложить, какие вопросы задать
## 3. Откройте новый чат → вставьте промт → приложите файлы → работайте
## 4. После завершения шага — отметьте ✅ и переходите к следующему

---

## ШАГ 1: Чтение литературы фазы 1 ✅/⬜
**Статус:** СЛЕДУЮЩИЙ ШАГ

**Что делать:**
1. Прочитать Provost главу 2, стр. 19-42 (23 стр., нужен перевод)
2. Прочитать Huyen DMLS главу 2 (или summary: github.com/serodriguez68)
3. Перечитать конспект CRISP-DM + Нетбай (conspect_crispdm_netbay.md)

**Приложить к чату:** conspect_crispdm_netbay.md + literature.md
**Задать Claude:** «Я прочитал Provost гл.2 и Huyen гл.2. Вот мои вопросы: ...»

**Готовность:** могу ответить на вопросы из чеклистов понимания в literature.md

---

## ШАГ 2: Заполнение Project Brief ⬜
**Статус:** после шага 1

**Что делать:**
1. Открыть Project_Brief_Template_v2.docx
2. Открыть project_brief_supplement.md (дополнения: Current Solution, Risks, Terminology, Costs, формальная постановка)
3. Открыть supplement_questions_risks_reports.md → раздел «Фаза 1: Business Understanding»
4. Заполнять раздел за разделом, отвечая на вопросы User Guide
5. Каждый раздел — отдельный коммит

**Приложить к чату:** Project_Brief_Template_v2.docx + project_brief_supplement.md + supplement_questions_risks_reports.md + conspect_crispdm_netbay.md
**Задать Claude:** «Помоги заполнить раздел X Project Brief. Вот мои ответы на вопросы: ...»

**Готовность:** Brief v1.0 заполнен, закоммичен в docs/

---

## ШАГ 3: EDA — описание данных (фаза 2, задачи 2.1-2.2) ⬜
**Статус:** после шага 2

**Что делать:**
1. Создать notebooks/01_data_description.ipynb
2. Загрузить все 5 CSV + heating_areas
3. Ответить на вопросы Data Description из supplement (раздел «Фаза 2, задача 2.2»)
4. Заполнить шаблон Data Description Report (supplement раздел 3.1)

**Приложить к чату:** phase2_data_understanding.md + supplement_questions_risks_reports.md + validate.py
**Задать Claude:** «Начинаю EDA. Вот описание данных: [вставить вывод df.info(), df.describe()]. Помоги с Data Description Report.»

**Готовность:** Data Description Report готов, коммит: `eda: add data description report`

---

## ШАГ 4: EDA — исследование (фаза 2, задача 2.3) ⬜
**Статус:** после шага 3

**Что делать:**
1. Создать notebooks/02_eda_exploration.ipynb
2. Пройти по чеклисту phase2 задача 2.3 (распределения, временные ряды, корреляции, профили, стационарность)
3. **КЛЮЧЕВОЕ: задача 2.3.7** — измерить инерционность (cross-correlation)
4. Заполнить лог гипотез
5. Ответить на вопросы Data Exploration из supplement
6. Заполнить шаблон Data Exploration Report (supplement раздел 3.2)

**Приложить к чату:** phase2_data_understanding.md + supplement_questions_risks_reports.md
**Задать Claude:** «Вот результаты EDA: [ключевые графики, статистики]. Инерционность = X часов. Помоги интерпретировать и заполнить Exploration Report.»

**Готовность:** EDA notebook + Exploration Report + лог гипотез, коммит: `eda: add exploration analysis`

---

## ШАГ 5: EDA — качество данных (фаза 2, задача 2.4) ⬜
**Статус:** после шага 4

**Что делать:**
1. Дополнить Pandera-валидацию (если нужно после EDA)
2. Ответить на вопросы Data Quality из supplement
3. Заполнить шаблон Data Quality Report (supplement раздел 3.3)

**Приложить к чату:** phase2_data_understanding.md + validate.py
**Задать Claude:** «Вот результаты проверки качества. Помоги с Data Quality Report.»

**Готовность:** DQR готов, docs/data_diagnostics.json обновлён

---

## ШАГ 6: EDA — упаковка + дашборд (фаза 2, задачи 2.5-2.6) ⬜
**Статус:** после шага 5

**Что делать:**
1. EDA Summary Report (2-3 стр. для бизнеса)
2. Streamlit EDA дашборд (dashboard/app.py)
3. Деплой на Streamlit Cloud

**Приложить к чату:** phase2_data_understanding.md
**Задать Claude:** «Помоги создать Streamlit дашборд для EDA. Вот ключевые визуализации: ...»

**Готовность:** Summary Report + дашборд + коммиты

---

## ШАГ 7: Gate Review 2→3 ⬜
**Статус:** после шага 6

**Что делать:**
1. Пройти gate_review_2_to_3.md — 6 шагов
2. Сверить допущения из Brief с EDA-результатами
3. Решение: GO / STOP / ITERATE

**Приложить к чату:** gate_review_2_to_3.md + Project Brief + EDA результаты
**Задать Claude:** «Провожу gate review. Вот допущения из Brief и результаты EDA. Помоги принять решение.»

**Готовность:** Gate review пройден, решение зафиксировано

---

## ШАГ 8: Чтение литературы фазы 3 ⬜
**Статус:** после шага 7

**Что читать:** (из literature.md)
- Modern Time Series Forecasting — главы 4-6
- Роадмапа — блоки 3.1, 11.1

**Готовность:** чеклисты понимания из literature.md заполнены

---

## ШАГ 9: Data Preparation (фаза 3) ⬜
**Статус:** после шага 8

**Что делать:**
1. Задача 3.1: Select Data — заполнить Rationale for Inclusion/Exclusion
2. Задача 3.2: Clean Data — очистка + Data Cleaning Report
3. Задача 3.3: Feature Engineering — 75 features по 5 группам
4. Задача 3.4: Integrate Data — решение по объединению подстанций
5. Задача 3.5: Format Data — parquet
6. Задача 3.6: Train/Test Split — walk-forward
7. Задача 3.7: Feature Pipeline — DVC pipeline (dvc.yaml)

**Приложить к чату:** phase3_data_preparation.md + supplement_questions_risks_reports.md
**Задать Claude:** «Начинаю фазу 3. Вот решение по подстанциям: [A/B/C]. Помоги с feature engineering.»

**Готовность:** Feature Dictionary, pipeline работает (dvc repro), коммиты по задачам

---

## ШАГ 10: Чтение литературы фазы 4 ⬜
**Статус:** после шага 9

**Что читать:** (из literature.md)
- ISLR — главы 5, 6, 8
- Modern TS Forecasting — главы 6-10
- Роадмапа — блоки 6, 7, 9, 11.3
- Provost гл.3 стр. 43-56 (опционально)
- Interpretable ML (Molnar) — SHAP
- Optuna docs

**Готовность:** чеклисты понимания заполнены

---

## ШАГ 11: Modeling (фаза 4) ⬜
**Статус:** после шага 10

**Что делать:**
1. Задача 4.1: выбор техник + допущения
2. Задача 4.2: test design (walk-forward CV)
3. Задача 4.3: обучение (OLS → ARIMA → LightGBM → XGBoost → ручной подбор → Optuna)
4. Задача 4.4: оценка (DM-test, сравнение, ранжирование)
5. Задача 4.5: Optuna tuning
6. Задача 4.6: SHAP
7. Задача 4.7: conformal PI
8. Задача 4.8: упаковка

**ПРОВЕРИТЬ РИСКИ:** M1 (data leakage), M2 (сезонность vs физика), M4 (SHAP vs domain), M5 (overfitting), M6 (LightGBM vs ARIMA)

**Приложить к чату:** phase4_modeling.md + supplement_questions_risks_reports.md (риски M1-M10)
**Задать Claude:** «Обучил OLS baseline, MAE = X. Вот диагностика остатков: [результаты]. Помоги интерпретировать и перейти к LightGBM.»

**Готовность:** лучшая модель определена, SHAP, conformal PI, все в MLflow

---

## ШАГ 12: Чтение литературы фазы 5 ⬜
**Статус:** после шага 11

**Что читать:**
- Trustworthy Online Controlled Experiments — главы 1-4, 7, 17
- Causal Inference: The Mixtape — главы 5, 7, 9
- Provost гл.7 стр. 147-178 + гл.8 стр. 195-204

---

## ШАГ 13: Evaluation (фаза 5) ⬜
**Статус:** после шага 12

**Что делать:**
1. Задача 5.1: бизнес-оценка (°C → рубли)
2. Задача 5.2: backtesting + попериодный анализ
3. Задача 5.2.3: **Digital Twin** — lookup-симулятор + simulation backtesting + what-if в дашборде
4. Задача 5.3: дизайн пилота (A/B, CUPED, power)
5. Задача 5.4: DAG + DiD
6. Задача 5.5: review процесса
7. Задача 5.6: решение deploy/iterate/stop
8. Задача 5.7: Evaluation Report + FINDINGS

**ПРОВЕРИТЬ РИСКИ:** M3, M7, M8, M10

**Приложить к чату:** phase5_6_eval_deploy.md + supplement_questions_risks_reports.md (шаблон Evaluation Report)

**Готовность:** Evaluation Report (5-8 стр.), решение GO/STOP

---

## ШАГ 14: Deployment (фаза 6) ⬜
**Статус:** после шага 13

**Что делать:**
1. Задача 6.1: план деплоя
2. Задача 6.2: FastAPI
3. Задача 6.3: продуктовый дашборд
4. Задача 6.4: мониторинг
5. Задача 6.5: Docker
6. Задача 6.6: Final Report (10-15 стр.) + Final Presentation (10-12 слайдов)
7. Задача 6.7: ретроспектива

**Приложить к чату:** phase5_6_eval_deploy.md + supplement_questions_risks_reports.md (шаблоны Final Report + Presentation + Experience Doc)

**Готовность:** GitHub repo публичный с README + результатами + скриншотами. docker-compose up работает. Streamlit Cloud дашборд. Проект завершён.

---

## БЫСТРАЯ НАВИГАЦИЯ: что приложить к чату

| Текущий шаг | Обязательно приложить | Опционально |
|---|---|---|
| 1. Чтение | conspect_crispdm_netbay.md, literature.md | — |
| 2. Brief | Project_Brief_Template_v2.docx, project_brief_supplement.md, supplement_questions_risks_reports.md | conspect_crispdm_netbay.md |
| 3-6. EDA | phase2_data_understanding.md, supplement_questions_risks_reports.md | validate.py |
| 7. Gate | gate_review_2_to_3.md | Project Brief |
| 9. Data Prep | phase3_data_preparation.md, supplement_questions_risks_reports.md | — |
| 11. Modeling | phase4_modeling.md, supplement_questions_risks_reports.md | literature.md |
| 13. Evaluation | phase5_6_eval_deploy.md, supplement_questions_risks_reports.md | — |
| 14. Deploy | phase5_6_eval_deploy.md, supplement_questions_risks_reports.md | — |
| Любой шаг | project_summary.md (если Claude потерял контекст) | — |

---

## ЕСЛИ CLAUDE ПОТЕРЯЛ КОНТЕКСТ:
1. Вставьте промт (блок А)
2. Приложите project_summary.md
3. Приложите документ текущей фазы
4. Напишите: «Мы на шаге N. Вот где остановились: ...»
