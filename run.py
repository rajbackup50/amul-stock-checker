import subprocess
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import io
import re

# Ensure UTF-8 output (especially for emojis)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INIT_FLAG = ".initialized"  # File to mark first-time setup complete

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

    subject = "✅ Amul Products Available!"
    body = "Good news! 🎉\n\nThe following Amul products are now IN STOCK:\n\n"

    for product in available_products:
        # Generate clean slug from product name
        slug = product.lower()
        slug = slug.replace(",", "")
        slug = slug.replace("|", "or")  # ✅ replace | with 'or' to match actual URL
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip("-")
        url = f"https://shop.amul.com/en/product/{slug}"
        body += f"• {product}\n👉 {url}\n\n"

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

    # Check lines for "Yay! <product> is available for purchase"
    for line in result.stdout.splitlines():
        match = re.search(r"Yay!\s*(.*?)\s*is available for purchase", line)
        if match:
            product_name = match.group(1).strip()
            available_products.append(product_name)

    if available_products:
        print(f"✅ Found {len(available_products)} product(s) in stock.")
        send_email(available_products)
    elif "Broke my heart" in result.stdout:
        print("❌ All products are currently sold out.")
    else:
        print("⚠️ Could not determine product availability. Please check manually.")

    return result.returncode

if __name__ == "__main__":
    if not os.path.exists(INIT_FLAG):
        install_dependencies()
    exit_code = run_robot()
    sys.exit(exit_code)
