import logging
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from enum import Enum

log = logging.getLogger(__name__)


class Observable:
    # A set of all attributes which get changed
    changed_attributes = set()

    def __init__(self):
        self.observed = defaultdict(list)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        for observer in self.observed.get(name, []):
            observer(name)

    def add_observer(self, name):
        self.observed[name].append(lambda name: self.changed_attributes.add(name))


def sanitise_args(obj: Observable, args, kwargs):
    kwarg_dict = dict()
    obj.changed_attributes = set()

    for arg in args:
        if isinstance(arg, dict):
            kwarg_dict.update(arg)

    for k, v in kwargs.items():
        if hasattr(type(obj), k):
            kwarg_dict[k] = v
            obj.changed_attributes.add(k)
        else:
            log.debug(f"{obj.__class__.__name__}.{k} - attribute ignored.")
            # raise ValueError(f"No such attribute: {k}")

    return kwarg_dict


class SortAlgorithm(Enum):
    SERVER_DEFAULT = 0,
    FUZZY_MATCH = 1


@dataclass
class Relay(Observable):
    digitalOutputStatus: str = ""
    uid: str = ""
    number: int = 0
    name: str = ""
    description: any = None
    weeklyProgramUID: any = None
    controllerUID: str = ""
    liftReaderUID: any = None
    constantState: str = ""
    apiKey: any = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        relay_dict = sanitise_args(self, args, kwargs)

        for property_name in relay_dict:
            if isinstance(relay_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, relay_dict[property_name])

        # Monitor Changes
        for k, v in asdict(self).items():
            if isinstance(v, (str, type(None), bool, int)):
                self.add_observer(k)

    def _remove_non_changed(self, relay_dict: dict):
        for key, value in list(relay_dict.items()):
            if key not in self.changed_attributes:
                relay_dict.pop(key)
        return relay_dict

    def dict(self, editable_only=False, changed_only=False):
        relay_dict = {}
        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                relay_dict[k] = v
            elif isinstance(v, type(None)):
                relay_dict[k] = None
            else:
                relay_dict[k] = str(v)

        if editable_only:
            if 'uid' in relay_dict:
                relay_dict.pop('uid')

        if changed_only:
            relay_dict = self._remove_non_changed(relay_dict)

        return relay_dict


@dataclass
class Card(Observable):
    technologyType: int = 0
    description: str = ""
    cardCode: str = ""
    status: str = "Free"
    cardholderUID: any = None
    cardType: str = "Magnetic"
    readerFunctionUID: any = None
    uid: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        card_dict = sanitise_args(self, args, kwargs)

        for property_name in card_dict:
            if isinstance(card_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, card_dict[property_name])

        # Monitor Changes
        for k, v in asdict(self).items():
            if isinstance(v, (str, type(None), bool, int)):
                self.add_observer(k)

    def _remove_non_changed(self, ch: dict):
        for key, value in list(ch.items()):
            if key not in self.changed_attributes:
                ch.pop(key)
        return ch

    def dict(self, editable_only=False, changed_only=False):
        c = {}
        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                c[k] = v
            elif isinstance(v, type(None)):
                c[k] = None
            else:
                c[k] = str(v)

        if editable_only:
            if 'uid' in c:
                c.pop('uid')
            if 'readerFunctionUID' in c:
                c.pop('readerFunctionUID')

        if changed_only:
            c = self._remove_non_changed(c)

        return c


