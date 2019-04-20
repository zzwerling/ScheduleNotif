from flask import Flask, request, render_template
import methods
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


def check_open_class():
    list = []

    with open('data.txt') as f:
        lines = f.read().splitlines()

    if not lines:
        return

    for l in lines:
        if methods.get_current_enrollment(l) > 0:

            methods.send_alert(l)
        else:
            list.append(l.strip())

    print(list)

    f.close()
    with open('data.txt', 'w') as f:
        for item in list:
            f.write("%s\n" % item)




scheduler = BackgroundScheduler()
scheduler.add_job(func=check_open_class, trigger="interval", seconds=15)
scheduler.start()


@app.route('/')
def render_page():

    return render_template('index.html')


@app.route('/submitform', methods=['POST'])
def submit_form():
    code = request.form['code']
    try:
        methods.get_current_enrollment(code)
        if (methods.get_current_enrollment(code) > 0):
            return ('That class is open')
        else:
            methods.write_data(code)
            return ('Success!')
    except ValueError:
        return ('Invalid code')

atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run()
