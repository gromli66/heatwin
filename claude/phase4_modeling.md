# Фаза 4: Modeling — чеклист

## Вход в фазу
- **Фаза 0 действует:** Git (feature branches), DVC (processed data tracked), Pandera, Makefile, MLflow setup
- Фаза 3 завершена: feature pipeline работает, train/val/test готовы
- Feature Dictionary заполнен — каждый feature с формулой и обоснованием
- Data leakage проверен и исключён
- Baseline можно посчитать: naive forecast и OLS подготовлены

## Источник фазы
CRISP-DM Phase 4 — 4 задачи:
1. Select Modeling Techniques → Modeling Technique, Modeling Assumptions
2. Generate Test Design → Test Design
3. Build Model → Parameter Settings, Models, Model Description
4. Assess Model → Model Assessment, Revised Parameter Settings

Добавлены задачи (не из CRISP-DM):
5. Hyperparameter Tuning → Best Parameters (из ML практики)
6. Interpretability → SHAP Analysis (из XAI)
7. Uncertainty Quantification → Prediction Intervals (из роадмапы блок 6)

---

## Задача 4.1: Выбор моделей и обоснование (Select Modeling Techniques)

### Что делаем
Определяем набор моделей для сравнения — от простых baseline до целевых.

### Пирамида моделей (от простого к сложному)

| Уровень | Модель | Зачем | Ожидание |
|---|---|---|---|
| **Baseline 1** | Naive forecast: T_return(t+6) = T_return(t) | Нижняя граница — если модель не бьёт naive, она бесполезна | MAE ~ 3-5°C |
| **Baseline 2** | Seasonal naive: T_return(t+6) = T_return(t - 24 + 6) | Учитывает суточный паттерн | MAE ~ 2-4°C |
| **Baseline 3** | ARIMA(p,d,q): авторегрессия без external features | Может ли чисто TS-модель конкурировать? Если да — features не добавляют инф. | MAE ~ 2-3°C |
| **Linear** | OLS: T_return ~ T_supply + T_outdoor + lags | Проверяет линейную гипотезу, диагностика остатков (Breusch-Pagan, DW) | MAE ~ 2-3°C |
| **Regularized** | Ridge / Lasso | Feature selection через L1, устойчивость через L2 | MAE ~ 1.5-2.5°C |
| **Tree-based** | LightGBM | Основная модель: быстрый, обрабатывает нелинейности, не нужен scaling | MAE < 2°C (цель) |
| **Tree-based** | XGBoost | Сравнение с LightGBM — литература показывает чуть выше точность, но медленнее | MAE < 2°C (цель) |
| **Deep** | LSTM (опционально) | Только если tree-based не достигает цели — сложнее, дольше, менее интерпретируем | ? |

### Обоснование выбора (привязка к литературе)
- LightGBM/XGBoost: Нетбай и др. (2020) показали экономию 5-15% с нейросетями; XAI4HEAT (2025) использовал tree-based модели с CVRMSE ~10.5%; литературный обзор из Research Report подтверждает — XGBoost наивысшая точность, LightGBM быстрее
- OLS как baseline: блок 9 роадмапы — обязательная диагностика остатков перед ML
- Naive forecast: Hyndman fpp3 — «если вы не можете побить naive, ваша модель бесполезна»

### Допущения каждой модели
| Модель | Допущения | Проверяем в фазе 3/4 |
|---|---|---|
| OLS | Линейность, гомоскедастичность, независимость остатков, нормальность остатков | Breusch-Pagan, Durbin-Watson, QQ-plot остатков |
| Ridge/Lasso | Те же + нужен scaling | StandardScaler fit на train |
| LightGBM | Нет строгих допущений, но: нет data leakage, features информативны | Feature importance, SHAP |
| XGBoost | Аналогично LightGBM | Feature importance, SHAP |
| LSTM | Достаточно данных для обучения, стационарность не обязательна | → определяется в фазе 3 |

### Блоки роадмапы
- **9.1**: OLS — коэффициенты, R², интерпретация
- **9.2**: диагностика остатков — Breusch-Pagan, DW, heteroscedasticity-robust SE (HAC)
- **9.3**: GLM — если energy как таргет (Gamma family)
- **11.1**: time series — ARIMA как дополнительный baseline (опционально)

### Чеклист готовности
- [ ] Пирамида моделей определена (минимум: naive + seasonal naive + ARIMA + OLS + LightGBM)
- [ ] ARIMA включён как TS-baseline (блок 11.1) — auto_arima или ручной подбор (p,d,q) по ACF/PACF
- [ ] Для каждой модели записано обоснование выбора (ссылка на литературу или EDA)
- [ ] Допущения каждой модели записаны — и план их проверки
- [ ] Записано: какую модель пробуем первой (рекомендация: naive → ARIMA → OLS → LightGBM)
- [ ] LSTM — решение: включаем или нет (и почему)

---

## Задача 4.2: Дизайн экспериментов (Generate Test Design)

### Что делаем

#### 4.2.1 Валидационная стратегия

**Walk-forward (expanding window)** — золотой стандарт для TS:
```
Fold 1: Train [сезон 1]              → Val [сезон 2]
Fold 2: Train [сезон 1-2]            → Val [сезон 3]
Fold 3: Train [сезон 1-3]            → Val [сезон 4]
Final:  Train [сезон 1-4]            → Test [сезон 5]
```

