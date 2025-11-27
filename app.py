import gradio as gr
from scraper import fetch_and_convert
from llm_client import answer_query
from utils import setup_logger

logger = setup_logger()

markdown_cache = {}
chat_histories = {}


def load_url(url):
    if not url.strip():
        logger.warning("Empty URL submitted")
        return gr.update(visible=True), "", {}, "Please enter a valid URL"

    logger.info(f"Loading URL: {url}")
    url_hash, markdown = fetch_and_convert(url)
    markdown_cache[url_hash] = markdown
    chat_histories[url_hash] = []
    return url_hash, markdown, "Page loaded. You can ask questions..."


def ask_bot(history, user_msg, url_hash):
    if not user_msg:
        logger.info("Empty user message")
        return history, ""

    context = markdown_cache.get(url_hash, "")
    if not context:
        logger.warning("No context found for URL hash")
        return history, "No context loaded. Load a page first."

    answer = answer_query(context, user_msg)

    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": answer})
    return history, ""


def main():
    with gr.Blocks() as demo:
        gr.Markdown("<h1 style='text-align: center;'>⚔️ WebSlayer ⚔️</h1>")

        url_input = gr.Textbox(label="Enter a website URL")
        load_button = gr.Button("Load WebPage", variant="primary")
        state_hash = gr.State("")

        with gr.Column():
            with gr.Row(equal_height=True):
                msg_input = gr.Textbox(
                    show_label=False,
                    placeholder="Type your message here...",
                    container=False,
                    scale=9,
                )
                send_button = gr.Button("SEND", scale=1)
            chatbox = gr.Chatbot(
                type="messages", height=450, container=False, layout="bubble"
            )


        load_button.click(
            load_url, inputs=[url_input], outputs=[state_hash, msg_input, msg_input]
        )
        url_input.submit(
            load_url, inputs=[url_input], outputs=[state_hash, msg_input, msg_input]
        )

        send_button.click(
            ask_bot,
            inputs=[chatbox, msg_input, state_hash],
            outputs=[chatbox, msg_input],
        )

        msg_input.submit(
            ask_bot,
            inputs=[chatbox, msg_input, state_hash],
            outputs=[chatbox, msg_input],
        )

    demo.launch(share=True)


if __name__ == "__main__":
    main()
