# This IOTA class contains the commands for communicating with a node through the HTTP API.
# All the following commands must include an HTTP header.

from __future__ import absolute_import, division, print_function, unicode_literals
import json
import urllib
import urllib.request
from iota import (
    Address,
    Iota,
    ProposedTransaction,
    Tag,
    TryteString,
    Transaction
)
import secrets
import string


class controller:
    register = None
    api_call_url = None

    # Initialize the IOTA class
    # :param register: access to all other class
    def __init__(self, register):
        self.register = register

    # Ser IOTA server URL
    # :param url: IOTA server URL
    def setApiCall(self, url):
        self.api_call_url = url

    # Send Request to URL
    # :param stringified: request body
    # :param headers: request header
    # :param url: IOTA server URL
    # :return json data that fetched from server URL
    def sendRequest(self, stringified, headers, url):

        if headers is None:
            headers = {
                'content-type': 'application/json',
                'X-IOTA-API-Version': '1'
            }

        if url is not None:
            self.api_call_url = url

        if self.api_call_url is None:
            self.api_call_url = "http://iota.av.it.pt:14265"

        request = urllib.request.Request(url=self.api_call_url, data=stringified.encode(), headers=headers)
        return_data = urllib.request.urlopen(request).read()
        return json.loads(return_data)

    # Check the consistency of transactions. A consistent transaction is one where the following statements are true:
    # The transaction isn't missing a reference transaction
    # The transaction's bundle is valid
    # The transaction's reference transactions are valid
    def checkConsistency(self, tails):
        command = {
            "command": "checkConsistency",
            "tails": tails
        }

        # Response
        # State ::State of the given transactions in the tails parameter. A true value means that all given transactions
        # are consistent. A false value means that one or more of the given transactions aren't consistent.
        # info :: If the state field is false, this field contains information about why the transaction is inconsistent
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Find transactions that contain the given values in their transaction fields. The parameters define the transaction
    # fields to search for, including bundles, addresses, tags, and approves.
    # Using multiple transaction fields, returns transactions hashes at the intersection of those values.
    def findTransactions(self, addresses):
        # Parameters
        # bundles :: Bundle hashes to search for - array of strings
        # addresses :: Addresses to search for (do not include the checksum) - array of strings
        # tags :: Tags to search for - array of strings
        # approvees :: Child transactions to search for	- array of strings
        command = {
            "command": "findTransactions",
            "addresses": addresses
        }

        # Response
        # An array of transaction hashes, is returned in the same order for all individual elements.
        # hashes :: The transaction hashes which are returned depend on your input.
        # - bundles: returns an array oftransaction hashes that contain the given bundle hash.
        # - addresses: returns an array of transaction hashes that contain the given address in the address field.
        # - tags: returns an array of transaction hashes that contain the given value in the tag field.
        # - approvees: returns an array of transaction hashes that contain the given transactions in their
        #   branchTransaction or trunkTransaction fields.
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Get the confirmed balance of an address.
    # If the tips parameter is missing, the returned balance is correct as of the latest confirmed milestone.
    def getBalances(self, addresses, threshold):
        # Parameters
        # addresses :: Address for which to get the balance (do not include the checksum) - array of strings
        # threshold :: Confirmation threshold between 0 and 100 - integer
        # tips (Optional):: Tips whose history of transactions to traverse to find the balance - array of strings
        command = {
            "command": "getBalances",
            "addresses": addresses,
            "threshold": threshold
        }

        # Response
        # balances :: Array of balances in the same order as the addresses parameters were passed to the endpoint
        # references :: The referencing tips. If no tips parameter was passed to the endpoint, this field contains
        #               the hash of the latest milestone that confirmed the balance
        # milestoneIndex :: The index of the milestone that confirmed the most recent balance
        # duration :: Number of milliseconds it took to process the request
        return self.sendRequest(json.dumps(command), None, None)

    # Get the inclusion states of a set of transactions. This endpoint determines if a transaction is confirmed
    # by the network (referenced by a valid milestone). You can search for multiple tips (and thus, milestones)
    # to get past inclusion states of transactions.
    def getInclusionStates(self, transactions, tips):
        # Parameters
        # transactions :: List of transaction hashes for which you want to get the inclusion state
        # tips (Optional) :: List of tip transaction hashes (including milestones) you want to search for
        command = {
            "command": "getInclusionStates",
            "transactions": transactions,
            "tips": tips
        }

        # Response
        # states :: List of boolean values in the same order as the transactions parameters. A true value means
        #           the transaction was confirmed
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Get information about a node.
    def getNodeInfo(self):
        command = {"command": "getNodeInfo"}
        return self.sendRequest(json.dumps(command), None, None)

    # Get tip transaction hashes from a node.
    def getTips(self):
        command = {"command": "getTips"}

        # Response
        # hashes :: Array of tip transaction hashes
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Get two consistent tip transaction hashes to use as branch/trunk transactions.
    def getTransactionsToApprove(self, depth):
        # Parameters
        # depth :: Number of bundles to go back to determine the transactions for approval.
        # reference (Optional) :: Transaction hash from which to start the weighted random walk. Use this parameter
        #           to make sure the returned tip transaction hashes approve a given reference transaction.
        command = {
            "command": "getTransactionsToApprove",
            "depth": depth,
        }

        # Response
        # trunkTransaction :: Valid trunk transaction hash
        # branchTransaction	 :: Valid branch transaction hash
        # duration :: The time it took to process the request in milliseconds
        return self.sendRequest(json.dumps(command), None, None)

    # Get a transaction's contents in trytes.
    def getTrytes(self, hashes):
        # Parameters
        # hashes :: Transaction hashes
        command = {
            "command": "getTrytes",
            "hashes": hashes
        }

        # Response
        # trytes :: Array of transaction trytes for the given transaction hashes (in the same order as the parameters)
        # duration :: Number of milliseconds it took to complete the request
        # --NOTE--
        # If a node doesn't have the trytes for a given transaction hash in its ledger, the value at the index of that
        # transaction hash is either null or a string of 9s.
        return self.sendRequest(json.dumps(command), None, None)

    # Abort the process that's started by the attachToTangle endpoint.
    def interruptAttachingToTangle(self):
        command = {"command": "interruptAttachingToTangle"}

        # Response
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Store transactions in a node's local storage.
    def storeTransactions(self, trytes):
        # Parameters
        # The value of the trytes parameter must be valid. Valid trytes are returned by the attachToTangle endpoint.
        # trytes :: Transaction trytes
        command = {
            "command": "storeTransactions",
            "trytes": trytes
        }

        # Response
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Check if an address was ever withdrawn from, either in the current epoch or in any previous epochs.
    # If an address has a pending transaction, it's also considered 'spent'.
    def wereAddressesSpentFrom(self, addresses):
        # Parameters
        # addresses ::addresses to check (do not include the checksum)
        command = {
            "command": "wereAddressesSpentFrom",
            "addresses": addresses
        }

        # Response
        # states :: States of the specified addresses in the same order as the values in the addresses parameter.
        #           A true value means that the address has been spent from.
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Broadcast transaction trytes to a node.
    def broadcastTransactions(self, trytes):
        # Parameters
        # trytes parameter for this endpoint must include proof of work, which is done by the attachToTangle endpoint.
        # trytes :: Valid transaction trytes
        command = {
            "command": "broadcastTransactions",
            "trytes": trytes
        }

        # Response
        # duration :: Number of milliseconds it took to complete the request
        return self.sendRequest(json.dumps(command), None, None)

    # Do proof of work on a node for the given transaction trytes.
    def attachToTangle(self, trunkTransaction, branchTransaction, trytes):
        # Parameters
        # The branchTransaction and trunkTransaction parameters are returned from the getTransactionsToApprove endpoint.
        # trunkTransaction :: Trunk transaction hash
        # branchTransaction :: Branch transaction hash
        # minWeightMagnitude :: Minimum weight magnitute
        # -- The minimum weight magnitude (MWM) is a variable that defines how much work is done during proof of work.
        # -- During proof of work, the transaction hash is repeatedly hashed until it ends in the same number of 0 trits
        # -- as the MWM. The higher the MWM, the harder the proof of work. When you interact with an IOTA network
        # -- as a client, you must use the correct MWM for that network. Otherwise, your transaction won't be valid
        # -- and the nodes will reject it.
        # trytes :: String of transaction trytes
        command = {
            "command": "attachToTangle",
            "trunkTransaction": trunkTransaction,
            "branchTransaction": branchTransaction,
            "minWeightMagnitude": 14,
            "trytes": trytes
        }
        # Response
        # The last 243 trytes of the return value consist of the following:
        # trunkTransaction + branchTransaction + nonce
        # trytes :: Transaction trytes that include a valid nonce field
        return self.sendRequest(json.dumps(command), None, None)

    # Encode Tryte
    # :param input_text: Tryte string
    # :return Tryte unicode
    def encodeTryte(self, input_text):
        message_trytes = TryteString.from_unicode(input_text)
        return message_trytes

    # Decode trytes into json array.
    # :param encoded_text: encode trytes
    # :return json array
    def decodeTryte(self, encoded_text):
        # More Information :: More Information https://pyota.readthedocs.io/en/latest/types.html
        try:
            txn_1 = Transaction.from_tryte_string(encoded_text)
            return {"address": txn_1.address,
                    "value": txn_1.value,
                    "legacy_tag": txn_1.legacy_tag,
                    "hash": txn_1.hash,
                    "timestamp": txn_1.timestamp,
                    "tag": txn_1.tag,
                    "current_index": txn_1.current_index,
                    "last_index": txn_1.last_index,
                    "bundle_hash": txn_1.bundle_hash,
                    "trunk_transaction_hash": txn_1.trunk_transaction_hash,
                    "branch_transaction_hash": txn_1.branch_transaction_hash,
                    "nonce": txn_1.nonce,
                    "signature_message_fragment": txn_1.signature_message_fragment.decode()
                    }
        except (ValueError, TypeError):
            print("Tryte decode has Error")
            return "continue"

    # Prompts the user securely for their seed.
    # IOTA Secure Seed Generator by Route Technologies [http://route.technology]
    def get_seed(self):
        sequence = string.ascii_uppercase + "9"
        seed = ''.join((secrets.choice(sequence) for i in range(81)))
        return seed

    # Add new transaction to the Tangle
    def sendToAddress(self, message, address, depth, tag, value):

        api = Iota("http://iota.av.it.pt:14265")
        # Sample Data
        # address = b'RECEIVINGWALLETADDRESSGOESHERE9WITHCHECKSUMANDSECURITYLEVELB999999999999999999999RQXIUOZMD'
        # depth = 3
        # tag = b'IOTAPASS'
        # value = 0

        # For more information, see :py:meth:`Iota.send_transfer`.
        try:
            api.send_transfer(
                depth=depth,
                # One or more :py:class:`ProposedTransaction` objects to add to the
                # bundle.
                transfers=[
                    ProposedTransaction(
                        # Recipient of the transfer.
                        address=Address(address),

                        # Amount of IOTA to transfer.
                        # By default this is a zero value transfer.
                        value=value,

                        # Optional tag to attach to the transfer.
                        tag=Tag(tag),

                        # Optional message to include with the transfer.
                        message=TryteString.from_string(message),
                    ),
                ],
            )
            return True
        except:
            return False
