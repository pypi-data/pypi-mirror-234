import os
import sys


#########################################
# CLASS THAT MANAGES YOUTUBE OPERATIONS #
#########################################
class Operations:
    audio_only = False
    chosen_operation = None
    chosen_path = None
    youtube_link = None
    selected_video_resolution = None

    def __init__(
        self,
        init_chosen_operation,
        init_youtube_link,
        init_chosen_path,
        init_selected_video_resolution,
    ):
        self.chosen_operation = init_chosen_operation
        self.chosen_path = init_chosen_path
        self.youtube_link = init_youtube_link
        self.selected_video_resolution = init_selected_video_resolution

    #########################################################################
    # SELECTS THE YOUTUBE OPERATION ( MP4 TO MP3 DOWNLOAD OR MP4 DOWNLOAD ) #
    #########################################################################
    async def Operation_Selection(self):
        if self.chosen_operation == "youtube video conversion":
            self.audio_only = True
        else:
            self.audio_only = False

        download_result = await self.__Youtube_Download()
        return download_result

    #######################################################################################
    # DOWNLOAD THE MP4 VIDEO OR AUDIO FILE BINARY DATA AND STORE IT IN THE OS FILE SYSTEM #
    #######################################################################################
    async def __Youtube_Download(self):
        try:
            import pytube.exceptions
            try:
                try:
                    try:
                        try:
                            try:
                                try:
                                    try:
                                        try:
                                            try:
                                                try:
                                                    try:
                                                        try:
                                                            try:
                                                                try:
                                                                    from pytube import (
                                                                        YouTube,
                                                                    )

                                                                    youtube_object = YouTube(
                                                                        self.youtube_link, use_oauth=False, allow_oauth_cache=False
                                                                    )

                                                                    if (
                                                                        self.selected_video_resolution
                                                                        is None
                                                                    ):
                                                                        video_audio = youtube_object.streams.filter(
                                                                            only_audio=self.audio_only
                                                                        ).first()

                                                                        audio_path = video_audio.download(
                                                                            max_retries=10,
                                                                            output_path=self.chosen_path,
                                                                        )

                                                                        os.rename(
                                                                            audio_path,
                                                                            audio_path
                                                                            + ".mp3",
                                                                        )

                                                                        return (
                                                                            audio_path
                                                                        )

                                                                    else:
                                                                        resolutions = []
                                                                        available_resolutions = [
                                                                            "144p",
                                                                            "360p",
                                                                            "720p",
                                                                        ]

                                                                        for (
                                                                            stream
                                                                        ) in youtube_object.streams.order_by(
                                                                            "resolution"
                                                                        ):
                                                                            for (
                                                                                index
                                                                            ) in range(
                                                                                0,
                                                                                len(
                                                                                    available_resolutions
                                                                                ),
                                                                            ):
                                                                                if (
                                                                                    available_resolutions[
                                                                                        index
                                                                                    ]
                                                                                    == stream.resolution
                                                                                ):
                                                                                    exist = resolutions.count(
                                                                                        stream.resolution
                                                                                    )
                                                                                    if (
                                                                                        exist
                                                                                        == 0
                                                                                    ):
                                                                                        resolutions.append(
                                                                                            stream.resolution
                                                                                        )
                                                                                    break

                                                                        maximum_available_resolution = resolutions[
                                                                            len(
                                                                                resolutions
                                                                            )
                                                                            - 1
                                                                        ]

                                                                        try:
                                                                            maximum_available_resolution = resolutions[
                                                                                resolutions.index(
                                                                                    self.selected_video_resolution
                                                                                )
                                                                            ]
                                                                        except (
                                                                            ValueError
                                                                        ):
                                                                            pass

                                                                        video_audio = youtube_object.streams.filter(
                                                                            only_audio=self.audio_only,
                                                                            res=maximum_available_resolution,
                                                                            progressive=True
                                                                        ).first()

                                                                        path = video_audio.download(
                                                                            output_path=self.chosen_path,
                                                                            max_retries=100,
                                                                        )

                                                                        return path

                                                                except (
                                                                    pytube.exceptions.RecordingUnavailable
                                                                ) as e:
                                                                    # print(e.message)
                                                                    return (
                                                                        "internal error"
                                                                    )
                                                            except (
                                                                pytube.exceptions.MembersOnly
                                                            ) as e:
                                                                # print(e.message)
                                                                return "internal error"
                                                        except (
                                                            pytube.exceptions.MaxRetriesExceeded
                                                        ) as e:
                                                            # print(e.message)
                                                            return "internal error"
                                                    except (
                                                        pytube.exceptions.LiveStreamError
                                                    ) as e:
                                                        # print(e.message)
                                                        return "internal error"
                                                except (
                                                    pytube.exceptions.HTMLParseError
                                                ) as e:
                                                    # print(e.message)
                                                    return "internal error"
                                            except (
                                                pytube.exceptions.AgeRestrictedError
                                            ) as e:
                                                # print(e.message)
                                                return "age restricted video"
                                        except pytube.exceptions.VideoPrivate as e:
                                            # print(e.message)
                                            return "internal error"
                                    except pytube.exceptions.ExtractError as e:
                                        # print(e.message)
                                        return "internal error"
                                except pytube.exceptions.PytubeError as e:
                                    # print(e.message)
                                    return "internal error"
                            except TypeError as e:
                                # print(e.message)
                                return "internal error"
                        except ValueError as e:
                            # print(e.message)
                            return "internal error"
                    except FileNotFoundError as e:
                        # print(e.message)
                        return "wrong path"
                except KeyboardInterrupt as e:
                    # print(e.message)
                    sys.exit(0)
            except pytube.exceptions.RegexMatchError as e:
                # print(e.message)
                return "wrong link"
        except ModuleNotFoundError as e:
            return "pytube missing"
