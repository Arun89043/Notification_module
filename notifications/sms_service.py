def send_notification_sms(user, message):
    
    print("📱 SMS SERVICE STARTED")

    phone = getattr(user, "phone_number", None)

    if phone:
        print(f"To: {phone}")
    else:
        print("⚠️ No phone number found, sending to user only")

    print(f"User: {user.username}")
    print(f"Message: {message}")
    print("---------------------------")

    return True