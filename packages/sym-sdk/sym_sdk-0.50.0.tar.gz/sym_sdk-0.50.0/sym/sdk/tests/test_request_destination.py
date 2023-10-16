import pytest as pytest

from sym.sdk import SlackChannelID, SlackChannelName, SlackUser, SlackUserGroup


class TestRequestDestination:
    def test_slack_channel_id_succeeds_for_valid_channel_ids(self):
        assert SlackChannelID(channel_id="C12345").channel_id == "C12345"
        assert SlackChannelID(channel_id="D12345").channel_id == "D12345"
        assert SlackChannelID(channel_id="G12345").channel_id == "G12345"
        assert SlackChannelID(channel_id="  C12345 ").channel_id == "C12345"

    @pytest.mark.parametrize(
        "channel_id, match_error",
        [
            ("", "must be non-empty"),
            (" ", "must be non-empty"),
            ("X123", "not a valid Slack Channel ID"),
        ],
    )
    def test_slack_channel_id_validate_channel_id_format_throws_error_if_not_valid_channel_id(
        self, channel_id, match_error
    ):
        with pytest.raises(ValueError, match=match_error):
            SlackChannelID(channel_id=channel_id)

    def test_slack_channel_id__str__(self):
        assert SlackChannelID(channel_id="C12345").__str__() == "SlackChannelID 'C12345'"
        assert SlackChannelID(channel_id="D12345").__str__() == "SlackChannelID 'D12345'"
        assert SlackChannelID(channel_id="G12345").__str__() == "SlackChannelID 'G12345'"
        assert SlackChannelID(channel_id="  C12345 ").__str__() == "SlackChannelID 'C12345'"

    def test_slack_channel_name_succeeds_if_channel_name_exists(self):
        assert (
            SlackChannelName(channel_name="is-valid-channel-name").channel_name
            == "is-valid-channel-name"
        )
        assert (
            SlackChannelName(channel_name="  is-valid-channel-name  ").channel_name
            == "is-valid-channel-name"
        )

    @pytest.mark.parametrize(
        "channel_name, match_error",
        [
            ("", "channel_name must be non-empty"),
            (" ", "channel_name must be non-empty"),
        ],
    )
    def test_slack_channel_name_throws_error_when_no_value_given(self, channel_name, match_error):
        with pytest.raises(ValueError, match=match_error):
            SlackChannelName(channel_name=channel_name)

    def test_slack_channel_name__str__(self):
        assert (
            SlackChannelName(channel_name="is-valid-channel-name").__str__()
            == "SlackChannelName 'is-valid-channel-name'"
        )
        assert (
            SlackChannelName(channel_name="  is-valid-channel-name  ").__str__()
            == "SlackChannelName 'is-valid-channel-name'"
        )

    def test_slack_user_succeeds_if_valid(self):
        assert SlackUser(user_id="W09876").user_id == "W09876"
        assert SlackUser(user_id="U12345").user_id == "U12345"
        assert SlackUser(user_id="  U12345  ").user_id == "U12345"

    @pytest.mark.parametrize(
        "user_id, match_error",
        [
            ("", "user_id must be non-empty"),
            (" ", "user_id must be non-empty"),
            (
                "X123",
                "X123 is not a valid Slack User ID. Slack User IDs must start with 'U' or 'W'.",
            ),
        ],
    )
    def test_slack_user_throws_error_if_invalid_user_id(self, user_id, match_error):
        with pytest.raises(ValueError, match=match_error):
            SlackUser(user_id=user_id)

    def test_slack_user__str__(self):
        assert SlackUser(user_id="U12345").__str__() == "SlackUser 'U12345'"
        assert SlackUser(user_id="  U12345  ").__str__() == "SlackUser 'U12345'"

    def test_slack_user_mention(self):
        assert SlackUser(user_id="U12345").mention() == "<@U12345>"
        assert SlackUser(user_id="  U12345  ").mention() == "<@U12345>"

    def test_slack_user_group_if_valid(self):
        assert SlackUserGroup(users=[SlackUser(user_id="U12345")]).users == [
            SlackUser(user_id="U12345")
        ]

    @pytest.mark.parametrize(
        "users, match_error",
        [
            ([], "at least 1 items"),
            (
                [
                    SlackUser(user_id="U1"),
                    SlackUser(user_id="U2"),
                    SlackUser(user_id="U3"),
                    SlackUser(user_id="U4"),
                    SlackUser(user_id="U5"),
                    SlackUser(user_id="U6"),
                    SlackUser(user_id="U7"),
                    SlackUser(user_id="U8"),
                ],
                "at most 7 items",
            ),
        ],
    )
    def test_slack_user_group_throws_error_if_invalid(self, users, match_error):
        with pytest.raises(ValueError, match=match_error):
            SlackUserGroup(users=users)

    def test_slack_user_group__str__(self):
        assert (
            SlackUserGroup(
                users=[SlackUser(user_id="U12345"), SlackUser(user_id="U6789")]
            ).__str__()
            == "SlackUserGroup '['U12345', 'U6789']'"
        )
