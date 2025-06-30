from flask import  render_template, flash, redirect, url_for,Blueprint
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
        msg = Message(subject=f"{form.subject.data}",
                      sender=form.email.data,
                      recipients=['surendrareddymandala@gmail.com'],
                      body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMobile Nuber :{form.mobile.data}\nQuery:\n{form.query.data}")
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message: {str(e)}', 'danger')
        return redirect(url_for('email.contact_form'))
    return render_template('form.html', form=form)
