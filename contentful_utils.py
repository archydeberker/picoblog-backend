import contentful_management

client = contentful_management.Client('CFPAT-JhmsGHABq620dFA4KsLlLvfinkhE8nKuSbhtvF5O0Fc')

space = 'ykwd6jregaye'
environment_id = 'master'

spaces = client.spaces().all()
assets = client.assets(space,environment_id).all()
print(assets)
entries = client.entries(space, environment_id).all()
print(entries)
