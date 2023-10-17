""" mcli modify user functions """
import argparse
import logging
from typing import Optional

from mcli.api.users.api_get_users import get_users as api_get_users
from mcli.config import MCLIConfig
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def modify_user(
    user_identifier: Optional[str] = None,
    **kwargs,
) -> int:
    """Updates user for admin mode.

    Args:
        user_identifier: Either the user id or the email of the user to set.
                         If None, then the user is cleared.

    Returns:
        0 if succeeded, else 1 (e.g., if the user is not found)
    """
    del kwargs

    # Get the current user
    conf = MCLIConfig.load_config()

    # Unset operations can be completed immediately.
    if user_identifier is None:
        conf.user_id = None
        conf.save_config()
        logger.info(f"{OK} Removed User")
        return 0

    # Set operations requires a query of all users to find the user that
    # corresponds to the provided id or email.
    #
    # NOTE: As the number of users grows, we may need to implement a query
    #       that directly filters on id/email to avoid looping through all
    #       users.
    user_id = None
    user_email = None
    users = api_get_users()
    for user in users:
        if user_identifier in (user.id, user.email):
            user_id = user.id
            user_email = user.email
            break

    if user_id is None:
        logger.error(f"{FAIL} Unable to find User {user_identifier}")
        return 1
    else:
        conf.user_id = user_id
        conf.save_config()
        logger.info(f"{OK} Updated User ID to {user_id} ({user_email})")
        return 0


def configure_user_argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("user_identifier", help="user id or email")
