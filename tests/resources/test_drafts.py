from unittest.mock import patch, Mock

from nylas_v3.models.drafts import Draft
from nylas_v3.resources.drafts import Drafts


class TestDraft:
    def test_draft_deserialization(self):
        draft_json = {
            "body": "Hello, I just sent a message using Nylas!",
            "cc": [{"email": "arya.stark@example.com"}],
            "attachments": [
                {
                    "content_type": "text/calendar",
                    "id": "4kj2jrcoj9ve5j9yxqz5cuv98",
                    "size": 1708,
                }
            ],
            "folders": ["8l6c4d11y1p4dm4fxj52whyr9", "d9zkcr2tljpu3m4qpj7l2hbr0"],
            "from": [{"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}],
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "id": "5d3qmne77v32r8l4phyuksl2x",
            "object": "draft",
            "reply_to": [
                {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
            ],
            "snippet": "Hello, I just sent a message using Nylas!",
            "starred": True,
            "subject": "Hello from Nylas!",
            "thread_id": "1t8tv3890q4vgmwq6pmdwm8qgsaer",
            "to": [{"name": "Jon Snow", "email": "j.snow@example.com"}],
            "date": 1705084742,
            "created_at": 1705084926,
        }

        draft = Draft.from_dict(draft_json)

        assert draft.body == "Hello, I just sent a message using Nylas!"
        assert draft.cc == [{"email": "arya.stark@example.com"}]
        assert len(draft.attachments) == 1
        assert draft.attachments[0].content_type == "text/calendar"
        assert draft.attachments[0].id == "4kj2jrcoj9ve5j9yxqz5cuv98"
        assert draft.attachments[0].size == 1708
        assert draft.folders == [
            "8l6c4d11y1p4dm4fxj52whyr9",
            "d9zkcr2tljpu3m4qpj7l2hbr0",
        ]
        assert draft.from_ == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert draft.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert draft.id == "5d3qmne77v32r8l4phyuksl2x"
        assert draft.object == "draft"
        assert draft.reply_to == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert draft.snippet == "Hello, I just sent a message using Nylas!"
        assert draft.starred is True
        assert draft.subject == "Hello from Nylas!"
        assert draft.thread_id == "1t8tv3890q4vgmwq6pmdwm8qgsaer"
        assert draft.to == [{"name": "Jon Snow", "email": "j.snow@example.com"}]
        assert draft.date == 1705084742
        assert draft.created_at == 1705084926

    def test_list_drafts(self, http_client_list_response):
        drafts = Drafts(http_client_list_response)

        drafts.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/drafts", None, None, None, overrides=None
        )

    def test_list_drafts_with_query_params(self, http_client_list_response):
        drafts = Drafts(http_client_list_response)

        drafts.list(
            identifier="abc-123",
            query_params={
                "subject": "Hello from Nylas!",
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/drafts",
            None,
            {
                "subject": "Hello from Nylas!",
            },
            None,
            overrides=None,
        )

    def test_find_draft(self, http_client_response):
        drafts = Drafts(http_client_response)

        drafts.find(identifier="abc-123", draft_id="draft-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/drafts/draft-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_create_draft(self, http_client_response):
        drafts = Drafts(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
        }

        drafts.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/drafts",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_create_draft_small_attachment(self, http_client_response):
        drafts = Drafts(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3,
                },
            ],
        }

        drafts.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/drafts",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_create_draft_large_attachment(self, http_client_response):
        drafts = Drafts(http_client_response)
        mock_encoder = Mock()
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3 * 1024 * 1024,
                },
            ],
        }

        with patch(
            "nylas.resources.drafts._build_form_request", return_value=mock_encoder
        ):
            drafts.create(identifier="abc-123", request_body=request_body)

            http_client_response._execute.assert_called_once_with(
                method="POST",
                path="/v3/grants/abc-123/drafts",
                data=mock_encoder,
                overrides=None,
            )

    def test_update_draft(self, http_client_response):
        drafts = Drafts(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
        }

        drafts.update(
            identifier="abc-123", draft_id="draft-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/drafts/draft-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_draft_small_attachment(self, http_client_response):
        drafts = Drafts(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3,
                },
            ],
        }

        drafts.update(
            identifier="abc-123", draft_id="draft-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/drafts/draft-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_draft_large_attachment(self, http_client_response):
        drafts = Drafts(http_client_response)
        mock_encoder = Mock()
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3 * 1024 * 1024,
                },
            ],
        }

        with patch(
            "nylas.resources.drafts._build_form_request", return_value=mock_encoder
        ):
            drafts.update(
                identifier="abc-123", draft_id="draft-123", request_body=request_body
            )

            http_client_response._execute.assert_called_once_with(
                method="PUT",
                path="/v3/grants/abc-123/drafts/draft-123",
                data=mock_encoder,
                overrides=None,
            )

    def test_destroy_draft(self, http_client_delete_response):
        drafts = Drafts(http_client_delete_response)

        drafts.destroy(identifier="abc-123", draft_id="draft-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/drafts/draft-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_send_draft(self, http_client_response):
        drafts = Drafts(http_client_response)

        drafts.send(identifier="abc-123", draft_id="draft-123")

        http_client_response._execute.assert_called_once_with(
            method="POST", path="/v3/grants/abc-123/drafts/draft-123", overrides=None
        )
