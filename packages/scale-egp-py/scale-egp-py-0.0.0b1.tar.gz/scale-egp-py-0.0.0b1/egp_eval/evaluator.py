from __future__ import annotations
from abc import ABC, abstractproperty
from typing import Any, Dict, List


class Score:
    def __init__(
        self,
        value: float,
    ) -> None:
        self.value = value

    def __post_init__(self):
        if self.value < 0 or self.value > 1:
            raise ValueError(f"score ({self.value}) must be between 0 and 1")


class Evaluation(ABC):
    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def scores(self) -> Dict[str, Score]:
        pass

    @abstractproperty
    def error(self) -> Exception:
        pass


class AutoEvaluation(Evaluation):
    name: str
    scores: Dict[str, Score]
    error: Exception

    def __init__(
        self,
        name: str,
        scores: Dict[str, Score],
        error: Exception,
    ):
        self.name = name
        self.scores = scores
        self.error = error


class HumanEvaluation(Evaluation):
    """
    Represents a human-based evaluation.
    """

    def __init__(
        self,
        job_id: str,
    ) -> None:
        self._job_id = job_id

    @property
    def status(self) -> str:
        """
        Returns:
            str: Status of the human evaluation.
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        Returns:
            str: Name of the human evaluation.
        """
        raise NotImplementedError

    @property
    def scores(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Dictionary of scores.
        """
        raise NotImplementedError

    @property
    def error(self) -> Exception:
        """
        Returns:
            Exception: Exception that occurred during evaluation.
        """
        raise NotImplementedError


class Evaluator(ABC):
    """
    An Evaluator is responsible for grading outputs.

    Evaluators return either:
        A score from [0,1], or:
        A dict of scores from [0,1].
    """

    def eval(
        self,
        output: Any,
        expected: Any = None,
        input: Any = None,
        **kwargs,
    ) -> Evaluation:
        raise NotImplementedError


# Evaluators require an output, and optionally can take an expected output
# and an input.

# We will require people to use instances of an evaluator, not the class itself.

# For HumanEvaluators, they must be statefully created/fetched from the server
# so that they are backed by an annotation project.

# For AutoEvaluators, they can be stateless.

# To figure out:
# - How do we handle the typing for long-running async evaluator responses
#   like HumanEvaluators?


class TaxonomyField:
    def __init__(
        self,
        field_id: str,
        title: str,
        choices: List[Dict[str, float]],
        conditions: List[Dict[str, str]],
    ) -> None:
        self.field_id = field_id
        self.title = title
        self.choices = choices
        self.conditions = conditions


class HumanEvaluator(Evaluator):
    """
    Decisions:
    1. HumanEvaluator objects are stateful and must be backed by a Studio project
    which is saved on the server.
    """

    @classmethod
    def create(
        cls,
        name: str,
        annotation_project_id: str = None,
    ) -> HumanEvaluator:
        """
        Create a HumanEvaluator. Under the hood, this creates a Studio project
        with project-level instructions. All evaluations of this HumanEvaluator
        will be created as tasks in the associated Studio project.

        Args:
            name (str):
                Name of the HumanEvaluator to be created.

        Returns:
            HumanEvaluator: Instance of the created HumanEvaluator.

        Supported attachments: https://docs.scale.com/reference/textcollectionattachment
        Supported taxonomy fields: https://docs.scale.com/reference/unitfield
        """
        raise NotImplementedError

    @classmethod
    def get(
        cls,
        name: str,
    ) -> HumanEvaluator:
        """
        Get an existing HumanEvaluator from the server.

        Args:
            name (str):
                Name of the HumanEvaluator to retrieve.

        Returns:
            HumanEvaluator: Instance of the retrieved HumanEvaluator.
        """
        raise NotImplementedError

    def eval(
        self,
        output: str,
        attachments: List[Any],
        fields: List[TaxonomyField],
        expected: str = None,
        input: str = None,
        instructions_url: str = None,
    ) -> Evaluation:
        """
        Call the Studio task creation API to create a new evaluation task.

        Args:
            output (str):
                The output data to be evaluated.
            attachments (List[Any]):
                List of supported attachments for the evaluation.
            fields (List[TaxonomyField]):
                List of taxonomy fields for the evaluation.
            expected (str, optional):
                The expected result for comparison. Defaults to None.
            input (str, optional):
                The input data for evaluation. Defaults to None.
            instructions_url (str, optional):
                URL linking to the instructions. Defaults to None.

        Returns:
            Evaluation: The created evaluation instance.
        """
        raise NotImplementedError

    def __init__(self, name: str = None):
        """
        API users should not call this method directly. Instead, use
        HumanEvaluator.create() or HumanEvaluator.get().

        Creates an instance of a HumanEvaluator.
        """
        raise NotImplementedError

    def view_in_browser() -> None:
        raise NotImplementedError
