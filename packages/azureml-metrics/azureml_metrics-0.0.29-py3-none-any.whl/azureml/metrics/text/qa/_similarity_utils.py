# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import logging

from typing import List, Callable, Any
from azureml.metrics.common.exceptions import MissingDependencies

try:
    from openai import InvalidRequestError
    import openai
    import openai.error
    from tenacity import (
        before_sleep_log,
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

except ImportError:
    safe_message = "Relevant GPT Star metrics packages are not available. " \
                   "Please run pip install azureml-metrics[prompt-flow]"
    raise MissingDependencies(
        safe_message, safe_message=safe_message
    )

logger = logging.getLogger(__name__)


def create_similarity_prompt(question: str, ground_truth: str, prediction: str) -> str:
    """
    Construct prompt using question, ground_truth and predicted sample for question answering.

    :param question: question used in question-answering task.
    :param ground_truth: example of ground truth.
    :param prediction: example of prediction to be evaluated.
    :param openai_params: Dictionary containing credentials for openai API.
    :return: string value of result obtained from openai API.
    """
    similarity_prompt = \
        'Equivalence, as a metric, measures the similarity between the predicted answer and the correct ' \
        'answer. If the information and content in the predicted answer is similar or equivalent to the ' \
        'correct answer, then the value of the Equivalence metric should be high, else it should be low. ' \
        'Given the question, correct answer, and predicted answer, determine the value of Equivalence ' \
        'metric using the following rating scale:\n' \
        'One star: the predicted answer is not at all similar to the correct answer\n' \
        'Two stars: the predicted answer is mostly not similar to the correct answer\n' \
        'Three stars: the predicted answer is somewhat similar to the correct answer\n' \
        'Four stars: the predicted answer is mostly similar to the correct answer\n' \
        'Five stars: the predicted answer is completely similar to the correct answer\n' \
        '\nThis rating value should always be an integer between 1 and 5. So the rating produced ' \
        'should be 1 or 2 or 3 or 4 or 5.' \
        '\n\nThe examples below show the Equivalence score for a question, a correct answer, ' \
        'and a predicted answer.'

    few_shot_text_qa = \
        '\n\n' \
        'question: What is the role of ribosomes?\n' \
        'correct answer: Ribosomes are cellular structures responsible for protein synthesis. They ' \
        'interpret the genetic information carried by messenger RNA (mRNA) and use it to assemble amino ' \
        'acids into proteins.\n' \
        'predicted answer: Ribosomes participate in carbohydrate breakdown by removing nutrients from ' \
        'complex sugar molecules.\n' \
        'stars: 1' \
        '\n\nquestion: Why did the Titanic sink?\n' \
        'correct answer: The Titanic sank after it struck an iceberg during its maiden voyage in 1912. The ' \
        'impact caused the ship\'s hull to breach, allowing water to flood into the vessel. The ship\'s ' \
        'design, lifeboat shortage, and lack of timely rescue efforts contributed to the tragic loss of life.\n' \
        'predicted answer: The sinking of the Titanic was a result of a large iceberg collision. This ' \
        'caused the ship to take on water and eventually sink, leading to the death of many passengers ' \
        'due to a shortage of lifeboats and insufficient rescue attempts.\n' \
        'stars: 2' \
        '\n\nquestion: What causes seasons on Earth?\n' \
        'correct answer: Seasons on Earth are caused by the tilt of the Earth\'s axis and its revolution ' \
        'around the Sun. As the Earth orbits the Sun, the tilt causes different parts of the planet to ' \
        'receive varying amounts of sunlight, resulting in changes in temperature and weather patterns.\n' \
        'predicted answer: Seasons occur because of the Earth\'s rotation and its elliptical orbit ' \
        'around the Sun. The tilt of the Earth\'s axis causes regions to be subjected to different ' \
        'sunlight intensities, which leads to temperature fluctuations and alternating weather conditions.\n' \
        'stars: 3' \
        '\n\nquestion: How does photosynthesis work?\n' \
        'correct answer: Photosynthesis is a process by which green plants and some other organisms ' \
        'convert light energy into chemical energy. This occurs as light is absorbed by chlorophyll ' \
        'molecules, and then carbon dioxide and water are converted into glucose and oxygen through a ' \
        'series of reactions.\n' \
        'predicted answer: In photosynthesis, sunlight is transformed into nutrients by plants and ' \
        'certain microorganisms. Light is captured by chlorophyll molecules, followed by the conversion ' \
        'of carbon dioxide and water into sugar and oxygen through multiple reactions.\n' \
        'stars: 4' \
        '\n\nquestion: What are the health benefits of regular exercise?\n' \
        'correct answer: Regular exercise can help maintain a healthy weight, increase muscle and bone ' \
        'strength, and reduce the risk of chronic diseases. It also promotes mental well-being by reducing ' \
        'stress and improving overall mood.\n' \
        'predicted answer: Routine physical activity can contribute to maintaining ideal body weight, ' \
        'enhancing muscle and bone strength, and preventing chronic illnesses. In addition, it supports ' \
        'mental health by alleviating stress and augmenting general mood.\n' \
        'stars: 5'

    prompt = \
        similarity_prompt + few_shot_text_qa + \
        '\n\nquestion: {}\ncorrect answer: {}\npredicted answer: {}\n' \
        'stars:'.format(question, ground_truth, prediction)

    return prompt


def create_coherence_prompt(question: str, prediction: str) -> str:
    """
    Construct prompt using question, context and predicted sample for question answering.

    :param question: question used in question-answering task.
    :param prediction: example of prediction to be evaluated.
    :param openai_params: Dictionary containing credentials for openai API.
    :return: star based metric based on coherence of answer.
    """
    coherence_prompt = \
        'Coherence of an answer is measured by how well all the sentences fit together and sound ' \
        'naturally as a whole. Consider the overall quality of the answer when evaluating coherence. ' \
        'Given the question and answer, score the coherence of answer between one to five stars using ' \
        'the following rating scale:\n' \
        'One star: the answer completely lacks coherence\n' \
        'Two stars: the answer mostly lacks coherence\n' \
        'Three stars: the answer is partially coherent\n' \
        'Four stars: the answer is mostly coherent\n' \
        'Five stars: the answer has perfect coherency\n' \
        '\nThis rating value should always be an integer between 1 and 5. So the rating produced should ' \
        'be 1 or 2 or 3 or 4 or 5.'

    few_shot_text_qa = \
        '\n\n' + \
        'question: What is your favorite indoor activity and why do you enjoy it?\n' \
        'answer: I like pizza. The sun is shining.\n' \
        'stars: 1' \
        '\n\nquestion: Can you describe your favorite movie without giving away any spoilers?\n' \
        'answer: It is a science fiction movie. There are dinosaurs. The actors eat cake. People must ' \
        'stop the villain.\n' \
        'stars: 2' \
        '\n\nquestion: What are some benefits of regular exercise?\n' \
        'answer: Regular exercise improves your mood. A good workout also helps you sleep better. Trees ' \
        'are green.\n' \
        'stars: 3' \
        '\n\nquestion: How do you cope with stress in your daily life?\n' \
        'answer: I usually go for a walk to clear my head. Listening to music helps me relax as well. ' \
        'Stress is a part of life, but we can manage it through some activities.\n' \
        'stars: 4' \
        '\n\nquestion: What can you tell me about climate change and its effects on the environment?\n' \
        'answer: Climate change has far-reaching effects on the environment. Rising temperatures result ' \
        'in the melting of polar ice caps, contributing to sea-level rise. Additionally, more frequent ' \
        'and severe weather events, such as hurricanes and heatwaves, can cause disruption to ecosystems ' \
        'and human societies alike.\n' \
        'stars: 5'

    prompt = \
        coherence_prompt + few_shot_text_qa + \
        '\n\nquestion: {}\nanswer: {}\nstars:'.format(question, prediction)

    return prompt


def create_relevance_prompt(context: str, question: str, prediction: str) -> str:
    """
    Construct prompt using question, context and predicted sample for question answering.

    :param context: context used in question-answering task.
    :param question: question used in question-answering task.
    :param prediction: example of prediction to be evaluated.
    :param openai_params: Dictionary containing credentials for openai API.
    :return: star based metric based on relevance of answer.
    """
    relevance_prompt = \
        'Relevance measures how well the answer addresses the main aspects of the question, ' \
        'based on the context. Consider whether all and only the important aspects are contained in the ' \
        'answer when evaluating relevance. Given the context and question, score the relevance of the ' \
        'answer between one to five stars using the following rating scale:\n' \
        'One star: the answer completely lacks relevance\n' \
        'Two stars: the answer mostly lacks relevance\n' \
        'Three stars: the answer is partially relevant\n' \
        'Four stars: the answer is mostly relevant\n' \
        'Five stars: the answer has perfect relevance\n' \
        '\nThis rating value should always be an integer between 1 and 5. So the rating produced ' \
        'should be 1 or 2 or 3 or 4 or 5.'

    few_shot_text_cqa = \
        '\n\n' \
        'context: Marie Curie was a Polish-born physicist and chemist who pioneered research on ' \
        'radioactivity and was the first woman to win a Nobel Prize.\n' \
        'question: What field did Marie Curie excel in?\n' \
        'answer: Marie Curie was a renowned painter who focused mainly on impressionist styles and ' \
        'techniques.\n' \
        'stars: 1' \
        '\n\ncontext: The Beatles were an English rock band formed in Liverpool in 1960, and they are ' \
        'widely regarded as the most influential music band in history.\n' \
        'question: Where were The Beatles formed?\n' \
        'answer: The band The Beatles began their journey in London, England, and they changed the ' \
        'history of music.\n' \
        'stars: 2' \
        '\n\ncontext: The recent Mars rover, Perseverance, was launched in 2020 with the main goal of ' \
        'searching for signs of ancient life on Mars. The rover also carries an experiment called MOXIE, ' \
        'which aims to generate oxygen from the Martian atmosphere.\n' \
        'question: What are the main goals of Perseverance Mars rover mission?\n' \
        'answer: The Perseverance Mars rover mission focuses on searching for signs of ancient ' \
        'life on Mars.\n' \
        'stars: 3' \
        '\n\ncontext: The Mediterranean diet is a commonly recommended dietary plan that emphasizes ' \
        'fruits, vegetables, whole grains, legumes, lean proteins, and healthy fats. Studies have shown ' \
        'that it offers numerous health benefits, including a reduced risk of heart disease and improved ' \
        'cognitive health.\n' \
        'question: What are the main components of the Mediterranean diet?\n' \
        'answer: The Mediterranean diet primarily consists of fruits, vegetables, whole grains, and ' \
        'legumes.\n' \
        'stars: 4' \
        '\n\ncontext: The Queen\'s Royal Castle is a well-known tourist attraction in the United ' \
        'Kingdom. It spans over 500 acres and contains extensive gardens and parks. The castle was ' \
        'built in the 15th century and has been home to generations of royalty.\n' \
        'question: What are the main attractions of the Queen\'s Royal Castle?\n' \
        'answer: The main attractions of the Queen\'s Royal Castle are its expansive 500-acre grounds, ' \
        'extensive gardens, parks, and the historical castle itself, which dates back to the 15th century ' \
        'and has housed generations of royalty.\n' \
        'stars: 5'

    prompt = \
        relevance_prompt + few_shot_text_cqa + \
        '\n\ncontext: {}\nquestion: {}\nanswer: {}\nstars:'.format(context, question, prediction)

    return prompt


def create_fluency_prompt(question: str, prediction: str) -> str:
    """
    Construct prompt using question, context and predicted sample for question answering.

    :param question: question used in question-answering task.
    :param prediction: example of prediction to be evaluated.
    :param openai_params: Dictionary containing credentials for openai API.
    :return: star based metric based on fluency of answer.
    """
    fluency_prompt = \
        'Fluency measures the quality of individual sentences in the answer, and whether they are ' \
        'well-written and grammatically correct. Consider the quality of individual sentences when' \
        ' evaluating fluency. Given the question and answer, score the fluency of the answer between ' \
        'one to five stars using the following rating scale:\n' \
        'One star: the answer completely lacks fluency\n' \
        'Two stars: the answer mostly lacks fluency\n' \
        'Three stars: the answer is partially fluent\n' \
        'Four stars: the answer is mostly fluent\n' \
        'Five stars: the answer has perfect fluency\n' \
        '\nThis rating value should always be an integer between 1 and 5. So the rating produced ' \
        'should be 1 or 2 or 3 or 4 or 5.'

    few_shot_text_qa = \
        '\n\n' + \
        'question: What did you have for breakfast today?\n' + \
        'answer: Breakfast today, me eating cereal and orange juice very good.\n' + \
        'stars: 1' + \
        '\n\nquestion: How do you feel when you travel alone?\n' + \
        'answer: Alone travel, nervous, but excited also. I feel adventure and like its time.\n' + \
        'stars: 2' + \
        '\n\nquestion: When was the last time you went on a family vacation?\n' + \
        'answer: Last family vacation, it took place in last summer. We traveled to a ' \
        'beach destination, very fun.\n' + \
        'stars: 3' + \
        '\n\nquestion: What is your favorite thing about your job?\n' + \
        'answer: My favorite aspect of my job is the chance to interact with diverse people. ' \
        'I am constantly learning from their experiences and stories.\n' + \
        'stars: 4' + \
        '\n\nquestion: Can you describe your morning routine?\n' + \
        'answer: Every morning, I wake up at 6 am, drink a glass of water, and do some light ' \
        'stretching. After that, I take a shower and get dressed for work. Then, I have a ' \
        'healthy breakfast, usually consisting of oatmeal and fruits, before leaving the ' \
        'house around 7:30 am.\n' + \
        'stars: 5'

    prompt = \
        fluency_prompt + few_shot_text_qa + \
        '\n\nquestion: {}\nanswer: {}\nstars:'.format(question, prediction)

    return prompt


def get_prediction(prompt_list: list, openai_params: dict, openai_api_batch_size: int = 20,
                   use_chat_completion_api: bool = None) -> List[str]:
    """
    Get prediction from openai API.

    :param prompt_list: constructed prompt for generating GPT similarity.
    :param openai_params: Dictionary containing credentials for openai API.
    :param openai_api_batch_size: number of prompts to be batched in one API call.
    :param use_chat_completion_api: boolean flag to choose between openAI completion vs chat completion API.
    """
    config_temperature = 0  # inorder to generate a deterministic result
    config_max_tokens = (
        1  # we need 1 token to produce the numerical output of score
    )

    results = []

    # updating the deployment_id if it's not set in openai_params
    if isinstance(openai_params, dict):
        if "deployment_id" not in openai_params.keys():
            openai_params["deployment_id"] = "gpt-35-turbo"
            logger.info("Using gpt-35-turbo for openai deployment_id as "
                        "deployment_id is not provided in openai_params")
        if "max_tokens" not in openai_params.keys():
            openai_params["max_tokens"] = config_max_tokens
        if "temperature" not in openai_params.keys():
            openai_params["temperature"] = config_temperature

        # retrieving the model name or deployment name when model is None
        model = openai_params.get("model", openai_params["deployment_id"])
    else:
        logger.warning("GPT related metrics need openai_params in a dictionary.")
        return results

    if use_chat_completion_api is None:
        if is_chat_completion_api(model):
            use_chat_completion_api = True
            # currently, batching is not supported in chat completion api.
            # so, setting the batch size to 1
            openai_api_batch_size = 1
        else:
            use_chat_completion_api = False

    for index in range(0, len(prompt_list), openai_api_batch_size):
        prompt_batch = list(prompt_list[index: index + openai_api_batch_size])
        # setting the prompt in openai params
        openai_params["prompt"] = prompt_batch

        # start and end index of batch to be used in case of exception
        batch_start_index = index
        batch_end_index = min(len(prompt_list), index + openai_api_batch_size)

        while True:
            try:
                api_output = completion_with_retry(
                    **openai_params
                )
                break

            except InvalidRequestError:
                logger.info("Content filter warning encountered. Going via single prompt "
                            "and skipping filtered results")
                api_output = {"choices": []}

                for row_index in range(batch_start_index, batch_end_index):
                    try:
                        cur_out = completion_with_retry(**openai_params)

                        if use_chat_completion_api:
                            predicted_result = cur_out["choices"][0]['message']['content']
                        else:
                            predicted_result = cur_out["choices"][0]["text"]

                        update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)

                    except InvalidRequestError as e:
                        predicted_result = e.__class__.__name__
                        logger.warning("Could not compute metric because of the following exception : " + str(e))
                        update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)
                break

            except Exception as e:
                api_output = {"choices": []}
                for row_index in range(batch_start_index, batch_end_index):
                    predicted_result = e.__class__.__name__
                    logger.warning("Could not compute metric because of the following exception : " + str(e))
                    update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)
                break

        # Collect predictions from response
        for row in api_output["choices"]:
            if use_chat_completion_api:
                predicted_result = row['message']['content']
            else:
                predicted_result = row["text"]

            result = predicted_result.strip().lower()
            results.append(result)

    return results


