from flask import Flask, jsonify, request
import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432", # database
    database="flask_intro"
)

cur = connection.cursor()

# instantiating a class (Flask)
app = Flask(__name__)

# List (empty)
REMINDERS = []

# Decorator
@app.route("/")
# Function
def index():
    # Fetch all the reminders from the database
    cur.execute("SELECT * FROM reminders")
    
    # store in a variable
    reminder_data = cur.fetchall()  # 50% correct
    print(reminder_data)
    reminder_data = [{"title": item[0], "description": item[1]} for item in reminder_data ] # list comprehension
    # JSON ->
    return jsonify({"reminders": reminder_data})

@app.route("/reminders/<int:id>")
def reminder(id):
    print("@@@@@@")
    print(id)
    print("@@@@@@")
    
    cur.execute(f"SELECT * FROM reminders WHERE id = {id};")
    reminder_data = cur.fetchone()
    try:
        reminder_dict = {
            "id": id,
            "title": reminder_data[0],
            "description": reminder_data[1]
        }
        return jsonify(reminder_dict)
    except:
    
        return jsonify({'message': "Sorry something bad happened"})#500
    
    
    
    """
    # TODO: Exercise for the day (Submit on Tuesday):
    # Without using `pyscop2.extras.DictCursor`, make changes to the output variable `reminder_data`
    # to return the following - a list of dictionaries
    # Instead of {
    "reminders": [
        [
            "Mirjam is awesome",
            "She is learning to code"
        ],
        [
            "Eat",
            "Food is healthy"
        ],
        [
            "Exercise",
            "Get your heart moving"
        ]
        ]
    }
    
    Return the following:

    "reminders": [
            {
                "title": "Mirjam is awesome",
                "description": "She is learning to code"
            },
            {
                "title": "Eat",
                "description": "Food is healthy"
            },
            {
                "title": "Exercise",
                "description": "Get your heart moving"
            }
          ]
        }
    """
    # JSON ->
    return jsonify({"reminders": reminder_data})


# we want to store "reminders"
#
# GET
# POST
# DELETE
# PATCH
# PUT
# how do we save the reminders?

# Decorator -- URL path call add-reminder
@app.route("/add-reminder", methods=["POST"])
def add_reminder():
    try:
        title = request.json['title']
    except KeyError:
        title = None

    
        
        # handle the exception (error handling)   
    try:
        description = request.json['description']
    except KeyError:
        description = None
    # Null   
    print(f"INSERT INTO reminders (title, description) VALUES({title}, {description});")
    cur.execute(f"INSERT INTO reminders (title, description) VALUES('{title}', '{description}');")
    connection.commit()
    print(title, description)
    # change the return value from empty list to have REMINDERS instead
    return jsonify({"reminders": REMINDERS})


# Core HTTP verbs a developer must know
# - GET
# - POST
# - DELETE
# - PATCH
# DELETE
    """ 
    @app.route("/reminders/<int:id>", methods=['DELETE'])
    def delete_reminder(id):
    cur.execute(f"DELETE FROM reminders WHERE id={id};")
    commit the changes
    connection.commit()
return jsonify({"message": "Successfully deleted!"}) """
#UPDATE
    
@app.route("/reminders/<int:id>/update", methods=['PUT'])
def update_reminders(id):
    cur.execute(f"""
            UPDATE reminders
        SET title='{request.json.get('title')}', 
        description='{request.json.get('description')}'
        WHERE id={id}
    """)
    connection.commit()
    # Exercise: Return the updated information as a dictionary
    return jsonify(f"{'reminders':remainders_update},")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050) # port for flask