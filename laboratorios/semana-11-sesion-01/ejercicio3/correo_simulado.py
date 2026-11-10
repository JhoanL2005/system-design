"""Un proveedor de correo de mentira: en vez de enviar, imprime el correo y
lo guarda en la lista ENVIADOS. Ya esta completo: no lo modifiques."""

ENVIADOS = []


def enviar_correo(destinatario, asunto):
    ENVIADOS.append((destinatario, asunto))
    print("[correo para " + destinatario + "] " + asunto)
