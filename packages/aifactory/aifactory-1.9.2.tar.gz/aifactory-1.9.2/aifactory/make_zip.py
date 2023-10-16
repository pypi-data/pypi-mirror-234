import os
import zipfile
import subprocess
import gdown
from IPython import get_ipython

def make_zip(key, main_name, func):
  run_type = 0
  main_filename = ''
  main_pyfilename = ''
  current_cwd = os.getcwd()  

  if '.py' not in main_name:
    run_type = 1

  if run_type == 1 and 'google.colab' in str(get_ipython()):
    print('Running on CoLab')
    run_type =2
  
  
  if run_type == 0: 
    print("python")
    main_filename = main_name
    main_pyfilename = main_name
  elif run_type == 1:     
    print("jupyter notebook")
    main_filename = main_name + '.ipynb'    
    pipes1 = subprocess.Popen(['jupyter','nbconvert', '--to','python', main_filename], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_out, std_err = pipes1.communicate()
    filename = os.path.splitext(main_filename)[0]  
    main_pyfilename = filename + '.py'
  elif run_type == 2: 
    print("google colab")
    #fileId=18s8l-9ONC8iXCke6RUPDEVKZl8OaX_Fo
    strs = main_name.split('=')

    ipynb_url = 'https://drive.google.com/uc?id=' + strs[1]
    main_filename = 'task.ipynb'
    output = '/content/' + main_filename
    gdown.download(ipynb_url, output)

    pipes1 = subprocess.Popen(['jupyter','nbconvert', '--to','python', main_filename], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_out, std_err = pipes1.communicate()
    filename = os.path.splitext(main_filename)[0]  
    main_pyfilename = filename + '.py'
  else: 
    print("not supported environments")
    return 
    
  pipes2 = subprocess.Popen(['pipreqs','--force', '--ignore', './drive,./train', './'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes2.communicate()
  
  with open("./requirements.txt", "r") as f:
    lines = f.readlines()
  with open("./requirements.txt", "w") as f:
    for line in lines:
      if 'aifactory' not in line:
        f.write(line)

  if run_type == 2:
    with open("./requirements.txt", "r") as f:
      lines = f.readlines()
    with open("./requirements.txt", "w") as f:
      for line in lines:
        if 'tensorflow' not in line:
          f.write(line)
        else:
          strs = line.split('+')
          f.write(strs[0])
          f.write('\n')
    
    with open("./requirements.txt", "r") as f:
      lines = f.readlines()
    with open("./requirements.txt", "w") as f:
      for line in lines:
        if 'torch' not in line:
          f.write(line)
        else:
          strs = line.split('+')
          f.write(strs[0])
          f.write('\n')
  
  zip_file = zipfile.ZipFile("./aif.zip", "w")  # "w": write 모드
  for (path, dir, files) in os.walk("./"):
    for file in files:        
      if "train" not in path and "drive" not in path and "sample_data" not in path and "aif.zip" not in file:
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()

  return main_pyfilename

def make_zip_train(key, main_name, func):
  run_type = 0
  main_filename = ''
  main_pyfilename = ''
  current_cwd = os.getcwd()  

  if '.py' not in main_name:
    run_type = 1

  if run_type == 1 and 'google.colab' in str(get_ipython()):
    print('Running on CoLab')
    run_type =2
  
  if run_type == 0: 
    print("python")
    main_filename = main_name
    main_pyfilename = main_name
  elif run_type == 1:     
    print("jupyter notebook")
    main_filename = main_name + '.ipynb'    
    pipes1 = subprocess.Popen(['jupyter','nbconvert', '--to','python', main_filename], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_out, std_err = pipes1.communicate()
    filename = os.path.splitext(main_filename)[0]  
    main_pyfilename = filename + '.py'
  elif run_type == 2: 
    print("google colab")
    #fileId=18s8l-9ONC8iXCke6RUPDEVKZl8OaX_Fo
    strs = main_name.split('=')

    ipynb_url = 'https://drive.google.com/uc?id=' + strs[1]
    main_filename = 'task.ipynb'
    output = '/content/' + main_filename
    gdown.download(ipynb_url, output)

    pipes1 = subprocess.Popen(['jupyter','nbconvert', '--to','python', main_filename], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_out, std_err = pipes1.communicate()
    filename = os.path.splitext(main_filename)[0]  
    main_pyfilename = filename + '.py'
  else: 
    print("not supported environments")
    return 
    
  pipes2 = subprocess.Popen(['pipreqs','--force', '--ignore', './drive,./train', './'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes2.communicate()
  
  with open("./requirements.txt", "r") as f:
    lines = f.readlines()
  with open("./requirements.txt", "w") as f:
    for line in lines:
      if 'aifactory' not in line:
        f.write(line)

  if run_type == 2:
    with open("./requirements.txt", "r") as f:
      lines = f.readlines()
    with open("./requirements.txt", "w") as f:
      for line in lines:
        if 'tensorflow' not in line:
          f.write(line)
        else:
          strs = line.split('+')
          f.write(strs[0])
          f.write('\n')
    
    with open("./requirements.txt", "r") as f:
      lines = f.readlines()
    with open("./requirements.txt", "w") as f:
      for line in lines:
        if 'torch' not in line:
          f.write(line)
        else:
          strs = line.split('+')
          f.write(strs[0])
          f.write('\n')
  
  zip_file = zipfile.ZipFile("./aif.zip", "w")  # "w": write 모드
  for (path, dir, files) in os.walk("./"):
    for file in files: 
      fname, ext = os.path.splitext(file)                   
      if "train" not in path and "data" not in path and "sample_data" not in path and "drive" not in path and "aif.zip" not in file and ".h5" not in ext and ".pth" not in ext :
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()

  return main_pyfilename
