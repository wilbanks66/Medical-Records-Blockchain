import hashlib
import json
from datetime import datetime


class MedicalRecordBlock:
    def __init__(self, index, timestamp, patient_name, age, diagnosis, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.patient_name = patient_name
        self.age = age
        self.diagnosis = diagnosis
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + self.patient_name + str(self.age) + self.diagnosis + self.previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()


class MedicalRecordChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return MedicalRecordBlock(0, datetime.now(), "Doug Wilbanks", 35, "None", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


class MedicalEvent:
    def __init__(self, patient_id, event_type, event_date, event_details):
        self.patient_id = patient_id
        self.event_type = event_type
        self.event_date = event_date
        self.event_details = event_details


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.now(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = datetime.now()
        previous_hash = previous_block.hash
        new_block = Block(index, timestamp, data, previous_hash)
        self.chain.append(new_block)

    def get_chain(self):
        return self.chain


class MedicalRecord:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.blockchain = Blockchain()

    def add_medical_event(self, event_type, event_date, event_details):
        medical_event = MedicalEvent(self.patient_id, event_type, event_date, event_details)
        self.blockchain.add_block(medical_event.__dict__)

    def get_medical_history(self):
        chain = self.blockchain.get_chain()
        medical_history = []
        for block in chain:
            if block.data["patient_id"] == self.patient_id:
                medical_history.append(MedicalEvent(**block.data))
        return medical_history
