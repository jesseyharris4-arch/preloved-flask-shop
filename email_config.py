from flask_mail import Mail

def init_mail(app):
    # Afrihost Email Hosting SMTP settings
    app.config['MAIL_SERVER'] = 'galloway.aserv.email'   # Afrihost SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'hello@prelovedlittlesandbigs.co.za'
    app.config['MAIL_PASSWORD'] = 'Prelovedlittlesandbigs1*'
    app.config['MAIL_DEFAULT_SENDER'] = 'hello@prelovedlittlesandbigs.co.za'

    mail = Mail(app)
    return mail
