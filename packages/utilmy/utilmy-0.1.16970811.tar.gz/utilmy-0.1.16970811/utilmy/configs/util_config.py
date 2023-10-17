# -*- coding: utf-8 -*-
""" utils for condig loading/ type checking
Doc::

    # python util_config.py test





"""
import importlib
import os
from pathlib import Path
from typing import Union

from box import Box

#########################################################################################################
from utilmy.utilmy_base import (log, loge, os_get_dirtmp)


#########################################################################################################
#########################################################################################################
def test_all():
    test1()
    test2()
    test3()



#################################################
def test1():
    """ config_load test code
    """
    flist = test_create_file(dirout=None)
    for xi in flist:
        cfg_dict = config_load(xi )
        if len(cfg_dict) > 2 or len(cfg_dict.get("database",dict())) > 2:
            log( str(xi) +", " + str(cfg_dict) +'', "\n")
        else :
            raise Exception( f" dict is empty {xi}"  )

    ###  Add other test for config_load
    xi=flist[0]

    log("# test to_dataclass")
    cfg_dict = config_load(xi, to_dataclass=True)
    log(cfg_dict.details )
    assert len(cfg_dict.details) == 4, "FAILED -> config_load(); The parameter to_dataclass doesn't work"

    log('\ntest config_field_name')
    cfg_dict = config_load(xi, config_field_name='details')
    assert len(cfg_dict) > 0, "FAILED -> config_load(); The parameter config_field_name doesn't work"

    log('\nENV variables')
    path = 'default_output_config/config.yaml'
    os.environ['myconfig'] = path
    cfg_dict = config_load(None, environ_path_default='myconfig', save_default=True)
    assert len(cfg_dict) > 1, "FAILED -> config_load(); The return value isn't expected"
    assert os.path.exists(os.path.abspath(path)), "FAILED -> config_load(); The config wasn't saved"

    log('\ntest path_default and save_default')
    path = 'default_output_config/config.yaml'
    cfg_dict = config_load(None,path_default=path,save_default=True)
    assert len(cfg_dict) > 1, "FAILED -> config_load(); cfg_dict is empty"
    assert os.path.exists(os.path.abspath(path)), "FAILED -> config_load(); The config wasn't saved"

    log('\ntest config_default')
    config_default= {"field1": "test config_default", "field2": {"version":"1.0"},"field3":"data"}
    cfg_dict = config_load(None,config_default=config_default)
    assert cfg_dict == config_default, "FAILED -> config_load(); The return value isn't expected"



def test2():
   """ config_isvalid_yaml  schema


   """
   dircur   = os_get_dirtmp()

   #######  yaml file ###############################################
   ss ="""
    string: "hello"
    regex: 'abcde'
    number: 13.12
    integer: 2
    boolean: True
    list: ['hi']
    enum: 1
    map:
        hello: 1
        another: "hi"
    empty: null
    date: 2015-01-01
    nest:
    integer: 1
    nest:
        string: "nested"   
   """
   to_file(ss, dircur + "/config_val.yaml")
   cfg_dict = config_load(  "config.yaml")


   #######  config_val file ########################################
   ss ="""
    string: str()
    regex: regex('abcde')
    number: num(min=1, max=13.12)
    integer: int()
    boolean: bool()
    list: list()
    enum: enum('one', True, 1)
    map: map()
    empty: null()
    date: day()
    nest:
    integer: int()
    nest:
        string: str()   
   """
   to_file(ss, dircur + "/config_val.yaml")
   isok = config_isvalid_yamlschema(cfg_dict,  dircur + "/config_val.yaml")
   log(isok)



def test3():
    """  test_pydanticgenrator(
    Docs::

        https://github.com/koxudaxi/datamodel-code-generator
        pip install datamodel-code-generator
    """
    from datamodel_code_generator import InputFileType
    # generating from json file
    pydantic_model_generator(
        Path("config.json"), InputFileType.Json, Path("pydantic_model_json.py")
    )
    assert Path("pydantic_model_json.py").exists(), "File does not exist"

    # generating from yaml file
    pydantic_model_generator(
        Path("config.yaml"), InputFileType.Yaml, Path("pydantic_model_yaml.py")
    )
    assert Path("pydantic_model_yaml.py").exists(), "File does not exist"


def test4():
    from pydantic import BaseModel
    cfg_dict = config_load("config.yaml")
    pydantic_model = convert_dict_to_pydantic(cfg_dict, "pydantic_config_val.yaml")
    assert isinstance(pydantic_model, BaseModel)



###############################################################################################
def to_file(txt, fpath, mode='a'):
    with open(fpath, mode=mode) as fp:
        fp.write(txt)


