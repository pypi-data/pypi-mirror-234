# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request views module."""

from flask import Blueprint

from .api import create_request_events_bp, create_requests_bp
from .ui import create_ui_blueprint

blueprint = Blueprint("invenio-requests-ext", __name__)


@blueprint.record_once
def init(state):
    """Register the module's services and indexers to the central registries."""
    svc_reg = state.app.extensions["invenio-records-resources"].registry
    idx_reg = state.app.extensions["invenio-indexer"].registry
    requests_ext = state.app.extensions["invenio-requests"]
    requests_service = requests_ext.requests_service
    events_service = requests_ext.request_events_service

    svc_reg.register(requests_service)
    svc_reg.register(events_service)

    idx_reg.register(requests_service.indexer, indexer_id="requests")
    idx_reg.register(events_service.indexer, indexer_id="events")


__all__ = (
    "blueprint",
    "create_ui_blueprint",
    "create_requests_bp",
    "create_request_events_bp",
)
