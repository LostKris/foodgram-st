import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core_models.models import Ingredient

_NAME_KEY = "name"
_MEASUREMENT_UNIT_KEY = "measurement_unit"
_INGREDIENT_REQUIRED_FIELDS = (_NAME_KEY, _MEASUREMENT_UNIT_KEY)
INGREDIENT_FILE = "data/ingredients.json"


class Command(BaseCommand):
    help = "Загрузка ингредиентов из JSON файла"

    def handle(self, *args, **kwargs):
        file_path: Path = Path(settings.BASE_DIR) / INGREDIENT_FILE

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR(f"Файл {file_path} не найден"),
            )
            return

        try:
            with open(file_path, "r", encoding="utf-8") as ingredients_file:
                file_content = ingredients_file.read()
        except IOError as ioError:
            self.stdout.write(
                self.style.ERROR(f"Ошибка чтения файла: {ioError}"),
            )
            return

        try:
            ingredient_list = json.loads(file_content)
        except json.JSONDecodeError as jsonDecodeError:
            self.stdout.write(
                self.style.ERROR(f"Ошибка парсинга JSON: {jsonDecodeError}"),
            )
            return
        if not isinstance(ingredient_list, list):
            self.stdout.write(self.style.ERROR("JSON должен содержать массив"))
            return

        created_count = sum(
            (1 for ingredient in ingredient_list
                if self._handle_ingredient(ingredient))
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно обработано {len(ingredient_list)} записей. "
                f"Создано новых: {created_count}"
            )
        )

    def _handle_ingredient(self, ingredient):
        if not isinstance(ingredient, dict):
            self.stdout.write(
                self.style.WARNING("Пропущен невалидный элемент"),
            )
            return False
        if not all(
            (field in ingredient for field in _INGREDIENT_REQUIRED_FIELDS),
        ):
            self.stdout.write(
                self.style.WARNING(
                    f"Пропущен ингредиент с неполными данными: {ingredient}",
                )
            )
            return False

        try:
            name = ingredient[_NAME_KEY]
            unit = ingredient[_MEASUREMENT_UNIT_KEY]
        except KeyError as keyError:
            self.stdout.write(
                self.style.ERROR(f"Отсутствует ключ: {keyError}"),
            )
            return False

        try:
            _, created = Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=unit,
                defaults={_NAME_KEY: name, _MEASUREMENT_UNIT_KEY: unit},
            )
        except Exception as exception:
            self.stdout.write(
                self.style.ERROR(
                    f"Ошибка при создании ингредиента {name}: {exception}",
                )
            )
            return False

        return created
