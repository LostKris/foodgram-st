from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core_models.models import Ingredient, Recipe, IngredientInRecipe
from favorites import favorite_manage
from shopping_cart import shopping_cart_manage
from subscriptions import subscription_manage
from users.models import User


class UserSerializer(djoser_serializers.UserSerializer):
    avatar = Base64ImageField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )
    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_is_subscribed(self, obj):
        user = self._user(obj)
        if user and user.is_authenticated:
            return subscription_manage.is_subscribed(user, obj)
        return False

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ['id']


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=IngredientInRecipe.objects.all(), source='ingredient')
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    class Meta:
        model = IngredientInRecipe
        fields = ('id','name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        return obj.ingredient.name
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class IngredientInRecipeMinifiedSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient')
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(source='ingredient_in_recipe', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self._user(obj)
        if user and user.is_authenticated:
            return favorite_manage.is_recipe_favorited(user, obj)
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self._user(obj)
        if user and user.is_authenticated:
            return shopping_cart_manage.is_in_shopping_list(user, obj)
        return False

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientInRecipeMinifiedSerializer(
        source='ingredient_in_recipe',
        many=True
    )
    class Meta:
        model = Recipe
        fields = ('ingredients', 'image', 'name', 'text', 'cooking_time',)

    def validate_ingredients(self, value):
        if value is None or not value:
            raise serializers.ValidationError("В рецепте должен быть хотя бы один ингредиент")
        ingredients = [item['ingredient'].id for item in value]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError("Значения ингредиентов должны быть уникальны")

        return value

    def validate_image(self, value):
        if value is None:
            raise serializers.ValidationError('Отсутствует картинка в поле "image"')
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient_in_recipe')

        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

        self._attach_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient_in_recipe', None)
        if ingredients is None:
            raise serializers.ValidationError('Должен быть передан список ингредиентов')

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()

        if ingredients is not None:
            instance.ingredient_in_recipe.all().delete()
            self._attach_ingredients(instance, ingredients)

        return instance

    def _attach_ingredients(self, recipe, ingredients):
        ingredient_objects = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient=item['ingredient'],
                amount=item['amount']
            )
            for item in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredient_objects)


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class UserWithRecipesSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context.get('recipes_limit', 10)
        recipes = obj.recipes.all()[:limit]
        serializer = RecipeMinifiedSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return len(obj.recipes.all())


class CreateUserSerializer(djoser_serializers.UserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    class Meta:
        model = User
        fields = ('avatar',)
