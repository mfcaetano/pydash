import json


player_parameters = '{"buffer_size" : 120, "max_buffer_size" : 60, "buffering_until" : 5, "playbak_step" : 1}'

player_parameters_dic = json.loads(player_parameters)

print(json.dumps(player_parameters_dic, indent = 4, sort_keys=True))