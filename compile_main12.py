from pathlib import Path
import py_compile
p = Path('c:/Users/Gehas/Desktop/web pt/2026 portfolio website/main_12.py')
py_compile.compile(str(p), doraise=True)
print('compiled successfully')
