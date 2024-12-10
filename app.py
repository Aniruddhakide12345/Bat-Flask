from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\Coding\Projects\P2\batinfo(1).csv')
df['Player'] = df['Player'].str.lower()  

@app.route('/')
def home():
    return "Welcome to the Cricket Stats API! Navigate to /players to view all players or use other API routes."

@app.route('/player/<name>', methods=['GET'])
def get_player_info(name):
   
    player = df[df['Player'] == name.lower()]
    
    if player.empty:
        return jsonify({'error': 'Player not found'}), 404
    player_data = player.iloc[0].to_dict()
    return jsonify(player_data)

@app.route('/players', methods=['GET'])
def get_all_players():
    try:
        return jsonify(df['Player'].str.title().tolist())
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': 'Failed to fetch players list'}), 500

@app.route('/stats', methods=['POST'])
def get_player_stats():
    try:
        data = request.get_json()
        if 'name' not in data:
            return jsonify({'error': 'Please provide a player name'}), 400
        
        name = data['name']
        player = df[df['Player'] == name.lower()]
        
        if player.empty:
            return jsonify({'error': 'Player not found'}), 404
        stats = {
            'Player': str(player.iloc[0]['Player']).title(),
            'Span': str(player.iloc[0]['Span']),
            'Matches': int(player.iloc[0]['Mat']),
            'Innings': int(player.iloc[0]['Inns']),
            'Not_Outs': int(player.iloc[0]['NO']),
            'Runs': int(player.iloc[0]['Runs']),
            'Highest_Score': str(player.iloc[0]['HS']),
            'Average': float(player.iloc[0]['Ave']),
            'Balls_Faced': int(player.iloc[0]['BF']),
            'Strike_Rate': float(player.iloc[0]['SR']),
            'Centuries': int(player.iloc[0]['100']),
            'Half_Centuries': int(player.iloc[0]['50']),
            'Ducks': int(player.iloc[0]['0']),
            'Fours': int(player.iloc[0]['4s']),
            'Sixes': int(player.iloc[0]['6s'])
        }
        return jsonify(stats)
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': 'Failed to fetch player stats'}), 500

if __name__ == '__main__':
    app.run(debug=True)