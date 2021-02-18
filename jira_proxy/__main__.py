import connexion
from loguru import logger

if __name__ == "__main__":

    logger.debug("initialize app")
    app = connexion.AioHttpApp(
        __name__,
        specification_dir="openapi/",
        resolver=connexion.resolver.RestyResolver("jira_proxy.api"),
    )

    app.add_api("api.yaml", pass_context_arg_name="request")

    logger.debug("start application")
    app.run(port=8080)
