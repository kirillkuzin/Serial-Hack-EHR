import umbral
import time
from umbral import pre, keys, signing, curve, params
from ethereum_core import EHR
from web3 import Web3

class Core():
    def __init__(self, privateKey = None):
        # umbral.config.set_default_curve()
        self.ehr = EHR()
        curveVar = curve.Curve(714)
        paramsVar = params.UmbralParameters(curveVar)
        if privateKey is None:
            self.privateKey = keys.UmbralPrivateKey.gen_key(params = paramsVar)
            self.privateKeyBytes = self.privateKey.to_bytes()
        else:
            self.privateKeyBytes = privateKey
            self.privateKey = keys.UmbralPrivateKey.from_bytes(key_bytes = self.privateKeyBytes)
        self.publicKey = self.privateKey.get_pubkey()

    def newUser(self, userAddress, firstName, lastName, dateOfBirth):
        userAddress = Web3.toChecksumAddress(userAddress)
        firstName, firstNameCapsule = pre.encrypt(self.publicKey, firstName)
        lastName, lastNameCapsule = pre.encrypt(self.publicKey, lastName)
        dateOfBirth, dateOfBirthCapsule = pre.encrypt(self.publicKey, dateOfBirth)
        firstNameCapsule = firstNameCapsule.to_bytes()
        lastNameCapsule = lastNameCapsule.to_bytes()
        dateOfBirthCapsule = dateOfBirthCapsule.to_bytes()
        self.ehr.newUser(userAddress, firstNameCapsule, lastNameCapsule, dateOfBirthCapsule, firstName, lastName, dateOfBirth)

    def addDisease(self, userAddress, diagnosis, therapy):
        userAddress = Web3.toChecksumAddress(userAddress)
        diseaseTimestamp = time.time()
        diseaseTimestamp = str(diseaseTimestamp).split('.')[0]
        diseaseTimestamp = bytes(diseaseTimestamp, encoding='utf-8')
        diagnosis, diagnosisCapsule = pre.encrypt(self.publicKey, diagnosis)
        therapy, therapyCapsule = pre.encrypt(self.publicKey, therapy)
        diseaseTimestamp, diseaseTimestampCapsule = pre.encrypt(self.publicKey, diseaseTimestamp)
        diagnosisCapsule = diagnosisCapsule.to_bytes()
        therapyCapsule = therapyCapsule.to_bytes()
        diseaseTimestampCapsule = diseaseTimestampCapsule.to_bytes()
        self.ehr.addDisease(userAddress, diseaseTimestampCapsule, diagnosisCapsule, therapyCapsule, diseaseTimestamp, diagnosis, therapy)

    def updateDisease(self, userAddress, diseaseTimestamp, message):
        userAddress = Web3.toChecksumAddress(userAddress)
        historyTimestamp = time.time()
        historyTimestamp = str(historyTimestamp).split('.')[0]
        historyTimestamp = bytes(historyTimestamp, encoding='utf-8')
        historyTimestamp, historyTimestampCapsule = pre.encrypt(self.publicKey, historyTimestamp)
        message, messageCapsule = pre.encrypt(self.publicKey, message)
        historyTimestamp = historyTimestamp.to_bytes()
        messageCapsule = messageCapsule.to_bytes()
        self.ehr.updateDisease(userAddress, historyTimestampCapsule, messageCapsule, diseaseTimestamp, historyTimestamp, message)

    def getUser(self, userAddress):
        userAddress = Web3.toChecksumAddress(userAddress)
        user = self.ehr.getUser(userAddress)
        curveVar = curve.Curve(714)
        paramsVar = params.UmbralParameters(curveVar)
        firstNameCapsule = pre.Capsule.from_bytes(user[0], paramsVar)
        lastNameCapsule = pre.Capsule.from_bytes(user[1], paramsVar)
        dateOfBirthCapsule = pre.Capsule.from_bytes(user[2], paramsVar)
        firstName = pre.decrypt(
            ciphertext = user[3],
            capsule = firstNameCapsule,
            decrypting_key = self.privateKey
        )
        lastName = pre.decrypt(
            ciphertext = user[4],
            capsule = lastNameCapsule,
            decrypting_key = self.privateKey
        )
        dateOfBirth = pre.decrypt(
            ciphertext = user[5],
            capsule = dateOfBirthCapsule,
            decrypting_key = self.privateKey
        )
        firstName = firstName.decode('utf-8')
        lastName = lastName.decode('utf-8')
        dateOfBirth = dateOfBirth.decode('utf-8')
        return firstName, lastName, dateOfBirth

    def getDiseasesTimestamps(self, userAddress):
        userAddress = Web3.toChecksumAddress(userAddress)
        diseasesTimestamps = self.ehr.getDiseasesTimestamps(userAddress)
        return diseasesTimestamps

    def getAllDiseases(self, userAddress):
        userAddress = Web3.toChecksumAddress(userAddress)
        diseasesTimestamps = self.getDiseasesTimestamps(userAddress)
        curveVar = curve.Curve(714)
        paramsVar = params.UmbralParameters(curveVar)
        diseases = []
        for diseaseTimestamp in diseasesTimestamps:
            disease = self.ehr.getDisease(userAddress, diseaseTimestamp)
            diagnosisCapsule = pre.Capsule.from_bytes(disease[3], paramsVar)
            therapyCapsule = pre.Capsule.from_bytes(disease[4], paramsVar)
            diagnosis = pre.decrypt(
                ciphertext = disease[5],
                capsule = diagnosisCapsule,
                decrypting_key = self.privateKey
            )
            therapy = pre.decrypt(
                ciphertext = disease[6],
                capsule = therapyCapsule,
                decrypting_key = self.privateKey
            )
            diseaseEncrypted = {
                'diagnosis': diagnosis.decode('utf-8'),
                'therapy': therapy.decode('utf-8')
            }
            diseases.append(diseaseEncrypted)
        return diseases