Альтернатива — **sliding window** (фиксированный размер train):
```
Fold 1: Train [сезон 1-2]  → Val [сезон 3]
Fold 2: Train [сезон 2-3]  → Val [сезон 4]
Final:  Train [сезон 3-4]  → Test [сезон 5]
```

Выбор зависит от: наличия structural change-point (sliding лучше если есть), количества сезонов (expanding если мало), вычислительного бюджета.

→ **Определяется в фазе 3:** количество fold'ов = количество сезонов - 1

#### 4.2.2 Метрики оценки

Из контракта метрик (Project Brief раздел 3.3):

| Метрика | Формула | Что показывает | Порог успеха |
|---|---|---|---|
| MAE | mean(abs(y - ŷ)) | Средняя ошибка в °C — главная метрика | < 2°C |
| RMSE | sqrt(mean((y - ŷ)²)) | Штрафует за большие ошибки сильнее | < 3°C |
| R² | 1 - SS_res / SS_tot | Доля объяснённой дисперсии | > 0.85 |
| MAPE | mean(abs(y - ŷ) / y) × 100 | Процентная ошибка — осторожно при y ≈ 0 | информативная |
| Coverage PI | % наблюдений внутри prediction interval | Калибровка неопределённости | ≥ 90% |

Дополнительные (диагностические):
| Метрика | Что показывает |
|---|---|
| MAE по подстанциям | Есть ли подстанция, на которой модель хуже? |
| MAE по часам суток | Есть ли часы, когда модель ошибается больше? |
| MAE по T_outdoor bins | Модель ломается в морозы или в тепло? |
| Residuals autocorrelation | Ljung-Box на остатках — есть ли паттерн, который модель не поймала? |

#### 4.2.3 Baseline evaluation

Перед запуском ML-моделей — посчитать baseline:
- Naive MAE = ?
- Seasonal naive MAE = ?
- ARIMA MAE = ? (auto_arima из pmdarima или statsmodels)
- OLS MAE = ?

Эти числа — нижняя планка. ML-модель должна бить все четыре.

#### 4.2.4 Формальный шаблон гипотезы (блок 14.1 роадмапы)

**Перед каждым статистическим тестом** заполнить шаблон:

| Поле | Пример |
|---|---|
| Вопрос | LightGBM точнее XGBoost? |
| H₀ | MAE(LightGBM) = MAE(XGBoost) |
| H₁ | MAE(LightGBM) < MAE(XGBoost) (односторонняя) |
| α | 0.05 |
| Тест | Paired permutation test (10000 перестановок) на fold-level MAE |
| Размер выборки | K fold'ов (→ определяется в фазе 3) |
| Решающее правило | Если p < 0.05 → отвергаем H₀, LightGBM значимо лучше |
| Результат | p = ?, решение = ? |

**Этот шаблон заполняется для КАЖДОГО теста в фазах 4-5:**
- Сравнение моделей (permutation test, DM-test)
- Нормальность остатков (Shapiro-Wilk)
- Гомоскедастичность (Breusch-Pagan)
- Автокорреляция остатков (Ljung-Box)
- Различие между подстанциями (Kruskal-Wallis)
- Change-point (CUSUM)

### Блоки роадмапы
- **6.1**: CI для метрик — bootstrap BCa для MAE/RMSE (не точечная оценка, а интервал)
- **7.1-7.3**: формулировка гипотез — H₀: MAE(LightGBM) = MAE(OLS), H₁: MAE(LightGBM) < MAE(OLS)
- **11.1**: walk-forward CV специфика, ARIMA baseline
- **14.1**: формализация гипотезы — шаблон H₀/H₁/α/тест/решение
- **14.2**: контракт метрик — primary, guardrail, secondary

### Чеклист готовности
- [ ] Валидационная стратегия выбрана: walk-forward / sliding window
- [ ] Количество fold'ов определено → определяется в фазе 3
- [ ] Все метрики из контракта метрик реализованы в коде (функция evaluate_model())
- [ ] Диагностические метрики (по подстанциям, часам, T_outdoor) реализованы
- [ ] Baseline (naive, seasonal naive, ARIMA, OLS) посчитаны — числа записаны
- [ ] Baseline залогирован в MLflow как первый эксперимент
- [ ] **Шаблон гипотезы** (14.1) заполнен для каждого запланированного теста (минимум 6 шаблонов)

---

## Задача 4.3: Обучение моделей (Build Model)

### Что делаем

#### 4.3.1 Порядок обучения (от простого к сложному)

**Итерация 1: OLS baseline**
- Обучить OLS на top-10 features (по корреляции с таргетом из EDA)
- Диагностика остатков (полный протокол — блок 9.2):
  1. Breusch-Pagan → шаблон 14.1: H₀ = гомоскедастичность, α = 0.05
  2. Если BP p < 0.05 → пересчитать SE через HAC Newey-West → записать оба варианта SE
  3. Durbin-Watson → шаблон 14.1: H₀ = нет автокорреляции 1-го порядка
  4. Если DW ≈ 0 или ≈ 4 → автокорреляция → HAC SE обязателен
  5. QQ-plot остатков + Shapiro-Wilk на остатках → шаблон 14.1: H₀ = нормальность
  6. Если SW p < 0.05 → GoF-тест: KS-тест на остатках с подбором распределения (Normal vs t vs Laplace)
- Записать MAE, RMSE, R² → MLflow run #1
- Записать: какие допущения нарушены и как это влияет

