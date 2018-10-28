from flask import Flask, request, render_template
from core import Core

application = Flask(__name__)

@application.route('/new')
def new():
    return render_template(
        'new_user.html'
    )

@application.route('/key', methods = ['POST'])
def key():
    userAddress = request.form.get('address')
    firstName = bytes(request.form.get('first_name'), encoding='utf-8')
    lastName = bytes(request.form.get('last_name'), encoding='utf-8')
    dateOfBirth = bytes(request.form.get('date'), encoding='utf-8')
    core = Core()
    core.newUser(userAddress, firstName, lastName, dateOfBirth)
    key = core.privateKeyBytes
    return render_template(
        'key.html',
        key = key
    )

@application.route('/profile')
def profile():
    key = request.args.get('key')
    userAddress = request.args.get('address')
    core = Core(privateKey = key)
    firstName, lastName, dateOfBirth = core.getUser(userAddress)
    diseases = core.getAllDiseases(userAddress)
    return render_template(
        'profile.html',
        userAddress = userAddress,
        firstName = firstName,
        lastName = lastName,
        dateOfBirth = dateOfBirth,
        diseases = diseases
    )

@application.route('/disease', methods = ['GET'])
def disease():
    key = request.args.get('key')
    userAddress = request.args.get('address')
    diagnosis = bytes(request.args.get('diagnosis'), encoding='utf-8')
    therapy = bytes(request.args.get('therapy'), encoding='utf-8')
    core = Core(privateKey = key)
    core.addDisease(userAddress, diagnosis, therapy)
    return 'Done'

if __name__ == '__main__':
    application.debug = True
    application.run()
