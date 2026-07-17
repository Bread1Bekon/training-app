from app.consumers.form_consumer import FormNotificationConsumer

if __name__ == "__main__":
    worker = FormNotificationConsumer()
    worker.start()