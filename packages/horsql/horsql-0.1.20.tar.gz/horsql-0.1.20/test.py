import horsql
import pandas as pd
from horsql import operators as o

db = horsql.connect("rps", "localhost", 5432, "dev", "dev", echo=True, pool_size=2)

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

db.public.users.get()

db.public.users.delete(user_id=84)


db.public.users.get(["user_name"], sum=["user_id"], user_id=o.lte(30))

"""
SELECT
user_id, user_name
FROM
public.users
WHERE (user_id in (1, 2) and email like '%%@%%')
"""
