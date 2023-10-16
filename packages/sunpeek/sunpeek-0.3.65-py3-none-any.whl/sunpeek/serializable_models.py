import uuid
import enum
from dataclasses import field
import datetime as dt
from pydantic.dataclasses import dataclass
import numpy as np
from pydantic import validator, constr
from typing import Union, Any, Dict, List, Tuple
import pint.errors

import sunpeek.components as cmp
import sunpeek.components.physical
from sunpeek.common.errors import AlgorithmError
from sunpeek.common.unit_uncertainty import Q
from sunpeek.components.base import IsVirtual, AlgoCheckMode
from sunpeek.components.helpers import SensorMap, DatetimeTemplates, AccuracyClass, InstallCondition
from sunpeek.components.fluids import UninitialisedFluid
from sunpeek.base_model import BaseModel


class ComponentBase(BaseModel):
    sensor_map: Union[Dict[str, Union[str, None]], None]

    @validator('sensor_map', pre=True)
    def get_raw_name(cls, v):
        out = {}
        for key, item in v.items():
            if isinstance(item, SensorMap):
                try:
                    out[key] = item.sensor.raw_name
                except AttributeError:
                    pass
            else:
                out[key] = item
        return out


def np_to_list(val):
    if isinstance(val, np.ndarray) and val.ndim == 1:
        return list(val)
    elif isinstance(val, np.ndarray) and val.ndim > 1:
        out = []
        for array in list(val):
            out.append(np_to_list(array))
        return out
    return val
4

class Quantity(BaseModel):
    magnitude: Union[float, List[float], List[List[float]]]
    units: str

    @validator('magnitude', pre=True)
    def convert_numpy(cls, val):
        return np_to_list(val)

    @validator('units', pre=True)
    def pretty_unit(cls, val):
        if isinstance(val, pint.Unit):
            return f"{val:~P}"
        return val


class SensorTypeValidator(BaseModel):
    name: str
    compatible_unit_str: str
    description: str
    # min_limit: Union[Quantity, None]
    # max_limit: Union[Quantity, None]
    # # non_neg: bool
    # max_fill_period: Union[dt.datetime, None]
    # sensor_hangs_period: Union[dt.datetime, None]
    # # high_maxerr_const: Union[Quantity, None]
    # # high_maxerr_perc: Union[Quantity, None]
    # # medium_maxerr_const: Union[Quantity, None]
    # # medium_maxerr_perc: Union[Quantity, None]
    # # low_maxerr_const: Union[Quantity, None]
    # # low_maxerr_perc: Union[Quantity, None]
    # # standard_install_maxerr_const: Union[Quantity, None]
    # # standard_install_maxerr_perc: Union[Quantity, None]
    # # poor_install_maxerr_const: Union[Quantity, None]
    # # poor_install_maxerr_perc: Union[Quantity, None]
    info_checks: Union[dict, None]
    max_fill_period: Union[dt.datetime, None]
    sensor_hangs_period: Union[dt.datetime, None]
    lower_replace_min: Union[Quantity, None]
    lower_replace_max: Union[Quantity, None]
    lower_replace_value: Union[Quantity, None]
    upper_replace_min: Union[Quantity, None]
    upper_replace_max: Union[Quantity, None]
    upper_replace_value: Union[Quantity, None]
    # equation: Union[str, None]
    common_units: Union[list, None]


class IAM_Method(BaseModel):
    method_type: str


class IAM_ASHRAE(IAM_Method):
    method_type = 'IAM_ASHRAE'
    b: Quantity


class IAM_K50(IAM_Method):
    method_type = 'IAM_K50'
    k50: Quantity
    b: Union[Quantity, None]


class IAM_Ambrosetti(IAM_Method):
    method_type = 'IAM_Ambrosetti'
    kappa: Quantity


class IAM_Interpolated(IAM_Method):
    method_type = 'IAM_Interpolated'
    aoi_reference: Quantity
    iam_reference: Quantity


