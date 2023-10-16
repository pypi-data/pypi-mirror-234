import enum
import time
import traceback
from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod
import pandas as pd

from sunpeek.common.errors import AlgorithmError
from sunpeek.common.utils import sp_logger
from sunpeek.components import Plant, Component
from sunpeek.components.base import AlgoCheckMode
from sunpeek.components.fluids import UninitialisedFluid
from sunpeek.components.types import UninitialisedCollector
from sunpeek.serializable_models import ProblemType, AlgoProblem, ProblemReport


@dataclass
class AlgoResult:
    """AlgoResult is returned by CoreAlgorithm.run(). It holds the algorithm output, the successful strategy (on of all
    possible algorithm strategies), and a ProblemReport with details about problems in any of the strategies.
    """
    output: Optional[Any]
    successful_strategy: Optional['CoreStrategy']
    problems: Optional[ProblemReport]

    @property
    def success(self):
        return self.problems.success

    @property
    def successful_strategy_str(self):
        return self.problems.successful_strategy_str


class CoreStrategy(ABC):
    """Strategy of some CoreAlgorithm. To be attached to an algorithm with algo.define_strategies().

    A strategy is defined for a specific component and should implement methods calc() and _report_problems().
    """
    name = '(unnamed strategy)'
    feedthrough_real_sensor = False

    def __init__(self, component: Component):
        self.component: Component = component

    @abstractmethod
    def _calc(self):
        """Implement calculation of strategy, using information from self.component
        """
        raise NotImplementedError()

    @abstractmethod
    def _report_problems(self, check_mode: AlgoCheckMode) -> ProblemReport:
        """Return list of AlgoProblem objects.
        #
        # Raises
        # ------
        # AttributeError : if component has no slot or attribute with a name required by the .
        """
        raise NotImplementedError()

    def get_problem_report(self, check_mode: AlgoCheckMode) -> ProblemReport:
        report = self._report_problems(check_mode)
        if not isinstance(report, ProblemReport):
            raise AlgorithmError(f'Strategy "{self}" returned problems with invalid type. Expected "ProblemReport", '
                                 f'got "{type(report)}".')
        return report

    def execute(self):
        """Try to calculate strategy, sanitize check output dict and return if ok.

        Returns
        -------
        elapsed_time : float, elapsed time in algorithm in seconds
        output : dict, strategy output, values are asserted to be unit-aware (pint-pandas) Series.

        Raises
        ------
        AlgorithmError
        """
        start_time = time.time()
        output = self._calc()
        elapsed_time = time.time() - start_time
        self.check_output(output)

        return elapsed_time, output

    def check_output(self, output):
        """Additional checks to be performed on output of a strategy.
        """
        pass

    @property
    def plant(self):
        return self.component.plant

    def __repr__(self):
        return f'SunPeek {self.__class__.__name__} called "{self.name}"'

    def __str__(self):
        return self.__class__.__name__


class VirtualSensorStrategy(CoreStrategy):  # noqa

    def check_output(self, output):
        """Specific checks for the output of virtual sensor calculations.
        """
        super().check_output(output)
        if not isinstance(output, dict):
            raise AlgorithmError(f'Strategy "{self}": Expected dict from call to execute(), but got {type(output)}.')

        for k, v in output.items():
            if v is None:
                if self.feedthrough_real_sensor:
                    # Output is allowed to be None for strategies that only use a real sensor, example:
                    # power_from_real_sensor strategy
                    continue
                else:
                    raise AlgorithmError(
                        f'Strategy "{self}": Calculation output {k} is None, expected pd.Series.')

            if not isinstance(v, pd.Series):
                raise AlgorithmError(f'Strategy "{self}": Calculation output {k} is {type(v)}, expected pd.Series.')

            # Test for length of calculated data
            if len(v) != len(self.plant.time_index):
                raise AlgorithmError(
                    f'Strategy "{self}": Size of returned virtual sensor data ({len(v)}) is incompatible with size of '
                    f'"Plant.time_index" ({len(self.plant.time_index)}).')

            # Test for a unit-aware (pint) pd.Series
            try:
                v.pint
            except AttributeError:
                raise AlgorithmError(f'Strategy "{self}": Calculation output {k} is pd.Series as expected, '
                                     f'but is not unit-aware (it lacks a dtype from pint-pandas).')


class StrategyErrorBehavior(str, enum.Enum):
    skip = 'skip'
    error = 'error'


