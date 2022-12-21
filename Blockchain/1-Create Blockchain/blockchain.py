import datetime
import  hashlib
import json
from flask import Flask, jsonify


#part-1 Building Blockchain
class blockchain:

    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash='0')

    def createBlock(self, proof, previousHash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash}
        self.chain.append(block)
        return block

    def getPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(
                str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] =='0000':
                checkProof = True
            else:
                newProof += 1
        return newProof

    def hash(self, block):
        encodedBlock  = json.dumps(block).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(
                str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            previousBlock = block
            blockIndex += 1
        return True


# part 2- Mining our Blockchain

# Creating web app
app = Flask(__name__)


#creating blockchain
bc = blockchain()


#Mining a new block
@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    previousBlock = bc.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = bc.proofOfWork(previousProof)
    previousHash = bc.hash(previousBlock)
    block = bc.createBlock(proof, previousHash)
    response = {'message': 'Congratulations, you just mined a block',
                'index': block['index'],
                'proof': block['proof'],
                'previousHash': block['previousHash'],
                'timestamp': block['timestamp'],}
    return jsonify(response), 200


# Getting our full blockchain
@app.route('/getChain', methods = ['GET'])
def getChain():
    response = {'chain': bc.chain,
                'length': len(bc.chain)}
    return jsonify(response), 200


# Check if blockchain is valid
@app.route('/isValid', methods = ['GET'])
def isValid():
    isvalid = bc.isChainValid(bc.chain)
    if isValid:
        response = {'message':'The blockchain is valid'}
    else: 
        response = {'message':'The blockchain is not valid'}
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0',port = 5000)