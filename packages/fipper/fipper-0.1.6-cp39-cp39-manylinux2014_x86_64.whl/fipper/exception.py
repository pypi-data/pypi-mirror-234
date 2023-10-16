# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================


class ExceptionDetected(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class GroupCallsAlready(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class ChatWithoutGroupCall(Exception):
    def __init__(self, err: str):
        super().__init__(err)


class GroupCallsSsrcDuplicate(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class GroupCallAddParticipantError(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class GroupCallNotFound(Exception):
    """Group call not found, raised by
    :meth:`~pycover.pycover.get_active_call`,
    :meth:`~pycover.pycover.get_call`
    """

    def __init__(
        self,
        chat_id: int,
    ):
        super().__init__(
            f'Group call not found with the chat id {chat_id}',
        )


class NodeJSNotInstalled(Exception):
    """Node.js isn’t installed, raised by
    :meth:`~pycover.pycover.start` or
    :meth:`~pycover.pycover.run`
    """

    def __init__(
        self,
        version_needed: str,
    ):
        super().__init__(
            f'Please install node ({version_needed}+)',
        )


class TooOldNodeJSVersion(Exception):
    """Node.js version is too old, raised by
    :meth:`~pycover.pycover.start` or
    :meth:`~pycover.pycover.run`
    """

    def __init__(
        self,
        version_needed: str,
        node_version: str,
    ):
        super().__init__(
            f'Needed node {version_needed}+, '
            'actually installed is '
            f'{node_version}',
        )


class InvalidStreamMode(Exception):
    """The stream mode is invalid, raised by
    :meth:`~pycover.pycover.change_stream` or
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Invalid stream mode',
        )


class ClientCallsNotSet(Exception):
    """An MtProto client not set to
    :class:`~pycover.PyCover`, raised by
    :meth:`~pycover.pycover.join_group_call`,
    :meth:`~pycover.pycover.leave_group_call`,
    :meth:`~pycover.pycover.change_volume_call`,
    :meth:`~pycover.pycover.change_stream`,
    :meth:`~pycover.pycover.pause_stream` and
    :meth:`~pycover.pycover.resume_stream`
    """

    def __init__(self, err=None):
        text_err = f'ClientClass Not Set'
        if err is not None:
            text_err = 'ClientClass Not Set' + f' -> {err}'
        super().__init__(
            text_err,
        )


class NodeJSNotRunning(Exception):
    """NodeJS core not running, do
    :meth:`~pycover.pycover.start`
    before call these methods, raised by
    :meth:`~pycover.pycover.join_group_call`,
    :meth:`~pycover.pycover.leave_group_call`,
    :meth:`~pycover.pycover.change_volume_call`,
    :meth:`~pycover.pycover.change_stream`,
    :meth:`~pycover.pycover.pause_stream` and
    :meth:`~pycover.pycover.resume_stream`
    """

    def __init__(self):
        super().__init__(
            'Node.js not running',
        )


class NoActiveGroupCall(Exception):
    """No active group call found, raised by
    :meth:`~pycover.pycover.join_group_call`,
    :meth:`~pycover.pycover.leave_group_call`,
    :meth:`~pycover.pycover.change_volume_call`,
    """

    def __init__(self):
        super().__init__(
            'No active group call',
        )


class NotInGroupCallError(Exception):
    """The userbot there isn't in a group call, raised by
    :meth:`~pycover.pycover.leave_group_call`
    """

    def __init__(self):
        super().__init__(
            'The userbot there isn\'t in a group call',
        )


class AlreadyJoinedError(Exception):
    """Already joined into group call, raised by
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Already joined into group call',
        )


class TelegramServerError(Exception):
    """Telegram Server is having some
    internal problems, raised by
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Telegram Server is having some '
            'internal problems',
        )


class ClientCallsAlreadyRunning(Exception):
    """PyCover client is already running, raised by
    :meth:`~pycover.pycover.start`,
    """

    def __init__(self):
        super().__init__(
            'ClientCalls Is Already Running',
        )


class TooManyCustomApiDecorators(Exception):
    """Too Many Custom Api Decorators, raised by
    :meth:`~pycover.CustomApi.on_update_custom_api`,
    """

    def __init__(self):
        super().__init__(
            'Too Many Custom Api Decorators',
        )


class InvalidMtProtoClient(Exception):
    """You set an invalid MtProto client, raised by
    :meth:`~pycover.PyCover`
    """

    def __init__(self):
        super().__init__(
            'Invalid MtProto Client',
        )


class NoVideoSourceFound(Exception):
    """This error is raised when the stream does not have video streams
    :meth:`~pycover.pycover.join_group_call` or
    :meth:`~pycover.pycover.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            f'No video source found on {path}',
        )


class InvalidVideoProportion(Exception):
    """FFmpeg have sent invalid video measure
    response, raised by
    :meth:`~pycover.pycover.join_group_call` or
    :meth:`~pycover.pycover.change_stream`
    """

    def __init__(self, message: str):
        super().__init__(
            message,
        )


class NoAudioSourceFound(Exception):
    """This error is raised when the stream does not have audio streams
    :meth:`~pycover.pycover.join_group_call` or
    :meth:`~pycover.pycover.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            f'No audio source found on {path}',
        )


class FFmpegNotInstalled(Exception):
    """FFmpeg isn't installed, this error is raised by
    :meth:`~pycover.pycover.join_group_call` or
    :meth:`~pycover.pycover.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            'FFmpeg ins\'t installed on your server',
        )


class RTMPStreamNeeded(Exception):
    """Needed an RTMP Stream, raised by
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Needed an RTMP Stream',
        )


class UnMuteNeeded(Exception):
    """Needed to unmute the userbot, raised by
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Needed to unmute the userbot',
        )


class ModuleNotFound(ImportWarning):
    def __init__(self, error: str):
        super().__init__(
            f'[ IMPORT WARNING ] - Install module ( {error} ) for running this command'
        )
