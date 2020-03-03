import braintree
import os
from braintree import BraintreeGateway, Configuration, Environment

# https: // developers.braintreepayments.com/start/hello-server/python

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        # sandbox using fake money hehe
        # fake credit cards provided
        merchant_id=os.getenv('BT_MERCHANT_ID'),
        public_key=os.getenv('BT_PUBLIC_KEY'),
        private_key=os.getenv('BT_PRIVATE_KEY')
    )
)
