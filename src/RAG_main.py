from RAG_llm_proxy import LlmProxy


def main():
    llmObj = LlmProxy("groq")

    prompt = f"""
    Answer the question: Which NFL team represented the AFC at Super Bowl 50?
    Using the context between <>, 
<
Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24u201310 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the "golden anniversary" with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as"Super Bowl L"), so that the logo could prominently feature the Arabic numerals 50.
>
    """
    response = llmObj.get_completion(prompt=prompt)

    print(response)

    prompt = f"""
    
    Rate from 0 to 100, the ground truth list of answers given by a language model: 
    Ground truth answers:
    Denver Broncos, 
    Denver Broncos, 
    Denver Broncos
    
    With the response given by a student.
    Response:
    {response}
    
    Rate the response considering if the student has included the ground truth answer. 
    More information provided by the student is not penalized.
    
  
    Only output a number from 0 to 100. Do not explain your output.
    """
    response = llmObj.get_completion(prompt=prompt)

    print(response)

    pass


if __name__ == "__main__":
    main()