@dataclass
class Area:
    uid: str = ""
    name: str = ""

    def __init__(self, area_dict: dict):
        for property_name in area_dict:
            if isinstance(area_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, area_dict[property_name])

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class SecurityGroup:
    ownerSiteUID: str = ""
    uid: str = ""
    name: str = ""
    apiKey: any = ""
    description: str = ""
    isAppliedToVisitor: bool = False

    def __init__(self, security_group_dict: dict):
        for property_name in security_group_dict:
            if isinstance(security_group_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, security_group_dict[property_name])

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class ScheduledMag(Observable):
    uid: str = ""
    securityGroupAPIKey: str = ""
    scheduledSecurityGroupUID: str = ""
    cardholderUID: str = ""
    toDateValid: str = ""
    fromDateValid: str = ""
    status: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        scheduled_mags_dict = sanitise_args(self, args, kwargs)

        # Initialise clss attributes from dictionary
        for property_name in scheduled_mags_dict:
            if isinstance(scheduled_mags_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, scheduled_mags_dict[property_name])
                self.add_observer(property_name)

    def dict(self, editable_only=False):
        c = {}
        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                c[k] = v
            elif isinstance(v, type(None)):
                c[k] = None
            else:
                c[k] = str(v)

        if editable_only:
            if 'uid' in c:
                c.pop('uid')
            if 'status' in c:
                c.pop('status')

        return c


@dataclass
class CardholderCustomizedField(Observable):
    uid: str = ""
    cF_BoolField_1: bool = False,
    cF_BoolField_2: bool = False
    cF_BoolField_3: bool = False
    cF_BoolField_4: bool = False
    cF_BoolField_5: bool = False
    cF_IntField_1: int = 0
    cF_IntField_2: int = 0
    cF_IntField_3: int = 0
    cF_IntField_4: int = 0
    cF_IntField_5: int = 0
    cF_DateTimeField_1: any = None
    cF_DateTimeField_2: any = None
    cF_DateTimeField_3: any = None
    cF_DateTimeField_4: any = None
    cF_DateTimeField_5: any = None
    cF_StringField_1: str = ""
    cF_StringField_2: str = ""
    cF_StringField_3: str = ""
    cF_StringField_4: str = ""
    cF_StringField_5: str = ""
    cF_StringField_6: str = ""
    cF_StringField_7: str = ""
    cF_StringField_8: str = ""
    cF_StringField_9: str = ""
    cF_StringField_10: str = ""
    cF_StringField_11: str = ""
    cF_StringField_12: str = ""
    cF_StringField_13: str = ""
    cF_StringField_14: str = ""
    cF_StringField_15: str = ""
    cF_StringField_16: str = ""
    cF_StringField_17: str = ""
    cF_StringField_18: str = ""
    cF_StringField_19: str = ""
    cF_StringField_20: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        custom_fields_dict = sanitise_args(self, args, kwargs)

        for property_name in custom_fields_dict:
            if isinstance(custom_fields_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, custom_fields_dict[property_name])

        # Monitor Changes
        for k, v in asdict(self).items():
            if isinstance(v, (str, type(None), bool, int)):
                self.add_observer(k)

    def dict(self, changed_only=False):
        c = dict()
        for k, v in asdict(self).items():
            if isinstance(v, (bool, int)):
                c[k] = v
            elif isinstance(v, int):
                c[k] = v
            elif isinstance(v, type(None)):
                c[k] = None
            else:
                c[k] = str(v)

        if changed_only:
            c = self._remove_non_changed(c)

        return c

    def _remove_non_changed(self, ch: dict):
        for key, value in list(ch.items()):
            if key not in self.changed_attributes:
                ch.pop(key)
        return ch


@dataclass
class CardholderPersonalDetail(Observable):
    uid: str = ""
    officePhone: str = ""
    cityOrDistrict: str = ""
    streetOrApartment: str = ""
    postCode: str = ""
    privatePhoneOrFax: str = ""
    mobile: str = ""
    email: str = ""
    carRegistrationNum: str = ""
    company: str = ""
    idFreeText: str = ""
    idType: str = "IdentityCard"

    def __init__(self, *args, **kwargs):
        super().__init__()
        person_details_dict = sanitise_args(self, args, kwargs)

        for property_name in person_details_dict:
            if isinstance(person_details_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, person_details_dict[property_name])

        # Monitor Changes
        for k, v in asdict(self).items():
            if isinstance(v, (str, type(None), bool, int)):
                self.add_observer(k)

    def dict(self, editable_only=False, changed_only=False, non_empty_only=False):
        ch = dict()

        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                ch[k] = v
            elif isinstance(v, type(None)):
                pass
                # ch[k] = None
            elif isinstance(v, str):
                if non_empty_only:
                    if len(v) > 0:
                        ch[k] = str(v)
                else:
                    ch[k] = str(v)
            else:
                pass

        if changed_only:
            ch = self._remove_non_changed(ch)

        if editable_only:
            ch = self._remove_non_editable(ch)

        return ch

    def _remove_non_changed(self, ch: dict):
        for key, value in list(ch.items()):
            if key not in self.changed_attributes:
                ch.pop(key)
        return ch

    @staticmethod
    def _remove_non_editable(ch: dict):
        if 'uid' in ch:
            ch.pop('uid')
        return ch


