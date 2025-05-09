from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        verbose_name='название',
        max_length=128,
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=64,
    )
    
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]
    
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    name = models.CharField(
        verbose_name='название',
        max_length=256,
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='ингредиенты',
    )
    cooking_time = models.PositiveIntegerField(
        'время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
    )
    
    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.name

class IngredientInRecipe(models.Model):
    """Промежуточная модель для связи рецептов и ингредиентов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='ингредиент',
    )
    amount = models.PositiveIntegerField(
        'количество',
        validators=[MinValueValidator(1)],
    )
    
    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe',
            )
        ]
    
    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name}'
            f' - {self.amount} {self.ingredient.measurement_unit}'
        )