class CollectorBase(BaseModel):
    test_reference_area: Union[str, None]
    test_type: Union[str, None]
    gross_length: Union[Quantity, None]
    iam_method: Union[IAM_K50, IAM_ASHRAE, IAM_Ambrosetti, IAM_Interpolated, None]
    name: str
    manufacturer_name: Union[str, None]
    product_name: Union[str, None]
    test_report_id: Union[str, None]
    licence_number: Union[str, None]
    certificate_date_issued: Union[dt.datetime, str, None]
    certificate_lab: Union[str, None]
    certificate_details: Union[str, None]
    collector_type: Union[str, None]
    area_gr: Union[Quantity, None]
    area_ap: Union[Quantity, None]
    gross_width: Union[Quantity, None]
    gross_height: Union[Quantity, None]
    a1: Union[Quantity, None]
    a2: Union[Quantity, None]
    a5: Union[Quantity, None]
    a8: Union[Quantity, None]
    kd: Union[Quantity, None]
    eta0b: Union[Quantity, None]
    eta0hem: Union[Quantity, None]
    f_prime: Union[Quantity, None]
    concentration_ratio: Union[Quantity, None]
    calculation_info: Union[Dict[str, str], None]
    aperture_parameters: Union[Dict[str, Union[Quantity, None]], None]


class Collector(CollectorBase):
    id: Union[int, None]
    name: str

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    def __repr__(self):
        return self.__str__()


class CollectorQDT(CollectorBase):
    a1: Quantity
    a2: Quantity
    a5: Quantity
    a8: Union[Quantity, None]


class CollectorSST(CollectorBase):
    ceff: Quantity


class SensorBase(BaseModel):
    description: Union[str, None]
    accuracy_class: Union[AccuracyClass, None]
    installation_condition: Union[InstallCondition, None]
    info: Union[dict, None] = {}
    raw_name: Union[str, None]
    native_unit: Union[str, None]
    sensor_type: Union[str, None]

    @validator('info', pre=True)
    def convert_info(cls, v):
        if isinstance(v, cmp.SensorInfo):
            return v._info
        return v

    @validator('native_unit', pre=True)
    def check_unit(cls, v):
        if isinstance(v, str):
            Q(1, v)

        return v


class Sensor(SensorBase):
    id: Union[int, None]
    plant_id: Union[int, None]
    raw_name: Union[str, None]
    sensor_type: Union[str, None]
    native_unit: Union[str, None]
    formatted_unit: Union[str, None]
    is_virtual: Union[bool, None]
    can_calculate: Union[bool, None]
    is_mapped: Union[bool, None]
    is_infos_set: Union[bool, None]

    @validator('sensor_type', pre=True)
    def convert_sensor_type(cls, v):
        if isinstance(v, cmp.SensorType):
            return v.name
        return v


class NewSensor(SensorBase):
    raw_name: str
    native_unit: str = None


class BulkUpdateSensor(Sensor):
    id: int


class FluidDefintion(SensorBase):
    id: Union[int, None]
    model_type: str
    name: str
    manufacturer: Union[str, None]
    description: Union[str, None]
    is_pure: bool
    dm_model_sha1: Union[str, None]
    hc_model_sha1: Union[str, None]
    heat_capacity_unit_te: Union[str, None]
    heat_capacity_unit_out: Union[str, None]
    heat_capacity_unit_c: Union[str, None]
    density_unit_te: Union[str, None]
    density_unit_out: Union[str, None]
    density_unit_c: Union[str, None]
    # heat_capacity_onnx: Union[str, None]
    # density_onnx: Union[str, None]

    # @validator('heat_capacity_onnx', 'density_onnx', pre=True)
    # def onnx_to_str(cls, v):
    #     try:
    #         return v.hex()
    #     except AttributeError:
    #         return v


class Fluid(BaseModel):
    id: Union[int, None]
    name: Union[str, None]
    manufacturer_name: Union[str, None]
    product_name: Union[str, None]
    fluid: FluidDefintion
    concentration: Union[Quantity, None]


class FluidSummary(BaseModel):
    name: Union[str, None]
    fluid: str
    concentration: Union[Quantity, None]

    @validator('fluid', pre=True)
    def fluid_name(cls, v):
        try:
            return v.name
        except AttributeError:
            return v


class Array(ComponentBase):
    id: Union[int, None]
    plant_id: Union[int, None]
    name: Union[str, None]
    collector: Union[str, None]
    area_gr: Union[Quantity, None]
    area_ap: Union[Quantity, None]
    azim: Union[Quantity, None]
    tilt: Union[Quantity, None]
    row_spacing: Union[Quantity, None]
    n_rows: Union[Quantity, None]
    ground_tilt: Union[Quantity, None]
    mounting_level: Union[Quantity, None]
    fluidvol_total: Union[Quantity, None]
    rho_ground: Union[Quantity, None]
    rho_colbackside: Union[Quantity, None]
    rho_colsurface: Union[Quantity, None]
    max_aoi_shadow: Union[Quantity, None]
    min_elevation_shadow: Union[Quantity, None]

    @validator('collector', pre=True)
    def convert_coll(cls, v):
        if isinstance(v, cmp.Collector):
            return v.name
        return v

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    def __repr__(self):
        return self.__str__()


