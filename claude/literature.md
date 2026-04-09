# Литература для проекта HeatWin

## Порядок чтения

### Перед фазой 0: Инженерная инфраструктура (обязательно)
16. Cookiecutter Data Science — документация (структура проекта, 10 мин)
17. Git Book — главы 1-3 (init, add, commit, branch, merge)

### Рекомендуется для фазы 0
18. DVC — Get Started (версионирование данных, 20 мин)
19. Pandera — Getting Started (валидация данных, 15 мин)

### Перед Project Brief (обязательно)
1. CRISP-DM Guide
2. Нетбай и др. (статья по теплоснабжению)
3. Data Science for Business — **только глава 2, стр. 19–42** (23 стр.)
11. Designing ML Systems (Huyen) — **только глава 2** (основной источник для framing)

### Перед фазой 2: Data Understanding (обязательно)
4. Forecasting: Principles and Practice — главы 2-3 (TS graphics, decomposition)
5. Python for Data Analysis — главы 5, 7, 9-11 (pandas, cleaning, visualization, TS)
6. Modern Time Series Forecasting with Python — главы 1-4 (EDA for TS, feature primer)
8. Роадмапа — блоки 3, 4.1, 5.1-5.2, 12.5, 12.8 (EDA, распределения, MoM/MLE, GoF, корреляция)

### Дополнительно для фазы 2 (для глубины)
7. ISLR — главы 2, 5.1-5.2 (bias-variance, bootstrap)
13. Storytelling with Data (Knaflic, 2015) — главы 1-4 (упаковка EDA для нетехнической аудитории)
14. Streamlit Documentation + Gallery (бесплатно) — для создания EDA-дашборда

### Перед фазой 3: Data Preparation (обязательно)
5. Modern Time Series Forecasting with Python — главы 4-6 (feature engineering, data prep, first models)
4. Forecasting: Principles and Practice — глава 5 (оценка прогноза, train/test, CV для TS)
6. Python for Data Analysis — главы 7, 11, 12 (cleaning, time series, advanced pandas)
8. Роадмапа — блоки 3.1, 11.1 (construct data, stationarity, differencing)

