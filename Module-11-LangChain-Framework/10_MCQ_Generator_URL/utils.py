from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders import RecursiveUrlLoader

def read_data_from_url(url):
    try:
        loader = RecursiveUrlLoader(url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text)
        text = loader.load()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def get_table_data(quiz_str):
        #convert quiz from string to dictinary
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]

        #iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
