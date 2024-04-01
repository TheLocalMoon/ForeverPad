from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["os"],
    "include_files": ["constants.py", "pdk.py", "plugins", "settings_window.py", "translate.json"]
}

setup(
    name="ForeverPad",
    version="0.1",
    description="\"Better than Notepad++!\"",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)]
)