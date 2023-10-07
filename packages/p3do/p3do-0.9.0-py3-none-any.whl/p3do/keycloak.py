import json
import keycloak as kc

from loguru import logger


class Keycloak:
    def __init__(self, server, username, password, user_realm_name, realm_name):
        self.server = server
        self.username = username
        self.password = password
        self.user_realm_name = user_realm_name
        self.realm_name = realm_name

        logger.info("Initializing server connection to {server}", server)
        self.keycloak_admin = kc.KeycloakAdmin(server_url=server,
                                            username=username,
                                            password=password,
                                            user_realm_name=user_realm_name,
                                            realm_name=realm_name)

    @logger.catch
    def import_mappers(self, f):
        data = json.load(f)
        mappers = data["identityProviderMappers"]

        logger.info("Found {} identity provider mappers", len(mappers))
        for idx, mapper in enumerate(mappers):
            logger.info("Push mapping {} of {}", idx+1, len(mappers))
            self.keycloak_admin.add_mapper_to_idp(mapper["identityProviderAlias"], mapper)
