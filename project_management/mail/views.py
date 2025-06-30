from flask import  render_template, flash, redirect, url_for,Blueprint,request
from flask_mail import Mail, Message
from  project_management.mail.forms import ContactForm
from project_management import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'surendrareddymandala@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyqumnevpwewrauz'
mail = Mail(app)
email=Blueprint('email',__name__)

@email.route('/contact', methods=['GET', 'POST'])
def contact_form():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            subject=form.subject.data,
            sender=form.email.data,
            recipients=['surendrareddymandala@gmail.com'],
            body=(
                f"Name:   {form.name.data}\n"
                f"Email:  {form.email.data}\n"
                f"Mobile: {form.mobile.data}\n\n"
                f"Message:\n{form.query.data}"
            )
        )
        try:
            mail.send(msg)
            # Use query‑string flag instead of flash
            return redirect(url_for('email.contact_form', success='1'))
        except Exception as e:
            # Optional: pass error via query too
            return redirect(url_for('email.contact_form', error=str(e)))

    # Render page (GET or failed POST)
    success = request.args.get('success')
    error   = request.args.get('error')
    return render_template('form.html', form=form,
                           success=success, error=error)
