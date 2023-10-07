from cement import Controller, ex


class Config(Controller):
    class Meta:
        label = 'config'
        stacked_on = 'base'
        stacked_type = 'nested'

        # text displayed at the top of --help output
        description = 'Set configuration parameters'

    @ex(
        help='get configured perian endpoint url',
    )
    def get_endpoint(self):
        endpoint = self.app.db.get("endpoint")

        if endpoint:
            self.app.log.info('Perian endpoint currently set to: %s' % endpoint)
        else:
            self.app.log.warning("Currently no endpoint configured")

    @ex(
        help='set perian endpoint url',
        arguments=[
            (['url'],
             {'help': 'perian endpoint url',
              'action': 'store'})
        ],
    )
    def set_endpoint(self):
        url = self.app.pargs.url

        matches = ["http", "https"]
        if any([x in url for x in matches]):
            self.app.db.set("endpoint", url)

            self.app.log.info('Setting Perian endpoint to: %s' % url)
        else:
            self.app.log.error(
                "The provided url is not correct. Please provide a url in the format: http://* or https://*")

    @ex(
        help='add private docker registry information',
        arguments=[
            (['name'],
             {'help': 'docker registry name',
              'action': 'store'}),
            (['url'],
             {'help': 'docker registry url',
              'action': 'store'}),
            (['username'],
             {'help': 'username for private docker registry',
              'action': 'store'}),
            (['password'],
             {'help': 'password for private docker registry',
              'action': 'store'})
        ],
    )
    def add_registry(self):
        name = self.app.pargs.name
        url = self.app.pargs.url
        username = self.app.pargs.username
        print(username)
        password = self.app.pargs.password

        registries = self.app.db.get("registries")

        if not registries:
            registries = {
                name: {
                    "name": name,
                    "url": url,
                    "username": username,
                    "password": password
                }
            }
        else:
            already_included = False
            for registry in registries:
                if registry == name:
                    already_included = True
                    registries[name] = {
                        "name": name,
                        "url": url,
                        "username": username,
                        "password": password
                    }

            if not already_included:
                registries[name] = {
                        "name": name,
                        "url": url,
                        "username": username,
                        "password": password
                    }

        self.app.db.set("registries", registries)
        self.app.log.info('Stored information for private docker registry: %s' % name)


    @ex(
        help='get stored private docker registry information',
        arguments=[
            (['-n', '--name'],
             {'help': 'stored  registry name',
              'action': 'store'})
        ],
    )
    def get_registry(self):
        name = self.app.pargs.name

        registries = self.app.db.get("registries")

        if not registries:
            self.app.log.warning("No stored docker registries found")
        else:
            if name and name in registries:
                self.app.log.info("Stored registry '" + name + "'")
                self.app.log.info("url -> "  + registries[name]['url'])
                self.app.log.info("username -> " + registries[name]['username'])
                self.app.log.info("password -> ******")
            else:
                self.app.log.info("Stored registry names: " + str(list(registries.keys())))
                self.app.log.info("Please provide a registry name to display more information")


    @ex(
        help='set authorization token',
        arguments=[
            (['token'],
             {'help': 'API authorization token',
              'action': 'store'})
        ],
    )
    def set_token(self):
        token = self.app.pargs.token

        if token:
            self.app.db.set("token", token)
            self.app.log.info('Setting API token to: %s' % token)


    @ex(
        help='get stored authorization token'
    )
    def get_token(self):
        token = self.app.db.get("token")

        if token:
            self.app.log.info('Stored API token: %s' % token)
        else:
            self.app.log.warning("No token stored")



    @ex(
        help='clear all perian configurations',
    )
    def clear(self):
        self.app.db.clear()
        self.app.log.info('Cleared all configurations')





