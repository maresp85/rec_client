from django.contrib import messages
from django.shortcuts import redirect
from social_core.exceptions import AuthAlreadyAssociated


def handle_auth_already_associated(backend, uid, user=None, *args, **kwargs):
    """
    Si el correo de Google ya está asociado a otro usuario,
    muestra un mensaje amigable en vez del error 500.
    """
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)

    if social:
        if user and social.user != user:
            messages.error(
                backend.strategy.request,
                'Este correo ya está siendo utilizado por otro cliente. '
                'Por favor, utilice un correo diferente.'
            )
            return redirect('login')

    return None
