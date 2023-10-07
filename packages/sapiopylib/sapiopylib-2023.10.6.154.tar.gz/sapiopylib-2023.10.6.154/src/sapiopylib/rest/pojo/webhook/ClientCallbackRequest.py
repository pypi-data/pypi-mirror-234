import base64
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional

from sapiopylib.rest.pojo.datatype.FieldDefinition import AbstractVeloxFieldDefinition
from sapiopylib.rest.pojo.datatype.TemporaryDataType import TemporaryDataType
from sapiopylib.rest.pojo.webhook.WebhookEnums import CallbackType


class AbstractClientCallbackRequest(ABC):
    """
    A request for a client callback to be shown to the user that invoked the webhook.
    """
    callback_context_data: Optional[str]

    def __init__(self, callback_context_data: Optional[str] = None):
        self.callback_context_data = callback_context_data

    @abstractmethod
    def get_callback_type(self) -> CallbackType:
        """
        Get the callback data type for this client callback result.
        """
        pass

    def to_json(self) -> Dict[str, Any]:
        return {
            'callbackType': self.get_callback_type().name,
            'callbackContextData': self.callback_context_data
        }


class DataRecordSelectionRequest(AbstractClientCallbackRequest):
    """
    A callback request to select a list of field map rows.
    """
    data_type_display_name: str
    data_type_plural_display_name: str
    field_def_list: List[AbstractVeloxFieldDefinition]
    field_map_list: List[Dict[str, Any]]
    dialog_message: Optional[str]
    multi_select: bool

    def __init__(self, data_type_display_name: str, data_type_plural_display_name: str,
                 field_def_list: List[AbstractVeloxFieldDefinition],
                 field_map_list: List[Dict[str, Any]],
                 dialog_message: Optional[str] = None, multi_select: bool = False,
                 callback_context_data: Optional[str] = None):
        super().__init__(callback_context_data)
        self.data_type_display_name = data_type_display_name
        self.data_type_plural_display_name = data_type_plural_display_name
        self.field_def_list = field_def_list
        self.field_map_list = field_map_list
        self.dialog_message = dialog_message
        self.multi_select = multi_select

    def get_callback_type(self) -> CallbackType:
        return CallbackType.DATA_RECORD_SELECTION

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['dialogMessage'] = self.dialog_message
        ret['dataTypeDisplayName'] = self.data_type_display_name
        ret['dataTypePluralDisplayName'] = self.data_type_plural_display_name
        ret['fieldDefinitionList'] = [x.to_json() for x in self.field_def_list]
        ret['fieldMapList'] = self.field_map_list
        ret['multiSelect'] = self.multi_select
        return ret


class MultiFilePromptRequest(AbstractClientCallbackRequest):
    """
    Request the user to upload multiple files. User will be asked fo upload one or more files.
    """
    dialog_title: str
    show_image_editor: bool
    file_extension: Optional[str]
    show_camera_button: bool

    def __init__(self, dialog_title: str, show_image_editor: bool = False, file_extension: Optional[str] = None,
                 show_camera_button: bool = False, callback_context_data: Optional[str] = None):
        """
        Request the user to upload multiple files.
        :param dialog_title: The title of the file prompt
        :param show_image_editor: Whether the user will see an image editor when image is uploaded in this file prompt.
        :param show_camera_button: Whether the user will be able to use camera to take a picture as an upload request,
        rather than selecting an existing file.
        :param file_extension: The acceptable file extensions for the file prompt. Comma separated.
        """
        super().__init__(callback_context_data)
        self.dialog_title = dialog_title
        self.show_image_editor = show_image_editor
        self.file_extension = file_extension
        self.show_camera_button = show_camera_button

    def get_callback_type(self):
        return CallbackType.MULTI_FILE_PROMPT

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret.update({
            'dialogTitle': self.dialog_title,
            'fileExtension': self.file_extension,
            'showImageEditor': self.show_image_editor,
            'showCameraButton': self.show_camera_button
        })
        return ret


