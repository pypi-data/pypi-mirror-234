from __future__ import annotations
import flask
import json

'''
    This file contains the class for the Kasumi SDK.
    It is used to interact with the Kasumi API.
'''
from typing import List, Dict, Any, Tuple, Union
from .abstract import *
from .embedding import KasumiEmbedding

import threading

class DefaultActionStrategy(AbstractKasumiActionStrategy):
    '''
    This class is used to implement the default search strategy.
    '''

    def on_single_result(result: List[KasumiActionResult]) -> Tuple[bool, List[KasumiActionResult]]:
        '''
            on single result,return processed single_result and complete search
            for simple scenario, can just judge if result empty
            for complex scenario, can judge if result is what we want using LLM or other method
        '''
        if len(result) == 0:
            return False,result
        else:
            return True,result
        
    def on_all_result(result: List[List[KasumiActionResult]]) -> List[KasumiActionResult]:
        '''
            on all result, maybe we can do some post process here
            for simple scenario, can just return first non-empty result
            for complex scenario, can do some post process here,eg: using LLM to summarize or other things
        '''
        temp_result = None
        for i in result:
            if len(i) != 0:
                temp_result = i
                break
        return temp_result

    def action(app: 'Kasumi', action_name: str, action_param: Dict) -> List[KasumiActionResult]:
        actions = sorted(app.get_actions(), key=lambda action: action.priority, reverse=True)
        all_results = []
        for action in actions:
            if action.name != action_name:
                continue
            single_result = action.action(action_param)
            complete,single_result = DefaultActionStrategy.on_single_result(single_result)
            all_results.append(single_result)
            if complete:
                break
        return DefaultActionStrategy.on_all_result(all_results)

class KasumiConfigration(AbstractKasumiConfigration):
    _token: str = ""
    _search_key: str = ""
    _kasumi_url: str = ""
    _app_id: int = 0
    _action_strategy: AbstractKasumiActionStrategy  

    def __init__(self, app_id: int, token: str, search_key: str,
                  search_strategy: AbstractKasumiActionStrategy = DefaultActionStrategy,
                  kasumi_url: str = "http://kasumi.miduoduo.org:8192"):
        self._app_id = app_id
        self._token = token
        self._search_key = search_key
        self._action_strategy = search_strategy
        self._kasumi_url = kasumi_url

    def get_app_id(self) -> int:
        return self._app_id

    def get_token(self) -> str:
        return self._token
    
    def get_search_key(self) -> str:
        return self._search_key
    
    def get_kasumi_url(self) -> str:
        return self._kasumi_url
    
    def get_action_strategy(self) -> AbstractKasumiActionStrategy:
        return self._action_strategy

class KasumiActionResultField(AbstractKasumiActionResultField):
    """
    KasumiSearchResultField is used to represent a field in the search result.
    _key: The key of the field.
    _content: The content of the field.
    _llm_disabled: this field will not be sent to the LLM if this is set to True.
    _show_disabled: this field will not be shown to the client if this is set to True.
    _is_file: this field is a file if this is set to True.
        _content_type only works when _is_file is set to True.
        _filename only works when _is_file is set to True.
        _url only works when _is_file is set to True.
        _filesize only works when _is_file is set to True.
    """
    _key: str = ""
    _content: str = ""
    _llm_disabled: bool = False
    _show_disabled: bool = False
    _is_file: bool = False
    _content_type: str = ""
    _filename: str = ""
    _url: str = ""
    _filesize: int = 0

    def __init__(
        self,key: str, content: str, llm_disabled: bool = False, show_disabled: bool = False, 
        is_file: bool = False, content_type: str = "", filename: str = "", url: str = "", filesize: int = 0
    ):
        self._key = key
        self._content = content
        self._llm_disabled = llm_disabled
        self._show_disabled = show_disabled
        self._is_file = is_file
        self._content_type = content_type
        self._filename = filename
        self._url = url
        self._filesize = filesize

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self._key,
            "content": self._content,
            "llm_disabled": self._llm_disabled,
            "show_disabled": self._show_disabled,
            "is_file": self._is_file,
            "content_type": self._content_type,
            "filename": self._filename,
            "url": self._url,
            "filesize": self._filesize
        }
    
