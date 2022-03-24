from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


@app.route('/help', methods=['GET'])
def first_endpoint():
    return "This is the Flask project, connected to the educational database. \n" \
           "Contains endpoints as such:\n" \
           "/input_info - takes \'name\' and \'age\' params containing args. " \
           "The output is different, depending on the method chosen (GET, POST).\n" \
           "/db_create - Creates \'table\' in the database. Options available: car_color, car_speed, cars.\n" \
           "/insert_data - \n" \
           "/get_data - \n" \
           "/delete_data - "


@app.route('/input_info', methods=['POST', 'GET'])
def input_info():

    if request.method == 'POST':
        name = request.args.get('name')
        age = request.args.get('age')
        user_json = {'name' : name,
                     'age' : age}
        return jsonify(user_json)
    elif request.method == 'GET':
        name = request.args.get('name')
        age = request.args.get('age')
        user_list = [name, age]
        return jsonify(user_list)


conn = psycopg2.connect(dbname='qa_ddl_25_16',
                        user='user_25_16',
                        password='123',
                        host='159.69.151.133',
                        port='5056')

@app.route('/table_create', methods = ['POST'])
def table_create():
    cur = conn.cursor()

    if conn:
        create = request.args.get('create')
        if create == 'car_color':
            cur.execute('CREATE TABLE public.car_color (color_id serial PRIMARY KEY, color varchar)')
        elif create == 'car_speed':
            cur.execute('CREATE TABLE public.car_speed (speed_id serial PRIMARY KEY, max_speed integer)')
        elif create == 'cars':
            cur.execute('CREATE TABLE public.cars (id serial PRIMARY KEY, car_name varchar not null, '
                        'car_model varchar not null, color_id serial not null, '
                        'speed_id serial not null, '
                        'FOREIGN KEY (color_id) REFERENCES car_color (color_id), '
                        'FOREIGN KEY (speed_id) REFERENCES car_speed (speed_id))')

        conn.commit()
        cur.close()
        return 'Table '+create+' was successfully created'



@app.route('/insert_data', methods = ['POST'])
def insert_data():
    cur = conn.cursor()

    if conn:
        table = request.args.get('table')
        if table == 'car_color':
            color = request.args.get('color')
            if color == 'all':
                colors = ['White','Yellow','Blue','Red','Green','Black','Brown','Azure','Ivory','Teal','Silver','Purple',
                          'Navy blue','Pea green','Gray','Orange','Maroon','Charcoal','Aquamarine','Coral','Fuchsia',
                          'Wheat','Lime','Crimson','Khaki','Hot pink','Magenta','Olden','Plum','Olive','Cyan']
                for i in range(len(colors)):
                    cur.execute("""INSERT INTO car_color (color) VALUES (%s)""", (colors[i], ))
            else:
                cur.execute("""INSERT INTO car_color (color) VALUES (%s)""", (color, ))
        elif table == 'car_speed':
            speed = request.args.get('speed')
            if speed == 'all':
                speed_list = []
                speed = 180
                for i in range(30):
                    speed_list.append(speed)
                    speed += 5
                for i in range(len(speed_list)):
                    cur.execute("""INSERT INTO car_speed (max_speed) VALUES (%s)""", (speed_list[i], ))
            else:
                cur.execute("""INSERT INTO car_speed (max_speed) VALUES (%s)""", (speed, ))
        elif table == 'cars':
            name = request.args.get('car_name')
            model = request.args.get('car_model')
            color_id = request.args.get('color_id')
            speed_id = request.args.get('speed_id')
            cur.execute("""INSERT INTO cars (car_name, car_model, color_id, speed_id) VALUES (%s, %s, %s, %s)""",
                        (name, model, color_id, speed_id))
        cur.execute('SELECT * FROM '+table)
        s = cur.fetchall()
        print(s)
        # jcolor = {}
        # for i in s:
        #     jcolor[str(i[0])] = {'color' : i[1]}
        # print(jcolor)

        conn.commit()
        cur.close()
        return jsonify(s)

@app.route('/get_data', methods = ['GET'])
def get_data():
    cur = conn.cursor()
    if conn:
        table = request.args.get('table')
        limit = request.args.get('limit')
        cur.execute('SELECT * FROM '+table+' LIMIT '+limit)
        s = cur.fetchall()

        fresult = []
        if table == 'cars':
            for i in s:
                result = {'id' : i[0],
                          'brand' : i[1],
                          'model' : i[2],
                          'color_id' : i[3],
                          'speed_id': i[4]}
                fresult.append(result)
        elif table == 'car_color':
            for i in s:
                result = {'id' : i[0],
                          'car_color' : i[1]}
                fresult.append(result)
        elif table == 'car_speed':
            for i in s:
                result = {'id' : i[0],
                          'car_speed' : i[1]}
                fresult.append(result)

        print(fresult)
        conn.commit()
        cur.close()
        return jsonify(fresult)


@app.route('/delete_data', methods = ['DELETE'])
def delete_data():
    cur = conn.cursor()

    if conn:
        table = request.args.get('table')
        #if table == 'car_color':
        # if table == 'all':
        #     for i in ['cars', 'car_speed', 'car_color']:
        #         cur.execute('DROP TABLE '+i)
        #     conn.commit()
        #     cur.close()
        #     return 'Tables',i[0],i[1],i[2],'were successfully deleted'
        cur.execute('DROP TABLE '+table)
        # elif table == 'car_speed':
        #     cur.execute('DROP TABLE car_speed')
        # elif table == 'cars':
        #     cur.execute('DROP TABLE cars')


    conn.commit()
    cur.close()
    return 'Table '+table+' was successfully deleted'

# @app.route('', methods=[''])
# def alter_():