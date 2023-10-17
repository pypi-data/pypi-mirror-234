from typing import Any, List, Dict, Union
from evaluator import Evaluation


class ScoreSummary:
    name: str
    average_score: float


class ComparisonScoreSummary:
    name: str
    diff: float
    improvements: int
    regressions: int


class ExperimentSummary:
    project_name: str
    experiment_name: str
    scores: Dict[str, ScoreSummary]


class ComparisonExperimentSummary:
    project_name: str
    base_experiment_scores: Dict[str, ScoreSummary]
    other_experiment_scores: Dict[str, ScoreSummary]
    comparison_scores: Dict[str, ComparisonScoreSummary]


class Experiment:
    """
    Represents an experiment.
    """

    project: str
    name: str
    description: str

    def __init__(self, project: str, name: str, description: str = None) -> None:
        self.project = project
        self.name = name
        self.description = description

    @classmethod
    def get(
        cls,
        project: str,
        name: str,
    ) -> "Experiment":
        """
        Retrieve an existing experiment.

        Args:
            project (str): Name of the project associated with the experiment.
            name (str): Name of the experiment.

        Returns:
            Experiment: The requested experiment.
        """
        raise NotImplementedError

    @classmethod
    def create(
        cls,
        project: str,
        name: str,
        description: str = None,
    ) -> "Experiment":
        """
        Create a new experiment.

        Args:
            project (str): Name of the project associated with the experiment.
            name (str): Name of the experiment.
            description (str, optional): Description of the experiment. Defaults to None.

        Returns:
            Experiment: The newly created experiment.
        """
        raise NotImplementedError

    def log(
        input: Any = None,
        output: Any = None,
        expected: Any = None,
        evaluations: List[Evaluation] = None,
        metadata: Any = None,
        dataset_row_id: Union[str, int] = None,
    ) -> None:
        """
        Log details about an experiment iteration.

        Args:
            input (Any, optional): Input data for the experiment iteration.
            output (Any, optional): Output data from the experiment iteration.
            expected (Any, optional): Expected results for comparison.
            evaluations (List[Evaluation], optional): List of evaluation results.
            metadata (Any, optional): Additional metadata or info related to the iteration.
            dataset_row_id (Union[str, int], optional): Identifier for the dataset row.
        """
        raise NotImplementedError

    def view_in_browser(self) -> None:
        """
        View the experiment details in a browser.
        """
        raise NotImplementedError

    def summarize(self) -> ExperimentSummary:
        """
        Summarize the results and statistics of the experiment.

        Returns:
            ExperimentSummary: A summary of the experiment results.
        """
        raise NotImplementedError

    def compare(self, other_experiment_name: str) -> ComparisonExperimentSummary:
        """
        Compare the results of this experiment to another experiment.

        Args:
            other_experiment_name (str): Name of the experiment to compare to.

        Returns:
            ExperimentComparisonSummary: A summary of the experiment comparison results.
        """
        raise NotImplementedError
