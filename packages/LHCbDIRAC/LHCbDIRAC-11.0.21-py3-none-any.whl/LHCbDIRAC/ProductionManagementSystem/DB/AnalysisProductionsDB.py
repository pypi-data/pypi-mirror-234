###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Database class for storing information about Analysis Productions

For more information on the meaning of the various objects see :py:mod:`.AnalysisProductionsClient`.

Tables are defined using SQLAlchemy and imported from :py:mod:`.AnalysisProductionsObjects`.
Example usage of this class can be found in `Test_AnalysisProductionsDB.py`.
"""
import functools
import datetime
from collections import defaultdict
from copy import deepcopy
from contextlib import contextmanager

from sqlalchemy import create_engine, delete, func, insert, or_, tuple_, select, case, JSON, cast, Integer
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import Session

from DIRAC.ConfigurationSystem.Client.Utilities import getDBParameters
from DIRAC.Core.Base.DIRACDB import DIRACDB
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise

from LHCbDIRAC.ProductionManagementSystem.DB.AnalysisProductionsObjects import (
    Base,
    AnalysisSample as AP,
    AutoTag,
    Tag,
    Request,
    AnalysisOwner,
)
from LHCbDIRAC.ProductionManagementSystem.DB.extra_func import json_group_array, json_group_object


def inject_session(func):
    """Decorator to inject the session into a class method

    Decorator to start a SQLAlchemy Session and inject it in the wrapped function
    as a keyword argument.
    """

    @functools.wraps(func)
    def new_func(self, *args, **kwargs):
        if "session" in kwargs:
            raise NotImplementedError("session cannot be passed through the inject_session decorator")
        with self.session as session:
            return func(self, *args, **kwargs, session=session)

    return new_func


class AnalysisProductionsDB(DIRACDB):
    __engineCache = {}

    def __init__(self, *, url=None, parentLogger=None):
        self.fullname = self.__class__.__name__
        super().__init__(parentLogger=parentLogger)
        if url is None:
            param = returnValueOrRaise(getDBParameters("ProductionManagement/AnalysisProductionsDB"))
            url = f"mysql://{param['User']}:{param['Password']}@{param['Host']}:{param['Port']}/{param['DBName']}"
        self.setURL(url)

    def setURL(self, url):
        if url not in self.__engineCache or ":memory:" in url:
            engine = create_engine(
                url, pool_recycle=3600, echo_pool=True, echo=self.log.getLevel() == "DEBUG", future=True
            )
            Base.metadata.create_all(engine)
            self.__engineCache[url] = engine
        self.engine = self.__engineCache[url]

    @property
    @contextmanager
    def session(self):
        with Session(self.engine, future=True) as session, session.begin():
            yield session

    @inject_session
    def listAnalyses(self, *, at_time=None, session: Session):
        query = _filterForTime(session.query(AP.wg, AP.analysis).distinct(), AP, at_time)
        result = defaultdict(list)
        for wg, analysis in query:
            result[wg].append(analysis)
        return dict(result)

    @inject_session
    def listAnalyses2(self, *, at_time=None, session: Session):
        # Select the owners of the analyses
        query = select(AnalysisOwner.wg, AnalysisOwner.analysis, AnalysisOwner.username).distinct()
        owners = defaultdict(lambda: defaultdict(list))
        for wg, analysis, username in session.execute(query).all():
            owners[wg][analysis].append(username)

        # Select the analyses and build the list of results
        query = select(
            AP.wg,
            AP.analysis,
            # Add a column n_{STATE_NAME} containing the number of analyses in each possible state
            *(
                # MySQL returns a decimal type from sum() so we need to cast it to an integer
                cast(func.sum(case((AP.state == state, 1), else_=0)), Integer).label(  # pylint: disable=not-callable
                    f"n_{state}"
                )
                for state in AP.VALID_STATES
            ),
            func.count().label("n_total"),  # pylint: disable=not-callable
        )
        query = query.group_by(AP.wg, AP.analysis)
        query = _filterForTime(query, AP, at_time)
        return [dict(row._mapping) | {"owners": owners[row.wg][row.analysis]} for row in session.execute(query).all()]

    @inject_session
    def listRequests(self, *, session: Session):
        analyses = select(
            AP.request_id,
            AP.name,
            AP.version,
            json_group_array(func.json_array(AP.wg, AP.analysis)).label("analyses"),
        )
        analyses = analyses.group_by(AP.request_id, AP.name, AP.version)
        analyses = _filterForTime(analyses, AP, at_time=None)
        analyses = analyses.subquery(name="requests")

        autotags = select(
            Request.request_id,
            # Can't use AGG_FUNC.filter as it's not supported by mysql
            case(
                (
                    func.sum(AutoTag.name.is_not(None)) == 0,  # pylint: disable=not-callable
                    func.json_object(type_=JSON),  # pylint: disable=not-callable
                ),
                else_=json_group_object(AutoTag.name, AutoTag.value),
            ).label("autotags"),
        )
        autotags = autotags.join(AutoTag, Request.request_id == AutoTag.request_id, isouter=True)
        autotags = autotags.group_by(Request.request_id)
        autotags = autotags.subquery(name="autotags")

        tags = select(
            AP.request_id,
            # Can't use AGG_FUNC.filter as it's not supported by mysql
            case(
                (
                    func.sum(Tag.name.is_not(None)) == 0,  # pylint: disable=not-callable
                    func.json_array(type_=JSON),  # pylint: disable=not-callable
                ),
                else_=json_group_array(func.json_array(Tag.name, Tag.value)),
            ).label("tags"),
        ).distinct()
        tags = tags.join(Tag, AP.sample_id == Tag.sample_id, isouter=True)
        tags = tags.group_by(AP.request_id)
        tags = tags.subquery(name="tags")

        query = select(analyses, autotags.c.autotags, tags.c.tags)
        query = query.join(autotags, analyses.c.request_id == autotags.c.request_id, isouter=True)
        query = query.join(tags, analyses.c.request_id == tags.c.request_id, isouter=True)
        return [dict(row._mapping) for row in session.execute(query).all()]

    @inject_session
    def getOwners(self, *, wg=None, analysis=None, session: Session):
        query = select(AnalysisOwner.username)
        query = query.where(AnalysisOwner.wg == wg)
        query = query.where(AnalysisOwner.analysis == analysis)
        return session.execute(query).scalars().all()

    @inject_session
    def setOwners(self, *, wg=None, analysis=None, owners=None, session: Session):
        query = select(AnalysisOwner.username)
        query = query.where(AnalysisOwner.wg == wg)
        query = query.where(AnalysisOwner.analysis == analysis)
        existing_owners = session.execute(query).scalars().all()

        new_owners = [
            {"wg": wg, "analysis": analysis, "username": owner} for owner in owners if owner not in existing_owners
        ]
        if new_owners:
            session.execute(insert(AnalysisOwner).values(new_owners))

        query = delete(AnalysisOwner)
        query = query.where(AnalysisOwner.wg == wg)
        query = query.where(AnalysisOwner.analysis == analysis)
        query = query.where(~AnalysisOwner.username.in_(owners))
        session.execute(query)

    @inject_session
    def getProductions(
        self, *, wg=None, analysis=None, version=None, name=None, state=None, at_time=None, session: Session
    ):
        query = select(
            AP.wg,
            AP.analysis,
            AP.sample_id,
            AP.validity_start,
            AP.validity_end,
            AP.name,
            AP.version,
            AP.request_id,
            AP.state,
            AP.last_state_update,
            AP.extra_info["transformations"].label("transformations"),
            AP.progress,
            AP.extra_info["jira_task"].label("jira_task"),
            AP.extra_info["merge_request"].label("merge_request"),
        )
        query = query.filter(*_buildCondition(wg, analysis, name, version))
        if state is not None:
            query = query.filter(AP.state == state)
        query = _filterForTime(query, AP, at_time)

        results = []
        for row in session.execute(query).all():
            result = {
                "name": row.name,
                "version": row.version,
                "request_id": row.request_id,
                "state": row.state,
                "last_state_update": row.last_state_update,
                "transformations": row.transformations,
            }
            if row.progress is not None:
                result["progress"] = row.progress
            if row.jira_task is not None:
                result["jira_task"] = row.jira_task
            if row.merge_request is not None:
                result["merge_request"] = row.merge_request
            result.update(
                {
                    "wg": row.wg,
                    "analysis": row.analysis,
                    "sample_id": row.sample_id,
                    # TODO: Remove
                    "owners": [],
                    "validity_start": row.validity_start,
                    "validity_end": row.validity_end,
                }
            )
            results.append(result)
        return results

    @inject_session
    def getArchivedRequests(self, *, state=None, session: Session):
        sq = (
            session.query(AP.request_id)
            .filter(or_(AP.validity_end.is_(None), datetime.datetime.now() < AP.validity_end))
            .distinct()
            .subquery()
        )
        query = session.query(Request).filter(~Request.request_id.in_(select(sq)))
        if state is not None:
            query = query.filter(AP.state == state)
        return [result.toDict() for result in query]

    @inject_session
    def getTags(self, wg, analysis, *, at_time=None, session: Session):
        return _getTags(session, wg=wg, analysis=analysis, at_time=at_time)

    @inject_session
    def getKnownAutoTags(self, *, session) -> set:
        return _getKnownAutoTags(session)

    @inject_session
    def registerTransformations(self, transforms: dict[int, list[dict]], *, session: Session):
        if not transforms:
            raise ValueError("No transforms passed")
        transforms = deepcopy(transforms)
        for request in session.query(Request).filter(Request.request_id.in_(transforms)):
            knownTransforms = {t["id"] for t in request.extra_info["transformations"]}
            for transform in transforms.pop(request.request_id):
                if transform["id"] in knownTransforms:
                    raise ValueError(f"Transformation is already known {transform['id']}")
                # TODO: Validate the transform object
                request.extra_info["transformations"].append(transform)
                # By default SQLAlchemy doesn't detect changes in JSON columns when using the ORM
                # Ideally this should be fixed in the database definition but flagging manually is
                # good enough for now
                flag_modified(request, "extra_info")
        if transforms:
            raise ValueError(f"Did not find requests for IDs: {list(transforms)}")

    @inject_session
    def deregisterTransformations(self, tIDs: dict[int, list[int]], *, session: Session):
        """See :meth:`~.AnalysisProductionsClient.registerTransformations`"""
        if not tIDs:
            raise ValueError("No transform IDs passed")
        tIDs = deepcopy(tIDs)
        query = session.query(Request).filter(Request.request_id.in_(tIDs))
        for request in query:
            for tID in tIDs.pop(request.request_id):
                for i, transform in enumerate(request.extra_info["transformations"]):
                    if transform["id"] == tID:
                        request.extra_info["transformations"].pop(i)
                        break
                else:
                    raise ValueError(f"Transformation {tID} is not known")
                flag_modified(request, "extra_info")
        if tIDs:
            raise ValueError(f"Did not find requests for IDs: {list(tIDs)}")

    def registerRequests(self, requests: list[dict]):
        request_ids = {r["request_id"] for r in requests}
        with self.session as session:
            known_ids = {i for i, in session.query(AP.request_id).filter(AP.request_id.in_(request_ids))}
            if known_ids:
                raise ValueError(f"Already registered requests: {known_ids!r}")

            for r in requests:
                self.log.info(
                    "Registering Analysis Production request",
                    f"{r['wg']} {r['analysis']} {r['version']} {r['request_id']} {r['name']}",
                )
                sample = AP(
                    request_id=r["request_id"],
                    name=r["name"],
                    version=r["version"],
                    wg=r["wg"],
                    analysis=r["analysis"],
                    validity_start=r["validity_start"],
                    extra_info=r["extra_info"],
                    auto_tags=[AutoTag(name=x["name"], value=x["value"]) for x in r["auto_tags"]],
                )
                # TODO: Remove
                # sample.owners = [User(username=x["username"]) for x in r["owners"]]
                session.add(sample)

        with self.session as session:
            query = session.query(AP)
            query = query.filter(AP.request_id.in_(request_ids))
            return [result.toDict() for result in query]

    @inject_session
    def addRequestsToAnalysis(self, wg: str, analysis: str, request_ids: list[id], *, session: Session):
        self.log.info("Adding samples to analysis", f"({wg}/{analysis}) {','.join(map(str, request_ids))}")

        query = select(AP.request_id, AP.sample_id).filter(
            AP.wg == wg,
            AP.analysis == analysis,
            AP.request_id.in_(request_ids),
            AP.validity_end.is_(None),
        )
        if already_existing := session.execute(query).all():
            raise ValueError(
                f"Some requests are already registered for {wg}/{analysis} request_id->sample_id mapping is "
                f"{ {request_id: sample_id for request_id, sample_id in already_existing} }"
            )

        query = insert(AP).values(
            [{"wg": wg, "analysis": analysis, "request_id": request_id} for request_id in request_ids]
        )
        session.execute(query)

    @inject_session
    def archiveSamples(self, sample_ids: list[int], *, session: Session):
        self.log.info("Archiving Analysis Productions", ",".join(map(str, sample_ids)))
        query = session.query(AP.sample_id)
        query = query.filter(AP.sample_id.in_(sample_ids))
        known_sample_ids = {i for i, in query}
        if len(known_sample_ids) != len(sample_ids):
            raise ValueError(f"Unknown sample IDs passed {known_sample_ids - set(sample_ids)!r}")
        query = query.filter(AP.validity_end.is_(None))
        known_sample_ids = {i for i, in query}
        if len(known_sample_ids) != len(sample_ids):
            raise ValueError(f"Some samples have already been archived {known_sample_ids - set(sample_ids)!r}")
        query = session.query(AP).filter(AP.sample_id.in_(sample_ids))
        query.update({"validity_end": func.now()})  # pylint: disable=not-callable

    @inject_session
    def archiveSamplesAtSpecificTime(self, sample_ids: list[int], archive_time: datetime.datetime, *, session: Session):
        self.log.info(f"Archiving Analysis Productions at {archive_time}", ",".join(map(str, sample_ids)))
        query = session.query(AP.sample_id)
        query = query.filter(AP.sample_id.in_(sample_ids))
        known_sample_ids = {i for i, in query}
        if len(known_sample_ids) != len(sample_ids):
            raise ValueError(f"Unknown sample IDs passed {known_sample_ids - set(sample_ids)!r}")
        query = query.filter(AP.validity_end.is_(None))
        known_sample_ids = {i for i, in query}
        if len(known_sample_ids) != len(sample_ids):
            raise ValueError(f"Some samples have already been archived {known_sample_ids - set(sample_ids)!r}")
        query = session.query(AP).filter(AP.sample_id.in_(sample_ids))

        query.update({"validity_end": archive_time})  # pylint: disable=not-callable

    @inject_session
    def setState(self, newState: dict[str, dict], *, session: Session):
        for request_id, updateDict in newState.items():
            query = session.query(Request).filter(Request.request_id == request_id)
            rowsUpdated = query.update({getattr(Request, k): v for k, v in updateDict.items()})
            if rowsUpdated != 1:
                raise ValueError(
                    f"Failed to update Request({request_id}) with {updateDict!r}, {rowsUpdated} matching rows found"
                )

    @inject_session
    def setTags(self, oldTags: dict[int, dict[str, str]], newTags: dict[int, dict[str, str]], *, session: Session):
        if set(oldTags) != set(newTags):
            raise ValueError("oldTags and newTags must contain the same keys")
        # Tags should always be lowercase in the database
        oldTags = {int(i): {str(k).lower(): str(v).lower() for k, v in x.items()} for i, x in oldTags.items()}
        newLengths = {int(i): len(x) for i, x in newTags.items()}
        newTags = {int(i): {str(k).lower(): str(v).lower() for k, v in x.items()} for i, x in newTags.items()}
        if newLengths != {i: len(x) for i, x in newTags.items()}:
            raise ValueError("newTags contains duplicate keys when converted to lowercase")

        # Compute what needs to be changed, while also ensuring the auto tags aren't touched
        knownAutoTags = _getKnownAutoTags(session)
        toRemove = []
        toAdd = []
        for sample_id, old in oldTags.items():
            new = newTags[sample_id]
            removed_tags = set(old) - set(new)
            modified_tags = {k: new[k] for k in set(new) & set(old) if new[k] != old[k]}
            added_tags = {k: new[k] for k in set(new) - set(old)}
            # Ensure that the automatic tags aren't being modifed
            if modifiedAutoTags := {*removed_tags, *modified_tags, *added_tags} & knownAutoTags:
                raise ValueError(f"Cannot modify AutoTags {modifiedAutoTags}")
            # Tags are modified by being removed and re-added allow for time-travel
            toRemove += [(sample_id, k) for k in {*removed_tags, *modified_tags}]
            toAdd += [(sample_id, k, v) for k, v in {**added_tags, **modified_tags}.items()]

        latestOldTags = _getTags(session, sample_ids=oldTags)
        if oldTags != latestOldTags:
            raise ValueError("oldTags is out of date")

        # Remove the old tags
        query = _filterForTime(session.query(Tag), Tag, at_time=None)
        query = query.filter(tuple_(Tag.sample_id, Tag.name).in_(toRemove))
        query.update({"validity_end": func.now()})  # pylint: disable=not-callable
        # Add the new tag values
        for sample_id, name, value in toAdd:
            session.add(Tag(sample_id=sample_id, name=name, value=value))


def _getKnownAutoTags(session: Session):
    return {name for name, in session.query(AutoTag.name).distinct()}


def _getTags(session, *, wg=None, analysis=None, at_time=None, sample_ids=None):
    results = defaultdict(dict)
    # Get the automatic tags
    query = session.query(AP.sample_id, AutoTag.name, AutoTag.value)
    query = query.filter(AP.request_id == AutoTag.request_id)
    if sample_ids:
        query = query.filter(AP.sample_id.in_(sample_ids))
    query = query.filter(*_buildCondition(wg, analysis))
    query = _filterForTime(query, AP, at_time)
    for sampleID, name, value in query:
        results[sampleID][name] = value
    # Get the manual tags
    query = session.query(AP.sample_id, Tag.name, Tag.value)
    query = query.filter(AP.sample_id == Tag.sample_id)
    if sample_ids:
        query = query.filter(AP.sample_id.in_(sample_ids))
    if wg is not None:
        query = query.filter(*_buildCondition(wg, analysis))
    query = _filterForTime(query, AP, at_time)
    query = _filterForTime(query, Tag, at_time)
    for sampleID, name, value in query:
        results[sampleID][name] = value
    return dict(results)


def _filterForTime(query, obj, at_time):
    if at_time is None:
        return query.filter(obj.validity_end.is_(None))
    else:
        return query.filter(
            obj.validity_start <= at_time,
            or_(obj.validity_end.is_(None), at_time < obj.validity_end),
        )


def _buildCondition(wg, analysis=None, name=None, version=None):
    """Build a SQLAlchemy query for the AnalysisProductions table"""
    if wg is not None:
        yield func.lower(AP.wg) == func.lower(wg)
    if analysis is not None:
        yield func.lower(AP.analysis) == func.lower(analysis)
    if name is not None:
        yield func.lower(AP.name) == func.lower(name)
    if version is not None:
        yield AP.version == version
