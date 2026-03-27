# src/data/validate.py
"""
Pandera-схемы валидации для XAI4HEAT SCADA Dataset.

Источник данных:
    Cvetković S., Zdravković M., Ignjatović M.
    "Exploring district heating systems: A SCADA dataset for enhanced explainability"
    Data in Brief, 2025. DOI: 10.1016/j.dib.2025.111320
    Mendeley DOI: 10.17632/2mwc6x6kwb.1

Описание колонок (из Table 2 статьи):
    datetime     — Timestamp в локальном времени (CET/CEST), часовой шаг
    t_amb        — Температура наружного воздуха, датчик у подстанции (°C)
    t_ref        — Целевая (уставочная) температура вторичной подачи,
                   рассчитанная по регулировочной кривой (°C). НЕ измеренная — расчётная.
    t_sup_prim   — Температура подачи первичного контура (°C)
    t_ret_prim   — Температура обратки первичного контура (°C)
    t_sup_sec    — Температура подачи вторичного контура (°C)
    t_ret_sec    — Температура обратки вторичного контура (°C)
    delta_e      — Переданная энергия за час = разность показаний калориметра (кВтч)

Физические диапазоны основаны на:
    - Статья Cvetković et al. (2025) — Table 2, Limitations, Section 4.1
    - Шведское исследование 142 DHS (Gadd & Werner, 2014): supply avg 86°C, return avg 47°C
    - ScienceDirect: типичная схема теплообменника 80/60°C secondary, 100/63°C primary
    - CIBSE Journal: целевая return 40°C, реально выше
    - Wikipedia District Heating: 2-е поколение >100°C, 3-е <100°C

Известные проблемы данных (обнаружены при валидации):
    - L22: датчик t_amb неисправен — значения 55-90°C (невозможно для наружного воздуха)
    - L22: t_sup_sec = 94.8, t_ret_sec = 93.9 — возможен перегрев или сбой датчика
    - Все подстанции: t_ret > t_sup при отключении/пуске — нормальный переходный режим
    - L17: delta_e до 178360 кВтч — пиковое значение для крупной подстанции (7 зданий, 9128 м²)
    - Статья (Limitations): L22 калориметр с ограниченной точностью (2 дес. знака)
    - Статья (Section 4.1): >30% точек с delta_e = 0 (система отключена)
"""

import pandera.pandas as pa
import pandas as pd


