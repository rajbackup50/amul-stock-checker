def send_email(available_products):
    print("📧 Sending email...")

    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    recipient = sender

    subject = "✅ Amul Products Available!"
    body = "Good news! 🎉\n\nThe following Amul products are now IN STOCK:\n\n"

    for product in available_products:
        url_slug = product.lower().replace(",", "").replace("|", "").replace("  ", " ").replace(" ", "-")
        url = f"https://shop.amul.com/en/product/{url_slug}"
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
    for line in result.stdout.splitlines():
        if "Yay!" in line:
            product_line = line.strip().replace("Yay! ", "").replace(" is available for purchase", "")
            available_products.append(product_line)

    if available_products:
        print(f"✅ Found {len(available_products)} product(s) in stock.")
        send_email(available_products)
    elif "Broke my heart" in result.stdout:
        print("❌ All products are currently sold out.")
    else:
        print("⚠️ Could not determine product availability. Please check manually.")

    return result.returncode
