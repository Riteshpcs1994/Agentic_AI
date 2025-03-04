


def sql_agent_query(user_query):
    prompt = f"""[INST]
    You are an expert SQL assistant. Your task is to generate SQL queries that work on an SQLite3 database based on the user-provided request.

    ### Database Schema:
    The database contains the following table schema:

    Employee Table:
    - employee_name (TEXT, NOT NULL): Name of the employee.
    - employee_email (TEXT, UNIQUE, NOT NULL): Email address of the employee.
    - org_name (TEXT): Organization name the employee works for.
    - designation (TEXT, NOT NULL): Job designation of the employee.
    - years_of_experience (REAL, NOT NULL): Total years of professional experience.
    - salary (REAL): Current salary of the employee.
    - location (TEXT): Work location of the employee.
    - hire_date (TEXT): Date of hiring.

    ### Task:
    Generate an **SQLite3-compatible SQL query** that fulfills the user's request. Follow these rules:
    1. Ensure the SQL query is **executable** and **optimized** for SQLite3.
    2. Do not include explanatory comments in the generated SQL.
    3. Do not modify the schema or add fields.
    4. If the user query cannot be translated into a valid SQL query, return an error message in the specified JSON format.

    ### Examples:

    User Query: Get the average salary of employees grouped by their job designation.
    {{
        "query": "SELECT designation, AVG(salary) AS average_salary FROM Employee GROUP BY designation;"
    }}

    User Query: Retrieve the names and email addresses of employees hired in the last 5 years.
    {{
        "query": "SELECT employee_name, employee_email FROM Employee WHERE hire_date >= DATE('now', '-5 years');"
    }}

    User Query: Invalid request that cannot be translated into SQL.
    {{
        "error": "The request cannot be translated into a valid SQL query."
    }}

    ### User Query:
    {user_query}

    ### Output Format:
    Provide the result in the following JSON format:

    {{
        "query": "<Generated SQL query>"
    }}

    OR (if the request cannot be translated into SQL):

    {{
        "error": "<Error message>"
    }}

    [/INST]"""
    return prompt

def classify_query(query):
    prompt = f"""[INST]
Classify this query into one of three categories:
1. General Query: Can be answered using general knowledge and reasoning without referencing any company-specific data.
2. Technical Query: Relates to project details, requiring access to the internal project database (e.g., techniques used, results, or project-specific knowledge).
3. Employee Details Query: Pertains to employee-related information (e.g., name, email, role, salary, location, designation, or hiring details) and requires consulting the company's employee database.

Return ONLY valid JSON in this format:
{{
    "query_type": "1|2|3",
    "reasoning": "brief explanation"
}}

Examples:
User Query: Which city has the highest average salary among employees?
Answer:
{{
    "query_type": "3",
    "reasoning": "The query requires analyzing the employee database to group employees by location and calculate the average salary."
}}

User Query: What is the latest AI technology trend?
Answer:
{{
    "query_type": "1",
    "reasoning": "The query is general and can be answered using general knowledge without requiring access to company data."
}}

User Query: What technologies were used in Project Alpha?
Answer:
{{
    "query_type": "2",
    "reasoning": "This query pertains to a specific project and requires checking the internal project database for details about the technologies used."
}}

User Query: How does economics work?
Answer:
{{
    "query_type": "1",
    "reasoning": "The query is general and can be answered using general knowledge without requiring access to company data."
}}

User Query: {query}
Answer:
[/INST]"""
    return prompt