import re

def tratar_erros_serializer(errors):
    messages = []
    for field, error_list in errors.items():
        for error in error_list:
            if 'required' in error.code:
                messages.append(f"O campo {field} é requerido")
            elif 'blank' in error.code:
                messages.append(f"O campo {field} não pode estar em branco")
            elif 'unique' in error.code:
                messages.append(f"Esse {field} já está em uso")
            elif 'max_digits' in error.code:
                messages.append(f"O campo {field.replace('_', ' ').title()} não pode ter mais de {extrair_max_digits(error)} dígitos no total")
            else:
                messages.append(f"Erro no campo {field}: {error}")

    return ', '.join(messages)

def extrair_max_digits(error_message):
    match = re.search(r'Ensure that there are no more than (\d+) digits', error_message)
    if match:
        return match.group(1)
    return None