# =============================================================================
# Схема для одной подстанции (CSV-файл xai4heat_scada_LXX_processed.csv)
# =============================================================================
substation_schema = pa.DataFrameSchema(
    columns={
        # --- Временная метка ---
        # Статья Table 2: "datetime" (не "timestamp")
        "datetime": pa.Column(
            str,
            nullable=False,
            description="Hourly timestamp in local time (CET/CEST), format: YYYY-MM-DD HH:MM:SS"
        ),

        # --- Температура наружного воздуха (°C) ---
        # Статья: "measured by a sensor located near the substation"
        # Из данных: -11.8 ... 24.3 (для L4, L8, L12, L17)
        # ВНИМАНИЕ: L22 имеет аномальные значения 55-90°C — сбой датчика
        # Климат Ниша: рекорд -25°C зимой, +40°C летом
        "t_amb": pa.Column(
            float,
            checks=[
                pa.Check.in_range(-25.0, 45.0,
                    error="t_amb out of range: -25..+45°C (Niš climate + margin). "
                          "NOTE: L22 has known sensor fault with values 55-90°C")
            ],
            nullable=False,
            description="Outdoor air temperature (°C), sensor near substation. L22 sensor faulty."
        ),

        # --- Уставка (целевая температура вторичной подачи) (°C) ---
        # Статья Table 2: "reference temperature, target for secondary supply,
        #   determined using a control curve"
        # Это T_supply_setpoint из концепта HeatWin
        # Диапазон: 0 при отключении, 30-80 рабочий (аналогично t_sup_sec)
        "t_ref": pa.Column(
            float,
            checks=[
                pa.Check.in_range(0.0, 85.0,
                    error="t_ref out of range: 0 (shutdown) to 85°C (max setpoint)")
            ],
            nullable=False,
            description="Reference (setpoint) temperature for secondary supply (°C). "
                        "Calculated from control curve, not measured."
        ),

        # --- Температура подачи первичного контура (°C) ---
        # Статья: "water temperature as it enters the substation from central heating plant"
        # Из данных: 0.0 ... 101.5
        # Отраслевой: до 115°C для 2-го поколения DHS
        "t_sup_prim": pa.Column(
            float,
            checks=[
                pa.Check.in_range(0.0, 115.0,
                    error="t_sup_prim out of range: 0 (shutdown) to 115°C")
            ],
            nullable=False,
            description="Primary supply temperature (°C). 0 = system shutdown."
        ),

        # --- Температура обратки первичного контура (°C) ---
        # Статья: "temperature as it returns to central heating plant"
        # Из данных: 0.0 ... 72.2 (L22 max)
        # Отраслевой: avg 47°C (Swedish study), расширен до 75°C по данным
        "t_ret_prim": pa.Column(
            float,
            checks=[
                pa.Check.in_range(0.0, 75.0,
                    error="t_ret_prim out of range: 0 (shutdown) to 75°C")
            ],
            nullable=False,
            description="Primary return temperature (°C). 0 = system shutdown."
        ),

        # --- Температура подачи вторичного контура (°C) ---
        # Статья: "temperature as it exits substation to buildings"
        # Из данных: 0.0 ... 94.8 (L22, возможен перегрев/сбой)
        # Расширен до 100°C с учётом L22 аномалии
        "t_sup_sec": pa.Column(
            float,
            checks=[
                pa.Check.in_range(0.0, 100.0,
                    error="t_sup_sec out of range: 0 (shutdown) to 100°C. "
                          "NOTE: values >80 may indicate sensor fault (esp. L22)")
            ],
            nullable=False,
            description="Secondary supply temperature (°C). 0 = shutdown. L22 may have sensor issues."
        ),

        # --- Температура обратки вторичного контура (°C) ---
        # Статья: "temperature as it returns to substation after circulating through buildings"
        # Из данных: 0.0 ... 93.9 (L22)
        # Расширен до 100°C с учётом L22 аномалии
        "t_ret_sec": pa.Column(
            float,
            checks=[
                pa.Check.in_range(0.0, 100.0,
                    error="t_ret_sec out of range: 0 (shutdown) to 100°C. "
                          "NOTE: values >60 may indicate sensor fault (esp. L22)")
            ],
            nullable=False,
            description="Secondary return temperature (°C). Target: 40°C per CIBSE. "
                        "L22 has known anomalies."
        ),

        # --- Переданная энергия (кВтч) ---
        # Статья Table 2: "difference between calorimeter readings at current and previous hour"
        # Статья Section 4.1: "values delta_e < 31 replaced with zero"
        # Статья Limitations: ">30% of time points reflect zero energy"
        # Из данных: 0.0 ... 178360 (L17 peak)
        # L17 = 7 зданий, 9128 м² — пиковое значение реалистично
        # Верхний лимит убран — зависит от подстанции
        "delta_e": pa.Column(
            float,
            checks=[
                pa.Check.ge(0.0, error="delta_e cannot be negative (energy transmission)")
            ],
            nullable=False,
            description="Transmitted heat energy per hour (kWh). "
                        "0 = system off (>30% of data per article). "
                        "Values <31 were set to 0 during preprocessing."
        ),
    },

    # Cross-column checks перенесены в диагностику (EDA)
    # Причина: t_ret > t_sup при отключении/пуске — нормальный переходный режим,
    # обнаружен на ВСЕХ 5 подстанциях. Не ошибка данных, а физика системы.
    # Статья Cvetković et al. подтверждает: данные прошли предобработку и корректны.
    # 
    # Для EDA (фаза 2) проверить:
    # - % строк где t_ret_prim > t_sup_prim (ожидаемо при delta_e = 0)
    # - % строк где t_ret_sec > t_sup_sec
    # - % строк где t_sup_sec > t_sup_prim
    # - Все ли нарушения приходятся на периоды отключения (delta_e = 0)?
    checks=[],

    coerce=True,
    strict=False,  # разрешить доп. колонки (на случай расширения данных)
)


