import os
from datetime import datetime
from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import DateTime, Index, Series

from jer_cdm.concepts import MeasurementConcept, UnitConcept


class OMOPMeasurementSchema(pa.SchemaModel):
    measurement_id: Index[int]
    person_id: Series[int]
    measurement_concept_id: Series[int]
    measurement_date: Series[str]
    measurement_datetime: Series[str] = pa.Field(nullable=True)
    measurement_type_concept_id: Series[int]
    operator_concept_id: Series[int] = pa.Field(nullable=True)
    value_as_number: Series[float] = pa.Field(nullable=True)
    value_as_concept_id: Series[int] = pa.Field(nullable=True)
    unit_concept_id: Series[int] = pa.Field(nullable=True)
    range_low: Series[float] = pa.Field(nullable=True)
    range_high: Series[float] = pa.Field(nullable=True)
    provider_id: Series[int] = pa.Field(nullable=True)
    visit_occurrence_id: Series[int] = pa.Field(nullable=True)
    visit_detail_id: Series[int] = pa.Field(nullable=True)
    measurement_source_value: Series[str] = pa.Field(nullable=True)
    measurement_source_concept_id: Series[int] = pa.Field(nullable=True)
    unit_source_value: Series[str] = pa.Field(nullable=True)
    unit_source_concept_id: Series[int] = pa.Field(nullable=True)
    value_source_value: Series[str] = pa.Field(nullable=True)
    measurement_event_id: Series[int] = pa.Field(nullable=True)
    meas_event_field_concept_id: Series[int] = pa.Field(nullable=True)


class MeasurementSchema(pa.SchemaModel):
    measurement_concept_id: Series[int]
    datetime: Series[DateTime]
    value: Series[float] = pa.Field(nullable=True)
    unit_concept_id: Series[int] = pa.Field(nullable=True)


def get_measurement_data_filepath() -> str:
    if 'MEASUREMENT_DATA_FILEPATH' in os.environ:
        return os.environ['MEASUREMENT_DATA_FILEPATH']
    return 'mocks/measurement_data_mock.csv'


def get_measurement_data(filepath: Optional[str] = None) -> pd.DataFrame:
    if filepath is None:
        filepath = get_measurement_data_filepath()
    ans = pd.read_csv(filepath)
    ans['datetime'] = pd.to_datetime(ans['datetime'])
    return ans[list(MeasurementSchema.to_schema().columns.keys())]


def write_measurement_df(
        measurement_df: pd.DataFrame, filepath: Optional[str] = None):
    MeasurementSchema.validate(measurement_df)
    if filepath is None:
        filepath = get_measurement_data_filepath()
    measurement_df.to_csv(filepath, index=False)


def get_measurement_row(
    measurement_concept_id: MeasurementConcept,
    datetime: datetime,
    value: float,
    unit_concept_id: UnitConcept,
):
    return pd.DataFrame.from_dict({
        'measurement_concept_id': [measurement_concept_id.value],
        'datetime': [datetime],
        'value': [value],
        'unit_concept_id': [unit_concept_id.value],
    })


def add_measurement_row(
    measurement_row: pd.DataFrame,
    measurement_df: pd.DataFrame,
):
    return pd.concat([measurement_df, measurement_row], ignore_index=True)[measurement_df.columns]


def get_mock_omop_measurement_row():
    data = {
        'measurement_id': [23970945],
        'person_id': [19204409],
        'measurement_concept_id': [0],
        'measurement_date': ['1990-02-02'],
        'measurement_datetime': [None],
        'measurement_type_concept_id': [0],
        'operator_concept_id': [None],
        'value_as_number': [None],
        'value_as_concept_id': [None],
        'unit_concept_id': [None],
        'range_low': [None],
        'range_high': [None],
        'provider_id': [None],
        'visit_occurrence_id': [None],
        'visit_detail_id': [None],
        'measurement_source_value': [None],
        'measurement_source_concept_id': [None],
        'unit_source_value': [None],
        'unit_source_concept_id': [None],
        'value_source_value': [None],
        'measurement_event_id': [None],
        'meas_event_field_concept_id': [None],
    }
    return pd.DataFrame.from_dict(data).set_index('measurement_id').astype({
        'operator_concept_id': 'Int64',
        'value_as_number': 'float',
        'value_as_concept_id': 'Int64',
        'range_low': 'float',
        'range_high': 'float',
        'provider_id': 'Int64',
        'visit_occurrence_id': 'Int64',
        'visit_detail_id': 'Int64',
        'unit_concept_id': 'Int64',
        'measurement_source_value': 'str',
        'measurement_source_concept_id': 'Int64',
        'unit_source_value': 'str',
        'unit_source_concept_id': 'Int64',
        'value_source_value': 'str',
        'measurement_event_id': 'Int64',
        'meas_event_field_concept_id': 'Int64',
    })
