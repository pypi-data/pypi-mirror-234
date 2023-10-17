from typing import Optional, List, Any


class Project():
    """
    Represents a project which acts as a namespace to group experiments.

    name (str): The name of the project, used as the primary identifier.
    description (str): A brief description providing additional details about the project.
    """

    name: str
    description: Optional[str]

    def __init__(self, name: str, description: Optional[str]) -> None:
        """
        Initializes a new Project instance.

        Args:
            name (str): The name of the project.
            description (str, optional): A brief description of the project. Defaults to None.
        """
        self.name = name
        self.description = description

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str] = None,
    ) -> "Project":
        """
        Create a new project.

        Args:
            name (str): Name of the project.
            description (str, optional): Description of the project. Defaults to None.

        Returns:
            Project: The newly created project.
        """
        raise NotImplementedError

    @classmethod
    def get(
        cls,
        name: str,
    ) -> "Project":
        """
        Retrieve an existing project.

        Args:
            name (str): Name of the project.

        Returns:
            Project: The requested project.
        """
        raise NotImplementedError

    @property
    def experiments(self) -> List[Any]:
        """
        Retrieve the list of experiments associated with this project.

        Returns:
            List[Any]: List of experiments associated with this project.
        """
        raise NotImplementedError