class KasumiActionResult(AbstractKasumiActionResult):
    _fields: List[KasumiActionResultField] = []

    def __init__(self, fields: List[KasumiActionResultField]):
        self._fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fields": [field.to_dict() for field in self._fields]
        }
    
    @staticmethod
    def load_from_dict(
        data: Dict[str, Any], disabled_llm_columns: List[str] = None, disabled_show_columns: List[str] = None,
        files: List[Dict[str, Union[int, str]]] = None
    ) -> KasumiActionResult:
        '''
            data will be sent to the LLM as normal text.
            disabled_llm_columns: this field will not be sent to the LLM if this is set to True.
            disabled_show_columns: this field will not be shown to the client if this is set to True.
            files: all files in this search result. be like this:
                [
                    {
                        "content_type": "image/png",
                        "filename": "1.png",
                        "url": "http://xxx.com/file/1.png",
                        "filesize": 1024",
                        "content": "anything",
                        "key": "result"
                    }
                ]
                content will not work if the url is set, but the key is still needed.
                if the url is not set, the content will be upload to kasumi OSS and the url will be set automatically.
        '''
        disabled_llm_columns = disabled_llm_columns or []
        disabled_show_columns = disabled_show_columns or []

        fields = []
        for key in data:
            value = data[key]
            fields.append(KasumiActionResultField(
                key=key, content=value, llm_disabled=key in disabled_llm_columns, show_disabled=key in disabled_show_columns
            ))

        for file in files or []:
            fields.append(KasumiActionResultField(
                key=file['key'], content=file['content'], 
                llm_disabled=file['key'] in disabled_llm_columns, 
                show_disabled=file['key'] in disabled_show_columns, 
                is_file=True, content_type=file['content_type'], 
                filename=file['filename'], url=file['url'], filesize=file['filesize']
            ))

        return KasumiActionResult(fields)

    @staticmethod
    def get_file_dict(
        content_type: str = 'application/octet-stream',
        filename: str = 'file',
        content: str = '',
        filesize: int = 0,
        key: str = 'result',
        url: str = ''
    ) -> Dict[str, Union[int, str]]:
        return {
            "content_type": content_type,
            "filename": filename,
            "content": content,
            "filesize": filesize,
            "key": key,
            "url": url
        }

class KasumiActionResponse(AbstractKasumiActionResponse):
    _code: int = 0
    _message: str = ""
    _data: List[KasumiActionResult]

    def __init__(self, code: int, message: str, data: List[KasumiActionResult]):
        self._code = code
        self._message = message
        self._data = data

    def get_code(self) -> int:
        return self._code

    def get_message(self) -> str:
        return self._message

    def get_data(self) -> List[KasumiActionResult]:
        return self._data
    
    def __str__(self) -> str:
        return f"KasumiActionResponse(code={self._code},message={self._message},data={self._data})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self._code,
            "message": self._message,
            "data": [result.to_dict() for result in self._data]
        }

class KasumiInfoResponse(AbstractKasumiInfoResponse):
    _code: int = 0
    _message: str = ""
    _data: Dict[str, Any]

    def __init__(self, code: int, message: str, data: Dict[str, Any]):
        self._code = code
        self._message = message
        self._data = data

    def get_code(self) -> int:
        return self._code

    def get_message(self) -> str:
        return self._message

    def get_data(self) -> Dict[str, Any]:
        return self._data

class KasumiSession(AbstractKasumiSession):
    _user_token: str = ""

