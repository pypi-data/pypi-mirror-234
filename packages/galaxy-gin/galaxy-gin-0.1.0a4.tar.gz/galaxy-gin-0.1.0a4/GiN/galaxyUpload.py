from ipyuploads.upload import ValueSerialization
from ipyuploads import Upload
import base64
from traitlets import Unicode, Bool, CaselessStrEnum, Dict, default, Bunch
from ._frontend import module_name, module_version
from ipywidgets.widgets.trait_types import InstanceDict, TypedTuple
from ipywidgets import ButtonStyle, register, CoreWidget, ValueWidget, widget_serialization



class GalaxyUpload(Upload):
    """Chunked upload widget"""
    _model_name = Unicode('GalaxyUploadModel').tag(sync=True)
    _model_module =  Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('GalaxyUploadView').tag(sync=True)
    _view_module =   Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    accept = Unicode(help='File types to accept, empty string for all').tag(sync=True)
    multiple = Bool(help='If True, allow for multiple files upload').tag(sync=True)
    disabled = Bool(help='Enable or disable button').tag(sync=True)
    icon = Unicode('upload', help="Font-awesome icon name, without the 'fa-' prefix.").tag(sync=True)
    button_style = CaselessStrEnum(
        values=['primary', 'success', 'info', 'warning', 'danger', ''], default_value='',
        help='Use a predefined styling for the button.').tag(sync=True)
    style = InstanceDict(ButtonStyle).tag(sync=True, **widget_serialization)
    error = Unicode(help='Error message').tag(sync=True)
    value = Dict(Dict(), help='The file upload value').tag(sync=True, echo_update=False,
                                                           from_json=ValueSerialization.deserialize_value,
                                                           to_json=ValueSerialization.serialize_value)
    busy = Bool(help='Is the widget busy uploading files').tag(sync=True)

    chunk_complete = lambda self, name, count, total: None
    file_complete = lambda self, name: None
    all_files_complete = lambda self, names: None

    def __init__(self, **kwargs):
        super(GalaxyUpload, self).__init__(**kwargs)
        self.on_msg(self.handle_messages)

        # Set optional callbacks
        if 'chunk_complete' in kwargs: self.chunk_complete = kwargs['chunk_complete']
        if 'file_complete' in kwargs: self.file_complete = kwargs['file_complete']
        if 'all_files_complete' in kwargs: self.all_files_complete = kwargs['all_files_complete']
    
    @staticmethod
    def write_chunk(name, encoded_chunk, first_chunk):
        mode = 'w' if first_chunk else 'a'
        with open(name, mode) as f:
            f.write(base64.b64decode(encoded_chunk).decode("utf-8"))
    
    @staticmethod
    def default_callback(**kwargs):
        pass








