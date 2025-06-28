import subprocess
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INIT_FLAG = ".initialized"

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("🧠 Initializing rfbrowser (playwright)...")
    subprocess.run(["rfbrowser", "init"], check=True)
    with open(INIT_FLAG, "w") as f:
        f.write("done")
    print("✅ Dependencies installed and initialization complete.")

def send_email(available_products):
    print("📧 Sending email...")
    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    recipient = sender

    subject = "✅ Amul Product Availability Update"
    body = "Good news! 🎉\n\nThe following Amul products are now IN STOCK:\n"
    for product in available_products:
        url_name = product.lower().replace(" ", "-").replace(",", "").replace("|", "").replace("--", "-").replace("ml-", "ml-or-")
        body += f"👉 {product}\n🔗 https://shop.amul.com/en/product/{url_name}\n\n"

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
    result = subprocess.run(["robot", "-d", "Results", "amul.robot"], capture_output=True, text=True)
    print(result.stdout)

    available_products = []
    for line in result.stdout.splitlines():
        if "✅" in line and "available for purchase" in line:
            product = line.split("✅")[1].split(" is")[0].strip()
            available_products.append(product)

    if available_products:
        print("📦 Available products found:", available_products)
        send_email(available_products)
    else:
        print("❌ No products are available.")

    return result.returncode

if __name__ == "__main__":
    if not os.path.exists(INIT_FLAG):
        install_dependencies()
    exit_code = run_robot()
    sys.exit(exit_code)
