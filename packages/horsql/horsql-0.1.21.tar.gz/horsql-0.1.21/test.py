import horsql
import pandas as pd
from horsql import operators as o

db = horsql.connect(
    database="rps",
    host="localhost",
    port=5432,
    user="dev",
    password="dev",
    dialect="postgresql",
    echo=True,
    pool_size=2,
)

db.connect()

users = [
    dict(email="poppo", user_name="pepei"),
]

df = pd.DataFrame(users)

db.public.users.create(df)

db.public.users.update(df, on_conflict=["email"], update=["user_name"])

db.public.users.order_by("user_id").get(
    chain=o.Or(o.Or(birthday=o.IsNull()), birthday=["1992-09-19"])
)

db.public.users.limit(limit=10)

db.public.users.get()

db.public.users.delete(user_id=84)

o.EqualsOrGreaterThan

db.public.users.get(["user_name"], sum=["user_id"], user_id=o.lte(30))

"""
SELECT
user_id, user_name
FROM
public.users
WHERE (user_id in (1, 2) and email like '%%@%%')
"""

new_user = pd.DataFrame(
    [{"user_name": "WilianZilv", "first_name": "Wilian", "last_name": "Silva"}]
)

# Create new records based on a dataframe
db.public.users.create(new_user)

# Upsert
db.public.users.create(new_user, on_conflict=["user_name"], update=["city", "country"])

# Updating records
new_user["city"] = "Curitiba"
new_user["country"] = "Brazil"

db.public.users.update(new_user, on_conflict=["user_name"], update=["city", "country"])


df = db.public.users.order_by("age", ascending=True).get()

df = db.public.users.order_by(["age", "country"], ascending=[True, False]).get()

# Limit
df = db.public.users.limit(limit=10).get()

df = db.public.users.order_by("age", ascending=True).limit(limit=10).get()

# Pagination
df = db.public.users.paginate(page=1, page_size=10).get()

df = (
    db.public.users.order_by("age", ascending=True).paginate(page=1, page_size=10).get()
)
