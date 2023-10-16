import asyncio
import time
from typing import Any, Dict

import requests
from threading import Thread
from .identity import DryId


class DryJob:
    def __init__(self, job_id, request):
        self.id = job_id
        self.request = request


class RunConfig:
    # Assuming this is a simplified representation of RunConfig from your Rust code
    def __init__(self, auth: Dict[str, Any] = {}, inject: Dict[str, str] = {}, disable_secrets: bool = False,
                 swap: Dict[DryId, Dict[str, Any]] = {}):
        self.auth = auth
        self.inject = inject
        self.disable_secrets = disable_secrets
        self.swap = swap

    def to_json(self):
        # Convert DryId instances to strings in the swap dictionary
        swap_str = {str(k): v for k, v in self.swap.items()}

        return {
            "auth": self.auth,
            "inject": self.inject,
            "disable_secrets": self.disable_secrets,
            "swap": swap_str
        }


class DryClient:
    def __init__(self, api_key, engine_host: str = "http://localhost:3000", proxy_host="http://localhost:3006",
                 proxy_name=DryId("worker", "queue"),
                 verbose=False):
        self.engine_host = engine_host
        self.proxy_identity = proxy_name
        self.proxy_host = proxy_host
        self.execute_endpoint = "/execute"
        self.register_proxy_endpoint = "/hire/*proxy_identity"
        self.submit_job_proxy_endpoint = "/retire/*job_id"
        self.get_jobs_proxy_endpoint = "/employ/*proxy_identity"
        self.api_key = api_key
        self.verbose = verbose
        self.handlers = {}  # Dictionary to map URLs to handler functions

    def run(self, dry_id: DryId, run_config: RunConfig = RunConfig(), args: Dict[str, Any] = {}) -> Dict[str, Any]:
        endpoint = f"{self.proxy_host}{self.execute_endpoint}"  # Replace with your actual endpoint
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Construct the payload based on your Rust code structure
        payload = {
            "identity": str(dry_id),
            "config": run_config.to_json(),
            "args": args
        }

        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # This will raise an HTTPError with the status code and message

    def route(self, url, handler_function):
        """
        A handler function must accept a single dictionary argument, which will contain the request body and headers
        of the job.
        """
        self.handlers[url] = handler_function
        return self  # Allow chaining

    def register_proxy(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        proxy_identity = str(self.proxy_identity)
        url = f"{self.proxy_host}{self.register_proxy_endpoint.replace('*proxy_identity', proxy_identity)}"
        try:
            response = requests.post(url, headers=headers, json={"identity": proxy_identity})
            if response.status_code == 200:
                self.report(f"Successfully registered proxy {proxy_identity}")
            else:
                print(f"Failed to register proxy {proxy_identity} with error: {response.text}")
        except Exception as e:
            print(f"Failed to register proxy {proxy_identity} with error: {e}")

    def report(self, message):
        if self.verbose:
            print(message)

    def submit_job_response(self, job_id, job_response):
        self.report(f"[PROXY] Submitting job response for job {job_id}")
        url = f"{self.proxy_host}{self.submit_job_proxy_endpoint.replace('*job_id', job_id)}"
        self.report(f"[PROXY] Submitting job response to {url}")
        headers = {"Authorization": f"Bearer {self.api_key}"}

        # Prepare the result field to match the expected StructuredResult enum
        structured_result = {
            "Generic": job_response  # Assuming job_response is the value you want to send
        }

        # Prepare the JSON body to match the expected CompleteJobEndpointArgs struct
        json_body = {
            "job_id": job_id,
            "result": structured_result
        }

        response = requests.post(url, headers=headers, json=json_body)  # Synchronous request
        if response.status_code == 200:
            self.report(f"[PROXY] Successfully submitted job response for job {job_id}")
        else:
            self.report(f"[PROXY] Failed to submit job response for job {job_id}")
            self.report(response.text)  # Log the response text to see the error message

    async def process_job(self, job):
        self.report(f"[PROXY] Processing job {job.id}, {job.request}")
        handler = self.handlers.get(job.request['url'])
        if handler:
            result = handler(job.request['body'])  # Ensure your handlers are async if necessary
            job_response = result
        else:
            self.report(f"[PROXY] No handler for job {job.id} with details {job.request}, skipping.")
            job_response = {"error": "No handler available for this job."}
        self.submit_job_response(job.id, job_response)

    def process_jobs(self, jobs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tasks = [self.process_job(job) for job in jobs]
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            self.report(f"[PROXY] Error processing jobs: {e}")
        finally:
            loop.close()

    def proxy_run(self):
        self.report("Starting DryProxy, a lightweight proxy server facilitating DryMerge integrations...")
        while True:
            url = f"{self.proxy_host}{self.get_jobs_proxy_endpoint.replace('*proxy_identity', str(self.proxy_identity))}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            try:
                self.report(f"[PROXY] Polling for jobs at {url}")
                response = requests.get(url, headers=headers,
                                        stream=True)  # Set stream=True to keep the connection open and long=True to
                # indicate long polling to the server
                if response.status_code == 200:
                    jobs_data = response.json().get("jobs", [])
                    jobs = [DryJob(job['id'], job['request']) for job in jobs_data]
                    self.process_jobs(jobs)
                else:
                    self.report(f"[PROXY] Job queue endpoint responded with error: {response.text}")
            except Exception as e:
                self.report(f"[PROXY] Error polling for jobs: {e}")

    def start(self, run_proxy=True):
        if run_proxy:
            self.register_proxy()
            proxy_thread = Thread(target=self.proxy_run)
            proxy_thread.start()


# client = (DryClient(
#     api_key="YOUR_API_KEY_HERE",
#     verbose=True, )
#           .route("print_with_reflect", lambda request: {'test': 'test'})
#           .route("py2", lambda request: {'test2': 'test2'}))
#
# client.start()
