from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from validators.custom_validators import validator_only_letters_numbers, ValidatorMaxSizeInMB


class Game(models.Model):
    TITLE_MAX_LENGTH = 30
    TITLE_MIN_LENGTH = 2

    CATEGORY_MAX_LENGTH = 10

    LEVEL_MAX_VALUE = 100
    LEVEL_MIN_VALUE = 1

    IMAGE_MAX_SIZE = 10

    DESCRIPTION_TEXT_FIELD_MAX_LENGTH = 200

    ACTION = 'Action'
    ADVENTURE = 'Adventure'
    PUZZLE = 'Puzzle'
    SIMULATION = 'Simulation'
    STRATEGY = 'Strategy'
    SPORT = 'Sports'
    OTHERS = 'Others'

    TYPE_CHOICES = [(x, x) for x in (ACTION, ADVENTURE, PUZZLE, SIMULATION, STRATEGY, SPORT, OTHERS)]

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=(
            MinLengthValidator(TITLE_MIN_LENGTH),
            validator_only_letters_numbers,
        )
    )

    category = models.TextField(
        max_length=CATEGORY_MAX_LENGTH,
        choices=TYPE_CHOICES,
    )
    max_level = models.IntegerField(
        blank=True,
        null=True,
        validators=(
            MaxValueValidator(LEVEL_MAX_VALUE),
            MinValueValidator(LEVEL_MIN_VALUE)
        )
    )

    image = models.ImageField(
        upload_to='game_images',
        validators=(
            ValidatorMaxSizeInMB(IMAGE_MAX_SIZE),
        )

    )
    description = models.TextField(
        blank=True,
        null=True,
    )
