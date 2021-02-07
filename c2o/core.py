import os, pathlib, json
from fhir.resources.capabilitystatement import *
from openapi_core.schema.specs.factories import SpecFactory
from openapi_core.schema.specs.models import Spec
from openapi_core import create_spec
from openapi_spec_validator import default_handlers
from jsonschema.validators import RefResolver
from openapi_schema_pydantic import OpenAPI
from helpers.observable import *

print("Hello World")


def convert(cap_statement, ops={}):
    """
    Converts a FHIR Capability Statement to OpenApi
    :param cap_statement:
    :param ops:
    :return:
    """
    blank_dict = {
        "info": {
            "title": "",
            "description": "",
            "version": ""
        },
        "paths": []
    }
    open_api = OpenAPI(**blank_dict)

    context = {
        "completed_events": [],
        "queued_events": [],
        "path": "",
        "parent": "",
        "fhir": cap_statement,
        "open_api": open_api
    }
    open_api.info.description
    on_start.notify_observers(cap_statement, context)
    recurse_object(cap_statement)
    on_end.notify_observers(cap_statement, context)

# events
on_start = Observable()
on_key_value = Observable()
on_value = Observable()
on_increased_depth = Observable()
on_end = Observable()


class CapabilityStatementObserver(Observer):
    @staticmethod
    def discriminator(self, event, context):
        return context["parent"] == "" and context["fhir"]["resourceType"] == "CapabilityStatement"

    def action(self, event, context):
        pass


CapabilityStatementObserver(on_start)

def recurse_object(obj, context):
    on_increased_depth.notify_observers({"value": obj}, context)
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                recurse_object(v, context)
            else:
                on_key_value.notify_observers({"key": k, "value": v}, context)
    else:
        for v in obj:
            if isinstance(v, dict) or isinstance(v, list):
                recurse_object(v, context)
            else:
                on_value.notify_observers({"value": v}, context)


def trigger():
    pass

def update_context():
    pass

"""
Loop through,
Process values,
Save dicts and arrays for end.
"""
cap_statement = json.load("data/example.json")  # CapabilityStatement.parse_file("data/example.json")
