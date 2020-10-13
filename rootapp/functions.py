def built_general_error_response_json(error_json):
	error_list = []
	for key in error_json:
		error_list.append({"title": key, "descr": error_json[key][0]["message"]})
	helper_dict = {"error": error_list}
	return helper_dict


def built_list_error_response_json(error_json):
	error_list = []
	for field in error_json:
		error_list.append({"title": field["code"], "descr": field["message"]})

	helper_dict = {"error": error_list}
	return helper_dict

def process_general_form_errors(error_dict):
	field = next(iter(error_dict))

	if field != "__all__":
		# response_json = built_general_error_response_json("Error in POST parameters",
		# 										  "Plz check Post Param specifications")
		response_json = built_general_error_response_json(error_dict)
		return response_json

	response_json = built_list_error_response_json(error_dict["__all__"])
	return response_json