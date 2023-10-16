from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Run all data loading commands in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display verbose output for all commands',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']

        # Run the load_unit_data command
        self.stdout.write(self.style.SUCCESS("Running load_unit_data..."))
        call_command('load_unit_data', verbose=verbose)

        # Rund the load_information_source command
        self.stdout.write(self.style.SUCCESS("Running load_information_source..."))
        call_command('load_information_source', verbose=verbose)

        self.stdout.write(self.style.SUCCESS("All data loading commands executed successfully."))