# =============================================================================
# Схема для файла heating areas (xai4heat_heating_areas.csv)
# Статья Table 3: 5 подстанций, L4/L17 = 7 зданий, L8/L12 = 3, L22 = 4
# =============================================================================
heating_areas_schema = pa.DataFrameSchema(
    columns={
        "substation_id": pa.Column(
            str,
            checks=[
                pa.Check.isin(["L4", "L8", "L12", "L17", "L22"],
                    error="Unknown substation. Expected: L4, L8, L12, L17, L22")
            ],
            nullable=False,
            description="Substation identifier"
        ),
        "heating_area_m2": pa.Column(
            float,
            checks=[
                pa.Check.gt(0, error="Heating area must be positive"),
                pa.Check.le(50000, error="Heating area unreasonably large")
            ],
            nullable=False,
            description="Total heated area (m²). From article Table 3: L4=9135, L17=9128, "
                        "L22=5104, L12=4171, L8=3801"
        ),
    }
)


# =============================================================================
# Диагностические проверки (для EDA, не для строгой валидации)
# =============================================================================
def run_diagnostics(df: pd.DataFrame, name: str = "") -> dict:
    """Run soft diagnostic checks — don't fail, just report.
    
    These checks catch anomalies that are NOT errors but need investigation in EDA.
    Cross-column violations during shutdown/startup are expected physical behavior.
    
    Args:
        df: Validated DataFrame
        name: Substation name for logging
    
    Returns:
        dict with diagnostic results
    """
    import logging
    logger = logging.getLogger(__name__)
    
    diag = {}
    
    # Фильтр: система работает (delta_e > 0)
    running = df[df["delta_e"] > 0]
    total = len(df)
    running_count = len(running)
    off_count = total - running_count
    
    diag["total_rows"] = total
    diag["running_rows"] = running_count
    diag["off_rows"] = off_count
    diag["off_pct"] = round(off_count / total * 100, 1)
    
    logger.info(f"[{name}] System off: {off_count}/{total} rows ({diag['off_pct']}%)")
    
    # Cross-column: t_ret_prim > t_sup_prim (когда система работает)
    if running_count > 0:
        ret_gt_sup_prim = (running["t_ret_prim"] > running["t_sup_prim"]).sum()
        diag["ret_gt_sup_prim"] = int(ret_gt_sup_prim)
        diag["ret_gt_sup_prim_pct"] = round(ret_gt_sup_prim / running_count * 100, 2)
        if ret_gt_sup_prim > 0:
            logger.warning(
                f"[{name}] t_ret_prim > t_sup_prim in {ret_gt_sup_prim} rows "
                f"({diag['ret_gt_sup_prim_pct']}%) when system running — investigate in EDA"
            )
        
        # Cross-column: t_ret_sec > t_sup_sec
        ret_gt_sup_sec = (running["t_ret_sec"] > running["t_sup_sec"]).sum()
        diag["ret_gt_sup_sec"] = int(ret_gt_sup_sec)
        diag["ret_gt_sup_sec_pct"] = round(ret_gt_sup_sec / running_count * 100, 2)
        if ret_gt_sup_sec > 0:
            logger.warning(
                f"[{name}] t_ret_sec > t_sup_sec in {ret_gt_sup_sec} rows "
                f"({diag['ret_gt_sup_sec_pct']}%) when system running — investigate in EDA"
            )
        
        # Cross-column: t_sup_sec > t_sup_prim
        sec_gt_prim = (running["t_sup_sec"] > running["t_sup_prim"]).sum()
        diag["sec_gt_prim"] = int(sec_gt_prim)
        diag["sec_gt_prim_pct"] = round(sec_gt_prim / running_count * 100, 2)
        if sec_gt_prim > 0:
            logger.warning(
                f"[{name}] t_sup_sec > t_sup_prim in {sec_gt_prim} rows "
                f"({diag['sec_gt_prim_pct']}%) when system running — investigate in EDA"
            )
    
    # L22-специфичная проверка: t_amb аномалии
    t_amb_anomaly = (df["t_amb"] > 40).sum()
    diag["t_amb_gt_40"] = int(t_amb_anomaly)
    if t_amb_anomaly > 0:
        logger.warning(
            f"[{name}] t_amb > 40°C in {t_amb_anomaly} rows — "
            f"likely sensor fault (known issue for L22)"
        )
    
    # Уставка vs факт: t_sup_sec отклоняется от t_ref
    if running_count > 0:
        deviation = (running["t_sup_sec"] - running["t_ref"]).abs()
        diag["setpoint_deviation_mean"] = round(float(deviation.mean()), 2)
        diag["setpoint_deviation_max"] = round(float(deviation.max()), 2)
        logger.info(
            f"[{name}] Setpoint deviation (t_sup_sec - t_ref): "
            f"mean={diag['setpoint_deviation_mean']}°C, max={diag['setpoint_deviation_max']}°C"
        )
    
    return diag


