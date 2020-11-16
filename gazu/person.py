from . import client as raw

from .sorting import sort_by_name
from .helpers import normalize_model_parameter
from .cache import cache

default = raw.default_client


@cache
def all_organisations(client=default):
***REMOVED***
    Returns:
        list: Organisations listed in database.
***REMOVED***
    return sort_by_name(raw.fetch_all("organisations", client=client))


@cache
def all_persons(client=default):
***REMOVED***
    Returns:
        list: Persons listed in database.
***REMOVED***
    return sort_by_name(raw.fetch_all("persons", client=client))


@cache
def get_person(id, client=default):
***REMOVED***
    Args:
        id (str): An uuid identifying a person.

    Returns:
        dict: Person corresponding to given id.
***REMOVED***
    return raw.fetch_one("persons", id, client=client)


@cache
def get_person_by_desktop_login(desktop_login, client=default):
***REMOVED***
    Args:
        desktop_login (str): Login used to sign in on the desktop computer.

    Returns:
        dict: Person corresponding to given desktop computer login.
***REMOVED***
    return raw.fetch_first(
        "persons", {"desktop_login": desktop_login}, client=client
    )


@cache
def get_person_by_email(email, client=default):
***REMOVED***
    Args:
        email (str): User's email.

    Returns:
        dict:  Person corresponding to given email.
***REMOVED***
    return raw.fetch_first("persons", {"email": email}, client=client)


@cache
def get_person_by_full_name(full_name, client=default):
***REMOVED***
    Args:
        full_name (str): User's full name

    Returns:
        dict: Person corresponding to given name.
***REMOVED***
    if " " in full_name:
        first_name, last_name = full_name.lower().split(" ")
***REMOVED***
        first_name, last_name = full_name.lower().strip(), ""
    for person in all_persons():
        is_right_first_name = first_name == person["first_name"].lower().strip()
        is_right_last_name = \
            len(last_name) == 0 or last_name == person["last_name"].lower()
        if is_right_first_name and is_right_last_name:
***REMOVED*** person
    return None


@cache
def get_person_url(person, client=default):
***REMOVED***
    Args:
        person (str / dict): The person dict or the person ID.

    Returns:
        url (str): Web url associated to the given person
***REMOVED***
    person = normalize_model_parameter(person)
    path = "{host}/people/{person_id}/"
    return path.format(
        host=raw.get_api_url_from_host(client=client),
        person_id=person["id"],
    )


@cache
def get_organisation(client=default):
***REMOVED***
    Returns:
        dict: Database information for organisation linked to auth tokens.
***REMOVED***
    return raw.get("auth/authenticated", client=client)["organisation"]


def new_person(
    first_name, last_name, email, phone="", role="user", desktop_login="",
    client=default
):
***REMOVED***
    Create a new person based on given parameters. His/her password will is
    set automatically to default.

    Args:
        first_name (str):
        last_name (str):
        email (str):
        phone (str):
        role (str): user, manager, admin (wich match CG artist, Supervisor
                    and studio manager)
        desktop_login (str): The login the users uses to log on its computer.

    Returns:
        dict: Created person.
***REMOVED***
    person = get_person_by_email(email)
    if person is None:
        person = raw.post(
            "data/persons/new",
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "role": role,
                "desktop_login": desktop_login,
            },
            client=client
***REMOVED***
    return person


def set_avatar(person, file_path, client=default):
***REMOVED***
    Upload picture and set it as avatar for given person.

    Args:
        person (str / dict): The person dict or the person ID.
        file_path (str): Path where the avatar file is located on the hard
                         drive.
***REMOVED***
    person = normalize_model_parameter(person)
    return raw.upload(
        "/pictures/thumbnails/persons/%s" % person["id"],
        file_path,
        client=client
    )


def get_presence_log(year, month, client=default):
***REMOVED***
    Args:
        year (int):
        month (int):

    Returns:
        The presence log table for given month and year.
***REMOVED***
    path = "data/persons/presence-logs/%s-%s" % (year, str(month).zfill(2))
    return raw.get(path, json_response=False, client=client)
