###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from enum import Enum
from typing import Any, Literal, Any

from pydantic import BaseModel as _BaseModel
from pydantic import Extra, Field, constr, PositiveInt, conlist, validator, confloat

from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise

FILETYPE_PATTERN = r"[A-Z0-9\.]+"


class ProductionStates(str, Enum):
    NEW = "New"
    ACTIVE = "Active"
    SUBMITTED = "Submitted"
    PPG_OK = "PPG OK"
    TECH_OK = "Tech OK"
    ACCEPTED = "Accepted"
    DONE = "Done"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"


class BaseModel(_BaseModel, extra=Extra.forbid):
    pass


class ProductionStep(BaseModel):
    id: PositiveInt | None = None
    name: str
    processing_pass: str

    class GaudirunOptions(BaseModel):
        command: conlist(str, min_items=1) | None = None
        files: list[str]
        format: str | None = None
        gaudi_extra_options: str | None = None
        processing_pass: str | None = None

    class LbExecOptions(BaseModel):
        entrypoint: str
        extra_options: dict[str, Any]
        extra_args: list[str] = []

    options: list[str] | GaudirunOptions | LbExecOptions  # TODO the list of str is for legacy compatibility
    options_format: str | None = None  # TODO This should be merged into options
    visible: bool
    multicore: bool = False
    ready: bool = True
    obsolete: bool = False

    class Application(BaseModel):
        name: str
        version: str
        nightly: str | None = None
        binary_tag: str | None = None

    application: Application

    class DataPackage(BaseModel):
        name: str
        version: str

    data_pkgs: list[DataPackage] = []

    class DBTags(BaseModel):
        DDDB: str | None = None
        CondDB: str | None = None
        DQTag: str | None = None

    dbtags: DBTags | None

    class FileType(BaseModel):
        type: constr(regex=FILETYPE_PATTERN)
        visible: bool

    input: list[FileType]
    output: conlist(FileType, min_items=1)

    @validator("input", "output", pre=True)
    def filetype_default(cls, filetypes, values):  # pylint: disable=no-self-argument
        """Expand a list of file types into the explicit form.

        This is to allow for a convenient list of input types to be specified.
        For example::

          input:
            - type: ["STREAM1.DST", "STREAM2.MDST"]
              visible: true
            - type: STREAM3.DST
              visible: false

        becomes::

          input:
            - type: STREAM1.DST
              visible: true
            - type: STREAM2.MDST
              visible: true
            - type: STREAM3.MDST
              visible: false
        """
        cleaned_filetypes = []
        for filetype in filetypes:
            if isinstance(filetype["type"], list):
                cleaned_filetypes.extend({"type": t, "visible": filetype["visible"]} for t in filetype["type"])
            else:
                cleaned_filetypes.append(filetype)
        return cleaned_filetypes

    @validator("application", pre=True, always=True)
    def application_default(cls, application, values):  # pylint: disable=no-self-argument
        if isinstance(application, str):
            name, version = application.rsplit("/", 2)
            application = {"name": name, "version": version}
        return application

    @validator("data_pkgs", pre=True, always=True)
    def data_pkgs_default(cls, data_pkgs, values):  # pylint: disable=no-self-argument
        cleaned_data_pkgs = []
        for data_pkg in data_pkgs:
            if isinstance(data_pkg, str):
                name, version = data_pkg.rsplit(".", 2)
                cleaned_data_pkgs.append({"name": name, "version": version})
            else:
                cleaned_data_pkgs.append(data_pkg)
        return cleaned_data_pkgs


class ProductionBase(BaseModel):
    type: str
    id: PositiveInt | None
    author: str = Field(default_factory=lambda: returnValueOrRaise(getProxyInfo())["username"])
    priority: constr(regex=r"^[12][ab]$")
    name: str
    inform: list[constr(strip_whitespace=True, min_length=3, max_length=50)] = []
    # TODO: I'm inclined to hardcode the list of known working groups
    wg: str
    comment: str = ""
    state: ProductionStates = ProductionStates.NEW
    steps: conlist(ProductionStep, min_items=1)


class SimulationProduction(ProductionBase):
    type: Literal["Simulation"]
    mc_config_version: str
    sim_condition: str
    fast_simulation_type: constr(strip_whitespace=True, min_length=4, max_length=32) = "None"
    # TODO This should move to EventType
    retention_rate: confloat(gt=0, le=1) = 1
    override_processing_pass: str | None = None

    class EventType(BaseModel):
        id: constr(regex=r"[0-9]{8}")
        num_events: PositiveInt
        num_test_events: PositiveInt = 10

    event_types: conlist(EventType, min_items=1)


class DataProduction(ProductionBase):
    class InputDataset(BaseModel):
        class BookkeepingQuery(BaseModel):
            configName: str
            configVersion: str
            inFileType: str
            inProPass: str
            # TODO: Accept None and lists on these
            inDataQualityFlag: str = "OK"
            inProductionID: str = "ALL"
            inTCKs: str = "ALL"

        conditions_dict: BookkeepingQuery
        # TODO: Remove conditions_id field once this is deployed and LbAnalysisProductions is updated
        conditions_id: int | None = None
        conditions_description: str
        event_type: constr(regex=r"[0-9]{8}")

    input_dataset: InputDataset


def parse_obj(obj: Any) -> ProductionBase:
    if obj.get("type") == "Simulation":
        return SimulationProduction.parse_obj(obj)
    return DataProduction.parse_obj(obj)
