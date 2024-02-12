from base64 import b64decode

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client
from django.test.utils import override_settings
from rest_framework_simplejwt.tokens import RefreshToken

pdf_raw: str = ('JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSA8RkVGRjA0M'
                 'UQwNDNFMDQzMjA0NEIwNDM5MDAyMDA0MzQwNDNFMDQzQTA0NDMwNDNDMDQzNTA0M0QwNDQyPgovUHJvZHVjZXIgKFNraWEvUERGIG0xMjIgR29vZ2xlIERvY3MgUmVuZGVyZXIpPj4KZW5kb2JqCjMgMCBvYmoKPDwvY2EgMQovQk0gL05vcm1hbD4+CmVuZG9iago0IDAgb2JqCjw8L0xlbmd0aCA4ND4+IHN0cmVhbQoxIDAgMCAtMSAwIDg0MiBjbQpxCi43NSAwIDAgLjc1IDAgMCBjbQoxIDEgMSBSRyAxIDEgMSByZwovRzMgZ3MKMCAwIDc5NCAxMTIzIHJlCmYKUQoKZW5kc3RyZWFtCmVuZG9iagoyIDAgb2JqCjw8L1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PC9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQovRXh0R1N0YXRlIDw8L0czIDMgMCBSPj4+PgovTWVkaWFCb3ggWzAgMCA1OTYgODQyXQovQ29udGVudHMgNCAwIFIKL1N0cnVjdFBhcmVudHMgMAovUGFyZW50IDUgMCBSPj4KZW5kb2JqCjUgMCBvYmoKPDwvVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWzIgMCBSXT4+CmVuZG9iago2IDAgb2JqCjw8L1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDUgMCBSPj4KZW5kb2JqCnhyZWYKMCA3CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMzIwIDAwMDAwIG4gCjAwMDAwMDAxNTEgMDAwMDAgbiAKMDAwMDAwMDE4OCAwMDAwMCBuIAowMDAwMDAwNTA4IDAwMDAwIG4gCjAwMDAwMDA1NjMgMDAwMDAgbiAKdHJhaWxlcgo8PC9TaXplIDcKL1Jvb3QgNiAwIFIKL0luZm8gMSAwIFI+PgpzdGFydHhyZWYKNjEwCiUlRU9GCg==')

@pytest.fixture
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(';base64,')
    extention = _format.split('/')[1]
    return ContentFile(b64decode(_raw_image), f'image.{extention}')

@pytest.fixture
def document() -> Category:
    return Documents.objects.create(document=image_content_file, ...)

def test_download_one_document(api_client, document):
    url = reverse('...')
    response = api_client.get(url, data={'ids': [document.id]})
    assert response.status_code == 200
    assert response.content == document