def is_chat_completion_api(model):
    """
    Check if we need openai chat completion or completion API for inference.

    :param model : model name to perform openai inference call.
    :return: True if we need to use chat-completion API.
    """
    # TODO : check if we need to update model_ids based on different endpoints.
    return model.startswith("gpt-35-turbo") or \
        model.startswith("gpt-3.5-turbo") or \
        model.startswith("gpt4") or \
        model.startswith("gpt-4")


def update_result(api_output, predicted_result, index, row_index, use_chat_completion_api):
    """
    Updating result based on structure of completion or chat completion API.
    """
    if use_chat_completion_api:
        current_result = {
            "message": {"content": predicted_result, "role": "system"},
            "index": row_index - index
        }
    else:
        current_result = {"text": predicted_result, "index": row_index - index}
    api_output["choices"].append(current_result)


def _create_retry_decorator() -> Callable[[Any], Any]:
    max_retries = 4
    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )


def completion_with_retry(**openai_params: Any) -> Any:
    """Use tenacity to retry the completion call.
    Copied from:
    https://github.com/hwchase17/langchain/blob/42df78d3964170bab39d445aa2827dea10a312a7/langchain/llms/openai.py#L98
    """
    retry_decorator = _create_retry_decorator()

    @retry_decorator
    def _completion_with_retry(**openai_params: Any) -> Any:
        # retrieving deployment_id if model is not present in openai parameters
        model = openai_params.get("model", openai_params["deployment_id"])

        if model.startswith("gpt-35-turbo") or model.startswith("gpt-3.5-turbo") \
                or model.startswith("gpt4") or model.startswith("gpt-4"):
            openai_params_chat_api = copy.deepcopy(openai_params)

            # hardcoded custom system prompt for all gpt-star metrics
            metrics_system_prompt = "You are an AI assistant. You will be given the definition of an " \
                                    "evaluation metric for assessing the quality of an answer in a " \
                                    "question-answering task. Your job is to compute an accurate evaluation " \
                                    "score using the provided evaluation metric."
            user_prompt = openai_params_chat_api['prompt'][0]
            messages = [{"role": "system", "content": metrics_system_prompt},
                        {"role": "user", "content": user_prompt}]
            openai_params_chat_api['messages'] = messages

            # deleting the prompt as we are adding messages
            del openai_params_chat_api['prompt']

            if 'best_of' in openai_params_chat_api:
                del openai_params_chat_api['best_of']

            return openai.ChatCompletion.create(**openai_params_chat_api)
        else:
            return openai.Completion.create(**openai_params)

    return _completion_with_retry(**openai_params)
