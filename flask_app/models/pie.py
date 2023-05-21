from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Pie:
    db_name = 'pies_derby'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO pies (name, filling, crust, user_id) VALUES ( %(name)s, %(filling)s, %(crust)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def get_pie_by_id(cls, data):
        query = "SELECT * FROM pies WHERE pies.id = %(pie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = """
            SELECT
                pies.id,
                pies.user_id,
                pies.name,
                pies.filling,
                pies.crust,
                users.first_name,
                users.last_name,
                COUNT(votes.pie_id) as votesNum
            FROM
                pies
            LEFT JOIN
                users ON pies.user_id = users.id
            LEFT JOIN
                votes ON pies.id = votes.pie_id
            GROUP BY
                pies.id
            ORDER BY
                votesNum DESC;"""
        results = connectToMySQL(cls.db_name).query_db(query)
        allPies = []
        if results:
            for pie in results:
                allPies.append(pie)
            return allPies
        return allPies

    @classmethod
    def get_user_pies(cls, data):
        query = "SELECT * FROM pies WHERE pies.user_id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        pies = []
        if results:
            for pie in results:
                pies.append(pie)
            return pies
        return pies

    @classmethod
    def update(cls, data):
        query = "UPDATE pies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pies WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def deleteAllVotes(cls, data):
        query = "DELETE FROM votes WHERE votes.pie_id = %(pies_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addVote(cls, data):
        query = "INSERT INTO votes (pie_id, user_id) VALUES ( %(pie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def unVote(cls, data):
        query = "DELETE FROM votes WHERE pie_id = %(pie_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_pie_voters(cls, data):
        query = "SELECT * from votes LEFT JOIN users on votes.user_id = users.id WHERE pie_id = %(pie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfVotes = []
        if results:
            for row in results:
                nrOfVotes.append(row['first_name'])
            return nrOfVotes
        return nrOfVotes

    @staticmethod
    def validate_pie(pie):
        is_valid = True
        
        if len(pie['name']) <= 0:
            flash('Pie Name should not be empty!', 'namePie')
            is_valid= False
        if len(pie['filling']) <= 0:
            flash('Pie Filling should not be empty!', 'fillingPie')
            is_valid= False
        if len(pie['crust']) <= 0:
            flash('Pie Crust should not be empty!', 'crustPie')
            is_valid= False
        return is_valid