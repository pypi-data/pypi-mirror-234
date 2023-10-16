from sunpeek.core_methods.virtuals import calculations as algos


def config_virtuals_ambient(plant):
    """Solar position, airmass, clearsky radiation, dew point"""
    problems = algos.SolarPosition(plant).get_config_problems()
    plant.map_vsensor('sun_azimuth', problems)
    plant.map_vsensor('sun_zenith', problems)
    plant.map_vsensor('sun_apparent_zenith', problems)
    plant.map_vsensor('sun_elevation', problems)
    plant.map_vsensor('sun_apparent_elevation', problems)

    # The following algorithms are commented because they are not needed for now (because radiation conversion
    # is not active at the moment).

    # Dew point temperature
    # problems = algos.DewPointTemperature(plant).config_problems
    # plant.map_vsensor('te_dew_amb', problems)

    # Clearsky solar radiation
    # problems = algos.DNIExtra(plant).config_problems
    # plant.map_vsensor('rd_dni_extra', problems)

    # Airmass
    # problems = algos.Airmass(plant).config_problems
    # plant.map_vsensor('rel_airmass', problems)
    # plant.map_vsensor('abs_airmass', problems)

    # Turbidity
    # Not needed for now, uncomment if needed.
    # problems = algos.LinkeTurbidity(plant).config_problems
    # plant.map_vsensor('linke_turbidity', problems)

    # Clearsky radiation
    # problems = algos.ClearskyRadiation(plant).config_problems
    # plant.map_vsensor('rd_ghi_clearsky', problems)
    # plant.map_vsensor('rd_dni_clearsky', problems)


def calculate_virtuals_ambient(plant):
    # Solar position
    result = algos.SolarPosition(plant).run()
    plant.sun_azimuth.update('azimuth', result)
    plant.sun_zenith.update('zenith', result)
    plant.sun_apparent_zenith.update('apparent_zenith', result)
    plant.sun_elevation.update('elevation', result)
    plant.sun_apparent_elevation.update('apparent_elevation', result)

    # Dew point temperature
    # result = algos.DewPointTemperature(plant).run()
    # plant.te_dew_amb.update('te_dew_amb', result)

    # Extraterrestrial solar radiation
    # result = algos.DNIExtra(plant).run()
    # plant.rd_dni_extra.update('dni_extra', result)

    # Airmass
    # result = algos.Airmass(plant).run()
    # plant.rel_airmass.update('rel_airmass', result)
    # plant.abs_airmass.update('abs_airmass', result)

    # Turbidity
    # result = algos.LinkeTurbidity(plant).run()
    # plant.linke_turbidity.update('linke_turbidity', result)

    # Clearsky radiation
    # result = algos.ClearskyRadiation(plant).run()
    # plant.rd_ghi_clearsky.update('ghi_clearsky', result)
    # plant.rd_dni_clearsky.update('dni_clearsky', result)


def config_virtuals_power(plant):
    # Thermal power
    plant.map_vsensor('tp', algos.ThermalPower(plant).get_config_problems())
    # Mass flow
    plant.map_vsensor('mf', algos.MassFlow(plant).get_config_problems())


def calculate_virtuals_power(plant):
    # Thermal power
    result = algos.ThermalPower(plant).run()
    plant.tp.update('tp', result)
    # Mass flow
    result = algos.MassFlow(plant).run()
    plant.mf.update('mf', result)


def config_virtuals_radiation(plant):
    """Horizontal irradiance components from plant radiation input slots
    """
    pass
#     # problems = algos.HorizontalIrradiances(plant).config_problems
#     # plant.map_vsensor('rd_ghi', problems)
#     # plant.map_vsensor('rd_bhi', problems)
#     # plant.map_vsensor('rd_dhi', problems)
#     # plant.map_vsensor('rd_dni', problems)


def calculate_virtuals_radiation(plant):
    """Horizontal irradiance components from plant radiation input slots
    """
    pass
#     # ghi, bhi, dhi, dni = algos.HorizontalIrradiances(plant).run()
#     # plant.rd_ghi.update(ghi)
#     # plant.rd_bhi.update(bhi)
#     # plant.rd_dhi.update(dhi)
#     # plant.rd_dni.update(dni)
