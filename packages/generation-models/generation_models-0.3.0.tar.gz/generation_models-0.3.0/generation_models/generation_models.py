from __future__ import annotations

import json
from enum import Enum

from pydantic import BaseModel, ValidationError, Field, validator, root_validator, parse_obj_as, conlist
from pydantic.fields import Validator
import typing as t
from typing_extensions import Annotated


ModelVariable = t.TypeVar("ModelVariable", bound=t.Type[BaseModel])


def optional_discriminators(unions: t.List[str]) -> t.Callable[[ModelVariable], ModelVariable]:
    def dec(model: ModelVariable) -> ModelVariable:
        for k in unions:
            field = model.__fields__[k]
            discriminator_lookup = {v.type_: k for k, v in field.sub_fields_mapping.items()}

            def handle_missing_discriminator(cls, values):
                if isinstance(values, dict) and field.discriminator_key not in values:
                    parsed = parse_obj_as(t.Union[tuple(f.type_ for f in field.sub_fields)], values)
                    values[field.discriminator_key] = discriminator_lookup[type(parsed)]
                return values

            field.class_validators[f"handle_missing_{field.discriminator_key}"] = Validator(
                handle_missing_discriminator, pre=True
            )
            field.populate_validators()
        return model

    return dec


class SolverConfig(BaseModel):
    """_"""

    time_limit: float = 8.0
    mip_gap_tolerance: float = 0.0
    verbose: bool = False
    hybrid_infeasible_tol: float = 0
    solver_specific: t.Dict[str, t.Any] = {}

    initial_time_limit: t.Optional[float] = Field(None, deprecated=True, description="Use time_limit instead")
    initial_mip_gap_tolerance: t.Optional[float] = Field(
        None, deprecated=True, description="Use mip_gap_tolerance instead"
    )
    initial_verbose: t.Optional[bool] = Field(None, deprecated=True, description="Use verbose instead")

    @root_validator(skip_on_failure=True, pre=True)
    def coerce_deprecated_args(cls, values):
        old_to_new = {
            "initial_time_limit": "time_limit",
            "initial_mip_gap_tolerance": "mip_gap_tolerance",
            "initial_verbose": "verbose",
        }
        for k, v in old_to_new.items():
            if values.get(k) is not None:
                if v in values:
                    raise ValueError(f"{k} is deprecated and cannot be provided if {v} is provided")
                else:
                    values[v] = values.pop(k)
        return values

    @validator("time_limit")
    def validate_time_limit(cls, v):
        assert 1e-3 < v < 1e3, f"time_limit must be between 0.001 and 1000 seconds, got {v:.4f} seconds."
        return v

    @validator("mip_gap_tolerance")
    def validate_mip_gap(cls, v):
        assert 0 <= v < 1, f"mip_gap_tolerance must be between 0 and 1, got {v}."
        return v


class StorageCoupling(str, Enum):
    ac = "ac"
    dc = "dc"
    hv_ac = "hv_ac"


class SingleAxisTracking(BaseModel):
    """_"""

    tracking_type: t.Optional[t.Literal["SAT"]] = "SAT"
    rotation_limit: float = 45.0
    backtrack: bool = True


class FixedTilt(BaseModel):
    """_"""

    tracking_type: t.Optional[t.Literal["FT"]] = "FT"
    tilt: float


class ScalarUtilization(BaseModel):
    """_"""

    dimension_type: t.Optional[t.Literal["scalar"]] = "scalar"
    actual: float
    lower: float
    upper: float

    @root_validator(skip_on_failure=True)
    def between_0_and_1(cls, values):
        for v in "actual", "lower", "upper":
            assert 0 <= values[v] <= 1, "must be between 0 and 1"
        return values


def _check_lengths(strs_lists: t.Dict[str, list]):
    str1 = next(iter(strs_lists.keys()))
    len1 = len(next(iter(strs_lists.values())))
    for k, v in strs_lists.items():
        assert len(v) == len1, f"{str1} and {k} must be the same length"


class TimeSeriesUtilization(BaseModel):
    """_"""

    dimension_type: t.Optional[t.Literal["time_series"]] = "time_series"
    actual: t.List[float]
    lower: t.List[float]
    upper: t.List[float]

    @root_validator(skip_on_failure=True)
    def between_0_and_1(cls, values):
        for v in "actual", "lower", "upper":
            assert all(0 <= vi <= 1 for vi in values[v]), "must be between 0 and 1"
        return values

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        _check_lengths({"actual": values["actual"], "lower": values["lower"], "upper": values["upper"]})
        return values

    def __len__(self) -> int:
        return len(self.actual)


