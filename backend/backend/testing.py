import uuid

# Generate a UUID from the string "password"
uuid_from_string = uuid.uuid5(uuid.NAMESPACE_OID, "password")

# Print the generated UUID
print(uuid_from_string)
