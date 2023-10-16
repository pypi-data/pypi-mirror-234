# from typing import Optional
# from pydantic import EmailStr
from beanie import WriteRules, DeleteRules
from beanie.operators import In
from unipoll_api import AccountManager
from unipoll_api.documents import Group, ResourceID, Workspace, Account, Policy, Poll, create_link
from unipoll_api.actions import PolicyActions, PollActions
from unipoll_api.utils import Permissions
from unipoll_api.schemas import WorkspaceSchemas, GroupSchemas, PolicySchemas, MemberSchemas, PollSchemas
from unipoll_api.exceptions import (WorkspaceExceptions, AccountExceptions, GroupExceptions, ResourceExceptions,
                                    PolicyExceptions, PollExceptions)


# Get a list of workspaces where the account is a owner/member
async def get_workspaces() -> WorkspaceSchemas.WorkspaceList:
    account = AccountManager.active_user.get()
    workspace_list = []

    search_result = await Workspace.find(Workspace.members.id == account.id).to_list()  # type: ignore

    # Create a workspace list for output schema using the search results
    for workspace in search_result:
        workspace_list.append(WorkspaceSchemas.WorkspaceShort(
            **workspace.model_dump(exclude={'members', 'groups', 'permissions'})))

    return WorkspaceSchemas.WorkspaceList(workspaces=workspace_list)


# Create a new workspace with account as the owner
async def create_workspace(input_data: WorkspaceSchemas.WorkspaceCreateInput) -> WorkspaceSchemas.WorkspaceCreateOutput:
    account: Account = AccountManager.active_user.get()
    # Check if workspace name is unique
    if await Workspace.find_one({"name": input_data.name}):
        raise WorkspaceExceptions.NonUniqueName(input_data.name)

    # Create a new workspace
    new_workspace = await Workspace(name=input_data.name, description=input_data.description).create()

    # Check if workspace was created
    if not new_workspace:
        raise WorkspaceExceptions.ErrorWhileCreating(input_data.name)

    # Create a policy for the new member
    # The member(creator) has full permissions on the workspace
    # new_policy = Policy(policy_holder_type='account',
    #                     policy_holder=(await create_link(account)),
    #                     permissions=Permissions.WORKSPACE_ALL_PERMISSIONS,
    #                     parent_resource=new_workspace)  # type: ignore

    # Add the current user and the policy to workspace member list
    # new_workspace.members.append(account)  # type: ignore
    # new_workspace.policies.append(new_policy)  # type: ignore
    await new_workspace.add_member(account=account, permissions=Permissions.WORKSPACE_ALL_PERMISSIONS, save=False)
    await Workspace.save(new_workspace, link_rule=WriteRules.WRITE)

    # Specify fields for output schema
    return WorkspaceSchemas.WorkspaceCreateOutput(**new_workspace.model_dump(include={'id', 'name', 'description'}))


# Get a workspace
async def get_workspace(workspace: Workspace,
                        include_groups: bool = False,
                        include_policies: bool = False,
                        include_members: bool = False,
                        include_polls: bool = False) -> WorkspaceSchemas.Workspace:
    groups = (await get_groups(workspace)).groups if include_groups else None
    members = (await get_workspace_members(workspace)).members if include_members else None
    policies = (await get_workspace_policies(workspace)).policies if include_policies else None
    polls = (await get_polls(workspace)).polls if include_polls else None
    # Return the workspace with the fetched resources
    return WorkspaceSchemas.Workspace(id=workspace.id,
                                      name=workspace.name,
                                      description=workspace.description,
                                      groups=groups,
                                      members=members,
                                      policies=policies,
                                      polls=polls)


# Update a workspace
async def update_workspace(workspace: Workspace,
                           input_data: WorkspaceSchemas.WorkspaceUpdateRequest) -> WorkspaceSchemas.Workspace:
    save_changes = False
    # Check if user suplied a name
    if input_data.name and input_data.name != workspace.name:
        # Check if workspace name is unique
        if await Workspace.find_one({"name": input_data.name}) and workspace.name != input_data.name:
            raise WorkspaceExceptions.NonUniqueName(input_data.name)
        workspace.name = input_data.name  # Update the name
        save_changes = True
    # Check if user suplied a description
    if input_data.description and input_data.description != workspace.description:
        workspace.description = input_data.description  # Update the description
        save_changes = True
    # Save the updated workspace
    if save_changes:
        await Workspace.save(workspace)
    # Return the updated workspace
    return WorkspaceSchemas.Workspace(**workspace.model_dump())


# Delete a workspace
async def delete_workspace(workspace: Workspace):
    await Workspace.delete(workspace, link_rule=DeleteRules.DO_NOTHING)
    # await Workspace.delete(workspace, link_rule=DeleteRules.DELETE_LINKS)
    if await workspace.get(workspace.id):
        raise WorkspaceExceptions.ErrorWhileDeleting(workspace.id)
    await Policy.find(Policy.parent_resource.id == workspace.id).delete()  # type: ignore
    await Group.find(Group.workspace.id == workspace).delete()  # type: ignore


