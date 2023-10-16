from lgt_data.mongo_repository import SlackContactUserRepository

search = SlackContactUserRepository().find("Kiryl",
                                  skip=0,
                                  limit=1000,
                                  deleted=False)

pass