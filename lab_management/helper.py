from openai import OpenAI
import os
api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)



def generate_gpt_response(available_equipements,student_experiment):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant in a laboratory. Your task is to provide relevant equipment suggestions based on the student's experiment description."},
            {"role": "user", "content": f"Based on the following available equipment {available_equipements} and the student's experiment description {student_experiment}, please provide a list of relevant equipment that can assist the student in their experiment.*IF NO SCIENTIFIC EXPIREMENT GIVEN ACT LIKE A CHAT BOT* AND SUGGEST ONLY EQUIPEMENT THAT ARE AVAILABLE IF NOTHING AVAILABLE SAY IT"}
        ],
    )

    return completion.choices[0].message.content
