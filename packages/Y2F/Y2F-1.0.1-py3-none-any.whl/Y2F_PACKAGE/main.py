import sys
import asyncio
from Y2F_PACKAGE import Graphical_User_Interface, Youtube_Content_Operations


####################################
# YOUTUBE VIDEO DOWNLOAD INTERFACE #
####################################
async def Youtube_Download():
    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("link request menu")
    youtube_link = await gui.Graphical_User_Interface_Selector()

    if youtube_link.lower() == "_back":
        await main_entry_point()

    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("path selection menu")
    selected_path = await gui.Graphical_User_Interface_Selector()

    if selected_path.lower() == "_back":
        await main_entry_point()

    selected_resolution = await Video_Resolution_Selection()

    if selected_resolution == "_back":
        await main_entry_point()

    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("video downloading warning")
    await gui.Graphical_User_Interface_Selector()

    file_download = Youtube_Content_Operations.Operations("youtube video download", youtube_link, selected_path,
                                                          selected_resolution)
    file_download_result = await file_download.Operation_Selection()

    message = file_download_result
    await Message_Displayer(message)


##########################################
# YOUTUBE MP3 VIDEO CONVERSION INTERFACE #
##########################################
async def Youtube_Conversion():
    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("link request menu")
    youtube_link = await gui.Graphical_User_Interface_Selector()

    if youtube_link.lower() == "_back":
        await main_entry_point()

    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("path selection menu")
    selected_path = await gui.Graphical_User_Interface_Selector()

    if selected_path.lower() == "_back":
        await main_entry_point()

    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("video downloading warning")
    await gui.Graphical_User_Interface_Selector()

    file_download = Youtube_Content_Operations.Operations("youtube video conversion", youtube_link, selected_path, None)
    file_download_result = await file_download.Operation_Selection()

    message = file_download_result
    await Message_Displayer(message)


###############################################################
# YOUTUBE VIDEO DOWNLOAD VIDEO RESOLUTION SELECTION INTERFACE #
###############################################################
async def Video_Resolution_Selection():
    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("resolution selection menu")
    selected_resolution = (await gui.Graphical_User_Interface_Selector()).lower()

    if selected_resolution == "144p":
        return selected_resolution
    elif selected_resolution == "360p":
        return selected_resolution
    elif selected_resolution == "720p":
        return selected_resolution
    elif selected_resolution == "_back":
        return selected_resolution
    else:
        await Video_Resolution_Selection()


#######################################
# YOUTUBE OPERTION FEEDBACK INTERFACE #
#######################################
async def Message_Displayer(gui_message):
    try:
        selected_gui = None

        if gui_message is not None:
            if gui_message == "pytube missing":
                selected_gui = "module not found"
            elif gui_message == "wrong path":
                selected_gui = "path not found"
            elif gui_message == "internal error":
                selected_gui = "unknown error"
            elif gui_message == "wrong link":
                selected_gui = "wrong link"
            elif gui_message == "age restricted video":
                selected_gui = "age restricted video"
            else:
                selected_gui = "download successful"

        gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages(selected_gui)
        await gui.Graphical_User_Interface_Selector()

        gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("clear screen")
        await gui.Graphical_User_Interface_Selector()

        await main_entry_point()
    except KeyboardInterrupt:
        sys.exit(0)


##############################
# MAIN ENTRY POINT INTERFACE #
##############################
async def main_entry_point():
    gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("main menu")
    selected_input = (await gui.Graphical_User_Interface_Selector()).lower()

    if selected_input == "d":
        await Youtube_Download()
    elif selected_input == "c":
        await Youtube_Conversion()
    elif selected_input == "e":
        gui = Graphical_User_Interface.Graphical_User_Interfaces_For_Menus_And_Messages("clear screen")
        await gui.Graphical_User_Interface_Selector()
        sys.exit(0)
    else:
        await main_entry_point()


def main():
    asyncio.run(main_entry_point())


if __name__ == "__main__":
    main()
