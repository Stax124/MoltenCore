import json


class PluginEncoder(json.JSONEncoder):
    def default(self, obj):
        data_out: dict = {}
        data_in: list[str] = list(obj.__dict__.keys())

        for i in data_in:
            if i.startswith("_"):
                continue
            if type(obj.__dict__[i]) in (list, dict, str, int, float, bool):
                data_out[i] = obj.__dict__[i]
            else:
                continue

        return data_out
