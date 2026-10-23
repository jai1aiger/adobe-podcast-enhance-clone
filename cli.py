"""
Command-Line Interface for Local Speech Enhancement
Usage:
    python cli.py input.wav output.wav --engine resemble
    python cli.py input.wav output.wav --engine deepfilter
"""

import argparse
import sys
import torch
import torchaudio

def enhance_resemble(input_path, output_path, denoise_only=False):
    from resemble_enhance.enhancer.inference import enhance
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading {input_path} on {device}...")
    audio, sr = torchaudio.load(input_path)
    
    if sr != 44100:
        resampler = torchaudio.transforms.Resample(sr, 44100)
        audio = resampler(audio)
    
    print("Processing audio through neural vocoder...")
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
    print(f"Enhanced audio saved to: {output_path}")

def enhance_deepfilter(input_path, output_path):
    from df.enhance import enhance as df_enhance, init_df, load_audio, save_audio
    
    print("Initializing DeepFilterNet...")
    model, df_state, _ = init_df()
    audio, _ = load_audio(input_path, sr=df_state.sr())
    print("Denoising...")
    enhanced = df_enhance(model, df_state, audio)
    save_audio(output_path, enhanced, sr=df_state.sr())
    print(f"Cleaned audio saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Local Adobe Enhance Speech CLI")
    parser.add_argument("input", help="Path to input audio file (WAV/MP3)")
    parser.add_argument("output", help="Path to save enhanced audio")
    parser.add_argument("--engine", choices=["resemble", "deepfilter"], default="resemble", help="Enhancement engine")
    parser.add_argument("--denoise-only", action="store_true", help="Denoise only without vocal resynthesis")
    
    args = parser.parse_args()

    if args.engine == "resemble":
        enhance_resemble(args.input, args.output, args.denoise_only)
    elif args.engine == "deepfilter":
        enhance_deepfilter(args.input, args.output)

if __name__ == "__main__":
    main()
