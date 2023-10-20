import io
import os
from typing import Optional
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.test import tag

from config.settings import env, DATA_FILES_DIR

username = env.str('SUPERUSER_USERNAME')
password = env.str('SUPERUSER_PASSWORD')


@tag('long_upload')
class BaseTestCase(TestCase):
    command_name: Optional[str] = None

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test class with output capture for 'import_cities' command."""
        super().setUpClass()
        cls.captured_output: io.StringIO = io.StringIO()
        cls.run_import_cities_command(cls.captured_output)

    @classmethod
    def run_import_cities_command(cls, captured_output: io.StringIO) -> None:
        """Run the 'import_cities' command with output capture."""
        with patch('sys.stdout', new=captured_output):
            call_command(cls.command_name)


class CreateSuperuserCommandTest(BaseTestCase):
    command_name = 'create_admin'

    def test_check_superuser_attributes(self) -> None:
        """Check superuser attributes."""
        superuser: User = User.objects.get(username='admin')
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.email, 'admin@admin.ru')

    def test_superuser_creation_output(self) -> None:
        """Test output when creating a superuser for the first time."""

        exp_output: str = (
            f'Created superuser {username} with password - {password}'
        )
        output_text: str = self.captured_output.getvalue()
        self.assertIn(exp_output, output_text)

    def test_existing_superuser_output(self) -> None:
        """Test output when a superuser already exists."""
        exp_output: str = f'The user with username {username} already exists'
        # Re-run
        self.run_import_cities_command(self.captured_output)
        output_text: str = self.captured_output.getvalue()
        self.assertIn(exp_output, output_text)


class ExcelImportTest(BaseTestCase):
    command_name = 'import_cities'

    def test_successful_data_import_output(self) -> None:
        """Test output when creating a superuser for the first time."""
        exp_output: str = 'Data uploaded successfully'
        output_text: str = self.captured_output.getvalue()
        self.assertIn(exp_output, output_text)

    def test_no_new_data_import_output(self) -> None:
        """Test output when a file already upload."""
        exp_output: str = 'No new cities to upload'
        ExcelImportTest.run_import_cities_command(self.captured_output)
        output_text: str = self.captured_output.getvalue()
        self.assertIn(exp_output, output_text)

    def test_missing_file_error_handling(self) -> None:
        """Test 'import_cities' command when the source file is renamed temporarily."""
        # Source file
        exp_output: str = 'File not found.'
        source_file_name: str = 'spisok_gorodov_RU.xlsx'
        source_path = os.path.join(DATA_FILES_DIR, source_file_name)
        new_path = os.path.join(DATA_FILES_DIR, 'new_file.xlsx')

        # Temporarily change the file name
        os.rename(source_path, new_path)

        self.run_import_cities_command(self.captured_output)
        output_text: str = self.captured_output.getvalue()
        self.assertIn(exp_output, output_text)

        # Rename the file back to its original name to restore it
        os.rename(new_path, source_path)
