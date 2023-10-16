def switch_case(switch_dict, case, default_case):
    return switch_dict.get(case, lambda: default_case)()