from django.db import migrations, models


def deduplicate_budgets(apps, schema_editor):
    """
    Before applying unique_together, remove duplicate (user, category) rows.
    Keep the one with the highest limit; delete the rest.
    """
    Budget = apps.get_model('checkam', 'Budget')
    seen = {}
    # Order by limit desc so the highest limit is processed first
    for budget in Budget.objects.order_by('-limit'):
        key = (budget.user_id, budget.category)
        if key in seen:
            budget.delete()
        else:
            seen[key] = budget.pk


class Migration(migrations.Migration):

    dependencies = [
        ('checkam', '0006_alter_budget_limit'),
    ]

    operations = [
        # 1. Add the category field (nullable so existing rows get default='other')
        migrations.AddField(
            model_name='budget',
            name='category',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('food', 'Food'), ('transport', 'Transport'), ('rent', 'Rent'),
                    ('data', 'Data'), ('salary', 'Salary'),
                    ('entertainment', 'Entertainment'),
                    ('utilities', 'Utilities'), ('other', 'Other'),
                ],
                default='other',
            ),
        ),
        # 2. Remove the old title field
        migrations.RemoveField(
            model_name='budget',
            name='title',
        ),
        # 3. Deduplicate existing rows BEFORE adding the unique constraint
        migrations.RunPython(deduplicate_budgets, migrations.RunPython.noop),
        # 4. Now it's safe to add unique_together
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together={('user', 'category')},
        ),
    ]
