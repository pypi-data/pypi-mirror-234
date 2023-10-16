from keycloak import KeycloakAdmin
from cast_common.aipRestCall import AipRestCall

keycloak_admin = KeycloakAdmin(server_url="http://arch-ps-2:8086/auth/",
                               username='admin',
                               password='admin',
                               verify=True)
user = keycloak_admin.get_users()

for item in user:
    if item['username']=='admin':
        user_id = item['id']
        break

clients = keycloak_admin.get_clients()
for item in clients:
    client_id = item['id']
    roles = keycloak_admin.get_available_client_roles_of_user(user_id,client_id)

pass
