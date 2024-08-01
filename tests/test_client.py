from nylas_v3 import Client
from nylas_v3.resources.applications import Applications
from nylas_v3.resources.attachments import Attachments
from nylas_v3.resources.auth import Auth
from nylas_v3.resources.calendars import Calendars
from nylas_v3.resources.connectors import Connectors
from nylas_v3.resources.contacts import Contacts
from nylas_v3.resources.drafts import Drafts
from nylas_v3.resources.events import Events
from nylas_v3.resources.folders import Folders
from nylas_v3.resources.grants import Grants
from nylas_v3.resources.messages import Messages
from nylas_v3.resources.threads import Threads
from nylas_v3.resources.webhooks import Webhooks


class TestClient:
    def test_client_init(self):
        client = Client(
            api_key="test-key",
            api_uri="https://test.nylas.com",
            timeout=60,
        )

        assert client.api_key == "test-key"
        assert client.api_uri == "https://test.nylas.com"
        assert client.http_client.timeout == 60

    def test_client_init_defaults(self):
        client = Client(
            api_key="test-key",
        )

        assert client.api_key == "test-key"
        assert client.api_uri == "https://api.us.nylas.com"
        assert client.http_client.timeout == 90

    def test_client_auth_property(self, client):
        assert client.auth is not None
        assert type(client.auth) is Auth

    def test_client_applications_property(self, client):
        assert client.applications is not None
        assert type(client.applications) is Applications

    def test_client_attachments_property(self, client):
        assert client.attachments is not None
        assert type(client.attachments) is Attachments

    def test_client_calendars_property(self, client):
        assert client.calendars is not None
        assert type(client.calendars) is Calendars

    def test_client_contacts_property(self, client):
        assert client.contacts is not None
        assert type(client.contacts) is Contacts

    def test_client_connectors_property(self, client):
        assert client.connectors is not None
        assert type(client.connectors) is Connectors

    def test_client_drafts_property(self, client):
        assert client.drafts is not None
        assert type(client.drafts) is Drafts

    def test_client_events_property(self, client):
        assert client.events is not None
        assert type(client.events) is Events

    def test_client_folders_property(self, client):
        assert client.folders is not None
        assert type(client.folders) is Folders

    def test_client_grants_property(self, client):
        assert client.grants is not None
        assert type(client.grants) is Grants

    def test_client_messages_property(self, client):
        assert client.messages is not None
        assert type(client.messages) is Messages

    def test_client_threads_property(self, client):
        assert client.threads is not None
        assert type(client.threads) is Threads

    def test_client_webhooks_property(self, client):
        assert client.webhooks is not None
        assert type(client.webhooks) is Webhooks
