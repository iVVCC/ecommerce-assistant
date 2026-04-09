import sys
import os

if __name__ == "__main__":
    import subprocess
    # 使用新的虚拟环境运行streamlit
    streamlit_path = os.path.join("new_venv", "Scripts", "streamlit.exe")
    subprocess.run([streamlit_path, "run", "src/frontend/app.py"])
