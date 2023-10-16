from unipoll_api import AccountManager
from unipoll_api.documents import Poll, Policy, Group, Account, Workspace
from unipoll_api.schemas import PollSchemas, QuestionSchemas, PolicySchemas, MemberSchemas, WorkspaceSchemas
from unipoll_api.utils import Permissions
from unipoll_api.exceptions import ResourceExceptions


async def get_polls(workspace: Workspace | None = None) -> PollSchemas.PollList:
    account = AccountManager.active_user.get()
    req_permissions = Permissions.WorkspacePermissions["get_polls"]  # type: ignore
    all_workspaces = [workspace] if workspace else await Workspace.find(fetch_links=True).to_list()

    poll_list = []
    for workspace in all_workspaces:
        permissions = await Permissions.get_all_permissions(workspace, account)
        if Permissions.check_permission(permissions, req_permissions):
            poll_list += workspace.polls  # type: ignore
        else:
            req_permissions = Permissions.WorkspacePermissions["get_poll"]
            for poll in workspace.polls:  # type: ignore
                if poll.public:  # type: ignore
                    poll_list.append(poll)
                else:
                    permissions = await Permissions.get_all_permissions(poll, account)
                    if Permissions.check_permission(permissions, req_permissions):
                        poll_list.append(poll)
    # Build poll list and return the result
    for poll in poll_list:
        poll_list.append(PollSchemas.PollShort(**poll.model_dump()))  # type: ignore
    return PollSchemas.PollList(polls=poll_list)


async def get_poll(poll: Poll,
                   include_questions: bool = False,
                   include_policies: bool = False) -> PollSchemas.PollResponse:
    account = AccountManager.active_user.get()
    questions = []
    policies = None

    permissions = await Permissions.get_all_permissions(poll, account)
    # Fetch the resources if the user has the required permissions
    if include_questions:
        req_permissions = Permissions.PollPermissions["get_poll_questions"]  # type: ignore
        if poll.public or Permissions.check_permission(permissions, req_permissions):
            questions = (await get_poll_questions(poll)).questions
    if include_policies:
        req_permissions = Permissions.PollPermissions["get_poll_policies"]  # type: ignore
        if Permissions.check_permission(permissions, req_permissions):
            policies = (await get_poll_policies(poll)).policies

    workspace = WorkspaceSchemas.WorkspaceShort(**poll.workspace.model_dump())  # type: ignore

    # Return the workspace with the fetched resources
    return PollSchemas.PollResponse(id=poll.id,
                                    name=poll.name,
                                    description=poll.description,
                                    public=poll.public,
                                    published=poll.published,
                                    workspace=workspace,
                                    questions=questions,
                                    policies=policies)


async def get_poll_questions(poll: Poll) -> QuestionSchemas.QuestionList:
    print("Poll: ", poll.questions)
    question_list = []
    for question in poll.questions:
        # question_data = question.model_dump()
        question_scheme = QuestionSchemas.Question(**question)
        question_list.append(question_scheme)
    # Return the list of questions
    return QuestionSchemas.QuestionList(questions=question_list)


async def get_poll_policies(poll: Poll) -> PolicySchemas.PolicyList:
    policy_list = []
    policy: Policy
    for policy in poll.policies:  # type: ignore
        permissions = Permissions.pollPermissions(policy.permissions).name.split('|')  # type: ignore
        # Get the policy_holder
        if policy.policy_holder_type == 'account':
            policy_holder = await Account.get(policy.policy_holder.ref.id)
        elif policy.policy_holder_type == 'group':
            policy_holder = await Group.get(policy.policy_holder.ref.id)
        else:
            raise ResourceExceptions.InternalServerError("Invalid policy_holder_type")
        if not policy_holder:
            # TODO: Replace with custom exception
            raise ResourceExceptions.InternalServerError("get_poll_policies() => Policy holder not found")
        # Convert the policy_holder to a Member schema
        policy_holder = MemberSchemas.Member(**policy_holder.model_dump())  # type: ignore
        policy_list.append(PolicySchemas.PolicyShort(id=policy.id,
                                                     policy_holder_type=policy.policy_holder_type,
                                                     # Exclude unset fields(i.e. "description" for Account)
                                                     policy_holder=policy_holder.model_dump(exclude_unset=True),
                                                     permissions=permissions))
    return PolicySchemas.PolicyList(policies=policy_list)


async def update_poll(poll: Poll, data: PollSchemas.UpdatePollRequest) -> PollSchemas.PollResponse:
    # Update the poll
    if data.name:
        poll.name = data.name
    if data.description:
        poll.description = data.description
    if data.public is not None:
        poll.public = data.public
    if data.published is not None:
        poll.published = data.published
    if data.questions:
        poll.questions = data.questions

    # Save the updated poll
    await Poll.save(poll)
    return await get_poll(poll, include_questions=True)


async def delete_poll(poll: Poll):
    # Delete the poll
    await Poll.delete(poll)

    # Check if the poll was deleted
    if await Poll.get(poll.id):
        raise ResourceExceptions.InternalServerError("Poll not deleted")
