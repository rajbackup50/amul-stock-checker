import subprocess
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INIT_FLAG = ".initialized"  # Hidden file used to track first-time setup

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("🧠 Initializing rfbrowser (playwright)...")
    subprocess.run(["rfbrowser", "init"], check=True)

    # Mark setup as completed
    with open(INIT_FLAG, "w") as f:
        f.write("done")
    print("✅ Dependencies installed and initialization complete.")

def send_email():
    print("📧 Sending email...")

    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    recipient = sender

    subject = "✅ Amul Product Available!"
    body = (
        "Good news! 🎉\n\n"
        "The Amul High Protein Buttermilk is now IN STOCK!\n"
        "👉 https://shop.amul.com/en/amul-high-protein-buttermilk-200-ml-or-pack-of-30"
    )

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

    print("✅ Email sent.")

def run_robot():
    print("🤖 Running amul.robot...")
    result = subprocess.run(["robot","-d","Results","amul.robot"], capture_output=True, text=True)
    print(result.stdout)

    if "Yay! The product is available for purchase" in result.stdout:
        print("✅ Product is IN STOCK! Sending email...")
        send_email()
    elif "Broke my heart, the product is sold out" in result.stdout:
        print("❌ Product is SOLD OUT at the moment.")
    else:
        print("⚠️ Could not determine product availability. Please check manually.")

    return result.returncode

if __name__ == "__main__":
    if not os.path.exists(INIT_FLAG):
        install_dependencies()
    exit_code = run_robot()
    sys.exit(exit_code)
