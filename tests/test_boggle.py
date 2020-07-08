from unittest import TestCase
from app import app ##how do I reference a parent directory in order to import the app module which is saved in the parent directory of the tests folder
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    #TODO -- write tests for every view function / feature!
    
    def setUp(self):
        """Function that runs before every test
        """

        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', response.session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_of_plays'))
            self.assertIn('<p>High Score:', response.data)  
            self.assertin('<p>Score:', response.data)
            self.assertin('Seconds Left:', response.data)
            
    def test_valid_word(self):
        """Test if word is valid by modifying the board in session"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.get_json['result'], 'ok')
        
    def test_invalid_word(self):
        """Test to see if word is in the dictionary text file"""
        
        self.client.get('/')
        response = self.client.get('/check-word?word=marlon')
        self.assertEqual(response.get_json['result'], 'not-on-board')    
    
    def test_non_english_word(self):
        """Test to see if word is on the board"""
        
        self.client.get('/')
        response = self.client.get('/check-word?word=jewhgfiujfdimd')
        self.assertEqual(response.get_json['result'], 'not-word')                                     
