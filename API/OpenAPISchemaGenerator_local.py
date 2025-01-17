# Import modules for SWAGGER UI (API documentation)
from drf_yasg.generators import OpenAPISchemaGenerator
import os


# Override methods in order to avoid duplications for multi-method views
class OpenAPISchemaGenerator_local(OpenAPISchemaGenerator):
    # Set an empty list [] for the given cases
    def remove_items_from_op_key_list(self, op_key_list):
        # The input list follows the pattern ['POST','save_user_tip','create']
        # Valid combinations are: POST-create, PUT-update, DELETE-delete
        if str(op_key_list[0]) == "POST" and str(op_key_list[2]) in ["update", "delete"]:
            elem2 = str(op_key_list[2])
            op_key_list.pop(0)
            op_key_list.pop(0)
            op_key_list.remove(elem2)
        elif str(op_key_list[0]) == "PUT" and str(op_key_list[2]) in ["create", "delete"]:
            elem2 = str(op_key_list[2])
            op_key_list.pop(0)
            op_key_list.pop(0)
            op_key_list.remove(elem2)
        elif str(op_key_list[0]) == "DELETE" and str(op_key_list[2]) in ["create", "update"]:
            elem2 = str(op_key_list[2])
            op_key_list.pop(0)
            op_key_list.pop(0)
            op_key_list.remove(elem2)
        return op_key_list

    # Remove lists from the original list generated by super() method
    def get_operation_keys(self, subpath, method, view):
        op_key_list_orig = super().get_operation_keys(subpath, method, view)
        op_key_list_new = self.remove_items_from_op_key_list(op_key_list_orig)
        return op_key_list_new

    # Handle the cases when the above list is empty
    def get_operation(self, view, path, prefix, method, components, request):
        if len(self.get_operation_keys(path[len(prefix) :], method, view)) == 0:
            return None
        else:
            return super().get_operation(view, path, prefix, method, components, request)

    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Add both HTTP and HTTPS to the list of schemes
        schema.schemes = ["https"]
        if os.environ.get("ENVIRONMENT_NAME") == "LOC":
            schema.schemes = ["http"]

        return schema
