from typing import Union, List
import datetime as dt
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse, FileResponse

import sunpeek.components.helpers
from sunpeek.api.routers.helper import update_obj
from sunpeek.api.dependencies import session, crud
from sunpeek.api.routers.plant import plant_router
from sunpeek.api.routers.config import config_router
from sunpeek.core_methods.pc_method import AvailablePCFormulae, AvailablePCMethods
from sunpeek.core_methods.pc_method.wrapper import run_performance_check, list_pc_problems
import sunpeek.core_methods.pc_method.plotting as pcp
import sunpeek.common.plot_utils as pu
import sunpeek.serializable_models as smodels
from sunpeek.common.errors import NoDataUploadedError


evaluations_router = APIRouter(
    prefix=plant_router.prefix + "/evaluations",
    tags=["methods", "evaluations"]
)

stored_evaluations_router = APIRouter(
    prefix=config_router.prefix + "/stored_evaluations/{stored_eval_id}",
    tags=["methods", "evaluations"]
)


@evaluations_router.get("/run")
@stored_evaluations_router.get("/run", tags=["methods", "evaluations"])
def run(plant_id: int, stored_eval_id: int, method: str = None,
        eval_start: str = "1900-01-01 00:00:00", eval_end: str = "2021-01-01 00:00:00",
        sess=Depends(session), crd=Depends(crud)):
    crd.get_plants(sess, plant_id=plant_id)
    raise HTTPException(status_code=501,
                        detail="Stored evaluations are not yet implemented in SunPeek", headers=
                        {"Retry-After": "Wed, 30 Nov 2022 23:59 GMT", "Cache-Control": "no-cache"})


@evaluations_router.get("/pc_method", summary="Run the PC method", response_model=smodels.PCMethodOutput)
def run_pc_method(plant_id: int,
                  method: Union[AvailablePCMethods, None] = None,
                  formula: Union[AvailablePCFormulae, None] = None,
                  eval_start: Union[dt.datetime, None] = None,
                  eval_end: Union[dt.datetime, None] = None,
                  ignore_wind: Union[bool, None] = None,
                  safety_pipes: Union[float, None] = None,
                  safety_uncertainty: Union[float, None] = None,
                  safety_others: Union[float, None] = None,
                  sess=Depends(session), crd=Depends(crud)):
    """Runs the PC Method for the specified dates range"""
    plant = crd.get_plants(sess, plant_id=plant_id)
    plant.context.set_eval_interval(eval_start=eval_start, eval_end=eval_end)

    try:
        pc_algo_result = run_performance_check(
            plant=plant,
            method=[method],
            formula=[formula],
            use_wind=[None] if ignore_wind is None else [not ignore_wind],
            safety_pipes=safety_pipes,
            safety_uncertainty=safety_uncertainty,
            safety_others=safety_others,
        )
    except NoDataUploadedError as e:
        # No data uploaded? Return unified error message (not repeated for each strategy tried)
        return JSONResponse(
            status_code=400,
            content={'error': 'Cannot run Performance Check.',
                     'message': str(e)}
        )

    pc_output = pc_algo_result.output
    if pc_output is not None:
        return pc_output

    # pc_output None -> None of the PC strategies was successful -> Return problem report
    return JSONResponse(
        status_code=400,
        content={'error': 'Could not calculate Performance Check.',
                 'message': f'None of the chosen Performance Check strategies '
                            f'({len(pc_algo_result.problems.sub_reports)}) was successful.',
                 'detail': pc_algo_result.problems.parse()}
    )


@evaluations_router.get("/pc_method_problems", summary="Report which PC method variants can be run",
                        response_model=List[smodels.PCMethodProblem])
def list_pc_problems_api(plant_id: int,
                         method: Union[AvailablePCMethods, None] = None,
                         formula: Union[AvailablePCFormulae, None] = None,
                         ignore_wind: Union[bool, None] = None,
                         sess=Depends(session), crd=Depends(crud)) -> List[smodels.PCMethodProblem]:
    """Runs the PC Method for the specified dates range"""
    plant = crd.get_plants(sess, plant_id=plant_id)
    pc_problems = list_pc_problems(
        plant=plant,
        method=[method],
        formula=[formula],
        use_wind=None if ignore_wind is None else [not ignore_wind],
    )

    return pc_problems


