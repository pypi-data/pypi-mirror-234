"""Example function defining for prompts from Sales Assistant project."""
import openai


# Example prompt structure
# You can drop the system part, but user part is a must.
# It only has 1 parameter so that it is easy to use with parallel requests.
async def summarize_customer_visits(input_dict):
    """Summarize customer visits."""
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that is working in sales department of a Logistics company.",
            },
            {
                "role": "user",
                "content": f"""\
            Extract important information from the provided data and summarize it with bullet points\
            in 200 or less words, without duplicates while keeping the order of the information provided\
            Include visit date information in all the summaries you have created\
            Output will be in {input_dict['language']}\
            information:\
             ```{input_dict['input_text']}```\
            Result:""",
            },
        ],
        # Temperature affects the randomness of the output. 0 means deterministic, 1 means random.
        temperature=0,
    )

    return completion.choices[0].message.content
