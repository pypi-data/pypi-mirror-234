"""
    Unit test for Roles update
"""
# pylint: disable=W0612, C0413
import os
import sys

sys.path.append(os.path.abspath(__file__ + "/../../../"))
from dataclasses import dataclass

from reva.lib.base.errors.errors import RolesUpdateError, RolesDeleteError
from reva.tests.roles.fake_roles_updater import FakeRolesUpdate
from reva.tests.roles.fake_roles_deleter import FakeRolesDeleter

os.environ['LENDSMART_REVA_HOME'] = "/home/deepesh"
os.environ['LENDSMART_REVA_UI_HOME'] = "/home/deepesh/workspace/ui"
os.environ['LENDSMART_REVA_WORKLET_HOME'] = "/home/deepesh/workspace/worklet"

@dataclass
class MockArguments:
    """
    hold the arguments for test
    """
    namespace: str = "apptest"
    action: str = "update"
    env: str = "dev"

def test_roles_1():
    """
    Case 1: len(local roles) < len(remote_roles)
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case1")
    try:
        result = updater.start()
    except RolesUpdateError as err:
        assert isinstance(err, RolesUpdateError)

def test_roles_2():
    """
    Case 2: len(local roles) = len(remote_roles)
            No update (local_role == remote_roles)
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case2")
    result = updater.start()

    assert isinstance(result, list)

def test_roles_3():
    """
    Case 3: len(local roles) = len(remote_roles)
            Changes in local (local_role != remote_roles)
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case3")
    result = updater.start()

    assert isinstance(result, list)

def test_roles_4():
    """
    Case 4: len(local roles) = len(remote_roles)
            Changes in local (local_role != remote_roles)
            CONFLICT (some role's updated at times not same)
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case4")
    try:
        result = updater.start()
    except RolesUpdateError as err:
        assert isinstance(err, RolesUpdateError)

def test_roles_5():
    """
    Case 5: len(local roles) > len(remote_roles)
            Some New Roles added
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case5")
    result = updater.start()

    assert isinstance(result, list)

def test_roles_6():
    """
    Case 6: len(local roles) > len(remote_roles)
            Some Updated + Some New Roles added
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case6")
    result = updater.start()

    assert isinstance(result, list)

def test_roles_7():
    """
    Case 7: len(local roles) > len(remote_roles)
            Some Updated + Some New Roles added
            CONFLICT (some role's updated at time doesnt match)
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case7")
    try:
        result = updater.start()
    except RolesUpdateError as err:
        assert isinstance(err, RolesUpdateError)

def test_roles_8():
    """
    Case 8: Some role's ID is empty string
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case8")
    try:
        result = updater.start()
    except RolesUpdateError as err:
        assert isinstance(err, RolesUpdateError)

def test_roles_9():
    """
    Case 9: Some role's ID is missing
    """
    arguments = MockArguments()
    updater = FakeRolesUpdate(arguments=arguments, test_case="case9")
    try:
        result = updater.start()
    except RolesUpdateError as err:
        assert isinstance(err, RolesUpdateError)


def test_delete_roles_2():
    """
    case 2: Role with ID present in remote
    """
    arguments = MockArguments()
    deleter = FakeRolesDeleter(arguments=arguments, case="case2")

    result = deleter.start()
    assert isinstance(result, list)

def test_delete_roles_3():
    """
    case 3: deploy.json containing 2 ids that are present in
            remote and 1 that is not present in remote.
    """
    arguments = MockArguments()
    deleter = FakeRolesDeleter(arguments=arguments, case="case3")
    try:
        result = deleter.start()
    except RolesDeleteError as err:
        assert isinstance(err, RolesDeleteError)

def test_delete_roles_4():
    """
    case 4: deploy.json containing 2 ids that are present in
            remote and 1 empty string.
    """
    arguments = MockArguments()
    deleter = FakeRolesDeleter(arguments=arguments, case="case4")
    try:
        result = deleter.start()
    except RolesDeleteError as err:
        assert isinstance(err, RolesDeleteError)

def test_delete_roles_5():
    """
    case 5: deploy.json containing 1 id that is not present in remote.
    """
    arguments = MockArguments()
    deleter = FakeRolesDeleter(arguments=arguments, case="case5")
    try:
        result = deleter.start()
    except RolesDeleteError as err:
        assert isinstance(err, RolesDeleteError)
