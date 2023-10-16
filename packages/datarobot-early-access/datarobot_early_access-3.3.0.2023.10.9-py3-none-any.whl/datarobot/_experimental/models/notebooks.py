#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot._experimental.models.enums import NotebookPermissions, NotebookStatus
from datarobot.models.api_object import APIObject
from datarobot.models.use_cases.utils import resolve_use_cases, UseCaseLike
from datarobot.utils.pagination import unpaginate

notebook_user_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("username"): t.String,
        t.Key("first_name"): t.String,
        t.Key("last_name"): t.String,
    }
)


notebook_activity_trafaret = t.Dict(
    {
        t.Key("at"): t.String,
        t.Key("by"): notebook_user_trafaret,
    }
)


notebook_settings_trafaret = t.Dict(
    {
        t.Key("show_line_numbers"): t.Bool,
        t.Key("hide_cell_titles"): t.Bool,
        t.Key("hide_cell_outputs"): t.Bool,
        t.Key("show_scrollers"): t.Bool,
    }
)


notebook_session_trafaret = t.Dict(
    {
        t.Key("status"): t.String,
        t.Key("notebook_id"): t.String,
        t.Key("started_at", optional=True): t.String,
    }
)


class NotebookUser(APIObject):
    """
    A user associated with a Notebook.

    Attributes
    ----------

    id : str
        The ID of the user.
    username : str
        The username of the user, usually their email address.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    """

    _converter = notebook_user_trafaret

    def __init__(self, id: str, username: str, first_name: str, last_name: str):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class NotebookSession(APIObject):
    """
    Information about the current status of a Notebook.

    Attributes
    ----------

    status : NotebookStatus
        The current status of the Notebook kernel.
    notebook_id : str
        The ID of the Notebook.
    started_at : Optional[str]
        The date and time when the notebook was started. Optional.
    """

    _converter = notebook_session_trafaret

    def __init__(self, status: NotebookStatus, notebook_id: str, started_at: Optional[str] = None):
        self.status = status
        self.notebook_id = notebook_id
        self.started_at = started_at


class NotebookActivity(APIObject):
    """
    A record of activity (i.e. last run, updated, etc.) in a Notebook.

    Attributes
    ----------

    at : str
        The time of the activity in the notebook.
    by : NotebookUser
        The user who performed the activity.
    """

    _converter = notebook_activity_trafaret

    def __init__(self, at: str, by: Dict[str, str]):
        self.at = at
        self.by = NotebookUser.from_server_data(by)


class NotebookSettings(APIObject):
    """
    Settings for a DataRobot Notebook.

    Attributes
    ----------

    show_line_numbers : bool
        Whether line numbers in cells should be displayed.
    hide_cell_titles : bool
        Whether cell titles should be displayed.
    hide_cell_outputs : bool
        Whether the cell outputs should be displayed.
    show_scrollers : bool
        Whether scrollbars should be shown on cells.
    """

    _converter = notebook_settings_trafaret

    def __init__(
        self,
        show_line_numbers: bool,
        hide_cell_titles: bool,
        hide_cell_outputs: bool,
        show_scrollers: bool,
    ):
        self.show_line_numbers = show_line_numbers
        self.hide_cell_titles = hide_cell_titles
        self.hide_cell_outputs = hide_cell_outputs
        self.show_scrollers = show_scrollers


