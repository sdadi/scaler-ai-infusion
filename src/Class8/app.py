import gradio as gr

from pipeline import process_exception
from session import daily_session


def submit_report(report: str, shipment_value: float, customer_tier: str):
    if shipment_value is None:
        raise gr.Error("Enter a shipment value.")
    try:
        result = process_exception(
            report, shipment_value, customer_tier, session=daily_session
        )
    except ValueError as error:
        raise gr.Error(str(error)) from error

    details = result["manager_note"] or result["customer_message"]
    return result, "\n".join(f"- {step}" for step in result["steps"]), details, daily_session.get_daily_log()


with gr.Blocks(title="Northwind Shipment Exception Desk") as demo:
    gr.Markdown("# Northwind Logistics | Shipment Exception Desk")
    with gr.Row():
        with gr.Column(scale=1):
            report_input = gr.Textbox(
                label="Exception report", lines=7, placeholder="Describe what happened to the shipment"
            )
            value_input = gr.Number(label="Shipment value (USD)", minimum=0, value=100)
            tier_input = gr.Radio(
                ["standard", "premium"], label="Customer tier", value="standard"
            )
            submit_button = gr.Button("Process exception", variant="primary")
        with gr.Column(scale=1):
            outcome_output = gr.JSON(label="Outcome")
            steps_output = gr.Markdown(label="Processing steps")
            response_output = gr.Textbox(label="Drafted response", lines=7, interactive=False)

    gr.Markdown("## Daily Triage Log")
    log_output = gr.JSON(label="Processed exceptions")
    summary_button = gr.Button("Generate Daily Summary")
    summary_output = gr.JSON(label="Daily summary")

    submit_button.click(
        submit_report,
        inputs=[report_input, value_input, tier_input],
        outputs=[outcome_output, steps_output, response_output, log_output],
    )
    summary_button.click(daily_session.generate_daily_summary, outputs=summary_output)


if __name__ == "__main__":
    demo.launch()