class Kasumi(AbstractKasumi):
    """
    This class is used to interact with the Kasumi API.

    :param config: The configuration of the Kasumi SDK.
    
    :raises all methods in Kasumi may raise KasumiException if the Kasumi API returns an error.
    """
    _config: KasumiConfigration = None
    _actions: List[AbstractKasumiAction] = []
    _sessions: Dict[int, KasumiSession] = {}
    _embedding: AbstractKasumiEmbedding = KasumiEmbedding()

    def __init__(self, config: KasumiConfigration):
        self._config = config

    def embeding_text(self, text: str) -> List[float]:
        ident = threading.get_ident()
        try:
            if ident in self._sessions:
                session = self._sessions[threading.get_ident()]
                embedding = self._embedding.embedding_text(self, text, TokenType.ENCRYPTION, session._user_token)
            else:
                embedding = self._embedding.embedding_text(self, text, TokenType.PLAINTEXT, self._config.get_token())
            return embedding
        except Exception as e:
            raise KasumiException("Failed to get embedding of text. for more information, please see the traceback. %s" % e)
        
    def search_embedding_similarity(self, embedding: List[float], top_k: int = 3) -> List[AbstractKasumiEmbeddingItem]:
        try:
            similarities = self._embedding.search_similarity(self, embedding, top_k=top_k)
            return similarities
        except Exception as e:
            raise KasumiException("Failed to search embedding similarity. for more information, please see the traceback. %s" % e)

    def get_embedding_by_id(self, id: str) -> AbstractKasumiEmbeddingItem:
        try:
            embedding = self._embedding.get_embedding_by_id(self, id)
            return embedding
        except Exception as e:
            raise KasumiException("Failed to get embedding by id. for more information, please see the traceback. %s" % e)
        
    def del_embedding_by_id(self, id: str) -> bool:
        try:
            return self._embedding.del_embedding_by_id(self, id)
        except Exception as e:
            raise KasumiException("Failed to delete embedding by id. for more information, please see the traceback. %s" % e)

    def insert_embedding(self, embedding: List[float], id: str) -> bool:
        try:
            return self._embedding.insert_embedding(self, embedding, id)
        except Exception as e:
            raise KasumiException("Failed to insert embedding. for more information, please see the traceback. %s" % e)

    def add_action(self, action: AbstractKasumiAction) -> None:
        action.set_app(self)
        self._actions.append(action)

    def get_actions(self) -> List[AbstractKasumiAction]:
        return self._actions

    def _handle_request_info(self, request: Dict[str, Any]) -> KasumiInfoResponse:
        if request.get('remote_search_key') != self._config.get_search_key():
            return KasumiInfoResponse(
                code=401, message="Unauthorized", data={}
            )
        
        desc = 'there are %d actions available:' % len(self._actions)
        for action in self._actions:
            desc += '\n\nname: %s' % action.name
            desc += '\ndescription: %s' % action.description
            desc += '\nparams example: %s' % json.dumps(action.param_template)
            desc += '\n\n'

        return KasumiInfoResponse(
            code=200, message="OK", data=desc,
        )

    def _handle_request_action(self, request: Dict[str, Any]) -> KasumiActionResponse:
        if request.get('remote_search_key') != self._config.get_search_key():
            return KasumiActionResponse(
                code=401, message="Unauthorized", data=[]
            )

        ident = threading.get_ident()
        token = request.get('token', '')
        session = KasumiSession()
        session._user_token = token
        self._sessions[ident] = session

        action_param = request.get('action_param','{}')
        action_name = request.get('action_name','')
        if action_name == '' or action_param == '{}' or action_param == '' or action_param is None:
            return KasumiActionResponse(
                code=200, message="OK", data=[KasumiActionResult.load_from_dict({
                    "result": "action_name or action_param cannot be empty"
                })]
            )

        action_param = json.loads(action_param)
        results = self._config.get_action_strategy().action(self, action_name, action_param)
        if ident in self._sessions:
            del self._sessions[ident]

        return KasumiActionResponse(
            code=200, message="OK", data=results
        )

    def run_forever(self, http_port: int = 3433) -> None:
        self.app = flask.Flask(__name__)

        @self.app.route('/info', methods=['POST'])
        def info():
            print(flask.request.get_json())
            request = flask.request.get_json()
            info_response = self._handle_request_info(request)
            return info_response.to_flask_response()
        
        @self.app.route('/action', methods=['POST'])
        def action():
            request = flask.request.get_json()
            action_response = self._handle_request_action(request)
            return action_response.to_flask_response()

        # launch http server
        global server
        from eventlet import wsgi, listen
        server = listen(('0.0.0.0', http_port))
        wsgi.server(server, self.app)

    def upload_file(self, file: bytes, filename: str, content_type: str = 'application/octet-stream') -> str:
        '''
            upload file to kasumi oss
            return url
            exception will be raised if upload failed
        '''
        from .upload import upload_bytes_with_upload_url, request_upload_url
        url = request_upload_url(filename, self._config.get_app_id(), self._config.get_search_key(), self._config.get_kasumi_url())
        return upload_bytes_with_upload_url(url, file, content_type)
