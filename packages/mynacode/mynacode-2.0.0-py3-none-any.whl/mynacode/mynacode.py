import numpy as np
import pandas as pd
import os, sys
import json, requests, ast
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import pickle
import urllib.request
from pathlib import Path
import glob, re, pkg_resources
import shutil, yaml, random, string
import time, copy

try:
    import torch
except ImportError:
    pass

try:
    import keras
except ImportError:
    try:
      import tensorflow.keras as keras
    except:
      pass

try:
    import tensorflow as tf
except ImportError:
    pass

import warnings
import functools

# Decorator function to suppress warnings within a specific function
def suppress_warnings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            result = func(*args, **kwargs)
        return result
    return wrapper

protocol = 'https'
IP = 'mynacode.com'

#protocol = 'http'
#IP = '127.0.0.1:8000'


uname = ""
ky = ""
run_id_global = ""
project_id_global = ""
run_dir_global = ""
project_dir_global = ""
prev_max = -9999999999
prev_min = 9999999999
metric_values = []
index_count = 0
sweep_global = False
save_best_results = False
first_sweep_run = False
dataset_dict = {}
results_dict = {}
track_config = {}
auth_failed = True
start_time = 0
end_time = 0



def login(username, key):
  global uname
  global ky
  global auth_failed

  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)

  if response.text == '1':
    uname = username
    ky = key
    auth_failed = False
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")
    auth_failed = True


'''
def metadata(run_id):

  if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.metadata()")
      return

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]

  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': uname, 'key': ky, 'system_information': str(system_info_list)}

  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)

  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")
'''

def create_project(project_name = "", project_directory = ""):

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.create_project()")
      return

    data = {'project_name': project_name, 'project_directory': project_directory, 'username': uname, 'key': ky}
    response = requests.post(protocol+'://'+IP+'/api/create_project_python', data=data)

    return response.text


def create_run(project_id = None, sweep = False, sweep_name = "", run_name = ""):

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.create_run()")
      return

    if not project_id:
      print("Please provide project ID")
      return

    data = {'project_id': project_id, 'username': uname, 'key': ky, 'sweep': sweep, 'sweep_name': sweep_name, 'run_name': run_name}
    response = requests.post(protocol+'://'+IP+'/api/create_run_python', data=data)

    return response.text


def start(base_folder = "", project = ""):

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.start()")
        return

    global project_id_global
    global project_dir_global
    global prev_max
    global prev_min
    global metric_values
    global metric_index
    global index_count


    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0


    if len(base_folder) == 0:
      base_folder = Path.cwd().as_posix()
    elif not os.path.exists(base_folder):
      print("Using current working directory. Path not found: ", base_folder)
      base_folder = Path.cwd().as_posix()

    if not os.path.exists(base_folder+'/'+'mynacode'):
      os.mkdir(base_folder+'/mynacode')

    if len(project) == 0:
      project = 'project'

    if not os.path.exists(base_folder+'/mynacode/'+project):
      os.mkdir(base_folder+'/mynacode/'+project)

    project_dir_global = base_folder+'/mynacode/'+project
    project_id_global = create_project(project, project_dir_global)
    print("Project Directory: ", project_dir_global)



