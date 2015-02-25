# TeamCityRestClient
Basic driver for TeamCity rest api: get builds info, cancel build, stop build.

usage example:
Build Setups: we have CPP, JAVA, SQL builds. need to cancel setups build if 1 of : CPP, JAVA, SQL is red.   
tc_client = TCClient(user, password, "teamcity-portal", 9090)
need_to_cancel = tc_client.get_build_fail_status_by_type('JAVA_BUILD') or \
                         tc_client.get_build_fail_status_by_type('CPP_BUILD') or \
                         tc_client.get_build_fail_status_by_type('SQL_BUILD')
if not need_to_cancel:
	return
print ('canceling current setup build')
print (build_id)
build_id = tc_client.get_running_builds_by_type('SETUP')
if not build_id == -1:
	tc_client.cancel_running_build(build_id)