def test_create_file(dirout=None):
    import yaml, json, toml

    dir_cur = os_get_dirtmp() if dirout is None else dirout

    ##### create file for test
    ddict = {"data": "test", "details": {"version":"1.0", 'integer': 1, 'float': 1.0, 'boolean': True }}

    flist = []

    ##### create config.yaml
    with open( dir_cur + "/config.yaml", mode="w") as fp:
        ddict['list1'] = [1,2]
        yaml.dump(ddict, fp, default_flow_style=False)
        flist.append(dir_cur + "/config.yaml")


    #### create config.json
    with open( dir_cur + "/config.json", mode="w") as fp:
        json.dump(ddict, fp,indent=3)
        flist.append(dir_cur + "/config.json")

    #### create config.conf
    # TODO: the function config_load doesn't support conf files
    data_ini="""[APP]
            ENVIRONMENT = development
            DEBUG = False

            [DATABASE]
            USERNAME = root
            PASSWORD = p@ssw0rd
    """
    with open( dir_cur + "/config.conf", "w") as fp:
        fp.write(data_ini)
        flist.append(dir_cur + "/config.conf")

    #### create config.toml
    with open( dir_cur + "/config.toml", "w") as toml_file:
        toml.dump(ddict, toml_file)
        flist.append(dir_cur + "/config.toml")

    ### create  config.ini
    data_ini="""[APP]
            ENVIRONMENT = development
            DEBUG = False

            [DATABASE]
            USERNAME = root
            PASSWORD = p@ssw0rd
    """
    with open( dir_cur + "/config.ini", "w") as fp:
        fp.write(data_ini)
        flist.append(dir_cur + "/config.ini")


    ## create  config.properties
    properties="""[database]
            db.user=mkyong
            db.password=password
            db.url=localhost
    """
    with open( dir_cur + "/config.properties", "w") as fp:
        fp.write(properties)
        flist.append(dir_cur + "/config.properties")

    return flist




#########################################################################################################
def config_load(
        config_path:    str  = None,
        to_dataclass:   bool = True,
        config_field_name :  str  = None,
        environ_path_default: str = "config_path_default",
        path_default:   str  = None,
        config_default: dict = None,
        save_default:   bool = False,

        verbose=0
) -> dict:
    """ Universal config loader: .yaml, .conf, .toml, .json, .ini .properties INTO a dict
    Doc::

        config_path:    str  = None,
        to_dataclass:   bool = True,  True, can access the dict as dot   mydict.field
        config_field_name :  str  = Extract sub-field name from the dict

        --- Default config
        environ_path_default: str = "config_path_default",
        path_default:   str  = None,
        config_default: dict = None,
        save_default:   bool = False,

       -- Priority steps
        1) load config_path
        2) If not, load in USER/.myconfig/.config.yaml
        3) If not, create default save in USER/.myconfig/.config.yaml
        Args:
            config_path:    path of config or 'default' tag value
            to_dataclass:   dot notation retrieval

            path_default :  path of default config
            config_default: dict value of default config
            save_default:   save default config on disk
        Returns: dict config
    """
    import pathlib

    #########Default value setup ###########################################
    if path_default is None:
        config_path_default = os.environ.get(environ_path_default, str(os.path.dirname( os.path.abspath(__file__) )) + "/myconfig/config.yaml"  )
        path_default = os.path.dirname(config_path_default)
    else:
        config_path_default = path_default
        path_default = os.path.dirname(path_default)

    if config_default is None:
        config_default = {"field1": "test", "field2": {"version":"1.0"}}

    #########Config path setup #############################################
    if config_path is None or config_path == "default":
        log(f"Config: Using {config_path_default}")
        config_path = config_path_default
    else:
        config_path = pathlib.Path(config_path)

    ######### Load Config ##################################################
    import yaml
    try:
        log("Config: Loading ", config_path)
        if config_path.suffix in {".yaml", ".yml"}  :
            #Load the yaml config file
            with open(config_path, "r") as yamlfile:
                config_data = yaml.load(yamlfile, Loader=yaml.FullLoader)

            if isinstance(config_data, dict ):
                cfg = config_data
            else :
                dd = {}
                for x in config_data :
                    for key,val in x.items():
                       dd[key] = val
                cfg = dd

        elif config_path.suffix == ".json":
            import json
            cfg = json.loads(config_path.read_text())

        elif config_path.suffix in {".properties", ".ini", ".conf"}:
            from configparser import SafeConfigParser
            cfg = SafeConfigParser()
            cfg.read(str(config_path))

        elif config_path.suffix == ".toml":
            import toml
            cfg = toml.loads(config_path.read_text())
        else:
            raise Exception(f"not supported file {config_path}")

        if config_field_name in cfg :
            cfg = cfg[config_field_name]


        if verbose >=2 :
            log(cfg)

        if to_dataclass:  ### myconfig.val  , myconfig.val2
            from box import Box
            return Box(cfg)
        return cfg

    except Exception as e:
        log(f"Config: Cannot read file {config_path}", e)

    ######################################################################
    log("Config: Using default config")
    log(config_default)
    if save_default:
        log(f"Config: Writing config in {config_path_default}")
        os.makedirs(path_default, exist_ok=True)
        with open(config_path_default, mode="w") as fp:
            yaml.dump(config_default, fp, default_flow_style=False)

    return config_default