def init(sweep = False, sweep_name = "", run_name="", save_files = False):

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.init()")
        return

    global run_dir_global
    global run_id_global
    global prev_max
    global prev_min
    global metric_values
    global metric_index
    global index_count
    global first_sweep_run
    global sweep_global
    global start_time, end_time


    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0
    start_time, end_time = 0, 0


    config_dict={}

    if sweep == True:
      sweep_global = True
      first_sweep_run = True

      if len(str(sweep_name)) == 0:
        sweep_name = ""
      else:
        sweep_name = sweep_name

      r_id = create_run(int(project_id_global), sweep = True, sweep_name = sweep_name)
      run_id_global = r_id

      if len(str(sweep_name)) == 0:  
          run_dir_global = project_dir_global+'/S'+str(r_id)+'_'+str(datetime.now())[:10].replace("-","")
      else:
          run_dir_global = project_dir_global+'/S'+str(r_id)+'_'+sweep_name+'_'+str(datetime.now())[:10].replace("-","")
          
      os.mkdir(run_dir_global)
      config_dict.update({'sweep': sweep,'sweep_name': sweep_name, 'sweep_path': run_dir_global})
    else:
      sweep_global = False
      first_sweep_run = False
      r_id = create_run(int(project_id_global), run_name = run_name)
      run_id_global = r_id
      
      if len(str(run_name)) == 0:
        run_name = ""
      else:
        run_name = run_name

      if len(str(run_name)) == 0:  
          run_dir_global = project_dir_global+'/R'+str(r_id)+'_'+str(datetime.now())[:10].replace("-","")
      else:
          run_dir_global = project_dir_global+'/R'+str(r_id)+'_'+run_name+'_'+str(datetime.now())[:10].replace("-","")
          
      os.mkdir(run_dir_global)
      config_dict.update({'run_name': run_name, 'run_path': run_dir_global})

    print("Run Directory: ", run_dir_global)

    installed_packages = pkg_resources.working_set #Save all installed packages for that project
    installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])
    config_dict.update({"installed_packages":installed_packages_list})


    if save_files == True: #Python files
      py_files = glob.glob('./**/*.py', recursive=True)
      ipynb_files = glob.glob('./**/*.ipynb', recursive=True)

      if not os.path.exists(run_dir_global+'/files/'):
        os.mkdir(run_dir_global+'/files/')

      for file in py_files:
        shutil.copy(file, run_dir_global+'/files/')

      for file in ipynb_files:
        shutil.copy(file, run_dir_global+'/files/')

      config_dict.update({"python_files_path":run_dir_global+'/files/'})


    data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)




def csv(dataframe, run_id=None):

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.csv()")
        return

    if run_dir_global == "":
        print("Please run mynacode.init(...) to create a run before calling this function")
        return

    if not run_id:
        run_id = run_id_global

    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    size = sys.getsizeof(dataframe)/1024
    shape = dataframe.shape
    dtypes_list = []

    for d in dataframe.dtypes:
        dtypes_list.append(str(d))

    data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
            'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
            'username': uname, 'size': int(size), 'shape': str(shape), 'key': ky, 'node_name': 'CSV'}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")


def evenly_spaced_points(fpr, tpr, N):
    if N <= 0:
        return []

    if N == 1:
        return [fpr[np.argmin(fpr)]]

    step_size = (len(fpr) - 1) / (N - 1)

    indices = [int(round(i * step_size)) for i in range(N)]

    selected_points_fpr = [fpr[i] for i in indices]
    selected_points_tpr = [tpr[i] for i in indices]

    return selected_points_fpr, selected_points_tpr



def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)

    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)

    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]

    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')

    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)

    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])

    c_matrix = c_matrix.tolist()

    c_matrix = [item for sublist in c_matrix for item in sublist]

    return prec, rec, spec, f1, acc, npv_val, c_matrix


def save_file(run_id, filepath):

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.save_file()")
      return

    if not os.path.exists(filepath):
      print(filepath, ' doesn not exist')
      return

    file = {'file': open(filepath,'rb')}

    response = requests.post(protocol+'://'+IP+'/api/upload_file', files=file, data={'run_id':run_id, 'username': uname, 'key': ky})


def config(config_dict = {}, run_id = None):

  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.config()")
    return

  if run_dir_global == "":
    print("Please run mynacode.init(...) to create a run before calling this function")
    return

  if not run_id:
    run_id = run_id_global

  if config_dict:
    file=open(run_dir_global+"/config.yaml","w")
    yaml.dump(config_dict,file)
    file.close()
    config_dict.update({'config_file_path': run_dir_global+"/config.yaml"})

  data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': 'Datasets', 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)



