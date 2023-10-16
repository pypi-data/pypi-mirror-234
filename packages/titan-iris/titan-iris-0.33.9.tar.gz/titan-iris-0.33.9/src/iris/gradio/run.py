"""Module to run the gradio demo for inference."""

# ───────────────────────────────────────────────────── Imports ────────────────────────────────────────────────────── #
import os
import gradio as gr
from iris.sdk import iris_sdk


def sequence_classification_infer(text: str, runtime: str):
    """Function to run the sequence classification inference.

    Args:
        text (str): input text
        runtime (str): runtime engine

    Returns:
        list: label and score
    """
    url = os.getenv("IRIS_SDK_INFER_URL", "localhost:8000")
    task = "sequence_classification"
    text = [text]

    res_json = iris_sdk.infer(url=url, task_name=task, text=text, runtime=runtime)[0]

    label = res_json["label"]
    score = res_json["score"]

    return label, score


def pair_classification_infer(text1: str, text2: str, runtime: str):
    """Function to run the pair classification inference.

    Args:
        text1 (str): input text 1
        text2 (str): input text 2
        runtime (str): runtime engine

    Returns:
        list: label and score
    """
    url = os.getenv("IRIS_SDK_INFER_URL", "localhost:8000")
    task = "sequence_classification"
    text = [text1, text2]

    res_json = iris_sdk.infer(url=url, task_name=task, text=text, runtime=runtime)

    label = res_json["label"]
    score = res_json["score"]

    return label, score


def question_answering_infer(text: str, context: str, runtime: str):
    """Function to run the question answering inference.

    Args:
        text (str): input question
        context (str): input context
        runtime (str): runtime engine

    Returns:
        list: answer and score
    """
    url = os.getenv("IRIS_SDK_INFER_URL", "localhost:8000")
    task = "question_answering"

    text = [text]
    context = context
    res_json = iris_sdk.infer(url=url, task_name=task, text=text, context=context, runtime=runtime)

    answer = res_json["answer"]
    score = res_json["score"]
    return answer, score


with gr.Blocks() as demo:
    gr.Markdown("# Inference Demo Using the Triton Server: A Hands-On Demonstration")
    runtime = gr.Radio(
        ["onnx", "trt"],
        label="Runtime Engine",
        info="Choose the runtime engine for inference. (the runtime engine you serve the model in the triton server)",
    )

    with gr.Tab("Sequence Classification"):
        sc_input = gr.Textbox(label="Text", placeholder="Enter text here...")
        sc_button = gr.Button("Infer")
        with gr.Row():
            sc_label = gr.Textbox(label="Label")
            sc_score = gr.Textbox(label="Score")
    with gr.Tab("Pair Classification"):
        pc_input1 = gr.Textbox(label="Text1", placeholder="Enter text here...")
        pc_input2 = gr.Textbox(label="Text2", placeholder="Enter text here...")
        pc_button = gr.Button("Infer")
        with gr.Row():
            pc_label = gr.Textbox(label="Label")
            pc_score = gr.Textbox(label="Score")
    with gr.Tab("Question Answering"):
        qa_question = gr.Textbox(label="Question", placeholder="Enter text here...")
        qa_context = gr.Textbox(label="Context", placeholder="Enter text here...")

        qa_button = gr.Button("Infer")
        with gr.Row():
            qa_answer = gr.Textbox(label="Answer")
            qa_score = gr.Textbox(label="Score")
    gr.Markdown("\n")
    with gr.Accordion("Open for tutorial!", open=False):
        gr.Markdown("## Tutorial")
        gr.Markdown(
            "**Notice this is a demo for the inference server, so you need to serve the model in advance.**\n\
            You can refer to the TitanML Documentation for more details."
        )
        gr.Markdown(
            "Here we assume you have already pull the docker image from titanML website.\
            If not, please run the following command in your terminal."
        )
        gr.Markdown(
            """
        ```
        # pull a titan medium model
        iris pull <id_modelname>:M
        ```
        """
        )

        gr.Markdown("Then you can serve the model with the following command")
        gr.Markdown(
            """
        ```
        # deploy a titan medium model with triton 
        docker run --gpus all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v <mount_your_device> iris-triton-<id>:M
        ```
        """
        )
        gr.Markdown(
            "Following these steps, you can begin exploring the demo by clicking the `Infer` button! \n\
            **Please note that you can only use the model for specific tasks. For example, if your model \
                is trained on Sequence_classification, you can only perform Sequence_classification inferences here.**"
        )

        gr.Markdown("## Common Issues")
        gr.Markdown("1. check if you have installed the iris sdk")
        gr.Markdown("2. check if you expose the port from the docker container to your local machine")
        gr.Markdown("3. check if the model and task you are using is aligned with the model you serve")

    sc_button.click(sequence_classification_infer, inputs=[sc_input, runtime], outputs=[sc_label, sc_score])
    pc_button.click(pair_classification_infer, inputs=[pc_input1, pc_input2, runtime], outputs=[pc_label, pc_score])
    qa_button.click(question_answering_infer, inputs=[qa_question, qa_context, runtime], outputs=[qa_answer, qa_score])


def run(infer_url):
    """Main function to run the demo.

    Args:
        infer_url (str): url of the inference server(triton)
    """
    os.environ["IRIS_SDK_INFER_URL"] = infer_url
    demo.launch()


if __name__ == "__main__":
    # demo.launch()
    pass
