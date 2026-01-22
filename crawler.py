import requests

URL = "https://wayground.com/_quizserver/main/v2/quiz/{}?convertQuestions=false&includeFsFeatures=true&sanitize=read&questionMetadata=true&includeUserHydratedVariants=true"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


class QuizCrawler:
    def __init__(self, quiz_id):
        self.quiz_id = quiz_id
        self.url = URL.format(quiz_id)
        self.questions = []
        self.title = ""
        self.total_questions = 0

    def fetch_quiz_data(self):
        try:
            response = requests.get(self.url, headers=HEADERS)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to fetch data: {response.status_code}")
        except Exception as e:
            print(f"Error fetching quiz data: {e}")
            return {}

    def parse_questions(self):
        data = self.fetch_quiz_data()
        if data.get("success"):
            self.title = data["data"]["quiz"]["info"]["name"]
            raw_questions = data["data"]["quiz"]["info"]["questions"]
            for idx, raw_question in enumerate(raw_questions):
                try:
                    questions_text = (
                        raw_question["structure"]["query"]["text"]
                        .replace("<p>", "")
                        .replace("</p>", "")
                    )
                    question_answer_idx = raw_question["structure"]["answer"]
                    questions_answer = (
                        raw_question["structure"]["options"][question_answer_idx][
                            "text"
                        ]
                        .replace("<p>", "")
                        .replace("</p>", "")
                    )
                    self.questions.append(
                        {"question": questions_text, "answer": questions_answer}
                    )
                except Exception as e:
                    print(f"Error parsing question {idx + 1}: {e}")
                    self.questions.append(
                        {"question": "Parsing Error", "answer": "N/A"}
                    )
            self.total_questions = len(self.questions)
        else:
            raise Exception("Unable to retrieve quiz data.")
