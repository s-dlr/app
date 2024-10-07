from src.sql_update import ClientGoogle

client = ClientGoogle()
print(
    f"{client.host}/{client.indicateurs_spredsheet}/values/R1C1:R100C100?key={client.api_key}"
)
print(client.get_indicateurs())
client.update_values(
    "A1:C2",
    "USER_ENTERED",
    [["A", "B"], ["C", "D"]],
)
