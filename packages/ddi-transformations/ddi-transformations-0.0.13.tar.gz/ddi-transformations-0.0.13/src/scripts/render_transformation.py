import os
import traceback

from jinja2 import Environment, FileSystemLoader


class Transformations:
    TEMPLATE_PATH = template_folder = os.path.dirname(__file__) + "/../resources"
    TEMPLATE_NAME = "transformations_macro.sql"
    FIELDS = "fields"
    COLUMN_NAME = "name"
    SYSTEM_NAME = "systemName"
    JOB_NODE = "mapIngestionJobFieldColumnDTO"
    MAPPING = "mapping"
    CONFIG = "config"
    TRANSFORMATION_NODE = "transformations"
    SO = "SO"
    OBJECT = "object"

    @staticmethod
    def get_transformation(job_details: dict, column_mapping: dict, object_type: str):
        print("Start: get_transformation")
        transformation_resp = {}

        try:
            file_loader = FileSystemLoader(Transformations.TEMPLATE_PATH)
            env = Environment(loader=file_loader)
            template = env.get_template(Transformations.TEMPLATE_NAME)
            template.globals.update({'return': Transformations.return_function,
                                     'add_quotes': Transformations.add_quotes})

            if object_type == Transformations.SO:
                transformation_resp = Transformations.get_so_transformation(job_details, column_mapping, template)
            else:
                transformation_resp = Transformations.get_co_transformation(job_details, template)

        except TypeError as e:
            print(f"TypeError = {traceback.format_exc()}")
            raise

        except IndexError as e:
            print(f"IndexError = {traceback.format_exc()}")
            raise

        except KeyError as e:
            print(f"KeyError = {traceback.format_exc()}")
            raise

        except ValueError as e:
            print(f"ValueError = {traceback.format_exc()}")
            raise

        except AttributeError as e:
            print(f"AttributeError = {traceback.format_exc()}")
            raise

        except IOError as e:
            print(f"IOError = {traceback.format_exc()}")
            raise

        except Exception as e:
            print(f"Exception = {traceback.format_exc()}")
            raise

        print(f"End: get_transformation with response = {transformation_resp}")
        return transformation_resp

    def get_so_transformation(job_details, column_mapping, template):
        print("Start: get_so_transformation")
        transformation_resp = {}

        for job_data in job_details[Transformations.JOB_NODE]:
            column_name = column_mapping[job_data[Transformations.SYSTEM_NAME]]
            transform_output = ""
            trans_config = job_data[Transformations.MAPPING][0][Transformations.CONFIG][Transformations.TRANSFORMATION_NODE]

            if trans_config is not None and len(trans_config) > 0:
                transform_details = trans_config[0]
                transform_output = template.render(transform_details=transform_details, column_name=column_name).strip()
            transformation_resp[column_name] = transform_output

        print(f"End: get_so_transformation")
        return transformation_resp

    def get_co_transformation(job_details, template):
        print("Start: get_co_transformation")
        transformation_resp = {}

        for job_data in job_details[Transformations.OBJECT][Transformations.FIELDS]:
            column_name = job_data[Transformations.COLUMN_NAME]
            transform_output = ""
            trans_config = None

            if Transformations.TRANSFORMATION_NODE in job_data:
                trans_config = job_data[Transformations.TRANSFORMATION_NODE]

            if trans_config is not None and len(trans_config) > 0:
                transform_details = trans_config[0]
                transform_output = template.render(transform_details=transform_details, column_name=column_name).strip()
            transformation_resp[column_name] = transform_output

        print(f"End: get_co_transformation")
        return transformation_resp

    def return_function(var):
        return var

    def add_quotes(var):
        return "'" + var + "'"
        
 
if __name__ == '__main__':
    Transformations.get_transformation({}, {}, "SO")

