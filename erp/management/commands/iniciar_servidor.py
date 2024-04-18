from django.core.management.base import BaseCommand

from api.empresas.models import empresa
from api.autenticacao.models import Cargo
from api.usuarios.models import usuario

class Command(BaseCommand):
    help = 'Cria uma empresa, um cargo e um usuário de exemplo.'

    def handle(self, *args, **options):
        # Cria a empresa
        empresa_teste, created = empresa.objects.get_or_create(
            nome='Minha Empresa Teste',
            cnpj='12.345.678/9012-34',
            telefone='(12) 34567-8910',
            telefone_whatsapp='(12) 34567-8910',
            email='empresa@teste.com',
            endereco='Endereço da Empresa Teste'
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Empresa criada com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Empresa já existe.'))

        # Cria o cargo Administrador
        cargo_admin, created = Cargo.objects.get_or_create(
            nome='Administrador',
            descricao='Cargo de administrador da empresa',
            empresa=empresa_teste,
            nivel_acesso=10
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Cargo criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Cargo já existe.'))

        # Cria o usuário administrador
        usuario_admin, created = usuario.objects.get_or_create(
            nome='Admin teste',
            email='adm@gmail.com',
            telefone='(12) 34567-8910',
            empresa=empresa_teste,
            cargo=cargo_admin,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        if created:
            usuario_admin.password = 'teste123'  # Define a senha
            usuario_admin.save()
            self.stdout.write(self.style.SUCCESS('Usuário criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Usuário já existe.'))


        self.stdout.write(self.style.SUCCESS('Empresa, cargo e usuário criados com sucesso!'))
