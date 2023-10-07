import datetime
import time

from cement import Controller, ex
from rich.console import Console
from rich.table import Table
import sys
import perian
from perian.rest import ApiException
from perian.models.create_job_request import CreateJobRequest, DockerRegistryCredentials, OSStorageConfig, DockerRunParameters
from perian.models.flavor_query import FlavorQuery
from pcli.util import Loader
from time import sleep

def print_all_jobs(jobs, app):
    if len(jobs) > 0:
        table = Table()
        columns = ["ID", "Status", "Created", "Finished", "Logs"]
        for column in columns:
            table.add_column(column)

        for job in jobs:

            logs = ""
            if job.logs:
                logs = job.logs[0:50] + " ..."
            table.add_row(
                job.jid,
                job.status,
                job.created_at.strftime("%d.%m.%Y - %H:%M:%S") + " (UTC)",
                job.done_at.strftime("%d.%m.%Y - %H:%M:%S") + " (UTC)" if job.done_at else "",
                logs
            )

        console = Console()
        console.print(table)
    else:
        app.log.warning("No jobs found")


def get_optimal_flavor(flavor_query, endpoint, token, app):
    query = perian.FlavorQuery(**flavor_query)

    configuration = perian.Configuration(
        host=endpoint
    )

    with perian.ApiClient(configuration) as api_client:
        api_instance = perian.SelectionApi(api_client)

        try:
            api_response = api_instance.get_flavors_selection_get_flavors_post(query, limit=1, authorization="Bearer" + token)
            if  len(api_response.flavors) >= 1:
                return api_response.flavors[0]
            elif  len(api_response.flavors) == 0:
                app.log.error("No instance flavor found for criteria")
                sys.exit(1)
        except perian.ApiException as e:
            print(e)
            app.log.error("API error, please try again")
            sys.exit(1)

def get_flavor_description(flavor):
    gpu_data = None
    if flavor.gpu.no > 0:
        gpu_data = str(flavor.gpu.no) + " x " + flavor.gpu.gpus[0].name + " (" + str(flavor.gpu.memory.size) + " GB)"

    base_information = flavor.provider.name.value + ": " + str(flavor.cpu.cores) + " Cores, " + str(flavor.ram.size) + " GB Memory"

    if gpu_data:
        base_information = base_information + ", " + gpu_data

    all_information = base_information + " -> " + str(float(flavor.price.euro_price)) + " €/h"
    return all_information


