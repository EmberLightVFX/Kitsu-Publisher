from . import client as raw

from .helpers import normalize_model_parameter

default = raw.default_client


def update_shot_casting(project, shot, casting, client=default):
***REMOVED***
    Change casting of given shot with given casting (list of asset ids displayed
    into the shot).

    Args:
        shot (str / dict): The shot dict or the shot ID.
        casting (dict): The casting description.
        Ex: `casting = [{"asset_id": "asset-1", "nb_occurences": 3}]`

    Returns:
        dict: Related shot.
***REMOVED***
    shot = normalize_model_parameter(shot)
    project = normalize_model_parameter(project)
    path = "data/projects/%s/entities/%s/casting" % (project["id"], shot["id"])
    return raw.put(path, casting, client=client)


def update_asset_casting(project, asset, casting, client=default):
***REMOVED***
    Change casting of given asset with given casting (list of asset ids
    displayed into the asset).

    Args:
        asset (str / dict): The asset dict or the asset ID.
        casting (dict): The casting description.
        Ex: `casting = [{"asset_id": "asset-1", "nb_occurences": 3}]`

    Returns:
        dict: Related asset.
***REMOVED***
    asset = normalize_model_parameter(asset)
    project = normalize_model_parameter(project)
    path = "data/projects/%s/entities/%s/casting" % (
        project["id"],
        asset["id"],
    )
    return raw.put(path, casting, client=client)


def get_asset_type_casting(project, asset_type, client=default):
***REMOVED***
    Return casting for given asset_type.
    `casting = {
        "asset-id": [{"asset_id": "asset-1", "nb_occurences": 3}],
        ...
      }
    `
    Args:
        project (str / dict): The project dict or the project ID.
        asset_type (str / dict): The asset_type dict or the asset_type ID.

    Returns:
        dict: Casting of the given asset_type.
***REMOVED***

    project = normalize_model_parameter(project)
    asset_type = normalize_model_parameter(asset_type)
    path = "/data/projects/%s/asset-types/%s/casting" % (
        project["id"],
        asset_type["id"],
    )
    return raw.get(path, client=client)


def get_sequence_casting(sequence, client=default):
***REMOVED***
    Return casting for given sequence.
    `casting = {
        "shot-id": [{"asset_id": "asset-1", "nb_occurences": 3}]},
        ...
     }
    `
    Args:
        sequence (dict): The sequence dict

    Returns:
        dict: Casting of the given sequence.
***REMOVED***
    path = "/data/projects/%s/sequences/%s/casting" % (
        sequence["project_id"],
        sequence["id"],
    )
    return raw.get(path, client=client)


def get_shot_casting(shot, client=default):
***REMOVED***
    Return casting for given shot.
    `[{"asset_id": "asset-1", "nb_occurences": 3}]}`
    Args:
        shot (dict): The shot dict

    Returns:
        dict: Casting of the given shot.
***REMOVED***
    path = "/data/projects/%s/entities/%s/casting" % (
        shot["project_id"],
        shot["id"],
    )
    return raw.get(path, client=client)


def get_asset_casting(asset, client=default):
***REMOVED***
    Return casting for given asset.
    `[{"asset_id": "asset-1", "nb_occurences": 3}]}`
    Args:
        asset (dict): The asset dict

    Returns:
        dict: Casting for given asset.
***REMOVED***
    path = "/data/projects/%s/entities/%s/casting" % (
        asset["project_id"],
        asset["id"],
    )
    return raw.get(path, client=client)


def get_asset_cast_in(asset, client=default):
***REMOVED***
    Return shot list where given asset is casted.
    Args:
        asset (dict): The asset dict

    Returns:
        dict: Shot list where given asset is casted.
***REMOVED***
    asset = normalize_model_parameter(asset)
    path = "/data/assets/%s/cast-in" % asset["id"]
    return raw.get(path, client=client)


def all_entity_links_for_project(project, client=default):
***REMOVED***
    Args:
        project (dict): The project

    Returns:
        dict: Entity links for given project.
***REMOVED***
    project = normalize_model_parameter(project)
    path = "/data/projects/%s/entity-links" % project["id"]
    return raw.get(path, client=client)
