import json
from typing import Any, Dict, Literal, Optional
from typing import List as LList

from annotated_types import Annotated, Ge
from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel
from wandb_gql import gql

import wandb


class WorkspaceAPIBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
    

class WorkspaceView(WorkspaceAPIBaseModel):
    entity: str
    project: str
    display_name: str
    name: str
    id: str
    viewspec: WorkspaceViewSpec


class WorkspaceViewSpec(WorkspaceAPIBaseModel):
    section: WorkspaceViewSpecSection # this gives us workspace settings
    viz_expanded: bool = False
    library_expanded: bool = True
    # do we really need the ref?
    ref: Ref = Field(default_factory=Ref)


# maps to Config type in section.ts 
class WorkspaceViewSpecSection(WorkspaceAPIBaseModel):
    # omit type
    name: Optional[str]
    open_run_set: Optional[int]
    open_viz: Optional[bool]
    
    # openRunSet
    # hideRunSets
    run_sets: LList[Runset] = Field(default_factory=lambda: [Runset()])
    settings: Settings = Field(default_factory=Settings)

    # this is intentionally dict because it has arbitrary keys (the run ids)
    custom_run_colors: dict
    
    # panels
    
    panel_bank_config: PanelBankConfig 
    panel_bank_section_config: PanelBankSectionConfig


    # remove
    ref: Ref = Field(default_factory=Ref)


class PanelBankConfig(WorkspaceAPIBaseModel):
    state: int = 0
    # this gives us the workspace settings as well
    settings: PanelBankConfigSettings = Field(default_factory=PanelBankConfigSettings)
    sections: LList[PanelBankSectionConfig] = Field(
        default_factory=lambda: [PanelBankSectionConfig()]
    )
    # todo - remove
    ref: Optional[Ref] = None

    # Run keys are arbitrarily added here, so add some type checking for safety
    # All run keys have the shape (key:str, value:colour)
    @root_validator(pre=True)
    def check_arbitrary_keys(cls, values):  # noqa: N805
        fixed_keys = cls.__annotations__.keys()
        for k, v in values.items():
            if k not in fixed_keys and not isinstance(v, str):
                raise ValueError(f"Arbitrary key '{k}' must be of type 'str'")
        return values


class PanelBankConfigSettings(WorkspaceAPIBaseModel):
    # What's not included: 
    # defaultMoveToSectionName
    # highlightedCompanionRunOnly
    # showEmptySections
    # searchSectionsOpen
    auto_organize_prefix: int = 2
    show_empty_sections: bool = False
    sort_alphabetically: bool = False
    search_query: Optional[str] = None
    search_history: Optional[LList[Dict[Literal["query"], str]]] = None
    auto_expand_search_results: Optional[bool] = None

# Maps to PanelBankSectionConfig in types.ts
# Settings for 
class PanelBankSectionConfig(WorkspaceAPIBaseModel):
    # __id__ 
    flow_config: FlowConfig = Field(default_factory=FlowConfig)
    is_open: bool = False
    local_panel_settings: Settings = Field(default_factory=Settings)
    name: str = "Hidden Panels"
    panels: LList["PanelTypes"] = Field(default_factory=list)
    sorted: int = 0
    pinned: bool = False
    type: str = "flow"
    # internal so can remove
    ref: Optional[Ref] = None


# Defaults coming from getDefaultPanelSectionConfig() and matches PanelBankFlowSectionConfig/types.ts
class FlowConfig(WorkspaceAPIBaseModel):
    snap_to_columns: bool = True
    columns_per_page: int = 3
    rows_per_page: int = 2
    gutter_width: int = 16
    box_width: int = 460
    box_height: int = 300


# This maps to the DEFAULT EMPTY configs in panelsettings.ts and 
class Settings(WorkspaceAPIBaseModel):
    ignore_outliers: bool = False
    # local active ones are ignored
    smoothing_type: str = "exponential"
    smoothing_weight: int = 0
    # This was missing
    useRunsTableGroupingInPanels: bool = False
    
    x_axis: str = "_step"
    x_axis_min: Optional[Annotated[float, Ge(0)]] = None
    x_axis_max: Optional[Annotated[float, Ge(0)]] = None
    
    color_run_names: Optional[bool] = None
    max_runs: Optional[int] = None
    point_visualization_method: Optional[
        Literal["bucketing-gorilla", "sampling"]
    ] = None
    suppress_legends: Optional[bool] = None
    show_min_max_on_hover: Optional[bool] = None
    tooltip_number_of_runs: Optional[Literal["single", "default", "all_runs"]] = None
    
    x_axis_active: bool = False
    smoothing_active: bool = False
    
    # can probably remove - this is internal?
    # ref: Optional[Ref] = None




