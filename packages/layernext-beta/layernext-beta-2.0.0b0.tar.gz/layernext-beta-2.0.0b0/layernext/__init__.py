import base64

from layernext import datalake, dataset, studio
from layernext.datalake.constants import (AnnotationUploadType, ItemType,
                                          MediaType, ObjectType, SortField,
                                          SortFieldName, SortOrder)

__version__ = '2.0.0b0'

class LayerNextClient:
    """
    Python SDK of LayerNext
    """

    def __init__(self, api_key: str, secret: str, layernext_url: str) -> None:
        _string_key_secret = f'{api_key}:{secret}'
        _key_secret_bytes = _string_key_secret.encode("ascii")
        _encoded_key_secret_bytes = base64.b64encode(_key_secret_bytes)
        self.encoded_key_secret = _encoded_key_secret_bytes.decode("ascii")
        self.layernext_url = layernext_url
        self.__check_sdk_version_compatibility()

    def __check_sdk_version_compatibility(self):
        """
        Check if the SDK version is compatible with the datalake backend version
        """
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        version_id = __version__.split('b')[0]

        _datalake_client.check_sdk_version_compatibility(version_id)

    """
    Annotation data upload from json file with new format and unique_name
    """

    def upload_annotations_by_unique_name(
            self,
            operation_unique_id: str,
            json_data_file_path: str,
            is_normalized: bool,
            is_model_run: bool
    ):

        self.__upload_annotations(
            None,
            operation_unique_id,
            json_data_file_path,
            None,
            is_normalized,
            is_model_run,
            upload_type=AnnotationUploadType.BY_UNIQUE_NAME
        )

    """
    Annotation data upload from json file with new format and bucket name
    """

    def upload_annotations_by_storage_path(
            self,
            operation_unique_id: str,
            json_data_file_path: str,
            is_normalized: bool,
            is_model_run: bool,
            bucket_name: str = None
    ):

        self.__upload_annotations(
            None,
            operation_unique_id,
            json_data_file_path,
            None,
            is_normalized,
            is_model_run,
            bucket_name=bucket_name,
            upload_type=AnnotationUploadType.BY_STORAGE_PATH
        )

    """
    Deprecated - annotation data upload from json file
    """

    def upload_annoations_for_folder(
            self,
            collection_base_path: str,
            operation_unique_id: str,
            json_data_file_path: str,
            shape_type: str,
            is_normalized: bool,
            is_model_run: bool,
            destination_project_id: str = None
    ):
        
        if collection_base_path is not None and collection_base_path != "":
            collection_id = self.get_collection_id_by_name(collection_base_path)
        else:
            collection_id = None

        self.__upload_annotations(
            collection_id,
            operation_unique_id,
            json_data_file_path,
            shape_type,
            is_normalized,
            is_model_run,
            destination_project_id,
            None,
            upload_type=AnnotationUploadType.BY_FILE_NAME_OR_UNIQUE_NAME
        )

    """
    New annotation data upload from json file with new format and file name
    """

    def upload_annotations_for_collection(
            self,
            collection_name: str,
            operation_unique_id: str,
            json_data_file_path: str,
            is_normalized: bool,
            is_model_run: bool
    ):
        
        if collection_name is not None and collection_name != "":
            collection_id = self.get_collection_id_by_name(collection_name)
        else:
            raise Exception("Collection name cannot be empty")

        self.__upload_annotations(
            collection_id,
            operation_unique_id,
            json_data_file_path,
            None,
            is_normalized,
            is_model_run,
            upload_type=AnnotationUploadType.BY_FILE_NAME
        )

    """
    New annotation data upload from json file with new format and job id
    @param job_id: job id
    @param operation_unique_id: operation id
    @param json_data_file_path: json file path
    @param is_normalized: boolean
    @param is_model_run: boolean
    """

    def upload_annotations_by_job_id(
            self,
            job_id: str,
            operation_unique_id: str,
            json_data_file_path: str,
            is_normalized: bool,
            is_model_run: bool
    ):

        self.__upload_annotations(
            job_id,
            operation_unique_id,
            json_data_file_path,
            None,
            is_normalized,
            is_model_run,
            upload_type=AnnotationUploadType.BY_JOB_ID
        )
    """
    common function to upload annotations
    @param unique_id: if upload done by collection name, unique id represents collection id. if upload done by job id, unique id represents job id.
    @param operation_unique_id: operation id
    @param json_data_file_path: json file path
    @param shape_type: shape type
    @param is_normalized: boolean
    @param is_model_run: boolean
    @param destination_project_id: destination project id
    @param version: version (v1, v2) this is used to support backward compatibility
    @param bucket_name: bucket name
    @param upload_type: upload type (BY_FILE_NAME, BY_STORAGE_PATH, BY_UNIQUE_NAME, BY_FILE_NAME_OR_UNIQUE_NAME, BY_JOB_ID)
    """
    def __upload_annotations(
            self,
            unique_id: str,
            operation_unique_id: str,
            json_data_file_path: str,
            shape_type: str,
            is_normalized: bool,
            is_model_run: bool,
            destination_project_id: str = None,
            version: str = "v2",
            bucket_name: str = None,
            upload_type: AnnotationUploadType = AnnotationUploadType.BY_FILE_NAME
    ):
        """
        Upload annotation data from a json file
        """
        # init datalake client
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        if is_model_run:
            _datalake_client.upload_modelrun_from_json(
                unique_id,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized,
                destination_project_id,
                version,
                bucket_name,
                upload_type
            )
        else:
            _datalake_client.upload_groundtruth_from_json(
                unique_id,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized,
                destination_project_id,
                version,
                bucket_name,
                upload_type
            )

    """
    Download dataset
    """

    def download_dataset(
            self,
            version_id: str,
            export_type: str,
            custom_download_path: str = None,
            is_media_include=True
    ):
        # init dataset client
        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url, custom_download_path)

        # start download
        _dataset_client.download_dataset(
            version_id, export_type, is_media_include)

    """"
    Images/video upload - deprecated
    """

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object="", override=False):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.file_upload(path, collection_type, collection_name, meta_data_object,None, override, None)

    """"
    Images/video upload to a collection
    @param path: local folder path (absolute)
    @param content_type: 'image' or 'video'
    @param collection_name: Collection which files to be uploaded to.
    If existing one is given new files are added to that collection
    @param meta_data_object: Object to specify custom meta data fields and flags
    @param meta_data_override: override provided meta_data_object in case of the file exist already in datalake
    """

    def upload_files_to_collection(
            self,
            path: str,
            content_type: str,
            collection_name: str,
            meta_data_object={},
            meta_data_override=False,
            metadata_file_path=None,
            storage_prefix_path=None,
            annotation_data={
                "json_data_file_path": None,
                "operation_unique_id": None,
                "is_normalized": False,
                "is_model_run": False,
            },
            application_code=None,

    ):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        if collection_name == "":
            print(f'Invalid collection name "{collection_name}"')
            return {
                "is_success": False,
                "collection_id": None
            }
        if content_type.lower() == "image":
            collection_type = MediaType.IMAGE.value
        elif content_type.lower() == "video":
            collection_type = MediaType.VIDEO.value
        else:
            collection_type = MediaType.OTHER.value

        upload_details = _datalake_client.file_upload(
            path,
            collection_type,
            collection_name,
            meta_data_object,
            application_code,
            meta_data_override,
            storage_prefix_path
        )

        # if json file path is provided and upload is successful, upload metadata for the files
        if metadata_file_path is not None and upload_details["is_success"] == True:
            job_id = upload_details["job_id"]
            self.wait_for_job_complete(job_id)
            self.upload_metadata_by_job_id(job_id, metadata_file_path)

        # if annotation data is provided and upload is successful, upload annotations for the files
        if annotation_data["json_data_file_path"] is not None and upload_details["is_success"] == True:
            job_id = upload_details["job_id"]
            # if operation id is not provided, or is_model_run, is_normalized is not boolean, return error message and skip annotation upload
            if annotation_data["operation_unique_id"] is None or not isinstance(annotation_data["is_normalized"], bool) or not isinstance(annotation_data["is_model_run"], bool):
                print("Invalid annotation data. Failed to upload annotations. Please provide valid annotation data according to the documentation")
                return upload_details
            self.wait_for_job_complete(job_id)
            self.upload_annotations_by_job_id(
                job_id,
                annotation_data["operation_unique_id"],
                annotation_data["json_data_file_path"],
                annotation_data["is_normalized"],
                annotation_data["is_model_run"]
            )
            print("Annotations uploaded successfully")

        return upload_details
    
    """
    This method is used to create a collection head with given name and content type
    """
    def create_or_update_collection(
            self,
            collection_name: str,
            content_type: str,
            custom_meta_object={},
    ):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        if collection_name == "":
            print(f'Invalid collection name "{collection_name}"')
            return {
                "is_success": False,
                "collection_id": None
            }
        if content_type.lower() == "image":
            collection_type = MediaType.IMAGE.value
        elif content_type.lower() == "video":
            collection_type = MediaType.VIDEO.value
        elif content_type.lower() == "other":
            collection_type = MediaType.OTHER.value
        else:
            print(f'Invalid content type "{content_type}"')
            return {
                "is_success": False,
                "collection_id": None
            }
        
        return _datalake_client.create_collection_head(
            collection_name,
            collection_type,
            custom_meta_object
        )

    """
    get item details
    @param unique_name: unique file name
    @param fields_filter: filter to get required meta data
    """

    def get_file_details(
            self,
            unique_name: str,
            fields_filter: dict = None
    ):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        return _datalake_client.get_item_details(unique_name, fields_filter)

    """
    get collection details
    @param collection_id: id of the collection
    @param fields_filter: filter to get required meta data
    """

    def get_collection_details(
            self,
            collection_id: str,
            fields_filter: dict = None
    ):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        return _datalake_client.get_collection_details(collection_id, fields_filter)
    
    """
    get collection id by name
    @param collection_name: name of the collection
    @param content_type: 'image', 'video' or 'other'
    """
    def get_collection_id_by_name(
            self,
            collection_name: str,
            content_type: str = "image"
    ):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        
        if content_type.lower() == "image":
            collection_type = MediaType.IMAGE.value
        elif content_type.lower() == "video":
            collection_type = MediaType.VIDEO.value
        elif content_type.lower() == "other":
            collection_type = MediaType.OTHER.value
        else:
            raise Exception("Invalid content type")

        return _datalake_client.get_collection_id_by_name(collection_name, collection_type)


    """"
    trash common logic for sdk
    @param collection_id: collection id
    @param query: query to filter the objects
    @param filter: filter to filter the objects
    @param object_type: 'image' or 'video'
    @param object_list: list of object ids
    @param is_all_selected: boolean
    """

    def __trash_objects(
            self,
            collection_id: str,
            query: str,
            filter,
            object_type: int,
            object_list,
            is_all_selected=True
    ):

        filter = self.__create_filter(filter)

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        response = _datalake_client.get_selection_id(
            collection_id, query, filter, object_type, object_list, is_all_selected)

        print('selection id: ', response)
        get_selection_id_success = True
        if ("isSuccess" in response):
            if (response["isSuccess"] == False):
                get_selection_id_success = False
        if (get_selection_id_success):
            selection_id = response['selectionTag']
            return _datalake_client.trash_datalake_object(selection_id)
        else:
            print('trash_response: ', {
                "isSuccess": False
            })
            return {
                "isSuccess": False,
                "message": response["warningMsg"]
            }

    """"
    Images/video trash from datalake
    @param datalake_query: query to select objects
    @param datalake_filter: filter to select objects
    @param content_type: 'image' or 'video'
    """

    def trash_objects_from_datalake(
            self,
            datalake_query: str,
            datalake_filter={},
            content_type: str = "image",
    ):
        # print(f'create project using query, filter and collections - project name: {project_name}, ')

        # Prevent all objects case
        if datalake_query == "" and (datalake_filter == "" or datalake_filter == {}):
            print('At least either valid filter or query should be given')
            return {
                "is_success": False,
                "error": "Not enough selection parameters"
            }

        if content_type == "image":
            object_type = ObjectType.IMAGE.value
        elif content_type == "video":
            object_type = ObjectType.VIDEO.value
        else:
            print('No valid content type')
            return {
                "is_success": False,
                "error": "Should specify either image or video as content type"
            }
        try:

            response = self.__trash_objects(
                "", datalake_query, datalake_filter, object_type, [])
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """"
    Images/video trash from collection
    @param collection id: collection id
    @param query: query to select objects
    @param filter: filter to select objects
    """

    def trash_objects_from_collection(
            self,
            collection_id: str,
            query: str = "",
            filter={},
    ):

        if (filter == None):
            filter = {}

        if (collection_id == None or collection_id == ''):
            print('collection id must be provided')
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }
        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }

        try:
            # if query and filter are empty, collection will be trashed
            if (query == "" or query == None) and (filter == "" or filter == {}):
                response = self.__trash_objects(
                    "", query, filter, object_type, [collection_id], False)
            else:
                response = self.__trash_objects(
                    collection_id, query, filter, 0, [], True)

            print('trash_response: ', response.get("message"))
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "isSuccess": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    Deprecated
    Download collection annotations from datalake
    @param collection_id - id of collection
    @param operation_id - Optional: id of the model (same operation_id given in upload annotations) - default: None
    @param custom_download_path - Optional: custom download path for save downloaded files - default: None
    """

    def download_annotations(
            self,
            collection_id: str,
            operation_id,
            custom_download_path: str = None,
            is_media_include=True
    ):

        print(
            'This method is now deprecated and please switch to "download_collection" function as this will be removed in future')
        # init dataset client
        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url, custom_download_path)

        operation_id_list = []
        annotation_type = "all"
        if operation_id != None:
            operation_id_list.append(operation_id)
        else:
            annotation_type = "human"

        # start download
        _dataset_client.download_annotations(
            collection_id, annotation_type, operation_id_list, is_media_include)

    """
    Download collection annotations from datalake
    @param collection_id - id of collection
    @param annotation_type - Optional: annotation category, can be given ("machine", "human" or "all") - default: "all"
    @param operation_id_list - Optional: id list of the model or ground truth (same operation_id_list given in upload annotations) - default: []
    @param custom_download_path - Optional: custom download path for save downloaded files - default: None
    """

    def download_collection(
            self,
            collection_id: str,
            annotation_type="all",
            operation_id_list=[],
            custom_download_path: str = None,
            is_media_include=True
    ):
        # init dataset client
        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url, custom_download_path)

        # start download
        _dataset_client.download_annotations(
            collection_id, annotation_type, operation_id_list, is_media_include)

    """
    Use to upload annotations for a collection, when file upload to collection.
    @param collection_name: name of the collection
    @param file_path: file path of the folder which contains the files
    @param meta_data_object: meta data object
    @param json_data_file_path: json file path which contains the annotations
    @param is_normalized: boolean
    @param is_model_run: boolean
    """
    def upload_data(
            self, 
            collection_name: str, 
            file_path: str, 
            meta_data_object: dict, 
            operation_unique_id: str, 
            json_data_file_path: str,
            is_normalized: bool, 
            is_model_run: bool,
    ):

        upload_details = None
        if (file_path == None):
            print('File upload cannot be done')
        else:
            upload_details = self.file_upload(
                file_path, MediaType.IMAGE.value, collection_name, meta_data_object)
            
            if upload_details["is_success"] == False:
                print('Failed to upload files. File upload failed')
                raise Exception("Failed to upload files. File upload failed")

        if (json_data_file_path == None):
            print('Failed to upload annotations. Json file path is required')
        else:
            job_id = upload_details["job_id"]
            res = self.wait_for_job_complete(job_id)

            if res["is_success"] == False:
                print('Failed to upload annotations. File upload failed')
                raise Exception("Failed to upload annotations. File upload failed")

            self.upload_annotations_by_job_id(
                job_id, operation_unique_id, json_data_file_path, is_normalized, is_model_run)

        return upload_details

    """"
    get upload progress
    """

    def get_upload_status(self, collection_name):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.get_upload_status(collection_name)

    """
    remove annotations of collection model run
    """

    def remove_annotations(self, collection_id: str, model_run_id: str):
        print(
            f'remove annotations of collection: {collection_id}, operation id: {model_run_id}')

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        _datalake_client.remove_collection_annotations(
            collection_id, model_run_id)

    def get_valid_sort_fields(self) -> list:
        value_list: list = []
        for field in SortFieldName:
            value_list.append(field.value)
        return value_list

    ''''
    Create sort filter
    @sort_obj: {field:"date_modified"/"date_created"/"name"/"size"/"video_index", order: "ASC/DESC"}
    @return: modified sort object(which will compatible withe node side request)
    '''

    def __create_sort_filter(self, sort_obj: dict) -> dict:
        modified_sort: dict = {}
        valid_sort_order: list = [SortOrder.ASC.value, SortOrder.DESC.value]

        if "sort_order" in sort_obj:
            sort_order = sort_obj["sort_order"]
            if sort_order not in valid_sort_order:
                raise Exception(f"Invalid sort order. Provide ${valid_sort_order}")
            else:
                modified_sort["sortOrder"] = sort_order

        if "sort_by_field" in sort_obj:
            field = sort_obj["sort_by_field"]
            if field == SortFieldName.DATE_CREATED.value:
                modified_sort["sortByField"] = SortField.DATE_CREATED.value
            elif field == SortFieldName.DATE_MODIFIED.value:
                modified_sort["sortByField"] = SortField.DATE_MODIFIED.value
            elif field == SortFieldName.NAME.value:
                modified_sort["sortByField"] = SortField.NAME.value
            elif field == SortFieldName.SIZE.value:
                modified_sort["sortByField"] = SortField.SIZE.value
            elif field == SortFieldName.VIDEO_INDEX.value:
                modified_sort["sortByField"] = SortField.VIDEO_INDEX.value
            else:
                valid_fields: list = self.get_valid_sort_fields()
                raise Exception(f"Invalid sort field name.should provide ${valid_fields}")

        return modified_sort

    """
    use to create appropriate filter object from user filter input
    """

    def __create_filter(self, filter):
        # { "annotation_types": ["human", "raw", "machine"], "from_date": "", "to_date": "" }
        return_filter = {
            "annotationTypes": [],
            "date": {},
            "tags": [],
            "labels": [],
            "metadata": {}
        }
        if "annotation_types" in filter:
            if "human" in filter["annotation_types"]:
                return_filter["annotationTypes"].append(2)
            if "raw" in filter["annotation_types"]:
                return_filter["annotationTypes"].append(0)
            if "machine" in filter["annotation_types"]:
                return_filter["annotationTypes"].append(1)
        if "to_date" in filter:
            return_filter["date"]["toDate"] = filter["to_date"]
        if "from_date" in filter:
            return_filter["date"]["fromDate"] = filter["from_date"]
        return return_filter

    """
    create annotation studio project using query, filter and collections
    """

    def __create_studio_project(
            self,
            project_name: str,
            collection_id: str,
            query: str,
            filter,
            object_type: int,
            object_list,
            fps,
            frames_per_task,
            assign_to_all,
            send_email,
            content_type,
            default_shape_type,
    ):
        # print(f'create project using query, filter and collections - project name: {project_name}, ')
        filter = self.__create_filter(filter)

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)

        response = _datalake_client.get_selection_id(
            collection_id, query, filter, object_type, object_list)
        print('selection id: ', response)
        get_selection_id_success = True
        if ("isSuccess" in response):
            if (response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            project_response = _studio_client.create_project(
                project_name,
                response['selectionTag'],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                default_shape_type,
                content_type)
            return project_response
        else:
            print('project_response: ', {
                "isSuccess": False
            })
            return {
                "isSuccess": False
            }

    def __get_object_type_by_id(self, object_id: str):
        print(f'get object type by id: {object_id}')

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        response = _datalake_client.get_object_type_by_id(object_id)
        return response

    """
    create annotation studio project using query, filter and collections
    """

    def create_annotation_project_from_collection(
            self,
            project_name: str,
            collection_id: str,
            query: str = "",
            filter={},
            fps: int = 4,
            frames_per_task: int = 120,
            assign_to_all=False,
            send_email=False,
            default_shape_type="rectangle"
    ):
        # print(f'create project using query, filter and collections - project name: {project_name}, ')

        if (collection_id == None or collection_id == ''):
            print('collection id must be provided')
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }
        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }
        content_type = None
        if (object_type == ObjectType.VIDEO.value or object_type == ObjectType.VIDEO_COLLECTION.value):
            content_type = ObjectType.VIDEO.value
        elif (object_type == ObjectType.IMAGE.value or object_type == ObjectType.IMAGE_COLLECTION.value):
            content_type = ObjectType.IMAGE.value
        else:
            print('object type is not supported')
            return {
                "isSuccess": False,
                "error": 'object type is not supported'
            }

        # if((fps == None) and (object_type == ObjectType.VIDEO.value or object_type == ObjectType.VIDEO_COLLECTION.value)):
        #    print('fps must be provided')
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__create_studio_project(
                project_name,
                collection_id,
                query,
                filter,
                0,
                [],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                content_type,
                default_shape_type)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "isSuccess": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    create annotation studio project using query, filter and collections
    """

    def create_annotation_project_from_datalake(
            self,
            project_name: str,
            datalake_query: str,
            datalake_filter={},
            content_type: str = "image",
            fps: int = 4,
            frames_per_task: int = 120,
            assign_to_all=False,
            send_email=False,
            default_shape_type="rectangle"
    ):
        # print(f'create project using query, filter and collections - project name: {project_name}, ')

        # Prevent all objects case
        if datalake_query == "" and (datalake_filter == "" or datalake_filter == {}):
            print('At least either valid filter or query should be given')
            return {
                "is_success": False,
                "error": "Not enough selection parameters"
            }

        # if(object_type == ObjectType.VIDEO or object_type == ObjectType.VIDEO_COLLECTION):
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }
        if content_type == "image":
            object_type = ObjectType.IMAGE.value
        elif content_type == "video":
            object_type = ObjectType.VIDEO.value
        else:
            print('No valid content type')
            return {
                "is_success": False,
                "error": "Should specify either image or video as content type"
            }
        try:
            response = self.__create_studio_project(
                project_name,
                "",
                datalake_query,
                datalake_filter,
                object_type,
                [],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                object_type,
                default_shape_type)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    update annotation project using query, filter and collections
    """

    def __update_objects_to_studio_project(
            self,
            project_id: str,
            collection_id: str,
            query: str,
            filter,
            object_type: int,
            object_list,
            fps,
            frames_per_task,
            assign_to_all,
            send_email,
            content_type,
            default_shape_type="rectangle",
    ):
        # print(f'create project using query, filter and collections - project id: {project_id}, ')
        filter = self.__create_filter(filter)

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)

        response = _datalake_client.get_selection_id(
            collection_id, query, filter, object_type, object_list)
        print('selection id: ', response)
        get_selection_id_success = True
        if ("isSuccess" in response):
            if (response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            project_response = _studio_client.update_project(
                project_id,
                response['selectionTag'],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                default_shape_type,
                content_type
            )
            print('project_response: ', project_response)
            return project_response
        else:
            print('project_response: ', {
                "is_success": False
            })
            return {
                "is_success": False
            }

    """
    update annotation studio project using query, filter and collections
    """

    def add_files_to_annotation_project_from_collection(
            self,
            project_id: str,
            collection_id: str,
            query: str,
            filter,
            fps: int = 0,
            frames_per_task: int = 120,
            assign_to_all=False,
            send_email=False,
            default_shape_type="rectangle"
    ):
        # print(f'create project using query, filter and collections - project name: {project_id}, ')

        if collection_id == None or collection_id == '':
            return {
                "is_success": False,
                "error": 'collection id must be provided'
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "is_success": False,
                "error": 'object type cannot find for collection id'
            }
        content_type = None
        if object_type == ObjectType.IMAGE_COLLECTION.value or object_type == ObjectType.IMAGE.value:
            content_type = ObjectType.IMAGE.value
        elif object_type == ObjectType.VIDEO_COLLECTION.value or object_type == ObjectType.VIDEO.value:
            content_type = ObjectType.VIDEO.value
        else:
            print('No valid content type')
            return {
                "is_success": False,
                "error": "Should specify either image or video as content type"
            }
        # if(fps == None and (object_type == ObjectType.VIDEO.value or object_type == ObjectType.VIDEO_COLLECTION.value)):
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__update_objects_to_studio_project(
                project_id,
                collection_id,
                query,
                filter,
                0,
                [],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                content_type,
                default_shape_type)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    update annotation studio project using query, filter and collections
    """

    def add_files_to_annotation_project_from_datalake(
            self,
            project_id: str,
            query: str,
            filter,
            content_type: str,
            fps: int = 0,
            frames_per_task: int = 120,
            assign_to_all=False,
            send_email=False,
            default_shape_type="rectangle"
    ):
        # print(f'create project using query, filter and collections - project name: {project_id}, ')

        if query == "" and (filter == "" or filter == {}):
            print('At least either valid filter or query should be given')
            return {
                "is_success": False,
                "error": "Not enough selection parameters"
            }

        if content_type == "image":
            object_type = ObjectType.IMAGE.value
        elif content_type == "video":
            object_type = ObjectType.VIDEO.value
        else:
            print('No valid content type')
            return {
                "is_success": False,
                "error": "Should specify either image or video as content type"
            }
        try:
            response = self.__update_objects_to_studio_project(
                project_id,
                "",
                query,
                filter,
                object_type,
                [],
                fps,
                frames_per_task,
                assign_to_all,
                send_email,
                object_type,
                default_shape_type)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    delete a annotation studio project by project id
    """

    def delete_annotation_project(self, project_id: str):
        if (project_id == None or project_id == ""):
            print("Project id not valid")
            return {
                "is_success": False,
                "error": f'Project id not available'
            }
        print(f'delete project - project id: {project_id}')
        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)
        try:
            response = _studio_client.delete_project(project_id)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    update the labels of studio project
    """

    def __update_labels_to_studio_project(self, project_id: str, add_list, remove_list):
        # print(f'add labels to project - project id: {project_id}, add label list: {add_list}, remove label list: {remove_list}')

        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)

        response = _studio_client.update_labels_to_project(
            project_id, add_list, remove_list)

        return response

    """
    add the labels of studio project
    """

    def add_labels_to_studio_project(self, project_id: str, add_list):
        print(
            f'add labels to project - project id: {project_id}, label list: {add_list}')
        try:
            response = self.__update_labels_to_studio_project(
                project_id, add_list, [])
            print('response: ', response)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    remove the labels of studio project
    """

    def remove_labels_to_studio_project(self, project_id: str, remove_list):
        print(
            f'remove labels to project - project id: {project_id}, label list: {remove_list}')

        try:
            response = self.__update_labels_to_studio_project(
                project_id, [], remove_list)
            print('response: ', response)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    Get list of studio project
    """

    def get_annotation_project_list(self):
        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)
        return _studio_client.studio_project_list()

    """
    create dataset from search objects
    create dataset from search objects
    @param dataset_name - name of the dataset
    @param collection_id - collection_id for search objects
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @param object_type - object_type for search objects
    @param object_list - object_list for search objects
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def __create_dataset(
            self,
            dataset_name: str,
            collection_id: str,
            query: str,
            filter,
            object_type,
            object_list,
            split_nfo,
            labels,
            export_types,
            operation_list,
            augmentation_list):
        print(f'create dataset - dataset name: {dataset_name}')

        if dataset_name == "" or dataset_name == None:
            print(f'Invalid dataset name "{dataset_name}"')
            return {
                "is_success": False,
                "error": "Invalid dataset name"
            }
        if object_type.lower() == "image":
            object_type = ObjectType.IMAGE.value
        elif object_type.lower() == "image_collection":
            object_type = ObjectType.IMAGE_COLLECTION.value
        elif object_type.lower() == "dataset":
            object_type = ObjectType.DATASET.value
        else:
            print("Invalid content type - should be either 'image'")
            return {
                "is_success": False,
                "collection_id": None
            }

        filter = self.__create_filter(filter)

        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url)

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        response = _datalake_client.get_selection_id(
            collection_id, query, filter, object_type, object_list)
        print('selection id: ', response)
        get_selection_id_success = True
        if ("isSuccess" in response):
            if (response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            dataset_response = _dataset_client.create_dataset(
                dataset_name,
                response['selectionTag'],
                split_nfo,
                labels,
                export_types,
                operation_list,
                augmentation_list)
            print('dataset_response: ', dataset_response)
            return dataset_response
        else:
            print('dataset_response: ', {
                "isSuccess": False
            })
            return {
                "isSuccess": False
            }

    """
    create dataset from search objects on collection
    @param dataset_name - name of the dataset
    @param collection_id - collection_id for search objects
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def create_dataset_from_collection(
            self,
            dataset_name: str,
            collection_id: str,
            split_info,
            labels=[],
            export_types=[],
            query: str = "",
            filter={},
            operation_list=None,
            augmentation_list=None):

        if (collection_id == None):
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }
        if object_type == ObjectType.IMAGE_COLLECTION.value:
            object_type = "image"
        else:
            return {
                "isSuccess": False,
                "error": 'collection type is not acceptable for create dataset, only image collections are valid'
            }

        return self.__create_dataset(
            dataset_name,
            collection_id,
            query,
            filter,
            object_type,
            [],
            split_info,
            labels,
            export_types,
            operation_list,
            augmentation_list)

    """
    create dataset from search objects on datalake
    @param dataset_name - name of the dataset
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @param content_type - content_type for search objects
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def create_dataset_from_datalake(
            self,
            dataset_name: str,
            split_info,
            labels=[],
            export_types=[],
            item_type="image",
            query: str = "",
            filter={},
            operation_list=None,
            augmentation_list=None):

        return self.__create_dataset(
            dataset_name,
            None,
            query,
            filter,
            item_type,
            [],
            split_info,
            labels,
            export_types,
            operation_list,
            augmentation_list)

    """
    update dataset from search objects
    @param version_id - id of the base version
    @param collection_id - collection_id for search objects
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @param object_type - object_type for search objects
    @param object_list - object_list for search objects
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @param is_new_version_required - whether creating new version (True) or update existing version (False)
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def __update_dataset_version(
            self,
            version_id: str,
            collection_id: str,
            query: str,
            filter,
            object_type,
            object_list,
            split_info,
            labels,
            export_types,
            is_new_version_required,
            operation_list,
            augmentation_list):
        print(f'create dataset - dataset version id: {version_id}')

        if object_type.lower() == "image":
            object_type = ObjectType.IMAGE.value
        elif object_type.lower() == "image_collection":
            object_type = ObjectType.IMAGE_COLLECTION.value
        elif object_type.lower() == "dataset":
            object_type = ObjectType.DATASET.value
        else:
            print("Invalid content type - should be either 'image'")
            return {
                "is_success": False
            }

        filter = self.__create_filter(filter)

        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url)

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        response = _datalake_client.get_selection_id(
            collection_id, query, filter, object_type, object_list)
        print('selection id: ', response)
        get_selection_id_success = True
        if ("isSuccess" in response):
            if (response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            dataset_response = _dataset_client.update_dataset_version(
                version_id,
                response['selectionTag'],
                split_info,
                labels,
                export_types,
                is_new_version_required,
                operation_list,
                augmentation_list)
            print('dataset_response: ', dataset_response)
            return dataset_response
        else:
            print('dataset_response: ', {
                "isSuccess": False
            })
            return {
                "isSuccess": False
            }

    """
    update dataset from search objects on collection
    @param version_id - id of the base version
    @param collection_id - collection_id for search objects
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @param is_new_version_required - whether creating new version (True) or update existing version (False)
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def update_dataset_version_from_collection(
            self,
            version_id: str,
            collection_id: str,
            split_info,
            labels=[],
            export_types=[],
            query: str = "",
            filter={},
            is_new_version_required=False,
            operation_list=None,
            augmentation_list=None):

        if (collection_id == None or collection_id == ""):
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }
        if (version_id == None or version_id == ""):
            return {
                "isSuccess": False,
                "error": 'version id must be provided'
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }
        if object_type == ObjectType.IMAGE_COLLECTION.value:
            object_type = "image"
        else:
            return {
                "isSuccess": False,
                "error": 'collection type is not acceptable for create dataset, only image collections are valid'
            }

        return self.__update_dataset_version(
            version_id,
            collection_id,
            query,
            filter,
            object_type,
            [],
            split_info,
            labels,
            export_types,
            is_new_version_required,
            operation_list,
            augmentation_list)

    """
    update dataset from search objects on datalake
    @param version_id - id of the base version
    @param split_info - dataset split information - {
            "train": number,
            "test": number,
            "validation": number
        }
    @param labels - dataset selected labels
    @param export_types - dataset selected export types
    @param item_type - content_type for search objects
    @param query - query for search objects
    @param filter - filter for filter objects - {
        "annotation_types": ["human", "raw", "machine"],
        "from_date": "", "to_date": ""
    }
    @param is_new_version_required - whether creating new version (True) or update existing version (False)
    @operation_list - operation id list
    @augmentation_list - augmentation list
    """

    def update_dataset_version_from_datalake(
            self,
            version_id: str,
            split_info,
            labels=[],
            export_types=[],
            item_type: str = "image",
            query: str = "",
            filter={},
            is_new_version_required=False,
            operation_list=None,
            augmentation_list=None):

        if (version_id == None or version_id == ""):
            return {
                "isSuccess": False,
                "error": 'version id must be provided'
            }
        return self.__update_dataset_version(
            version_id,
            None,
            query,
            filter,
            item_type,
            [],
            split_info,
            labels,
            export_types,
            is_new_version_required,
            operation_list,
            augmentation_list)

    """
    delete dataset version
    @param version_id - id of the deleting version
    """

    def delete_dataset_version(self, version_id: str):
        print(f'delete dataset version - dataset version id: {version_id}')

        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url)
        response = _dataset_client.delete_dataset_version(version_id)
        print(response)
        return response

    """
    Get list of all system labels
    """

    def get_all_labels(self):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.get_system_labels()

    """
    Get list of system labels that attached to given group
    """

    def get_labels_in_group(self, group_id):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.get_system_labels(group_id)

    """
    Create system label
    """

    def create_system_label(self, label):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.create_system_label(label)

    """
    Create a group from labels (label keys)
    """

    def create_label_group(self, group_name, label_ids):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.create_label_group(group_name, label_ids)

    """
    Attach labels to a group
    """

    def attach_labels_to_group(self, group_id, label_ids):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.attach_labels_to_group(group_id, label_ids)

    """
    Detach labels from group
    """

    def detach_labels_from_group(self, group_id, label_ids):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.detach_labels_from_group(group_id, label_ids)

    """
    List All label groups
    """

    def get_all_label_groups(self):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.get_all_label_groups()

    """
    Attach label group to annotation project
    """

    def attach_label_group_to_annotation_project(self, project_id, group_id):
        _studio_client = studio.StudioClient(
            self.encoded_key_secret, self.layernext_url)
        return _studio_client.project_set_label_group(project_id, group_id)

    """
    Deprecated
    Download project annotations
    @param project_id - id of annotation project
    @param task_status_list - (Optional): To filter by task status - default: []
    @param is_annotated_only - (Optional): If True, then only the annotated images are downloaded - default: False
    @param custom_download_path - (Optional): To download data to required location instead of current directory - default: None
    """

    def download_project_annotations(
            self,
            project_id,
            task_status_list: list = [],
            is_annotated_only: bool = False,
            custom_download_path: str = None,
            is_media_include=True):

        print(
            'This method is now deprecated and please switch to "download_annotation_projects" function as this will be removed in future')
        # init dataset client
        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url, custom_download_path)

        project_id_list = []
        project_id_list.append(project_id)
        # start download
        _dataset_client.download_annotations_for_project_v2(
            project_id_list, task_status_list, is_annotated_only, is_media_include)

    """
    Download multiple project annotations
    @param project_id_list - id list of annotation projects
    @param task_status_list - (Optional): To filter by task status - default: []
    @param is_annotated_only - (Optional): If True, then only the annotated images are downloaded - default: False
    @param custom_download_path - (Optional): To download data to required location instead of current directory - default: None
    """

    def download_annotation_projects(
            self,
            project_id_list,
            task_status_list: list = [],
            is_annotated_only: bool = False,
            custom_download_path: str = None,
            is_media_include=True):

        if task_status_list == None:
            task_status_list = []

        # init dataset client
        _dataset_client = dataset.DatasetClient(
            self.encoded_key_secret, self.layernext_url, custom_download_path)

        # start download
        _dataset_client.download_annotations_for_project_v2(
            project_id_list, task_status_list, is_annotated_only, is_media_include)

    """
    Wait until job complete
    @param job_id - id of the relevant job
    """

    def wait_for_job_complete(self, job_id: str):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.wait_for_job_complete(job_id)

    """
    Get downloadable url of a file in Data Lake
    @param file_key - File path in Data Lake
    """

    def get_downloadable_url(self, file_key: str):
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        return _datalake_client.get_file_download_url(file_key)

    """
    Upload metadata data from a json file
    """

    def upload_metadata_for_files(
            self,
            collection_name: str,
            content_type: str,
            json_data_file_path: str,
    ):
        # init datalake client
        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        
        if collection_name is not None and collection_name != "":
            collection_id = self.get_collection_id_by_name(collection_name, content_type)
        else:
            raise Exception("Collection name cannot be empty")

        _datalake_client.upload_metadata_from_json(
            collection_id,
            json_data_file_path
        )

    """
    Upload metadata from a json file with unique names
    @param: json_data_file_path - path of the json file in format - [{file:str, metadata:{Field:str, Tags:[str]}}]
    @item_type: "image", "video", "other"
    @query: datalake query
    """
    def upload_metadata_by_unique_name(
            self,
            json_data_file_path: str,
    ):
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layernext_url)

        _datalake_client.upload_metadata_from_unique_name_json(json_data_file_path)

    """
    Upload metadata from a json file with storage path
    @param: json_data_file_path - path of the json file in format - [{file:str, metadata:{Field:str, Tags:[str]}}]
    @bucket_name: bucket name, if not given, default bucket will be used
    """
    def upload_metadata_by_storage_path(
            self,
            json_data_file_path: str,
            bucket_name: str = None
    ):
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layernext_url)

        _datalake_client.upload_metadata_from_storage_path_json(json_data_file_path, bucket_name)

    """
    Upload metadata from a json file with job id
    @param: json_data_file_path - path of the json file in format - [{file:str, metadata:{Field:str, Tags:[str]}}]
    @job_id: job id, it is required
    """
    def upload_metadata_by_job_id(
            self,
            job_id: str,
            json_data_file_path: str,
    ):
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layernext_url)

        _datalake_client.upload_metadata_from_job_id(job_id, json_data_file_path)

    """
    Upload metadata data from a metadata object
    """

    def upload_metadata_for_collection(
            self,
            collection_name: str,
            content_type: str,
            metadata_obj: dict,
            is_apply_to_all_files=True):

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        if content_type.lower() == "image":
            collection_type = MediaType.IMAGE.value
        elif content_type.lower() == "video":
            collection_type = MediaType.VIDEO.value
        elif content_type.lower() == "other":
            collection_type = MediaType.OTHER.value
        else:
            raise Exception("Invalid content type")

        _datalake_client.upload_metadata_from_metaObject(
            collection_name,
            collection_type,
            metadata_obj,
            is_apply_to_all_files
        )

    """
    get item list from data lake
    @item_type: "image", "video", "other", "image_collection", "video_collection", "other_collection", "dataset"
    @query: datalake query
    @filter: {date: {fromDate: "", toDate: ""}, "annotation_types": ["human", "raw", "machine"]}
    @page_index - index of the page
    @page_size - size of the page, maximum = 1000
    @sort_order: {sort_by_field:"date_modified"/"date_created"/"name"/"size"/"video_index", sort_order: "ASC/DESC"}
    """

    def get_item_list_from_datalake(
            self,
            item_type,
            query: str = "",
            filter={},
            page_index=0,
            page_size=20,
            sort_order: dict = {},
    ):

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        item_type_enum = 2
        if item_type == "image":
            item_type_enum = ObjectType.IMAGE.value
        elif item_type == "video":
            item_type_enum = ObjectType.VIDEO.value
        elif item_type == "other":
            item_type_enum = ObjectType.OTHER.value
        elif item_type == "image_collection":
            item_type_enum = ObjectType.IMAGE_COLLECTION.value
        elif item_type == "video_collection":
            item_type_enum = ObjectType.VIDEO_COLLECTION.value
        elif item_type == "other_collection":
            item_type_enum = ObjectType.OTHER_COLLECTION.value
        elif item_type == "dataset":
            item_type_enum = ObjectType.DATASET.value

        filter = self.__create_filter(filter)
        sort_filter = self.__create_sort_filter(sort_order)
        return _datalake_client.get_item_list_from_datalake(
            item_type_enum,
            query,
            filter,
            page_index,
            page_size,
            sort_filter
        )

    """
    download files from collection(videos, images, others)
    @param collection_id: collection id
    @param folder_name: folders where files will be downloaded
    @param page_index: index of the page
    @param page_size: size of the page, maximum = 1000
    @param query: datalake query
    @param metalake_filter: {date: {fromDate: "", toDate: ""}, "annotation_types": ["human", "raw", "machine"]}
    @sort_order: {sort_by_field:"date_modified"/"date_created"/"name"/"size"/"video_index", sort_order: "ASC/DESC"}
    @return: {isSuccess: True/False, message: ""}
    """

    def download_files_from_collection(self,
                                       collection_id: str,
                                       folder_name: str,
                                       page_index: int = 0,
                                       page_size: int = 20,
                                       query: str = "",
                                       metalake_filter: dict = {},
                                       sort_order: dict = {}
                                       ) -> dict:

        assert isinstance(collection_id, str), "collection_id must be a string"
        assert isinstance(folder_name, str), "folder_name must be a string"
        assert isinstance(query, str), "query must be a string"
        assert isinstance(metalake_filter, dict), "data_filter must be a dictionary"
        assert isinstance(page_index, int), "page_index must be an integer"
        assert isinstance(page_size, int), "page_size must be an integer"

        if collection_id == "":
            return {
                "is_success": False,
                "message": "collection_id should not empty"
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "is_success": False,
                "message": 'object type cannot find for collection id'
            }
        item_type_enum = 2
        if object_type == ObjectType.IMAGE_COLLECTION.value:
            item_type_enum = ObjectType.IMAGE.value
        elif object_type == ObjectType.VIDEO_COLLECTION.value:
            item_type_enum = ObjectType.VIDEO.value
        elif object_type == ObjectType.OTHER_COLLECTION.value:
            item_type_enum = ObjectType.OTHER.value
        else:
            return {
                "is_success": False,
                "message": 'collection type is not acceptable get item list'
            }

        metalake_filter = self.__create_filter(metalake_filter)
        # metalake_filter["contentType"] = item_type_enum
        sort_filter = self.__create_sort_filter(sort_order)

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layernext_url)
        return _datalake_client.download_files_batch_wise(item_type_enum, query, metalake_filter, page_index, page_size,
                                                          folder_name,
                                                          {"collection_id": collection_id}, sort_filter)

    """
        Download files from metalake
       @param item_type: supported types are "image", "video", "other"
       @param folder_name: folders where files will be downloaded
       @param page_index: index of the page
       @param page_size: size of the page, maximum = 1000
       @param query: datalake query
       @param metalake_filter: {date: {fromDate: "", toDate: ""}, "annotation_types": ["human", "raw", "machine"]}
       @sort_order: {sort_by_field:"date_modified"/"date_created"/"name"/"size"/"video_index", sort_order: "ASC/DESC"}
       @return: {isSuccess: True/False, message: ""}
       """

    def download_files_from_metalake(self,
                                     item_type: str,
                                     folder_name: str,
                                     page_index: int = 0,
                                     page_size: int = 20,
                                     query: str = "",
                                     metalake_filter: dict = {},
                                     sort_order: dict = {}
                                     ) -> dict:

        assert isinstance(item_type, str), "item_type must be a string"
        assert isinstance(folder_name, str), "folder_name must be a string"
        assert isinstance(query, str), "query must be a string"
        assert isinstance(metalake_filter, dict), "data_filter must be a dictionary"
        assert isinstance(page_index, int), "page_index must be an integer"
        assert isinstance(page_size, int), "page_size must be an integer"

        allowed_types = [ItemType.IMAGE.value, ItemType.VIDEO.value, ItemType.OTHER.value]

        if item_type not in allowed_types:
            raise Exception("Invalid item type, available types are: " + str(allowed_types))

        item_type_enum = 0
        if item_type == ItemType.IMAGE.value:
            item_type_enum = ObjectType.IMAGE.value
        elif item_type == ItemType.VIDEO.value:
            item_type_enum = ObjectType.VIDEO.value
        elif item_type == ItemType.OTHER.value:
            item_type_enum = ObjectType.OTHER.value

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layernext_url)

        metalake_filter = self.__create_filter(metalake_filter)
        # metalake_filter["contentType"] = item_type_enum
        sort_filter = self.__create_sort_filter(sort_order)

        return _datalake_client.download_files_batch_wise(item_type_enum, query, metalake_filter, page_index, page_size,
                                                          folder_name,
                                                          {"item_type": item_type_enum}, sort_filter)

    """
    get item list from collection in datalake
    @collection_id: id of the collection
    @query: datalake query
    @filter: {date: {fromDate: "", toDate: ""},  "annotation_types": ["human", "raw", "machine"]}
    @page_index - index of the page
    @page_size - size of the page, maximum = 1000
    @sort_order: {sort_by_field:"date_modified"/"date_created"/"name"/"size"/"video_index", sort_order: "ASC/DESC"}
    """

    def get_item_list_from_collection(
            self,
            collection_id,
            query: str = "",
            filter={},
            page_index=0,
            page_size=20,
            sort_order: dict = {},
    ):

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)
        item_type_enum = 2
        if collection_id == None or collection_id == "":
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]

        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }
        if object_type == ObjectType.IMAGE_COLLECTION.value:
            item_type_enum = ObjectType.IMAGE.value
        elif object_type == ObjectType.VIDEO_COLLECTION.value:
            item_type_enum = ObjectType.VIDEO.value
        elif object_type == ObjectType.OTHER_COLLECTION.value:
            item_type_enum = ObjectType.OTHER.value
        else:
            return {
                "isSuccess": False,
                "error": 'collection type is not acceptable get item list'
            }

        filter = self.__create_filter(filter)
        # filter["contentType"] = item_type_enum
        sort_filter = self.__create_sort_filter(sort_order)

        return _datalake_client.get_item_list_from_collection(
            item_type_enum,
            collection_id,
            query,
            filter,
            page_index,
            page_size,
            sort_filter
        )


    """
    Use for insert embedding list to images
    @embedding_list - [
        {
            "uniqueName": "example_collection_example_image.jpg",
            "embeddings": [0.23,0.56,....]
        },
        {
            "uniqueName": "example_collection_example_image.jpg",
            "embeddings": [0.23,0.56,....]
        },.......
    ]
    uniqueName string length limit 256 characters
    embedding vector dimension limit 2048
    """
    def insert_image_embeddings_batch(self, embedding_list):
        if embedding_list == None:
            return {
                "success": False,
                "message": "embedding_list is None"
            }
        if type(embedding_list) != list:
            return {
                "success": False,
                "message": "embedding_list is not a list"
            }
        if len(embedding_list) > 100:
            return {
                "success": False,
                "message": "embedding_list length is more than 100"
            }

        def is_embedding_dict(embedding_obj):
            return (
                isinstance(embedding_obj, dict) and
                'embeddings' in embedding_obj and isinstance(embedding_obj['embeddings'], list) and
                'uniqueName' in embedding_obj and isinstance(embedding_obj['uniqueName'], str)
            )

        if not all(is_embedding_dict(d) for d in embedding_list):
            return {
                "success": False,
                "message": "embedding_list doesn't follow format"
            }

        _datalake_client = datalake.DatalakeClient(
            self.encoded_key_secret, self.layernext_url)

        return _datalake_client.insert_embeddings_batch(embedding_list)


    """
    Use for insert embedding list to images
    @embedding_list - [
        {
            "uniqueName": "example_collection_example_image.jpg",
            "embeddings": [0.23,0.56,....]
        },
        {
            "uniqueName": "example_collection_example_image.jpg",
            "embeddings": [0.23,0.56,....]
        },.......
    ]
    uniqueName string length limit 256 characters
    embedding vector dimension limit 2048
    """
    def insert_image_embeddings(self, embedding_list):
        if embedding_list == None:
            return {
                "success": False,
                "message": "embedding_list is None"
            }
        if type(embedding_list) != list:
            return {
                "success": False,
                "message": "embedding_list is not a list"
            }
        count = 0
        temp_embedding_list = []
        for embedding in embedding_list:
            if count == len(embedding_list)-1:
                temp_embedding_list.append(embedding)
                response = self.insert_image_embeddings_batch(temp_embedding_list)
                if response["success"] == False:
                    return response
                return {
                    "success": True
                }
            elif count % 100 == 0 and count != 0:
                response = self.insert_image_embeddings_batch(temp_embedding_list)
                if response["success"] == False:
                    return response
                temp_embedding_list = []
            else:
                temp_embedding_list.append(embedding)
            count += 1

        return {
                    "success": True
                }
