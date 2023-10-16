from enum import Enum
from sharingiscaring.GRPCClient.CCD_Types import *  # noqa: F403


class CredentialElement(Enum):
    firstName = "First Name"
    lastName = "Last Name"
    sex = "Sex"
    dob = "Date of Birth"
    countryOfResidence = "Country of Residence"
    nationality = "Nationatility"
    idDocType = "Identity Document Type"
    idDocNo = "Identity Document Number"
    idDocIssuer = "Identity Document Issuer"
    idDocIssuedAt = "ID Valid from"
    idDocExpiresAt = "ID Valid to"
    nationalIdNo = "National ID number"
    taxIdNo = "Tax ID number"


class CredentialDocType(Enum):
    na = "0"
    Passport = "1"
    National_ID_Card = "2"
    Driving_License = "3"
    Immigration_Card = "4"


class Credentials:
    """
    This class processes credential information as retrieved from the node.
    """

    def __init__(self):
        pass

    def determine_id_providers(self, ac):
        """
        Input to this method is the output from the node.
        """
        credentials = []
        for key, v in ac.items():
            v: CCD_AccountCredential  # noqa: F405
            if v.initial:
                v = v.initial
            elif v.normal:
                v = v.normal

            c = {
                "ip_identity": v.ip_id,
                "created_at": v.policy.created_at,
                "valid_to": v.policy.valid_to,
            }
            if len(v.policy.attributes.keys()) > 0:
                for key, revealedAttribute in v.policy.attributes.items():
                    value = revealedAttribute
                    c.update({CredentialElement[key].value: value})
            credentials.append(c)
        return credentials


class Identity:
    def __init__(self, account_info: CCD_AccountInfo):  # noqa: F405
        if account_info:
            self.credentials = Credentials().determine_id_providers(
                account_info.credentials
            )
            self.threshold = account_info.threshold
        else:
            self.credentials = []
            self.threshold = 0
