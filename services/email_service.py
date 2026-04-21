import smtplib

def send_email(to_email, message):

    sender_email = "ishika.jindal0907@gmail.com"
    password = "sxluvpupnyaiarek"

    try:
        print("Connecting to Gmail...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(sender_email, password)
        
        print("Sending email...")
        
        email_text = f"Subject: Bank Assistant Response\n\n{message}"
        
        server.sendmail(sender_email, to_email, email_text)
        
        server.quit()
        
        print("Email sent successfully")
    
    except Exception as e:
        print("Error:", e)


# TEST
if __name__ == "__main__":
    
    send_email(
        "ishika.jindal907@gmail.com",
        "Your balance is Rs 50000"
    )