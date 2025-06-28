import subprocess
import sys

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("🧠 Initializing rfbrowser (playwright)...")
    subprocess.run(["rfbrowser", "init", "--skip-browser-download"], check=True)
    subprocess.run(["playwright", "install", "chromium"], check=True)

def run_robot():
    print("🤖 Running amul.robot...")
    result = subprocess.run(["robot", "amul.robot"], capture_output=True, text=True)
    
    # Print full Robot output for debugging/logging
    print(result.stdout)
    
    # Parse meaningful result from robot console logs
    if "Yay! The product is available for purchase" in result.stdout:
        print("✅ Product is IN STOCK! Order now!")
    elif "Broke my heart, the product is sold out" in result.stdout:
        print("❌ Product is SOLD OUT at the moment.")
    else:
        print("⚠️ Could not determine product availability. Please check manually.")

    return result.returncode

if __name__ == "__main__":
    install_dependencies()
    exit_code = run_robot()
    sys.exit(exit_code)
