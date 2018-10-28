import json
import datetime
import time
from web3 import Web3, HTTPProvider
from settings import *

class Contract:
    DEFAULT_GAS_PRICE = 21000000000
    DEFAULT_GAS = 1000000

    web3 = Web3(HTTPProvider(INFURA_LINK))

    def __init__(self):
        contractAddress = Web3.toChecksumAddress(CONTRACT_ADDRESS)
        with open('ehr.json', 'r') as abiDefinition:
            abiStorage = json.load(abiDefinition)
        self.publicKey = Web3.toChecksumAddress(PUBLIC_KEY)
        self.privateKey = PRIVATE_KEY
        self.contract = self.web3.eth.contract(
            address = contractAddress,
            abi = abiStorage
        )

    def _buildTx(self):
        tx = self.contract.buildTransaction({
            'gasPrice': self.DEFAULT_GAS_PRICE,
            'gas': self.DEFAULT_GAS,
            'nonce': self.web3.eth.getTransactionCount(self.publicKey)
        })
        return tx

    def _ethTransaction(self, tx):
        signed = self.web3.eth.account.signTransaction(
            tx,
            private_key = self.privateKey
        )
        result = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = None
        while receipt == None:
            receipt = self.web3.eth.getTransactionReceipt(result)
        if receipt.get('status') == 1:
            return True
        else:
            return False

class EHR(Contract):
    def newUser(self, userAddress, firstNameCapsule, lastNameCapsule, dateOfBirthCapsule, firstName, lastName, dateOfBirth):
        tx = self._buildTx().newUser(userAddress, firstNameCapsule, lastNameCapsule, dateOfBirthCapsule, firstName, lastName, dateOfBirth)
        self._ethTransaction(tx)

    def addDisease(self, userAddress, diseaseTimestampCapsule, diagnosisCapsule, therapyCapsule, diseaseTimestamp, diagnosis, therapy):
        nowTimestamp = Web3.sha3(self._getNowTimestamp())
        tx = self._buildTx().addDisease(userAddress, diseaseTimestampCapsule, diagnosisCapsule, therapyCapsule, nowTimestamp, diseaseTimestamp, diagnosis, therapy)
        self._ethTransaction(tx)

    def updateDisease(self, userAddress, historyTimestampCapsule, messageCapsule, diseaseTimestamp, historyTimestamp, message):
        nowTimestamp = Web3.sha3(self._getNowTimestamp())
        tx = self._buildTx().updateDisease(userAddress, historyTimestampCapsule, messageCapsule, diseaseTimestamp, nowTimestamp, historyTimestamp, message)
        self._ethTransaction(tx)

    # def updateDisease(self, userAddress, diseaseTimestamp, result):
    #     tx = self._buildTx().closeDisease(userAddress, diseaseTimestamp, result)
    #     self._ethTransaction(tx)

    def getUser(self, userAddress):
        user = self.contract.call().users(userAddress)
        return user

    def getDiseasesTimestamps(self, userAddress):
        diseasesTimestamps = self.contract.call().getDiseasesTimestamps(userAddress)
        return diseasesTimestamps

    def getDisease(self, userAddress, diseaseTimestamp):
        disease = self.contract.call().diseases(userAddress, diseaseTimestamp)
        return disease

    def getHistorysTimestamps(self, userAddress, diseaseTimestamp):
        historysTimestamps = self.contract.call().getHistorysTimestamps(userAddress, diseaseTimestamp)
        return historysTimestamps

    def getHistorys(self, userAddress, diseaseTimestamp, historyTimestamp):
        historys = self.contract.call().historys(userAddress, diseaseTimestamp, historyTimestamp)
        return historys

    def _getNowTimestamp(self):
        timestamp = time.mktime(datetime.datetime.today().timetuple())
        return int(timestamp)