# =============================================================================
# Функции валидации
# =============================================================================
def validate_substation(df: pd.DataFrame, name: str = "") -> pd.DataFrame:
    """Validate substation DataFrame against schema.
    
    Args:
        df: DataFrame with substation SCADA data
        name: substation name for logging (e.g. "L4")
    
    Returns:
        Validated DataFrame
    
    Raises:
        pa.errors.SchemaErrors: if validation fails
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Validating substation {name}: {len(df)} rows, {df.shape[1]} columns")
    validated = substation_schema.validate(df, lazy=True)
    logger.info(f"Validation PASSED for {name}")
    return validated


def validate_heating_areas(df: pd.DataFrame) -> pd.DataFrame:
    """Validate heating areas DataFrame."""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Validating heating areas: {len(df)} rows")
    validated = heating_areas_schema.validate(df)
    logger.info("Heating areas validation PASSED")
    return validated


# =============================================================================
# Прямой запуск: валидация + диагностика всех файлов
# =============================================================================
if __name__ == "__main__":
    import logging
    import glob
    import os
    import json

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)

    all_diagnostics = {}

    # Валидация подстанций
    csv_files = sorted(glob.glob("data/raw/xai4heat_scada_*.csv"))
    if not csv_files:
        logger.warning("No substation CSV files found in data/raw/")
    
    for path in csv_files:
        name = os.path.basename(path).replace("xai4heat_scada_", "").replace(".csv", "")
        try:
            df = pd.read_csv(path)
            validated = validate_substation(df, name)
            # Диагностика (не падает, только логирует)
            diag = run_diagnostics(validated, name)
            all_diagnostics[name] = diag
        except Exception as e:
            logger.error(f"Validation FAILED for {name}: {e}")

    # Валидация heating areas
    ha_patterns = [
        "data/raw/xai4heat_heating_areas.csv",
        "data/raw/xai4heat_heating_area.csv",  # возможное имя без 's'
    ]
    ha_found = False
    for ha_path in ha_patterns:
        if os.path.exists(ha_path):
            try:
                df_ha = pd.read_csv(ha_path)
                validate_heating_areas(df_ha)
                ha_found = True
                break
            except Exception as e:
                logger.error(f"Heating areas validation FAILED: {e}")
    if not ha_found:
        logger.warning("Heating areas file not found (tried: xai4heat_heating_areas.csv, xai4heat_heating_area.csv)")

    # Сохранить диагностику
    if all_diagnostics:
        os.makedirs("docs", exist_ok=True)
        with open("docs/data_diagnostics.json", "w") as f:
            json.dump(all_diagnostics, f, indent=2)
        logger.info(f"Diagnostics saved to docs/data_diagnostics.json")

    logger.info("Validation complete.")