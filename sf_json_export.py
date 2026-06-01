import json

def write_sf_json(var1_name, var2_name, edges1, edges2,
                  sf_pass, unc_pass, sf_fail, unc_fail,
                  out_path, description="auto-generated scale factors"):
    data_template = lambda name, contents, descr: {
        "name": name,
        "version": 1,
        "inputs": [
            {"name": var1_name, "type": "real", "description": var1_name},
            {"name": var2_name, "type": "real", "description": var2_name}
        ],
        "output": {"name": "sf", "type": "real", "description": descr},
        "data": {
            "nodetype": "multibinning",
            "inputs": [var1_name, var2_name],
            "edges": [edges1, edges2],
            "content": contents,
            "flow": "clamp"
        }
    }
    payload = {
        "schema_version": 2,
        "description": description,
        "corrections": [
            data_template("sf_pass" , sf_pass , "data/MC scale factor (pass)"),
            data_template("unc_pass", unc_pass, "uncertainty (pass)"),
            data_template("sf_fail" , sf_fail , "data/MC scale factor (fail)"),
            data_template("unc_fail", unc_fail, "uncertainty (fail)")
        ]
    }
    with open(out_path, 'w') as f:
        json.dump(payload, f, indent=2)
