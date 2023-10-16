"""
    Handles the autotest
"""
import asyncio
from autotest.lib.generator.initialize import FlowGeneratorInitializer
from autotest.lib.runner.initializer import AutoTestInitializer
from autotest.lib.lib.lend_event import LendEvent
from autotest.lib.client_builder.aws.lambda_obj import LambdaObj
from autotest.lib.base.setup import DriverSetup
from reva.lib.utils.get_paths import PathGetter
from reva.lib.utils.get_json_files import JsonFileGetter
from reva.exception import UnsupportedPlatformError



class AutoTest:
    """
        This class handles the auto test
    """

    def __init__(self, arguments):
        self.arguments = arguments

    def start(self):
        """
            start the auto test process
        """
        if self.arguments.platform == "remote":
            return RemoteAutoTest(arguments=self.arguments).run()
        if self.arguments.platform == "local":
            return LocalAutoTest(arguments=self.arguments).run()
        raise UnsupportedPlatformError(
            "Unsupported platform " + self.arguments.platform)


class AutoTestRunner:
    """
        Autotest runner
    """

    def __init__(self, arguments):
        self.arguments = arguments

    def get_workflow_json(self):
        """
            This function will get the workflow json
        """
        workflow_json_path = PathGetter().get_ui_config_path(
            namespace=self.arguments.namespace)
        file_path = workflow_json_path + "/" + \
            self.arguments.workflow + ".json"
        return JsonFileGetter().get_file_by_path(file_path)

    def generate_payload(self):
        """
            This function generate the data
        """
        return {
            "event_data": {
                "intent_data": self.get_workflow_json(),
                "product_name": self.arguments.product,
                "loan_role": self.arguments.group,
                "combination_samples": int(self.arguments.limit_random or "5"),
                "entry_url": self.arguments.project_url,
                "test_datas": self.arguments.fixures,
                "selected_combination_index" : self.arguments.spec
            }
        }


class RemoteAutoTest(AutoTestRunner):
    """
        This will run the test on remote
    """

    def run(self):
        """
            Run the test in remote server
        """
        print("--------- Test started in Remote", self.generate_payload())
        return LambdaObj().invoke(
            self.generate_payload(),
            "e2e_generator_dev_handler"
        )


class LocalAutoTest(AutoTestRunner):
    """
        This will run the test in local
    """
    async def start(self, payload):
        """
            start the test
        """
        event_data = {
            "event_data" : payload
        }
        lend_event = LendEvent(event_data)
        driver = DriverSetup().get_driver(
            "headless-chromium"
        )
        return AutoTestInitializer(
            driver = driver,
            lend_event = lend_event
        ).initailize()

    async def create_async_tasks(self, payload_test_datas):
        """
        create tasks
        """
        results = await asyncio.gather(*[asyncio.create_task(self.start(data))
                                         for data in payload_test_datas])
        return results

    async def main(self, payload_test_datas):
        """
        this function will create tasks for all requested docs
        """
        return await self.create_async_tasks(payload_test_datas)

    def get_test_payload(self):
        """
            This function retuns the payload
        """
        lend_event = LendEvent(self.generate_payload())
        generator = FlowGeneratorInitializer(lend_event)
        return generator.get_payload()


    def run(self):
        """
            run the test in local
        """
        if self.arguments.action == "list":
            return self.get_test_payload()
        return asyncio.run(self.main(self.get_test_payload()))
