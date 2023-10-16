from typing import Optional
from sunpeek.core_methods.virtuals import calculations as algos
from sunpeek.common.errors import CalculationError


def config_virtuals_ambient(array):
    """Virtual sensors for sun- and shadow-related stuff in array.
    """
    # Angle of incidence
    problems = algos.AngleOfIncidence(array).get_config_problems()
    array.map_vsensor('aoi', problems)

    # Internal shading
    problems = algos.InternalShading(array).get_config_problems()
    array.map_vsensor('is_shadowed', problems)
    array.map_vsensor('internal_shading_ratio', problems)
    array.map_vsensor('shadow_angle', problems)
    array.map_vsensor('shadow_angle_midpoint', problems)


def calculate_virtuals_ambient(array):
    # Angle of incidence
    result = algos.AngleOfIncidence(array).run()
    array.aoi.update('aoi', result)

    # Internal shading
    result = algos.InternalShading(array).run()
    # Cannot take is_shadowed from a "feedthrough" strategy because that would not calculate the other outputs,
    # "shadow_angle", "shadow_angle_midpoint" etc.
    if array.is_shadowed.is_virtual:
        array.is_shadowed.update('is_shadowed', result)
    array.internal_shading_ratio.update('internal_shading_ratio', result)
    array.shadow_angle.update('shadow_angle', result)
    array.shadow_angle_midpoint.update('shadow_angle_midpoint', result)


def config_virtuals_power(array):
    # Thermal power
    array.map_vsensor('tp', algos.ThermalPower(array).get_config_problems())
    # Mass flow
    array.map_vsensor('mf', algos.MassFlow(array).get_config_problems())


def calculate_virtuals_power(array):
    # Thermal power
    array.tp.update('tp', algos.ThermalPower(array).run())
    # Mass flow
    array.mf.update('mf', algos.MassFlow(array).run())


def config_virtuals_temperature(array):
    """Virtual sensors for mean operating temperature, temperature derivative etc.
    """
    problems = algos.ArrayTemperatures(array).get_config_problems()
    array.map_vsensor('te_op', problems)
    array.map_vsensor('te_op_deriv', problems)


def calculate_virtuals_temperature(array):
    result = algos.ArrayTemperatures(array).run()
    array.te_op.update('te_op', result)
    array.te_op_deriv.update('te_op_deriv', result)


def config_virtuals_radiation(array):
    """Array plane-of-array irradiance (global, beam, diffuse) including masking, shading etc.
    """
    problems = algos.TiltedIrradiances(array).get_config_problems()
    array.map_vsensor('rd_gti', problems)
    array.map_vsensor('rd_bti', problems)
    array.map_vsensor('rd_dti', problems)

    # Incidence angle modifier
    array.map_vsensor('iam', algos.AlgoIAM(array).get_config_problems())


def calculate_virtuals_radiation(array, strategy: Optional[str] = None):
    """Array irradiance components, including beam shading and diffuse masking.
    """
    if strategy is None:
        algo = algos.TiltedIrradiances(array)
    elif strategy == 'feedthrough':
        strategy = algos.StrategyTiltedIrradiance_feedthrough(array)
        algo = algos.TiltedIrradiances(array, strategies=[strategy])
    else:
        raise CalculationError(f'Unknown strategy string: "{strategy}".')

    result = algo.run()
    array.rd_gti.update('rd_gti', result)
    array.rd_bti.update('rd_bti', result)
    array.rd_dti.update('rd_dti', result)

    # Incidence angle modifier
    result = algos.AlgoIAM(array).run()
    array.iam.update('iam', result)
