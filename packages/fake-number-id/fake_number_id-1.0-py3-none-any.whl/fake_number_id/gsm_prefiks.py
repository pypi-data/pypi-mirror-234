from faker import Faker
import phonenumbers


def telepon(operator: str, international: bool = False) -> str:
    fake = Faker(locale="id_iD")
    nomor = '{0}{1}'.format(operator.value, fake.msisdn()[5:])
    nomor_seri = phonenumbers.parse(nomor, "ID")
    if international:
        return phonenumbers.format_number(nomor_seri, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    else:
        return phonenumbers.format_number(nomor_seri, phonenumbers.PhoneNumberFormat.NATIONAL)

def layanan_operator(operator: str) -> tuple[str]:
    data = str(operator).split('.')
    return (data[0], operator.value)