# noinspection PyArgumentList
class CoreAlgorithm(ABC):
    """Superclass for all SunPeek core algorithms, mainly virtual sensors, PC (Performance Check) method and D-CAT
    energy yield methods.

    This class handles various strategies for an algorithm (e.g. various implementations to calculate thermal power,
    or various Performance Check methods, equations etc.

    *args and **kwargs passed to object creation are forwarded to :meth:`define_strategies`.
    """

    def __init__(self, component: Component, strategies: Optional[List[VirtualSensorStrategy]] = None, *args, **kwargs):
        self.component = component
        self.strategies = strategies or self.define_strategies(*args, **kwargs)
        self.problems = ProblemReport()

    @abstractmethod
    def define_strategies(self, *args, **kwargs) -> List[VirtualSensorStrategy]:
        raise NotImplementedError()

    def run(self, on_strategy_error: StrategyErrorBehavior = 'skip') -> AlgoResult:
        """Calculates algorithm using its defined strategies, stopping at the first successful strategy.

        Parameters
        ----------
        on_strategy_error : str, optional
            If 'raise', exceptions that occur during a strategy.execute() are raised. If not, they are saved as
            own_problems in self.problems. In any case, errors are logged.

        Raises
        ------
        AlgorithmError : if algorithm has no strategies defined, or if getting some strategy problems fails.
        """
        if on_strategy_error not in list(StrategyErrorBehavior):
            raise AlgorithmError(f'Invalid value for "on_strategy_error": {on_strategy_error}. '
                                 f'Valid values are: {", ".join(StrategyErrorBehavior)}')

        if not self.strategies:
            raise AlgorithmError(f'Cannot run algo "{self}": No calculation strategies defined.')

        self.problems = ProblemReport(success=False)
        for strategy in self.strategies:
            report = strategy.get_problem_report(check_mode=AlgoCheckMode.config_and_data)
            self.problems.add_sub(strategy.name, report)

            if report.success:
                try:
                    elapsed_time, output = strategy.execute()
                    self.problems.success = True
                    self.problems.problem_slots = report.problem_slots
                    sp_logger.debug(f'Done in {elapsed_time:3.1f}s '
                                    f'Algo "{self}" run() on component "{self.component.name}": '
                                    f'Successful using strategy "{strategy.name}". ')
                    return AlgoResult(output, strategy, self.problems)

                except Exception as e:
                    # The philosophy behind catching all Exceptions here: We always calculate all virtual sensors
                    # at `calculate_virtuals(plant)`, we don't know beforehand and therefore don't calculate virtuals
                    # specifically for some particular evaluation (like the PC method).
                    # For example: A particular virtual sensor that is not required by the PC method might fail
                    # to calculate, but that would not affect running the PC method. That's why we decided to catch
                    # all exceptions during calculation here and report them as `AlgoProblem`.
                    # The full exception trace is reported in the log files.
                    sp_logger.error(f'Algo "{self}" run() on component {self.component.name}: '
                                    f'error in strategy.execute() for "{strategy}": {traceback.format_exc()}')
                    if on_strategy_error == StrategyErrorBehavior.error:
                        raise
                    else:
                        self.problems.add_own(
                            AlgoProblem(ProblemType.unexpected_in_calc,
                                        description=f'An unexpected calculation error of type "{type(e)}" has occurred '
                                                    f'during calculation of strategy "{strategy}". '
                                                    f'For further information, see '
                                                    f'https://docs.sunpeek.org/errors.html#unexpected-calculation-error'))

        sp_logger.info(f'Algo "{self}" run(): Could not calculate, none of the {len(self.strategies)} strategies was '
                       f'successful.')

        return AlgoResult(None, None, self.problems)

    def get_config_problems(self) -> ProblemReport:
        """Cycle through all algo strategies, return ProblemReport of all strategy problems.
        Stops at first successful strategy, copies problem slots from strategy.
        """
        if not self.strategies:
            raise AlgorithmError(f'Cannot run algo "{self}": No calculation strategies defined.')

        algo_report = ProblemReport(success=False)
        for strategy in self.strategies:
            report = strategy.get_problem_report(AlgoCheckMode.config_only)
            algo_report.add_sub(strategy.name, report)
            if report.success:
                algo_report.success = True
                algo_report.problem_slots = report.problem_slots
                break

        return algo_report

    def allowed_components(self) -> tuple:
        # List of allowed components. By default, only Plant is allowed.
        return Plant,

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, val):
        allowed_components = self.allowed_components()
        if not isinstance(allowed_components, tuple):
            raise AlgorithmError(f'Algo "{self}": allowed_components() returned invalid type. '
                                 f'Expected tuple, got {type(allowed_components)}.')
        for c in allowed_components:
            if not issubclass(c, Component):
                raise AlgorithmError(f'Algo "{self}": allowed_components() returned an invalid component '
                                     f'of class "{c.__name__}". '
                                     f'Allowed components must be subclasses of "Component", e.g. Plant, Array etc.')
        if not isinstance(val, self.allowed_components()):
            raise AlgorithmError(f'Algo "{self}" got a component of invalid type {str(val)}. '
                                 f'Valid types are: {self.valid_components}.')

        self._component = val

    @property
    def strategies(self):
        if self._strategies is None:
            self._strategies = self.define_strategies()
        return self._strategies

    @strategies.setter
    def strategies(self, strategies):
        if strategies is None:
            self._strategies = []
            return

        for s in strategies:
            if not issubclass(type(s), CoreStrategy):
                raise AlgorithmError(f'Cannot add strategy to algorithm {self}: '
                                     f'Expected "CoreStrategy" object, but got "{type(s)}".')

        snames = [s.name for s in strategies]
        duplicates = [x for n, x in enumerate(snames) if x in snames[:n]]
        if duplicates:
            raise AlgorithmError(f'Cannot add strategies with duplicate names to algo "{self}". '
                                 f'Duplicate strategy names: {", ".join(duplicates)}.')

        self._strategies = strategies

    @property
    def valid_components(self):
        valid_component_names = [c.__name__ for c in self.allowed_components()]
        return ', '.join(valid_component_names)

    @property
    def successful_strategy(self) -> Optional[CoreStrategy]:
        for strategy in self.strategies:
            r = strategy.get_problem_report(AlgoCheckMode.config_only)
            if r.success:
                return strategy
        return None

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'SunPeek algorithm "{self.__class__.__name__}"'


## Specific validation code

def is_valid_fluid(fluid, check_mode: AlgoCheckMode) -> bool:
    if check_mode == AlgoCheckMode.config_only:
        return fluid is not None
    return (fluid is not None) and (not isinstance(fluid, UninitialisedFluid))


def is_valid_collector(collector, check_mode: AlgoCheckMode) -> bool:
    if check_mode == AlgoCheckMode.config_only:
        return collector is not None
    return (collector is not None) and (not isinstance(collector, UninitialisedCollector))
