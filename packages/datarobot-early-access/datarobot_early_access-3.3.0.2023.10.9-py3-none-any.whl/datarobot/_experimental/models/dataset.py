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
from typing import List, Optional, Type

from typing_extensions import TypedDict

from datarobot import Dataset as BaseDataset
from datarobot._experimental.models.recipes import Recipe
from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.credential import Credential
from datarobot.models.dataset import _remove_empty_params, TDataset
from datarobot.models.use_cases.utils import add_to_use_case
from datarobot.utils.waiters import wait_for_async_resolution


class MaterializationDestination(TypedDict):
    catalog: str
    schema: str
    # Table name to create and materialize the recipe to. This table should not already exist.
    table: str


class Dataset(BaseDataset):
    """Represents a Dataset returned from the api/v2/datasets/ endpoints with extra method to create from a Recipe."""

    @classmethod
    @add_to_use_case(allow_multiple=True)
    def create_from_recipe(
        cls: Type[TDataset],
        recipe: Recipe,
        name: Optional[str] = None,
        do_snapshot: Optional[bool] = None,
        persist_data_after_ingestion: Optional[bool] = None,
        categories: Optional[List[str]] = None,
        credential: Optional[Credential] = None,
        use_kerberos: Optional[bool] = None,
        materialization_destination: Optional[MaterializationDestination] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> TDataset:
        """
        A blocking call that creates a new Dataset from the recipe.
        Returns when the dataset has been successfully uploaded and processed.

        .. versionadded:: FUTURE

        Returns
        -------
        response: Dataset
            The Dataset created from the uploaded data
        """
        base_data = {
            "recipe_id": recipe.id,
            "name": name,
            "do_snapshot": do_snapshot,
            "persist_data_after_ingestion": persist_data_after_ingestion,
            "categories": categories,
            "use_kerberos": use_kerberos,
            "materialization_destination": materialization_destination,
        }
        data = _remove_empty_params(base_data)
        if credential is not None:
            data["credential_id"] = credential.credential_id

        upload_url = f"{cls._path}fromRecipe/"
        response = cls._client.post(upload_url, data=data)

        new_dataset_location = wait_for_async_resolution(
            cls._client, response.headers["Location"], max_wait
        )
        return cls.from_location(new_dataset_location)
