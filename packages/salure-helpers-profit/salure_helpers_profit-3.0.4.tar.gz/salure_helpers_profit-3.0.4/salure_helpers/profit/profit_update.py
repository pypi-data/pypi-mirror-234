import base64
import json
import warnings
import pandas as pd
import requests
from salure_helpers.salureconnect import SalureConnect
from typing import Union, List


class UpdateConnector(SalureConnect):
    def __init__(self, label: str, test_environment: bool = False, debug: bool = False):
        super().__init__()
        if test_environment:
            self.base_url = 'resttest.afas.online'
        else:
            self.base_url = 'rest.afas.online'
        credentials = self.get_system_credential(system='profit', label=label, test_environment=test_environment)
        self.environment = credentials['environment']
        base64token = base64.b64encode(credentials['token'].encode('utf-8')).decode()
        self.headers = {'Authorization': 'AfasToken ' + base64token,
                        'IntegrationId': '38092_135680'}
        self.debug = debug

    def update(self, updateconnector, data) -> requests.Response:
        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, updateconnector)

        update = requests.request("PUT", url, data=data, headers=self.headers)

        return update

    def update_person(self, data: dict, overload_fields: dict = None, method='PUT') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['employee_id', 'mail_work', 'mail_private', 'mobile_work', 'mobile_private', 'nickname', 'first_name', 'initials', 'prefix', 'last_name', 'prefix_birth_name',
                          'birth_name', 'gender', 'nationality', 'birth_date', 'country_of_birth', 'ssn', 'marital_status', 'date_of_marriage', 'date_of_divorce', 'phone_work', 'phone_private', 'city_of_birth',
                          'birth_name_separate', 'name_use', 'match_person_on', 'birthname_partner', 'prefix_birthname_partner']
        required_fields = ['employee_id', 'person_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/KnPerson')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "KnPerson": {
                            "Element": {
                                "Fields": {
                                    "MatchPer": "0" if "match_person_on" not in data else data['match_person_on'],
                                    "BcCo": data['person_id']
                                }
                            }
                        }
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"EmAd": data['mail_work']}) if 'mail_work' in data else fields_to_update
        fields_to_update.update({"EmA2": data['mail_private']}) if 'mail_private' in data else fields_to_update
        fields_to_update.update({"MbNr": data['mobile_work']}) if 'mobile_work' in data else fields_to_update
        fields_to_update.update({"MbN2": data['mobile_private']}) if 'mobile_private' in data else fields_to_update
        fields_to_update.update({"CaNm": data['nickname']}) if 'nickname' in data else fields_to_update
        fields_to_update.update({"FiNm": data['first_name']}) if 'first_name' in data else fields_to_update
        fields_to_update.update({"In": data['initials']}) if 'initials' in data else fields_to_update
        fields_to_update.update({"Is": data['prefix']}) if 'prefix' in data else fields_to_update
        fields_to_update.update({"LaNm": data['last_name']}) if 'last_name' in data else fields_to_update
        fields_to_update.update({"IsBi": data['prefix_birth_name']}) if 'prefix_birth_name' in data else fields_to_update
        fields_to_update.update({"NmBi": data['birth_name']}) if 'birth_name' in data else fields_to_update
        fields_to_update.update({"ViGe": data['gender']}) if 'gender' in data else fields_to_update
        fields_to_update.update({"PsNa": data['nationality']}) if 'nationality' in data else fields_to_update
        fields_to_update.update({"DaBi": data['birth_date']}) if 'birth_date' in data else fields_to_update
        fields_to_update.update({"RsBi": data['country_of_birth']}) if 'country_of_birth' in data else fields_to_update
        fields_to_update.update({"SoSe": data['ssn']}) if 'ssn' in data else fields_to_update
        fields_to_update.update({"ViCs": data['marital_status']}) if 'marital_status' in data else fields_to_update
        fields_to_update.update({"DaMa": data['date_of_marriage']}) if 'date_of_marriage' in data else fields_to_update
        fields_to_update.update({"DaMa": data['date_of_divorce']}) if 'date_of_divorce' in data else fields_to_update
        fields_to_update.update({"TeNr": data['phone_work']}) if 'phone_work' in data else fields_to_update
        fields_to_update.update({"TeN2": data['phone_private']}) if 'phone_private' in data else fields_to_update
        fields_to_update.update({"RsBi": data['city_of_birth']}) if 'city_of_birth' in data else fields_to_update
        fields_to_update.update({"SpNm": data['birth_name_separate']}) if 'birth_name_separate' in data else fields_to_update
        fields_to_update.update({"ViUs": data['name_use']}) if 'name_use' in data else fields_to_update
        fields_to_update.update({"NmPa": data['birthname_partner']}) if 'birthname_partner' in data else fields_to_update
        fields_to_update.update({"IsPa": data['prefix_birthname_partner']}) if 'prefix_birthname_partner' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['KnPerson']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_user(self, data: dict, method='POST') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param method: request type (must be post or put)
        :return: status code for request and optional error message
        """
        allowed_fields = ['profit_user_code', 'person_id', 'userPrincipalName', 'mail']
        required_fields = ['profit_user_code', 'person_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnUser'

        base_body = {
            "KnUser": {
                "Element": {
                    "@UsId": data['profit_user_code'],
                    "Fields": {
                        "MtCd": 1,
                        "BcCo": data['person_id'],
                        "Nm": "SALURE",
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"Upn": data['userPrincipalName']}) if 'userPrincipalName' in data else fields_to_update
        fields_to_update.update({"EmAd": data['mail']}) if 'mail' in data else fields_to_update

        # Update the request body with update fields
        base_body['KnUser']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def upload_photo(self, filepath: str, person_id: str, filename: str = None) -> requests.Response:
        """
        This code opens a file located at filename in binary mode, reads its contents, encodes the contents in base64, and assigns the result to filestream.
        Then, it creates a JSON object representing an image upload request to an API endpoint.
        This JSON object is converted to a string using json.dumps and assigned to body_image_upload.
        :param filepath: The filepath (complete path including filename) of the image to be uploaded
        :param filename: The filename of the image to be uploaded
        :param person_id: The personal id number of the user in AFAS
        """
        open_file = open(filepath, 'rb').read()
        filestream = base64.b64encode(open_file).decode('utf-8')
        body_image_upload = {"KnPerson": {
            "Element": {
                "Fields": {
                    "MatchPer": "0",
                    "BcCo": person_id,
                    "FileName": "filename" if filename is None else filename,
                    "FileStream": filestream,

                }
            }
        }
        }
        body_image_upload = json.dumps(body_image_upload)
        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnPerson'
        update = requests.put(url=url, data=body_image_upload, headers=self.headers)
        return update

    def update_organisation(self, data: dict, method: str, custom_fields: dict = None) -> requests.Response:
        """
        This function updates organisations in CRM with the AFAS updateconnect 'KnOrganisation'.
        :param data: Deliver all the data which should be updated in list format. The data should at least contain the required_fields and can contain also the allowed fields
        :param method: Is a PUT for an update of an existing cost carrier. is a POST for an insert of a new cost carrier
        :param custom_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: The status code from AFAS Profit
        """
        required_fields = ['organisation_id', 'name', 'blocked']
        allowed_fields = ['collective_ledger_account', 'search_name', 'kvk_number', 'phone_number_work', 'email_work', 'vat_number', 'status',
                          'mailbox_address', 'country', 'street', 'housenumber', 'housenumber_add', 'zipcode', 'residence', 'search_living_place_by_zipcode']

        # Check if the fields in data exists in the required or allowed fields
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method != 'PUT' and method != 'POST' and method != 'DELETE':
            raise ValueError('Parameter method should be PUT, POST or DELETE (in uppercase)')

        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnOrganisation/KnOrganisation/MatchOga,BdIdBcCo,Nm,Bl/0,1,{data['organisation_id']},{data['name']},{data['blocked']}"
            base_body = {}
        else:
            url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnOrganisation')

            base_body = {
                "KnOrganisation": {
                    "Element": {
                        "Fields": {
                            "MatchOga": "0",
                            "BcId": 1,
                            "BcCo": data['organisation_id'],
                            "Nm": data['name'],
                            "Bl": data['blocked']
                        },
                        "Objects": {

                        }
                    }
                }
            }

            address_body = {
                "KnBasicAddressAdr": {
                    "Element": {
                        "Fields": {
                        }
                    }
                }
            }

            # If one of the optional fields of a subelement is included, we need to merge the whole JSON object to the basebody
            if any(field in data.keys() for field in allowed_fields):
                fields_to_update = {}
                fields_to_update.update({"PbAd": data['mailbox_address']}) if 'mailbox_address' in data else fields_to_update
                fields_to_update.update({"CoId": data['country']}) if 'country' in data else fields_to_update
                fields_to_update.update({"Ad": data['street']}) if 'street' in data else fields_to_update
                fields_to_update.update({"HmNr": data['housenumber']}) if 'housenumber' in data else fields_to_update
                fields_to_update.update({"HmAd": data['housenumber_add']}) if 'housenumber_add' in data else fields_to_update
                fields_to_update.update({"ZpCd": data['zipcode']}) if 'zipcode' in data else fields_to_update
                fields_to_update.update({"Rs": data['residence']}) if 'residence' in data else fields_to_update
                fields_to_update.update({"ResZip": data['search_living_place_by_zipcode']}) if 'search_living_place_by_zipcode' in data else fields_to_update

                # merge subelement with basebody if there are address fields added. If not, don't add the address part to the base_body
                if len(fields_to_update) > 0:
                    address_body['KnBasicAddressAdr']['Element']['Fields'].update(fields_to_update)
                    base_body['KnOrganisation']['Element']['Objects'].update(address_body)

            # Add allowed fields to the basebody if they are available in the data. Fields that are not exists in the basebody, should not be added tot this basebody to prevent errrors.
            fields_to_update = {}
            fields_to_update.update({"SeNm": data['search_name']}) if 'search_name' in data else fields_to_update
            fields_to_update.update({"CcNr": data['kvk_number']}) if 'kvk_number' in data else fields_to_update
            fields_to_update.update({"TeNr": data['phone_number_work']}) if 'phone_number_work' in data else fields_to_update
            fields_to_update.update({"EmAd": data['email_work']}) if 'email_work' in data else fields_to_update
            fields_to_update.update({"FiNr": data['vat_number']}) if 'vat_number' in data else fields_to_update
            fields_to_update.update({"StId": data['status']}) if 'status' in data else fields_to_update

            base_body['KnOrganisation']['Element']['Fields'].update(fields_to_update)

            # Now create a dict for all the custom fields. This fields are not by default added to the base_body because they're not always present in the dataset
            fields_to_update = {}
            fields_to_update.update(custom_fields) if custom_fields is not None else ''

            # Update the request body with update fields
            base_body['KnOrganisation']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_debtor(self, data: dict, overload_fields: dict = None, method='PUT') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['match_person_on', 'enter_birthname_seperate', 'person_id', 'country', 'street', 'house_number', 'house_number_add', 'postal_code',
                          'mailbox_address', 'city', 'person_id', 'mail_private', 'nickname', 'first_name', 'initials', 'prefix', 'last_name',
                          'prefix_birth_name', 'birth_name', 'prefix_partner_name', 'partner_name', 'gender', 'phone_private', 'name_use',
                          'autonumber_person', 'search_address_by_postal_code']
        required_fields = ['debtor_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnSalesRelationPer'

        base_body = {
            "KnSalesRelationPer": {
                "Element": {
                    "@DbId": data['debtor_id'],
                    "Fields": {
                        "CuId": "EUR",
                        "IsDb": True
                    },
                    "Objects": {
                        "KnPerson": {
                            "Element": {
                                "Fields": {
                                    "MatchPer": "0" if "match_person_on" not in data else data['match_person_on'],
                                    "BcId": 1
                                },
                                "Objects": {
                                }
                            }
                        }
                    }
                }
            }
        }

        address_body = {
            "KnBasicAddressAdr": {
                "Element": {
                    "Fields": {
                    }
                }
            },
            "KnBasicAddressPad": {
                "Element": {
                    "Fields": {
                    }
                }
            }
        }

        # If one of the optional fields of a subelement is included, we need to merge the whole JSON object to the basebody
        if any(field in data.keys() for field in allowed_fields):
            fields_to_update = {}
            fields_to_update.update({"PbAd": data['mailbox_address']}) if 'mailbox_address' in data else fields_to_update
            fields_to_update.update({"CoId": data['country']}) if 'country' in data else fields_to_update
            fields_to_update.update({"Ad": data['street']}) if 'street' in data else fields_to_update
            fields_to_update.update({"HmNr": data['house_number']}) if 'house_number' in data else fields_to_update
            fields_to_update.update({"HmAd": data['house_number_add']}) if 'house_number_add' in data else fields_to_update
            fields_to_update.update({"ZpCd": data['postal_code']}) if 'postal_code' in data else fields_to_update
            fields_to_update.update({"Rs": data['city']}) if 'city' in data else fields_to_update
            fields_to_update.update({"ResZip": data['search_address_by_postal_code']}) if 'search_address_by_postal_code' in data else fields_to_update

            # merge subelement with basebody if there are address fields added. If not, don't add the address part to the base_body
            if len(fields_to_update) > 0:
                address_body['KnBasicAddressAdr']['Element']['Fields'].update(fields_to_update)
                address_body['KnBasicAddressPad']['Element']['Fields'].update(fields_to_update)
                base_body['KnSalesRelationPer']['Element']['Objects']['KnPerson']['Element']['Objects'].update(address_body)

        # Add fields to the basebody of the debtor itself (not the person)
        fields_to_update = {}
        fields_to_update.update({"ColA": data['collective_ledger_account']}) if 'collective_ledger_account' in data else fields_to_update
        fields_to_update.update({"PaCd": data['payment_condition']}) if 'payment_condition' in data else fields_to_update
        # Update the request body with update fields
        base_body['KnSalesRelationPer']['Element']['Fields'].update(fields_to_update)

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update({"AutoNum": data['autonumber_person']}) if 'autonumber_person' in data else fields_to_update
        fields_to_update.update({"SpNm": data['enter_birthname_seperate']}) if 'enter_birthname_seperate' in data else fields_to_update
        fields_to_update.update({"BcCo": data['person_id']}) if 'person_id' in data else fields_to_update
        fields_to_update.update({"PbAd": data['mailbox_address']}) if 'mailbox_address' in data else fields_to_update
        fields_to_update.update({"EmA2": data['mail_private']}) if 'mail_private' in data else fields_to_update
        fields_to_update.update({"CaNm": data['nickname']}) if 'nickname' in data else fields_to_update
        fields_to_update.update({"FiNm": data['first_name']}) if 'first_name' in data else fields_to_update
        fields_to_update.update({"In": data['initials']}) if 'initials' in data else fields_to_update
        fields_to_update.update({"Is": data['prefix']}) if 'prefix' in data else fields_to_update
        fields_to_update.update({"LaNm": data['last_name']}) if 'last_name' in data else fields_to_update
        fields_to_update.update({"IsBi": data['prefix_birth_name']}) if 'prefix_birth_name' in data else fields_to_update
        fields_to_update.update({"NmBi": data['birth_name']}) if 'birth_name' in data else fields_to_update
        fields_to_update.update({"IsPa": data['prefix_partner_name']}) if 'prefix_partner_name' in data else fields_to_update
        fields_to_update.update({"NmPa": data['partner_name']}) if 'partner_name' in data else fields_to_update
        fields_to_update.update({"ViGe": data['gender']}) if 'gender' in data else fields_to_update
        fields_to_update.update({"TeN2": data['phone_private']}) if 'phone_private' in data else fields_to_update
        fields_to_update.update({"ViUs": data['name_use']}) if 'name_use' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['KnSalesRelationPer']['Element']['Objects']['KnPerson']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_creditor(self, method: str, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['person_id', 'internal_id', 'match_person_on', 'log_birthname_seperately', 'collective_account', 'preferred_delivery_method', 'automatic_payment', 'compact', 'payment_specification', 'remark']
        required_fields = ['creditor_id']

        if method != 'PUT' and method != 'POST' and method != 'DELETE':
            raise ValueError('Parameter method should be PUT, POST or DELETE (in uppercase)')

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnPurchaseRelationPer'

        base_body = {
            "KnPurchaseRelationPer": {
                "Element": {
                    "@CrId": data['creditor_id'],
                    "Fields": {
                        "CuId": "EUR",
                        "IsCr": True
                    },
                    "Objects": {
                        "KnPerson": {
                            "Element": {
                                "Fields": {
                                    "MatchPer": "0" if "match_person_on" not in data else data['match_person_on'],
                                },
                                "Objects": {
                                }
                            }
                        }
                    }
                }
            }
        }

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update({"Rm": data['remark']}) if 'remark' in data else fields_to_update
        fields_to_update.update({"PaCd": data['payment_condition']}) if 'person_id' in data else fields_to_update
        fields_to_update.update({"ColA": data['collective_account']}) if 'collective_account' in data else fields_to_update
        fields_to_update.update({"InPv": data['preferred_delivery_method']}) if 'preferred_delivery_method' in data else fields_to_update
        fields_to_update.update({"AuPa": data['automatic_payment']}) if 'automatic_payment' in data else fields_to_update
        fields_to_update.update({"PaCo": data['compact']}) if 'compact' in data else fields_to_update
        fields_to_update.update({"PaSp": data['payment_specification']}) if 'payment_specification' in data else fields_to_update

        base_body['KnPurchaseRelationPer']['Element']['Fields'].update(fields_to_update)

        # Update the request body with update fields
        fields_to_update = {}
        fields_to_update.update({"BcId": data['internal_id']}) if 'internal_id' in data else fields_to_update
        fields_to_update.update({"BcCo": data['person_id']}) if 'person_id' in data else fields_to_update
        fields_to_update.update({"MatchPer": data['compare_on']}) if 'compare_on' in data else fields_to_update
        fields_to_update.update({"SpNm": data['log_birthname_seperately']}) if 'log_birthname_seperately' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        base_body['KnPurchaseRelationPer']['Element']['Objects']['KnPerson']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_employee(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        allowed_fields = ['employee_id', 'city_of_birth']
        required_fields = ['employee_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Fields": {
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"LwRs": data['city_of_birth']}) if 'city_of_birth' in data else fields_to_update

        # This is to include custom fields
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Fields'].update(fields_to_update)

        update = requests.request("PUT", url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_address(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        allowed_fields = ['street_number_add', 'city', 'match_employees_on', 'ssn', 'find_address_based_on_postal_code']
        required_fields = ['employee_id', 'person_id', 'country', 'street', 'street_number', 'postal_code', 'startdate']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/KnPerson')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "KnPerson": {
                            "Element": {
                                "Fields": {
                                    "MatchPer": "1" if "match_employees_on" not in data else data['match_employees_on'],
                                    "BcCo": data['person_id']
                                },
                                "Objects": {
                                    "KnBasicAddressAdr": {
                                        "Element": {
                                            "Fields": {
                                                "CoId": data['country'],
                                                "PbAd": False,
                                                "Ad": data['street'],
                                                "HmNr": data['street_number'],
                                                "BcCo": data['employee_id'],
                                                "ZpCd": data['postal_code'],
                                                "ResZip": data['search_address_by_postal_code'] if 'search_address_by_postal_code' in data.keys() else True,
                                                "BeginDate": data['startdate']
                                            }
                                        }
                                    },
                                    "KnBasicAddressPad": {
                                        "Element": {
                                            "Fields": {
                                                "CoId": data['country'],
                                                "PbAd": False,
                                                "Ad": data['street'],
                                                "HmNr": data['street_number'],
                                                "BcCo": data['employee_id'],
                                                "ZpCd": data['postal_code'],
                                                "ResZip": data['search_address_by_postal_code'] if 'search_address_by_postal_code' in data.keys() else True,
                                                "BeginDate": data['startdate']
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"HmAd": data['street_number_add']}) if 'street_number_add' in data else fields_to_update
        fields_to_update.update({"Rs": data['city']}) if 'city' in data else fields_to_update

        # This is to include custom fields
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['KnPerson']['Element']['Objects']['KnBasicAddressAdr']['Element']['Fields'].update(fields_to_update)
        base_body['AfasEmployee']['Element']['Objects']['KnPerson']['Element']['Objects']['KnBasicAddressPad']['Element']['Fields'].update(fields_to_update)
        base_body['AfasEmployee']['Element']['Objects']['KnPerson']['Element']['Fields'].update({"SoSe": data['ssn']}) if 'ssn' in data else None

        if self.debug:
            print(json.dumps(base_body))

        update = requests.request("POST", url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_contract(self, data: dict, overload_fields: dict = None, method: str = 'POST') -> requests.Response:
        """
        :param data: Dictionary of fields that you want to update in AFAS. Only fields listed in allowed arrays are accepted. Fields listed in required fields array, are mandatory
        :param overload_fields: Dictionary of dictionaries. Specify sub dictionaries for each section you want to update.
        Specify as key which element you want to update, available options are: schedule, salary, contract, function.
        Example: overload_fields = {"employee": {"field": value}}
        :param method: request type
        :return: status code for request and optional error message
        """

        # Contract fields
        required_fields_contract = ['employee_id', 'startdate_contract']
        allowed_fields_contract = ['employee_id', 'type_of_employment', 'enddate_contract', 'termination_reason', 'termination_initiative', 'probation_period',
                                   'probation_enddate', 'cao', 'terms_of_employment', 'type_of_contract', 'employer_number', 'type_of_employee', 'employment',
                                   'seniority_date', 'contract_chain_code', 'start_date_contract_chain', 'date_in_service_original', 'number_income_ratio']

        # Function fields
        required_fields_function = ['organizational_unit', 'function_id', 'costcenter_id']
        allowed_fields_function = ['costcarrier_id']

        # Timetable fields
        required_fields_timetable = ['weekly_hours', 'parttime_percentage']
        allowed_fields_timetable = ['changing_work_pattern', 'days_per_week', 'fte', 'on-call_contract', 'type_of_schedule']

        # Workschedule fields (Optional: if one field is given, all fields are required)
        fields_workschedule = ['startdate_workcycle', 'workcycle', 'start_week', 'index_number']

        # Salary fields
        required_fields_salary = ['type_of_salary', 'period_table']
        allowed_fields_salary = ['step', 'function_scale', 'salary_scale', 'salary_year', 'net_salary', 'apply_timetable', 'salary_amount']

        if method == 'POST':
            allowed_fields = allowed_fields_contract + allowed_fields_salary + allowed_fields_timetable + allowed_fields_function
            required_fields = required_fields_contract + required_fields_function + required_fields_timetable + required_fields_salary
        elif method == 'PUT':
            allowed_fields = allowed_fields_contract + required_fields_function + required_fields_timetable + required_fields_salary + allowed_fields_salary + allowed_fields_timetable + allowed_fields_function
            required_fields = required_fields_contract
        else:
            raise ValueError(f'Method {method} not supported, only POST and PUT are supported')

        # Check if there are fields that are not allowed or fields missing that are required
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasContract')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "AfasContract": {
                            "Element": {
                                "@DaBe": data['startdate_contract'],
                                "Fields": {
                                }
                            }
                        }
                    }
                }
            }
        }

        # Extra JSON objects which are optional at contract creation
        function_dict = {
            "AfasOrgunitFunction": {
                "Element": {
                    "@DaBe": data['startdate_contract'],
                    "Fields": {
                    }
                }
            }
        }

        timetable = {
            "AfasTimeTable": {
                "Element": {
                    "@DaBg": data['startdate_contract'],
                    "Fields": {
                        "StPa": True
                    }
                }
            }
        }

        salary = {
            "AfasSalary": {
                "Element": {
                    "@DaBe": data['startdate_contract'],
                    "Fields": {
                    }
                }
            }
        }

        # If one of the optional fields of a subelement is included, we need to merge the whole JSON object to the basebody
        if any(field in data.keys() for field in allowed_fields_function):
            for field in required_fields_function:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for function are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"DpId": data['organizational_unit']}) if 'organizational_unit' in data else fields_to_update
            fields_to_update.update({"FuId": data['function_id']}) if 'function_id' in data else fields_to_update
            fields_to_update.update({"CrId": data['costcenter_id']}) if 'costcenter_id' in data else fields_to_update
            fields_to_update.update({"CcId": data['costcarrier_id']}) if 'costcarrier_id' in data else fields_to_update
            # add overload function fields to the body
            if overload_fields is not None and 'function' in overload_fields.keys():
                fields_to_update.update(overload_fields['function'])

            # merge subelement with basebody
            function_dict['AfasOrgunitFunction']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(function_dict)

        if any(field in data.keys() for field in allowed_fields_timetable):
            for field in required_fields_timetable:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for timetable are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"StPa": data['changing_work_pattern']}) if 'changing_work_pattern' in data else fields_to_update
            fields_to_update.update({"HrWk": data['weekly_hours']}) if 'weekly_hours' in data else fields_to_update
            fields_to_update.update({"PcPt": data['parttime_percentage']}) if 'parttime_percentage' in data else fields_to_update
            fields_to_update.update({"DyWk": data['days_per_week']}) if 'days_per_week' in data else fields_to_update
            fields_to_update.update({"Ft": data['fte']}) if 'fte' in data else fields_to_update
            fields_to_update.update({"ClAg": data['on-call_contract']}) if 'on-call_contract' in data else fields_to_update
            fields_to_update.update({"EtTy": data['type_of_schedule']}) if 'type_of_schedule' in data else fields_to_update
            # add overload schedule fields to the body
            if overload_fields is not None and 'schedule' in overload_fields.keys():
                fields_to_update.update(overload_fields['schedule'])

            timetable['AfasTimeTable']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(timetable)

        if any(field in data.keys() for field in fields_workschedule):
            for field in fields_workschedule:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for workschedules are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            workschedule = {
                "Objects": [
                    {
                        "AfasWorkTime": {
                            "Element": {
                                "@DaBe": data['startdate_workcycle'],
                                "Fields": {
                                    "Twcy": data['workcycle'],
                                    "Twcp": data['start_week'],
                                    "Twcc": data['index_number']
                                }
                            }
                        }
                    }
                ]
            }
            base_body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element'].update(workschedule)

        if any(field in data.keys() for field in allowed_fields_salary):
            for field in required_fields_salary:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for salaries are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"SaSt": data['step']}) if 'step' in data else fields_to_update
            fields_to_update.update({"SaPe": data['type_of_salary']}) if 'type_of_salary' in data else fields_to_update
            fields_to_update.update({"EmSa": data['salary_amount']}) if 'salary_amount' in data else fields_to_update
            fields_to_update.update({"PtId": data['period_table']}) if 'period_table' in data else fields_to_update
            fields_to_update.update({"VaSc": data['salary_scale']}) if 'salary_scale' in data else fields_to_update
            fields_to_update.update({"TaId": data['salary_scale_type']}) if 'salary_scale_type' in data else fields_to_update
            fields_to_update.update({"FuSc": data['function_scale']}) if 'function_scale' in data else fields_to_update
            fields_to_update.update({"FuTa": data['function_scale_type']}) if 'function_scale_type' in data else fields_to_update
            fields_to_update.update({"SaYe": data['salary_year']}) if 'salary_year' in data else fields_to_update
            fields_to_update.update({"NtSa": data['net_salary']}) if 'net_salary' in data else fields_to_update
            fields_to_update.update({"TtPy": data['apply_timetable']}) if 'apply_timetable' in data else fields_to_update
            # add overload salary fields to the body
            if overload_fields is not None and 'salary' in overload_fields.keys():
                fields_to_update.update(overload_fields['salary'])

            salary['AfasSalary']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(salary)

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update({"DaEn": data['enddate_contract']}) if 'enddate_contract' in data else fields_to_update
        fields_to_update.update({"PEmTy": data['type_of_employment']}) if 'type_of_employment' in data else fields_to_update
        fields_to_update.update({"ViIe": data['termination_initiative']}) if 'termination_initiative' in data else fields_to_update
        fields_to_update.update({"ViRe": data['termination_reason']}) if 'termination_reason' in data else fields_to_update
        fields_to_update.update({"ViTo": data['probation_period']}) if 'probation_period' in data else fields_to_update
        fields_to_update.update({"DaEt": data['probation_enddate']}) if 'probation_enddate' in data else fields_to_update
        fields_to_update.update({"ClId": data['cao']}) if 'cao' in data else fields_to_update
        fields_to_update.update({"WcId": data['terms_of_employment']}) if 'terms_of_employment' in data else fields_to_update
        fields_to_update.update({"ApCo": data['type_of_contract']}) if 'type_of_contract' in data else fields_to_update
        fields_to_update.update({"CmId": data['employer_number']}) if 'employer_number' in data else fields_to_update
        fields_to_update.update({"EmMt": data['type_of_employee']}) if 'type_of_employee' in data else fields_to_update
        fields_to_update.update({"ViEt": data['employment']}) if 'employment' in data else fields_to_update
        fields_to_update.update({"StAc": data['seniority_date']}) if 'seniority_date' in data else fields_to_update
        fields_to_update.update({"DaSc": data['start_date_contract_chain']}) if 'start_date_contract_chain' in data else fields_to_update
        fields_to_update.update({"ViKe": data['contract_chain_code']}) if 'contract_chain_code' in data else fields_to_update
        fields_to_update.update({"DbYs": data['date_in_service_original']}) if 'date_in_service_original' in data else fields_to_update
        fields_to_update.update({"EnS2": data['number_income_ratio']}) if 'number_income_ratio' in data else fields_to_update
        # add overload contract fields to the body
        if overload_fields is not None and 'contract' in overload_fields.keys():
            fields_to_update.update(overload_fields['contract'])

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasContract']['Element']['Fields'].update(fields_to_update)

        if self.debug:
            print(json.dumps(base_body))

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_contract_with_rehire(self, data: dict, overload_fields: dict = None, method='POST') -> requests.Response:
        """
        :param data: Dictionary of fields that you want to update in AFAS. Only fields listed in allowed arrays are accepted. Fields listed in required fields array, are mandatory
        :param overload_fields: Dictionary of dictionaries. Specify sub dictionaries for each section you want to update.
        Specify as key which element you want to update, available options are: schedule, salary, contract, function.
        Example: overload_fields = {"employee": {"field": value}}
        :param method: request type
        :return: status code for request and optional error message
        """

        # Contract fields
        required_fields_contract = ['employee_id', 'startdate_contract']
        allowed_fields_contract = ['employee_id', 'type_of_employment', 'enddate_contract', 'termination_reason', 'termination_initiative', 'probation_period',
                                   'probation_enddate', 'cao', 'terms_of_employment', 'type_of_contract', 'employer_number', 'type_of_employee', 'employment'
                                   'seniority_date', 'contract_chain_code', 'start_date_contract_chain', 'number_income_ratio']

        # Function fields
        required_fields_function = ['organizational_unit', 'function_id', 'costcenter_id']
        allowed_fields_function = ['costcarrier_id']

        # Timetable fields
        required_fields_timetable = ['weekly_hours', 'parttime_percentage']
        allowed_fields_timetable = ['changing_work_pattern', 'days_per_week', 'fte', 'on-call_contract', 'type_of_schedule']

        # Workschedule fields (Optional: If one field is given, all 4 are required)
        fields_workschedule = ['startdate_workcycle', 'workcycle', 'start_week', 'index_number']

        # Salary fields
        required_fields_salary = ['type_of_salary', 'period_table']
        allowed_fields_salary = ['step', 'function_scale', 'salary_scale', 'salary_year', 'net_salary', 'apply_timetable', 'salary_amount']

        allowed_fields = allowed_fields_contract + allowed_fields_salary + allowed_fields_timetable + allowed_fields_function
        required_fields = required_fields_contract + required_fields_function + required_fields_timetable + required_fields_salary

        # Check if there are fields that are not allowed or fields missing that are required
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasContract')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Fields": {
                        "Bl": False
                    },
                    "Objects": {
                        "AfasContract": {
                            "Element": {
                                "@DaBe": data['startdate_contract'],
                                "Fields": {
                                }
                            }
                        }
                    }
                }
            }
        }

        # Extra JSON objects which are optional at contract creation
        function_dict = {
            "AfasOrgunitFunction": {
                "Element": {
                    "@DaBe": data['startdate_contract'],
                    "Fields": {
                    }
                }
            }
        }

        timetable = {
            "AfasTimeTable": {
                "Element": {
                    "@DaBg": data['startdate_contract'],
                    "Fields": {
                        "StPa": True
                    }
                }
            }
        }

        salary = {
            "AfasSalary": {
                "Element": {
                    "@DaBe": data['startdate_contract'],
                    "Fields": {
                    }
                }
            }
        }

        # If one of the optional fields of a subelement is included, we need to merge the whole JSON object to the basebody
        if any(field in data.keys() for field in allowed_fields_function):
            for field in required_fields_function:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for function are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"DpId": data['organizational_unit']}) if 'organizational_unit' in data else fields_to_update
            fields_to_update.update({"FuId": data['function_id']}) if 'function_id' in data else fields_to_update
            fields_to_update.update({"CrId": data['costcenter_id']}) if 'costcenter_id' in data else fields_to_update
            fields_to_update.update({"CcId": data['costcarrier_id']}) if 'costcarrier_id' in data else fields_to_update
            # add overload function fields to the body
            if overload_fields is not None and 'function' in overload_fields.keys():
                fields_to_update.update(overload_fields['function'])

            # merge subelement with basebody
            function_dict['AfasOrgunitFunction']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(function_dict)

        if any(field in data.keys() for field in allowed_fields_timetable):
            for field in required_fields_timetable:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for timetable are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"StPa": data['changing_work_pattern']}) if 'changing_work_pattern' in data else fields_to_update
            fields_to_update.update({"HrWk": data['weekly_hours']}) if 'weekly_hours' in data else fields_to_update
            fields_to_update.update({"PcPt": data['parttime_percentage']}) if 'parttime_percentage' in data else fields_to_update
            fields_to_update.update({"DyWk": data['days_per_week']}) if 'days_per_week' in data else fields_to_update
            fields_to_update.update({"Ft": data['fte']}) if 'fte' in data else fields_to_update
            fields_to_update.update({"ClAg": data['on-call_contract']}) if 'on-call_contract' in data else fields_to_update
            fields_to_update.update({"EtTy": data['type_of_schedule']}) if 'type_of_schedule' in data else fields_to_update
            # add overload schedule fields to the body
            if overload_fields is not None and 'schedule' in overload_fields.keys():
                fields_to_update.update(overload_fields['schedule'])

            timetable['AfasTimeTable']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(timetable)

        if any(field in data.keys() for field in fields_workschedule):
            for field in fields_workschedule:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for workschedule are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            workschedule = {
                "Objects": [
                    {
                        "AfasWorkTime": {
                            "Element": {
                                "@DaBe": data['startdate_workcycle'],
                                "Fields": {
                                    "Twcy": data['workcycle'],
                                    "Twcp": data['start_week'],
                                    "Twcc": data['index_number']
                                }
                            }
                        }
                    }
                ]
            }
            base_body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element'].update(workschedule)

        if any(field in data.keys() for field in allowed_fields_salary):
            for field in required_fields_salary:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for salaries are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            fields_to_update = {}
            fields_to_update.update({"SaSt": data['step']}) if 'step' in data else fields_to_update
            fields_to_update.update({"SaPe": data['type_of_salary']}) if 'type_of_salary' in data else fields_to_update
            fields_to_update.update({"EmSa": data['salary_amount']}) if 'salary_amount' in data else fields_to_update
            fields_to_update.update({"PtId": data['period_table']}) if 'period_table' in data else fields_to_update
            fields_to_update.update({"VaSc": data['salary_scale']}) if 'salary_scale' in data else fields_to_update
            fields_to_update.update({"FuSc": data['function_scale']}) if 'function_scale' in data else fields_to_update
            fields_to_update.update({"SaYe": data['salary_year']}) if 'salary_year' in data else fields_to_update
            fields_to_update.update({"NtSa": data['net_salary']}) if 'net_salary' in data else fields_to_update
            fields_to_update.update({"TtPy": data['apply_timetable']}) if 'apply_timetable' in data else fields_to_update
            # add overload salary fields to the body
            if overload_fields is not None and 'salary' in overload_fields.keys():
                fields_to_update.update(overload_fields['salary'])

            salary['AfasSalary']['Element']['Fields'].update(fields_to_update)
            base_body['AfasEmployee']['Element']['Objects'].update(salary)

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update({"DaEn": data['enddate_contract']}) if 'enddate_contract' in data else fields_to_update
        fields_to_update.update({"PEmTy": data['type_of_employment']}) if 'type_of_employment' in data else fields_to_update
        fields_to_update.update({"ViIe": data['termination_initiative']}) if 'termination_initiative' in data else fields_to_update
        fields_to_update.update({"ViRe": data['termination_reason']}) if 'termination_reason' in data else fields_to_update
        fields_to_update.update({"ViTo": data['probation_period']}) if 'probation_period' in data else fields_to_update
        fields_to_update.update({"DaEt": data['probation_enddate']}) if 'probation_enddate' in data else fields_to_update
        fields_to_update.update({"ClId": data['cao']}) if 'cao' in data else fields_to_update
        fields_to_update.update({"WcId": data['terms_of_employment']}) if 'terms_of_employment' in data else fields_to_update
        fields_to_update.update({"ApCo": data['type_of_contract']}) if 'type_of_contract' in data else fields_to_update
        fields_to_update.update({"CmId": data['employer_number']}) if 'employer_number' in data else fields_to_update
        fields_to_update.update({"EmMt": data['type_of_employee']}) if 'type_of_employee' in data else fields_to_update
        fields_to_update.update({"ViEt": data['employment']}) if 'employment' in data else fields_to_update
        fields_to_update.update({"StAc": data['seniority_date']}) if 'seniority_date' in data else fields_to_update
        fields_to_update.update({"DaSc": data['start_date_contract_chain']}) if 'start_date_contract_chain' in data else fields_to_update
        fields_to_update.update({"ViKe": data['contract_chain_code']}) if 'contract_chain_code' in data else fields_to_update
        fields_to_update.update({"EnS2": data['number_income_ratio']}) if 'number_income_ratio' in data else fields_to_update
        # add overload contract fields to the body
        if overload_fields is not None and 'contract' in overload_fields.keys():
            fields_to_update.update(overload_fields['contract'])

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasContract']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_function(self, data: dict, overload_fields: dict = None, method="PUT") -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :param method: PUT or POST, depending on the case
        :return: status code for request and optional error message
        """
        allowed_fields = ['formation', 'costcarrier', 'employment_number']
        required_fields = ['startdate', 'employee_id', 'organizational_unit', 'function', 'costcentre']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasOrgunitFunction')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "AfasOrgunitFunction": {
                            "Element": {
                                "@DaBe": data['startdate'],
                                "Fields": {
                                    "DpId": data['organizational_unit'],
                                    "FuId": data['function'],
                                    "CrId": data['costcentre']
                                }
                            }
                        }
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"FpId": data['formation']}) if 'formation' in data else fields_to_update
        fields_to_update.update({"CcId": data['costcarrier']}) if 'costcarrier' in data else fields_to_update
        fields_to_update.update({"DvSn": data['employment_number']}) if 'employment_number' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasOrgunitFunction']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_salary(self, data: dict, overload_fields: dict = None, method='PUT') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :param method: PUT or POST, depending on the case
        :return: status code for request and optional error message
        """
        allowed_fields = ['step', 'period_table', 'salary_year', 'function_scale', 'function_scale_type', 'salary_scale',
                          'salary_scale_type', 'salary_amount', 'net_salary', 'apply_timetable', 'employment_number']
        required_fields = ['startdate', 'employee_id', 'salary_type']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasSalary')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "AfasSalary": {
                            "Element": {
                                "@DaBe": data['startdate'],
                                "Fields": {
                                    "SaPe": data['salary_type'],
                                    "EmSa": data['salary_amount']
                                }
                            }
                        }
                    }
                }
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"SaSt": data['step']}) if 'step' in data else fields_to_update
        fields_to_update.update({"SaYe": data['salary_year']}) if 'salary_year' in data else fields_to_update
        fields_to_update.update({"PtId": data['period_table']}) if 'period_table' in data else fields_to_update.update({"PtId": 5})
        fields_to_update.update({"VaSc": data['salary_scale']}) if 'salary_scale' in data else fields_to_update
        fields_to_update.update({"TaId": data['salary_scale_type']}) if 'salary_scale_type' in data else fields_to_update
        fields_to_update.update({"FuSc": data['function_scale']}) if 'function_scale' in data else fields_to_update
        fields_to_update.update({"FuTa": data['function_scale_type']}) if 'function_scale_type' in data else fields_to_update
        fields_to_update.update({"NtSa": data['net_salary']}) if 'net_salary' in data else fields_to_update
        fields_to_update.update({"TtPy": data['apply_timetable']}) if 'apply_timetable' in data else fields_to_update
        fields_to_update.update({"DvSn": data['employment_number']}) if 'employment_number' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasSalary']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_subscription(self, data: dict, method: str, custom_fields: dict = None) -> requests.Response:
        """
        Update the subscriptions in AFAS Profit
        :param data: data to update. This is a dictionary with the subscription_id as key and the data to update as value
        :param method: method to use (POST or PUT). POST is used to create a new subscription, PUT is used to update an existing subscription
        :param custom_fields: custom fields to update. Give the key and the value of the field. For example: {'DFEDS8-DSF9uD-DDSA': 'value'}
        :return: the response from AFAS Profit
        """
        required_fields = ['subscription_id']
        allowed_fields = ['start_date_subscription', 'end_date_subscription', 'item_type_id', 'item_code', 'amount', 'subscription_line_id', 'start_date_subscription_line', 'end_date_subscription_line', 'reason_of_termination']

        # Check if the fields in data exists in the required or allowed fields
        self.__check_fields(data, required_fields, allowed_fields)

        if method != 'POST' and method != 'PUT' and method != 'DELETE':
            raise ValueError('The method should be POST, PUT or DELETE')

        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/FbSubscription/SuNr/{data['subscription_id']}"
            base_body = {}
        else:
            if 'subscription_line_id' in data.keys() or 'start_date_subscription_line' in data.keys():
                url = f'https://{self.environment}.{self.base_url}/ProfitRestServices/connectors/FbSubscription/FbSubscriptionLines/'
            else:
                url = f'https://{self.environment}.{self.base_url}/ProfitRestServices/connectors/FbSubscription/'

            base_body = {
                "FbSubscription": {
                    "Element": {
                        "Fields": {
                            "SuNr": data['subscription_id']
                        },
                        "Objects": {

                        }
                    }
                }
            }

            lines_body = {
                "FbSubscriptionLines": {
                    "Element": {
                        "Fields": {
                        }
                    }
                }
            }

            # If one of the optional fields of a subelement is included, we need to merge the whole JSON object to the basebody
            if any(field in data.keys() for field in allowed_fields):
                fields_to_update = {}
                fields_to_update.update({"VaIt": data['item_type_id']}) if 'item_type_id' in data else fields_to_update
                fields_to_update.update({"ItCd": data['item_code']}) if 'item_code' in data else fields_to_update
                fields_to_update.update({"Id": data['subscription_line_id']}) if 'subscription_line_id' in data else fields_to_update
                fields_to_update.update({"DaSt": data['start_date_subscription_line']}) if 'start_date_subscription_line' in data else fields_to_update
                fields_to_update.update({"DaEn": data['end_date_subscription_line']}) if 'end_date_subscription_line' in data else fields_to_update
                fields_to_update.update({"Qu": data['amount']}) if 'amount' in data else fields_to_update
                fields_to_update.update({"VaRs": data['reason_of_termination']}) if 'reason_of_termination' in data else fields_to_update

                # merge subelement with basebody if there are address fields added. If not, don't add the address part to the base_body
                if len(fields_to_update) > 0:
                    lines_body['FbSubscriptionLines']['Element']['Fields'].update(fields_to_update)
                    base_body['FbSubscription']['Element']['Objects'].update(lines_body)

            # Add allowed fields to the basebody if they are available in the data. Fields that are not exists in the basebody, should not be added tot this basebody to prevent errrors.
            fields_to_update = {}
            fields_to_update.update({"SuSt": data['start_date_subscription']}) if 'start_date_subscription' in data else fields_to_update
            fields_to_update.update({"SuEn": data['end_date_subscription']}) if 'end_date_subscription' in data else fields_to_update
            fields_to_update.update({"VaRs": data['reason_of_termination_subscription']}) if 'reason_of_termination_subscription' in data else fields_to_update
            base_body['FbSubscription']['Element']['Fields'].update(fields_to_update)

            # Now create a dict for all the custom fields. This fields are not by default added to the base_body because they're not always present in the dataset
            fields_to_update = {}
            fields_to_update.update(custom_fields) if custom_fields is not None else ''

            # Update the request body with update fields
            base_body['FbSubscription']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)
        return update

    def update_timetable(self, data: dict, overload_fields: dict = None, method="PUT") -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :param method: PUT or POST, depending on the case
        :return: status code for request and optional error message
        """

        allowed_fields = ['changing_work_pattern', 'days_per_week', 'fte', 'employment_number', 'type_of_schedule']
        required_fields = ['startdate', 'employee_id', 'weekly_hours', 'parttime_percentage']

        # Fields workschedule (Optional: If one field is given, all fields are required)
        fields_workschedule = ['startdate_workcycle', 'workcycle', 'start_week', 'index_number']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasTimeTable')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "AfasTimeTable": {
                            "Element": {
                                "@DaBg": data['startdate'],
                                "Fields": {
                                    "StPa": True,
                                    "HrWk": data['weekly_hours'],
                                    "PcPt": data['parttime_percentage']
                                }
                            }
                        }
                    }
                }
            }
        }

        if any(field in data.keys() for field in fields_workschedule):
            for field in fields_workschedule:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for workschedules are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            workschedule = {
                "Objects": [
                    {
                        "AfasWorkTime": {
                            "Element": {
                                "@DaBe": data['startdate_workcycle'],
                                "Fields": {
                                    "Twcy": data['workcycle'],
                                    "Twcp": data['start_week'],
                                    "Twcc": data['index_number']
                                }
                            }
                        }
                    }
                ]
            }
            base_body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element'].update(workschedule)

        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"StPa": data['changing_work_pattern']}) if 'changing_work_pattern' in data else fields_to_update
        fields_to_update.update({"DyWk": data['days_per_week']}) if 'days_per_week' in data else fields_to_update
        fields_to_update.update({"Ft": data['fte']}) if 'fte' in data else fields_to_update
        fields_to_update.update({"DvSn": data['employment_number']}) if 'employment_number' in data else fields_to_update
        fields_to_update.update({"EtTy": data['type_of_schedule']}) if 'type_of_schedule' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def new_wage_component(self, data: dict, overload_fields: dict = None, method="POST") -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['enddate', 'contract_no', 'apply_type']
        required_fields = ['employee_id', 'parameter', 'startdate', 'value']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/ProfitRestServices/connectors/HrVarValue/HrVarValue/VaId,Va,EmId,DaBe/{data['parameter']},{data['value']},{data['employee_id']},{data['startdate']}"
            base_body = {}
        else:
            url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'HrVarValue')
            base_body = {
                "HrVarValue": {
                    "Element": {
                        "Fields": {
                            "VaId": data['parameter'],
                            "Va": data['value'],
                            "EmId": data['employee_id'],
                            "DaBe": data['startdate']
                        }
                    }
                }
            }
            fields_to_update = {}

            # Add fields that you want to update a dict (adding to body itself is too much text)
            fields_to_update.update({"EnSe": data['contract_no']} if 'contract_no' in data else fields_to_update)
            fields_to_update.update({"DaEn": data['enddate']} if 'enddate' in data else fields_to_update)
            fields_to_update.update({"DiTp": data['apply_type']} if 'apply_type' in data else fields_to_update)

            fields_to_update.update(overload_fields) if overload_fields is not None else ''

            # Update the request body with update fields
            base_body['HrVarValue']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def new_wage_mutation(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        allowed_fields = ['period_table']
        required_fields = ['employee_id', 'year', 'month', 'employer_id', 'wage_component_id', 'value']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'HrCompMut')

        base_body = {
            "HrCompMut": {
                "Element": {
                    "@Year": data['year'],
                    "@PeId": data['month'],
                    "@EmId": data['employee_id'],
                    "@ErId": data['employer_id'],
                    "@Sc02": data['wage_component_id'],
                    "Fields": {
                        "VaD1": data['value']
                    }
                }
            }
        }
        fields_to_update = {}
        selector_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        selector_to_update.update({"@PtId": data['period_table']}) if 'period_table' in data else selector_to_update.update({"@PtId": 5})

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['HrCompMut']['Element']['Fields'].update(fields_to_update)
        base_body['HrCompMut']['Element'].update(selector_to_update)

        update = requests.request("POST", url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_bank_account(self, data: dict, overload_fields: dict = None, method='PUT') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['bankname', 'country', 'cash_payment', 'salary_bank_account', 'acc_outside_sepa', 'bank_type', 'iban_check', 'sequence_number', 'bic_code']
        required_fields = ['employee_id', 'iban']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnEmployee/AfasEmployee/@EmId/{data['employee_id']}/AfasBankInfo/SeNo/{data['sequence_number']}"
            base_body = {}
        else:
            url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee/AfasBankInfo')
            base_body = {
                "AfasEmployee": {
                    "Element": {
                        "@EmId": data['employee_id'],
                        "Objects": {
                            "AfasBankInfo": {
                                "Element": {
                                    "@NoBk": False,  # Cash payment (old)
                                    "Fields": {
                                        "IbCk": True,  # IBAN check (always true)
                                        "Iban": data['iban']  # "NL91ABNA0417164300"
                                    }
                                }
                            }
                        }
                    }
                }
            }

            fields_to_update = {}

            # Add fields that you want to update a dict (adding to body itself is too much text)
            fields_to_update.update({"BkIc": data['cash_payment']}) if 'bankname' in data else fields_to_update
            fields_to_update.update({"CoId": data['country']}) if 'country' in data else fields_to_update
            fields_to_update.update({"@NoBk": data['cash_payment']}) if 'cash_payment' in data else fields_to_update
            fields_to_update.update({"SaAc": data['salary_bank_account']}) if 'salary_bank_account' in data else fields_to_update
            fields_to_update.update({"FoPa": data['acc_outside_sepa']}) if 'acc_outside_sepa' in data else fields_to_update
            fields_to_update.update({"BkTp": data['bank_type']}) if 'bank_type' in data else fields_to_update
            fields_to_update.update({"IbCk": data['iban_check']}) if 'iban_check' in data else fields_to_update
            fields_to_update.update({"SeNo": data['sequence_number']}) if 'sequence_number' in data else fields_to_update
            fields_to_update.update({"Bic": data['bic_code']}) if 'bic_code' in data else fields_to_update

            fields_to_update.update(overload_fields) if overload_fields is not None else ''

            # Update the request body with update fields
            base_body['AfasEmployee']['Element']['Objects']['AfasBankInfo']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_bank_account_person(self, data: dict, overload_fields: dict = None, method='POST') -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :param method: request type
        :return: status code for request and optional error message
        """
        allowed_fields = ['bankname', 'country', 'bank_type', 'bic_code', 'match_employees_on', 'ssn']
        required_fields = ['person_id', 'iban', 'iban_check']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnPerson/KnBankAccount'
        base_body = {
            "KnPerson": {
                "Element": {
                    "Fields": {
                        "MatchPer": "1" if "match_employees_on" not in data else data['match_employees_on'],
                        "BcCo": data['person_id']
                    },
                    "Objects": {
                        "KnBankAccount": {
                            "Element": {
                                "Fields": {
                                    "Iban": data['iban'],
                                    "IbCk": data['iban_check']
                                }
                            }
                        }
                    }
                }
            }
        }

        fields_to_update = {}
        fields_to_update_person = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"CoId": data['country']}) if 'country' in data else fields_to_update
        fields_to_update.update({"BkTp": data['bank_type']}) if 'bank_type' in data else fields_to_update
        fields_to_update.update({"IbCk": data['iban_check']}) if 'iban_check' in data else fields_to_update
        fields_to_update.update({"Bic": data['bic_code']}) if 'bic_code' in data else fields_to_update
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        fields_to_update_person.update({"SoSe": data['ssn']}) if 'ssn' in data else fields_to_update_person

        # Update the request body with update fields
        base_body['KnPerson']['Element']['Objects']['KnBankAccount']['Element']['Fields'].update(fields_to_update)

        base_body['KnPerson']['Element']['Fields'].update(fields_to_update_person)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def new_employee_with_first_contract(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Any custom fields that are not in the allowed or required fields. Specify sub dictionaries for each section you want to update.
        Available options are: employee, person, contract, function, schedule, salary. Specify like: overload_fields = {"employee": {"field": value}}
        :return: status code for request and optional error message
        """

        # Person fields
        required_fields_person = ['last_name', 'gender', 'first_name', 'date_of_birth', 'country', 'ssn']
        allowed_fields_person = ['employee_id', 'date_of_death', 'initials', 'email_work', 'email_home', 'country_of_birth', 'place_of_birth', 'prefix',
                                 'birth_name_separate', 'name_use', 'send_payslip', 'send_annual_statement', 'match_employees_on', 'nickname', 'birthname', 'prefix_birthname', 'prefix_birthname_partner', 'birthname_partner',
                                 'mail_work', 'mail_private', 'mobile_work', 'mobile_private', 'marital_status', 'date_of_marriage', 'phone_work', 'phone_private', 'nationality', 'auto_number']

        # Address fields
        required_fields_address = ['house_number', 'street', 'street_number_add', 'postal_code', 'city', 'address_country']
        allowed_fields_address = ['search_address_by_postal_code']

        # contract fields
        required_fields_contract = ['date_effective', 'type_of_contract', 'collective_agreement', 'terms_of_employment', 'employment', 'type_of_employee', 'employer']
        allowed_fields_contract = ['end_date_contract', 'seniority_date', 'date_in_service_original', 'probation_period_code', 'end_date_probation_period', 'contract_chain_code', 'start_date_contract_chain', 'number_income_ratio']

        # function fields
        required_fields_function = ['organizational_unit', 'date_effective', 'function_id', 'costcenter', 'costcarrier']

        # schedule fields
        required_fields_schedule = ['weekly_hours', 'parttime_percentage']
        allowed_fields_schedule = ['changing_work_pattern', 'days_per_week', 'fte', 'type_of_schedule', 'on-call_contract']

        # workschedule fields (Optional: If one field is given, all fields are required)
        fields_workschedule = ['startdate_workcycle', 'workcycle', 'start_week', 'index_number']

        # salary fields
        required_fields_salary = ['type_of_salary']
        allowed_fields_salary = ['step', 'salary_scale', 'salary_scale_type', 'function_scale', 'function_scale_type', 'salary_year',
                                 'net_salary', 'apply_timetable', 'amount']

        allowed_fields = allowed_fields_person + allowed_fields_salary + allowed_fields_schedule + allowed_fields_contract + allowed_fields_address
        required_fields = required_fields_contract + required_fields_function + required_fields_schedule + required_fields_salary + required_fields_address + required_fields_person

        # Check if there are fields that are not allowed or fields missing that are required
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee')

        body = {
            "AfasEmployee": {
                "Element": {
                    # "@EmId": data['employee_id'],  # Employee selector
                    "Fields": {},
                    "Objects": {
                        "KnPerson": {
                            "Element": {
                                "Fields": {
                                    "PadAdr": False,  # Postbus adres
                                    "AutoNum": False if 'auto_number' not in data.keys() else data['auto_number'],  # Autonumber
                                    # Match existing employees on BSN [{"id":"0","description":"Zoek op BcCo (Persoons-ID)"},{"id":"1","description":"Burgerservicenummer"},{"id":"2","description":"Naam + voorvoegsel + initialen + geslacht"},{"id":"3","description":"Naam + voorvoegsel + initialen + geslacht + e-mail werk"},{"id":"4","description":"Naam + voorvoegsel + initialen + geslacht + mobiel werk"},{"id":"5","description":"Naam + voorvoegsel + initialen + geslacht + telefoon werk"},{"id":"6","description":"Naam + voorvoegsel + initialen + geslacht + geboortedatum"},{"id":"7","description":"Altijd nieuw toevoegen"}]
                                    "MatchPer": "1" if "match_employees_on" not in data.keys() else data['match_employees_on'],
                                    "BcCo": data['employee_id'],  # Employee ID
                                    "SeNm": data['last_name'][:10],  # Search name
                                    "FiNm": data['first_name'],  # First Name
                                    "LaNm": data['last_name'],  # Last Name
                                    "SpNm": False,  # Birthname seperately
                                    "NmBi": data['last_name'],  # Birthname
                                    # Use of name [{"id":"0","description":"Birth name"},{"id":"1","description":"Partner's birth name + Birth name"},{"id":"2","description":"Partner birth name"},{"id":"3","description":"Birth name + Partner's birth name"}]
                                    "ViUs": "0",
                                    # Gender [{"id":"M","description":"Male"},{"id":"U","description":"Unknown"},{"id":"F","description":"Female"}]
                                    "ViGe": data['gender'],
                                    "PsNa": data['country'],  # Nationality
                                    "DaBi": data['date_of_birth'],  # Birth date
                                    "SoSe": data['ssn']  # SSN
                                },
                                "Objects": [
                                    {
                                        "KnBasicAddressAdr": {
                                            "Element": {
                                                "Fields": {
                                                    "CoId": data['address_country'],  # Country
                                                    "PbAd": False,  # Postbusadres
                                                    "Ad": data['street'],  # Street
                                                    "HmNr": data['house_number'],  # Streetnumber
                                                    "HmAd": data['street_number_add'],  # Streetnumber addition
                                                    "ZpCd": data['postal_code'],  # Postal code
                                                    "Rs": data['city'],  # City
                                                    "ResZip": data['search_address_by_postal_code'] if 'search_address_by_postal_code' in data.keys() else True,
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "KnBasicAddressPad": {
                                            "Element": {
                                                "Fields": {
                                                    "CoId": data['address_country'],  # Country
                                                    "PbAd": False,  # Postbusadres
                                                    "Ad": data['street'],  # Street
                                                    "HmNr": data['house_number'],  # Streetnumber
                                                    "HmAd": data['street_number_add'],  # Streetnumber addition
                                                    "ZpCd": data['postal_code'],  # Postal code
                                                    "Rs": data['city'],  # City
                                                    "ResZip": data['search_address_by_postal_code'] if 'search_address_by_postal_code' in data.keys() else True,
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        "AfasContract": {
                            "Element": {
                                "@DaBe": data['date_effective'],
                                "Fields": {
                                    "ClId": data['collective_agreement'],  # Cao - fixed
                                    "WcId": data['terms_of_employment'],  # Arbeidsvoorwaarde - Fixed op zoetwarenindustrie - 36 uur
                                    "ApCo": data['type_of_contract'],  # Type of contract
                                    "CmId": data['employer'],  # employer - fixed
                                    "EmMt": data['type_of_employee'],  # Type of employee (1=personeelslid)
                                    "ViEt": data['employment']  # Dienstbetrekking
                                }
                            }
                        },
                        "AfasOrgunitFunction": {
                            "Element": {
                                "@DaBe": data['date_effective'],  # Startdate organizational unit
                                "Fields": {
                                    "DpId": data['organizational_unit'],  # OE
                                    "FuId": data['function_id'],  # Function 0232=medewerk(st)er
                                    "CcId": data['costcarrier'],  # fixed on default: Profit
                                    "CrId": data['costcenter']  # Cost center
                                }
                            }
                        },
                        "AfasTimeTable": {
                            "Element": {
                                "@DaBg": data['date_effective'],  # Startdate Timetable
                                "Fields": {
                                    "StPa": True,  # Wisselend arbeidspatroon
                                    "HrWk": data['weekly_hours'],  # Weekly hours
                                    "PcPt": data['parttime_percentage']  # Parttime percentage
                                }
                            }
                        },
                        "AfasSalary": {
                            "Element": {
                                "@DaBe": data['date_effective'],  # Startdate salary
                                "Fields": {
                                    "SaPe": data['type_of_salary'],  # Sort of salary - fixed (V=vast)
                                    "PtId": 5  # Period table - fixed (periode HRM)
                                }
                            }
                        }
                    }
                }
            }
        }

        if any(field in data.keys() for field in fields_workschedule):
            for field in fields_workschedule:
                if field not in data.keys():
                    raise KeyError('Field {field} is required. Required fields for workschedules are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

            workschedule = {
                "Objects": [
                    {
                        "AfasWorkTime": {
                            "Element": {
                                "@DaBe": data['startdate_workcycle'],
                                "Fields": {
                                    "Twcy": data['workcycle'],
                                    "Twcp": data['start_week'],
                                    "Twcc": data['index_number']
                                }
                            }
                        }
                    }
                ]
            }
            body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element'].update(workschedule)

        # Add overload fields to the base of the employee data
        fields_to_update_employee = {}
        fields_to_update_employee.update({"DaMa": data['date_of_marriage']}) if 'date_of_marriage' in data else fields_to_update_employee
        fields_to_update_employee.update({"DaDe": data['date_of_death']}) if 'date_of_death' in data else fields_to_update_employee
        fields_to_update_employee.update({"PsPv": data['send_payslip']}) if 'send_payslip' in data else fields_to_update_employee
        fields_to_update_employee.update({"YsPv": data['send_annual_statement']}) if 'send_annual_statement' in data else fields_to_update_employee
        body['AfasEmployee']['Element'].update({"@EmId": data['employee_id'] if "employee_id" in data else {}})
        # add overload employee fields to  the body
        if overload_fields is not None and 'employee' in overload_fields.keys():
            fields_to_update_employee.update(overload_fields['employee'])
        body['AfasEmployee']['Element']['Fields'].update(fields_to_update_employee)

        # Add overload fields to the base of the contract data
        fields_to_update_contract = {}
        fields_to_update_contract.update({"DaEn": data['end_date_contract']}) if 'end_date_contract' in data else fields_to_update_contract
        fields_to_update_contract.update({"StAc": data['seniority_date']}) if 'seniority_date' in data else fields_to_update_contract
        fields_to_update_contract.update({"ViTo": data['probation_period_code']}) if 'probation_period_code' in data else fields_to_update_contract
        fields_to_update_contract.update({"DaEt": data['end_date_probation_period']}) if 'end_date_probation_period' in data else fields_to_update_contract
        fields_to_update_contract.update({"DaSc": data['start_date_contract_chain']}) if 'start_date_contract_chain' in data else fields_to_update_contract
        fields_to_update_contract.update({"ViKe": data['contract_chain_code']}) if 'contract_chain_code' in data else fields_to_update_contract
        fields_to_update_contract.update({"DbYs": data['date_in_service_original']}) if 'date_in_service_original' in data else fields_to_update_contract
        fields_to_update_contract.update({"EnS2": data['number_income_ratio']}) if 'number_income_ratio' in data else fields_to_update_contract
        # add overload contract fields to  the body
        if overload_fields is not None and 'contract' in overload_fields.keys():
            fields_to_update_contract.update(overload_fields['contract'])
        body['AfasEmployee']['Element']['Objects']['AfasContract']['Element']['Fields'].update(fields_to_update_contract)

        # Add overload fields to the base of the salary data
        fields_to_update_salary = {}
        fields_to_update_salary.update({"SaSt": data['step']}) if 'step' in data else fields_to_update_salary
        fields_to_update_salary.update({"SaYe": data['salary_year']}) if 'salary_year' in data else fields_to_update_salary
        fields_to_update_salary.update({"PtId": data['period_table']}) if 'period_table' in data else fields_to_update_salary.update({"PtId": 5})
        fields_to_update_salary.update({"VaSc": data['salary_scale']}) if 'salary_scale' in data else fields_to_update_salary
        fields_to_update_salary.update({"TaId": data['salary_scale_type']}) if 'salary_scale_type' in data else fields_to_update_salary
        fields_to_update_salary.update({"FuSc": data['function_scale']}) if 'function_scale' in data else fields_to_update_salary
        fields_to_update_salary.update({"FuTa": data['function_scale_type']}) if 'function_scale_type' in data else fields_to_update_salary
        fields_to_update_salary.update({"NtSa": data['net_salary']}) if 'net_salary' in data else fields_to_update_salary
        fields_to_update_salary.update({"TtPy": data['apply_timetable']}) if 'apply_timetable' in data else fields_to_update_salary
        fields_to_update_salary.update({"EmSa": data['amount']}) if 'amount' in data else fields_to_update_salary
        if overload_fields is not None and 'salary' in overload_fields.keys():
            fields_to_update_salary.update(overload_fields['salary'])
        # Update the request body with update fields
        body['AfasEmployee']['Element']['Objects']['AfasSalary']['Element']['Fields'].update(fields_to_update_salary)

        # Add overload fields to the base of the person data
        fields_to_update_person = {}
        fields_to_update_person.update({"In": data['initials']}) if 'initials' in data else fields_to_update_person
        fields_to_update_person.update({"CoBi": data['country_of_birth']}) if 'country_of_birth' in data else fields_to_update_person
        fields_to_update_person.update({"RsBi": data['place_of_birth']}) if 'place_of_birth' in data else fields_to_update_person
        fields_to_update_person.update({"IsBi": data['birthname_prefix']}) if 'birthname_prefix' in data else fields_to_update_person
        fields_to_update_person.update({"NmBi": data['birthname']}) if 'birthname' in data else fields_to_update_person
        fields_to_update_person.update({"IsPa": data['prefix_birthname_partner']}) if 'prefix_birthname_partner' in data else fields_to_update_person
        fields_to_update_person.update({"NmPa": data['birthname_partner']}) if 'birthname_partner' in data else fields_to_update_person
        fields_to_update_person.update({"EmAd": data['email_work']}) if 'email_work' in data else fields_to_update_person
        fields_to_update_person.update({"EmA2": data['email_home']}) if 'email_home' in data else fields_to_update_person
        fields_to_update_person.update({"SpNm": data['birth_name_separate']}) if 'birth_name_separate' in data else fields_to_update_person
        fields_to_update_person.update({"ViUs": data['name_use']}) if 'name_use' in data else fields_to_update_person
        fields_to_update_person.update({"Is": data['prefix']}) if 'prefix' in data else fields_to_update_person
        fields_to_update_person.update({"CaNm": data['nickname']}) if 'nickname' in data else fields_to_update_person
        fields_to_update_person.update({"EmAd": data['mail_work']}) if 'mail_work' in data else fields_to_update_person
        fields_to_update_person.update({"EmA2": data['mail_private']}) if 'mail_private' in data else fields_to_update_person
        fields_to_update_person.update({"MbNr": data['mobile_work']}) if 'mobile_work' in data else fields_to_update_person
        fields_to_update_person.update({"MbN2": data['mobile_private']}) if 'mobile_private' in data else fields_to_update_person
        fields_to_update_person.update({"CaNm": data['nickname']}) if 'nickname' in data else fields_to_update_person
        fields_to_update_person.update({"PsNa": data['nationality']}) if 'nationality' in data else fields_to_update_person
        fields_to_update_person.update({"ViCs": data['marital_status']}) if 'marital_status' in data else fields_to_update_person
        fields_to_update_person.update({"DaMa": data['date_of_marriage']}) if 'date_of_marriage' in data else fields_to_update_person
        fields_to_update_person.update({"TeNr": data['phone_work']}) if 'phone_work' in data else fields_to_update_person
        fields_to_update_person.update({"TeN2": data['phone_private']}) if 'phone_private' in data else fields_to_update_person
        if overload_fields is not None and 'person' in overload_fields.keys():
            fields_to_update_person.update(overload_fields['person'])
        # Update the request body with update fields
        body['AfasEmployee']['Element']['Objects']['KnPerson']['Element']['Fields'].update(fields_to_update_person)

        # Add overload fields to the base of the schedule data
        fields_to_update_schedule = {}
        fields_to_update_schedule.update({"StPa": data['changing_work_pattern']}) if 'changing_work_pattern' in data else fields_to_update_schedule
        fields_to_update_schedule.update({"DyWk": data['days_per_week']}) if 'days_per_week' in data else fields_to_update_schedule
        fields_to_update_schedule.update({"Ft": data['fte']}) if 'fte' in data else fields_to_update_schedule
        fields_to_update_schedule.update({"EtTy": data['type_of_schedule']}) if 'type_of_schedule' in data else fields_to_update_schedule
        fields_to_update_schedule.update({"ClAg": data['on-call_contract']}) if 'on-call_contract' in data else fields_to_update_schedule
        if overload_fields is not None and 'schedule' in overload_fields.keys():
            fields_to_update_schedule.update(overload_fields['schedule'])
        # Update the request body with update fields
        body['AfasEmployee']['Element']['Objects']['AfasTimeTable']['Element']['Fields'].update(fields_to_update_schedule)

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update_organisational_unit = {}
        if overload_fields is not None and 'organisational_unit' in overload_fields.keys():
            fields_to_update_organisational_unit.update(overload_fields['organisational_unit'])
        # Update the request body with update fields
        body['AfasEmployee']['Element']['Objects']['AfasOrgunitFunction']['Element']['Fields'].update(fields_to_update_organisational_unit)

        if self.debug:
            print(json.dumps(body))

        update = requests.request('POST', url, data=json.dumps(body), headers=self.headers)

        return update

    def create_sickleave(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """

        allowed_fields = {
            'safety_net': 'SfNt',
            'end_date': 'DaEn',
            'end_date_report_date': 'DMeE',
            'reason_ending': 'ViRs',
            'end_date_expected': 'DaEs',
            'available_first_day': 'TPBe',
            'total_hours': 'ThAb'
        }
        required_fields = ['employee_id', 'start_date', 'start_date_report_date', 'type_of_sickleave', 'percentage_available']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "HrIllness": {
                "Element": {
                    "Fields": {
                        "EmId": f"{data['employee_id']}",
                        "DaBe": f"{data['start_date']}",
                        "DMeB": f"{data['start_date_report_date']}",
                        "ViIt": f"{data['type_of_sickleave']}"
                    },
                    "Objects": [
                        {
                            "HrAbsIllnessProgress": {
                                "Element": {
                                    "Fields": {
                                        "DaTi": f"{data['start_date']}",
                                        "PsPc": f"{data['percentage_available']}"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['HrIllness']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['HrIllness']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        update = requests.post(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrIllness', data=json.dumps(base_body), headers=self.headers)

        return update

    def update_sickleave(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        allowed_fields = {
            'safety_net': 'SfNt',
            'end_date': 'DaEn',
            'end_date_report_date': 'DMeE',
            'reason_ending': 'ViRs',
            'start_date': 'DaBe',
            'start_date_report_date': 'DMeB',
            'end_date_expected': 'DaEs',
            'available_first_day': 'TPBe',
            'type_of_sickleave': 'ViIt',
            'total_hours': 'ThAb'
        }
        required_fields = ['guid']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "HrIllnessGUID": {
                "Element": {
                    "@GUID": f"{data['guid']}",
                    "Fields": {
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['HrIllnessGUID']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['HrIllnessGUID']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.put(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrIllnessGUID',
                                data=json.dumps(base_body), headers=self.headers)

        return response

    def delete_sickleave(self, sickleave_guid: Union[int, str]) -> requests.Response:
        response = requests.delete(url=f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrIllnessGUID/HrIllnessGUID/@GUID/{sickleave_guid}",
                                   headers=self.headers)
        return response

    def create_leave(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :return: status code for request and optional error message
        """
        allowed_fields = {
            'total_hours': "DuRa",
            'partial_leave': "LeDt",
            'employment_id': "EnSe",
            'reason_of_leave': "ViLr",
            'leave_id': "Id"
        }
        required_fields = ['employee_id', 'start_date', 'end_date', 'type_of_leave']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "HrAbsence": {
                "Element": {
                    "Fields": {
                        "EmId": data["employee_id"],
                        "ViAt": data["type_of_leave"],
                        "DaBe": data["start_date"],
                        "DaEn": data["end_date"]
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['HrAbsence']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['HrAbsence']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.post(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrAbsence',
                                 data=json.dumps(base_body), headers=self.headers)

        return response

    def update_leave(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :return: status code for request and optional error message
        """
        allowed_fields = {
            "total_hours": "DuRa",
            "partial_leave": "LeDt",
            "employment_id": "EnSe",
            "reason_of_leave": "ViLr",
            "leave_id": "Id",
            "employee_id": "EmId",
            "type_of_leave": "ViAt",
            "start_date": "DaBe",
            "end_date": "DaEn"
        }
        required_fields = ['leave_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "HrAbsenceID": {
                "Element": {
                    "Fields": {
                        "Id": data["leave_id"]
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['HrAbsenceID']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['HrAbsenceID']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.put(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrAbsenceID',
                                data=json.dumps(base_body),
                                headers=self.headers)

        return response

    def delete_leave(self, leave_id: Union[int, str]) -> requests.Response:
        """
        method used to delete leave from AFAS
        :param leave_id: leave id, may be a string or number
        :return: response object
        """
        response = requests.delete(url=f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrAbsenceID/HrAbsenceID/Id/{leave_id}",
                                   headers=self.headers)

        return response

    def create_leave_balance(self, data: dict, overload_fields: dict = None) -> requests.Response:
        # has to be implemented still. Different endpoint then leave balance corrections
        pass

    def update_leave_balance(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :return: status code for request and optional error message
        """
        allowed_fields = {
            "correction_reason": "ViCr",
            "booking_date": "RgDa",
            "employment_id": "EnSe",
            "note": "Re",
            "process_in_payroll": "CcPy",
            "leave_balance": "BlId",
            "weeks": "CoWk"
        }
        required_fields = ['employee_id', 'type_of_leave', 'hours']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "HrAbsCorrection": {
                "Element": {
                    "Fields": {
                        "EmId": data["employee_id"],
                        "ViAt": data["type_of_leave"],
                        "HhMm": data["hours"]
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['HrAbsCorrection']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['HrAbsCorrection']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.post(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrAbsCorrection',
                                 data=json.dumps(base_body),
                                 headers=self.headers)

        return response

    def create_post_calculation(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :return: status code for request and optional error message
        """
        allowed_fields = {
            'id': "Id",
            'external_key': "XpRe",
            'quantity': "Qu",
            'employee_id': "EmId",
            'type_of_hours': "StId",
            "costcenter_employee": "CrId",
            "approved": "Ap",
            "description": "Ds",
            "project_id": "PrId",
            "project_phase": "PrSt",
            "specification_axis_code_1": "V1Cd",
            "specification_axis_code_2": "V2Cd",
            "specification_axis_code_3": "V3Cd",
            "specification_axis_code_4": "V4Cd",
            "specification_axis_code_5": "V5Cd"
        }
        required_fields = ['date', 'item_type', 'item_code']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "PtRealization": {
                "Element": {
                    "Fields": {
                        "DaTi": data["date"],
                        "VaIt": data["item_type"],
                        "ItCd": data["item_code"]
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['PtRealization']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['PtRealization']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.post(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/PtRealization',
                                 data=json.dumps(base_body), headers=self.headers)

        return response

    def update_post_calculation(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Custom Fields with custom ID's can be entered here with key: value
        :return: status code for request and optional error message
        """
        allowed_fields = {
            'external_key': "XpRe",
            'quantity': "Qu",
            'employee_id': "EmId",
            'type_of_hours': "StId",
            'date': "DaTi",
            'item_type': "VaIt",
            'item_code': "ItCd",
            "costcenter_employee": "CrId",
            "approved": "Ap",
            "description": "Ds",
            "project_id": "PrId",
            "project_phase": "PrSt",
            "specification_axis_code_1": "V1Cd",
            "specification_axis_code_2": "V2Cd",
            "specification_axis_code_3": "V3Cd",
            "specification_axis_code_4": "V4Cd",
            "specification_axis_code_5": "V5Cd"
        }
        required_fields = ['id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        base_body = {
            "PtRealization": {
                "Element": {
                    "Fields": {
                        "Id": data["id"]
                    }
                }
            }
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            base_body['PtRealization']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add custom fields to the body
        base_body['PtRealization']['Element']['Fields'].update(overload_fields) if overload_fields is not None else ''

        response = requests.put(url=f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/PtRealization',
                                data=json.dumps(base_body),
                                headers=self.headers)

        return response

    def delete_post_calculation(self, post_calculation_id: Union[int, str], date: str) -> requests.Response:
        """
        method used to delete postcalculation from AFAS
        :param post_calculation_id: post_calculation_id id, may be a string or number
        :param date: date, must be yyyy-mm-dd, is DaTi from original booking
        :return: response object
        """
        response = requests.delete(url=f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/PtRealization/PtRealization/Id,DaTi/{post_calculation_id},{date}",
                                   headers=self.headers)

        return response

    def update_cost_center(self, data: dict, method: str, custom_fields: dict = None) -> requests.Response:
        """
        This function updates HR cost centers with the AFAS updateconnect 'HrCosteCentre'.
        :param data: Deliver all the data which should be updated in list format. The data should at least contain the required_fields and can contain also the allowed fields
        :param method: Is a PUT for an update of an existing cost center. is a POST for an insert of a new cost center
        :param custom_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: The status code from AFAS Profit
        """
        required_fields = ['cost_center_id', 'cost_center_description', 'employer_id', 'blocked']
        allowed_fields = ['cost_center_type']

        # Check if the fields in data exists in the required or allowed fields
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method != 'PUT' and method != 'POST' and method != 'DELETE':
            raise ValueError('Parameter method should be PUT, POST or DELETE (in uppercase)')

        # Do a delete call if the method is a delete. Delete do not need a body
        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrCostCentre/HrCostCentre/CmId,CrId,CrDs,Bl/{data['employer_id']},{data['cost_center_id']},{data['cost_center_description']},{data['blocked']}"
            base_body = {}
        else:
            url = 'https://{}.{}/profitrestservices/connectors/HrCostCentre'.format(self.environment, self.base_url)

            base_body = {
                "HrCostCentre": {
                    "Element": {
                        "Fields": {
                            "CmId": data['employer_id'],
                            "CrId": data['cost_center_id'],
                            "CrDs": data['cost_center_description'],
                            "Bl": data['blocked']
                        }
                    }
                }
            }

            # Now create a dict for all the allowed fields. This fields are not by default added to the base_body because they're not always present in the dataset
            fields_to_update = {}
            fields_to_update.update({"CrTy": data['cost_center_type']}) if 'cost_center_type' in data else fields_to_update

            # Also add custom_fields to the base_body.
            fields_to_update.update(custom_fields) if custom_fields is not None else ''

            # Update the request body with update fields
            base_body['HrCostCentre']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def update_cost_carrier(self, data: dict, method: str, custom_fields: dict = None) -> requests.Response:
        """
        This function updates HR cost carriers with the AFAS updateconnect 'HrCosteCarrier'.
        :param data: Deliver all the data which should be updated in list format. The data should at least contain the required_fields and can contain also the allowed fields
        :param method: Is a PUT for an update of an existing cost carrier. is a POST for an insert of a new cost carrier
        :param custom_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: The status code from AFAS Profit
        """
        required_fields = ['cost_carrier_id', 'cost_carrier_description', 'employer_id', 'blocked']
        allowed_fields = []

        # Check if the fields in data exists in the required or allowed fields
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method != 'PUT' and method != 'POST' and method != 'DELETE':
            raise ValueError('Parameter method should be PUT, POST or DELETE (in uppercase)')

        if method == 'DELETE':
            url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrCostCarrier/HrCostCarrier/CmId,CcId,CcDs,Bl/{data['employer_id']},{data['cost_carrier_id']},{data['cost_carrier_description']},{data['blocked']}"
            base_body = {}
        else:
            url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'HrCostCarrier')

            base_body = {
                "HrCostCarrier": {
                    "Element": {
                        "Fields": {
                            "CmId": data['employer_id'],
                            "CcId": data['cost_carrier_id'],
                            "CcDs": data['cost_carrier_description'],
                            "Bl": data['blocked']
                        }
                    }
                }
            }

            # Now create a dict for all the custom fields. This fields are not by default added to the base_body because they're not always present in the dataset
            fields_to_update = {}
            fields_to_update.update(custom_fields) if custom_fields is not None else ''

            # Update the request body with update fields
            base_body['HrCostCarrier']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def terminate_employee(self, data: dict, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        allowed_fields = ['termination_initiative']
        required_fields = ['employee_id', 'termination_date', 'end_date_contract', 'start_date_contract']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'KnEmployee')

        base_body = {
            "AfasEmployee": {
                "Element": {
                    "@EmId": data['employee_id'],
                    "Objects": {
                        "AfasContract": {
                            "Element": {
                                "@DaBe": data['start_date_contract'],
                                "Fields": {
                                    "DaEn": data['end_date_contract'],
                                    "DaEe": data['termination_date']
                                }
                            }
                        }
                    }
                }
            }
        }

        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"ViIe": data['termination_initiative']}) if 'termination_initiative' in data else fields_to_update
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body['AfasEmployee']['Element']['Objects']['AfasContract']['Element']['Fields'].update(fields_to_update)

        update = requests.request("PUT", url, data=json.dumps(base_body), headers=self.headers)

        return update

    def create_dossieritem_reaction(self, data: dict, attachments: dict = None) -> requests.Response:
        allowed_fields = {
            'reaction_to': 'RTId',
        }
        required_fields = ['dossieritem_id', 'reaction', 'reaction_visibility']

        required_fields_attachment = ['filename', 'attachment_filepath']
        allowed_fields_attachment = []

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnSubjectReaction"

        payload = {
            "KnReaction": {
                "Element": {
                    "Fields": {
                        "SbId": data['dossieritem_id'],  # Dossieritem ID
                        "SbTx": data['reaction'],  # reaction text
                        "VaRe": data['reaction_visibility']  # either I for Internal or IE for Internal and External
                    }
                }
            }
        }
        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['KnReaction']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        if attachments is not None:
            attachment_basebody = {
                "Objects": [
                ]
            }

            for attachment in attachments:
                self.__check_fields(data=attachment, required_fields=required_fields_attachment, allowed_fields=allowed_fields_attachment)
                attachment_body = {
                    "KnReactionAttachment": {
                        "Element": {
                            "Fields": {
                                "FileName": attachment['filename'],
                                "FileStream": base64.b64encode(bytearray(open(attachment['attachment_filepath'], mode='rb').read())).decode("utf-8")
                            }
                        }
                    }
                }
                attachment_basebody['Objects'].append(attachment_body)

            # now update main body with attachment body
            payload['KnReaction']['Element'].update(attachment_basebody)

        if self.debug:
            print(json.dumps(payload))

        update = requests.post(url, data=json.dumps(payload), headers=self.headers)

        return update

    def upload_dossieritem(self, data: dict, attachments: Union[list[dict], None] = None, overload_fields: list = None) -> requests.Response:
        """
        :param data: any fields that are in required and allowed_fields
        :param attachments: list of dicts that should each contain a filename and attachment_filepath
        :param overload_fields: list of dicts that should each contain a complete object for a free dossieritem. Example:
        [{
            "KnS15": {
                "Element": {
                    "@SbId": dossieritemId,
                    "Fields": {
                        "U51DC4BF14827261B10A2F69D9B460346": "value1",
                        "U5CAEF2DE4FD25D4E7AA8B99999969318": "value2",
                    }
                }
            }
        }]
        :return: response
        """
        allowed_fields = {
            'subject': 'Ds',
            'note': 'SbTx',
            'date_created': 'Da',
            'created_by': 'UsId',
            'person_responsible': 'EmId',
            'is_done': 'St',
            'property_1': 'FvF1',
            'property_2': 'FvF2',
            'property_3': 'FvF3',
            'save_file_with_subject': 'FileTrans',
            'profile_id': 'ProfileId'
        }
        allowed_fields_subject_link = {
            'sales_administration_id': "SiUn",
            'sales_invoice_type_id': "SiTp",
            'sales_invoice_id': "SiId",
            'purchase_administration_id': "PiUn",
            'purchase_invoice_type_id': "PiTp",
            'purchase_invoice_id': "PiId",
            'project_id': "PjId",
            'campaign_id': "CaId",
            'active': "FaSn",
            'precalculation_id': "QuId",
            'subscription_id': "SuNr",
            'item_type': "VaIt",
            'item_code': "BiId",
            'course_id': "CrId",
            'forecast_id': "FoSn",
            'car_id': "CcSn",
            'organizational_unit': "OE",
            'purchase_order_id': "Por",
            'sales_offer_id': "Squ",
            'sales_order_id': "Sor",
            'purchase_offer_id': "Pqu",
            'location_id': "LoId",
            'application_id': "ApId",
            "to_purchase_relation": "ToPR",
            "to_sales_relation": "ToSR",
            "to_applicant": "ToAp",
            "to_employee": "ToEm",
            "to_person": "ToBC",
            "destination_type_id": "SfTp",
            # this field is a bit tricky. This is actually the destination, which mostly will be the employee ID
            # However it can also contain other IDs such as the purchase relation ID or the applicant ID.
            # It should never contain the person_id, that should go in the person_id field. This logic is very weird but thats how AFAS wants it
            "destination": "SfId",
            # Usually employee_id is used instead of destination, but if you want to use destination, you can use this field to specify the type of destination
            "employee_id": "SfId",
            "person_id": "BcId",
        }
        required_fields = ['dossieritem_type_id']

        required_fields_attachment = ['filename', 'attachment_filepath']
        allowed_fields_attachment = []

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))
        if "employee_id" not in data and "person_id" not in data:
            warnings.warn("Either employee_id or person_id should likely be specified")
        if "employee_id" in data and "destination" in data:
            raise ValueError("Either employee_id or destination should be specified, not both")

        url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/KnSubject"

        payload = {
            "KnSubject": {
                "Element": {
                    # "@SbId": id, # optional dossieritem ID
                    "Fields": {
                        "StId": data['dossieritem_type_id'],  # Dossieritem type
                        "Ds": data['subject'] if 'subject' in data else data['filename'],  # this is for legacy reasons, used to be same as filename
                    },
                    "Objects": [
                        {
                            "KnSubjectLink": {
                                "Element": {
                                    # "@SbId": id, # optional dossieritem ID
                                    "Fields": {
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['KnSubject']['Element']['Fields'].update({allowed_fields[field]: data[field]})

        # Add allowed fields to the body
        for field in (allowed_fields_subject_link.keys() & data.keys()):
            payload['KnSubject']['Element']['Objects'][0]['KnSubjectLink']['Element']['Fields'].update({allowed_fields_subject_link[field]: data[field]})

        # check if the attachments parameter is specified, if not, use the legacy way (does not support multiple attachments)
        if attachments is None and 'filename' in data and 'attachment_filepath' in data:
            attachments = [{"filename": data['filename'],
                            "attachment_filepath": data['attachment_filepath']}]
        elif attachments is None:
            attachments = []

        # add overload objects to  the body (custom dossieritems)
        for dossieritem in overload_fields:
            payload['KnSubject']['Element']['Objects'].append(dossieritem)

        for attachment in attachments:
            self.__check_fields(data=attachment, required_fields=required_fields_attachment, allowed_fields=allowed_fields_attachment)
            attachment_body = {
                "KnSubjectAttachment": {
                    "Element": {
                        "Fields": {
                            "FileName": attachment['filename'],
                            "FileStream": base64.b64encode(bytearray(open(attachment['attachment_filepath'], mode='rb').read())).decode("utf-8")
                        }
                    }
                }
            }
            payload['KnSubject']['Element']['Objects'].append(attachment_body)

        if self.debug:
            print(json.dumps(payload))

        update = requests.post(url, data=json.dumps(payload), headers=self.headers)

        return update

    def create_journalentries(self, df: pd.DataFrame):
        """
        This function can be used to upload journalentries to Afas profit
        :param df: The dataframe with the journal entries of a certain administration id specified.
        :return: upload_summary containing a string with information about the upload
        :return: status_codes containing the status codes corresponding to the upload_summary
        """
        # Check if all necessary columns are present
        columns_in_df = df.columns.tolist()
        required_fields_financial_entry = ['general_ledger_id', 'cost_centre_id', 'description', 'date_approved', 'date_booking', 'booking_number', 'debet', 'credit', 'year', 'period', 'administration_id', 'journal_id']
        self.__check_fields(data=columns_in_df, required_fields=required_fields_financial_entry, allowed_fields=[])

        upload_summary = []
        status_codes = []  # extract all period and year data as a list and drop duplicates from the list
        df['unique_period_year_per_administration'] = df['period'].astype(str) + df['year'].astype(str) + df['administration_id'].astype(str) + df['journal_id'].astype(str)
        year_period_per_administration_list = df['unique_period_year_per_administration'].unique().tolist()
        for unique_period in year_period_per_administration_list:
            df_period = df[df['unique_period_year_per_administration'] == unique_period]
            # drop the columns that are not needed for the upload iteration
            df_period = df_period.sort_values(by=['booking_number', 'date_booking'])
            # pass the index payload and the dataframe to the upload method
            update = self.__create_journalentry_for_period(df=df_period)
            json_update = update.json()
            # get values from first row of df (all rows are the same for the same period)
            df_period_values = df.to_dict(orient='records')[0]
            if 200 <= update.status_code < 300:
                upload_summary.append(f"Journal entries for year {df_period_values['year']}, period {df_period_values['period']}, adminstration {df_period_values['administration_id']} and journal {df_period_values['journal_id']} uploaded successfully. Status code: {update.status_code}")
                status_codes.append(update.status_code)
            else:
                upload_summary.append(f"Journal entries for year {df_period_values['year']}, period {df_period_values['period']}, adminstration {df_period_values['administration_id']} and journal {df_period_values['journal_id']} failed. Status code: {update.status_code} {json_update['externalMessage']}")
                status_codes.append(update.status_code)

        return upload_summary, status_codes

    def __create_journalentry_for_period(self, df: pd.DataFrame) -> requests.Response:
        """
        This function is an internal function used in conjunction with upload_journalentries. This function updates Afas profit for updateconnector: 'Fientries'.
        :param df: The dataframe with the journal entries for the year period and administration id specified in the data. This dataframe needs debit and credit values that equal out per booking number.
        :return: The response from AFAS Profit
        """
        base_body = {
            "FiEntryPar": {
                "Element": {
                    "Fields": {
                        "Year": df.iloc[0]['year'],
                        "Peri": df.iloc[0]["period"],
                        "UnId": df.iloc[0]['administration_id'],
                        "JoCo": df.iloc[0]['journal_id']
                    },
                    "Objects": [
                        {
                            "FiEntries": {
                                "Element": []
                            }
                        }
                    ]
                }
            }
        }
        for row in df.to_dict(orient='records'):
            single_entry = {
                "Fields": {
                    "VaAs": "1",
                    "AcNr": row["general_ledger_id"],
                    "EnDa": row['date_booking'],
                    "BpDa": row['date_approved'],
                    "BpNr": row['booking_number'],
                    "Ds": row['description'],
                    "AmDe": row['debet'],
                    "AmCr": row['credit']
                },
                "Objects": [
                    {
                        "FiDimEntries": {
                            "Element": {
                                "Fields": {
                                    "DiC1": row['cost_centre_id'],
                                    "DiC2": row['cost_carrier_id']
                                }
                            }
                        }
                    }
                ]
            }
            base_body['FiEntryPar']["Element"]["Objects"][0]["FiEntries"]["Element"].append(single_entry)

        json_body = json.dumps(base_body)
        update = requests.request("POST", url=f'https://{self.environment}.{self.base_url}/ProfitRestServices/connectors/FiEntries', data=json_body, headers=self.headers)

        return update

    def update_applicant(self, data: dict, method: str, overload_fields: dict = None) -> requests.Response:
        """
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param method: Method to be used in update function
        :param overload_fields: overload_fields: The custom fields in this dataset. Give the key of the field and the value. For example: {DFEDS8-DSF9uD-DDSA: 'Vrij veld'}
        :return: status code for request and optional error message
        """
        required_fields = ['last_name', 'gender', 'application_number']
        allowed_fields = ['initials', 'first_name', 'date_of_birth', 'email', 'mobile_phone', 'country', 'street', 'housenumber',
                          'housenumber_addition', 'postal_code', 'city', 'site_guid', 'work_email', 'person_id']

        # Check if the fields in data exists in the required or allowed fields
        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        if method != 'PUT' and method != 'POST':
            raise ValueError('Parameter method should be PUT or POST (in uppercase)')

        if method == 'DELETE':
            raise ValueError('Parameter method should NOT be DELETE')
        else:
            url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, 'HrCreateApplicant')

            base_body = {
                "HrCreateApplicant": {
                    "Element": {
                        "Fields": {
                            "VcSn": data['application_number'],
                            "LaNm": data['last_name'],  # prefix incorporated
                            "ViGe": data['gender']  # M, O, V of X
                        }
                    }
                }
            }

            # Add allowed fields to the basebody if they are available in the data. Fields that are not exists in the basebody, should not be added tot this basebody to prevent errors.
            fields_to_update = {}
            fields_to_update.update({"In": data['initials']}) if 'initials' in data else fields_to_update  # initials, afleiden van de naam
            fields_to_update.update({"FiNm": data['first_name']}) if 'first_name' in data else fields_to_update  # first name
            fields_to_update.update({"DaBi": data['date_of_birth']}) if 'date_of_birth' in data else fields_to_update  # "YYYY-MM-DD", date of birth
            fields_to_update.update({"EmA2": data['email']}) if 'email' in data else fields_to_update  # private email
            fields_to_update.update({"EmAd": data['work_email']}) if 'work_email' in data else fields_to_update  # private email
            fields_to_update.update({"MbN2": data['mobile_phone']}) if 'mobile_phone' in data else fields_to_update  # private mobile phone
            fields_to_update.update({"CoId": data['country']}) if 'country' in data else fields_to_update  # country, default at Stibbe is NL
            fields_to_update.update({"Ad": data['street']}) if 'street' in data else fields_to_update
            fields_to_update.update({"HmNr": data['housenumber']}) if 'housenumber' in data else fields_to_update
            fields_to_update.update({"HmAd": data['housenumber_addition']}) if 'housenumber_addition' in data else fields_to_update
            fields_to_update.update({"ZpCd": data['postal_code']}) if 'postal_code' in data else fields_to_update
            fields_to_update.update({"Rs": data['city']}) if 'city' in data else fields_to_update
            fields_to_update.update({"StId": data['site_guid']}) if 'site_guid' in data else fields_to_update
            fields_to_update.update({"BcCo": data['person_id']}) if 'person_id' in data else fields_to_update

            base_body['HrCreateApplicant']['Element']['Fields'].update(fields_to_update)

            # Now create a dict for all the custom fields. This fields are not by default added to the base_body because they're not always present in the dataset
            fields_to_update = {}
            fields_to_update.update(overload_fields) if overload_fields is not None else ''

            # Update the request body with possibly extra fields as defined in the script
            base_body['HrCreateApplicant']['Element']['Fields'].update(fields_to_update)

        update = requests.request(method, url, data=json.dumps(base_body), headers=self.headers)

        return update

    def upload_payslip(self, data: dict) -> requests.Response:
        """
        This method is for uploading payslip dossieritems on the internal AFAS dossieritem type (-2).
        :param data:
        :return:
        """
        allowed_fields = []
        required_fields = ['filename', 'subject', 'employee_id', 'attachment_filepath']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        url = f"https://{self.environment}.{self.base_url}/profitrestservices/connectors/HrEmpPaySlip"

        payload = {
            "HrEmpPaySlip": {
                "Element": {
                    "Fields": {
                        "EmId": data['employee_id'],
                        "Ds": data['subject'],
                        "FileName": data['filename'],
                        "FileStream": base64.b64encode(bytearray(open(data['attachment_filepath'], mode='rb').read())).decode("utf-8")
                    }
                }
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers=self.headers)

        return response

    def post(self, rest_type, updateconnector, data) -> requests.Response:
        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, updateconnector)

        update = requests.request(rest_type, url, data=data, headers=self.headers)

        return update

    @staticmethod
    def __check_fields(data: Union[dict, List], required_fields: List, allowed_fields: List):
        if isinstance(data, dict):
            data = data.keys()

        for field in data:
            if field not in allowed_fields and field not in required_fields:
                warnings.warn('Field {field} is not implemented. Optional fields are: {allowed_fields}'.format(field=field, allowed_fields=tuple(allowed_fields)))

        for field in required_fields:
            if field not in data:
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))