class Notebook(APIObject):
    """
    Metadata for a DataRobot Notebook accessible to the user.

    Attributes
    ----------

    id : str
        The ID of the Notebook.
    name : str
        The name of the Notebook.
    permissions : List[NotebookPermission]
        The permissions the user has for the Notebook.
    tags : List[str]
        Any tags that have been added to the Notebook. Default is an empty list.
    created : NotebookActivity
        Information on when the Notebook was created and who created it.
    updated : NotebookActivity
        Information on when the Notebook was updated and who updated it.
    last_viewed : NotebookActivity
        Information on when the Notebook was last viewed and who viewed it.
    settings : NotebookSettings
        Information on global settings applied to the Notebook.
    org_id : str
        The organization ID associated with the Notebook.
    description : Optional[str]
        The description of the Notebook. Optional.
    session : Optional[NotebookSession]
        Metadata on the current status of the Notebook and its kernel. Optional.
    use_case_id : Optional[str]
        The ID of the Use Case the Notebook is associated with. Optional.
    """

    _path = "api-gw/nbx/notebooks/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("name"): t.String,
            t.Key("description", optional=True): t.Or(t.String, t.Null),
            t.Key("permissions"): t.List(t.String),
            t.Key("tags"): t.List(t.String),
            t.Key("created"): notebook_activity_trafaret,
            t.Key("updated", optional=True): notebook_activity_trafaret,
            t.Key("last_viewed"): notebook_activity_trafaret,
            t.Key("settings"): notebook_settings_trafaret,
            t.Key("org_id", optional=True): t.String,
            t.Key("session", optional=True): t.Or(notebook_session_trafaret, t.Null),
            t.Key("use_case_id", optional=True): t.Or(t.String, t.Null),
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        permissions: List[str],
        tags: List[str],
        created: Dict[str, Any],
        last_viewed: Dict[str, Any],
        settings: Dict[str, bool],
        updated: Optional[Dict[str, Any]] = None,
        org_id: Optional[str] = None,
        description: Optional[str] = None,
        session: Optional[Dict[str, str]] = None,
        use_case_id: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.permissions = [NotebookPermissions[permission] for permission in permissions]
        self.tags = tags
        self.created = NotebookActivity.from_server_data(created)
        self.updated = updated if not updated else NotebookActivity.from_server_data(updated)
        self.last_viewed = (
            last_viewed if not last_viewed else NotebookActivity.from_server_data(last_viewed)
        )
        self.settings = NotebookSettings.from_server_data(settings)
        self.org_id = org_id
        self.session = NotebookSession.from_server_data(session) if session else session
        self.use_case_id = use_case_id

    @classmethod
    def get(cls, notebook_id: str) -> Notebook:
        """
        Retrieve a single notebook

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook you want to retrieve.

        Returns
        -------
        notebook : Notebook
            The requested notebook.
        """
        url = f"{cls._client.domain}/{cls._path}{notebook_id}/"
        r_data = cls._client.get(url)
        return Notebook.from_server_data(r_data.json())

    @classmethod
    def list(
        cls,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        order_by: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owners: Optional[List[str]] = None,
        query: Optional[str] = None,
        use_cases: Optional[UseCaseLike] = None,
    ) -> List[Notebook]:
        """
        List all Notebooks available to the user.

        Parameters
        ----------
        created_before : Optional[str]
            List Notebooks created before a certain date. Optional.
        created_after : Optional[str]
            List Notebooks created after a certain date. Optional.
        order_by : Optional[str]
            Property to sort returned Notebooks. Optional.
            Supported properties are "name", "created", "updated", "tags", and "lastViewed".
            Prefix the attribute name with a dash to sort in descending order,
            e.g. order_by='-created'.
            By default, the order_by parameter is None.
        tags : Optional[List[str]]
            A list of tags that returned Notebooks should be associated with. Optional.
        owners : Optional[List[str]]
            A list of user IDs used to filter returned Notebooks.
            The respective users share ownership of the Notebooks. Optional.
        query : Optional[str]
            A specific regex query to use when filtering Notebooks. Optional.
        use_cases : Optional[UseCase or List[UseCase] or str or List[str]]
            Filters returned Notebooks by a specific Use Case or Cases. Accepts either the entity or the ID. Optional.
        Returns
        -------
        notebooks : List[Notebook]
            A list of Notebooks available to the user.
        """
        params = {
            "created_before": created_before,
            "created_after": created_after,
            "order_by": order_by,
            "tags": tags,
            "owners": owners,
            "query": query,
        }
        params = resolve_use_cases(use_cases=use_cases, params=params, use_case_key="use_case_id")
        url = f"{cls._client.domain}/{cls._path}"
        r_data = unpaginate(url, params, cls._client)
        return [Notebook.from_server_data(data) for data in r_data]
