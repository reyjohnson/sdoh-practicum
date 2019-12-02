import json

class Questionnaire:
    def __init__(self, serialized):
        self.name = ""
        self.title = ""
        self.status = ""
        self.meta = None
        self.code = None

        self.groups = []

        self.deserialize(serialized)

    def deserialize(self, serialized):
        self.name = serialized.get('name')
        self.title = serialized.get('title')
        self.status = serialized.get('status')
        self.meta = serialized.get('meta')
        self.code = serialized.get('code')

        self.groups = [QuestionGroup(x) for x in serialized.get('item')]

    def serialize(self):
        return {
            "name": self.name,
            "title": self.title,
            "status": self.status,
            "meta": self.meta,
            "code": self.code,
            "resourceType": "Questionnaire",
            "item": [x.serialize() for x in self.groups]
        }

    def generate_form(self):
        form_parts = [x.generate_form() for x in self.groups]
        return f'<form>{"".join(form_parts)}</form>'

    def generate_FHIR_submission(self):
        pass


class QuestionGroup:
    def __init__(self, serialized):
        self.code = None
        self.required = None
        self.link_id = None
        self.text = None

        self.questions = []

        self.deserialize(serialized)

    def deserialize(self, serialized):
        self.code = serialized.get('code')
        self.required = serialized.get('required')
        self.link_id = serialized.get('linkId')
        self.text = serialized.get('text')

        self.questions = [Question(x) for x in serialized.get('item')]

    def serialize(self):
        return {
            "type": "group",
            "code": self.code,
            "required": self.required,
            "linkID": self.link_id,
            "text": self.text,
            "item": [x.serialize() for x in self.questions]
        }

    def generate_form(self):
        form_parts = [x.generate_form() for x in self.questions]
        form_html = "".join(form_parts)
        return f"<fieldset>" \
               f"<legend>{self.text}</legend>" \
               f"{form_html}</fieldset>"


class Question:
    def __init__(self, serialized):
        self.text = ""
        self.type = None
        self.code = None
        self.extension = None
        self.required = None
        self.link_id = None

        self.answer_options = []
        self.answer = None

        self.deserialize(serialized)

    def deserialize(self, serialized):
        self.text = serialized.get('text')
        self.type = serialized.get('type')
        self.code = serialized.get('code')
        self.extension = serialized.get('extension')
        self.required = serialized.get('required')
        self.link_id = serialized.get('linkId')

        if serialized.get('answerOption') is not None:
            self.answer_options = [AnswerOption(x) for x in serialized.get('answerOption')]

    def serialize(self):
        return {
            "text": self.text,
            "type": self.type,
            "code": self.code,
            "extension": self.extension,
            "required": self.required,
            "linkID": self.link_id,
            "answerOption": [x.serialize() for x in self.answer_options]
        }

    def generate_form(self):
        html = None

        if self.type == 'string':
            html = f'{self.text}<br>' \
                   f'<input type="text"><br>'

        elif self.type == 'choice':
            html = f'{self.text}<br>' \
                   f'<select name="{self.link_id}">' \
                   f'{"".join([x.generate_form() for x in self.answer_options])}' \
                   f'</select>' \
                   f'<br>'

        elif self.type == 'decimal':
            html = f'{self.text}<br>' \
                   f'<input type="number"><br>'

        return html


class AnswerOption:
    def __init__(self, serialized):
        self.text_display = ""
        self.coded_value = ""

        self.deserialize(serialized)

    def deserialize(self, serialized):
        value_coding = serialized.get('valueCoding')
        self.text_display = value_coding.get('display')
        self.coded_value = value_coding.get('code')

    def serialize(self):
        return {
            "valueCoding": {
                "code": self.coded_value,
                "display": self.text_display
            }
        }

    def generate_form(self):
        return f'<option value="{self.coded_value}">{self.text_display}</option>'


QUESTIONNAIRE_FILE = 'PRAPAREquest.json'


def load_questionnaire(path=QUESTIONNAIRE_FILE):
    with open(path) as infile:
        serialized = json.load(infile)
    return Questionnaire(serialized)


if __name__ == '__main__':
    questionnaire = load_questionnaire()
    question_types = [x.type for x in [y for y in questionnaire.groups] for x in x.questions]
    # print(set(question_types))
    # print(questionnaire.serialize())
    print(questionnaire.generate_form())