**Итерация 1.5: ARIMA baseline (блок 11.1)**
- auto_arima (pmdarima) или ручной подбор (p,d,q) по ACF/PACF из EDA
- Обучить только на T_return (без external features) — проверяет: даёт ли feature engineering прибавку?
- Записать MAE, RMSE → MLflow run #1.5
- Сравнить с naive и OLS: если ARIMA ≈ OLS → features не добавляют информации, нужно пересмотреть feature engineering
- DM-тест: ARIMA vs naive → шаблон 14.1

**Итерация 2: LightGBM с дефолтными параметрами**
- Обучить на всех features из Feature Dictionary
- → определяется в фазе 3: конкретный список features (30-80)
- Записать MAE, RMSE, R² → MLflow run #2
- Сравнить с OLS: лучше? На сколько?

**Итерация 3: XGBoost с дефолтными параметрами**
- Аналогично LightGBM
- Записать → MLflow run #3
- Сравнить с LightGBM: лучше? На сколько?

**Итерация 4: Feature selection**
- SHAP values для лучшей модели из итерации 2-3
- Отбросить features с |SHAP| ≈ 0
- Переобучить с reduced feature set
- Записать → MLflow run #4
- Сравнить: потеряли ли точность? Если нет — оставить reduced set (проще = лучше)

**Итерация 4.5: Ручной подбор гиперпараметров (обучение перед Optuna)**

Цель: понять что каждый параметр делает, прежде чем отдать поиск Optuna. Без этого Optuna — чёрный ящик.

Для LightGBM (или лучшей модели из итераций 2-3):

| Параметр | Дефолт | Попробовать | Что влияет |
|---|---|---|---|
| n_estimators | 100 | 500, 1000, 2000 | Больше = точнее, но медленнее. С early_stopping = автоматически |
| learning_rate | 0.1 | 0.01, 0.05, 0.1 | Ниже = точнее, но нужно больше деревьев |
| max_depth | -1 (нет) | 5, 7, 10, 15 | Ограничивает сложность, защита от переобучения |
| num_leaves | 31 | 15, 31, 63, 127 | Альтернатива max_depth для LightGBM (leaf-wise) |
| min_child_samples | 20 | 5, 20, 50, 100 | Минимум строк в листе, регуляризация |
| subsample | 1.0 | 0.7, 0.8, 0.9 | Доля строк для каждого дерева (bagging) |
| colsample_bytree | 1.0 | 0.7, 0.8, 0.9 | Доля features для каждого дерева |
| reg_alpha | 0 | 0, 0.1, 1.0 | L1 регуляризация |
| reg_lambda | 0 | 0, 0.1, 1.0 | L2 регуляризация |

Процедура:
1. Менять ОДИН параметр за раз, остальные фиксированы
2. Для каждого значения — запустить walk-forward CV, записать MAE
3. Построить графики: параметр vs MAE (понять кривую — где plateau, где overfitting)
4. Зафиксировать «разумный диапазон» для каждого параметра → передать Optuna
5. Записать наблюдения: «learning_rate < 0.01 не улучшает, max_depth > 10 переобучает»

Это НЕ замена Optuna — это обучение + определение search space для Optuna.

- Записать лучшую ручную конфигурацию → MLflow run #4.5
- Сравнить с дефолтами: на сколько улучшилось ручным подбором?

**Итерация 5: Hyperparameter tuning** (задача 4.5) — Optuna использует search space из итерации 4.5

**Итерация 6 (опционально): LSTM**
- Только если tree-based не достигает MAE < 2°C
- → определяется по результатам итераций 2-5

#### 4.3.2 MLflow logging для каждого эксперимента

```python
with mlflow.start_run(run_name="lightgbm_v1_default"):
    # Параметры
    mlflow.log_params({
        "model": "LightGBM",
        "n_features": len(feature_list),
        "horizon_h": 6,
        "train_period": "2019-2022",
        "val_period": "2022-2023",
        "test_period": "2023-2024",
    })
    # Метрики
    mlflow.log_metrics({
        "val_mae": val_mae,
        "val_rmse": val_rmse,
        "val_r2": val_r2,
        "test_mae": test_mae,  # только для финальной модели
    })
    # Артефакты
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_artifact("residuals_plot.png")
    mlflow.sklearn.log_model(model, "model")
```

### Блоки роадмапы
- **9.1**: OLS — fit, коэффициенты, p-value, R²
- **9.2**: диагностика остатков — Breusch-Pagan, DW, QQ-plot
- **9.4** (если применимо): GLM Gamma для energy

### Чеклист готовности
- [ ] OLS обучен, полная диагностика остатков выполнена (BP → HAC SE если нужно → DW → SW), результаты в MLflow
- [ ] ARIMA baseline обучен (auto_arima), MAE записан, DM-test vs naive выполнен
- [ ] LightGBM с дефолтами обучен, результаты в MLflow
- [ ] XGBoost с дефолтами обучен, результаты в MLflow
- [ ] Все модели сравнены — записано какая лучше и на сколько
- [ ] DM-test: ARIMA vs лучшая ML-модель — features дают прибавку? (если нет — пересмотреть FE)
- [ ] Feature selection через SHAP — reduced set определён
- [ ] Post-processing: сглаживание протестировано, MAE с/без сглаживания сравнены
- [ ] Каждый эксперимент в MLflow: параметры, метрики, артефакты
- [ ] Каждое сравнение — через шаблон 14.1 (H₀/H₁/α/тест/p-value/решение)
- [ ] Git commit для каждой итерации: `model: add OLS baseline`, `model: add ARIMA`, `model: add LightGBM v1`

