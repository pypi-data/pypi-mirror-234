from enum import Enum


class CallbackType(Enum):
    """
    All possible client callbacks a webhook handler could use.
    """
    FILE_PROMPT = 0
    MULTI_FILE_PROMPT = 1
    WRITE_FILE = 2
    DATA_RECORD_SELECTION = 3
    TABLE_ENTRY_DIALOG = 4
    FORM_ENTRY_DIALOG = 5
    LIST_DIALOG = 6
    OPTION_DIALOG = 7


class WebhookEndpointType(Enum):
    """
    Invocation point type that the webhook endpoint will be called by Sapio.
    """
    ACTIONMENU = 'Action Menu', False
    FORMTOOLBAR = 'Form Toolbar', False
    TABLETOOLBAR = 'Table Toolbar', False
    TEMP_DATA_FORM_TOOLBAR = 'Temporary Data Form Toolbar', False
    TEMP_DATA_TABLE_TOOLBAR = 'Temporary Data Table Toolbar', False
    VELOXONSAVERULEACTION = 'Velox On Save Rule Action', True
    VELOX_RULE_ACTION = 'Velox Rule Action', True
    VELOXELNRULEACTION = 'Velox ELN Rule Action', True
    NOTEBOOKEXPERIMENTMAINTOOLBAR = 'Notebook Experiment Main Toolbar Button', False
    EXPERIMENTENTRYTOOLBAR = 'Notebook Experiment Entry Toolbar Button', False
    SELECTIONDATAFIELD = 'Selection Data Field', False
    REPORT_BUILDER_TEMPLATE_DATA_POPULATOR = 'Report Builder Template Data Populator Plugin', False
    SCHEDULEDPLUGIN = 'Scheduled Plugin', False,
    ACTIONDATAFIELD = 'Action Data Field', False
    CALENDAR_EVENT_CLICK_HANDLER = 'Calendar Event Click Handler Plugin', False
    CUSTOM = 'Custom Plugin Point', False,
    ACTION_TEXT_FIELD = 'Action Text Field Plugin', False
    NOTEBOOKEXPERIMENTGRABBER = 'Notebook Experiment Grabber', False

    display_name: str
    retry_endpoint: bool

    def __init__(self, display_name: str, retry_endpoint: bool):
        self.display_name = display_name
        self.retry_endpoint = retry_endpoint


class WebhookDirectiveType(Enum):
    """
    All client callback directives available to a Sapio webhook.
    """
    FORM = 'FormDirectivePojo'
    TABLE = 'TableDirectivePojo'
    CUSTOM_REPORT = 'CustomReportDirectivePojo'
    EXPERIMENT_ENTRY = 'ExperimentEntryDirectivePojo'
    ELN_EXPERIMENT = 'NotebookExperimentDirectivePojo'
    HOME_PAGE = 'HomePageDirectivePojo'

    jackson_type: str

    def __init__(self, jackson_type: str):
        self.jackson_type = jackson_type
