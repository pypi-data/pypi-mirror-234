#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Checklist """

# standard python imports

from dataclasses import asdict, dataclass
from typing import Any

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger

logger = create_logger()


@dataclass
class Checklist:
    """RegScale Checklist

    :return: RegScale Checklist
    """

    # Required
    status: str
    assetId: int
    tool: str
    baseline: str
    id: int = 0
    isPublic: bool = True
    uuid: str = None
    vulnerabilityId: str = None
    ruleId: str = None
    cci: str = None
    check: str = None
    results: str = None
    comments: str = None
    createdById: str = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    datePerformed: str = None

    def __hash__(self):
        """
        Enable object to be hashable
        :return: Hashed Checklist
        """
        return hash(
            (
                self.tool,
                self.vulnerabilityId,
                self.ruleId,
                self.baseline,
                self.check,
                self.results,
                self.comments,
                self.assetId,
            )
        )

    def __eq__(self, other) -> "Checklist":
        """
        Compare Checklists
        :param other:
        :return: Updated Checklist
        :rtype: Checklist
        """
        return (
            # Unique values
            # Tool, VulnerabilityId, RuleId, Baseline, [Check], Results, Comments, Status, AssetId,
            # TenantsId, CCI, Version
            self.tool == other.tool
            and self.vulnerabilityId == other.vulnerabilityId
            and self.ruleId == other.ruleId
            and self.baseline == other.baseline
            and self.check == other.check
            and self.results == other.results
            and self.comments == other.comments
            and self.assetId == other.assetId
        )

    @staticmethod
    def insert_or_update_checklist(
        app: Application,
        new_checklist: "Checklist",
        existing_checklists: list["Checklist"],
    ) -> int:
        """Insert or update a checklist
        :param app: RegScale Application instance
        :param new_checklist: New checklist to insert or update
        :param existing_checklists: Existing checklists to compare against
        :return: int of the checklist id
        """
        delete_keys = [
            "asset",
            "uuid",
            "lastUpdatedById",
            "dateLastUpdated",
            "createdById",
            "dateCreated",
        ]
        for dat in existing_checklists:
            for key in delete_keys:
                if key in dat:
                    del dat[key]
        api = Api(app)
        matching_checklists = [
            Checklist.from_dict(chk)
            for chk in existing_checklists
            if Checklist.from_dict(chk) == new_checklist
        ]
        if matching_checklists:
            logger.info("Updating checklist %s", new_checklist.baseline)
            new_checklist.id = matching_checklists[0].id
            res = api.put(
                url=app.config["domain"] + f"/api/securitychecklist/{new_checklist.id}",
                json=asdict(new_checklist),
            )
        else:
            logger.info("Inserting checklist %s", new_checklist.baseline)
            res = api.post(
                url=app.config["domain"] + "/api/securitychecklist",
                json=asdict(new_checklist),
            )
        if res.status_code != 200:
            logger.warning(
                "Unable to insert or update checklist %s", new_checklist.baseline
            )
            return None
        return res.json()["id"]

    @staticmethod
    def get_checklists(
        parent_id: int, parent_module: str = "components"
    ) -> list["Checklist"]:
        """Return all checklists for a given component
        :param parent_id: RegScale parent id
        :param component_id: RegScale component id
        :return: _description_
        """
        app = Application()
        api = Api(app)
        logger.debug("Fetching all checklists for %s %s", parent_module, parent_id)
        checklists = []
        query = """
                           query {
                securityChecklists(skip: 0, take: 50,where:{asset: {parentId: {eq: parent_id_placeholder}, parentModule: {eq: "parent_module_placeholder"}}}) {
                    items {
                            id
                            asset {
                              id
                              name
                              parentId
                              parentModule
                            }
                            status
                            tool
                            datePerformed
                            vulnerabilityId
                            ruleId
                            cci
                            check
                            results
                            baseline
                            comments
                    }
                    totalCount
                    pageInfo {
                        hasNextPage
                    }
                }
            }
            """.replace(
            "parent_id_placeholder", str(parent_id)
        ).replace(
            "parent_module_placeholder", parent_module
        )
        data = api.graph(query)
        if "securityChecklists" in data and "items" in data["securityChecklists"]:
            for item in data["securityChecklists"]["items"]:
                item["assetId"] = item["asset"]["id"]
                checklists.append(item)
        return checklists

    @staticmethod
    def from_dict(obj: Any) -> "Checklist":
        _id = int(obj.get("id", 0))
        _isPublic = bool(obj.get("isPublic"))
        _uuid = str(obj.get("uuid")) if obj.get("uuid") else None
        _tool = str(obj.get("tool"))
        _vulnerabilityId = str(obj.get("vulnerabilityId"))
        _ruleId = str(obj.get("ruleId"))
        _cci = str(obj.get("cci")) if obj.get("cci") else None
        _baseline = str(obj.get("baseline"))
        _check = str(obj.get("check"))
        _results = str(obj.get("results"))
        _comments = str(obj.get("comments"))
        _status = str(obj.get("status"))
        _assetId = int(obj.get("assetId", 0))
        _createdById = str(obj.get("createdById")) if obj.get("createdById") else None
        _dateCreated = str(obj.get("dateCreated")) if obj.get("dateCreated") else None
        _lastUpdatedById = (
            str(obj.get("lastUpdatedById")) if obj.get("lastUpdatedById") else None
        )
        _dateLastUpdated = (
            str(obj.get("dateLastUpdated")) if obj.get("dateLastUpdated") else None
        )
        _datePerformed = (
            str(obj.get("datePerformed")) if obj.get("datePerformed") else None
        )
        return Checklist(
            _status,
            _assetId,
            _tool,
            _baseline,
            _id,
            _isPublic,
            _uuid,
            _vulnerabilityId,
            _ruleId,
            _cci,
            _check,
            _results,
            _comments,
            _createdById,
            _dateCreated,
            _lastUpdatedById,
            _dateLastUpdated,
            _datePerformed,
        )
