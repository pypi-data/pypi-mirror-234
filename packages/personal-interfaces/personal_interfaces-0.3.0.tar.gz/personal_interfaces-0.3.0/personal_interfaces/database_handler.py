"""
Model to create and maintain the connection to the Database.
"""
import os
from typing import Dict, Type, Optional, List
# DB library
from deta import Deta, _Base

# The query operational
query_filters: Dict[str, str] = {
    "equal": "",
    "not_equal": "?ne",
    "less_than": "?lt",
    "greater_than": "?gt",
    "less_than_equal": "?lte",
    "greater_than_equal": "?gte",
    "range": "?r",
    "contains": "?contains",
    "not_contains": "?not_contains"
}


class DatabaseHandler:
    """Database model that stablish the connection to the server.

    """
    _db: Deta
    _base: _Base
    _connected: bool = False
    _instances: Dict[Type, Type]

    def connect(self, data_base: str) -> None:
        """
        Stablish the connection to the server.

        Raises:
        -------
            - AssertionError: If the connection is not established.
        """
        project_key = os.environ.get('DB_ACCESS_TOKEN')
        if project_key is None:
            raise Warning("There's no project key valid." +
                          " Add the env variable called `DB_ACCESS_TOKEN`")
        self._db = Deta(project_key=project_key)
        # If everything is cool, then just return the base
        base = self._db.Base(name=data_base)
        self._base = base
        # After that, also set the attribute of connection
        self._connected = True

    # ========================================================== #
    # Add the methods of `QUERY`, `CREATE`, `UPDATE`, `DELETE`   #
    # ========================================================== #

    def query(self, data: Optional[dict] = None, filter_by: str = "equal") -> List[dict]:
        """Query to the DB only if you have a database connection. The filter by
        let you select between all the operators available. The options are:

        - `equal`
        - `not_equal`
        - `less_than`
        - `greater_than`
        - `less_than_equal`
        - `greater_than_equal`
        - `range`
        - `contains`
        - `not_contains`

        Args:
        -------
            - data (dict): Data to use in the `query`.
            - filter_by: (str): Parameter to filter the query. Defaults to "equal".

        Raises:
        -------
            - ConnectionError: If you didn't specify the base first.
        """
        if not self._connected:
            raise ConnectionError(
                "You must connect first to the DB. Please do it with the method `.connect`.")
        # Now, just use kwargs commands to perform the query.
        filter_by = filter_by.lower()
        if filter_by not in query_filters:
            raise ValueError("The filter that you provided is not supported." +
                             f" You gave {filter_by} but the only filters are" +
                             f" `{query_filters.keys()}`.")
        # Now, depending on what did you provide, modify the data
        if data:
            data = {key+query_filters[filter_by]                    : value for key, value in data.items()}
            # Now, search for that in the DB
            response = self._base.fetch(data)
        else:
            response = self._base.fetch()
        # After all the items have been fetched, check if we can return something or not.
        if response.items:
            return response.items
        # If there's no items to return, just return the empty dict
        return [{}]

    def create(self, data: dict) -> str:
        """Perform a creation in the DB.

        Args:
        -------
            - data (dict): Data to use in the `create` method.

        Returns:
        -------
            - Key from the creation of this object.
        """
        if not self._connected:
            raise ConnectionError(
                "You must connect first to the DB. Please do it with the method `.connect`.")
        # Now, just perform the creation of that object.
        response = self._base.insert(data)
        # Return only the key of the element created
        return response["key"]  # type: ignore #

    def update(self, data: Dict[str, str]) -> None:
        """Perform a update of an existing element in the DB.

        Args:
        -------
            - data (dict): Data to use in the `update` method.

        Returns:
        -------
            - Key from the creation of this object.
        """
        if not self._connected:
            raise ConnectionError(
                "You must connect first to the DB. Please do it with the method `.connect`.")
        # Don't need to return nothing, just perform the method
        self._base.put(data, key=data["key"])

    def delete(self, data_id: str) -> None:
        """Delete an existing element in the DB.

        Args:
        -------
            - data (dict): Data to use in the `update` method.

        Returns:
        -------
            - Key from the creation of this object.
        """
        if not self._connected:
            raise ConnectionError(
                "You must connect first to the DB. Please do it with the method `.connect`.")
        # Now, just perform the creation of that object.
        self._base.delete(data_id)
        # Don't need to return nothing
