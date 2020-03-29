import Database


print(Database.registerUser("test_last", "test_vor", "57072", "street.str", "16a", "testing", "test@test.de"))

ses = Database.login("test@test.de", "testing")
print(ses)
