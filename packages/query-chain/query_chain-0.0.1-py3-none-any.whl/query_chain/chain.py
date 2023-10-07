import os
import json

from .query import Query

OUTPUT_DIR: str = "outputs"


class Chain:
    def __init__(self, name, llm, context=None, queries=None):
        self.name = name
        self.llm = llm
        self.context = context
        self.queries = queries if queries else []

    def add_prompt(self, prompt):
        self.add_prompt(prompt)

    def run(self):
        for query in self.queries:
            query.run()


class SequentialChain(Chain):

    def __init__(self, name, llm, context=None):
        super().__init__(name, llm, context)
        self.query_counter = 0

    def add_prompt(self, prompt):
        self.queries.append(Query(prompt, self.llm.call))
        self.query_counter += 1

    def run(self):

        # Check if the output directory exists.
        if not os.path.exists(OUTPUT_DIR):
            # Create the output directory.
            os.makedirs(OUTPUT_DIR)

        json_file_path = os.path.join(OUTPUT_DIR, f"{self.name}.json")

        # Write the JSON object to the file.
        output_json = {
            "name": self.name,
            "context:": self.context,
            "queries": {}
        }

        for i, query in enumerate(self.queries):
            result = query.run(self.context if i == 0 else self.queries[i - 1].context)
            query.context = result['new_context']
            output_json["queries"][i] = query.json_output()

        with open(json_file_path, "w") as f:
            json.dump(output_json, f, indent=4)