class FilePromptRequest(AbstractClientCallbackRequest):
    """
    Request for a single file prompt to be displayed to the user. User will be asked to upload a file.

    dialog_title: The title of the file prompt

    show_image_editor: Whether the user will see an image editor when image is uploaded in this file prompt.

    show_camera_button: Whether the user will be able to use camera to take a picture as an upload request, rather
    than selecting an existing file.

    file_extension: The acceptable file extensions for the file prompt. Comma separated.
    """
    dialog_title: str
    show_image_editor: bool
    file_extension: Optional[str]
    show_camera_button: bool

    def __init__(self, dialog_title: str, show_image_editor: bool = False, file_extension: Optional[str] = None,
                 show_camera_button: bool = False, callback_context_data: Optional[str] = None):
        """
        Request for a file prompt to be displayed to the user.

        :param dialog_title: The title of the file prompt
        :param show_image_editor: Whether the user will see an image editor when image is uploaded in this file prompt.
        :param show_camera_button: Whether the user will be able to use camera to take a picture as an upload request,
        rather than selecting an existing file.
        :param file_extension: The acceptable file extensions for the file prompt. Comma separated.
        """
        super().__init__(callback_context_data)
        self.dialog_title = dialog_title
        self.show_image_editor = show_image_editor
        self.file_extension = file_extension
        self.show_camera_button = show_camera_button

    def get_callback_type(self):
        return CallbackType.FILE_PROMPT

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret.update({
            'dialogTitle': self.dialog_title,
            'fileExtension': self.file_extension,
            'showImageEditor': self.show_image_editor,
            'showCameraButton': self.show_camera_button
        })
        return ret


class FormEntryDialogRequest(AbstractClientCallbackRequest):
    """
    Requests the current context's user to pop up a client callback asking user to enter info in a form.

    title: The title of the form entry dialog
    message: The message to show on top of the entry dialog.
    data_type_def: The type definition, including field definitions and layouts, for this form.
    """
    title: str
    message: str
    data_type_def: TemporaryDataType

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['title'] = self.title
        ret['message'] = self.message
        ret['temporaryDataTypePojo'] = self.data_type_def.to_json()
        return ret

    def __init__(self, title: str, message: str, data_type_def: TemporaryDataType,
                 callback_context_data: Optional[str] = None):
        """
        Requests the current context's user to pop up a client callback asking user to enter info in a form.

        :param title: The title of the form entry dialog
        :param message: The message to show on top of the entry dialog.
        :param data_type_def: The type definition, including field definitions and layouts, for this form.
        """
        super().__init__(callback_context_data)
        self.title = title
        self.message = message
        self.data_type_def = data_type_def

    def get_callback_type(self) -> CallbackType:
        return CallbackType.FORM_ENTRY_DIALOG


class ListDialogRequest(AbstractClientCallbackRequest):
    """
    Payload for request for the user to select an option in a list dialog displayed.

    title: title of the list dialog prompt
    multi_select: Whether we allow user to multi-select in this list dialog.
    option_list: The available options text for the user.
    """
    title: str
    multi_select: bool
    option_list: List[str]

    def get_callback_type(self) -> CallbackType:
        return CallbackType.LIST_DIALOG

    def __init__(self, title: str, multi_select: bool, option_list: List[str],
                 callback_context_data: Optional[str] = None):
        """
        Payload for request for the user to select an option in a list dialog displayed.

        :param title: title of the list dialog prompt
        :param multi_select: Whether we allow user to multi-select in this list dialog.
        :param option_list: The available options text for the user.
        """
        super().__init__(callback_context_data)
        self.title = title
        self.multi_select = multi_select
        self.option_list = option_list

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['title'] = self.title
        ret['multiSelect'] = self.multi_select
        ret['optionList'] = self.option_list
        return ret


class OptionDialogRequest(AbstractClientCallbackRequest):
    """
    Payload to request for the user to select a button option displayed in a dialog.

    title: The title of this dialog
    message: The message to show on top of the dialog body
    button_list: The buttons user can press, in order of user's theme button order style.
    default_selection: What user would select if the user has cancelled.
    closable: Whether the user can close (cancel) the dialog.
    """
    title: str
    message: str
    button_list: List[str]
    default_selection: int
    closable: bool

    def __init__(self, title: str, message: str, button_list: List[str], default_selection: int = 0,
                 closable: bool = False, callback_context_data: Optional[str] = None):
        """
        Payload to request for the user to select a button option displayed in a dialog.

        :param title: The title of this dialog
        :param message: The message to show on top of the dialog body
        :param button_list: The buttons user can press, in order of user's theme button order style.
        :param default_selection: What user would select if the user has cancelled.
        :param closable: Whether the user can close (cancel) the dialog.
        """
        super().__init__(callback_context_data)
        self.title = title
        self.message = message
        self.button_list = button_list
        self.default_selection = default_selection
        self.closable = closable

    def get_callback_type(self) -> CallbackType:
        return CallbackType.OPTION_DIALOG

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['title'] = self.title
        ret['message'] = self.message
        ret['buttonList'] = self.button_list
        ret['defaultSelection'] = self.default_selection
        ret['closable'] = self.closable
        return ret


