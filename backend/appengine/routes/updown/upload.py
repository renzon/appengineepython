# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blob_app import blob_facade
from routes import updown
from routes.updown import ok
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


def index(_handler, _logged_user, files):
    blob_infos = _handler.get_uploads('files[]')
    save_blobs_cmd = blob_facade.save_blob_files_cmd(blob_infos, _logged_user)
    save_blobs_cmd()
    path = router.to_path(updown)
    return RedirectResponse(path)