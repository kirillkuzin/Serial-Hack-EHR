import umbral
import time
from web3 import Web3
from flask import Flask, request, render_template
from umbral import pre, keys, signing
from ethereum_core import EHR

application = Flask(__name__)
ehr = EHR()

umbral.config.set_default_curve()

if __name__ == '__main__':
    privateKey = keys.UmbralPrivateKey.gen_key()
    publicKey = privateKey.get_pubkey()
    firstName = b'Kirill'
    lastName = b'Kirill'
    dateOfBirth = b'953373600'
    firstName, firstNameCapsule = pre.encrypt(publicKey, firstName)
    lastName, lastNameCapsule = pre.encrypt(publicKey, lastName)
    dateOfBirth, dateOfBirthCapsule = pre.encrypt(publicKey, dateOfBirth)
    ehr.newUser('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', firstName, lastName, dateOfBirth)
    user = ehr.getUser('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa')
    firstName = pre.decrypt(
        ciphertext = user[0],
        capsule = firstNameCapsule,
        decrypting_key = privateKey
    )
    lastName = pre.decrypt(
        ciphertext = user[1],
        capsule = lastNameCapsule,
        decrypting_key = privateKey
    )
    dateOfBirth = pre.decrypt(
        ciphertext = user[2],
        capsule = dateOfBirthCapsule,
        decrypting_key = privateKey
    )
    print(firstName)
    print(lastName)
    print(dateOfBirth)
    diagnosis = b'Hello'
    therapy = b'World'
    ts = time.time()
    ts = str(ts).split('.')[0]
    ts = bytes(ts, encoding='utf-8')
    diagnosis, diagnosisCapsule = pre.encrypt(publicKey, diagnosis)
    therapy, therapyCapsule = pre.encrypt(publicKey, therapy)
    ts, tsCapsule = pre.encrypt(publicKey, ts)
    diseaseTimestamp = ehr.addDisease('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', ts, diagnosis, therapy)
    disease = ehr.getDisease('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', diseaseTimestamp)
    diagnosis = pre.decrypt(
        ciphertext = disease[2],
        capsule = diagnosisCapsule,
        decrypting_key = privateKey
    )
    therapy = pre.decrypt(
        ciphertext = disease[3],
        capsule = therapyCapsule,
        decrypting_key = privateKey
    )
    print(diagnosis)
    print(therapy)
    diseasesTimestamps = ehr.getDiseasesTimestamps('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa')
    print(diseasesTimestamps)
    message = b'This is part of history of disease'
    ts = time.time()
    ts = str(ts).split('.')[0]
    ts = bytes(ts, encoding='utf-8')
    message, messageCapsule = pre.encrypt(publicKey, message)
    ts, tsCapsule = pre.encrypt(publicKey, ts)
    historyTimestamp = ehr.updateDisease('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', diseaseTimestamp, ts, message)
    historysTimestamps = ehr.getHistorysTimestamps('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', diseaseTimestamp)
    print(historysTimestamps)
    historys = ehr.getHistorys('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', diseaseTimestamp, historyTimestamp)
    print(historys)
    message = pre.decrypt(
        ciphertext = historys[2],
        capsule = messageCapsule,
        decrypting_key = privateKey
    )
    print(message)
    # user = ehr.getUser('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa')

    # print(firstName)
    # print(lastName)
    # print(dateOfBirth)
    # ehr.addDisease('0x3AEBce1ffF6CB2bB76082C964F80bd7295DbBFDa', 'Болезнь', 'Лечиться')

    # application.debug = True
    # application.run()
    # alices_private_key = keys.UmbralPrivateKey.gen_key()
    # alices_public_key = alices_private_key.get_pubkey()
    # data = b'Hi, my name is Kirill'
    # print(data)
    # ciphertext, capsule = pre.encrypt(
    #     alices_public_key,
    #     data
    # )
    # print(ciphertext)
    # cleartext = pre.decrypt(
    #     ciphertext=ciphertext,
    #     capsule=capsule,
    #     decrypting_key=alices_private_key
    # )
    # print(cleartext)