@optional_discriminators(["utilization"])
class ReserveMarket(BaseModel):
    """_"""

    price: t.List[float]
    offer_cap: float
    utilization: t.Union[ScalarUtilization, TimeSeriesUtilization] = Field(..., discriminator="dimension_type")
    duration_requirement: float = Field(0.0, description="market requirement for offer duration (hours)")
    obligation: t.Optional[t.List[float]]

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if isinstance(values["utilization"], TimeSeriesUtilization):
            _check_lengths({"price": values["price"], "utilization": values["utilization"]})
        if values["obligation"]:
            _check_lengths({"price": values["price"], "obligation": values["obligation"]})
        return values

    def __len__(self) -> int:
        return len(self.price)


class ReserveMarkets(BaseModel):
    """_"""

    up: t.Optional[t.Dict[str, ReserveMarket]]
    down: t.Optional[t.Dict[str, ReserveMarket]]

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        length = None
        for attrib in "up", "down":
            for v in (values[attrib] or dict()).values():
                if length is None:
                    length = len(v)
                else:
                    assert len(v) == length, "all reserve markets must contain data of the same length"
        return values

    def __len__(self) -> int:
        for v in (self.up or dict()).values():
            return len(v)


class DARTPrices(BaseModel):
    """Mirrors Pandera schema used by the library, but allows for columns of different length, so that users can
    pass, e.g., 5M RTM prices and 1H DAM prices"""

    rtm: conlist(float, min_items=1)
    dam: conlist(float, min_items=1)
    imbalance: t.Optional[conlist(float, min_items=1)]
    rtorpa: t.Optional[conlist(float, min_items=1)]  # this attribute gets dropped on instantiation

    @root_validator(skip_on_failure=True)
    def check_imbalance(cls, values):
        if values["rtorpa"]:
            if values["imbalance"]:
                raise ValueError("Only one of 'rtorpa' and 'imbalance' may be provided")
            values["imbalance"] = values["rtorpa"]
        if values["imbalance"]:
            assert len(values["imbalance"]) == len(values["rtm"]), "Imbalance must have same length as RTM"
        del values["rtorpa"]
        return values


def _check_time_interval(sub_hourly, hourly, time_interval_mins, subhourly_str, hourly_str):
    rt_intervals_per_hour, err = divmod(len(sub_hourly), len(hourly))
    assert err == 0, f"length of {hourly_str} must divide length of {subhourly_str}"
    assert (
        60 / rt_intervals_per_hour == time_interval_mins
    ), f"lengths of {subhourly_str} and {hourly_str} must reflect time_interval_mins"


class DARTPriceScenarios(BaseModel):
    """_"""

    rtm: conlist(conlist(float, min_items=1), min_items=1)
    dam: conlist(conlist(float, min_items=1), min_items=1)
    weights: t.List[float]

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        assert len(values["dam"]) == len(values["rtm"]) == len(values["weights"])
        return values

    def __len__(self):
        return len(self.rtm[0])


class MarketBase(BaseModel):
    """_"""

    energy_prices: t.Union[DARTPrices, t.List[float], DARTPriceScenarios]
    reserve_markets: t.Optional[ReserveMarkets] = None
    time_interval_mins: t.Optional[int] = 60
    load_peak_reduction: t.Optional[LoadPeakReduction] = None
    dam_award: t.Optional[t.List[float]] = None

    @root_validator(skip_on_failure=True)
    def validate_dam_award(cls, values):
        if values["dam_award"] is not None:
            assert isinstance(
                values["energy_prices"], (DARTPrices, DARTPriceScenarios)
            ), "When providing a dam_award, separate DAM and RTM prices are required."
            if isinstance(values["energy_prices"], DARTPriceScenarios):
                rtm_prices = values["energy_prices"].rtm[0]
            else:
                rtm_prices = values["energy_prices"].rtm
            _check_time_interval(
                sub_hourly=rtm_prices,
                hourly=values["dam_award"],
                time_interval_mins=values["time_interval_mins"],
                subhourly_str="rtm prices",
                hourly_str="dam awards",
            )
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval(cls, values):
        if isinstance(values["energy_prices"], DARTPrices):
            _check_time_interval(
                values["energy_prices"].rtm,
                values["energy_prices"].dam,
                values["time_interval_mins"],
                "rtm prices",
                "dam prices",
            )
        return values

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if values["reserve_markets"]:
            if isinstance(values["energy_prices"], DARTPriceScenarios):
                dam_prices = values["energy_prices"].dam[0]
            else:
                dam_prices = values["energy_prices"].dam
            _check_lengths(
                {
                    "dam prices": dam_prices,
                    "reserve market data": values["reserve_markets"],
                }
            )

        if values["load_peak_reduction"]:
            _check_lengths(
                {"rtm prices": values["energy_prices"].rtm, "peak reduction data": values["load_peak_reduction"]}
            )
        return values


class SolarResourceTimeSeries(BaseModel):
    """_"""

    year: t.List[int]
    month: t.List[int]
    day: t.List[int]
    hour: t.List[int]
    minute: t.List[int]
    tdew: t.List[float]
    df: t.List[float]
    dn: t.List[float]
    gh: t.List[float]
    pres: t.List[float]
    tdry: t.List[float]
    wdir: t.List[float]
    wspd: t.List[float]
    alb: t.Optional[t.List[float]]
    snow: t.Optional[t.List[float]]

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        try:
            _check_lengths({k: v for k, v in values.items() if v is not None})
        except AssertionError:
            raise AssertionError("solar resource time series data must have consistent lengths")
        return values

    def __len__(self) -> int:
        return len(self.year)


