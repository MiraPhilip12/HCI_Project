import pandas as pd
import os

class QuestionDatabase:
    def __init__(self):
        # Set absolute path to the folder where THIS file sits
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, 'questions.xlsx')
        self.load_database()
    
    def load_database(self):
        """Load data from the Excel file directly"""
        try:
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f"Missing: {self.db_path}")

            print(f"📖 Reading Excel: {self.db_path}")
            # Read all sheets into a dictionary
            excel_data = pd.read_excel(self.db_path, sheet_name=None)
            
            self.age_groups = excel_data['Age_Groups']
            self.subjects = excel_data['Subjects']
            self.questions = excel_data['Questions']
            
            print(f"✅ Database Loaded: {len(self.questions)} questions found.")
        except Exception as e:
            print(f"❌ DB Load Error: {e}")
            self.create_default_data()

    def create_default_data(self):
        """Emergency backup if Excel fails to load"""
        self.questions = pd.DataFrame([{
            'ID': 1, 'Age_Group_ID': 1, 'Subject_ID': 1, 
            'Question': 'What is 10 + 5?', 'Correct_Answer': '15', 
            'Options': '10|15|20|25', 'Type': 'multiple_choice', 'Hint': 'Add 5 to 10'
        }])

    def get_questions(self, age_id, sub_id):
        # Ensure numeric filtering
        mask = (self.questions['Age_Group_ID'].astype(int) == int(age_id)) & \
               (self.questions['Subject_ID'].astype(int) == int(sub_id))
        return self.questions[mask].to_dict('records')