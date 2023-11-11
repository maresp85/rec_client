from users.models import User, Enterprise


class CreateUser:
    def __init__(self, data, referred_code, company_id, request=None):
        self._data = data
        self._referred_code = referred_code
        self._company_id = company_id

    def execute(self):
        self._created_from_server = False
        if 'created_from_server' in self._data:
            self._created_from_server = True

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
            user.created_from_server = self._created_from_server
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
        
        user.save()