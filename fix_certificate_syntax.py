import os

file_path = r'm:/my projects/ACADEMIC OS/academic_os/hr/templates/hr/certificate_print.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken {% if %} tags caused by the formatter
# Target: 
# {% if organization.region %}{{ organization.region|upper }} MAKTABGACHA VA MAKTAB TA'LIMI<br>BO'LIMIGA
# QARASHLI{% endif %}

fixed_content = content.replace(
    "{% if organization.region %}{{ organization.region|upper }} MAKTABGACHA VA MAKTAB TA'LIMI<br>BO'LIMIGA\n            QARASHLI{% endif %}",
    "{% if organization.region %}{{ organization.region|upper }} MAKTABGACHA VA MAKTAB TA'LIMI<br>BO'LIMIGA QARASHLI{% endif %}"
)

# Target:
# {% if organization.address %}{{ organization.address }}{% else %}Manzil kiritilmagan{% endif %}, Tel: {% if
# organization.phone_number %}{{ organization.phone_number }}{% else %}kiritilmagan{% endif %}

fixed_content = fixed_content.replace(
    "{% if organization.address %}{{ organization.address }}{% else %}Manzil kiritilmagan{% endif %}, Tel: {% if\n            organization.phone_number %}{{ organization.phone_number }}{% else %}kiritilmagan{% endif %}",
    "{% if organization.address %}{{ organization.address }}{% else %}Manzil kiritilmagan{% endif %}, Tel: {% if organization.phone_number %}{{ organization.phone_number }}{% else %}kiritilmagan{% endif %}"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Syntax issues fixed in certificate_print.html via script.")
