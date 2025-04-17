models = [
    ("A05", "4/64", 450000),
    ("A05", "4/128", 500000),
    ("A06", "4/64", 480000),
    ("A06", "4/128", 520000),
    ("A05s", "4/64", 470000),
    ("A05s", "4/128", 510000),
    ("A16", "4/128", 600000),
    ("A16", "6/128", 650000)
]

for model in models:
    db.session.add(PhoneModel(
        model_name=model[0],
        storage=model[1],
        price=model[2]
    ))
db.session.commit()