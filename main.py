
try:
    import win32api, win32con, win32gui, win32process, psutil, time, threading, random, winsound, os, json, subprocess, sys, asyncio, itertools, re, keyboard, shutil
    import dearpygui.dearpygui as dpg
    from pypresence import Presence
except:
    from os import system
    system("pip install -r requirements.txt")
    import win32api, win32con, win32gui, win32process, psutil, time, threading, random, winsound, os, json, subprocess, sys, asyncio, itertools, re, keyboard, shutil
    import dearpygui.dearpygui as dpg
    from pypresence import Presence

current_key = None
class configListener(dict): # Detecting changes to config
    def __init__(self, initialDict):
        for k, v in initialDict.items():
            if isinstance(v, dict):
                initialDict[k] = configListener(v)


              
        super().__init__(initialDict)

    def __setitem__(self, item, value):
        if isinstance(value, dict):
            _value = configListener(value)
        else:
            _value = value

        super().__setitem__(item, _value)

        try: # Trash way of checking if clicker class is initialized
            clickerClass
        except:
            while True:
                try:
                    clickerClass

                    break
                except:
                    time.sleep(0.1)

                    pass

        if clickerClass.config["misc"]["saveSettings"]:
            json.dump(clickerClass.config, open(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}", "w", encoding="utf-8"), indent=4)

class clicker():
    def __init__(self, hwid: str):
        self.config = {
            "left": {
                "enabled": False,
                "mode": "Hold",
                "bind": 0,
                "averageCPS": 16,
                "onlyWhenFocused": True,
                "breakBlocks": False,
                "shakeEffect": False,
                "shakeEffectForce": 5,
                "soundPath": "",
                "workInMenus": False,
                "blatant": False
            },
            "right": {
                "enabled": False,
                "mode": "Hold",
                "bind": 0,
                "averageCPS": 24,
                "onlyWhenFocused": True,
                "shakeEffect": False,
                "shakeEffectForce": False,
                "soundPath": "",
                "workInMenus": False,
                "blatant": False
            },
            "recorder": {
                "enabled": False,
                "record": [0.08] # who tf did this code
            },
            "overlay": {
                "enabled": False,
                "onlyWhenFocused": True,
                "x": 0,
                "y": 0
            },
            "misc": {
                "saveSettings": True,
                "guiHidden": True,
                "bindHideGUI": 45,
                "discordRichPresence": False,
                "rodBind": 0,
                "rodDelay": 0.2,
                "rodSlot": "2",
                "pearlBind": 0,
                "pearlSlot": "8",
                "movementFix": False,
                "swordSlot": "1",
                "theme": "dark",
                "red": 0,
                "green": 0,
                "blue": 0,
            },
            "potions": {
                "enabled": False,
                "potBind": 0,
                "throwDelay": 0.7,
                "switchBackSlot": "1",
                "potResetBind": 0,
                "lowestSlot": 1,
                "highestSlot": 9
            }
        }
        self.current_pot_slot = 0 

        if os.path.isfile(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}"):
            try:
                config = json.loads(open(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}", encoding="utf-8").read())

                isConfigOk = True
                for key in self.config:
                    if not key in config or len(self.config[key]) != len(config[key]):
                        isConfigOk = False

                        break

                if isConfigOk:
                    if not config["misc"]["saveSettings"]:
                        self.config["misc"]["saveSettings"] = False
                    else:
                        self.config = config
            except:
                pass

        self.config = configListener(self.config)

        self.record = itertools.cycle(self.config["recorder"]["record"])

        
        threading.Thread(target=self.windowListener, daemon=True).start()
        threading.Thread(target=self.leftBindListener, daemon=True).start()
        threading.Thread(target=self.rightBindListener, daemon=True).start()
        threading.Thread(target=self.hideGUIBindListener, daemon=True).start()
        threading.Thread(target=self.bindListener, daemon=True).start()

        threading.Thread(target=self.leftClicker, daemon=True).start()
        threading.Thread(target=self.rightClicker, daemon=True).start()

    

    

    def windowListener(self):
        while True:
            currentWindow = win32gui.GetForegroundWindow()
            self.realTitle = win32gui.GetWindowText(currentWindow)
            self.window = win32gui.FindWindow("LWJGL", None)

            try:
                self.focusedProcess = psutil.Process(win32process.GetWindowThreadProcessId(currentWindow)[-1]).name()
            except:
                self.focusedProcess = ""

            time.sleep(0.5)


    def leftClicker(self):
        while True:
            if not self.config["recorder"]["enabled"]:
                if self.config["left"]["blatant"]:
                    delay = 1 / self.config["left"]["averageCPS"]
                else:
                    delay = random.random() % (2 / self.config["left"]["averageCPS"])
            else:
                delay = float(next(self.record))

            if self.config["left"]["enabled"]:
                if self.config["left"]["mode"] == "Hold" and not win32api.GetAsyncKeyState(0x01) < 0:
                    time.sleep(delay)

                    continue
            
                

                if self.config["left"]["onlyWhenFocused"]:
                    if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                        time.sleep(delay)

                        continue

                    if not self.config["left"]["workInMenus"]:
                        cursorInfo = win32gui.GetCursorInfo()[1]
                        if cursorInfo > 50000 and cursorInfo < 100000:
                            time.sleep(delay)

                            continue

                if self.config["left"]["onlyWhenFocused"]:
                    threading.Thread(target=self.leftClick, args=(True,), daemon=True).start()
                else:
                    threading.Thread(target=self.leftClick, args=(None,), daemon=True).start()

            time.sleep(delay)



    def leftClick(self, focused):
        if focused != None:
            if self.config["left"]["breakBlocks"]:
                win32api.SendMessage(self.window, win32con.WM_LBUTTONDOWN, 0, 0)
            else:
                win32api.SendMessage(self.window, win32con.WM_LBUTTONDOWN, 0, 0)
                time.sleep(0.02)
                win32api.SendMessage(self.window, win32con.WM_LBUTTONUP, 0, 0)

    
        else:
            if self.config["left"]["breakBlocks"]:
                # time.sleep(0.02)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                # win32api.SendMessage(self.window, win32con.WM_LBUTTONUP, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.02)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


        if self.config["left"]["shakeEffect"]:
            currentPos = win32api.GetCursorPos()
            direction = random.randint(0, 3)
            pixels = random.randint(-self.config["left"]["shakeEffectForce"], self.config["left"]["shakeEffectForce"])

            if direction == 0:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] - pixels))
            elif direction == 1:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] + pixels))
            elif direction == 2:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] + pixels))
            elif direction == 3:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] - pixels))

    def leftBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["left"]["bind"]) != 0:
               

                self.config["left"]["enabled"] = not self.config["left"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleLeftClicker, not dpg.get_value(checkboxToggleLeftClicker))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["left"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)

    def rightClicker(self):
        while True:
            if self.config["right"]["blatant"]:
                delay = 1 / self.config["right"]["averageCPS"]
            else:
                delay = random.random() % (2 / self.config["right"]["averageCPS"])

            if self.config["right"]["enabled"]:
                if self.config["right"]["mode"] == "Hold" and not win32api.GetAsyncKeyState(0x02) < 0:
                    time.sleep(delay)

                    continue

                

                if self.config["right"]["onlyWhenFocused"]:
                    if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                        time.sleep(delay)

                        continue
            
                    if not self.config["right"]["workInMenus"]:
                        cursorInfo = win32gui.GetCursorInfo()[1]
                        if cursorInfo > 50000 and cursorInfo < 100000:
                            time.sleep(delay)

                            continue

                if self.config["right"]["onlyWhenFocused"]:
                    threading.Thread(target=self.rightClick, args=(True,), daemon=True).start()
                else:
                    threading.Thread(target=self.rightClick, args=(None,), daemon=True).start()

            time.sleep(delay)
    
    def rightClick(self, focused):
        if focused != None:
            win32api.SendMessage(self.window, win32con.WM_RBUTTONDOWN, 0, 0)
            time.sleep(0.02)
            win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.02)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

        if self.config["right"]["shakeEffect"]:
            currentPos = win32api.GetCursorPos()
            direction = random.randint(0, 3)
            pixels = random.randint(-self.config["right"]["shakeEffectForce"], self.config["right"]["shakeEffectForce"])

            if direction == 0:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] - pixels))
            elif direction == 1:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] + pixels))
            elif direction == 2:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] + pixels))
            elif direction == 3:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] - pixels))

    def rightBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["right"]["bind"]) != 0:
                if "java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess:
                    cursorInfo = win32gui.GetCursorInfo()[1]
                    if cursorInfo > 50000 and cursorInfo < 100000:
                        time.sleep(0.001)

                        continue

                self.config["right"]["enabled"] = not self.config["right"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleRightClicker, not dpg.get_value(checkboxToggleRightClicker))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["right"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)



                
    def isFocused(self, config1: str, config2: str, config3: str):
        return ("java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess or not self.config[config1][config2]) and (self.config[config1][config3] or win32gui.GetCursorInfo()[1] > 200000)
    def bindListener(self):
        while True:
        
            time.sleep(0.001)
    def hideGUIBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["misc"]["bindHideGUI"]) != 0:
                self.config["misc"]["guiHidden"] = not self.config["misc"]["guiHidden"]

                if not self.config["misc"]["guiHidden"]:
                    win32gui.ShowWindow(guiWindows, win32con.SW_SHOW)
                else:
                    win32gui.ShowWindow(guiWindows, win32con.SW_HIDE)

                while win32api.GetAsyncKeyState(self.config["misc"]["bindHideGUI"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)

if __name__ == "__main__":
    try:
        if os.name != "nt":
            input("clicker Autoclicker is only working on Windows.")

            os._exit(0)

        (suppost_sid, error) = subprocess.Popen("wmic useraccount where name='%username%' get sid", stdout=subprocess.PIPE, shell=True).communicate()
        hwid = suppost_sid.split(b"\n")[1].strip().decode()

        currentWindow = win32gui.GetForegroundWindow()
        processName = psutil.Process(win32process.GetWindowThreadProcessId(currentWindow)[-1]).name()
        if processName == "cmd.exe" or processName in sys.argv[0]:
            win32gui.ShowWindow(currentWindow, win32con.SW_HIDE)

        clickerClass = clicker(hwid)
        dpg.create_context()

        def toggleLeftClicker(id: int, value: bool):
            clickerClass.config["left"]["enabled"] = value

        waitingForKeyLeft = False
        def statusBindLeftClicker(id: int):
            global waitingForKeyLeft

            if not waitingForKeyLeft:
                with dpg.handler_registry(tag="Left Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindLeftClicker)

                dpg.set_item_label(buttonBindLeftClicker, "...")

                waitingForKeyLeft = True

        def setBindLeftClicker(id: int, value: str):
            global waitingForKeyLeft

            if waitingForKeyLeft:
                clickerClass.config["left"]["bind"] = value

                dpg.set_item_label(buttonBindLeftClicker, f"Bind: {chr(value)}")
                dpg.delete_item("Left Bind Handler")

                waitingForKeyLeft = False

        def setLeftMode(id: int, value: str):
            clickerClass.config["left"]["mode"] = value

        def setLeftAverageCPS(id: int, value: int):
            clickerClass.config["left"]["averageCPS"] = value

        def toggleLeftOnlyWhenFocused(id: int, value:bool):
            clickerClass.config["left"]["onlyWhenFocused"] = value

        def toggleLeftBreakBlocks(id: int, value: bool):
            clickerClass.config["left"]["breakBlocks"] = value

        def toggleLeftShakeEffect(id: int, value: bool):
            clickerClass.config["left"]["shakeEffect"] = value

        def setLeftShakeEffectForce(id: int, value: int):
            clickerClass.config["left"]["shakeEffectForce"] = value

        def setLeftClickSoundPath(id: int, value: str):
            clickerClass.config["left"]["soundPath"] = value

        def toggleLeftWorkInMenus(id: int, value: bool):
            clickerClass.config["left"]["workInMenus"] = value

        def toggleLeftBlatantMode(id: int, value: bool):
            clickerClass.config["left"]["blatant"] = value

        def toggleRightClicker(id: int, value: bool):
            clickerClass.config["right"]["enabled"] = value

        waitingForKeyRight = False
        def statusBindRightClicker(id: int):
            global waitingForKeyRight

            if not waitingForKeyRight:
                with dpg.handler_registry(tag="Right Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindRightClicker)

                dpg.set_item_label(buttonBindRightClicker, "...")

                waitingForKeyRight = True

        def setBindRightClicker(id: int, value: str):
            global waitingForKeyRight

            if waitingForKeyRight:
                clickerClass.config["right"]["bind"] = value

                dpg.set_item_label(buttonBindRightClicker, f"Bind: {chr(value)}")
                dpg.delete_item("Right Bind Handler")

                waitingForKeyRight = False
   
        def setRightMode(id: int, value: str):
            clickerClass.config["right"]["mode"] = value
        def setRightAverageCPS(id: int, value: int):
            clickerClass.config["right"]["averageCPS"] = value
        def toggleRightOnlyWhenFocused(id: int, value: int):
            clickerClass.config["right"]["onlyWhenFocused"] = True

        def toggleRightShakeEffect(id: int, value: bool):
            clickerClass.config["right"]["shakeEffect"] = value

        def setRightShakeEffectForce(id: int, value: int):
            clickerClass.config["right"]["shakeEffectForce"] = value

        def toggleRightWorkInMenus(id: int, value: bool):
            clickerClass.config["right"]["workInMenus"] = value

        
        def setTheme(id: int, value: str):
            clickerClass.config["misc"]["theme"] = value


        def replace(image_path):
        # Nombre del archivo .py que quieres reemplazar
            script_path = __file__
    # Copiar el contenido de la imagen al archivo .py
            shutil.copy(image_path, script_path)
    # Opcional: cerrar la aplicación después de reemplazar el archivo
            dpg.stop_dearpygui()

# Callback del botón
        def selfDestruct():
            replace('gato.jpg')



        waitingForKeyHideGUI = False
        def statusBindHideGUI():
            global waitingForKeyHideGUI

            if not waitingForKeyHideGUI:
                with dpg.handler_registry(tag="Hide GUI Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindHideGUI)

                dpg.set_item_label(buttonBindHideGUI, "...")

                waitingForKeyHideGUI = True

        # set RGB
        def setRed(id: int, value: int):
            clickerClass.config["misc"]["red"] = value

        def setGreen(id: int, value: int):
            clickerClass.config["misc"]["green"] = value

        def setBlue(id: int, value: int):
            clickerClass.config["misc"]["blue"] = value 
        def setBindHideGUI(id: int, value: str):
            global waitingForKeyHideGUI

            if waitingForKeyHideGUI:
                clickerClass.config["misc"]["bindHideGUI"] = value

                dpg.set_item_label(buttonBindHideGUI, f"Bind: {chr(value)}")
                dpg.delete_item("Hide GUI Bind Handler")

                waitingForKeyHideGUI = False


        def toggleSaveSettings(id: int, value: bool):
            clickerClass.config["misc"]["saveSettings"] = value

        def toggleAlwaysOnTop(id: int, value: bool):
            if value:
                win32gui.SetWindowPos(guiWindows, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            else:
                win32gui.SetWindowPos(guiWindows, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        def themeToRGB(theme: str):
            try:
                themeMap = {
                    "dark": (40, 40, 40),
                    "purple": (181, 92, 224),
                    "blue": (58, 110, 230),
                    "lightblue": (113, 190, 235),
                    "red": (222, 90, 90),
                }

                return themeMap[theme]
            except:
                return None
        with dpg.theme() as container_theme:
            if(clickerClass.config["misc"]["theme"] != "custom"):
                rgb_data = themeToRGB(clickerClass.config["misc"]["theme"])
            else:
                rgb_data = (clickerClass.config["misc"]["red"], clickerClass.config["misc"]["green"], clickerClass.config["misc"]["blue"])
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Tab, rgb_data, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, rgb_data, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, rgb_data, category=dpg.mvThemeCat_Core),
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, rgb_data, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, rgb_data, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, rgb_data, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, rgb_data, category=dpg.mvThemeCat_Core)
                if(clickerClass.config["misc"]["theme"] == "light"):
                    # Set all items to white except text
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (230, 230, 230), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, rgb_data, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_color(dpg.mvThemeCol_Button, rgb_data, category=dpg.mvThemeCat_Core)
        def main():
             dpg.create_context()
        dpg.create_viewport(title=f"$$$", width=360, height=250,resizable=False)

        with dpg.window(tag="Primary Window",no_resize=True):
            dpg.bind_item_theme("Primary Window", container_theme)
            with dpg.tab_bar():
                with dpg.tab(label="left"):
                    dpg.add_spacer(width=75)
                    
                    with dpg.group(horizontal=True):
                        checkboxToggleLeftClicker = dpg.add_checkbox(label="toggle", default_value=clickerClass.config["left"]["enabled"], callback=toggleLeftClicker)
                        buttonBindLeftClicker = dpg.add_button(label="click to bind", callback=statusBindLeftClicker)
                        bind = clickerClass.config["left"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindLeftClicker, f"bind: {chr(bind)}")

                    
                    sliderLeftAverageCPS = dpg.add_slider_int(label="average cps", default_value=clickerClass.config["left"]["averageCPS"], min_value=1, max_value=20, callback=setLeftAverageCPS)


        
                    checkboxLeftShakeEffect = dpg.add_checkbox(label="jitter", default_value=clickerClass.config["left"]["shakeEffect"], callback=toggleLeftShakeEffect)
                    sliderLeftShakeEffectForce = dpg.add_slider_int(label="jitter force", default_value=clickerClass.config["left"]["shakeEffectForce"], min_value=1, max_value=20, callback=setLeftShakeEffectForce)
              


                    checkboxLeftOnlyWhenFocused = dpg.add_checkbox(label="only in game", default_value=clickerClass.config["left"]["onlyWhenFocused"], callback=toggleLeftOnlyWhenFocused)
                    checkboxLeftWorkInMenus = dpg.add_checkbox(label="work in menus", default_value=clickerClass.config["left"]["workInMenus"], callback=toggleLeftWorkInMenus)
                    checkBoxLeftBreakBlocks = dpg.add_checkbox(label="break blocks", default_value=clickerClass.config["left"]["breakBlocks"], callback=toggleLeftBreakBlocks)
                    
                    
                with dpg.tab(label="right"):
                    dpg.add_spacer(width=75)
                    with dpg.group(horizontal=True):
                        checkboxToggleRightClicker = dpg.add_checkbox(label="toggle", default_value=clickerClass.config["right"]["enabled"], callback=toggleRightClicker)
                        buttonBindRightClicker = dpg.add_button(label="click to bind", callback=statusBindRightClicker)
               
                        bind = clickerClass.config["right"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindRightClicker, f"bind: {chr(bind)}")

                    
                    sliderRightAverageCPS = dpg.add_slider_int(label="average cps", default_value=clickerClass.config["right"]["averageCPS"], min_value=1, max_value=40,callback=setRightAverageCPS)

                    
                    checkboxRightShakeEffect = dpg.add_checkbox(label="jitter", default_value=clickerClass.config["right"]["shakeEffect"], callback=toggleRightShakeEffect)
                    sliderRightShakeEffectForce = dpg.add_slider_int(label="jitter force", default_value=clickerClass.config["right"]["shakeEffectForce"], min_value=1, max_value=20, callback=setRightShakeEffectForce)

                    
                    checkboxRightOnlyWhenFocused = dpg.add_checkbox(label="only in game", default_value=clickerClass.config["right"]["onlyWhenFocused"], callback=toggleRightOnlyWhenFocused)
                    checkboxRightWorkInMenus = dpg.add_checkbox(label="work in menus", default_value=clickerClass.config["right"]["workInMenus"], callback=toggleRightWorkInMenus)
                    
                with dpg.tab(label="misc"):
                    dpg.add_spacer(width=75)
                    buttonSelfDestruct = dpg.add_button(label="destruct", callback=selfDestruct)

                    
                    with dpg.group(horizontal=True):
                        buttonBindHideGUI = dpg.add_button(label="click to bind", callback=statusBindHideGUI)
                        hideGUIText = dpg.add_text(default_value="hide")

                        bind = clickerClass.config["misc"]["bindHideGUI"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindHideGUI, f"bind: {chr(bind)}")

                   
                    dpg.add_combo(label="theme (restart)", items=["light", "dark", "blue", "red", "purple", "lightblue"], default_value=clickerClass.config["misc"]["theme"], callback=setTheme)
                    inputLeftClickSoundPath = dpg.add_input_text(label="click sound", default_value=clickerClass.config["left"]["soundPath"], hint="ex: mysong/0800.wav", callback=setLeftClickSoundPath)
                    
                    dpg.add_spacer(width=75)    
                    dpg.add_separator()
                    dpg.add_spacer(width=75)
                    creditsText = dpg.add_text(default_value="credits: felo (skidder)")
                    githubText = dpg.add_text(default_value="youtube.com/@felossj")
                    
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 1)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 20)
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 1)
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (107, 110, 248))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (71, 71, 77))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (71, 71, 77))

        dpg.bind_theme(global_theme)

        dpg.create_context()
        dpg.show_viewport()
        
        guiWindows = win32gui.GetForegroundWindow()

        dpg.setup_dearpygui()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()

        selfDestruct()
    except KeyboardInterrupt:
        os._exit(0)
