import honeyhive

honeyhive.api_key = "YOUR_API_KEY"
honeyhive.openai.api_key = "OPENAI_API_KEY"


####################
# Generation and feedback examples
####################

# Create a task
task = honeyhive.create_task(
    task="Blog writer",
    description="Writing blog posts for users based on topic and tone",
)

# Create a prompt
prompt1 = honeyhive.create_prompt(
    task="Blog title writer",
    name="Blog title writer 1",
    description="First attempt at a blog title writer",
    prompt="Write a blog post about {topic} in the {tone} tone.",
    model="openai:text-davinci-003",
    hyperparameters={"max_tokens": 100, "temperature": 0.9},
    few_shot_examples=[
        {
            "topic": "weather",
            "tone": "informative",
            "completion": "Temperature is expected to be 90 degrees today.",
        },
        {
            "topic": "weather",
            "tone": "funny",
            "completion": "Going to the beach today? Don't forget your sunscreen!",
        },
    ],
)

# Call generations
generations = honeyhive.generate(
    task="Blog title writer",
    inputs=[
        {"topic": "weather", "tone": "informative"},
        {"topic": "weather", "tone": "funny"},
    ],
    # prompts=["Blog title writer 1"],
    best_of=2,
    metrics="LexicalDiversity",
)

# Proivde feedback on generations
honeyhive.feedback(
    generation_id=generations[0].generation_id,
    feedback={
        "user": "user1",
        "user_country": "USA",
        "rejected": False,
        "edited": True,
        "feedback": "This is a great blog post!",
        "final_version": "Temperature rises up to 90 degrees today.",
    },
)

# Look at generations
honeyhive.get_generations(
    task="Blog title writer",
    prompts=["Blog title writer 1", "Blog title writer 2"],
    start_date="2022-12-01",
    end_date="2021-12-03",
)

####################
# Evaluation examples
####################

# Upload a validation dataset to test over
dataset = honeyhive.create_dataset(
    task="Blog title writer",
    name="blog_title_test",
    description="Validation dataset for blog title writer",
    purpose="validation",
    data=open("blog_title_test.csv", "r").read(),
)

# Add a metric to test over
metric = honeyhive.create_metric(
    task="Blog title writer",
    name="IsPassive",
    code_snippet="""
    def is_passive_voice(sentence):
        import nltk
        from nltk import word_tokenize, pos_tag
        from nltk.corpus import wordnet as wn
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        passive = False
        # tokenize sentence
        tokens = word_tokenize(sentence)
        # tag sentence
        tagged = pos_tag(tokens)
        # check if verb is in passive form
        for i in range(len(tagged)):
            if tagged[i][1] == 'VBN':
                # check if verb is in passive form
                if tagged[i][0] == lemmatizer.lemmatize(tagged[i][0], wn.VERB):
                    passive = True
        # map True/False to 1/0
        return int(passive)
    """,
)

# import prompts needed for the task
blog_title_prompts = honeyhive.get_prompts(task="Blog title writer")

# run evaluation for the prompts on the dataset
test_results = honeyhive.evaluate(
    task="Blog title writer",
    prompts=[prompt.name for prompt in blog_title_prompts],
    dataset="blog_title_validation",
    metrics=["BLEU", "ROGUE", "METEOR", "IsPassive"],
)

print(test_results)

# output looks like:
# [
#   {
#     "prompt": "Blog title writer",
#     "dataset": "blog_title_validation",
#     "metrics": {
#       "BLEU": 0.5,
#       "ROGUE": 0.5,
#       "METEOR": 0.5,
#       "IsPassive": 0.5
#     }
#   },
#   ...
# ]

##################
# Fine tuning examples
##################

# get all generations for a task
generations = honeyhive.Completion(
    task="financial-statement-summarizer",
    start_date="2022-12-01",
    end_date="2022-12-31",
)

# filter generations where passive is true, user_country is US, lexical diversity is greater than 0.5
generations_df = pd.DataFrame(generations)
generations_df = generations_df[
    (generations_df["feedback"]["passive"] == True)
    & (generations_df["feedback"]["user_country"] == "US")
    & (generations_df["feedback"]["lexical_diversity"] > 0.5)
    & (generations_df["feedback"]["BLEU"] > 0.5)
]
generations_df = generations_df[["prompt", "generation"]]

# fine tune model on the filtered generations
fine_tuning_job = honeyhive.fine_tune(
    task="financial-statement-summarizer",
    generations=generations_df.to_dict("records"),
    model="openai:text-curie-001",
    hyperparameters={
        "learning_rate": 1e-5,
        "batch_size": 8,
        "epochs": 1,
        "max_length": 512,
    },
    strategy="SFT",
)

print(fine_tuning_job)
# output looks like:
# {
#   "job_id": "job_id",
#   "status": "running",
#   "task": "financial-statement-summarizer",
#   "model": "openai:text-curie-001",
#   "hyperparameters": {
#     "learning_rate": 1e-5,
#     "batch_size": 8,
#     "epochs": 1,
#     "max_length": 512
#   }
# }
