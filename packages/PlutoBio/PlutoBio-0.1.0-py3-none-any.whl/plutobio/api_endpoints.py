from enum import Enum


class APIEndpoints(str, Enum):
    experiments = "lab/experiments"
    projects = "lab/projects"
