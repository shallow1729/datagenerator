import subprocess
inp = open('sample.txt', 'r')
result = subprocess.check_output(['python3', 'gen_json.py', '-l', '10'], stdin=inp, text=True)
print(result)

