from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="NeuroVroom",
    version="1.0",
    description="The game aims to provide an engaging and accessible platform to assess patients' reflex and timing.",
    executables=executables
)