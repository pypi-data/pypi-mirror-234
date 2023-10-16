import os
import sys

sys.path.append(os.path.abspath(__file__ + "/../../../"))
from dataclasses import dataclass

from reva.permissions import main

os.environ['LENDSMART_REVA_HOME'] = "/home/deepesh"
os.environ['LENDSMART_REVA_UI_HOME'] = "/home/deepesh/workspace/ui"
os.environ['LENDSMART_REVA_WORKLET_HOME'] = "/home/deepesh/workspace/worklet"

@dataclass
class MockArguments:
    """
    hold the arguments for test
    """
    namespace: str = "apptest"
    action: str = "delete"
    env: str = "dev"

def test_permissions():
    arguments = MockArguments()
    main(argument=arguments)

test_permissions()