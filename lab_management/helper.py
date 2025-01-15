from openai import OpenAI

client = OpenAI(api_key="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")



def generate_gpt_response(available_equipements,student_experiment):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant in a laboratory. Your task is to provide relevant equipment suggestions based on the student's experiment description."},
            {"role": "user", "content": f"Based on the following available equipment {available_equipements} and the student's experiment description {student_experiment}, please provide a list of relevant equipment that can assist the student in their experiment.*IF NO SCIENTIFIC EXPIREMENT GIVEN ACT LIKE A CHAT BOT* AND SUGGEST ONLY EQUIPEMENT THAT ARE AVAILABLE IF NOTHING AVAILABLE SAY IT"}
        ],
    )

    return completion.choices[0].message.content