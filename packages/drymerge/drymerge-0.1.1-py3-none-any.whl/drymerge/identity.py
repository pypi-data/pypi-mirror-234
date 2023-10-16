import re


class IdentityError(Exception):
    pass


class DryId:
    VALID_TYPES = {"queue", "api", "merge", "state", "route", "fragment", "fn"}

    def __init__(self, name, type_, namespace=None, organization=None, version=None):
        if not self.is_valid_string(name) or \
                (namespace and not self.is_valid_string(namespace)) or \
                (organization and not self.is_valid_string(organization)):
            raise IdentityError("Invalid characters in name, namespace, or organization.")

        if type_ not in self.VALID_TYPES:
            raise IdentityError(f"Invalid type: {type_}. Must be one of: {', '.join(self.VALID_TYPES)}")

        if version and not isinstance(version, int):
            raise IdentityError("Version must be an integer or None.")

        self.name = name
        self.namespace = namespace
        self.organization = organization
        self.type_ = type_
        self.version = version

    def __str__(self):
        namespace_str = f"{self.namespace}/" if self.namespace else "~/"
        organization_str = f"{self.organization}/" if self.organization else ""
        version_str = f":{self.version}" if self.version else ""
        type_str = f".{self.type_}" if self.type_ else ""
        idstr = f"{organization_str}{namespace_str}{self.name}{type_str}{version_str}"
        return idstr

    @staticmethod
    def is_valid_string(value):
        return not any(char in value for char in ['/', ':', '.'])

    @staticmethod
    def parse_identity_string(id_str):
        parts = id_str.split('/')
        if len(parts) != 3:
            raise IdentityError(f"Invalid identity string: {id_str}")

        organization, namespace, remainder = parts
        name, type_, version = DryId.parse_remainder(remainder)

        return DryId(name, namespace, organization, type_, version)

    @staticmethod
    def parse_remainder(remainder):
        match = re.match(r"([^\.]+)\.([^:]+)(?::(\d+))?", remainder)
        if not match:
            raise IdentityError(f"Invalid remainder format: {remainder}")

        name, type_, version = match.groups()
        return name, type_, int(version) if version else None
