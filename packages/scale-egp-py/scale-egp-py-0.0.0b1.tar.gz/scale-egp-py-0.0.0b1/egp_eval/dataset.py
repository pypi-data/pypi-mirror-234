from typing import Any, List, TypedDict, Union
import csv


class RowSubmissions:
    def __init__(self, job_id: Union[str, int]):
        self._job_id = job_id

    @property
    def status(self) -> str:
        """
        Returns:
            str: Status of the row submissions.
        """
        raise NotImplementedError

    @property
    def ids(self) -> List[Union[str, int]]:
        """
        Returns:
            List[Union[str, int]]: Identifiers of the submitted rows.
        """
        raise NotImplementedError


class DatasetRow:
    """
    Represents a single row in a dataset, with input data, expected results, and associated metadata.
    """

    input: Any
    output: Any
    metadata: Any

    def __init__(self, input: Any, output: Any = None, metadata: Any = None):
        """
        Initialize a new dataset row instance.

        Args:
            input (Any):
                Input data for this row.
            output (Any, optional):
                Output data for this row. Defaults to None.
            metadata (Any, optional):
                Additional information or attributes for this row. Defaults to None.
        """
        self.input = input
        self.output = output
        self.metadata = metadata

    @property
    def id() -> Union[str, int]:
        """
        Retrieve the identifier for the dataset row.

        Returns:
            Union[str, int]: An identifier for the dataset row.
        """
        raise NotImplementedError


class DatasetSummary:
    num_rows: int


class CreateDatasetRowInput(TypedDict):
    input: Any
    expected: Any
    metadata: Any


class Dataset:
    """
    Represents a dataset.
    """

    name: str
    description: str
    _version: Union[str, int]

    def __init__(
        self,
        name: str = None,
        description: str = None,
        version: Union[str, int] = None,
    ):
        self.name = name
        self.description = description
        self._version = version

    @classmethod
    def say_hello(cls):
        print("Print - Hello from EGP")
        return "Return - Hello from EGP"

    @classmethod
    def get(
        cls,
        name: str,
        version: Union[str, int] = None,
    ) -> "Dataset":
        """
        Retrieve a dataset.

        Args:
            name (str): Name of the dataset.
            version (Union[str, int], optional): Version identifier for the dataset.

        Returns:
            Dataset: The requested dataset.
        """
        raise NotImplementedError

    @classmethod
    def create(
        cls,
        name: str,
        description: str = None,
    ) -> "Dataset":
        """
        Create a new dataset.

        Args:
            name (str): Name of the dataset.
            description (str, optional): Description of the dataset.
            version (Union[str, int], optional): Version identifier for the dataset.

        Returns:
            Dataset: The newly created dataset.
        """
        raise NotImplementedError

    def delete_row(
        self,
        id: Union[str, int],
    ) -> None:
        """
        Delete a specific row from the dataset by ID.

        Args:
            id (Union[str, int]): Identifier of the row to delete.
        """
        raise NotImplementedError

    def update_row(
        self,
        id: Union[str, int],
        input: Any,
        output: Any,
        metadata: Any = None,
    ) -> None:
        """
        Update a specific row in the dataset by ID.

        Args:
            id (Union[str, int]): Identifier of the row to update.
            input (Any): New input data for the row.
            output (Any): New output data for the row.
            metadata (Any, optional): New metadata for the row.
        """
        raise NotImplementedError

    def get_row(
        self,
        id: Union[str, int],
    ) -> DatasetRow:
        """
        Retrieve a specific row from the dataset by ID.

        Args:
            id (Union[str, int]): Identifier of the row to retrieve.

        Returns:
            DatasetRow: The row with the specified ID.
        """
        raise NotImplementedError

    def insert_row(
        self,
        row: CreateDatasetRowInput,
    ) -> Union[str, int]:
        """
        Insert a new row into the dataset.

        Args:
            row (CreateDatasetRowInput): New row to insert.

        Returns:
            Union[str, int]: Identifier of the inserted row.
        """
        raise NotImplementedError

    def insert_rows(
        self,
        rows: List[CreateDatasetRowInput],
    ) -> RowSubmissions:
        """
        Insert new rows into the dataset.

        Args:
            rows (List[CreateDatasetRowInput]): List of new rows to insert.

        Returns:
            RowSubmissions: Identifier of the inserted rows.
        """
        raise NotImplementedError

    def insert_from_csv(
        self,
        file_path: str,
        input_column: str,
        expected_column: str = None,
        metadata_columns: List[str] = None,
    ) -> None:
        """
        Inserts rows into the dataset from a CSV file.

        Args:
            file_path (str): Path to the CSV file.
            input_column (str): The column representing input.
            expected_column (str, optional): The column representing the expected value.
            metadata_columns (List[str]): Columns containing metadata.
        """
        with open(file_path, "r") as data_csv:
            reader = csv.reader(data_csv)
            self.insert(
                [
                    {
                        "input": row[input_column],
                        "expected": row[
                            expected_column
                        ],  # Optional ground truth output
                        "metadata": {
                            column: row[column] for column in metadata_columns
                        },
                    }
                    for row in reader
                ]
            )

    def insert_from_pandas_df(
        self,
        df,
        input_column: str,
        expected_column: str = None,
        metadata_columns: List[str] = None,
    ) -> None:
        """
        Inserts rows into the dataset from a Pandas DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to insert.
            input_column (str): The column representing input.
            expected_column (str, optional): The column representing the expected value.
            metadata_columns (List[str]): Columns containing metadata.
        """
        self.insert(
            [
                {
                    "input": row[input_column],
                    "expected": row[expected_column],  # Optional ground truth output
                    "metadata": {column: row[column] for column in metadata_columns},
                }
                for row in df
            ]
        )

    @property
    def rows() -> List[DatasetRow]:
        """
        Returns the rows present in the dataset.

        Returns:
            List[DatasetRow]: A list of rows in the dataset.
        """
        raise NotImplementedError

    def _fetch(self):
        for record in self.rows:
            yield {
                "id": record.id,
                "input": record.input,
                "expected": record.expected,
                "metadata": record.metadata,
            }

    def __iter__(self):
        return self._fetch()

    def view_in_browser() -> None:
        """
        Opens the dataset in a browser for viewing.
        """
        raise NotImplementedError

    def summarize() -> DatasetSummary:
        """
        Summarize the data in the dataset.
        """
        raise NotImplementedError

    @property
    def id() -> Union[str, int]:
        raise NotImplementedError