class NewArray(Array):
    name: str
    collector: str
    sensors: Union[Dict[str, NewSensor], None]
    sensor_map: Union[dict, None]


class DataUploadDefaults(BaseModel):
    id: Union[int, None]
    datetime_template: Union[DatetimeTemplates, None]
    datetime_format: Union[str, None]
    timezone: Union[str, None]
    csv_separator: Union[str, None]
    csv_decimal: Union[str, None]
    csv_encoding: Union[str, None]
    index_col: Union[int, None]


class PlantBase(ComponentBase):
    owner: Union[str, None]
    operator: Union[str, None]
    description: Union[str, None]
    location_name: Union[str, None]
    elevation: Union[Quantity, None]
    fluid_solar: Union[FluidSummary, str, None]
    arrays: Union[List[Array], None]
    fluid_vol: Union[Quantity, None]
    raw_sensors: Union[List[Sensor], None]
    virtuals_calculation_uptodate: Union[bool, None]

    @validator('fluid_solar', pre=True)
    def convert_fluid(cls, v):
        if isinstance(v, cmp.Fluid):
            if isinstance(v, UninitialisedFluid):
                return FluidSummary(name=v.fluid_def_name, fluid=v.fluid_def_name, concentration=None)
            return FluidSummary(name=v.name, fluid=v.fluid.name, concentration=getattr(v, 'concentration', None))
        return v


class Plant(PlantBase):
    name: Union[str, None]
    id: Union[int, None]
    latitude: Union[Quantity, None]
    longitude: Union[Quantity, None]
    fluid_solar: Union[FluidSummary, str, None]
    local_tz_string_with_DST: Union[str, None]
    data_upload_defaults: Union[DataUploadDefaults, None]

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    def __repr__(self):
        return self.__str__()


class UpdatePlant(Plant):
    sensors: Union[Dict[str, NewSensor], None]
    fluid_solar: Union[FluidSummary, None]


class NewPlant(PlantBase):
    name: str
    latitude: Quantity
    longitude: Quantity
    fluid_solar: Union[FluidSummary, None]
    raw_sensors: Union[List[NewSensor], None]
    sensor_map: Union[dict, None]


class PlantSummaryBase(BaseModel):
    name: Union[str, None]
    owner: Union[str, None]
    operator: Union[str, None]
    description: Union[str, None]
    location_name: Union[str, None]
    latitude: Union[Quantity, None]
    longitude: Union[Quantity, None]
    elevation: Union[Quantity, None]


class PlantSummary(PlantSummaryBase):
    id: int
    name: str
    virtuals_calculation_uptodate: Union[bool, None]


class PlantDataStartEnd(BaseModel):
    start: Union[dt.datetime, None]
    end: Union[dt.datetime, None]


class Error(BaseModel):
    error: str
    message: str
    detail: str


class Job(BaseModel):
    id: uuid.UUID
    status: cmp.helpers.ResultStatus
    result_url: Union[str, None]
    plant: Union[str, None]

    @validator('plant', pre=True)
    def plant_to_str(cls, v):
        if v is not None:
            return v.name


class JobReference(BaseModel):
    job_id: uuid.UUID
    href: str

    @validator('job_id')
    def uuid_to_str(cls, v):
        if v is not None:
            return str(v)


class ConfigExport(BaseModel):
    collectors: List[Collector]
    sensor_types: List[SensorTypeValidator]
    fluid_definitions: List[Union[FluidDefintion, None]]
    plant: Plant


