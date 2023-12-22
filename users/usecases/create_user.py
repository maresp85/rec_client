from users.models import Enterprise, User


class CreateUser:
    def __init__(self, data: dict, referred_code: str, company_id: int, ip_address: str):
        self._data: dict = data
        self._referred_code: str = referred_code
        self._company_id: int = company_id
        self._ip_address: str = ip_address

    def execute(self):
        self._company = Enterprise.objects.filter(id=self._company_id).first()
        
        self._create_user()  

    def _create_user(self):
        user = User.objects.filter(username=self._data['document_number'].strip()).first()

        if not user:
            user = User.objects.create_user(
                self._data['document_number'].strip(),
                '',
                'secret*rec_client_2022'
            )
            user.client_id = int(self._data['id']) if 'id' in self._data else None
            user.first_name = self._data['first_name']
            user.last_name = self._data['last_name']
            user.mobile_number = self._data['mobile_number']
            user.address = self._data['address']
            user.address_payment = self._data['address_payment']
            user.city = self._data['city'] if 'city' in self._data else None
            user.document_number = self._data['document_number'].strip()
            user.referred_code = self._referred_code if self._referred_code else None
            user.company = self._company
        else:
            user.first_name = self._data['first_name']
            user.last_name = self._data['last_name']
            user.mobile_number = self._data['mobile_number']
            user.address = self._data['address']
            user.address_payment = self._data['address_payment']
            user.company = self._company

        user.ip_address = self._ip_address

        user.save()
