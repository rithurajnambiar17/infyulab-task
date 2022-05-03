import shutil
import os
from flask import Flask, render_template, request, send_from_directory
import cv2
import random

#first create the route
app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def main():
   return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result(): 
   vid_path = request.form.get('vid_path')
   output_path = request.form.get('output_path')

   if request.method == "POST":
      vidcap = cv2.VideoCapture(vid_path)
      success,image = vidcap.read()
      count = 0
      while success:
         cv2.imwrite(output_path + "/frame%d.jpg" % count, image)     # save frame as JPEG file      
         success,image = vidcap.read()
         count += 1
      ls = os.listdir(output_path)
      rand = random.choice(ls)
      result = output_path + '/' + rand
      src = result
      shutil.copy(src, app.static_folder)
      return render_template('result.html', result = rand)
   else:
      result = 'Some thing went wrong!!'
      return render_template('result.html', result=result)

if __name__ == '__main__':
   app.run(debug = True)