#### 4.3.5 Post-processing предсказаний (из Нетбая)

Нетбай (2020) применял оконное сглаживание (алгоритм Ханна) к предсказаниям для устранения рваности.

Для HeatWin — после получения предсказаний лучшей модели:
- Применить скользящее среднее (window=3, 5, 7) к ряду предсказаний
- Экспоненциальное сглаживание (EWM) как альтернатива
- Сравнить MAE с и без сглаживания (на val set)
- Если сглаживание улучшает MAE → включить в pipeline. Если нет → не включать
- **ВНИМАНИЕ:** сглаживание добавляет задержку. Для оперативного управления (период 3ч) это может быть критично. Для прогноза на 6ч — скорее допустимо
- Визуализация: график «raw predictions vs smoothed vs actual» на характерной неделе

---

## Задача 4.4: Оценка моделей (Assess Model)

### Что делаем

#### 4.4.1 Сравнение моделей

Таблица результатов (заполняется по ходу):

| Модель | Val MAE | Val RMSE | Val R² | Test MAE | Test RMSE | Test R² | Комментарий |
|---|---|---|---|---|---|---|---|
| Naive | ? | ? | ? | ? | ? | ? | baseline |
| Seasonal naive | ? | ? | ? | ? | ? | ? | baseline |
| ARIMA | ? | ? | ? | ? | ? | ? | TS-baseline (без external features) |
| OLS (top-10) | ? | ? | ? | ? | ? | ? | линейный baseline |
| LightGBM default | ? | ? | ? | ? | ? | ? | |
| XGBoost default | ? | ? | ? | ? | ? | ? | |
| Best tuned | ? | ? | ? | ? | ? | ? | после 4.5 |
| Best reduced | ? | ? | ? | ? | ? | ? | после feature selection |

→ Test-метрики считаем ТОЛЬКО для финальной модели (иначе — overfitting на test)

#### 4.4.2 Статистическое сравнение моделей

Не «MAE модели A = 1.8, модели B = 1.9, значит A лучше». А: «статистически ли разница значима?»

Каждое сравнение — через шаблон 14.1 (из задачи 4.2.4):

- **Paired permutation test:** H₀: MAE(LightGBM) = MAE(XGBoost), на fold-level ошибках → шаблон 14.1
- **Diebold-Mariano test:** специфичный для прогнозов — H₀: прогнозы одинаково точны → шаблон 14.1
- **DM-test: ARIMA vs LightGBM** — доказывает что features дают прибавку сверх авторегрессии → шаблон 14.1
- **Bootstrap CI для разности MAE:** BCa bootstrap для (MAE_A - MAE_B), если 0 не в CI — значимая разница
- Если > 2 моделей сравниваются → BH-коррекция FDR (блок 12.7)

→ Блок 7 роадмапы: формулировка гипотезы, выбор теста, p-value, вывод

#### 4.4.3 Диагностика остатков лучшей модели (расширенная)

**Визуальная диагностика:**
- **Residuals plot:** ŷ vs residuals — нет ли паттерна?
- **Residuals ACF:** Ljung-Box — нет ли автокорреляции в ошибках? → шаблон 14.1: H₀ = нет автокорреляции
- **Residuals по подстанциям:** box-plot — одинаково ли хорошо на всех?
- **Residuals по часам:** есть ли часы, когда модель систематически ошибается?
- **Residuals по T_outdoor bins:** ломается ли модель в экстремальных температурах?
- **Residuals vs T_outdoor:** нет ли гетероскедастичности (ошибки растут с T_outdoor)?
- **Residuals по времени (temporal):** нет ли тренда в ошибках? → ведёт к CUSUM (4.4.6)

**Формальные тесты на остатках (блоки 12.5, 12.6, 12.10 — пропущенные ранее):**

#### 4.4.4 GoF-тест на остатках (блок 12.5)

Те же тесты, что в EDA (фаза 2), но теперь на остатках модели, не на raw data:
- **Shapiro-Wilk** на остатках → шаблон 14.1: H₀ = остатки нормальные
- Если p < 0.05 (не нормальные) → **KS-тест** с подбором: Normal vs t-distribution vs Laplace
- **QQ-plot остатков** с fitted distribution (не только Normal)
- Зачем: нормальность остатков влияет на (а) корректность OLS CI, (б) калибровку parametric PI, (в) выбор между parametric и conformal PI

#### 4.4.5 Kruskal-Wallis + Dunn post-hoc по подстанциям (блок 12.6)

Формальная проверка: «отличается ли качество модели между подстанциями?»
- **Kruskal-Wallis** на |residuals| по группам (substation) → шаблон 14.1: H₀ = медианы |residuals| одинаковы для всех подстанций
- Если p < 0.05 → **Dunn post-hoc** с BH-коррекцией FDR → какие пары подстанций значимо различаются
- Зачем: если L22 значимо хуже — рассмотреть отдельную модель или исключить из MVP
- Это из пет-проект плана (этап 3) — потеряно при переносе, восстановлено

#### 4.4.6 CUSUM на остатках (блок 12.10)