class SensorSlotValidator(BaseModel):
    """
    A pydantic class used to hold and validate information on a component sensor slot.

    Parameters
    ----------
    name : str
        The name of the slot, which behaves like a component attribute and can be used to access the mapped sensor from
        the component. e.g. te_amb. `name` only needs to be unique and understandable in the context of a specific
        component, e.g. the `tp` slot of a plant includes the total power of all arrays, whereas `tp` of an array is
        just that array's power.
    descriptive_name : str
        A longer more descriptive name, e.g. for display to a user in a front end client. Limited to 24 characters
    description : str
        A description of the purpose and use of the slot.
    virtual : enum
        Whether the sensor for a slot is always virtual, can be virtual given certain conditions, or is never virtual
    """

    name: str
    sensor_type: Union[str, SensorTypeValidator]
    descriptive_name: constr(max_length=57)
    virtual: IsVirtual
    description: Union[str, None]


## PC Method -----------------------

class PCMethodOutputPlant(BaseModel):
    id: Union[int, None]
    plant: Plant

    n_intervals: Union[int, None]
    total_interval_length: Union[dt.timedelta, None]
    datetime_intervals_start: Union[List[dt.datetime], None]
    datetime_intervals_end: Union[List[dt.datetime], None]

    tp_measured: Union[Quantity, None]
    tp_sp_measured: Union[Quantity, None]
    tp_sp_estimated: Union[Quantity, None]
    tp_sp_estimated_safety: Union[Quantity, None]
    mean_tp_sp_measured: Union[Quantity, None]
    mean_tp_sp_estimated: Union[Quantity, None]
    mean_tp_sp_estimated_safety: Union[Quantity, None]

    target_actual_slope: Union[Quantity, None]
    target_actual_slope_safety: Union[Quantity, None]

    fluid_solar: Union[FluidSummary, None]
    mean_temperature: Union[Quantity, None]
    mean_fluid_density: Union[Quantity, None]
    mean_fluid_heat_capacity: Union[Quantity, None]

    @validator('datetime_intervals_start', 'datetime_intervals_end', pre=True)
    def array_to_list(cls, val):
        if isinstance(val, np.ndarray):
            return list(val)


class PCMethodOutputData(BaseModel):
    id: Union[int, None]

    te_in: Union[Quantity, None]
    te_out: Union[Quantity, None]
    te_op: Union[Quantity, None]
    te_op_deriv: Union[Quantity, None]

    aoi: Union[Quantity, None]
    iam_b: Union[Quantity, None]
    ve_wind: Union[Quantity, None]

    rd_gti: Union[Quantity, None]
    rd_bti: Union[Quantity, None]
    rd_dti: Union[Quantity, None]


class PCMethodOutputArray(BaseModel):
    id: Union[int, None]
    array: Array
    data: PCMethodOutputData

    tp_sp_measured: Union[Quantity, None]
    tp_sp_estimated: Union[Quantity, None]
    tp_sp_estimated_safety: Union[Quantity, None]
    mean_tp_sp_measured: Union[Quantity, None]
    mean_tp_sp_estimated: Union[Quantity, None]
    mean_tp_sp_estimated_safety: Union[Quantity, None]


class PCMethodOutput(BaseModel):
    id: Union[int, None]
    plant: PlantSummary

    datetime_eval_start: dt.datetime
    datetime_eval_end: dt.datetime

    # Algorithm settings
    pc_method_name: str
    evaluation_mode: str
    formula: int
    wind_used: bool

    # Results
    settings: Dict[str, Any]  # Type checking done in PCSettings
    plant_output: PCMethodOutputPlant
    array_output: List[PCMethodOutputArray]


class OperationalEvent(BaseModel):
    id: Union[int, None]
    plant: Union[str, PlantSummary]
    event_start: dt.datetime
    event_end: Union[dt.datetime, None]
    ignored_range: bool = False
    description: Union[str, None]
    original_timezone: Union[str, None]


class PCMethodSettings(BaseModel):
    safety_uncertainty: Union[float, None]
    safety_pipes: Union[float, None]
    safety_others: Union[float, None]
    evaluation_mode: Union[str, None]
    formula: Union[int, None]
    wind_used: Union[bool, None]


# def dataclass_to_pydantic(cls: dataclasses.dataclass, name: str) -> BaseModel:
#     # get attribute names and types from dataclass into pydantic format
#     pydantic_field_kwargs = dict()
#     for _field in dataclasses.fields(cls):
#         # check is field has default value
#         if isinstance(_field.default, dataclasses._MISSING_TYPE):
#             # no default
#             default = ...
#         else:
#             default = _field.default
#
#         try:
#             for i, typ in enumerate(_field.type.__args__):
#
#         except AttributeError:
#             pass
#
#         pydantic_field_kwargs[ _field.name] = (_field.type, default)
#
#     return pydantic.create_model(name, **pydantic_field_kwargs, __base__=BaseModel)


