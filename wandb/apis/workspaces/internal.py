import json
from typing import Any, Dict, Literal, Optional
from typing import List as LList

from annotated_types import Annotated, Ge
from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel
from wandb_gql import gql

import wandb

# these internal objects should be factored out into a separate module as a
# shared dependency between Workspaces and Reports API
from wandb.apis.reports.v2.internal import *  # noqa: F403

from internal_types import *  # noqa: F403


def upsert_view2(view: WorkspaceView, clone: bool = False) -> Dict[str, Any]:
    query = gql(
        """
        mutation UpsertView2($id: ID, $entityName: String, $projectName: String, $type: String, $name: String, $displayName: String, $description: String, $spec: String, $parentId: ID, $locked: Boolean, $previewUrl: String, $coverUrl: String, $showcasedAt: DateTime, $createdUsing: ViewSource) {
        upsertView(
            input: {id: $id, entityName: $entityName, projectName: $projectName, name: $name, displayName: $displayName, description: $description, type: $type, spec: $spec, parentId: $parentId, locked: $locked, previewUrl: $previewUrl, coverUrl: $coverUrl, showcasedAt: $showcasedAt, createdUsing: $createdUsing}
        ) {
            view {
            id
            ...ViewFragmentMetadata2
            __typename
            }
            inserted
            __typename
        }
        }

        fragment ViewFragmentMetadata2 on View {
        id
        name
        displayName
        type
        description
        user {
            id
            username
            photoUrl
            admin
            name
            __typename
        }
        updatedBy {
            id
            name
            username
            __typename
        }
        entityName
        project {
            id
            name
            entityName
            readOnly
            __typename
        }
        previewUrl
        coverUrl
        updatedAt
        createdAt
        starCount
        starred
        parentId
        locked
        viewCount
        showcasedAt
        alertSubscription {
            id
            __typename
        }
        accessTokens {
            id
            token
            view {
            id
            __typename
            }
            type
            emails
            createdBy {
            id
            username
            email
            name
            __typename
            }
            createdAt
            lastAccessedAt
            revokedAt
            projects {
            id
            name
            entityName
            __typename
            }
            __typename
        }
        __typename
        }
        """
    )

    api = wandb.Api()

    if clone or not (name := view.name):
        random_id = wandb.util.generate_id(11)
        name = _workspaceify(random_id)

    spec = view.viewspec.model_dump(by_alias=True, exclude_none=True)

    # hack: We're re-using Report API objects. In the Report API, the value here
    # is expected to be None, but for Workspaces it's expected to be []
    filters = spec["section"]["runSets"][0]["filters"]
    if "filters" in filters and len(filters["filters"]) > 0:
        filters["filters"][0]["filters"] = []

    variables = {
        "entityName": view.entity,
        "projectName": view.project,
        "name": name,
        "displayName": view.display_name,
        "type": "project-view",
        "description": "",
        "spec": json.dumps(spec),
        "locked": False,
    }

    # Adding the view Id breaks stuff for reasons I don't understand
    # if view.id:
    #     variables["id"] = view.id

    response = api.client.execute(query, variables)

    return response


def _get_view(entity: str, project: str, view_name: str) -> Dict[str, Any]:
    # Use this query because it let you use view_name instead of id
    query = gql(
        """
        query View($entityName: String, $name: String, $viewType: String = "runs", $userName: String, $viewName: String) {
            project(name: $name, entityName: $entityName) {
                allViews(viewType: $viewType, viewName: $viewName, userName: $userName) {
                    edges {
                        node {
                            id
                            displayName
                            spec
                        }
                    }
                }
            }
        }
        """
    )

    api = wandb.Api()

    response = api.client.execute(
        query,
        {
            "viewType": "project-view",
            "entityName": entity,
            "projectName": project,
            "name": project,
            "viewName": _workspaceify(view_name),
        },
    )

    edges = response.get("project", {}).get("allViews", {}).get("edges", [])

    try:
        view = edges[0]["node"]
    except IndexError:
        raise ValueError(f"Workspace `{view_name}` not found in project `{project}`")
    else:
        return view


def get_view(entity: str, project: str, view_name: str) -> View:
    view_dict = _get_view(entity, project, view_name)

    spec = view_dict["spec"]
    display_name = view_dict["displayName"]
    id = view_dict["id"]
    parsed_spec = WorkspaceViewspec.model_validate_json(spec)

    return View(
        entity=entity,
        project=project,
        display_name=display_name,
        name=view_name,
        id=id,
        viewspec=parsed_spec,
    )


def _workspaceify(name: str) -> str:
    return f"nw-{name}-v"


def _unworkspaceify(name: str) -> str:
    return name.replace("nw-", "").replace("-v", "")