Change-point detection не в raw data (это EDA), а в ошибках модели:
- **CUSUM** на cumulative sum of residuals → шаблон 14.1: H₀ = нет сдвига в среднем остатков
- Визуализация: CUSUM chart с control limits
- Зачем: если CUSUM показывает сдвиг → модель деградирует в определённый период → concept drift
- Это фундамент мониторинга в фазе 6 — если drift обнаружен на историческом test set, нужна стратегия переобучения

#### 4.4.7 Проверка на overfitting

- Train MAE ≈ Val MAE? Если train MAE << val MAE — overfitting
- Learning curves: MAE vs размер train set — убывает ли?
- Cross-validation variance: MAE на разных fold'ах — стабильна ли?

#### 4.4.8 MDE / Power analysis (блок 14.4)

По результатам модели рассчитать:
- Дисперсия остатков σ² = var(residuals) на val set
- При данном σ и размере test set: **MDE** (minimal detectable effect) при power = 80%, α = 0.05
- Формула (для простого сравнения средних): MDE = (z_α + z_β) × σ × √(2/n)
- Интерпретация: «модель может обнаружить разницу ≥ X°C с 80% вероятностью»
- Перевод в бизнес: «если экономия < X°C — мы не сможем её доказать с текущими данными»
- Зачем: (а) обоснование достаточности данных, (б) дизайн пилота (фаза 5), (в) честная оценка: если MDE > 2°C при σ из данных — нужно больше данных или другой дизайн
- Связь с контрактом метрик: MDE должна быть < заявленного эффекта 5% (≈ X°C в абсолютных единицах)

### Блоки роадмапы
- **7.1-7.3**: гипотезы — paired permutation test, DM-test (каждый через шаблон 14.1)
- **6.1**: bootstrap BCa для CI разности метрик
- **9.2**: диагностика остатков OLS — BP, DW, HAC SE
- **11.1**: Ljung-Box для остатков, DM-test для ARIMA vs ML
- **12.5**: GoF-тесты на остатках — Shapiro-Wilk, KS с подбором распределения
- **12.6**: Kruskal-Wallis + Dunn post-hoc по подстанциям
- **12.7**: множественные сравнения — BH-коррекция FDR
- **12.10**: CUSUM на остатках — change-point / concept drift
- **14.1**: формальный шаблон H₀/H₁/α для каждого теста
- **14.4**: MDE / power analysis

### Чеклист готовности
- [ ] Таблица сравнения моделей заполнена (val-метрики для всех, test — только для финальной)
- [ ] Каждое сравнение оформлено через шаблон 14.1 (H₀, H₁, α, тест, p-value, решение)
- [ ] Paired permutation test или DM-test выполнен для top-2 моделей
- [ ] DM-test: ARIMA vs лучшая ML-модель — доказано что features дают прибавку
- [ ] Bootstrap CI для разности MAE рассчитан
- [ ] BH-коррекция применена если > 2 сравнений
- [ ] **GoF на остатках:** Shapiro-Wilk выполнен → шаблон 14.1 заполнен
- [ ] **GoF расширенный:** если не нормальные → KS-тест с альтернативными распределениями
- [ ] **Kruskal-Wallis** на |residuals| по подстанциям → шаблон 14.1 заполнен
- [ ] Если KW p < 0.05 → **Dunn post-hoc** с BH-коррекцией → пары записаны
- [ ] **CUSUM** на остатках по времени — change-point найден / не найден → шаблон 14.1
- [ ] Residuals plot для лучшей модели — нет систематического паттерна
- [ ] Ljung-Box на остатках → шаблон 14.1 заполнен
- [ ] Residuals по подстанциям/часам/T_outdoor — слабые места модели задокументированы
- [ ] Overfitting check: train MAE vs val MAE — разница < 20%
- [ ] **MDE рассчитан:** при текущем σ, MDE = ? °C при power 80%
- [ ] **MDE vs бизнес-эффект:** MDE < заявленного эффекта 5%? Если нет — задокументировано

---

## Задача 4.5: Hyperparameter Tuning (не из CRISP-DM)

### Что делаем

#### Инструмент: Optuna (рекомендация)
- Bayesian optimization — эффективнее grid/random search
- Pruning — рано останавливает плохие trial'ы
- Интеграция с MLflow — каждый trial логируется

#### Search space (стартовый, для LightGBM)
```python
{
    "n_estimators": (100, 2000),
    "learning_rate": (0.01, 0.3, log=True),
    "max_depth": (3, 12),
    "num_leaves": (15, 127),
    "min_child_samples": (5, 100),
    "subsample": (0.5, 1.0),
    "colsample_bytree": (0.5, 1.0),
    "reg_alpha": (1e-8, 10, log=True),
    "reg_lambda": (1e-8, 10, log=True),
}
```
→ Конкретные границы определяются в фазе 3-4 по масштабу данных