class ProblemType(str, enum.Enum):
    component_slot = 'Component slot'
    real_sensor_missing = 'Real sensor'
    virtual_sensor_missing = 'Virtual sensor'
    real_or_virtual_sensor_missing = 'Real or virtual sensor'
    component_attrib = 'Component attribute problem'
    fluid_missing = 'Fluid missing'
    collector_missing = 'Collector missing'
    collector_type = 'Wrong collector type'
    collector_param = 'Invalid collector parameter'
    sensor_info = 'Sensor info problem'
    component_missing = 'Component missing'
    other_problem = 'Unspecified problem'
    unexpected_in_calc = 'Unexpected calculation error'
    unexpected_getting_problems = 'Unexpected error getting problem report'


@dataclass
class AlgoProblem:
    """A class used to hold information on a problem / missing info for a calculation / CoreStrategy.
    Can be used to track problems / missing information back to the root cause.

    Parameters
    ----------
    problem_type : ProblemType enum
    affected_component : Plant, Array, Collector, optional
        The component where some problem occurs / information is missing.
    affected_item_name : str, optional
        Typically the name of the affected sensor slot or attribute of the affected component.
    description : str, optional
    """
    problem_type: ProblemType
    affected_component: Union[Any, None] = None
    affected_item_name: Union[str, None] = None
    description: Union[str, None] = None

    def __init__(self, problem_type, affected_component=None, affected_item_name=None, description=None):
        # Defining an explicit init because affected_component got silently cast into the wrong serializable model.
        self.problem_type = problem_type
        self.affected_item_name = affected_item_name
        self.description = description

        if affected_component is None:
            self.affected_component = None
            return

        if isinstance(affected_component, sunpeek.components.physical.Plant):
            self.affected_component = Plant.from_orm(affected_component)
        elif isinstance(affected_component, sunpeek.components.physical.Array):
            self.affected_component = Array.from_orm(affected_component)
        elif isinstance(affected_component, sunpeek.components.types.Collector):
            self.affected_component = Collector.from_orm(affected_component)
        else:
            raise ValueError(f'Unexpected component: Expected ORM Plant, Array or Collector, '
                             f'got {type(affected_component)}.')


