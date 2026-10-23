"""
Adobe Podcast Enhance Speech - Local Web UI Clone
Powered by Resemble Enhance & DeepFilterNet with Gradio
"""

import os
import torch
import torchaudio
import gradio as gr

def process_audio(audio_path, engine, denoise_only):
    if audio_path is None:
        return None, "Please upload an audio file first."

    out_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(out_dir, f"{base_name}_enhanced.wav")

    try:
        if engine == "Resemble Enhance (Studio Vocoder)":
            from resemble_enhance.enhancer.inference import enhance
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            audio, sr = torchaudio.load(audio_path)
            
            if sr != 44100:
                resampler = torchaudio.transforms.Resample(sr, 44100)
                audio = resampler(audio)
            
            enhanced_audio, new_sr = enhance(
                audio[0],
                sr=44100,
                device=device,
                nfe=64 if not denoise_only else 1,
                solver="midpoint",
                lambd=0.9,
                tau=0.5
            )
            torchaudio.save(output_path, enhanced_audio.unsqueeze(0).cpu(), new_sr)
            return output_path, f"Enhanced successfully using Resemble Enhance ({device.upper()})."

        elif engine == "DeepFilterNet (Ultra-Fast CPU)":
            from df.enhance import enhance as df_enhance, init_df, load_audio, save_audio
            
            model, df_state, _ = init_df()
            audio, _ = load_audio(audio_path, sr=df_state.sr())
            enhanced = df_enhance(model, df_state, audio)
            save_audio(output_path, enhanced, sr=df_state.sr())
            return output_path, "Cleaned successfully using DeepFilterNet (CPU)."

        else:
            return None, "Unknown engine selected."

    except Exception as e:
        return None, f"Error processing audio: {str(e)}"

# Custom CSS matching Adobe Podcast clean studio aesthetics
custom_css = """
.gradio-container {
    max-width: 850px !important;
    margin: auto !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}
.title-header {
    text-align: center;
    margin-bottom: 25px;
}
"""

with gr.Blocks(title="Adobe Enhance Speech Clone", css=custom_css) as demo:
    gr.Markdown(
        """
        # 🎙️ Enhance Speech (Local Studio Sound)
        ### Clean-Room 100% Offline Replica of Adobe Podcast Enhance
        Upload raw, echoey, or noisy mic recordings and get broadcast-ready studio audio.
        """
    )
    
    with gr.Row():
        with gr.Column():
            input_audio = gr.Audio(label="Input Audio (Original)", type="filepath")
            
            engine_selector = gr.Radio(
                choices=["Resemble Enhance (Studio Vocoder)", "DeepFilterNet (Ultra-Fast CPU)"],
                value="Resemble Enhance (Studio Vocoder)",
                label="AI Enhancement Engine"
            )
            
            denoise_only_check = gr.Checkbox(
                label="Denoise Only (Skip neural high-frequency synthesis)",
                value=False
            )
            
            enhance_btn = gr.Button("✨ Enhance Speech", variant="primary")

        with gr.Column():
            output_audio = gr.Audio(label="Enhanced Audio (Studio Sound)", type="filepath")
            status_text = gr.Textbox(label="Status", interactive=False)

    enhance_btn.click(
        fn=process_audio,
        inputs=[input_audio, engine_selector, denoise_only_check],
        outputs=[output_audio, status_text]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