def torch_model(model=None, metric_name=None, metric_value=None, goal='maximize', current_epoch=None, track={}, run_id=None):

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_model()")
      return

    global prev_min
    global prev_max
    global metric_values
    global index_count
    results_dict = {}

    if run_dir_global == "":
      print("Please run mynacode.init(...) to create a run before calling this function")
      return

    if not os.path.exists(run_dir_global+'/model'):
      os.mkdir(run_dir_global+'/model')

    if model:
      with open(run_dir_global+'/model/saved_network.pkl', 'wb') as f:
          dill.dump(model, f, protocol=4)

      metric_values.append(metric_value)

      if goal == 'maximize':
        if metric_value > prev_max:
          prev_max = metric_value
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'maximize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': current_epoch+1})

          torch.save(model.state_dict(), run_dir_global+'/model/best_model_chkpt.pt')

          with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
            f.write('Metric: '+ str(results_dict['metric_name']))
            f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
            f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

          model_dict = {'library':'PyTorch', 'metric_values': metric_values,
                              'best_model_statedict_path': run_dir_global+'/model/best_model_chkpt.pt',
                              'best_model_network_path': run_dir_global+'/model/saved_network.pkl',
                              'best_model_logs_path': run_dir_global+'/model/best_model_logs.txt'}

          config_dict = {**model_dict, **results_dict, **track}

          results(results_dict = config_dict, run_id = None)

      elif goal == 'minimize':
        if metric_value < prev_min:
          prev_min = metric_value
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'minimize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': current_epoch+1})

          torch.save(model.state_dict(), run_dir_global+'/model/best_model_chkpt.pt')

          with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
            f.write('Metric: '+ str(results_dict['metric_name']))
            f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
            f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

          model_dict = {'library':'PyTorch', 'metric_values': metric_values,
                              'best_model_statedict_path': run_dir_global+'/model/best_model_chkpt.pt',
                              'best_model_network_path': run_dir_global+'/model/saved_network.pkl',
                              'best_model_logs_path': run_dir_global+'/model/best_model_logs.txt'}

          config_dict = {**model_dict, **results_dict, **track}

          results(results_dict = config_dict, run_id = None)

      index_count += 1
    else:
      print("Please specify a Pytorch model.")
      return


def torch_reset():

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_refresh()")
      return

    global metric_values
    global index_count
    index_count = 0
    metric_values = []

    print("Model Directory: "+run_dir_global+'/model')





def newest(path):
    files = os.listdir(path)
    if len(files) == 0:
        return None
    paths = [os.path.join(path, basename) for basename in files]
    newest_data_folder =  max(paths, key=os.path.getctime)

    try:
        temp = re.split(r'[\\/]', newest_data_folder)[-1].split('_')[-1]
        print("The path to the most recent dataset stored on the local machine:\n"+newest_data_folder)
        return newest_data_folder
    except:
        return None

