@dataclass
class ProblemReport:
    """Standardized reporting of problems / missing information required to perform some calculation.

    This applies to all calculations in SunPeek, i.e. both virtual sensors and other calculations e.g. PC method.
    Any CoreStrategy and CoreAlgorithm holds / can return a ProblemReport which holds structured information as to
    what problems / missing information there is that prevents the strategy / algo to complete.

    ProblemReport implements an n-level tree, where each node (ProblemReport) has n leaves (own_problems) and points
    at m other nodes (sub_problems). sub_problems are implemented as dict with key == strategy name.

    Parameters
    ----------
    success : bool, optional, default True
        True if the algo or strategy holding / producing the problem report is successful, meaning that at least
        parts of its results can be calculated and / or only optional information is missing.
    own_problems : List[AlgoProblem], optional
        List of reported problems that affect the algo / strategy itself (as opposed to problems coming from called /
        sub algorithms). Example: Strategy needs some component attribute, but that attribute is None.
    sub_reports : Dict[str, ProblemReport], optional
        Problems that are not directly associated to the algo / strategy holding this ProblemReport, but rather stem
        from a previous calculation / strategy. Example: Strategy needs some virtual sensor, but that had its own
        problems, reported as a ProblemReport.
    virtuals_reports : Dict[Tuple[Any, str], 'ProblemReport']
        Problems arising from virtual sensors. These are kept separate from sub_reports because the same virtual sensor
        report might appear in several locations of the problem tree, but should only be parsed once.
    problem_slots : List[str], optional
        Set by virtual sensor strategies, problem_slots can be used to report partial success, i.e.:
        If a strategy is successful for some but not all virtual sensors, the success flag can be set to True,
        and the ProblemReport applies only to the virtual sensor slot names which cannot be calculated,
        i.e. the problem_slots.
    """
    success: Union[bool, None] = True
    own_problems: Union[List[AlgoProblem], None] = None
    sub_reports: Union[Dict[str, 'ProblemReport'], None] = None
    virtuals_reports: Union[Dict[Tuple[Any, str], 'ProblemReport'], None] = None
    problem_slots: Union[List[str], None] = field(default_factory=list)  # Used if some virtual sensors / slots fail

    @property
    def successful_strategy_str(self) -> Union[str, None]:
        """Loop through strategies, return name of first successful strategy, or None if no strategy was successful.
        """
        if not self.success:
            return None
        for strategy_name, problem in self.sub_reports.items():
            if problem.success:
                return strategy_name
        return None

    @staticmethod
    def get_virtual_state(component, slot_name) -> IsVirtual:
        try:
            is_virtual = component.sensor_slots[slot_name].virtual
        except KeyError:
            raise AlgorithmError(f'Error adding AlgoProblem: '
                                 f'Component slot {slot_name} not found in component {component}.')
        return is_virtual

    @staticmethod
    def _cname(component: cmp.Component) -> str:
        """Return verbose component name with class + name.
        """
        class_name = component.__class__.__name__.lower()
        if isinstance(component, cmp.Plant):
            return class_name
        return f'{class_name} "{component.name}"'

    def add_own(self, algo_problems: Union[AlgoProblem, List[AlgoProblem]]) -> None:
        """Add "leaf" to problem tree: add 1 or more AlgoProblems to report.
        """
        # lst = [] if self.own_problems is None else self.own_problems
        if algo_problems is None:
            return
        lst = self.own_problems or []
        if not isinstance(algo_problems, list):
            algo_problems = [algo_problems]
        lst.extend(algo_problems)
        self.own_problems = lst
        self.success = False

    def add_virtual(self, component: cmp.Component, slot_name: str, problem_report: 'ProblemReport') -> None:
        """Add subtree of virtual sensor problems to `self.virtuals_reports`.
        """
        self.virtuals_reports = self.virtuals_reports or {}
        self.virtuals_reports[(component, slot_name)] = problem_report

    def add_sub(self, strategy_name: str, problem_report: 'ProblemReport') -> None:
        """Add subtree to problem tree: Add 1 ProblemReport subtree.
        """
        self.sub_reports = self.sub_reports or {}
        self.sub_reports[strategy_name] = problem_report
        self.success = False

    def add_missing_component(self, component: cmp.Component,
                              missing_component_class_name: str,
                              description: str) -> None:
        """Add a "missing component" AlgoProblem as own problem.
        """
        algo_problem = AlgoProblem(ProblemType.component_missing, component, missing_component_class_name, description)
        self.add_own(algo_problem)

    def add_missing_sensor(self, component: cmp.Component,
                           slot_name: str,
                           check_mode: AlgoCheckMode,
                           # enforce_real: bool = False
                           ) -> None:
        """Add a "missing sensor" AlgoProblem as own problem.
        """
        is_virtual = self.get_virtual_state(component, slot_name)
        if is_virtual is IsVirtual.never:
            self.add_missing_real_sensor(component, slot_name)
            return

        if is_virtual is IsVirtual.always:
            problem_type = ProblemType.virtual_sensor_missing
            description = (f'"{component.sensor_slots[slot_name].descriptive_name}" '
                           f'({slot_name}) in {self._cname(component)}: '
                           f'Virtual sensor calculation failed.')

        elif is_virtual is IsVirtual.possible:
            problem_type = ProblemType.real_or_virtual_sensor_missing
            description = (f'"{component.sensor_slots[slot_name].descriptive_name}" ({slot_name}) '
                           f'in {self._cname(component)}: '
                           f'Sensor missing or virtual sensor calculation failed.')
        else:
            raise ValueError(f'Unexpected IsVirtual value of slot {slot_name}: "{is_virtual}". '
                             f'Expected one of {", ".join(list(IsVirtual))}')

        self.add_own(AlgoProblem(problem_type, component, slot_name, description))

        s = getattr(component, slot_name)
        if s is None or not s.is_virtual:
            return

        # If virtual sensor for which calculation failed: Add subtree to problem tree
        if check_mode is None:
            raise AlgorithmError(f'Input "check_mode" required to treat a virtual sensor in problem reporting.')
        add_vsensor = ((check_mode == AlgoCheckMode.config_and_data) or
                       (check_mode == AlgoCheckMode.config_only and s._problems is not None))
        if add_vsensor:
            self.add_virtual(component, slot_name, s.problems)

    def add_missing_real_sensor(self, component: cmp.Component,
                                slot_name: str,
                                # description: str = None,
                                ) -> None:
        """Add a "missing real sensor" AlgoProblem as own problem.
        """
        if IsVirtual.always == self.get_virtual_state(component, slot_name):
            raise ValueError(f'Component slot {slot_name} in {component.name} can never be real. '
                             f'This is an internal SunPeek error. Please report it.')

        description = (f'"{component.sensor_slots[slot_name].descriptive_name}" '
                       f'({slot_name}) in {self._cname(component)}: '
                       f'Sensor missing.')

        self.add_own(AlgoProblem(ProblemType.real_sensor_missing, component, slot_name, description))

    def add_missing_sensor_info(self, component: cmp.Component, slot_name: str = None,
                                info_name: str = None, description: str = None) -> None:
        """Add a "missing fluid" AlgoProblem as own problem.
        """
        if description is None:
            if info_name is None:
                raise AlgorithmError(f'"info_name" required to generate missing sensor info description.')
            description = (f'Sensor info "{info_name}" missing for sensor '
                           f'"{component.sensors[slot_name].raw_name}" '
                           f'({slot_name} in {self._cname(component)}). '
                           f'This can be fixed on the Sensor Details page.')
        algo_problem = AlgoProblem(ProblemType.sensor_info, component, slot_name, description)
        self.add_own(algo_problem)

    def add_missing_attrib(self, component: Union[cmp.Component, cmp.Collector],
                           attrib_name: str, description: str = None) -> None:
        """Add a "missing attribute" AlgoProblem as own problem.
        """
        description = (f'Missing information "{attrib_name}" in {self._cname(component)}. '
                       f'{"" if description is None else description}')
        algo_problem = AlgoProblem(ProblemType.component_slot, component, attrib_name, description)
        self.add_own(algo_problem)

    def add_zero_collector_param(self, component: cmp.Collector,
                                 attrib_name: str) -> None:
        """Add a "component_attrib" AlgoProblem as own problem, for collector parameters that should be nonzero.
        """
        description = (f'Collector parameter "{attrib_name}" is None or zero but is required to be nonzero.'
                       f'in {self._cname(component)}.')
        algo_problem = AlgoProblem(ProblemType.collector_param, component, attrib_name, description)
        self.add_own(algo_problem)

    def add_nonzero_collector_param(self, component: cmp.Collector,
                                    attrib_name: str) -> None:
        """Add a "component_attrib" AlgoProblem as own problem, for collector parameters that should be zero.
        """
        description = (f'Collector parameter "{attrib_name}" is nonzero but is required to be zero, '
                       f'in {self._cname(component)}.')
        algo_problem = AlgoProblem(ProblemType.collector_param, component, attrib_name, description)
        self.add_own(algo_problem)

    def add_missing_collector(self, component: cmp.Component, slot_name: str) -> None:
        """Add a "missing collector" AlgoProblem as own problem.
        """
        description = (f'"{slot_name}" in {self._cname(component)}: '
                       f'Collector is missing (None) or invalid (UninitialisedCollector). '
                       f'In case you defined a collector, this is an internal SunPeek error. Please report it.')
        algo_problem = AlgoProblem(ProblemType.component_missing, component, slot_name, description)
        self.add_own(algo_problem)

    def add_wrong_collector_type(self, component: cmp.Collector,
                                 expected: cmp.CollectorTypes | List[cmp.CollectorTypes],
                                 received: cmp.CollectorTypes) -> None:
        """Add a "wrong collector type" AlgoProblem as own problem.
        """
        expected = expected if isinstance(expected, list) else [expected]
        expected = [x.value if isinstance(x, enum.Enum) else x for x in expected]
        received = received.value if isinstance(received, enum.Enum) else received
        description = (f'Wrong collector type: '
                       f'Expected a collector of type {" or ".join(expected)}, '
                       f'but received "{received}".')
        algo_problem = AlgoProblem(ProblemType.collector_type, component, '', description)
        self.add_own(algo_problem)

    def add_missing_fluid(self, component: cmp.Component, slot_name: str) -> None:
        """Add a "missing fluid" AlgoProblem as own problem.
        """
        description = (f'"{slot_name}" in {self._cname(component)}: '
                       f'Fluid is missing (None) or invalid (UninitialisedFluid). '
                       f'In case you defined a fluid, this is an internal SunPeek error. Please report it.')
        algo_problem = AlgoProblem(ProblemType.fluid_missing, component, slot_name, description)
        self.add_own(algo_problem)

    def add_generic_slot_problem(self, component: cmp.Component, description: str) -> None:
        """Add a generic ProblemType.component_slot AlgoProblem as own problem
        """
        self.add_own(AlgoProblem(ProblemType.component_slot, component, description=description))

    def parse(self,
              include_successful_strategies: bool = False,
              include_problem_slots: bool = True,
              ) -> str:
        """Parse ProblemReport into single string. Includes virtual sensors as sub-report.
        """
        main_report = self.to_tree(include_successful_strategies, include_problem_slots).parse()
        virtuals_root = self.virtuals_to_tree(include_successful_strategies)
        virtuals = '' if virtuals_root.is_leaf else f'\nVirtual Sensors:\n{virtuals_root.parse(node_whitespace=False)}'

        return main_report + virtuals

    def to_tree(self, include_successful_strategies: bool, include_problem_slots: bool = True) -> 'TreeNode':
        """Return the root node representing the ProblemReport as an n-tree. Virtual sensor problems are left out.
        """
        root_node = TreeNode()
        # Add own problems as children leaves
        if self.own_problems is not None:
            for algo_problem in self.own_problems:
                root_node.add(TreeNode(algo_problem.description))
        # Add sub_reports as children nodes
        if self.sub_reports is not None:
            for k, v in self.sub_reports.items():
                include_slots = v.problem_slots and include_problem_slots
                skip = v.success and not include_successful_strategies and not include_slots
                if skip:
                    continue
                if not v.success:
                    root_node.add(TreeNode(k, v.to_tree(include_successful_strategies, include_problem_slots).children))
                    continue
                if not v.problem_slots:
                    root_node.add(TreeNode(k, [TreeNode('No problems found.')]))
                else:  # partial success, some virtual sensors missing
                    message = f'Some virtual sensors could not be calculated: {", ".join(self.problem_slots)}. {k}'
                    root_node.add(
                        TreeNode(message, v.to_tree(include_successful_strategies, include_problem_slots).children))

        return root_node

    def virtuals_to_tree(self, include_successful_strategies: bool) -> 'TreeNode':
        """Return the root node representing the virtual sensor ProblemReports as an n-tree.
        """
        virtuals_report = self.collect_virtuals_report()
        root_node = TreeNode()
        if not virtuals_report:
            return root_node

        for k, v in virtuals_report.items():
            component, slot = k
            message = (f'"{component.sensor_slots[slot].descriptive_name}" '
                       f'({slot}) in {self._cname(component)}: '
                       f'Virtual sensor calculation failed. Details:')
            root_node.add(TreeNode(message, v.to_tree(include_successful_strategies).children))

        return root_node

    def collect_virtuals_report(self) -> Dict[Tuple[Any, str], 'ProblemReport']:
        """Recursively collect all virtual sensor problems in ProblemReport, avoiding duplicate entries.
        """
        v_reports = {}
        # Collect own virtual sensor report
        if self.virtuals_reports is not None:
            v_reports.update(self.virtuals_reports)
        # Collect virtual sensor report in sub-strategies
        if self.sub_reports is not None:
            for sub_report in self.sub_reports.values():
                v_reports.update(sub_report.collect_virtuals_report())

        return v_reports


class TreeNode:
    """n-tree, consisting of structural information (nodes, leaves) and string messages.
    """

    def __init__(self, message: str = '', children: List['TreeNode'] = None):
        self.message = message
        self.children = children or []

    def add(self, child: 'TreeNode'):
        self.children.append(child)

    @property
    def is_leaf(self) -> bool:
        return not bool(self.children)

    def parse(self, level: int = -1, node_whitespace: bool = True) -> str:
        """Return string representation of the tree.
        """
        output = ''
        indentation = '  ' * level
        if self.message:
            bullet = '-' if self.is_leaf else ">"
            newline = f'\n' if node_whitespace and not self.is_leaf else ''
            output += f'{newline}{indentation}{bullet} {self.message}\n'
        for child in self.children:
            output += child.parse(level + 1, node_whitespace=node_whitespace)
        return output


# Goal = Report success / problems of a specific PC method strategy.
@dataclass
class PCMethodProblem:
    evaluation_mode: str
    formula: int
    wind_used: bool
    success: bool
    problem_str: str
