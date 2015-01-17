# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext.blobstore import blobstore
from blob_app import blob_facade

from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from routes.updown import upload, download
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(_logged_user):
    success_url = router.to_path(upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(success_url, gs_bucket_name=bucket)

    cmd = blob_facade.list_blob_files_cmd(_logged_user)
    blob_files = cmd()
    delete_path = router.to_path(delete)
    download_path = router.to_path(download)
    blob_file_form = blob_facade.blob_file_form()

    def localize_blob_file(blob_file):
        blob_file_dct = blob_file_form.fill_with_model(blob_file, 64)
        blob_file_dct['delete_path'] = router.to_path(delete_path, blob_file_dct['id'])
        blob_file_dct['download_path'] = router.to_path(download_path,
                                                        blob_file.blob_key,
                                                        blob_file_dct['filename'])
        return blob_file_dct

    localized_blob_files = [localize_blob_file(blob_file) for blob_file in blob_files]
    context = {'upload_url': url,
               'blob_files': localized_blob_files}
    return TemplateResponse(context, 'updown/home.html')


def delete(blob_file_id):
    blob_facade.delete_blob_file_cmd(blob_file_id).execute()
    return RedirectResponse(router.to_path(index))