# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from structured_log_json import jsonlogger
import logging
'''
1. inherited  logging class Formatter;
2. inherited  logging class Handler;
'''


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    logger = jsonlogger.setup_logging("./", "mimicrouter", __name__, "dmf", logging.INFO,['filename','processName'])
    test = {

        "event_domain": "mimic_multimode_ruling",
        "event_action": "attack",
        "event_object":"test1",
        "event_service":"test2",
        "event_status":"test3",
        "event_subject":"test4",
        "router_multimode_ruling":
            [
	            {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"2.2.2.2",
                    "mask":32,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
                {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"11.11.11.11",
                    "mask":32,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
                {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"100.0.12.0",
                    "mask":24,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
	            {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"100.0.17.0",
                    "mask":24,
                    "nexthop_info.nexthop":["100.0.13.3"]
			    }

		    ]
    }
    for i in range(5):
        print(logger.info("test",extra=test))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
