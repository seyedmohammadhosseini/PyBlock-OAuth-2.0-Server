# the ZMQ is a high-performance asynchronous messaging library, aimed at use in distributed or concurrent applications.
# It provides a message queue, but unlike message-oriented middleware, a ZeroMQ system can run
# without a dedicated message broker.
# https://github.com/seyedmohammadhosseini/pyzmq

import zmq
from zmq.utils.monitor import recv_monitor_message
import json


class controller:

    # Initialize the database class
    # :param register: access to all other class
    def __init__(self, register):
        self.register = register
        pass

    # check input type is json or not
    # :param input: any type of data
    # :return True for json and else False
    @staticmethod
    def is_json(input):
        try:
            json.loads(input)
        except ValueError as e:
            return False
        return True

    # Processing of new pending Transaction that added on the Tangle by Application or Server
    # :param configuration
    # :param libraries : object of all libraries
    # :param ticket : object of sub-processing ticket class
    # :user user : object of sub-processing user class
    def pending(self, configuration, libraries, ticket, user):

        libraries = libraries
        iota = libraries['iota']
        exists = []

        while True:
            transactions = iota.findTransactions([configuration['ZMQ']['ADDRESS']])
            for transaction in transactions['hashes']:
                if transaction not in exists:
                    exists.append(transaction)
                    data = iota.getTrytes([transaction])
                    trytes = data['trytes'][0]
                    data = iota.decodeTryte(trytes)

                    if data == "continue":
                        continue

                    # Ignore input transactions; these have cryptographic signatures,
                    # not human-readable messages.
                    if data['value'] < 0:
                        continue

                    if "signature_message_fragment" in data:
                        if self.is_json(data['signature_message_fragment']):
                            tangle_data = json.loads(data['signature_message_fragment'])

                            if "info" in tangle_data and "signature" in tangle_data:

                                if "user_id" in tangle_data['info'] and "nonce" in tangle_data['info'] and "step" in tangle_data['info']:

                                    user_info = user.get_user_info_call_from_zmq(tangle_data['info']['user_id'])
                                    public_key = user_info[5]
                                    sign_result = libraries['secure'].signature_verify(
                                        public_key,
                                        tangle_data['info'],
                                        tangle_data['signature']
                                    )
                                    if not sign_result:
                                        continue

                                    if str(tangle_data['info']['step']) == "checkin":
                                        exist_this_ticket = ticket.check_ticket_by_user_id_and_nonce(
                                            tangle_data['info']['user_id'],
                                            tangle_data['info']['nonce'],
                                            data['timestamp'],
                                            "checkin"
                                        )

                                        if not exist_this_ticket:
                                            ticket_id = ticket.add_by_tangle_data(
                                                tangle_data,
                                                data['timestamp'],
                                                transaction,
                                                0,
                                                "pending",
                                                data['value'],
                                                tangle_data['info']["zone"],
                                                ""
                                            )
                                            parent_id = ticket.find_parent(
                                                tangle_data['info']['user_id'],
                                                tangle_data['info']['nonce'],
                                                "checkout"
                                            )
                                            if parent_id:
                                                ticket.set_parent(ticket_id, parent_id)

                                    elif str(tangle_data['info']['step']) == "checkout":
                                        exist_this_ticket = ticket.check_ticket_by_user_id_and_nonce(
                                            tangle_data['info']['user_id'],
                                            tangle_data['info']['nonce'],
                                            data['timestamp'],
                                            "checkout"
                                        )
                                        if not exist_this_ticket:
                                            parent_id = ticket.find_parent(
                                                tangle_data['info']['user_id'],
                                                tangle_data['info']['nonce'],
                                                "checkin"
                                            )
                                            ticket.add_by_tangle_data(
                                                tangle_data,
                                                data['timestamp'],
                                                transaction,
                                                parent_id,
                                                "pending",
                                                data['value'],
                                                "",
                                                tangle_data['info']["zone"]
                                            )
                                    else:
                                        print("Status Error : " + str(tangle_data['info']['step']))
            break
    # Processing of new confirm Transaction that added on the Tangle by Application or Server
    # :param configuration
    # :param libraries : object of all libraries
    # :param ticket : object of sub-processing ticket class
    # :user user : object of sub-processing user class
    def confirm(self, configuration, libraries, ticket, user):
        libraries = libraries
        iota = libraries['iota']
        context = zmq.Context()
        socket = zmq.Socket(context, zmq.SUB)
        monitor = socket.get_monitor_socket()

        socket.connect(configuration['ZMQ']['SERVER'])

        while True:
            status = recv_monitor_message(monitor)
            if status['event'] == zmq.EVENT_CONNECTED:
                break
            elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
                pass

        socket.subscribe(configuration['ZMQ']['ADDRESS'])

        while True:
            try:
                data = socket.recv_string()
                data = data.split(' ')
                transaction = data[1]
                data = iota.getTrytes([transaction])
                trytes = data['trytes'][0]
                data = iota.decodeTryte(trytes)

                if data == "continue":
                    continue

                # Ignore input transactions; these have cryptographic signatures,
                # not human-readable messages.
                if data['value'] < 0:
                    continue

                if "signature_message_fragment" in data:
                    if self.is_json(data['signature_message_fragment']):
                        tangle_data = json.loads(data['signature_message_fragment'])
                        if "info" in tangle_data and "signature" in tangle_data:

                            if "user_id" in tangle_data['info'] and "nonce" in tangle_data['info'] and "step" in \
                                    tangle_data['info']:

                                user_info = user.get_user_info_call_from_zmq(tangle_data['info']['user_id'])
                                public_key = user_info[5]
                                sign_result = libraries['secure'].signature_verify(
                                    public_key,
                                    tangle_data['info'],
                                    tangle_data['signature']
                                )
                                if not sign_result:
                                    continue

                                if str(tangle_data['info']['step']) == "checkin":

                                    ticket_id = ticket.check_ticket_by_user_id_and_nonce(
                                        tangle_data['info']['user_id'],
                                        tangle_data['info']['nonce'],
                                        data['timestamp'],
                                        "checkin"
                                    )

                                    if not ticket_id:
                                        ticket_id = ticket.add_by_tangle_data(
                                            tangle_data,
                                            data['timestamp'],
                                            transaction,
                                            0,
                                            "confirm",
                                            data['value'],
                                            tangle_data['info']["zone"],
                                            ""
                                        )
                                        parent_id = ticket.find_parent(
                                            tangle_data['info']['user_id'],
                                            tangle_data['info']['nonce'],
                                            "checkout"
                                        )
                                        if parent_id:
                                            ticket.set_parent(ticket_id, parent_id)
                                    else:
                                        ticket.update_ticket_status_by_ticket_id(
                                            ticket_id,
                                            "confirm"
                                        )

                                elif str(tangle_data['info']['step']) == "checkout":
                                    ticket_id = ticket.check_ticket_by_user_id_and_nonce(
                                        tangle_data['info']['user_id'],
                                        tangle_data['info']['nonce'],
                                        data['timestamp'],
                                        "checkout"
                                    )
                                    if not ticket_id:
                                        parent_id = ticket.find_parent(
                                            tangle_data['info']['user_id'],
                                            tangle_data['info']['nonce'],
                                            "checkin"
                                        )
                                        ticket.add_by_tangle_data(
                                            tangle_data,
                                            data['timestamp'],
                                            transaction,
                                            parent_id,
                                            "pending",
                                            data['value'],
                                            "",
                                            tangle_data['info']["zone"]
                                        )
                                    else:
                                        ticket.update_ticket_status_by_ticket_id(
                                            ticket_id,
                                            "confirm"
                                        )
                                else:
                                    print("Status Error : " + str(tangle_data['info']['step']))
            except ValueError as e:
                print("Error: " + str(e))


