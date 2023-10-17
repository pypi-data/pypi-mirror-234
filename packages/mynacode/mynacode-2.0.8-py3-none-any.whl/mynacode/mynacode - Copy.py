import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime

#protocol = 'https'
protocol = 'http'


IP = '127.0.0.1:8000'
#IP = 'mynacode.com'
#prev_func_list = ['a1zqw_9_', 'b1zqw_9_']
prev_func_list = []
prev_node = -999
username = ""
key = ""
run_id = -999


def reset_os_variables():

    os.environ["include_variables"] = 'False'
    os.environ["variables_to_track"] = '[]'
    os.environ["variables_to_not_track"] = '[]'
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    reset_os_variables()
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def project(project_name, project_id = -999):
  global run_id

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  project_info_list = ['Codebase Python ' + platform.python_version()]
  
  project_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          project_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            project_info_list.append("GPU ID " + str(gpu_id))
            project_info_list.append(gpu_name)
            project_info_list.append(str(gpu_memory) + " MB")
  except:
      project_info_list.append("No NVIDIA Driver found")

  project_info_list.append("    CPU    ")
  project_info_list.append(platform.processor())
  project_info_list.append(platform.platform())
  project_info_list.append(platform.machine())
  project_info_list.append("    MEMORY    ")
  project_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'project_id' : project_id, 'project_name': project_name, 'installed_packages': str(installed_packages_list),
          'username': username, 'key': key, 'run_information': str(project_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/create_project', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['exists'] == 0:
      print("Created a new project.")
    else:
      print("Project exists. Created a new run")
      
  run_id = response_dict['run_id']
  reset_os_variables()    
  
def node(node_name = "", filename = "", lineno = 0, node_description="", library_function = 0):
  global prev_node
  
  if prev_node == -999:
    data = {'current_node_name': node_name, 'node_description': node_description,
            'username': username, 'key': key, 'run_id': run_id,
            'filepath': filename, 'line_number': lineno, 'library_function': library_function}
  else:
    data = {'current_node_name': node_name, 'connect_with':  prev_node, 'node_description': node_description,
            'username': username, 'key': key, 'run_id': run_id,
            'filepath': filename, 'line_number': lineno, 'library_function': library_function}

  response = requests.post(protocol+'://'+IP+'/api/create_node', data=data)

  if response.text == '-1':
    print("Authentication failed")

      
  prev_node = response.text #Store previous node


def node_log(variables, main_function = False):
  global prev_node
  if len(variables) == 0:
    return 0
  
  for var_key in variables:
      if len(str(variables[var_key]))>40:
          variables[var_key] = 'Large value'
      else:
          variables[var_key] = str(variables[var_key])

  if main_function == True:
      data = {'run_id':run_id, '_id': prev_node, 'type':'node', 'variables': str(variables), 'username': username, 'key': key, 'main_function':1}
  else:
      data = {'_id': prev_node, 'type':'node', 'variables': str(variables), 'username': username, 'key': key, 'main_function':0}

  response = requests.post(protocol+'://'+IP+'/api/set_variables', data=data)


def include_variables(status = False, include_only = [], exclude_only = []):
  if status == False:
    return
  elif status == True:
    os.environ["include_variables"] = 'True'
    
    if len(include_only) != 0:
      variables_to_track = []
      for var in include_only:
        variables_to_track.append(var)
      os.environ["variables_to_track"] = str(variables_to_track)
      print(os.environ["variables_to_track"])
      
    elif len(exclude_only) != 0:
      variables_to_not_track = []
      for var in exclude_only:
        variables_to_not_track.append(var)
      os.environ["variables_to_not_track"] = str(variables_to_not_track)
      print(os.environ["variables_to_not_track"])
      
    else:
      pass


def tracefunc(frame, event, arg):
    save_function = False
    library_function = False
    global prev_func_list
    
    if '__autograph_generated' in frame.f_code.co_filename:
        pass
    elif 'Attributes' in frame.f_code.co_filename or 'Attributes' in frame.f_code.co_name:
        pass
    elif "Python" in frame.f_code.co_filename:
        pass
    elif "<module" in frame.f_code.co_name:
        pass
    elif ("<" in frame.f_code.co_name or "<" in frame.f_code.co_filename) and ("<ipython-input" not in frame.f_code.co_filename):
        pass
    elif "site-packages" in frame.f_code.co_filename:
        pass
    elif "dist-packages" in frame.f_code.co_filename:
        pass
    elif "lib/python" in frame.f_code.co_filename:
        pass
    elif "_init_" in frame.f_code.co_name:
        pass
    else:
        save_function = True
        
    if save_function:
        
        if event == "call":
            if not library_function:
              if frame.f_code.co_name in prev_func_list:
                return
              else:
                prev_func_list.pop(0)
                prev_func_list.append(frame.f_code.co_name)

            if library_function == True:
                node(frame.f_code.co_filename.rsplit('/', 1)[1], frame.f_code.co_filename, frame.f_code.co_firstlineno,"", 1)
            else:
              if 'ipykernel' not in frame.f_code.co_filename:
                  node(frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno,"", 0)
              else:
                  node(frame.f_code.co_name, 'Jupyter notebook', 0,"", 0)
                  
        if event == "return":
            variables_to_log = {}
            include_variables = os.environ.get("include_variables") == 'True'
            
            if include_variables:
              variables_to_track = set(ast.literal_eval(os.environ.get("variables_to_track")))
              variables_to_not_track = set(ast.literal_eval(os.environ.get("variables_to_not_track")))

              if len(variables_to_track) != 0:
                variables_to_log.update({key: frame.f_locals[key] for key in variables_to_track if key in frame.f_locals})
                    
              elif len(variables_to_not_track) != 0:
                for key in frame.f_locals:
                  if key not in variables_to_not_track:
                    variables_to_log[key] = frame.f_locals[key]
                    
              else:
                for key in frame.f_locals:
                  variables_to_log[key] = frame.f_locals[key]
                          

              if frame.f_code.co_name == 'main': #code ends here
                  node_log(variables_to_log, True)
              else:
                  node_log(variables_to_log, False)

        return tracefunc
    
   
def settrace(state=True, library_function=False, repitition = 2):
  global prev_func_list
  prev_func_list = ['f'] * repitition
    
  if state==True: 
      sys.setprofile(tracefunc)
  else:
      sys.setprofile(None)