# List all members of a workspace
async def get_workspace_members(workspace: Workspace) -> MemberSchemas.MemberList:
    member_list = []
    member: Account

    account: Account = AccountManager.active_user.get()

    permissions = await Permissions.get_all_permissions(workspace, account)
    req_permissions = Permissions.WorkspacePermissions["get_workspace_members"]  # type: ignore
    if Permissions.check_permission(permissions, req_permissions):
        for member in workspace.members:  # type: ignore
            member_data = member.model_dump(include={'id', 'first_name', 'last_name', 'email'})
            member_scheme = MemberSchemas.Member(**member_data)
            member_list.append(member_scheme)
    # Return the list of members
    return MemberSchemas.MemberList(members=member_list)


# Add groups/members to group
async def add_workspace_members(workspace: Workspace,
                                member_data: MemberSchemas.AddMembers) -> MemberSchemas.MemberList:
    accounts = set(member_data.accounts)
    # Remove existing members from the accounts set
    accounts = accounts.difference({member.id for member in workspace.members})  # type: ignore
    # Find the accounts from the database
    account_list = await Account.find(In(Account.id, accounts)).to_list()
    # Add the accounts to the group member list with basic permissions
    for account in account_list:
        await workspace.add_member(account, Permissions.WORKSPACE_BASIC_PERMISSIONS, save=False)
    await Workspace.save(workspace, link_rule=WriteRules.WRITE)
    # Return the list of members added to the group
    return MemberSchemas.MemberList(members=[MemberSchemas.Member(**account.model_dump()) for account in account_list])


# Remove a member from a workspace
async def remove_workspace_member(workspace: Workspace, account_id: ResourceID):
    # Check if account_id is specified in request, if account_id is not specified, use the current user
    if account_id:
        account = await Account.get(account_id)  # type: ignore
    else:
        account = AccountManager.active_user.get()
    # Check if the account exists
    if not account:
        raise AccountExceptions.AccountNotFound(account_id)
    # Check if the account is a member of the workspace
    if account.id not in [ResourceID(member.id) for member in workspace.members]:  # type: ignore
        raise WorkspaceExceptions.UserNotMember(workspace, account)
    # Remove the account from the workspace
    if await workspace.remove_member(account):
        # Return the list of members added to the group
        member_list = [MemberSchemas.Member(**account.model_dump()) for account in workspace.members]  # type: ignore
        return MemberSchemas.MemberList(members=member_list)
    raise WorkspaceExceptions.ErrorWhileRemovingMember(workspace, account)


# Get a list of groups where the account is a member
async def get_groups(workspace: Workspace) -> GroupSchemas.GroupList:
    account = AccountManager.active_user.get()
    permissions = await Permissions.get_all_permissions(workspace, account)
    # Check if the user has permission to get all groups
    req_permissions = Permissions.WorkspacePermissions["get_groups"]  # type: ignore
    if Permissions.check_permission(permissions, req_permissions):
        groups = [GroupSchemas.GroupShort(**group.model_dump()) for group in workspace.groups]  # type: ignore
    # Otherwise, return only the groups where the user has permission to get the group
    else:
        groups = []
        for group in workspace.groups:
            user_permissions = await Permissions.get_all_permissions(group, account)
            required_permission = Permissions.GroupPermissions['get_group']
            if Permissions.check_permission(Permissions.GroupPermissions(user_permissions),  # type: ignore
                                            required_permission):
                groups.append(GroupSchemas.GroupShort(**group.model_dump()))  # type: ignore
    # Return the list of groups
    return GroupSchemas.GroupList(groups=groups)


# Create a new group with account as the owner
async def create_group(workspace: Workspace,
                       input_data: GroupSchemas.GroupCreateInput) -> GroupSchemas.GroupCreateOutput:
    # await workspace.fetch_link(workspace.groups)
    account = AccountManager.active_user.get()

    # Check if group name is unique
    group: Group  # For type hinting, until Link type is supported
    for group in workspace.groups:  # type: ignore
        if group.name == input_data.name:
            raise GroupExceptions.NonUniqueName(group)

    # Create a new group
    new_group = Group(name=input_data.name,
                      description=input_data.description,
                      workspace=workspace)  # type: ignore

    # Check if group was created
    if not new_group:
        raise GroupExceptions.ErrorWhileCreating(new_group)

    # Add the account to group member list
    await new_group.add_member(account, Permissions.GROUP_ALL_PERMISSIONS)

    # Create a policy for the new group
    permissions = Permissions.WORKSPACE_BASIC_PERMISSIONS  # type: ignore
    new_policy = Policy(policy_holder_type='group',
                        policy_holder=(await create_link(new_group)),
                        permissions=permissions,
                        parent_resource=workspace)  # type: ignore

    # Add the group and the policy to the workspace
    workspace.policies.append(new_policy)  # type: ignore
    workspace.groups.append(new_group)  # type: ignore
    await Workspace.save(workspace, link_rule=WriteRules.WRITE)

    # Return the new group
    return GroupSchemas.GroupCreateOutput(**new_group.model_dump(include={'id', 'name', 'description'}))