### Дополнительно для фазы 3 (для глубины)
15. Feature Engineering for ML (Zheng & Casari, O'Reilly, 2018) — numeric features, interactions, selection

### Перед моделированием (фаза 4)
7. An Introduction to Statistical Learning (ISLR) — главы 5, 6, 8 (CV, regularization, boosting)
5. Modern Time Series Forecasting with Python — главы 6-10 (models, evaluation, tuning)
8. Роадмапа — блоки 6, 7, 9, 11.3 (CI, гипотезы, OLS диагностика, PI)

### Дополнительно для фазы 4
20. Interpretable ML (Molnar, бесплатно) — SHAP, permutation importance, PDP
21. Optuna Documentation (бесплатно) — Bayesian hyperparameter tuning
3. Data Science for Business — **глава 3, стр. 43–56** (13 стр., модель как упрощение, overfitting). Опционально: **глава 5, стр. 93–118** (если ISLR тяжёлый)

### Перед оценкой и пилотом (фаза 5)
9. Trustworthy Online Controlled Experiments — главы 1-4, 7, 17 (A/B, CUPED, SRM, pitfalls)
10. Causal Inference: The Mixtape — главы 5, 7, 9 (DAG, ITS, DiD)
8. Роадмапа — блоки 8, 10, 14 (A/B дизайн, причинность, алгоритм тестирования)
3. Data Science for Business — **глава 7, стр. 147–178** (expected value, cost-benefit) + **глава 8, только стр. 195–204** (profit curves)

### Перед деплоем (фаза 6)
11. Designing Machine Learning Systems — главы 7-9 (deployment, distribution shifts, monitoring)
22. FastAPI Documentation (бесплатно) — REST API для inference
23. Docker Documentation — Get Started (бесплатно) — контейнеризация

### Домен (фоном)
12. Нетбай и др. (статья)

---

## Полный каталог

### 1. CRISP-DM Guide (1999)
- **Авторы:** Chapman, Clinton, Kerber et al.
- **Объём:** 76 страниц
- **Доступ:** бесплатно — https://keithmccormick.com/wp-content/uploads/CRISP-DM%20No%20Brand.pdf
- **Фазы проекта:** 1–6 (все)
- **Закрывает:** методология проекта целиком, структура артефактов, итерационный подход, 4 задачи фазы Business Understanding (бизнес-цели, оценка ситуации, цели data mining, project plan)
- **Не закрывает:** ML-специфику (нет feature engineering, train/test split), устарел (1999), нет команды/ролей, нет A/B

### 2. Data Science for Business
- **Авторы:** Foster Provost, Tom Fawcett
- **Издательство:** O'Reilly, 2013
- **Доступ:** платно (требует перевода)
- **Фазы проекта:** 1, 4, 5
- **Читаем 77 стр. из 414 (19%):**
  - **Фаза 1 (сейчас):** Глава 2, стр. 19–42 (23 стр.) — типы DS-задач, «think backwards», перевод бизнеса в DS
  - **Фаза 4 (моделирование):** Глава 3, стр. 43–56 (13 стр.) — модель как упрощение, overfitting интуитивно. Опционально: Глава 5, стр. 93–118 (25 стр.) — только если ISLR тяжёлый
  - **Фаза 5 (evaluation):** Глава 7, стр. 147–178 (31 стр.) — expected value, cost-benefit матрица. Глава 8, **только** стр. 195–204 (10 стр.) — profit curves
- **Пропускаем:** Главы 1, 4, 6, 9–14 (337 стр.) — покрыто ISLR/Huyen или не релевантно для HeatWin
- **Закрывает:** мышление «от бизнеса к модели», cost-benefit ошибок, profit curves
- **Не закрывает:** time series, feature engineering, deployment, MLOps

### 3. bizML Framework
- **Автор:** Harvard Business Review, 2024
- **Доступ:** платно (статья HBR)
- **Фазы проекта:** 1
- **Закрывает:** бизнес-фрейминг ML-проектов, коммуникация с нетехническими стейкхолдерами, современная альтернатива CRISP-DM для фазы 1
- **Не закрывает:** техническую реализацию, data preparation, modeling

### 4. Forecasting: Principles and Practice, 3rd ed.
- **Авторы:** Rob J. Hyndman, George Athanasopoulos
- **Издательство:** OTexts, 2021
- **Доступ:** бесплатно — https://otexts.com/fpp3/
- **Фазы проекта:** 2–4
- **Закрывает:** EDA временных рядов, декомпозиция (тренд, сезонность), ARIMA, exponential smoothing, регрессия для TS, кросс-валидация для TS (walk-forward), метрики прогноза (MAE, RMSE, MAPE), backtesting
- **Не закрывает:** ML-модели (LightGBM, нейросети), feature engineering для gradient boosting, deployment

### 5. Modern Time Series Forecasting with Python
- **Автор:** Manu Joseph
- **Издательство:** Packt, 2022
- **Доступ:** платно
- **Фазы проекта:** 2–4
- **Закрывает:** feature engineering для TS (лаги, rolling stats, calendar features), LightGBM/XGBoost для прогнозирования, SHAP, walk-forward CV, интерпретируемость
- **Не закрывает:** бизнес-фрейминг, deployment, A/B-тестирование

### 6. Python for Data Analysis, 3rd ed.
- **Автор:** Wes McKinney
- **Издательство:** O'Reilly, 2022
- **Доступ:** бесплатно — https://wesmckinney.com/book/
- **Фазы проекта:** 2–3
- **Закрывает:** pandas, numpy, matplotlib — работа с датами, groupby, merge, pivot, визуализации, time series в pandas
- **Не закрывает:** статистику, моделирование, бизнес-логику — чисто инструмент

### 7. An Introduction to Statistical Learning (ISLR), 2nd ed.
- **Авторы:** James, Witten, Hastie, Tibshirani
- **Издательство:** Springer, 2021
- **Доступ:** бесплатно — https://www.statlearning.com/
- **Фазы проекта:** 4
- **Ключевые главы:** Глава 5 (resampling/bootstrap/CV), Глава 8 (tree-based methods)
- **Закрывает:** блоки 5–7 роадмапы (оценивание, CI, гипотезы), регрессия, классификация, bootstrap, model selection, деревья, бустинг
- **Не закрывает:** time series (нет главы!), A/B-тестирование, deployment, Bayesian

### 8. Роадмапа «Математическая статистика и эконометрика для DS»
- **Автор:** t.me/postypashki_old
- **Дата:** March 2026
- **Доступ:** бесплатно
- **Фазы проекта:** 4–5
- **Закрывает:** полный каталог тестов и CI, алгоритм A/B (блок 14), EDA, распределения, оценивание, time series инференс, причинность
- **Не закрывает:** код, примеры, объяснения — это карта знаний, не учебник

### 9. Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing
- **Авторы:** Ron Kohavi, Diane Tang, Ya Xu
- **Издательство:** Cambridge University Press, 2020
- **Доступ:** платно
- **Фазы проекта:** 5
- **Закрывает:** блоки 8, 14 роадмапы — A/B дизайн, CUPED, SRM, variance reduction, множественное тестирование, метрики, guardrails, pitfalls
- **Не закрывает:** ML-моделирование, time series, domain-specific

### 10. Causal Inference: The Mixtape
- **Автор:** Scott Cunningham
- **Издательство:** Yale University Press, 2021
- **Доступ:** бесплатно — https://mixtape.scunning.com/
- **Фазы проекта:** 5
- **Закрывает:** блок 10.2 роадмапы — DAG, DiD (difference-in-differences), IV, RDD, каузальный эффект
- **Не закрывает:** ML, time series forecasting, бизнес-фрейминг

### 11. Designing Machine Learning Systems
- **Автор:** Chip Huyen
- **Издательство:** O'Reilly, 2022
- **Доступ:** платно
- **Фазы проекта:** 1, 3, 6
- **Ключевые главы:** Глава 2 (Framing ML Problems), Глава 5 (Feature Engineering), Главы 7–9 (Deployment, Monitoring, Data Distribution Shifts)
- **Закрывает:** design decisions для ML-систем, мониторинг drift, production trade-offs, framing ML problems
- **Не закрывает:** статистику (CI, гипотезы), time series специфику, A/B-тестирование

### 12. Нетбай Г.В. и др. «Прогнозное управление локальной городской системой теплоснабжения на основе нейросетевого моделирования»
- **Авторы:** Нетбай, Онискив, Столбов, Каримов
- **Журнал:** Вестник ЮУрГУ. Сер. «Компьютерные технологии, управление, радиоэлектроника», 2020, Т.20, №3
- **Доступ:** бесплатно — https://vestnik.susu.ru/ctcr/article/view/10017
- **DOI:** 10.14529/ctcr200303
- **Фазы проекта:** домен + фаза 4
- **Закрывает:** domain knowledge теплосетей, MLP и LSTM для прогноза T котла, реальные данные городской теплосети, benchmark экономии 5–15%, обоснование нейросетевого подхода
- **Не закрывает:** gradient boosting, CI, A/B, deployment

### 13. Storytelling with Data: A Data Visualization Guide for Business Professionals
- **Автор:** Cole Nussbaumer Knaflic
- **Издательство:** Wiley, 2015
- **Доступ:** платно
- **Фазы проекта:** 2 (упаковка), 5 (презентация результатов)
- **Ключевые главы:** Глава 1 (context), Глава 2 (choosing visual), Глава 3 (clutter), Глава 4 (focus attention)
- **Закрывает:** перевод технических визуализаций в понятные для бизнеса, аннотирование графиков, executive summary, принцип explanatory vs exploratory
- **Не закрывает:** статистику, ML, time series — чисто навык коммуникации результатов

### 14. Streamlit Documentation + Gallery
- **Автор:** Streamlit (Snowflake)
- **Доступ:** бесплатно — https://docs.streamlit.io/ + https://streamlit.io/gallery
- **Фазы проекта:** 2 (EDA-дашборд), 5 (результаты модели), 6 (продуктовый дашборд)
- **Что читать:** Get Started (30 мин), Multipage Apps, Layouts and Containers, Chart elements, Deploy
- **Закрывает:** интерактивные дашборды на Python без фронтенд-опыта, деплой на Streamlit Cloud, фильтры и виджеты
- **Не закрывает:** статистику, ML, бизнес-логику — чисто инструмент визуализации
- **Примечание по рынку (2024-2025):** Streamlit — лидер по загрузкам среди Python-дашбордов (972K/мес), востребован в вакансиях DS в РФ и ЕС. Для enterprise/production рассмотреть Plotly Dash или Grafana. Для корпоративного BI в РФ — Power BI, Apache Superset, Metabase.

### 15. Feature Engineering for Machine Learning: Principles and Techniques for Data Scientists
- **Авторы:** Alice Zheng, Amanda Casari
- **Издательство:** O'Reilly, 2018
- **Доступ:** платно
- **Фазы проекта:** 3 (feature engineering)
- **Ключевые главы:** Numeric Features, Interaction Features, Feature Selection
- **Закрывает:** log-трансформации, binning, interaction features, filter/wrapper/embedded selection
- **Не закрывает:** time series специфику (лаги, rolling), deployment, бизнес-фрейминг

### 16. Cookiecutter Data Science — Documentation
- **Автор:** DrivenData
- **Доступ:** бесплатно — https://drivendata.github.io/cookiecutter-data-science/
- **Фазы проекта:** 0 (структура проекта)
- **Что читать:** Opinions + Directory Structure (10 мин)
- **Закрывает:** стандартная структура DS-проекта, разделение notebooks/src/data, принцип «analysis is a DAG»
- **Не закрывает:** статистику, ML, бизнес-логику — чисто организация кода

### 17. Pro Git Book (Scott Chacon, Ben Straub)
- **Доступ:** бесплатно — https://git-scm.com/book/en/v2
- **Фазы проекта:** 0 (Git) → все последующие
- **Что читать:** Главы 1-3 (Getting Started, Git Basics, Branching)
- **Закрывает:** init, add, commit, push, pull, branch, merge, .gitignore, feature branch workflow
- **Не закрывает:** всё остальное — чисто инструмент версионирования кода

### 18. DVC Documentation — Get Started
- **Доступ:** бесплатно — https://dvc.org/doc/start
- **Фазы проекта:** 0 (init) → 2 (raw data) → 3 (processed data) → 4 (models)
- **Что читать:** Get Started (20 мин)
- **Закрывает:** версионирование данных (dvc init, add, push, pull), remote storage, .dvc файлы
- **Не закрывает:** Git (DVC дополняет, не заменяет), ML, статистику

### 19. Pandera Documentation — Getting Started
- **Доступ:** бесплатно — https://pandera.readthedocs.io/en/stable/
- **Фазы проекта:** 0 (setup) → 2 (data quality) → 3 (pipeline validation) → 4 (input validation)
- **Что читать:** Getting Started + DataFrameSchema (25 мин)
- **Закрывает:** декларативная валидация DataFrames, типы колонок, ограничения, интеграция в pipeline
- **Не закрывает:** статистику, ML — чисто инструмент контроля качества данных

### 20. Interpretable Machine Learning: A Guide for Making Black Box Models Explainable
- **Автор:** Christoph Molnar
- **Доступ:** бесплатно — https://christophm.github.io/interpretable-ml-book/
- **Фазы проекта:** 4 (интерпретируемость)
- **Что читать:** SHAP, Permutation Importance, PDP, ICE
- **Закрывает:** SHAP values, summary/dependence/waterfall plots, permutation importance, partial dependence
- **Не закрывает:** causality (SHAP ≠ причинность), deployment, бизнес-фрейминг

### 21. Optuna Documentation
- **Доступ:** бесплатно — https://optuna.readthedocs.io/
- **Фазы проекта:** 4 (hyperparameter tuning)
- **Что читать:** Tutorial (30 мин), LightGBM integration, MLflow integration
- **Закрывает:** Bayesian optimization (TPE), pruning, study/trial API, визуализация optimization history
- **Не закрывает:** статистику, ML-теорию — чисто инструмент оптимизации

### 22. FastAPI Documentation
- **Доступ:** бесплатно — https://fastapi.tiangolo.com/
- **Фазы проекта:** 6 (API)
- **Что читать:** Tutorial - User Guide (1-2 часа)
- **Закрывает:** REST API на Python, Pydantic validation, async, auto-docs (Swagger), TestClient
- **Не закрывает:** ML, статистику, бизнес-логику — чисто инструмент

### 23. Docker Documentation — Get Started
- **Доступ:** бесплатно — https://docs.docker.com/get-started/
- **Фазы проекта:** 0 (init), 6 (full containerization)
- **Что читать:** Parts 1-4 (30 мин)
- **Закрывает:** Dockerfile, docker-compose, build, run, volumes, ports
- **Не закрывает:** Kubernetes, CI/CD, cloud deploy — только локальная контейнеризация
