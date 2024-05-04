from django.test import TestCase

class ErpTestCase(TestCase):
    def print_test_success(self, test_name):
        print(f"\033[92m{test_name} passou\033[00m")  # \033[92m é a cor verde, \033[00m é a cor padrão

    def print_test_error(self, test_name):
        print(f"\033[91m{test_name} falhou\033[00m")

    def assertEqual(self, first, second, msg=None):
        test_name = self.id().split('.')[-1]
        if first == second:
            self.print_test_success(test_name)
        else:
            self.print_test_error(test_name)
            super().assertEqual(first, second, msg)