class SolarResource(BaseModel):
    """_"""

    latitude: float
    longitude: float
    time_zone_offset: float
    elevation: float
    data: SolarResourceTimeSeries
    monthly_albedo: t.Optional[t.List[float]]
    typical: bool = True

    @root_validator(skip_on_failure=True)
    def check_data_if_typical(cls, values):
        if values["typical"]:
            assert (
                len(values["data"].year) % 8760 == 0
            ), "solar resource time series data must represent 1 year when typical is true"
            assert (values["data"].month[0], values["data"].day[0], values["data"].hour[0]) == (
                1,
                1,
                0,
            ), "solar resource data must start at Jan 1, hour 0 when typical is true"
        return values

    def __len__(self) -> int:
        return len(self.data)


class PSMRegion(str, Enum):
    """_"""

    NorthAmerica = "North America"
    AsiaPacific = "Asia/Pacific"


class SolarResourceLocation(BaseModel):
    """_"""

    latitude: float
    longitude: float
    region: PSMRegion = PSMRegion.NorthAmerica

    class Config:
        extra = "forbid"


class FileComponent(BaseModel):
    """_"""

    path: str


class PVModuleCEC(BaseModel):
    """_"""

    bifacial: bool
    a_c: float
    n_s: float
    i_sc_ref: float
    v_oc_ref: float
    i_mp_ref: float
    v_mp_ref: float
    alpha_sc: float
    beta_oc: float
    t_noct: float
    a_ref: float
    i_l_ref: float
    i_o_ref: float
    r_s: float
    r_sh_ref: float
    adjust: float
    gamma_r: float
    bifacial_transmission_factor: float
    bifaciality: float
    bifacial_ground_clearance_height: float


class MermoudModuleTech(str, Enum):
    """_"""

    SiMono = "mtSiMono"
    SiPoly = "mtSiPoly"
    CdTe = "mtCdTe"
    CIS = "mtCIS"
    uCSi_aSiH = "mtuCSi_aSiH"


class PVModuleMermoudLejeune(BaseModel):
    """_"""

    bifacial: bool
    bifacial_transmission_factor: float
    bifaciality: float
    bifacial_ground_clearance_height: float
    tech: MermoudModuleTech
    iam_c_cs_iam_value: t.Optional[t.List[float]]
    iam_c_cs_inc_angle: t.Optional[t.List[float]]
    i_mp_ref: float
    i_sc_ref: float
    length: float
    n_diodes: int
    n_parallel: int
    n_series: int
    r_s: float
    r_sh_0: float
    r_sh_exp: float
    r_sh_ref: float
    s_ref: float
    t_c_fa_alpha: float
    t_ref: float
    v_mp_ref: float
    v_oc_ref: float
    width: float
    alpha_sc: float
    beta_oc: float
    mu_n: float
    n_0: float
    custom_d2_mu_tau: t.Optional[float]


class BaseInverter(BaseModel):
    """_"""

    mppt_low: float
    mppt_high: float
    paco: float
    vdco: float
    pnt: float
    includes_xfmr: bool = False


class Inverter(BaseInverter):
    """_"""

    pso: float
    pdco: float
    c0: float
    c1: float
    c2: float
    c3: float
    vdcmax: float
    tdc: t.List[t.List[float]] = Field(default_factory=lambda: [[1.0, 52.8, -0.021]])


class ONDTemperatureDerateCurve(BaseModel):
    """_"""

    ambient_temp: t.List[float]
    max_ac_power: t.List[float]


class ONDEfficiencyCurve(BaseModel):
    """_"""

    dc_power: t.List[float]
    ac_power: t.List[float]


class ONDInverter(BaseInverter):
    """_"""

    temp_derate_curve: ONDTemperatureDerateCurve
    nominal_voltages: t.List[float]
    power_curves: t.List[ONDEfficiencyCurve]
    dc_turn_on: float
    aux_loss: t.Optional[float]
    aux_loss_threshold: t.Optional[float]

    @root_validator(skip_on_failure=True)
    def check_sufficient_power_curves_voltages(cls, values):
        assert (
            len(values["power_curves"]) == len(values["nominal_voltages"]) == 3
        ), "3 power curves and corresponding voltages required for OND model"
        return values

    @root_validator(skip_on_failure=True)
    def check_aux_loss_etc(cls, values):
        if (values.get("aux_loss") is None) != (values.get("aux_loss_threshold") is None):
            raise AssertionError("either both or neither of aux_loss and aux_loss_threshold must be provided")
        return values


InverterTypes = t.Union[Inverter, ONDInverter, str, FileComponent]
PVModuleTypes = t.Union[PVModuleCEC, PVModuleMermoudLejeune, str, FileComponent]


