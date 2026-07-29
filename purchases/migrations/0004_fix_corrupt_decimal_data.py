from django.db import migrations


def fix_corrupt_decimals(apps, schema_editor):
    """Replace empty-string values stored in DecimalFields with 0."""
    with schema_editor.connection.cursor() as cursor:
        for field in ('unit_price', 'markup_percent', 'selling_price', 'subtotal'):
            cursor.execute(
                f"UPDATE purchases_purchaseorderitem SET {field} = 0 WHERE {field} = ''"
            )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_alter_purchaseorderitem_selling_price_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_corrupt_decimals, reverse),
    ]
