# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext.blobstore import BlobInfo

from base import BlobstoreTestCase
from blob_app import blob_facade
from gaepermission.model import MainUser
from mock import Mock
from mommygae import mommy
from routes.updown import upload


class UploadTests(BlobstoreTestCase):
    def test_upload(self):
        handler = Mock()
        blob_key = self.save_blob('some data')
        blob_info = BlobInfo.get(blob_key)
        handler.get_uploads = lambda k: [blob_info]
        user = mommy.save_one(MainUser)
        upload.index(handler, user, None)
        blob_files = blob_facade.list_blob_files_cmd(user)()
        self.assertEqual(1, len(blob_files))
        self.assertEqual(blob_key, blob_files[0].blob_key)