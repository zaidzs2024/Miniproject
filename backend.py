from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/voting_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)

# Define the Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

# Initialize the database
@app.before_request
def create_tables():
    db.create_all()

# API endpoint to get candidates
@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    candidate_list = [{'id': c.id, 'name': c.name, 'votes': c.votes} for c in candidates]
    return jsonify(candidate_list)

# API endpoint to cast a vote
@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    candidate_id = data.get('candidate_id')
    candidate = Candidate.query.get(candidate_id)

    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404

    # Increment the vote count
    candidate.votes += 1
    new_vote = Vote(candidate_id=candidate_id)
    db.session.add(new_vote)
    db.session.commit()

    return jsonify({'message': f'Vote cast for {candidate.name}'}), 200

if __name__ == '__main__':
    app.run(debug=True)



