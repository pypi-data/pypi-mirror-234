print("Loaded")
import subprocess
import os
import tkinter as tk

import Task
package_path = os.path.dirname(os.path.abspath(Task.__file__))
task_path = os.path.join(package_path, "Task")
print(task_path)

try:
    result = subprocess.run(['python', 'path/to/script.py'], capture_output=True, text=True, stderr=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    # The command returned a non-zero exit code
    with open('error.txt', 'w') as f:
        f.write(e.stderr)
else:
    # The command completed successfully
    # Do something with the output if necessary
    pass
time.wait(10000)
