
import subprocess, sys

packages = ["pandas", "scikit-learn", "flask", "flask-cors", "requests", "numpy"]

def install(package):
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except:
        print(f"Failed to install {package}. Try running: pip install {package}")

for p in packages: install(p)
print("\n✅ Setup Complete! Ready for Step 3.")