def np_data(train=[], train_labels=[], val=[], val_labels=[], test=[], test_labels=[], dataset_name="dataset", if_sweep_save_once = True, run_id = None):


  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.data()")
    return

  global first_sweep_run

  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent 'data()' calls in the current sweep are ignored. To create a new sweep, run 'init()', or, for repeated calls within a sweep, set 'if_sweep_save_once = False'.")
    return

  config_dict = {}

  train = np.array(train)
  val = np.array(val)
  test = np.array(test)

  train_labels = np.array(train_labels)
  val_labels = np.array(val_labels)
  test_labels = np.array(test_labels)

  if project_dir_global == "":
    print("Please run mynacode.start(...) to initialize a project before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return


  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  dataset_name = dataset_name.replace("_", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"_"+dataset_name
  else:
      dataset_folder = "R"+str(run_id_global)+"_"+dataset_name

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')


  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('_')[-1] != dataset_name:
      save_new_data_flag = 1
  else:
      if (len(train_labels) > 0) and (os.path.exists(newest_data_folder + '/train_labels.pkl')): #Both exist
          percent_20 = int((20/100)*len(train_labels))

          with open(newest_data_folder + '/train_labels.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], train_labels[:percent_20]): #Both exist but not equal
                  save_new_data_flag = 1
              else:
                  config_dict.update({'train_labels_path': newest_data_folder + '/train_labels.pkl'})
                  config_dict.update({'train_set_path': newest_data_folder + '/train_set.pkl'})
                  
      elif (~(os.path.exists(newest_data_folder + '/train_labels.pkl'))) and (len(train_labels) == 0): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/val_labels.pkl')) and (save_new_data_flag == 0) and (len(val_labels) > 0)):
          percent_20 = int((20/100)*len(val_labels))

          with open(newest_data_folder + '/val_labels.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], val_labels[:percent_20]):
                  save_new_data_flag = 1
              else:
                  config_dict.update({'val_labels_path': newest_data_folder + '/val_labels.pkl'})
                  config_dict.update({'val_set_path': newest_data_folder + '/val_set.pkl'})
                  
      elif ((~(os.path.exists(newest_data_folder + '/val_labels.pkl'))) and (save_new_data_flag == 0) and (len(val_labels) == 0)):
          pass
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_labels.pkl')) and (save_new_data_flag == 0) and (len(test_labels) > 0):
          percent_20 = int((20/100)*len(test_labels))

          with open(newest_data_folder + '/test_labels.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], test_labels[:percent_20]):
                  save_new_data_flag = 1
              else:
                  config_dict.update({'test_labels_path': newest_data_folder + '/test_labels.pkl'})
                  config_dict.update({'test_set_path': newest_data_folder + '/test_set.pkl'})
                  
      elif ((~(os.path.exists(newest_data_folder + '/test_labels.pkl'))) and (save_new_data_flag == 0) and (len(test_labels) == 0)):
          pass
      else:
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '_' + dataset_folder 

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)

      if len(train) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/train_set.pkl', 'wb') as f:
            dill.dump(train, f, protocol=4)
        config_dict.update({'train_set_path': current_dir+'/data/'+dataset_folder+'/train_set.pkl'})

      if len(val) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/val_set.pkl', 'wb') as f:
            dill.dump(val, f, protocol=4)
        config_dict.update({'val_set_path': current_dir+'/data/'+dataset_folder+'/val_set.pkl'})

      if len(test) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/test_set.pkl', 'wb') as f:
            dill.dump(test, f, protocol=4)
        config_dict.update({'test_set_path': current_dir+'/data/'+dataset_folder+'/test_set.pkl'})


      if len(train_labels) > 0:
        #train_unique, train_count = np.unique(train_labels, return_counts=True)
        #config_dict.update({'label_names_train': train_unique.tolist(), 'train_count':train_count.tolist()})
        with open(current_dir+'/data/'+dataset_folder+'/train_labels.pkl', 'wb') as f:
            dill.dump(train_labels, f, protocol=4)
        config_dict.update({'train_labels_path': current_dir+'/data/'+dataset_folder+'/train_labels.pkl'})

      if len(val_labels) > 0:
        #val_unique, val_count = np.unique(val_labels, return_counts=True)
        #config_dict.update({'label_names_val': val_unique.tolist(), 'val_count':val_count.tolist()})
        with open(current_dir+'/data/'+dataset_folder+'/val_labels.pkl', 'wb') as f:
            dill.dump(val_labels, f, protocol=4)
        config_dict.update({'val_labels_path': current_dir+'/data/'+dataset_folder+'/val_labels.pkl'})


      if len(test_labels) > 0:
        #test_unique, test_count = np.unique(test_labels, return_counts=True)
        #config_dict.update({'label_names_test': test_unique.tolist(), 'test_count':test_count.tolist()})
        with open(current_dir+'/data/'+dataset_folder+'/test_labels.pkl', 'wb') as f:
            dill.dump(test_labels, f, protocol=4)
        config_dict.update({'test_labels_path': current_dir+'/data/'+dataset_folder+'/test_labels.pkl'})

      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")


  config_dict.update({'library': 'NumPy'})
  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)

  #dataset_dict = config_dict



def torch_dataloader(train=None, val=None, test=None, dataset_name="dataset", label_index=1, if_sweep_save_once = True, run_id = None):

  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_data()")
    return

  global first_sweep_run
  train_labels_list = []


  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return

  config_dict = {}

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  dataset_name = dataset_name.replace("_", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"_"+dataset_name
  else:
      dataset_folder = "R"+str(run_id_global)+"_"+dataset_name

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')

  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('_')[-1] != dataset_name:
      save_new_data_flag = 1
  else:
      if (train != None) and (len(train) > 0) and (os.path.exists(newest_data_folder + '/train_dataloader.pkl')): #Both exist

          with open(newest_data_folder + '/train_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(train))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
              else:
                  config_dict.update({'train_dataloader_path': newest_data_folder + '/train_dataloader.pkl'})
      elif (~(os.path.exists(newest_data_folder + '/train_dataloader.pkl'))) and (train == None): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/val_dataloader.pkl')) and (save_new_data_flag == 0) and (val != None) and (len(val) > 0)):
          with open(newest_data_folder + '/val_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(val))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
              else:
                  config_dict.update({'val_dataloader_path': newest_data_folder + '/val_dataloader.pkl'})
      elif ((~(os.path.exists(newest_data_folder + '/val_dataloader.pkl'))) and (save_new_data_flag == 0) and (val == None)):
          pass
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_dataloader.pkl')) and (save_new_data_flag == 0) and (test != None) and (len(test) > 0):
          with open(newest_data_folder + '/test_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(test))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print(b1, b2)
                  save_new_data_flag = 1
              else:
                  config_dict.update({'test_dataloader_path': newest_data_folder +'/test_dataloader.pkl'})
      elif ((~(os.path.exists(newest_data_folder + '/test_dataloader.pkl'))) and (save_new_data_flag == 0) and (test == None)):
          pass
      else:
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '_' + dataset_folder

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)


      #print("To log the label count as an optional feature, the DataLoaders dataset should have a 'targets' attribute.")

      if train:
        '''
        if label_index:
            train_ds = train.dataset
            if hasattr(train_ds, 'targets'):
                train_labels_list = train_ds.targets
                print("Training labels count logged.")
        '''

        with open(current_dir+'/data/'+dataset_folder+'/train_dataloader.pkl', 'wb') as f:
            dill.dump(train, f, protocol=4)
        config_dict.update({'train_dataloader_path': current_dir+'/data/'+dataset_folder+'/train_dataloader.pkl'})

      if val:
        with open(current_dir+'/data/'+dataset_folder+'/val_dataloader.pkl', 'wb') as f:
            dill.dump(val, f, protocol=4)
        config_dict.update({'val_dataloader_path': current_dir+'/data/'+dataset_folder+'/val_dataloader.pkl'})

      if test:
        with open(current_dir+'/data/'+dataset_folder+'/test_dataloader.pkl', 'wb') as f:
            dill.dump(test, f,protocol=4)
        config_dict.update({'test_dataloader_path': current_dir+'/data/'+dataset_folder+'/test_dataloader.pkl'})


      ''''
      train_labels_list = np.array(train_labels_list)
      val_labels = np.array(val_labels)
      test_labels = np.array(test_labels)

      if len(train_labels_list) > 0:
        train_unique, train_count = np.unique(train_labels_list, return_counts=True)
        config_dict.update({'train_labels': train_unique.tolist(), 'train_count':train_count.tolist()})

      if len(val_labels) > 0:
        val_unique, val_count = np.unique(val_labels, return_counts=True)
        config_dict.update({'val_labels': val_unique.tolist(), 'val_count':val_count.tolist()})

      if len(test_labels) > 0:
        test_unique, test_count = np.unique(test_labels, return_counts=True)
        config_dict.update({'test_labels': test_unique.tolist(), 'test_count':test_count.tolist()})
      '''

      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")

  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  config_dict.update({'library': 'PyTorch'})

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)
  #dataset_dict = config_dict



def tf_dataset(train=None, val=None, test=None, dataset_name="dataset", label_index=1, if_sweep_save_once = True, run_id = None):


  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.tensorflow_data()")
    return

  global first_sweep_run
  train_labels_list = []


  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return

  config_dict = {}

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  dataset_name = dataset_name.replace("_", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"_"+dataset_name
  else:
      dataset_folder = "R"+str(run_id_global)+"_"+dataset_name


  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')

  if newest_data_folder == None:
      print("a")
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('_')[-1] != dataset_name:
      print("b")
      save_new_data_flag = 1
  else:
      if (train != None) and (len(train) > 0) and (os.path.exists(newest_data_folder + '/train_dataset.pkl')): #Both exist
          print("c")

          x = tf.data.Dataset.load(newest_data_folder + '/train_dataset.pkl')

          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in train:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'train_dataset_path': newest_data_folder + '/train_dataset.pkl'})
              
      elif (~(os.path.exists(newest_data_folder + '/train_dataset.pkl'))) and (train == None): #Both don't exist
          print("d")
          pass
      else: #One exists, one doesn't
          print("e")
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/val_dataset.pkl')) and (save_new_data_flag == 0) and (val != None) and (len(val) > 0)):
          print("f")

          x = tf.data.Dataset.load(newest_data_folder + '/val_dataset.pkl')
          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in val:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'val_dataset_path': newest_data_folder + '/val_dataset.pkl'})
              
      elif ((~(os.path.exists(newest_data_folder + '/val_dataset.pkl'))) and (save_new_data_flag == 0) and (val == None)):
          print("g")
          pass
      else:
          print("h")
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_dataset.pkl')) and (save_new_data_flag == 0) and (test != None) and (len(test) > 0):
          print("i")

          x = tf.data.Dataset.load(newest_data_folder + '/test_dataset.pkl')
          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in test:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'test_dataset_path': newest_data_folder + '/test_dataset.pkl'})
              
      elif ((~(os.path.exists(newest_data_folder + '/test_dataset.pkl'))) and (save_new_data_flag == 0) and (test == None)):
          print("j")
          pass
      else:
          print("k")
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '_' + dataset_folder

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)

      if train:
        tf.data.Dataset.save(train, current_dir+'/data/'+dataset_folder +'/train_dataset.pkl')
        config_dict.update({'train_dataset_path': current_dir+'/data/'+dataset_folder +'/train_dataset.pkl'})

      if val:
        tf.data.Dataset.save(val, current_dir+'/data/'+dataset_folder +'/val_dataset.pkl')
        config_dict.update({'val_dataset_path': current_dir+'/data/'+dataset_folder +'/val_dataset.pkl'})

      if test:
        tf.data.Dataset.save(test, current_dir+'/data/'+dataset_folder +'/test_dataset.pkl')
        config_dict.update({'test_dataset_path': current_dir+'/data/'+dataset_folder +'/test_dataset.pkl'})

      config_dict.update({'prev_saved_data': False})
      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")
      config_dict.update({'prev_saved_data': True})

  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  config_dict.update({'library': 'Tensorflow'})

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)


