from enum import IntFlag


class Role(IntFlag):

    ADMIN = 1 << 0

    MANAGER = 1 << 1

    EMPLOYEE = 1 << 2

    @classmethod
    def extract_roles_tuple(cls):
        roles = []
        for role_name, role_value in cls.__dict__.get("_member_map_").items():
            roles.append((role_value.value, role_name.lower().capitalize()))

        return roles