@dataclass
class CardholderType:
    uid: str = ""
    typeName: str = ""
    defaultBPTemplate: str = ""

    def __init__(self, cardholder_type_dict: dict):
        for property_name in cardholder_type_dict:
            if isinstance(cardholder_type_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, cardholder_type_dict[property_name])

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class Cardholder(Observable):
    uid: str = ""
    lastName: str = ""
    firstName: str = ""
    cardholderIdNumber: any = None
    status: any = None
    fromDateValid: any = None
    isFromDateActive: any = None
    toDateValid: any = None
    isToDateActive: any = None
    photo: any = None
    cardholderType: CardholderType = None
    securityGroup: SecurityGroup = None
    cardholderPersonalDetail: CardholderPersonalDetail = None
    cardholderCustomizedField: CardholderCustomizedField = None
    insideArea: Area = None
    ownerSiteUID: str = ""
    securityGroupApiKey: any = None
    ownerSiteApiKey: any = None
    accessGroupApiKeys: any = None
    liftAccessGroupApiKeys: any = None
    cardholderTypeUID: str = ""
    departmentUID: any = None
    description: str = ""
    grantAccessForSupervisor: any = None
    isSupervisor: any = None
    needEscort: any = None
    personalWeeklyProgramUID: any = None
    pinCode: str = ""
    sharedStatus: str = ""
    securityGroupUID: str = ""
    accessGroupUIDs: any = None
    liftAccessGroupUIDs: any = None
    lastDownloadTime: any = None
    lastInOutArea: str = ""
    lastInOutReaderUID: any = None
    lastInOutDate: any = None
    lastAreaReaderDate: any = None
    lastAreaReaderUID: any = None
    lastPassDate: any = None
    lastReaderPassUID: any = None
    insideAreaUID: str = ""
    cards: list = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        cardholder_dict = sanitise_args(self, args, kwargs)

        for property_name in cardholder_dict:
            if isinstance(cardholder_dict[property_name], list):
                if property_name == "cards":
                    setattr(self, property_name, [])
                    for card_entry in cardholder_dict[property_name]:
                        if isinstance(card_entry, Card):
                            self.cards.append(card_entry)
                        else:
                            self.cards.append(Card(card_entry))
                else:
                    setattr(self, property_name, cardholder_dict[property_name])

            if property_name == "cardholderPersonalDetail":
                if isinstance(cardholder_dict[property_name], CardholderPersonalDetail):
                    self.cardholderPersonalDetail = cardholder_dict[property_name]

            if property_name == "cardholderCustomizedField":
                if isinstance(cardholder_dict[property_name], CardholderCustomizedField):
                    self.cardholderCustomizedField = cardholder_dict[property_name]

            if isinstance(cardholder_dict[property_name], dict):
                if property_name == "insideArea":
                    self.insideArea = Area(cardholder_dict[property_name])
                if property_name == "securityGroup":
                    self.securityGroup = SecurityGroup(cardholder_dict[property_name])
                if property_name == "cardholderType":
                    self.cardholderType = CardholderType(cardholder_dict[property_name])
                if property_name == "cardholderPersonalDetail":
                    self.cardholderPersonalDetail = CardholderPersonalDetail(cardholder_dict[property_name])
                if property_name == "cardholderCustomizedField":
                    self.cardholderCustomizedField = CardholderCustomizedField(cardholder_dict[property_name])

            if isinstance(cardholder_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, cardholder_dict[property_name])

        # Monitor Changes
        for k, v in asdict(self).items():
            if isinstance(v, (str, type(None), bool, int)):
                self.add_observer(k)

    def to_search_pattern(self):
        pattern = ""
        if self.firstName:
            pattern += self.firstName + " "
        if self.lastName:
            pattern += self.lastName + " "
        if self.cardholderPersonalDetail:
            if self.cardholderPersonalDetail.company:
                pattern += self.cardholderPersonalDetail.company + " "
            if self.cardholderPersonalDetail.email:
                pattern += self.cardholderPersonalDetail.email
        return pattern

    def pretty_print(self, obj: object = None):
        if obj is None:
            obj = self
        for attribute_name in obj.__dict__:
            if attribute_name != 'observed':
                attribute = getattr(obj, attribute_name)
                if isinstance(attribute, list):
                    print(f"{attribute_name}:")
                    print(f"\t{str(attribute)}")
                elif hasattr(attribute, '__dict__'):
                    print(f"{attribute_name}:")
                    obj.pretty_print(attribute)
                else:
                    print(f"\t{attribute_name:<25}" + str(attribute))

    def dict(self, editable_only=False, changed_only=False, non_empty_only=False):
        ch = dict()

        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                ch[k] = v
            elif isinstance(v, type(None)):
                if not non_empty_only:
                    ch[k] = None
            elif isinstance(v, str):
                if non_empty_only:
                    if len(v) > 0:
                        ch[k] = str(v)
                else:
                    ch[k] = str(v)
            else:
                pass

        if changed_only:
            ch = self._remove_non_changed(ch)

        if editable_only:
            ch = self._remove_non_editable(ch)

        return ch

    def _remove_non_changed(self, ch: dict):
        for key, value in list(ch.items()):
            if key not in self.changed_attributes:
                ch.pop(key)
        return ch

    @staticmethod
    def _remove_non_editable(ch: dict):
        if 'uid' in ch:
            ch.pop('uid')
        if 'ownerSiteUID' in ch:
            ch.pop('ownerSiteUID')
        if 'lastDownloadTime' in ch:
            ch.pop('lastDownloadTime')
        if 'lastInOutArea' in ch:
            ch.pop('lastInOutArea')
        if 'lastInOutReaderUID' in ch:
            ch.pop('lastInOutReaderUID')
        if 'lastInOutDate' in ch:
            ch.pop('lastInOutDate')
        if 'lastAreaReaderDate' in ch:
            ch.pop('lastAreaReaderDate')
        if 'lastAreaReaderUID' in ch:
            ch.pop('lastAreaReaderUID')
        if 'lastPassDate' in ch:
            ch.pop('lastPassDate')
        if 'lastReaderPassUID' in ch:
            ch.pop('lastReaderPassUID')
        if 'status' in ch:
            ch.pop('status')
        if 'insideArea' in ch:
            ch.pop('insideArea')
        if 'cardholderPersonalDetail' in ch:
            ch.pop('cardholderPersonalDetail')
        if 'cardholderCustomizedField' in ch:
            ch.pop('cardholderCustomizedField')
        if 'cardholderType' in ch:
            ch.pop('cardholderType')
        if 'securityGroup' in ch:
            ch.pop('securityGroup')
        if 'cards' in ch:
            ch.pop('cards')
        if 'accessGroupUIDs' in ch:
            ch.pop('accessGroupUIDs')
        if 'liftAccessGroupUIDs' in ch:
            ch.pop('liftAccessGroupUIDs')

        return ch


if __name__ == "__main__":
    cardholdertype = CardholderType(typeName="test")
    print(cardholdertype.typeName)

    '''securityGroup = SecurityGroup(ownerSiteUID="1234",
                                  uid="sdfs", name="test", apiKey="None", description="test", isAppliedToVisitor=False)
    print(securityGroup.name)
    print(securityGroup.uid)'''