# Get all policies of a workspace
async def get_workspace_policies(workspace: Workspace) -> PolicySchemas.PolicyList:
    policy_list = await PolicyActions.get_policies(resource=workspace)

    return PolicySchemas.PolicyList(policies=policy_list.policies)


# Get a policy of a workspace
async def get_workspace_policy(workspace: Workspace,
                               account_id: ResourceID | None = None) -> PolicySchemas.PolicyOutput:
    # Check if account_id is specified in request, if account_id is not specified, use the current user
    account: Account = await Account.get(account_id) if account_id else AccountManager.active_user.get()  # type: ignore
    policy_list = await PolicyActions.get_policies(resource=workspace, policy_holder=account)
    user_policy = policy_list.policies[0]

    return PolicySchemas.PolicyOutput(
        permissions=user_policy.permissions,  # type: ignore
        policy_holder=user_policy.policy_holder)


# Set permissions for a user in a workspace
async def set_workspace_policy(workspace: Workspace,
                               input_data: PolicySchemas.PolicyInput) -> PolicySchemas.PolicyOutput:
    policy: Policy | None = None
    account: Account | None = None
    if input_data.policy_id:
        policy = await Policy.get(input_data.policy_id)
        if not policy:
            raise PolicyExceptions.PolicyNotFound(input_data.policy_id)
        # BUG: Beanie cannot fetch policy_holder link, as it can be a Group or an Account
        else:
            account = await Account.get(policy.policy_holder.ref.id)
    else:
        if input_data.account_id:
            account = await Account.get(input_data.account_id)
            if not account:
                raise AccountExceptions.AccountNotFound(input_data.account_id)
        else:
            account = AccountManager.active_user.get()
        # Make sure the account is loaded
        if not account:
            raise ResourceExceptions.APIException(code=500, detail='Unknown error')  # Should not happen

        try:
            # Find the policy for the account
            p: Policy
            for p in workspace.policies:  # type: ignore
                if p.policy_holder_type == "account":
                    if p.policy_holder.ref.id == account.id:
                        policy = p
                        break
                # if not policy:
                #     policy = Policy(policy_holder_type='account',
                #                     policy_holder=(await create_link(account)),
                #                     permissions=Permissions.WorkspacePermissions(0),
                #                     workspace=workspace)
        except Exception as e:
            raise ResourceExceptions.InternalServerError(str(e))

    # Calculate the new permission value from request
    new_permission_value = 0
    for i in input_data.permissions:
        try:
            new_permission_value += Permissions.WorkspacePermissions[i].value  # type: ignore
        except KeyError:
            raise ResourceExceptions.InvalidPermission(i)
    # Update permissions
    policy.permissions = Permissions.WorkspacePermissions(new_permission_value)  # type: ignore
    await Policy.save(policy)

    # Get Account or Group from policy_holder link
    # HACK: Have to do it manualy, as Beanie cannot fetch policy_holder link of mixed types (Account | Group)
    if policy.policy_holder_type == "account":  # type: ignore
        policy_holder = await Account.get(policy.policy_holder.ref.id)  # type: ignore
    elif policy.policy_holder_type == "group":  # type: ignore
        policy_holder = await Group.get(policy.policy_holder.ref.id)  # type: ignore

    # Return the updated policy
    return PolicySchemas.PolicyOutput(
        permissions=Permissions.WorkspacePermissions(policy.permissions).name.split('|'),  # type: ignore
        policy_holder=MemberSchemas.Member(**policy_holder.model_dump()))  # type: ignore


# Get a list of polls in a workspace
async def get_polls(workspace: Workspace) -> PollSchemas.PollList:
    return await PollActions.get_polls(workspace)


# Create a new poll in a workspace
async def create_poll(workspace: Workspace, input_data: PollSchemas.CreatePollRequest) -> PollSchemas.PollResponse:
    # Check if poll name is unique
    poll: Poll  # For type hinting, until Link type is supported
    for poll in workspace.polls:  # type: ignore
        if poll.name == input_data.name:
            raise PollExceptions.NonUniqueName(poll)

    # Create a new poll
    new_poll = Poll(name=input_data.name,
                    description=input_data.description,
                    workspace=workspace,  # type: ignore
                    public=input_data.public,
                    published=input_data.published,
                    questions=input_data.questions,
                    policies=[])

    # Check if poll was created
    if not new_poll:
        raise PollExceptions.ErrorWhileCreating(new_poll)

    # Add the poll to the workspace
    workspace.polls.append(new_poll)  # type: ignore
    await Workspace.save(workspace, link_rule=WriteRules.WRITE)

    # Return the new poll
    return PollSchemas.PollResponse(**new_poll.model_dump())
