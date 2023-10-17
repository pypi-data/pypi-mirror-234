import os
import sys
import platform


##########################################################
# CLASS THAT STORES AND MANAGES GRAPHICAL USER INTERFACE #
##########################################################
class Graphical_User_Interfaces_For_Menus_And_Messages:
    selected_graphical_user_interface = None

    def __init__(self, init_selected_graphical_user_interface):
        self.selected_graphical_user_interface = init_selected_graphical_user_interface

    async def Graphical_User_Interface_Selector(self):
        selected_input = None

        if self.selected_graphical_user_interface == "main menu":
            selected_input = await self.__Main_Menu()
        elif self.selected_graphical_user_interface == "link request menu":
            selected_input = await self.__Youtube_Video_Link_Request_Sub_Menu()
        elif self.selected_graphical_user_interface == "resolution selection menu":
            selected_input = await self.__Video_Resolution_Selection_Menu()
        elif self.selected_graphical_user_interface == "path selection menu":
            selected_input = await self.__Youtube_Video_Download_Path_Sub_Menu()
        elif self.selected_graphical_user_interface == "download successful":
            selected_input = await self.__File_Successfully_Installed_Message()
        elif self.selected_graphical_user_interface == "module not found":
            selected_input = await self.__Module_Not_Found_Error()
        elif self.selected_graphical_user_interface == "path not found":
            selected_input = await self.__Path_Not_Found_Error()
        elif self.selected_graphical_user_interface == "unknown error":
            selected_input = await self.__An_Unknown_Error_Occurred()
        elif self.selected_graphical_user_interface == "wrong link":
            selected_input = await self.__Wrong_Link_Error_Occurred()
        elif self.selected_graphical_user_interface == "video downloading warning":
            await self.__Video_Downloading_Warning()
        elif self.selected_graphical_user_interface == "age restricted video":
            await self.__Age_Restriction_Error()
        elif self.selected_graphical_user_interface == "clear screen":
            await self.__Clear_Screen()

        return selected_input

    async def __Clear_Screen(self):
        detected_operating_system = platform.system()

        if detected_operating_system == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    async def __Main_Menu(self):
        try:
            await self.__Clear_Screen()

            print(
                "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "[][]   .???! .7??7 .!JYYJ7:  ^??????7     .~7??JJJJJJJJJJJJJJJJJJ??7~.    [][]"
            )
            print(
                "[][]    G@@@:7@@@J:B@@BP@@@J Y@@@@@@#   ^5PPPPPPPPPPPPPPPPPPPPPPPPPP5^    [][]"
            )
            print(
                "[][]    :&@@JG@@G ?@@@~ &@@@.J@@@B:::   JP555555555PYYPPPPP555555555PJ    [][]"
            )
            print(
                "[][]     ?@@&@@@^ :~~^:G@@@5 J@@@#77^   YP55555555PP~ ^!J5PPP5555555PY    [][]"
            )
            print(
                "[][]      G@@@@J     ^B@@@Y  J@@@@@@Y  .5P55555555PP^    .^!YP555555PY.   [][]"
            )
            print(
                "[][]      ~@@@#.    7&@@#!   J@@@B::.  .5P55555555PP^    .^!YP555555PY.   [][]"
            )
            print(
                "[][]      ^@@@B   .Y@@@G^.:. J@@@B      YP55555555PP~ ^!J5PPP5555555PY    [][]"
            )
            print(
                "[][]      ^@@@B   ?@@@@&&&@P Y@@@B      JP555555555PYYPPPPP555555555PJ    [][]"
            )
            print(
                "[][]      ^@@@B   ?@@@@&&&@P Y@@@B      ^5PPPPPPPPPPPPPPPPPPPPPPPPPP5^    [][]"
            )
            print(
                "[][]      .~!!~   :!~~~!!!!^ :!~!~       .~7??JJJJJJJJJJJJJJJJJJ??7~.     [][]"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )
            print(
                "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "[][]  ENTER 'C' TO CONVERT A YOUTUBE VIDEO IN MP3 FORMAT                  [][]"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "[][]  ENTER 'D' TO DOWNLOAD A VIDEO IN MP4 FORMAT                         [][]"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "[][]  ENTER 'E' TO EXIT                                                   [][]"
            )
            print(
                "[][]                                                                      [][]"
            )
            print(
                "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )
            print(
                "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Youtube_Video_Link_Request_Sub_Menu(self):
        try:
            await self.__Clear_Screen()

            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]                                                          [][]")
            print("[][] ENTER THE LINK OF THE YOUTUBE VIDEO YOU WANT TO DOWNLOAD [][]")
            print("[][]                                                          [][]")
            print("[][]                                                          [][]")
            print("[][]                                                          [][]")
            print("[][]          ENTER '_BACK' TO CANCEL THE DOWNLOAD            [][]")
            print("[][]                                                          [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Youtube_Video_Download_Path_Sub_Menu(self):
        try:
            await self.__Clear_Screen()

            print(
                "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )
            print(
                "[][]                                                             [][]"
            )
            print(
                "[][] ENTER THE PATH WHERE THE YOUTUBE VIDEO YOU WANT TO DOWNLOAD [][]"
            )
            print(
                "[][] WILL BE SAVED                                               [][]"
            )
            print(
                "[][]                                                             [][]"
            )
            print(
                "[][]                                                             [][]"
            )
            print(
                "[][]                                                             [][]"
            )
            print(
                "[][] ENTER '_BACK' TO CANCEL THE DOWNLOAD                        [][]"
            )
            print(
                "[][]                                                             [][]"
            )
            print(
                "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
            )

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Video_Resolution_Selection_Menu(self):
        try:
            await self.__Clear_Screen()

            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]       SELECT THE VIDEO RESOLUTION      [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]                                        [][]")
            print("[][]         ['144p', '360p', '720p']       [][]")
            print("[][]                                        [][]")
            print("[][]                                        [][]")
            print("[][]                                        [][]")
            print("[][]  ENTER '_BACK' TO CANCEL THE DOWNLOAD  [][]")
            print("[][]                                        [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Module_Not_Found_Error(self):
        try:
            await self.__Clear_Screen()

            print("|||||||||||||||||||||||||||||||||||||||||")
            print("[][]       PYTUBE NOT INSTALLED      [][]")
            print("|||||||||||||||||||||||||||||||||||||||||")
            print("[][]                                 [][]")
            print("[][]      [ ENTER COMMAND ]          [][]")
            print("[][]                                 [][]")
            print("[][] 'python -m pip install pytube'  [][]")
            print("[][]                                 [][]")
            print("[][]            OR                   [][]")
            print("[][]                                 [][]")
            print("[][] 'python3 -m pip install pytube' [][]")
            print("|||||||||||||||||||||||||||||||||||||||||")
            print("|||||||||||||||||||||||||||||||||||||||||")
            print("[][]      PRESS ANY KEY TO EXIT      [][]")
            print("|||||||||||||||||||||||||||||||||||||||||\n\n")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Path_Not_Found_Error(self):
        try:
            await self.__Clear_Screen()

            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][] PATH NOT FOUND. YOU HAVE ENTERED THE WRONG PATH [][]")
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]              PRESS ANY KEY TO EXIT              [][]")
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Age_Restriction_Error(self):
        try:
            await self.__Clear_Screen()

            print("|||||||||||||||||||||||||||||||||||||")
            print("[][] THE VIDEO IS AGE RESTRICTED [][]")
            print("|||||||||||||||||||||||||||||||||||||")
            print("|||||||||||||||||||||||||||||||||||||")
            print("[][]   PRESS ANY KEY TO EXIT     [][]")
            print("|||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __An_Unknown_Error_Occurred(self):
        try:
            await self.__Clear_Screen()

            print("|||||||||||||||||||||||||||||||")
            print("[][]     UNKNOWN ERROR     [][]")
            print("|||||||||||||||||||||||||||||||")
            print("|||||||||||||||||||||||||||||||")
            print("[][] PRESS ANY KEY TO EXIT [][]")
            print("|||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Wrong_Link_Error_Occurred(self):
        try:
            await self.__Clear_Screen()

            print("||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][] YOU HAVE ENTERED AN INVALID YOUTUBE LINK [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]           PRESS ANY KEY TO EXIT          [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __File_Successfully_Installed_Message(self):
        try:
            await self.__Clear_Screen()

            print("|||||||||||||||||||||||||||||||||||||")
            print("[][] FILE SUCCESSFULLY INSTALLED [][]")
            print("|||||||||||||||||||||||||||||||||||||")
            print("|||||||||||||||||||||||||||||||||||||")
            print("[][]    PRESS ANY KEY TO EXIT    [][]")
            print("|||||||||||||||||||||||||||||||||||||")

            selected_input = input("\n\n[ _ ] Input: ")

            return selected_input
        except KeyboardInterrupt:
            sys.exit(0)

    async def __Video_Downloading_Warning(self):
        try:
            await self.__Clear_Screen()

            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]      [ ! ! ! ]      WARNING     [ ! ! ! ]      [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]              VIDEO IS DOWNLOADING              [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("[][]  [ ! ! ! ] DO NOT CLOSE THE PROGRAM [ ! ! ! ]  [][]")
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n\n\n")

        except KeyboardInterrupt:
            sys.exit(0)