@evaluations_router.get("/pc_method_report", summary="Run the PC method and create a pdf report")
def get_pc_method_report(plant_id: int,
                         method: Union[AvailablePCMethods, None] = None,
                         formula: Union[AvailablePCFormulae, None] = None,
                         eval_start: Union[dt.datetime, None] = None,
                         eval_end: Union[dt.datetime, None] = None,
                         ignore_wind: Union[bool, None] = None,
                         safety_pipes: Union[float, None] = None,
                         safety_uncertainty: Union[float, None] = None,
                         safety_others: Union[float, None] = None,
                         with_interval_plots: Union[bool, None] = None,
                         include_creation_date: Union[bool, None] = None,
                         anonymize: Union[bool, None] = None,
                         sess=Depends(session), crd=Depends(crud)):
    """Run the PC Method for the specified dates range and return a pdf report.
    """
    plant = crd.get_plants(sess, plant_id=plant_id)
    # Need to guarantee context is at least bound by plant.time_index, or report plots look weird.
    plant.context.set_eval_interval(eval_start=eval_start, eval_end=eval_end)

    try:
        pc_algo_result = run_performance_check(
            plant=plant,
            method=[method],
            formula=[formula],
            use_wind=[None] if ignore_wind is None else [not ignore_wind],
            safety_pipes=safety_pipes,
            safety_uncertainty=safety_uncertainty,
            safety_others=safety_others,
        )
    except NoDataUploadedError as e:
        # No data uploaded? Return unified error message (not repeated for each strategy tried)
        return JSONResponse(
            status_code=400,
            content={'error': 'Cannot run Performance Check.',
                     'message': str(e)}
        )

    if pc_algo_result.output is None:
        return JSONResponse(
            status_code=400,
            content={'error': 'Could not calculate Performance Check.',
                     'message': f'None of the chosen Performance Check strategies '
                                f'({len(pc_algo_result.problems.sub_reports)}) was successful.',
                     'detail': pc_algo_result.problems.parse()}
        )

    if pc_algo_result.output.plant_output.n_intervals == 0:
        return JSONResponse(
            status_code=400,
            content={'error': 'Performance Check found no intervals.',
                     'message': 'Performance Check found no intervals.',
                     'detail': 'The Performance Check analysis worked, but found no valid intervals in the specific time range.'}
        )

    # Create pdf report
    settings = pu.PlotSettings(with_interval_plots=with_interval_plots,
                               include_creation_date=include_creation_date,
                               anonymize=anonymize)
    pdf_path = pcp.create_pdf_report(pc_output=pc_algo_result.output, settings=settings)
    response = FileResponse(pdf_path, media_type="application/pdf",
                            filename='SunPeek PC report ' + pu.filename_from_string(plant.name))

    return response

# @evaluations_router.get("/pc_method", summary="Run the PC method", response_model=smodels.PCMethodOutput)
# def quick_run_pc_method(plant_id: int, method: AvailablePCMethods,
#                         equation: Union[AvailablePCEquations, None],
#                         eval_start: Union[dt.datetime, None] = None,
#                         eval_end: Union[dt.datetime, None] = None,
#                         sess=Depends(session), crd=Depends(crud)):
#     """Runs the PC Method for the specified dates range"""
#     plant = crd.get_plants(sess, plant_id=plant_id)
#     plant.context.set_eval_interval(eval_start=eval_start, eval_end=eval_end)
#     pc_obj = PCMethod.create(method=method.name, plant=plant, equation=equation)
#     pc_output = pc_obj.run()
#     return pc_output


# @methods_router.get("/get-dcat-method-results")
# async def get_dcat_method_results(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Retrieves the results of the DCAT method for the specified dates range"""
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [1,1,2,1.5] }
#     return results_dict


# @methods_router.get("/run-pc-method")
# async def run_performance_check(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Runs the PC method on the clean data stored between the specified dates range"""
#
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [.35,.39,1.69,4.86,6.23,.51,5.25] }
#
#     return results_dict


# @methods_router.get("/run-dcat-method")
# async def run_dcat_method(plant_id: str, start_date: str = "2021-05-20 13:00:00", end_date: str = "2021-05-21 13:00:00"):
#     """Runs the DCAT method on the clean data stored between the specified dates range"""
#
#     results_dict = {"plant_id": plant_id,"start_date":start_date, "end_date":end_date, "results_array": [.35,.39,1.69,4.86,6.23,.51,5.25] }
#
#     return results_dict


@evaluations_router.get("/pc_method_settings", summary="Get Settings for the PC method", response_model=smodels.PCMethodSettings)
def get_pc_method_settings(plant_id: int, sess=Depends(session), crd=Depends(crud)):
    """Runs the PC Method for the specified dates range"""
    settings = crd.get_components(sess, sunpeek.components.helpers.PCSettingsDefaults, plant_id=plant_id)
    if len(settings) == 1:
        return settings[0]
    return JSONResponse(
        status_code=400,
        content={'error': 'PC Method Settings not found.',
                 'message': 'No PC-Method setting seems to be directly assigned to this plant.',
                 'detail': 'This might happen if the submitted plant_id is incorrect or missing, or in case multiple/no Settings are assigned to the plant due to a inconsitency in the databse.'}
    )

@evaluations_router.post("/pc_method_settings", summary="Update Settings for the PC method", response_model=smodels.PCMethodSettings)
def update_pc_method_settings(plant_id: int, setting_update: smodels.PCMethodSettings, sess=Depends(session), crd=Depends(crud)):
    """Runs the PC Method for the specified dates range"""
    setting = crd.get_components(sess, component=sunpeek.components.helpers.PCSettingsDefaults, plant_id=plant_id)
    if len(setting) != 1:
        return JSONResponse(
            status_code=400,
            content={'error': 'PC Method Settings not found.',
                     'message': 'Settings for the PC-Method not found.',
                     'detail': 'This might happen if the submitted plant_id is incorrect or missing, or in case multiple/no settings are assigned to the plant due to a inconsistency in the database.'}
        )
    setting = setting[0]
    setting = update_obj(setting, setting_update)
    setting = crd.update_component(sess, setting)
    return setting
