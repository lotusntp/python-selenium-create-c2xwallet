import json
account_list = json.load(open('sample.json'))
data = []

for key in account_list:
    email = key['email']
    mnemonic = key['mnemonic']
    data.append({"name":email,"memoni":mnemonic})

final = json.dumps(data, indent=2)

print(final)