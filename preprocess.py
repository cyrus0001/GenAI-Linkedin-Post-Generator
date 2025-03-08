import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

    enriched_posts = []

    for post in posts:
        # Fix encoding issues by removing or replacing invalid characters
        post["text"] = post["text"].encode("utf-8", "replace").decode("utf-8")

        metadata = extract_metadata(post["text"])
        post.update(metadata)
        enriched_posts.append(post)

    # Get unified tags mapping
    unified_tags = get_unified_tags(enriched_posts)

    # Replace tags with unified versions
    for post in enriched_posts:
        post["tags"] = list({unified_tags.get(tag, tag) for tag in post["tags"]})

    # Save processed data
    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)  # Ensure proper encoding


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract the number of lines, the language of the post, and relevant tags.

    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: "line_count", "language", and "tags".
    3. "tags" should be an array of up to three relevant text tags.
    4. Language should be one of: "English", "Hinglish", "Spanish", or "German".
       (Hinglish means a mix of Hindi and English)

    Here is the actual post:
    "{post}"
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.invoke(response)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse metadata.")

    return res


def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post["tags"])

    unique_tags_list = ", ".join(unique_tags)

    template = '''
    I will give you a list of tags. You need to unify them based on the following rules:

    1. Merge similar tags into broader categories.
       - Example: "Jobseekers", "Job Hunting" → "Job Search"
       - Example: "Motivation", "Inspiration", "Drive" → "Motivation"
       - Example: "Personal Growth", "Personal Development", "Self Improvement" → "Self Improvement"
       - Example: "Scam Alert", "Job Scam" → "Scams"

    2. Each tag should follow Title Case convention (e.g., "Job Search").
    3. Return a JSON object without a preamble.
    4. JSON structure: {{"Original Tag": "Unified Tag"}}

    Here is the list of tags:
    "{tags}"
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.invoke(response)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tags.")

    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
