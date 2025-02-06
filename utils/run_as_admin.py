import sys
import os
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join([sys.argv[0]] + sys.argv[1:]),
            None, 
            1
        )
        sys.exit()

if __name__ == "__main__":
    # Check if running as admin, if not, restart with admin rights
    if not is_admin():
        run_as_admin()
    else:
        # Start the AI Implementer with admin rights
        subprocess.run([sys.executable, "ai_implementer.py"])