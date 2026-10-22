import os
import torch
import subprocess
import scipy.io.wavfile as wavfile
from transformers import MusicgenForConditionalGeneration, AutoProcessor

GENRES = [
    {
        "id": "track_01",
        "title": "90mph Gales (Top of the Stack)",
        "genre": "UK Grime & Bassline",
        "bpm": "140 BPM",
        "filename": "adi_01_90mph_gales_starlink_grime.mp3",
        "prompt": "140 BPM aggressive UK grime instrumental, distorted 808 square-wave sub-bass, syncopated skippy hi-hats, hard acoustic kick, dark grime synth lead, London Bow sound, clash energy, studio master"
    },
    {
        "id": "track_02",
        "title": "868 Jeweller (Anti-Jam)",
        "genre": "UK Drill & 4x4 Bassline",
        "bpm": "142 BPM",
        "filename": "adi_02_868_jeweller_ajax_drill.mp3",
        "prompt": "142 BPM UK drill and northern Yorkshire 4x4 bassline hybrid, sliding 808 bass glides, fast triplet hi-hat rolls, dark minor piano chords, bouncy organ bass stabs, crisp punchy drums"
    },
    {
        "id": "track_03",
        "title": "ColorVu Evidence (250 Px/m)",
        "genre": "Melodic UK Rap & Road Wave",
        "bpm": "138 BPM",
        "filename": "adi_03_colorvu_evidence_cctv_rap.mp3",
        "prompt": "138 BPM melodic UK rap and afro-swing instrumental beat, warm electric guitar plucks, smooth sub-bass, bouncy percussion, warm Rhodes keys, radio hit production"
    },
    {
        "id": "track_04",
        "title": "Neon Perimeter (Night Patrol)",
        "genre": "80s Retro Synthwave",
        "bpm": "112 BPM",
        "filename": "adi_04_neon_perimeter_synthwave.mp3",
        "prompt": "112 BPM 80s retro synthwave, driving analog synth arpeggios, pulsing retro bassline, gated reverb snare, nostalgic brass synth pads, cinematic cyberpunk night drive atmosphere"
    },
    {
        "id": "track_05",
        "title": "Fiber Optic Groove",
        "genre": "Deep House & Club EDM",
        "bpm": "124 BPM",
        "filename": "adi_05_fiber_optic_groove_deephouse.mp3",
        "prompt": "124 BPM melodic deep house, pumping 4x4 kick drum, warm groovy sub-bassline, lush electric piano chords, vocal chops, crisp open hi-hats, Ibiza summer club sunset vibe"
    },
    {
        "id": "track_06",
        "title": "Holme Moss Chill (Field Memos)",
        "genre": "Lo-Fi Hip Hop & Chillhop",
        "bpm": "84 BPM",
        "filename": "adi_06_holme_moss_chill_lofi.mp3",
        "prompt": "84 BPM relaxing lo-fi hip hop beats, warm vintage Rhodes electric piano chords, vinyl crackle and hiss, lazy boom bap drum beat, smooth acoustic bassline, cozy rainy day vibe"
    },
    {
        "id": "track_07",
        "title": "Pennine Stone Acoustic",
        "genre": "Acoustic Indie & Britpop",
        "bpm": "115 BPM",
        "filename": "adi_07_pennine_stone_acoustic.mp3",
        "prompt": "115 BPM British indie rock and acoustic folk, chiming acoustic guitar strumming, melodic driving bass guitar, punchy live drum kit, warm uplifting melody, Manchester indie sound"
    }
]

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading MusicGen model on: {device}...")
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
    print("MusicGen initialized successfully!")

    os.makedirs("audio", exist_ok=True)
    os.makedirs("scratch_audio", exist_ok=True)

    sampling_rate = model.config.audio_encoder.sampling_rate

    for idx, item in enumerate(GENRES, 1):
        print(f"\n[{idx}/{len(GENRES)}] Generating {item['genre']} -> '{item['title']}'...")
        inputs = processor(
            text=[item["prompt"]],
            padding=True,
            return_tensors="pt"
        ).to(device)

        # Generate ~20-25 seconds of music (1000 new tokens)
        with torch.no_grad():
            audio_values = model.generate(**inputs, max_new_tokens=1000)

        raw_wav = f"scratch_audio/{item['id']}_raw.wav"
        audio_data = audio_values[0, 0].cpu().numpy()
        wavfile.write(raw_wav, rate=sampling_rate, data=audio_data)

        # Convert to pristine 320kbps MP3 with master volume normalization
        target_mp3 = os.path.join("audio", item["filename"])
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_wav,
            "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
            "-b:a", "320k",
            target_mp3
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f" -> Mastered & Saved: {target_mp3}")
        else:
            print(f" -> Error mastering {target_mp3}: {res.stderr}")

    print("\nALL 7 MULTI-GENRE STUDIO TRACKS GENERATED AT $0 TOKEN COST!")

if __name__ == "__main__":
    main()