try:
  class MynacodeCallback(keras.callbacks.Callback):

      def __init__(self, metric_name, goal='maximize', track={}, run_id=None):

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          self.metric_name = metric_name
          self.goal = goal
          self.run_id = run_id
          self.best_model = None
          self.best_metric_value = 0
          self.best_metric_epoch = 0
          self.save_model = False
          self.track_config = track

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return


      def on_train_end(self, logs=None):

          global metric_values
          global index_count

          print("Model Directory: "+run_dir_global+'/model')

          index_count = 0
          metric_values = []


      def on_epoch_end(self, epoch, logs=None):
          global metric_values
          global index_count
          global prev_min
          global prev_max
          results_dict = {}


          if self.metric_name not in logs.keys():
            print(self.metric_name + ' not found in log keys')
            keys = list(logs.keys())
            print("End epoch {} of training; got log keys: {}".format(epoch, keys))
          else:
            metric_values.append(logs.get(self.metric_name))
            
            if self.goal == 'maximize':
              if logs.get(self.metric_name) > prev_max:
                prev_max = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'maximize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch+1})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                self.model.save(run_dir_global+'/model/best_model_chkpt.hdf5')
                
                with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
                  f.write('Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/model/best_model_chkpt.hdf5',
                                    'best_model_logs_path': run_dir_global+'/model/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)

            elif self.goal == 'minimize':
              if logs.get(self.metric_name) < prev_min:
                prev_min = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'minimize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch+1})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                self.model.save(run_dir_global+'/model/best_model_chkpt.hdf5')
                
                with open(run_dir_global+'/model/best_model_logs.txt', 'w') as f:
                  f.write('Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/model/best_model_chkpt.hdf5',
                                    'best_model_logs_path': run_dir_global+'/model/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)

            index_count += 1

except:
  pass


@suppress_warnings
def results(y_true = [], y_pred = [], threshold=0.5, results_dict = {}, problem_type = 'binary classification', run_id = None):


    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.results()")
      return

    if not run_id:
      run_id = run_id_global

    if len(y_true) != 0 and len(y_pred) != 0:

      y_pred = np.array(y_pred).flatten()
      y_true = np.array(y_true).flatten()

      zero_idx = np.where(y_true == 0)[0]
      one_idx = np.where(y_true == 1)[0]

      prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_pred, threshold)
      fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_pred)

      fpr_spaced, tpr_spaced = evenly_spaced_points(fpr, tpr, 500)

      hist_zero = plt.hist(y_pred[zero_idx].tolist(), bins=30)
      hist_zero_freq = hist_zero[0]
      hist_zero_bins = hist_zero[1]

      hist_one = plt.hist(y_pred[one_idx].tolist(), bins=30)
      hist_one_freq = hist_one[0]
      hist_one_bins = hist_one[1]

      binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'hist_zero_freq': hist_zero_freq.tolist(), 'hist_zero_bins': hist_zero_bins.tolist(),
              'hist_one_freq': hist_one_freq.tolist(), 'hist_one_bins': hist_one_bins.tolist(),'fpr': fpr_spaced, 'tpr': tpr_spaced,
              'threshold': round(threshold, 4)}

      results_dict.update(binary)

    data = {'run_id' : run_id, 'results_dict': str(results_dict), 'node_name': 'Results', 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")


def load_run(run_id = None):
    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.results()")
      return

    data = {'run_id' : run_id, 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/load_run', data=data)

    response_dict = ast.literal_eval(response.text)
    
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    
    return_dict = {}

    if 'dataset_library' in response_dict:

        if response_dict['dataset_library'] == 'NumPy':
            if 'train' in response_dict:
              with open(response_dict['train_set'], "rb") as file:
                  train = dill.load(file)
                  return_dict.update({'train_set': train})
                  
            if 'val' in response_dict:
              with open(response_dict['val_set'], "rb") as file:
                  val = dill.load(file)
                  return_dict.update({'val_set': val})
                  
            if 'test' in response_dict:
              with open(response_dict['test_set'], "rb") as file:
                  test = dill.load(file)
                  return_dict.update({'test_set': test})
                  
            if 'train_labels' in response_dict:
              with open(response_dict['train_labels'], "rb") as file:
                  train_labels = dill.load(file)
                  return_dict.update({'train_labels': train_labels})
                  
            if 'val_labels' in response_dict:
              with open(response_dict['val_labels'], "rb") as file:
                  val_labels = dill.load(file)
                  return_dict.update({'val_labels': val_labels})
                  
            if 'test_labels' in response_dict:
              with open(response_dict['test_labels'], "rb") as file:
                  test_labels = dill.load(file)
                  return_dict.update({'test_labels': test_labels})

        elif response_dict['dataset_library'] == 'PyTorch':
            if 'train_dataloader' in response_dict:
              with open(response_dict['train_dataloader'], "rb") as file:
                  train = dill.load(file)
                  return_dict.update({'train_dataloader': train})
                  
            if 'val_dataloader' in response_dict:
              with open(response_dict['val_dataloader'], "rb") as file:
                  val = dill.load(file)
                  return_dict.update({'val_dataloader': val})
                  
            if 'test_dataloader' in response_dict:
              with open(response_dict['test_dataloader'], "rb") as file:
                  test = dill.load(file)
                  return_dict.update({'test_dataloader': test})

        elif response_dict['dataset_library'] == 'Tensorflow':
            pass
        else:
            pass
          
    if 'model_library' in response_dict:
        
        if response_dict['model_library'] == 'PyTorch':
            model_statedict = torch.load(response_dict['best_model_statedict'])
            with open(response_dict['best_model_network'], "rb") as file:
                model_network = dill.load(file)
            return_dict.update({'best_model_statedict': model_statedict, 'best_model_network': model_network})
            
        elif response_dict['model_library'] == 'Keras':
            model = tf.keras.models.load_model(model_path)
            return_dict.update({'best_model': model})

    return return_dict
        

