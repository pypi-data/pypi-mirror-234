from grpc_reflection.v1alpha import reflection
from loguru import logger

# Example service_configs
# service_configs = {
#     "AreaOfInterestApi": {
#         "pb_definition": area_of_interest_api_pb2,
#         "grpc_definition": area_of_interest_api_pb2_grpc,
#         "servicer_instance": AreaOfInterestApi(db_pool),
#     }
# }


class ServiceConfig:
    def __init__(self, server, service_configs):
        self.server = server
        self.service_configs = service_configs

        # Add each servicer to the server
        for service_name, config in self.service_configs.items():
            grpc_definition = config["grpc_definition"]
            servicer_instance = config["servicer_instance"]

            # Get the appropriate add_*Servicer_to_server function
            add_servicer_func = getattr(
                grpc_definition, f"add_{service_name}Servicer_to_server"
            )

            # Add the servicer instance to the server
            add_servicer_func(servicer_instance, self.server)

            logger.info(f"Added {service_name} to server")

    def enable_reflection(self):
        # For each pb_definition in service_configs, add it to the server reflection
        SERVICE_NAMES = tuple(
            [
                self.service_configs[service]["pb_definition"]
                .DESCRIPTOR.services_by_name[service]
                .full_name
                for service in self.service_configs
            ]
        )

        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        logger.info("Enabled server reflection")