class Layout(BaseModel):
    """_"""

    orientation: t.Optional[str]
    vertical: t.Optional[int]
    horizontal: t.Optional[int]
    aspect_ratio: t.Optional[float]

    @root_validator(skip_on_failure=True)
    def all_or_none(cls, values):
        missing = [v is None for k, v in values.items()]
        assert all(missing) or not any(missing), "Either all or no attributes must be assigned in Layout"
        return values


class Transformer(BaseModel):
    """_"""

    rating: t.Optional[float]
    load_loss: float
    no_load_loss: float


class ACLosses(BaseModel):
    """_"""

    ac_wiring: float = 0.01
    transmission: float = 0.0
    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    poi_adjustment: float = 0.0  # TODO: deprecate this?
    transformer_load: t.Optional[float]  # deprecate
    transformer_no_load: t.Optional[float]  # deprecate
    hv_transformer: t.Optional[Transformer]
    mv_transformer: t.Optional[Transformer]

    @root_validator(skip_on_failure=True)
    def check_repeated_hv_transformer(cls, values):
        assert (values["transformer_load"] is None and values["transformer_no_load"] is None) or values[
            "hv_transformer"
        ] is None, "Cannot provide hv_transformer if transformer_load or transformer_no_load are provided"
        return values


class DCLosses(BaseModel):
    """_"""

    dc_optimizer: float = 0.0
    enable_snow_model: bool = False
    dc_wiring: float = 0.02
    soiling: t.List[float] = Field(default_factory=lambda: 12 * [0.0])
    diodes_connections: float = 0.005
    mismatch: float = 0.01
    nameplate: float = 0.0
    rear_irradiance: float = 0.0
    mppt_error: float = 0.0  # TODO: remove once mppt_error deprecated, equivalent to tracking_error
    tracking_error: float = 0.0

    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    lid: float = 0.0
    dc_array_adjustment: float = 0.0

    @root_validator(skip_on_failure=True)
    def check_tracker_losses(cls, values):  # TODO: remove once mppt_error deprecated, equivalent to tracking_error
        assert (
            values["mppt_error"] * values["tracking_error"] == 0.0
        ), "Only one of mppt_error and tracking_error may be nonzero"
        return values


class Losses(ACLosses, DCLosses):
    """_"""

    class Config:
        extra = "forbid"


class DCProductionProfile(BaseModel):
    """_"""

    power: t.List[float]
    voltage: t.List[float]
    ambient_temp: t.Optional[t.List[float]]

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        _check_lengths({"power": values["power"], "voltage": values["voltage"]})
        if values["ambient_temp"]:
            _check_lengths({"power": values["power"], "ambient_temp": values["ambient_temp"]})
        return values

    def __len__(self) -> int:
        return len(self.power)


class ACProductionProfile(BaseModel):
    """_"""

    power: t.List[float]
    ambient_temp: t.Optional[t.List[float]]

    # if ACProductionProfile is allowed to have extra fields in the payload, then a DCProductionProfile payload will be
    # coerced into an ACProductionProfile object if something is wrong with voltage
    class Config:
        extra = "forbid"

    @root_validator(skip_on_failure=True)
    def check_length(cls, values):
        if values["ambient_temp"]:
            _check_lengths({"power": values["power"], "ambient_temp": values["ambient_temp"]})
        return values

    def __len__(self) -> int:
        return len(self.power)


ProductionProfile = t.Union[DCProductionProfile, ACProductionProfile]


class BaseSystemDesign(BaseModel):
    """_"""

    dc_capacity: float
    ac_capacity: float
    poi_limit: float


@optional_discriminators(["tracking"])
class PVSystemDesign(BaseSystemDesign):
    """_"""

    modules_per_string: t.Optional[int]
    strings_in_parallel: t.Optional[int]
    tracking: t.Union[FixedTilt, SingleAxisTracking] = Field(..., discriminator="tracking_type")
    azimuth: t.Optional[float]
    gcr: float


class TermUnits(str, Enum):
    """_"""

    hours = "hours"
    days = "days"
    years = "years"


class ProjectTermMixin(BaseModel):
    """_"""

    project_term: int = 1
    project_term_units: TermUnits = "years"


class BaseGenerationModel(ProjectTermMixin):
    """_"""

    project_type: t.Optional[t.Literal["generation"]] = "generation"
    time_interval_mins: int = 60


def scale_project_term_to_hours(project_term: int, project_term_units: TermUnits) -> int:
    if project_term_units == "hours":
        return project_term
    elif project_term_units == "days":
        return 24 * project_term
    else:  # years
        return 8760 * project_term