#### Бюджет
- n_trials = 100-200 (для Optuna с pruning — достаточно)
- CV = walk-forward (каждый trial оценивается на всех fold'ах)
- Время: ~1-4 часа на обычном железе для LightGBM

### Блоки роадмапы
- **5.2**: MLE — Optuna по сути ищет максимум likelihood (или минимум loss)
- **14.4**: MDE/power — tuning влияет на финальную точность, которая определяет реалистичность MDE

### Чеклист готовности
- [ ] Ручной подбор (итерация 4.5) выполнен: графики «параметр vs MAE» для ключевых параметров
- [ ] Search space для Optuna сужен на основе ручного подбора
- [ ] Optuna study создан и подключён к MLflow
- [ ] Search space определён для лучшей модели из задачи 4.3
- [ ] n_trials выполнено (минимум 50, рекомендуется 100+)
- [ ] Best trial записан: параметры, val MAE
- [ ] Модель переобучена с best params на полном train — финальный val MAE записан
- [ ] Сравнение: tuned vs default — на сколько улучшилось?

---

## Задача 4.6: Интерпретируемость (не из CRISP-DM — из XAI)

### Что делаем

#### 4.6.1 Feature Importance
- LightGBM built-in importance (gain, split)
- Permutation importance (model-agnostic — надёжнее)
- Топ-15 features — визуализация bar chart

#### 4.6.2 SHAP Analysis
- SHAP summary plot (beeswarm) — какие features важны и как влияют
- SHAP dependence plots для top-5 features — нелинейные зависимости
- SHAP interaction plots (если время позволяет) — взаимодействия features
- SHAP waterfall для конкретных предсказаний — «почему модель дала 52°C в этот час?»

#### 4.6.3 Бизнес-интерпретация
- Перевод SHAP в язык оператора: «модель считает, что T_return будет высокой, потому что: (1) вчера в это время T_return тоже была высокой, (2) на улице потеплело на 5°C за 3 часа»
- Проверка здравого смысла: совпадает ли feature importance с domain knowledge оператора?
- Если не совпадает — красный флаг: либо модель нашла что-то новое, либо data leakage

### Блоки роадмапы
- **10.1** (частично): причинность — SHAP показывает association, не causation, но помогает строить гипотезы

### Чеклист готовности
- [ ] Feature importance (gain + permutation) рассчитана и визуализирована
- [ ] SHAP summary plot построен — top-15 features
- [ ] SHAP dependence plot для top-5 features
- [ ] Минимум 2 SHAP waterfall для конкретных предсказаний (хороший прогноз + плохой прогноз)
- [ ] Бизнес-интерпретация: для каждого из top-5 features — объяснение на языке оператора
- [ ] Sanity check: feature importance совпадает с domain knowledge? Если нет — задокументировано почему

---

## Задача 4.7: Quantification of Uncertainty (не из CRISP-DM — из роадмапы)

### Что делаем

#### 4.7.1 Conformal Prediction Intervals
- Split conformal: calibration set = val set, test set для оценки coverage
- Для каждого предсказания ŷ: интервал [ŷ - q, ŷ + q] где q = quantile(|y_cal - ŷ_cal|, 1-α)
- Target coverage: 90% (α = 0.10) — из контракта метрик

#### 4.7.2 Bootstrap CI для метрик модели
- Bootstrap BCa для MAE: «MAE = 1.7°C, 95% CI [1.5, 1.9]»
- Bootstrap BCa для R²: «R² = 0.91, 95% CI [0.88, 0.93]»
- Это не CI для предсказаний — это CI для оценки качества модели

#### 4.7.3 Calibration plot
- Predicted coverage vs actual coverage для разных α (0.01, 0.05, 0.10, 0.20, 0.50)
- Идеальная модель: точки на диагонали
- Если систематически ниже — интервалы слишком узкие (overconfident)

### Блоки роадмапы
- **6.1**: bootstrap BCa — конструирование CI
- **6.2**: conformal prediction — distribution-free, finite-sample coverage guarantee
- **11.3**: prediction intervals для TS (PI vs CI)
- **14.3**: UQ в контексте A/B — нужно для power analysis

### Чеклист готовности
- [ ] Conformal PI построены с target coverage 90%
- [ ] Actual coverage на test set посчитана — записана (должна быть ≥ 90%)
- [ ] Bootstrap BCa для MAE и RMSE — точечная оценка + 95% CI
- [ ] Calibration plot построен — модель калибрована / overconfident / underconfident
- [ ] PI визуализированы: прогноз ± интервал на нескольких днях из test set

---

## Задача 4.8: Упаковка результатов

### Выход 1: Modeling Notebook (для технического рецензента)
- Все эксперименты с кодом
- MLflow UI screenshot или ссылка
- Таблица сравнения моделей
- Диагностика и SHAP
- Conformal PI и calibration

### Выход 2: Modeling Summary Report (для нетехнического стейкхолдера)
- 3-5 страниц без кода:
  1. «Мы попробовали 5 подходов, лучший — LightGBM с MAE = X°C»
  2. Аннотированный график: прогноз vs факт на неделе из test set
  3. «Модель считает главными факторами: (1) вчерашняя обратка, (2) температура на улице, (3) время суток» — SHAP на языке оператора
  4. «Прогноз с полосой неопределённости: модель уверена на 90%, что T_return будет между X и Y°C»
  5. «Потенциал экономии: в Z% часов модель обнаруживает перетоп, что соответствует W тыс. руб/сезон»

### Выход 3: Обновление дашборда
- Новая вкладка в Streamlit-дашборде: Model Results
  - Selector: модель, подстанция, период
  - График: прогноз vs факт + PI
  - Таблица метрик
  - SHAP summary

### Чеклист готовности упаковки
- [ ] Modeling Notebook чистый — Kernel Restart & Run All работает
- [ ] MLflow содержит все эксперименты с параметрами и метриками
- [ ] Modeling Summary Report готов (3-5 стр., без кода)
- [ ] Дашборд обновлён — вкладка Model Results работает
- [ ] Минимум 1 визуализация «прогноз vs факт» аннотирована для нетехнической аудитории

---

## Gate criteria: переход в фазу 5 (Evaluation)

### Техническая полнота
- [ ] Baseline посчитаны (naive, seasonal naive, ARIMA, OLS) — MAE записаны
- [ ] ARIMA baseline включён — DM-test vs naive выполнен
- [ ] Минимум 2 ML-модели обучены (LightGBM + XGBoost)
- [ ] Лучшая модель бьёт все baseline статистически значимо (permutation test или DM-test, p < 0.05)
- [ ] MAE < 2°C на val set (из контракта метрик) — или зафиксировано что не достигнуто
- [ ] Conformal PI coverage ≥ 90% — или зафиксировано что не достигнуто
- [ ] SHAP analysis выполнен — top-10 features задокументированы
- [ ] Residuals diagnostics пройдены — систематические ошибки задокументированы

### Статистическая строгость (блоки 12, 14)
- [ ] Каждый тест оформлен через шаблон 14.1 (H₀/H₁/α/тест/p-value/решение)
- [ ] GoF на остатках: Shapiro-Wilk (12.5) выполнен, распределение определено
- [ ] Kruskal-Wallis + Dunn (12.6): качество модели по подстанциям проверено
- [ ] CUSUM на остатках (12.10): concept drift проверен
- [ ] MDE / Power analysis (14.4): рассчитан, сравнён с заявленным эффектом 5%

### Воспроизводимость
- [ ] Все эксперименты в MLflow с параметрами, метриками, артефактами
- [ ] Лучшая модель сохранена (pickle/joblib или MLflow model)
- [ ] Random seed фиксирован — результаты воспроизводимы
- [ ] Git commits для каждой итерации моделирования

### Упаковка
- [ ] Modeling Summary Report готов для нетехнической аудитории
- [ ] Дашборд обновлён с вкладкой Model Results
- [ ] Прогноз vs факт аннотирован

### Готовность к пилоту
- [ ] Лучшая модель определена — записаны параметры, features, метрики
- [ ] Экономическая оценка: сколько перетопа обнаружила модель → сколько рублей
- [ ] Guardrail проверен: модель НЕ рекомендует режимы ниже T_return_min
- [ ] Bootstrap CI для MAE — точечная оценка + интервал для презентации клиенту
- [ ] MDE < заявленного эффекта — или задокументировано что данных недостаточно

---

## Литература для фазы 4

### Обязательно

#### Л.1: ISLR — главы 5, 6, 8
- **Доступ:** бесплатно — https://www.statlearning.com/
- **Что читать:** Глава 5 (Resampling: CV, Bootstrap), Глава 6 (Regularization: Ridge, Lasso), Глава 8 (Tree-Based Methods: Bagging, Boosting)
- **Для каких задач:** 4.1 (выбор моделей), 4.2 (CV), 4.3 (обучение), 4.4 (оценка)
- **Блоки роадмапы:** 6.1 (bootstrap), 9.1 (regression), блок деревьев

**Чеклист понимания:**
- [ ] Могу объяснить bias-variance tradeoff для OLS vs LightGBM
- [ ] Понимаю разницу Ridge vs Lasso и когда какой (Lasso для feature selection, Ridge для мультиколлинеарности)
- [ ] Могу объяснить boosting: последовательное обучение деревьев на остатках предыдущих
- [ ] Знаю, что такое learning rate в boosting и как он связан с n_estimators (trade-off)
- [ ] Понимаю OOB error для random forest и почему для boosting нужен hold-out

#### Л.2: Modern TS Forecasting with Python — главы 6-10
- **Автор:** Manu Joseph
- **Доступ:** платно (Packt)
- **Что читать:** Главы 6-10: Linear Models, Tree-Based, Deep Learning, Forecasting Strategies, Evaluation
- **Для каких задач:** 4.3 (обучение), 4.4 (оценка), 4.5 (tuning)
- **Блоки роадмапы:** 11.1

**Чеклист понимания:**
- [ ] Знаю, чем direct forecasting (отдельная модель на каждый h) отличается от recursive (модель предсказывает на 1 шаг, потом использует свой прогноз)
- [ ] Могу объяснить, почему walk-forward CV даёт более реалистичную оценку, чем single split
- [ ] Понимаю, что LightGBM «не знает» что данные — временной ряд; вся временная информация — в features
- [ ] Знаю, как интерпретировать learning curves (train vs val MAE по эпохам/n_estimators)

#### Л.3: Роадмапа — блоки 6, 7, 9, 11.3
- **Доступ:** бесплатно
- **Что читать:** Блок 6 (CI: bootstrap BCa, conformal), Блок 7 (гипотезы: permutation, DM-test), Блок 9 (OLS, диагностика), Блок 11.3 (PI для TS)
- **Для каких задач:** 4.2 (метрики), 4.4 (сравнение), 4.7 (UQ)

**Чеклист понимания:**
- [ ] Могу объяснить bootstrap BCa: зачем bias-correction и acceleration, чем лучше простого percentile
- [ ] Понимаю split conformal prediction: calibration set, conformity score, quantile → PI
- [ ] Могу провести paired permutation test: H₀, процедура перестановок, p-value
- [ ] Знаю Diebold-Mariano test: для чего, H₀, когда DM лучше чем permutation
- [ ] Могу интерпретировать Breusch-Pagan: H₀ (гомоскедастичность), p-value, что делать если отвергаем (HAC SE)

### Рекомендуется

#### Л.4: Interpretable Machine Learning (Christoph Molnar)
- **Доступ:** бесплатно — https://christophm.github.io/interpretable-ml-book/
- **Что читать:** Главы SHAP, Permutation Importance, PDP (Partial Dependence)
- **Для каких задач:** 4.6 (интерпретируемость)

**Чеклист понимания:**
- [ ] Понимаю SHAP values: что означает положительное/отрицательное значение для конкретного предсказания
- [ ] Знаю разницу между SHAP summary plot и SHAP dependence plot
- [ ] Могу объяснить Permutation Importance: процедура, почему не зависит от модели
- [ ] Понимаю ограничения SHAP: correlation ≠ causation, SHAP может вводить в заблуждение при мультиколлинеарности

#### Л.5: Optuna Documentation
- **Доступ:** бесплатно — https://optuna.readthedocs.io/
- **Что читать:** Tutorial (30 мин)
- **Для каких задач:** 4.5 (tuning)

**Чеклист понимания:**
- [ ] Могу создать study, определить objective function, запустить optimize()
- [ ] Понимаю TPE (Tree-structured Parzen Estimator) — как Optuna выбирает следующий trial
- [ ] Знаю, что такое pruning и зачем: ранняя остановка плохих trial'ов экономит время
- [ ] Могу подключить Optuna к MLflow для логирования каждого trial

#### Л.6: Data Science for Business (Provost & Fawcett) — выборочно
- **Доступ:** платно (требует перевода)
- **Что читать для фазы 4:** Глава 3, **стр. 43–56 только** (13 стр.) — модель как упрощение, overfitting интуитивно. Если ISLR оказался тяжёлым — дополнительно Глава 5, стр. 93–118 (25 стр.)
- **Для каких задач:** 4.1 (выбор моделей — интуитивное понимание), 4.4 (overfitting check)
- **Примечание:** если ISLR понятен — Provost гл.3 и гл.5 можно пропустить

**Чеклист понимания:**
- [ ] Могу объяснить на пальцах: почему слишком сложная модель хуже простой на новых данных
- [ ] Понимаю, что test set — это «экзамен, который модель не видела» и зачем это нужно

---

## Маппинг на роадмапу (сводка)

| Блок роадмапы | Задача фазы 4 | Что конкретно делаем |
|---|---|---|
| 5.2 MLE | 4.5 | Optuna как поиск максимума (минимума loss) |
| 6.1 Bootstrap BCa | 4.7 | CI для MAE, RMSE, R² |
| 6.2 Conformal | 4.7 | Prediction intervals с coverage guarantee |
| 7.1-7.3 Гипотезы | 4.4 | Permutation test, DM-test для сравнения моделей |
| 9.1 OLS | 4.3 | Linear baseline, коэффициенты, R² |
| 9.2 Диагностика | 4.3, 4.4 | BP → HAC SE, DW, QQ-plot, полный протокол |
| 9.3 GLM | 4.3 | Gamma для energy (если нужно) |
| 10.1 Причинность | 4.6 | SHAP → гипотезы о каузальности (осторожно) |
| 11.1 TS | 4.2, 4.3 | Walk-forward CV, ARIMA baseline, Ljung-Box остатков |
| 11.3 PI | 4.7 | Prediction intervals для TS |
| **12.5 GoF на остатках** | **4.4.4** | **Shapiro-Wilk + KS с подбором распределения на остатках** |
| **12.6 Непараметр. мульти-группы** | **4.4.5** | **Kruskal-Wallis + Dunn post-hoc по подстанциям** |
| 12.7 Множественные | 4.4 | BH-коррекция при > 2 сравнениях |
| **12.10 Change-point остатков** | **4.4.6** | **CUSUM на остатках — concept drift** |
| **14.1 Формализация гипотезы** | **4.2.4** | **Шаблон H₀/H₁/α/тест/решение для КАЖДОГО теста** |
| 14.2 Контракт метрик | 4.2 | Primary MAE < 2°C, guardrail, coverage ≥ 90% |
| 14.3 UQ pipeline | 4.7 | Conformal + Bootstrap |
| **14.4 MDE / Power** | **4.4.8** | **MDE при текущем σ, power 80%, связь с бизнес-эффектом** |

## Полный список артефактов фазы 4

| # | Артефакт | Аудитория | Задача |
|---|---|---|---|
| 1 | Model Selection Rationale (пирамида моделей) | Техн. | 4.1 |
| 2 | Test Design Document (CV strategy, метрики) | Техн. | 4.2 |
| 3 | MLflow Experiment Log (все runs) | Техн. | 4.3 |
| 4 | Comparison Table (все модели, val metrics) | Оба | 4.4 |
| 5 | Statistical Test Results (permutation/DM p-values) | Техн. | 4.4 |
| 6 | Residuals Diagnostics Report | Техн. | 4.4 |
| 7 | Optuna Study (best params, optimization history) | Техн. | 4.5 |
| 8 | SHAP Analysis (summary, dependence, waterfall) | Оба | 4.6 |
| 9 | Conformal PI + Calibration Plot | Техн. | 4.7 |
| 10 | Bootstrap CI for Metrics | Техн. | 4.7 |
| 11 | **Modeling Summary Report (3-5 стр., без кода)** | **Бизнес** | **4.8** |
| 12 | **Дашборд: вкладка Model Results** | **Оба** | **4.8** |
| 13 | Saved Model (pickle/MLflow) | Техн. | 4.3 |