class Job(Controller):
    class Meta:
        label = 'job'
        stacked_on = 'base'
        stacked_type = 'nested'

        # text displayed at the top of --help output
        description = 'Create and monitor jobs'

    @ex(
        help='create job on the perian sky job platform',
        arguments=[
            (['docker_image'],
             {'help': 'workload docker image',
              'action': 'store'}),
            (['-f', '--flavor'],
             {'help': 'id of the flavor',
              'action': 'store'}),
            (['-c', '--cores'],
             {'help': 'Amount of cpu cores',
              'action': 'store'}),
            (['-m', '--memory'],
             {'help': 'Amount of RAM memory',
              'action': 'store'}),
            (['-g', '--gpu'],
             {'help': 'Number of GPUs',
              'action': 'store'}),
            (['-t', '--token'],
             {'help': 'API token',
              'action': 'store'}),
            (['-s', '--storage-size'],
             {'help': 'size of storage to add to job container (in GB)',
              'action': 'store'}),
            (['-it', '--docker-image-tag'],
             {'help': 'tag for the docker image (default: latest)',
              'action': 'store'}),
            (['-cm', '--command'],
             {'help': 'command to execute in the workload docker container',
              'action': 'store'}),
            (['-u', '--registry-username'],
             {'help': 'private docker registry username',
              'action': 'store'}),
            (['-p', '--registry-password'],
             {'help': 'private docker registry password',
              'action': 'store'}),
            (['-ru', '--registry-url'],
             {'help': 'private docker registry url',
              'action': 'store'}),
            (['-r', '--registry'],
             {'help': 'stored private docker registry name',
              'action': 'store'}),
        ],
    )
    def create(self):
        token = self.app.pargs.token
        storage_size = self.app.pargs.storage_size
        docker_image = self.app.pargs.docker_image
        docker_image_tag = self.app.pargs.docker_image_tag
        command = self.app.pargs.command
        registry = self.app.pargs.registry
        registry_url = self.app.pargs.registry_url
        registry_username = self.app.pargs.registry_username
        registry_password = self.app.pargs.registry_password

        stored_token = self.app.db.get("token")
        stored_registries = self.app.db.get("registries")
        stored_endpoint = self.app.db.get("endpoint")

        if not stored_endpoint:
            self.app.log.error("Endpoint not configured yet. Please set the endpoint via the 'config' command")
            sys.exit(1)

        if not token and not stored_token:
            self.app.log.error(
                "No token provided or configured. Please provided the token (--token) or configure it via the 'config' command")
            sys.exit(1)

        try:
            request = {}
            current_token = None

            if token:
                current_token = token
            elif stored_token:
                current_token = stored_token

            flavor_description = ""
            loader = Loader(desc="Finding optimal flavor", end=flavor_description, timeout=0.05).start()
            if self.app.pargs.flavor:
                request['flavor_id'] = self.app.pargs.flavor
            else:
                # no flavor id provided, checking automatic flavor parameters
                filter_criteria = {}
                if self.app.pargs.cores:
                    filter_criteria['cpu'] = {
                        "cores": int(self.app.pargs.cores)
                    }
                if self.app.pargs.memory:
                    filter_criteria['ram'] = {
                        "size": int(self.app.pargs.memory)
                    }
                if self.app.pargs.gpu:
                    filter_criteria['gpu'] = {
                        "no": int(self.app.pargs.gpu)
                    }

                if len(filter_criteria) == 0:
                    self.app.log.error("You must either specify a flavor id or pass filter criteria via the command line options")
                    sys.exit(1)

                flavor = get_optimal_flavor(filter_criteria, stored_endpoint, current_token, self.app)
                request['flavor_id'] = flavor.pid
                loader.end = get_flavor_description(flavor)

                for i in range(10):
                    sleep(0.1)

            loader.stop()

            loader = Loader(desc="Creating job", end="Job created successfuly", timeout=0.05).start()

            if storage_size:
                request['os_storage_config'] = OSStorageConfig(
                    size=int(storage_size)
                )

            if not docker_image:
                self.app.log.error("No docker image provided. Please provide a docker image")
                sys.exit(1)
            else:
                request['docker_run_parameters'] = DockerRunParameters(
                    image_name=docker_image,
                    image_tag=docker_image_tag if docker_image_tag else "latest",
                    command=command if command else ""
                )

            if not registry_url and not registry:
                if not self.app.db.get("WARNING:REGISTRY"):
                    self.app.log.warning("You have not provided a docker registry url and no reference to a stored registry.")
                    self.app.log.warning("Please be informed that you therefore can only run workloads from publicly accessible registries.")
                    self.app.db.set("WARNING:REGISTRY", True)

            if registry_url:
                if not registry_password or not registry_username:
                    self.app.log.error("You have provided a registry url but the username or password was not set.")

            if registry:
                found = False
                for registry in stored_registries:
                    if registry == registry:
                        found = True
                        request['docker_registry_credentials'] = DockerRegistryCredentials(
                            url=stored_registries[registry]['url'],
                            username=stored_registries[registry]['username'],
                            password=stored_registries[registry]['password']
                        )
                if not found:
                    self.app.log.error("The provided stored registry name was not found.")


            configuration = perian.Configuration(
                host=stored_endpoint
            )

            with perian.ApiClient(configuration) as api_client:
                api_instance = perian.JobApi(api_client)
                job_request = perian.CreateJobRequest(**request)

                api_response = api_instance.create_job_job_create_post(job_request, authorization="Bearer" + current_token)

                jid = api_response.jid

                for i in range(10):
                    sleep(0.1)
                loader.stop()

                self.app.log.info("Job ID: " + str(jid))

        except ApiException as e:
            if "flavor type is blocked" in str(e.body):
                self.app.log.error("The selected flavor type is blocked for your account")
            else:
                self.app.log.error(e)
                sys.exit(1)



    @ex(
        help='get details of a created job',
        arguments=[
            (['job_id'],
             {'help': 'id of the job',
              'action': 'store'}),
            (['-t', '--token'],
             {'help': 'API token',
              'action': 'store'})
        ],
    )
    def get(self):
        jid = self.app.pargs.job_id
        token = self.app.pargs.token

        stored_token = self.app.db.get("token")
        stored_endpoint = self.app.db.get("endpoint")

        if not token and not stored_token:
            self.app.log.error("No token provided or configured. Please provided the token (--token) or configure it via the 'config' command")
            sys.exit(1)

        if not stored_endpoint:
            self.app.log.error("Endpoint not configured yet. Please set the endpoint via the 'config' command")
            sys.exit(1)

        try:
            current_token = None

            if token:
                current_token = token
            elif stored_token:
                current_token = stored_token

            configuration = perian.Configuration(
                host=stored_endpoint
            )

            with perian.ApiClient(configuration) as api_client:
                api_instance = perian.JobApi(api_client)

                if jid == "all":
                    api_response = api_instance.get_jobs_job_get_all_get(authorization="Bearer" + current_token)
                    print_all_jobs(api_response.jobs, self.app)
                else:
                    try:
                        api_response = api_instance.get_job_job_get_get(jid=jid, authorization="Bearer" + current_token)

                        self.app.log.debug("Successfully retrieved job details")
                        self.app.render(api_response.job.to_dict(), "job.jinja2")
                    except ApiException as e:
                        if "No job found" in str(e.body):
                            self.app.log.error("No job found with specified ID")

        except Exception as e:
            self.app.log.error(e)
            sys.exit(1)


