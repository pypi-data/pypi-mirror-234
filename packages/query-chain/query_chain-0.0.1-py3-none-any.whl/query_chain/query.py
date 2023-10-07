import hashlib
import pickle
import os
import logging

CHECKPOINT_DIR: str = "checkpoints"


def checkpoint(query_function):
    def wrapped_query_function(self, *args, **kwargs):

        # Hash the parameters.
        pickle_name = hashlib.sha256(str(args).encode() + str(kwargs).encode()).hexdigest()
        checkpoint_file = os.path.join(CHECKPOINT_DIR, f"{pickle_name}.pkl")

        # Check if the checkpoints directory exists.
        if not os.path.exists(CHECKPOINT_DIR):
            # Create the checkpoints directory.
            os.makedirs(CHECKPOINT_DIR)

        if os.path.exists(checkpoint_file):
            # Load the output from the checkpoint file.
            with open(checkpoint_file, "rb") as f:
                self.completion = pickle.load(f)

            # Log that the query was loaded from a checkpoint.
            logging.info(f"Query {self.prompt} loaded from checkpoint.")
        else:
            # Execute the query function and checkpoint the output.
            self.completion = query_function(self, *args, **kwargs)

            # Checkpoint the output.
            with open(checkpoint_file, "wb") as f:
                pickle.dump(self.completion, f)

            # Log that the query was completed successfully.
            logging.info(f"Query {self.prompt} completed successfully.")

        return self.completion

    return wrapped_query_function


class Query:
    def __init__(self, prompt, call, context=None):
        self.prompt = prompt
        self.call = call
        self.context = context
        self.completion = None

    @checkpoint
    def run(self, context=None):
        self.completion = self.call(self.prompt, context if context else self.context)
        return self.completion

    def json_output(self):
        return {
            "context": self.context,
            "prompt": self.prompt,
            "completion": self.completion
        }
