import cx_Freeze
executables = [cx_Freeze.Executable("chase.py")]
cx_Freeze.setup(
    name="Chase",
    options={"build.exe":{"packages":["pygame"],"include_files":["background.png","cookie.png","enemy.png","mainchar.png"]}},
    description="Avoid the enemy while trying to eat cookies in Chase!",
    executables=executables
)