def _check_time_interval_project_term(
    signal_len, signal_str, project_term, time_interval_mins, project_term_units: TermUnits
):
    """
    For more on why we treat project_term as an int and validate like we do check out this PR comment:
    https://github.com/Tyba-Energy/generation/pull/186#discussion_r1054578658. The broader PR has even more context
    should it be needed
    """
    signal_hours = int(signal_len * (time_interval_mins / 60))
    project_term_hours = scale_project_term_to_hours(project_term, project_term_units)
    assert project_term_hours == signal_hours, (
        f"project_term, project_term_units, time_interval_mins, and length of {signal_str} must be consistent; "
        f"got {project_term}, {project_term_units}, {time_interval_mins}, and {signal_len} respectively"
    )


class ExternalGenerationModel(BaseGenerationModel):
    """_"""

    losses: t.Union[ACLosses, Losses]
    production_override: ProductionProfile
    system_design: BaseSystemDesign

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        _check_time_interval_project_term(
            len(values["production_override"]),
            "production_override",
            values["project_term"],
            values["time_interval_mins"],
            values["project_term_units"],
        )
        return values

    def __len__(self) -> int:
        return len(self.production_override)


class Bus(str, Enum):
    DC = "DC"
    MV = "MV"
    HV = "HV"


class DownstreamSystem(BaseModel):
    """_"""

    losses: ACLosses  # still only ACLosses if modeling from inverter input, since almost every DC loss pertains to PV.
    system_design: BaseSystemDesign
    model_losses_from: Bus
    inverter: t.Optional[InverterTypes]

    @root_validator(skip_on_failure=True)
    def inverter_only_if_dc(cls, values):
        if values["inverter"] is not None:
            assert values["model_losses_from"] == Bus.DC, "model_losses_from must be 'DC' if inverter is provided"
        return values


class ACExternalGenerationModel(ExternalGenerationModel):
    """_"""

    generation_type: t.Optional[t.Literal["ExternalAC"]] = "ExternalAC"
    losses: ACLosses = ACLosses()
    production_override: ACProductionProfile

    @validator("losses")
    def no_mv_xfmr(cls, v: ACLosses):
        assert v.mv_transformer is None, (
            "losses.mv_transformer must be None, since the production_override provided in "
            "an ACExternalGenerationModel is assumed to be at the MV bus"
        )
        return v


class DCExternalGenerationModel(ExternalGenerationModel):
    """_"""

    generation_type: t.Optional[t.Literal["ExternalDC"]] = "ExternalDC"
    losses: Losses = Losses()
    production_override: DCProductionProfile
    inverter: InverterTypes


class ArrayDegradationMode(str, Enum):
    """_"""

    linear = "linear"
    compounding = "compounding"


def _solar_resource_is_typical(solar_resource) -> bool:
    if isinstance(solar_resource, SolarResource) and not solar_resource.typical:
        return False
    return True


def _pv_gen_len(solar_resource, project_term) -> int:
    if isinstance(solar_resource, SolarResource):
        if _solar_resource_is_typical(solar_resource):
            return len(solar_resource) * project_term
        return len(solar_resource)
    return 8760 * project_term


