# Copyright (C) 2022-2023 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import pytest

from common import get_project_role
from common import has_file_permission
from common import has_permission
from common import has_permissions
from common.permissions.exceptions import ProjectRoleNotFound


class TestPermissions:
    @pytest.mark.asyncio
    async def test_has_permission_true(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_false(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_platform_admin_true(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'admin',
        }
        url = (
            'http://auth/authorize?role=platform_admin&resource=project&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_no_project_code(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_permission('http://auth/', '', 'project', 'core', 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_service_error(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url, status_code=500)
        with pytest.raises(Exception):
            await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)


class TestFilePermissions:
    @pytest.mark.asyncio
    async def test_has_file_permission_true(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_outside_namefolder_true(self, httpx_mock):
        file_data = {
            'parent_path': 'another',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_false(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_outside_of_namefolder_false(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_project(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project2',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_container_type(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'dataset',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_archived(self, httpx_mock):
        file_data = {
            'status': 'ARCHIVED',
            'restore_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_namefolder(self, httpx_mock):
        file_data = {
            'type': 'name_folder',
            'name': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is True


class TestGetCurrentRole:
    @pytest.mark.asyncio
    async def test_get_current_role_admin(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'admin',
            'realm_roles': ['test_project-admin'],
        }
        result = await get_project_role('test_project', current_identity)
        assert result == 'platform_admin'

    @pytest.mark.asyncio
    async def test_get_current_role_member(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await get_project_role('test_project', current_identity)
        assert result == 'admin'

    async def test_get_current_role_non_default(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-customrole'],
        }
        result = await get_project_role('test_project', current_identity)
        assert result == 'customrole'


class TestBulkPermissions:
    auth_service_url = 'http://auth_service/v1/'
    permission_request = [
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'copy'},
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'view'},
    ]
    current_identity = {'role': 'collaborator', 'realm_roles': ['test_project-collaborator']}

    async def test_has_permissions_return_mapped_assertions(self, httpx_mock):
        granted = {'has_permission': True}
        mapped_result = {'greenroom_file_any_copy': True, 'greenroom_file_any_view': True}

        httpx_mock.add_response(
            method='POST',
            url=f'{self.auth_service_url}authorize',
            status_code=200,
            json=granted,
        )
        mapped = await has_permissions(
            self.auth_service_url, 'test_project', self.permission_request, self.current_identity
        )

        assert mapped == mapped_result

    async def test_has_permissions_raise_project_role_not_found_exception_for_invalid_role(self, httpx_mock):
        identity = self.current_identity
        identity['realm_roles'] = ['invalidproject-collaborator']
        with pytest.raises(ProjectRoleNotFound):
            await has_permissions(self.auth_service_url, 'test_project', self.permission_request, identity)
