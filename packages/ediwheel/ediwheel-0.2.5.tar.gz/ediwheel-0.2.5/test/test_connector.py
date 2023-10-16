import unittest

from ediwheel.connector import *


michelin = EdiConnectorConfig( # nullpointer
            host="https://bibserve.com/MichelinSCEBE/AdhocA2XML25Servlet",
            username="MWH9337",
            password="AdHoc?ForiGrC931",
            id="6069966",
            timeout_s=10,
        )
conti = EdiConnectorConfig( # Invalid credentials
    host="https://direct.conti.de/cgi-bin/easy-xml.cgi",
    username="07319622",
    password="Quentin12",
    id="07319622",
    timeout_s=10,
)
goodyear = EdiConnectorConfig( # WORKS
    host="https://xi.goodyear.com/tosxml/SWITZERLAND",
    username="C_30188579",
    password="CD69aa25ze228eEz",
    id="30188579",
    timeout_s=10,
)
vredestein = EdiConnectorConfig( # WORKS
    host="https://dealer.vredestein.com/adhocxml.dll",
    username="50705723",
    password="GREFRO10032021",
    id="50705723",
    timeout_s=10,
)
bridgestone = EdiConnectorConfig( # WORKS
    host="https://adhoc.bridgestone.eu/prod/adhoc",
    username="Bxp%A2",
    password="A2*Bxp",
    id="426009",
    timeout_s=10,
)

class TestConnector(unittest.TestCase):

    def test_vred(self):


        connector = EdiConnector(vredestein)
        connector.enquiry("8714692506864", "AP20565016WULAAB0")

    def test_bridgestone(self):
        connector = EdiConnector(bridgestone)
        connector.enquiry("3286340729611", "7296")

    def test_bridge_batch(self):
        connector = EdiConnector(bridgestone)
        eans = ["3286341075311", "3286341934212", "3286341029116"]
        sup_codes = ["10753", "19342", "10291"]
        connector.batch_inquiry(eans, sup_codes)

    def test_goodyear(self):
        connector = EdiConnector(goodyear)
        res = connector.enquiry("5452000662088", "529112")

        print(res)

    def test_michelin(self):
        connector = EdiConnector(michelin)
        res = connector.enquiry("", "")

        print(res)

    def test_conti(self):
        connector = EdiConnector(conti)
        res = connector.enquiry("4019238030891", "3110000000")

        print(res)