class PVGenerationModel(BaseGenerationModel):
    """_"""

    generation_type: t.Optional[t.Literal["PV"]] = "PV"
    solar_resource: t.Union[SolarResource, t.Tuple[float, float], SolarResourceLocation]
    inverter: InverterTypes
    pv_module: PVModuleTypes
    layout: Layout = Layout()
    losses: Losses = Losses()
    system_design: PVSystemDesign
    array_degradation_rate: float = 0.005
    array_degradation_mode: t.Optional[ArrayDegradationMode] = ArrayDegradationMode.linear

    def __len__(self) -> int:
        return _pv_gen_len(self.solar_resource, self.project_term)

    @root_validator(skip_on_failure=True)
    def check_project_term_units(cls, values):
        if _solar_resource_is_typical(values["solar_resource"]):
            assert (
                values["project_term_units"] == "years"
            ), "project_term_units of 'years' required when typical year is being modeled"
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        _check_time_interval_project_term(
            _pv_gen_len(values["solar_resource"], values["project_term"]),
            "solar_resource",
            values["project_term"],
            values["time_interval_mins"],
            values["project_term_units"],
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_degradation_mode_for_nontypical(cls, values):
        if not _solar_resource_is_typical(values["solar_resource"]):
            assert (
                values["array_degradation_mode"] is None
            ), "PV array degradation not currently supported for non-typical year simulations"
        return values

    @root_validator(skip_on_failure=True)
    def default_azimuth_from_location(cls, values):
        system_design: PVSystemDesign = values["system_design"]
        solar_resource = values["solar_resource"]
        if system_design.azimuth is None:
            if isinstance(solar_resource, tuple):
                system_design.azimuth = 180.0 if solar_resource[0] >= 0.0 else 0.0
            elif isinstance(solar_resource, (SolarResource, SolarResourceLocation)):
                system_design.azimuth = 180.0 if solar_resource.latitude >= 0.0 else 0.0
            else:
                raise NotImplementedError("No default azimuth handling for this solar resource model")
        return values


GenerationModel = Annotated[
    t.Union[PVGenerationModel, DCExternalGenerationModel, ACExternalGenerationModel],
    Field(discriminator="generation_type"),
]


class TableCapDegradationModel(BaseModel):
    """_"""

    annual_capacity_derates: t.List[float]


class TableEffDegradationModel(BaseModel):
    """_"""

    annual_efficiency_derates: t.List[float]


class BatteryHVACParams(BaseModel):
    """_"""

    container_temperature: float
    cop: float
    u_ambient: float
    discharge_efficiency_container: float
    charge_efficiency_container: float
    aux_xfmr_efficiency: float
    container_surface_area: float = 20.0
    design_energy_per_container: float = 750.0


class BatteryParams(BaseModel):
    """_"""

    power_capacity: float
    energy_capacity: float
    charge_efficiency: float
    discharge_efficiency: float
    degradation_rate: t.Optional[float]
    degradation_annual_cycles: float = 261  # cycle / work day
    hvac: t.Optional[BatteryHVACParams]
    capacity_degradation_model: t.Optional[TableCapDegradationModel]
    efficiency_degradation_model: t.Optional[TableEffDegradationModel]
    term: t.Optional[float]

    @root_validator(skip_on_failure=True)
    def check_cap_degradation_models(cls, values):
        assert not (
            values["degradation_rate"] is None and values["capacity_degradation_model"] is None
        ), "Either degradation_rate or capacity_degradation_model must be specified"
        assert (
            values["degradation_rate"] is None or values["capacity_degradation_model"] is None
        ), "Only one of degradation_rate and capacity_degradation_model may be specified"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        term = values["term"] or 0  # validate against term if term is provided
        for dm in "capacity", "efficiency":
            if values[f"{dm}_degradation_model"]:
                assert (
                    len(getattr(values[f"{dm}_degradation_model"], f"annual_{dm}_derates")) - 1 >= term
                ), f"annual_{dm}_derates must be long enough to cover battery term"
        return values


class EnergyStrategy(str, Enum):
    da = "DA"
    rt = "RT"
    dart = "DART"

    def to_market_config(self) -> MarketConfig:
        return {
            "DA": MarketConfig(da=BidOfferStrategy.quantity_only, rt=None),
            "RT": MarketConfig(da=None, rt=BidOfferStrategy.quantity_only),
            "DART": MarketConfig(da=BidOfferStrategy.quantity_only, rt=BidOfferStrategy.quantity_only),
        }[self]


class BidOfferStrategy(str, Enum):
    quantity_only = "quantity-only"
    price_quantity = "price-quantity"
    awarded = "awarded"


class MarketConfig(BaseModel):
    """_"""

    da: t.Optional[BidOfferStrategy]
    rt: t.Optional[BidOfferStrategy]

    @validator("rt")
    def valid_rt_configs(cls, v):
        if v not in {BidOfferStrategy.quantity_only, None}:
            raise ValueError("only quantity-only supported for RTM")
        return v

    @property
    def independent_dam(self) -> bool:
        return self.da is not None and self.rt is not None

    @property
    def value(self) -> str:
        """For symmetry with EnergyStrategy"""
        return json.dumps({"DAM": self.da.value, "RTM": self.rt.value})


default_market_config = MarketConfig(
    da=BidOfferStrategy.quantity_only,
    rt=None,
)


class Solver(str, Enum):
    HiGHS = "HiGHS"
    GLPK = "GLPK"
    HiGHS_GLPK = "HiGHS-GLPK"
    GLPK_HiGHS = "GLPK-HiGHS"


class BoundedFloat(BaseModel):
    actual: float
    min: float
    max: float


class StorageSolverOptions(BaseModel):
    """_"""

    cycling_cost_adder: float = 0.0
    annual_cycle_limit: float = None
    disable_intra_interval_variation: bool = False
    window: int = None
    step: int = None
    flexible_solar: bool = False
    symmetric_reg: bool = False
    energy_strategy: t.Optional[t.Union[EnergyStrategy, MarketConfig]]
    dart: t.Optional[bool]
    uncertain_soe: bool = True
    dam_annual_cycle_limit: float = None
    no_virtual_trades: bool = False
    initial_soe: t.Union[float, BoundedFloat] = 0.0
    duration_requirement_on_discharge: bool = True  # True for ERCOT
    no_stop_offers: bool = False  # just for comparing to competitors
    solver: t.Optional[Solver] = None
    solver_config: SolverConfig = SolverConfig()

    @root_validator(skip_on_failure=True)
    def coerce_strategy_to_market_config(cls, values):
        assert not (values["dart"] is not None and values["energy_strategy"] is not None), (
            "Only one of `dart` or `energy_strategy` may be provided. `dart` is deprecated; use `energy_strategy`"
            " instead."
        )
        strategy = values["energy_strategy"]
        if strategy is None:
            strategy = EnergyStrategy.dart if values["dart"] else EnergyStrategy.da
            values["dart"] = None
        if isinstance(strategy, EnergyStrategy):
            values["energy_strategy"] = strategy.to_market_config()

        if not values["energy_strategy"].independent_dam:
            if values["dam_annual_cycle_limit"] is not None:
                raise ValueError("Must model separate dam and rtm markets if dam_annual_cycle_limit is set")
            if values["no_virtual_trades"]:
                raise ValueError("Must model separate dam and rtm markets if no_virtual_trades is set to True")
        return values

    @root_validator(skip_on_failure=True)
    def check_solver_config(cls, values):
        if values["solver_config"].solver_specific and (values["solver"] not in {"HiGHS", "GLPK"}):
            raise ValueError("solver_specific options may only be passed when using HiGHS or GLPK solver")
        return values


class MultiStorageInputs(StorageSolverOptions):
    """_"""

    batteries: t.List[BatteryParams]

    @validator("batteries")
    def check_battery_terms(cls, v):
        if len(v) > 1:  # don't worry about terms if there's only one battery
            for battery in v:
                assert battery.term, "if multiple batteries are provided, terms must also be provided"
        return v


def _get_price_str_and_price(values):
    if isinstance(values["energy_prices"], DARTPrices):
        return "rtm prices", values["energy_prices"].rtm
    elif isinstance(values["energy_prices"], DARTPriceScenarios):
        return "rtm price", values["energy_prices"]
    else:
        return "energy_prices", values["energy_prices"]


class PeakWindow(BaseModel):
    """_"""

    mask: t.List[bool]
    price: float


class LoadPeakReduction(BaseModel):
    """_"""

    load: t.List[float]
    max_load: t.List[float]  # TODO: should be optional -- https://app.asana.com/0/1178990154879730/1203603348130562/f
    seasonal_peak_windows: t.List[PeakWindow] = []
    daily_peak_windows: t.List[PeakWindow] = []

    @root_validator(skip_on_failure=True)
    def check_lengths(cls, values):
        windows = [*values["seasonal_peak_windows"], *values["daily_peak_windows"]]
        assert (
            windows
        ), "One or both of seasonal_peak_windows and daily_peak_windows must be provided when using load_peak_reduction"
        length = len(values["load"])
        assert len(values["max_load"]) == length, "load and max_load must have same length"
        for window in windows:
            assert len(window.mask) == length, "peak masks must have same length as load"
        return values

    def __len__(self) -> int:
        return len(self.load)


class ImportExportLimitMixin(BaseModel):
    """_"""

    import_limit: t.Optional[t.List[float]]
    export_limit: t.Optional[t.List[float]]

    @root_validator(skip_on_failure=True)
    def validate_limits(cls, values):
        if values["import_limit"] is not None:
            assert all([v <= 0 for v in values["import_limit"]]), "import_limit must be <= 0"
        if values["export_limit"] is not None:
            assert all([v >= 0 for v in values["export_limit"]]), "export_limit must be >= 0"
        return values

    @root_validator(skip_on_failure=True)
    def check_import_export_lengths(cls, values):
        for limit in "import_limit", "export_limit":
            if values[limit]:
                price_str, price = _get_price_str_and_price(values)
                _check_lengths({limit: values[limit], price_str: price})
        return values


def _check_degrad_table_length(values: dict):
    if len(values["storage_inputs"].batteries) == 1:
        battery = values["storage_inputs"].batteries[0]
        pt = (
            scale_project_term_to_hours(
                values.get("project_term") or values["pv_inputs"].project_term,
                values.get("project_term_units") or values["pv_inputs"].project_term_units,
            )
            / 8760
        )
        for dm in "capacity", "efficiency":
            if dm_ob := getattr(battery, f"{dm}_degradation_model"):
                tbl_yrs = len(getattr(dm_ob, f"annual_{dm}_derates")) - 1
                assert tbl_yrs >= pt, f"annual_{dm}_derates must be long enough to cover project/battery term"
    return values


def _check_symmetric_reg_inputs(values: dict):
    if values["storage_inputs"].symmetric_reg:
        assert values.get(
            "reserve_markets"
        ), "when storage_inputs.symmetric_reg is True, reserve_markets must be provided"
        assert ("reg_up" in (values["reserve_markets"].up or dict())) and (
            "reg_down" in (values["reserve_markets"].down or dict())
        ), "when storage_inputs.symmetric_reg is True, both reg_up and reg_down reg markets must be provided"

    return values


def _check_dam_award_against_config(values):
    assert (values["dam_award"] is not None) == (
        values["storage_inputs"].energy_strategy.da == BidOfferStrategy.awarded
    ), "DAM award must be provided if and only if the DAM strategy is 'awarded'"


@optional_discriminators(["pv_inputs"])
class PVStorageModel(ImportExportLimitMixin, MarketBase):
    """_"""

    project_type: t.Optional[t.Literal["hybrid"]] = "hybrid"
    storage_inputs: MultiStorageInputs
    storage_coupling: StorageCoupling
    pv_inputs: GenerationModel
    enable_grid_charge_year: t.Optional[float]

    @property
    def project_term(self) -> int:
        """symmetric retrieval of project_term for convenience"""
        return self.pv_inputs.project_term

    @property
    def project_term_units(self) -> TermUnits:
        return self.pv_inputs.project_term_units

    @root_validator(skip_on_failure=True)
    def check_dam_award_against_config(cls, values):
        _check_dam_award_against_config(values)
        return values

    @root_validator(skip_on_failure=True)
    def check_time_intervals(cls, values):
        assert (
            values["time_interval_mins"] <= values["pv_inputs"].time_interval_mins
        ), "price time_interval_mins must less than or equal to pv time_interval_mins"
        return values

    @root_validator(skip_on_failure=True)
    def check_price_time_interval_against_pv_project_term(cls, values):
        price_str, price = _get_price_str_and_price(values)
        _check_time_interval_project_term(
            len(price),
            price_str,
            values["pv_inputs"].project_term,
            values["time_interval_mins"],
            values["pv_inputs"].project_term_units,
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_battery_terms(cls, values):
        if len(values["storage_inputs"].batteries) > 1:
            total_batt_yrs = sum(bat.term for bat in values["storage_inputs"].batteries)
            assert (
                scale_project_term_to_hours(values["pv_inputs"].project_term, values["pv_inputs"].project_term_units)
                >= total_batt_yrs * 8760
            ), "project_term must be greater than or equal to the total battery terms"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        return _check_degrad_table_length(values)

    @root_validator(skip_on_failure=True)
    def check_sym_reg_inputs(cls, values):
        return _check_symmetric_reg_inputs(values)


class StandaloneStorageModel(ProjectTermMixin, ImportExportLimitMixin, MarketBase):
    """_"""

    project_type: t.Optional[t.Literal["storage"]] = "storage"
    storage_inputs: MultiStorageInputs
    downstream_system: t.Optional[DownstreamSystem]
    ambient_temp: t.Optional[t.List[float]]

    @root_validator(skip_on_failure=True)
    def check_dam_award_against_config(cls, values):
        _check_dam_award_against_config(values)
        return values

    @root_validator(skip_on_failure=True)
    def check_ambient_temp_length(cls, values):
        if values["ambient_temp"]:
            price_str, price = _get_price_str_and_price(values)
            _check_lengths({price_str: price, "ambient_temp": values["ambient_temp"]})
        return values

    @root_validator(skip_on_failure=True)
    def check_time_interval_project_term(cls, values):
        price_str, price = _get_price_str_and_price(values)
        _check_time_interval_project_term(
            len(price), price_str, values["project_term"], values["time_interval_mins"], values["project_term_units"]
        )
        return values

    @root_validator(skip_on_failure=True)
    def check_battery_and_project_terms(cls, values):
        # only validate battery terms if a battery term is passed or multiple batteries are passed
        if len(values["storage_inputs"].batteries) > 1 or values["storage_inputs"].batteries[0].term is not None:
            total_batt_yrs = sum(bat.term for bat in values["storage_inputs"].batteries)
            project_term_hours = scale_project_term_to_hours(values["project_term"], values["project_term_units"])
            total_battery_term_hours = int(total_batt_yrs * 8760)
            assert (
                project_term_hours == total_battery_term_hours
            ), "project_term must be consistent with the total battery terms"
            price_str, price = _get_price_str_and_price(values)
            price_hours = int(len(price) * (values["time_interval_mins"] / 60))
            assert (
                price_hours >= total_battery_term_hours
            ), f"length of {price_str} must be greater than total battery terms"
        return values

    @root_validator(skip_on_failure=True)
    def check_degrad_table_length(cls, values):
        return _check_degrad_table_length(values)

    @root_validator(skip_on_failure=True)
    def check_sym_reg_inputs(cls, values):
        return _check_symmetric_reg_inputs(values)


def get_pv_model(**data: t.Any) -> GenerationModel:
    try:
        m = PVGenerationModel(**data)
    except ValidationError:
        try:
            m = DCExternalGenerationModel(**data)
        except ValidationError:
            m = ACExternalGenerationModel(**data)
    return m


def get_pv_storage_model(**data: t.Any) -> PVStorageModel:
    return PVStorageModel(**data)


def get_standalone_storage_model(model: dict) -> StandaloneStorageModel:
    return StandaloneStorageModel(**model)


JobModel = Annotated[
    t.Union[StandaloneStorageModel, PVStorageModel, GenerationModel], Field(discriminator="project_type")
]


@optional_discriminators(["model"])
class AsyncModelBase(BaseModel):
    """_"""

    id: str
    model: JobModel
    results_path: t.Optional[str]


@optional_discriminators(["model"])
class AsyncPVModel(AsyncModelBase):
    """_"""

    id: str
    model: GenerationModel


class AsyncPVStorageModel(AsyncModelBase):
    """_"""

    id: str
    model: PVStorageModel


class AsyncStandaloneStorageModel(AsyncModelBase):
    """_"""

    id: str
    model: StandaloneStorageModel
