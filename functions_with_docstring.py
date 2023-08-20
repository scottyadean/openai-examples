def check_for_duplicate_links(path_to_new_content, links):
    """
 Checks for duplicate links in a given list of links.
 
 Parameters:
 path_to_new_content (Path): The path to the new content.
 links (list): A list of links.
 
 Returns:
 bool: True if a duplicate link is found, False otherwise.
 
     """
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def dataframe_to_database(df, table_name):
    """
 This function takes in a pandas dataframe and a table name as parameters and creates an in-memory sqlite database with the dataframe as a table.
 
 Parameters:
 df (pandas.DataFrame): The dataframe to be converted to a database table.
 table_name (str): The name of the table to be created in the database.
 
 Returns:
 engine (sqlalchemy.engine.base.Engine): The engine of the in-memory sqlite database.
 
     """
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


def execute_query(engine, query):
    """
 Executes a given query on a given engine and returns the result.
 
 Parameters:
 engine (sqlalchemy.engine.Engine): The engine to execute the query on.
 query (str): The query to execute.
 
 Returns:
 list: A list of tuples containing the result of the query.
 
     """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def grade(correct_answer_dict, answers):
    """
This function takes two arguments, a dictionary of correct answers and a dictionary of answers given by a student. It then compares the two dictionaries and returns a grade and a pass/fail message.

Parameters:
correct_answer_dict (dict): A dictionary of correct answers.
answers (dict): A dictionary of answers given by a student.

Returns:
A string containing the grade and a pass/fail message.

Example:
grade({'Q1': 'A', 'Q2': 'B', 'Q3': 'C'}, {'Q1': 'A', 'Q2': 'B', 'Q3': 'C'})

Returns:
"3 out of 3 correct! You achieved: 100 % : Passed!"
     """
    correct_answers = 0
    for question, answer in answers.items():
        if answer.upper() == correct_answer_dict[question].upper()[16]:
            correct_answers+=1
    grade = 100 * correct_answers / len(answers)

    if grade < 60:
        passed = "Not passed!"
    else:
        passed = "Passed!"
    return f"{correct_answers} out of {len(answers)} correct! You achieved: {grade} % : {passed}"


def handle_response(response):
    """
 This function takes in a response dictionary as an argument and returns a query string.
 
 Parameters:
 response (dict): A dictionary containing the response from a user.
 
 Returns:
 query (str): A query string.
 
 
 The function checks if the response text starts with a space and if so, it adds the word 'Select' to the beginning of the string. It then returns the query string.
     """
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query