def config_isvalid_yamlschema(config_dict: dict, schema_path: str = 'config_val.yaml', silent: bool = False) -> bool:
    """Validate using a  yaml file.
    Doc::

        Args:
            config_dict:
            schema_path:
            silent:
        Returns: True/False
    """
    import yamale
    schema = yamale.make_schema(schema_path)

    try:
        result = schema.validate(config_dict, data_name=schema_path, strict=True)
        if not result.isValid():
            raise yamale.YamaleError([result])
        return True

    except yamale.YamaleError as e:
        for result in e.results:
            loge(f"Error validating data '{result.data}' with '{result.schema}'\n\t")
            for error in result.errors:
                loge(f"\t{error}")
        return False


def config_isvalid_pydantic(config_dict: dict,
                            pydanctic_schema: str = 'config_py.yaml', silent: bool = False) -> bool:
    """Validate using a pydantic files
    Docs::

            config_dict:
            pydanctic_schema:
            silent:
        Returns: True/False
    """
    import yamale
    try:
        return True

    except yamale.YamaleError as e:
        return False


##################################################################################################
##################################################################################################
def convert_yaml_to_box(yaml_path: str) -> Box:
    with open(yaml_path) as f:
        data = yaml.load(f)
    return Box(data)


def convert_dict_to_pydantic(config_dict: dict, schema_name: str):
    # pip install pydantic-gen
    from pydantic_gen import SchemaGen

    generated = SchemaGen(schema_name)
    generated.to_file(f"{schema_name.split('.')[0]}.py")

    pydantic_module = importlib.import_module(
        f"zz936.configs.{schema_name.split('.')[0]}"
    )
    return pydantic_module.MainSchema(**config_dict)


def pydantic_model_generator(
        input_file: Union[Path, str],
        input_file_type,
        output_file: Path,
        **kwargs,
) -> None:
    """ Generate Pydantic template
    Docs::

        Args:
            input_file:
            input_file_type:
            output_file:
            **kwargs:

        Returns:
        # https://github.com/koxudaxi/datamodel-code-generator
        # pip install datamodel-code-generator

    """
    from datamodel_code_generator import Error, generate

    try:
        generate(
            input_file, input_file_type=input_file_type, output=output_file, **kwargs
        )
    except Error as e:
        loge(f"Error occurred while generating pydantic model: `{e.message}`")
    else:
        log(
            f"Successfully generated pydantic model from {input_file} to {output_file}"
        )




#########################################################################################################
def global_verbosity(cur_path, path_relative="/../../config.json",
                   default=5, key='verbosity',):
    """ Get global verbosity
    verbosity = global_verbosity(__file__, "/../../config.json", default=5 )

    verbosity = global_verbosity("repo_root", "config/config.json", default=5 )

    cur_path:
    path_relative:
    key:
    default:
    :return:
    """
    import utilmy, json
    try   :
      if 'repo_root' == cur_path  :
          cur_path =  utilmy.git_repo_root()

      if '.json' in path_relative :
         dd = json.load(open(os.path.dirname(os.path.abspath(cur_path)) + path_relative , mode='r'))

      elif '.yaml' in path_relative or '.yml' in path_relative :
         import yaml
         dd = yaml.load(open(os.path.dirname(os.path.abspath(cur_path)) + path_relative , mode='r'))

      else :
          raise Exception( path_relative + " not supported ")
      verbosity = int(dd[key])

    except Exception as e :
      verbosity = default
      #raise Exception(f"{e}")
    return verbosity







if __name__ == "__main__":
    import fire
    fire.Fire()






def zzz_config_load_validate(config_path: str, schema_path: str, silent: bool = False
                             ) -> Union[Box, None]:

    import yamale
    schema = yamale.make_schema(schema_path)
    data = yamale.make_data(config_path)

    try:
        yamale.validate(schema, data)
        return convert_yaml_to_box(config_path)

    except yamale.YamaleError as e:
        log("Validation failed!\n")
        for result in e.results:
            log(f"Error validating data '{result.data}' with '{result.schema}'\n\t")
            for error in result.errors:
                log(f"\t{error}")
        if not silent:
            raise e