class TableEntryDialogRequest(AbstractClientCallbackRequest):
    """
    Client callback request prompting user a table entry dialog.

    title: The title to show in the table entry dialog
    message: The message to show on top of the dialog body
    data_type_def: The field definition and layouts for this dialog.
    field_map_list: The default values in this table before user started to edit.
    Note: this must be filled with number of rows you want to edit
    (if user is presented with 5 rows, enter 5 dictionaries inside the list)
    """
    title: str
    message: str
    data_type_def: TemporaryDataType
    field_map_list: List[Dict[str, Any]]

    def __init__(self, title: str, message: str, data_type_def: TemporaryDataType,
                 field_map_list: List[Dict[str, Any]], callback_context_data: Optional[str] = None):
        """
        Client callback request prompting user a table entry dialog.

        :param title: The title to show in the table entry dialog
        :param message: The message to show on top of the dialog body
        :param data_type_def: The field definition and layouts for this dialog.
        :param field_map_list: The default values in this table before user started to edit.
        Note: this must be filled with number of rows you want to edit
        (if user is presented with 5 rows, enter 5 dictionaries inside the list)
        """
        super().__init__(callback_context_data)
        self.title = title
        self.message = message
        self.data_type_def = data_type_def
        self.field_map_list = field_map_list

    def get_callback_type(self) -> CallbackType:
        return CallbackType.TABLE_ENTRY_DIALOG

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['title'] = self.title
        ret['message'] = self.message
        ret['temporaryDataTypePojo'] = self.data_type_def.to_json()
        ret['fieldMapList'] = self.field_map_list
        return ret


class WriteFileRequest(AbstractClientCallbackRequest):
    """
    Write a short amount of file data onto the client. The user will download this file from browser.

    The return object from server is of type WriteFileResult, which you can use to check if user has cancelled.
    Note: file data will be stored in RAM in this operation.

    file_bytes: The file data to write.
    file_path: The filename of the written file.
    """
    file_bytes: bytes
    file_path: str

    def __init__(self, file_bytes: bytes, file_path: str, callback_context_data: Optional[str] = None):
        super().__init__(callback_context_data)
        self.file_bytes = file_bytes
        self.file_path = file_path

    def get_callback_type(self) -> CallbackType:
        return CallbackType.WRITE_FILE

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['filePath'] = self.file_path
        encoded_data: bytes = base64.b64encode(self.file_bytes)
        ret['fileBytes'] = encoded_data.decode("utf-8")
        return ret


class MultiFileRequest(AbstractClientCallbackRequest):
    """
    Write multiple files to the user browser all at once. To fill the request, you can use it like a dictionary.

    The return object from server is of type WriteFileResult, which you can use to check if user has cancelled.
    """

    json_built: Dict[str, str]

    def __init__(self, initial_data: Dict[str, bytes] = None, callback_context_data: Optional[str] = None):
        super().__init__(callback_context_data)
        self.json_built = dict()
        if initial_data is not None:
            for key, value in initial_data.items():
                self.put(key, value)

    def __setitem__(self, key: str, value: bytes):
        self.put(key, value)

    def __getitem__(self, key: str):
        return self.json_built.get(key)

    def __iter__(self):
        return self.json_built.__iter__()

    def __hash__(self):
        return hash(self.json_built)

    def __eq__(self, other):
        if not isinstance(other, MultiFileRequest):
            return False
        return self.json_built == other.json_built

    def __len__(self):
        return len(self.json_built)

    def put(self, file_name: str, file_data: bytes) -> None:
        """
        Add a file to upload into this request.
        :param file_name: The file name to upload
        :param file_data: The file data to upload.
        """
        if not file_name or not file_data:
            return
        encoded_data: bytes = base64.b64encode(file_data)
        if not encoded_data:
            return
        self.json_built[file_name] = encoded_data.decode("utf-8")

    def get_callback_type(self) -> CallbackType:
        return CallbackType.WRITE_FILE

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = super().to_json()
        ret['files'] = self.json_built
        return ret
