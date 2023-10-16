#!/usr/bin/env python3

import grpc
from pytarantula.tarantula.v1 import tarantula_api_pb2 as tarantula_api
from pytarantula.tarantula.v1 import tarantula_api_pb2_grpc as tarantula_grpc

class TarantulaClient:
    def __init__(self, host):
        self.channel = grpc.insecure_channel(host)
        self.stub = tarantula_grpc.tarantulaservicestub(self.channel)

    def create_order(self, exchange, order):
        """
        Create an order on a specified exchange.

        :param exchange: The exchange on which the order will be placed.
        :param order: The order details.
        :return: Transaction details.
        """
        request = tarantula_api.CreateOrderRequest(exchange=exchange, order=order)
        return self.stub.CreateOrder(request)

    def cancel_order(self, transaction):
        """
        Cancel an order using its transaction details.

        :param transaction: The transaction details of the order.
        :return: Cancel order response.
        """
        request = tarantula_api.CancelOrderRequest(transaction=transaction)
        return self.stub.CancelOrder(request)
