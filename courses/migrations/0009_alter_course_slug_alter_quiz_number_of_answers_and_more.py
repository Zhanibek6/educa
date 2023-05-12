# Generated by Django 4.1.4 on 2023-05-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0008_quiz_number_of_answers_alter_quiz_difficulty_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Необязательно. Отображаемая адресная строка курса",
                max_length=200,
                unique=True,
                verbose_name="Слаг",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="number_of_answers",
            field=models.IntegerField(
                default=5,
                help_text="По умолчанию 5",
                verbose_name="Количество вариантов ответа",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="required_score_to_pass",
            field=models.IntegerField(
                help_text="На какое минимальное количество правильных процентов вопросов должен ответить студент",
                verbose_name="Требуемый результат для прохождения теста (в процентах %)",
            ),
        ),
    ]