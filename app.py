from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"


boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show the board.
    """
    ##create and set up the game board
    board = boggle_game.make_board()  
    ##set up session variables
    session['board'] = board
    highscore = session.get("highscore", 0) ##get the highscore value for the "highscore" key, if there is none set, create a key and set the value to 0.
    num_of_plays = session.get("num_of_plays", 0)
    
    return render_template("index.html", board=board, highscore=highscore, num_of_plays=num_of_plays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary.
    """

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Get score, update number of plays, and update high score if record was broken
    """
    score = request.json["score"] ##How does this call work
    highscore = session.get("highscore", 0)
    
    ##Note the below code:
    num_of_plays = session.get("num_of_plays", 0)
    session['num_of_plays'] = num_of_plays + 1
    
    return jsonify(brokeRecord = score > highscore)
    