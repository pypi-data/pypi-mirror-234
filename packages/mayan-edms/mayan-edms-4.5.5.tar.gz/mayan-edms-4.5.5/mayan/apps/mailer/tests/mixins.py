import json

from mayan.apps.testing.tests.mixins import TestMixinObjectCreationTrack

from ..models import UserMailer

from .literals import (
    TEST_EMAIL_ADDRESS, TEST_EMAIL_FROM_ADDRESS, TEST_USER_MAILER_LABEL
)
from .mailers import TestBackend


class MailerTestMixin(TestMixinObjectCreationTrack):
    _test_object_model = UserMailer
    _test_object_name = '_test_user_mailer'

    def _create_test_user_mailer(self):
        self._test_user_mailer = UserMailer.objects.create(
            default=True,
            enabled=True,
            label=TEST_USER_MAILER_LABEL,
            backend_path=TestBackend.backend_id,
            backend_data=json.dumps(
                obj={
                    'from': TEST_EMAIL_FROM_ADDRESS
                }
            )
        )


class DocumentMailerViewTestMixin(MailerTestMixin):
    def _request_test_document_link_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_link_single', kwargs={
                'document_id': self._test_document.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            },
        )

    def _request_test_document_link_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_link_multiple', query={
                'id_list': self._test_document.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            },
        )


class DocumentFileMailerViewTestMixin(MailerTestMixin):
    def _request_test_document_file_link_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_file_link_single', kwargs={
                'document_file_id': self._test_document_file.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )

    def _request_test_document_file_link_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_file_link_multiple', query={
                'id_list': self._test_document_file.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )

    def _request_test_document_file_attachment_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_file_attachment_single', kwargs={
                'document_file_id': self._test_document_file.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )

    def _request_test_document_file_attachment_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_file_attachment_multiple', query={
                'id_list': self._test_document_file.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )


class DocumentVersionMailerViewTestMixin(MailerTestMixin):
    def _request_test_document_version_link_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_version_link_single', kwargs={
                'document_version_id': self._test_document_version.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            },
        )

    def _request_test_document_version_link_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_version_link_multiple', query={
                'id_list': self._test_document_version.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            },
        )

    def _request_test_document_version_attachment_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_version_attachment_single',
            kwargs={
                'document_version_id': self._test_document_version.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )

    def _request_test_document_version_attachment_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_version_attachment_multiple',
            query={
                'id_list': self._test_document_version.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self._test_user_mailer.pk
            }
        )


class MailerViewTestMixin(MailerTestMixin):
    def _request_test_user_mailer_create_view(self):
        self._test_object_track()

        response = self.post(
            viewname='mailer:user_mailer_create', kwargs={
                'backend_path': TestBackend.backend_id
            }, data={
                'default': True,
                'enabled': True,
                'label': TEST_USER_MAILER_LABEL,
            }
        )

        self._test_object_set()

        return response

    def _request_test_user_mailer_delete_view(self):
        return self.post(
            viewname='mailer:user_mailer_delete', kwargs={
                'mailer_id': self._test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_edit_view(self):
        return self.post(
            viewname='mailer:user_mailer_edit', kwargs={
                'mailer_id': self._test_user_mailer.pk
            }, data={
                'label': '{}_edited'.format(TEST_USER_MAILER_LABEL)
            }
        )

    def _request_test_user_mailer_list_view(self):
        return self.get(
            viewname='mailer:user_mailer_list'
        )

    def _request_test_user_mailer_log_entry_view(self):
        return self.get(
            viewname='mailer:user_mailer_log', kwargs={
                'mailer_id': self._test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_test_view(self):
        return self.post(
            viewname='mailer:user_mailer_test', kwargs={
                'mailer_id': self._test_user_mailer.pk
            }, data={
                'email': getattr(
                    self, '_test_email_address', TEST_EMAIL_ADDRESS
                )
            }
        )
