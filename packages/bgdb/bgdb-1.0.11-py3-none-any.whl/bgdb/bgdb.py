import bgdb

# Overarching session class for bdgdb
class BGDB:
    def __init__(self, db_url, env_mode=False):

        # Initialise a Client() on the BGDBSession()
        # Establish a client connection
        self.client = bgdb.Client(db_url)
        self.client.login(use_env=env_mode)

        # Setup search session
        self.search = bgdb.Search(self.client)

        # Setup utils module
        self.utils = bgdb.Utils(self.client)
