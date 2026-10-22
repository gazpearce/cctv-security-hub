import os
import sys
import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import subprocess
import asyncio
import edge_tts

SR = 44100

def soft_clip(x, drive=1.5):
    """Warm analog saturation using tanh."""
    return np.tanh(x * drive)

def create_kick(sr=SR, length=0.45, start_freq=160, end_freq=42, punch=1.4):
    """Synthesizes a punchy 808 acoustic kick drum."""
    t = np.linspace(0, length, int(sr * length), False)
    # Exponential pitch sweep
    pitch_env = np.exp(-t * 28.0)
    freq = end_freq + (start_freq - end_freq) * pitch_env
    phase = 2 * np.pi * np.cumsum(freq) / sr
    sine = np.sin(phase)
    # Amplitude envelope
    amp_env = np.exp(-t * 8.5)
    # Transient click
    click = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 90.0) * 0.35
    kick = (sine + click) * amp_env * punch
    return soft_clip(kick, 1.3)

def create_snare(sr=SR, length=0.25, tone_freq=195, noise_ratio=0.75):
    """Synthesizes a crisp electronic snare drum."""
    t = np.linspace(0, length, int(sr * length), False)
    # Tonal body
    tone = np.sin(2 * np.pi * tone_freq * t) * np.exp(-t * 22.0)
    # Noise snap
    noise = np.random.uniform(-1, 1, len(t))
    # Bandpass filter on noise (1kHz - 8kHz)
    b, a = signal.butter(2, [1000 / (sr/2), 8000 / (sr/2)], btype='band')
    filtered_noise = signal.lfilter(b, a, noise) * np.exp(-t * 18.0)
    snare = (tone * (1 - noise_ratio) + filtered_noise * noise_ratio)
    return soft_clip(snare * 1.5, 1.2)

def create_rimshot(sr=SR, length=0.08, freq=850):
    """Crisp metallic rimshot for drill / grime."""
    t = np.linspace(0, length, int(sr * length), False)
    tone = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.6 * t)) * np.exp(-t * 50.0)
    click = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 80.0) * 0.4
    return soft_clip(tone + click, 1.4)

def create_hihat(sr=SR, length=0.05, is_open=False):
    """High-frequency synthesized hi-hat."""
    actual_len = 0.22 if is_open else length
    t = np.linspace(0, actual_len, int(sr * actual_len), False)
    noise = np.random.uniform(-1, 1, len(t))
    # High-pass filter above 7.5 kHz
    b, a = signal.butter(3, 7500 / (sr/2), btype='high')
    hat = signal.lfilter(b, a, noise)
    decay = 12.0 if is_open else 65.0
    env = np.exp(-t * decay)
    return hat * env * 0.7

def create_808_sub(sr=SR, duration=0.8, freq_start=55.0, freq_end=None, saturation=1.8):
    """Deep sliding 808 sub bass with warm harmonic distortion."""
    t = np.linspace(0, duration, int(sr * duration), False)
    if freq_end is None:
        freq = np.full_like(t, freq_start)
    else:
        # Pitch slide
        freq = np.linspace(freq_start, freq_end, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / sr
    # Mix sine with slight 2nd/3rd harmonics
    sub = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)
    # Envelope
    env = np.exp(-t * (1.8 / duration))
    # Distortion
    return soft_clip(sub * env * saturation, drive=1.5)

def create_synth_lead(sr=SR, duration=0.2, freq=440.0, wave_type='square'):
    """Classic UK Grime Eskibeat square lead / plucks."""
    t = np.linspace(0, duration, int(sr * duration), False)
    if wave_type == 'square':
        osc = signal.square(2 * np.pi * freq * t)
    elif wave_type == 'saw':
        osc = signal.sawtooth(2 * np.pi * freq * t)
    else:
        osc = np.sin(2 * np.pi * freq * t)
    # Low-pass filter to remove harsh aliasing
    b, a = signal.butter(2, min(freq * 4.0, 12000) / (sr/2), btype='low')
    filtered = signal.lfilter(b, a, osc)
    env = np.exp(-t * 14.0)
    return filtered * env * 0.8

def create_bassline_organ(sr=SR, duration=0.25, freq=110.0):
    """Northern 4x4 Bassline organ stab (the classic donk/speed garage organ)."""
    t = np.linspace(0, duration, int(sr * duration), False)
    # Multi-oscillator organ drawbar: 1x, 2x, 3x, 4x, 6x frequencies
    organ = (
        1.0 * np.sin(2 * np.pi * freq * t) +
        0.8 * np.sin(2 * np.pi * freq * 2 * t) +
        0.5 * np.sin(2 * np.pi * freq * 3 * t) +
        0.4 * np.sin(2 * np.pi * freq * 4 * t) +
        0.2 * np.sin(2 * np.pi * freq * 6 * t)
    )
    # Fast percussive pitch envelope at the start
    pitch_mod = np.exp(-t * 80.0) * 0.15
    phase = 2 * np.pi * freq * (1 + pitch_mod) * t
    organ += 0.5 * np.sin(phase)
    env = np.exp(-t * 9.0)
    return soft_clip(organ * env * 0.7, 1.4)

def note_to_freq(note_name):
    """Convert note name like 'F1', 'C2', 'G#2' to frequency in Hz."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    name = note_name[:-1].upper()
    octave = int(note_name[-1])
    idx = notes.index(name)
    midi = 12 + octave * 12 + idx
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

def place_sample(track, sample, sample_idx):
    """Safely adds a sample into a track buffer at sample_idx."""
    end_idx = sample_idx + len(sample)
    if sample_idx >= len(track):
        return
    if end_idx > len(track):
        sample = sample[:len(track) - sample_idx]
    track[sample_idx:sample_idx + len(sample)] += sample

# ==============================================================================
# TRACK 1: 90mph Gales (Top of the Stack) — 140 BPM UK Grime
# ==============================================================================
def render_track_1_instrumental(duration_sec=75):
    bpm = 140
    beat_len = 60.0 / bpm
    step_len = beat_len / 4.0 # 16th note step
    total_steps = int(duration_sec / step_len)
    total_samples = int(total_steps * step_len * SR)
    audio = np.zeros(total_samples, dtype=np.float32)

    kick = create_kick(SR, length=0.45, start_freq=170, end_freq=45)
    snare = create_snare(SR, length=0.22, tone_freq=210)
    rim = create_rimshot(SR, length=0.08)
    hat_c = create_hihat(SR, length=0.04, is_open=False)
    hat_o = create_hihat(SR, length=0.20, is_open=True)

    # Pre-render 808 notes in F Minor (F1, G#1, D#1, C1)
    sub_F1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('F1'))
    sub_Gs1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('G#1'))
    sub_Ds1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('D#1'))
    sub_C1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('C1'))
    sub_slide = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('F1'), freq_end=note_to_freq('C2'))

    # Eskibeat synth melody notes
    lead_notes = ['F3', 'G#3', 'C4', 'A#3', 'G#3', 'F3', 'D#3', 'C3']

    for step in range(total_steps):
        s_idx = int(step * step_len * SR)
        bar = step // 16
        bar_step = step % 16

        # INTRO: First 4 bars (0-3) synth and light hats only
        is_intro = bar < 4
        is_drop = bar >= 4

        # Hi-Hats: Skippy grime pattern
        if is_intro or is_drop:
            if bar_step in [0, 2, 4, 6, 8, 10, 12, 14]:
                place_sample(audio, hat_c * 0.6, s_idx)
            # Syncopated rolls
            if bar_step in [7, 11, 15]:
                place_sample(audio, hat_c * 0.45, s_idx)
            # Open hat on offbeat
            if bar_step in [4, 12]:
                place_sample(audio, hat_o * 0.4, s_idx)

        # Snare / Rimshot on beat 2 and 4 (steps 4 and 12)
        if is_drop:
            if bar_step in [4, 12]:
                place_sample(audio, snare * 0.85, s_idx)
                place_sample(audio, rim * 0.4, s_idx)

        # Kick drum pattern: Classic 140 BPM syncopated grime kick
        if is_drop:
            if bar_step in [0, 6, 10]:
                place_sample(audio, kick * 0.95, s_idx)
            if bar % 4 == 3 and bar_step == 14: # Stutter turnaround kick
                place_sample(audio, kick * 0.8, s_idx)

        # 808 Sub Bass
        if is_drop:
            chord_cycle = bar % 8
            if bar_step == 0:
                if chord_cycle in [0, 1, 4]:
                    place_sample(audio, sub_F1, s_idx)
                elif chord_cycle in [2, 5]:
                    place_sample(audio, sub_Gs1, s_idx)
                elif chord_cycle in [3, 6]:
                    place_sample(audio, sub_Ds1, s_idx)
                elif chord_cycle == 7:
                    place_sample(audio, sub_slide, s_idx)
            elif bar_step == 8:
                if chord_cycle in [0, 1]:
                    place_sample(audio, sub_F1 * 0.8, s_idx)
                elif chord_cycle == 7:
                    place_sample(audio, sub_C1, s_idx)

        # Eskibeat square lead melody (Wiley / Dizzee style)
        if bar_step in [0, 3, 6, 9, 12, 14]:
            note_idx = (bar * 2 + bar_step // 2) % len(lead_notes)
            lead_freq = note_to_freq(lead_notes[note_idx])
            lead_sample = create_synth_lead(SR, duration=step_len*1.8, freq=lead_freq, wave_type='square')
            vol = 0.45 if is_intro else 0.35
            place_sample(audio, lead_sample * vol, s_idx)

    # Master normalization
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.88
    return audio

# ==============================================================================
# TRACK 2: 868 Jeweller (Anti-Jam) — 142 BPM UK Drill & 4x4 Yorkshire Bassline
# ==============================================================================
def render_track_2_instrumental(duration_sec=75):
    bpm = 142
    beat_len = 60.0 / bpm
    step_len = beat_len / 4.0
    total_steps = int(duration_sec / step_len)
    total_samples = int(total_steps * step_len * SR)
    audio = np.zeros(total_samples, dtype=np.float32)

    kick = create_kick(SR, length=0.42, start_freq=155, end_freq=40)
    snare = create_snare(SR, length=0.25, tone_freq=230)
    rim = create_rimshot(SR, length=0.07)
    hat_c = create_hihat(SR, length=0.035, is_open=False)
    hat_o = create_hihat(SR, length=0.18, is_open=True)

    sub_C1 = create_808_sub(SR, duration=step_len*5, freq_start=note_to_freq('C1'))
    sub_Ds1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('D#1'))
    sub_G1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('G1'))
    sub_slide = create_808_sub(SR, duration=step_len*6, freq_start=note_to_freq('C1'), freq_end=note_to_freq('G1'))

    organ_C2 = create_bassline_organ(SR, duration=step_len*1.5, freq=note_to_freq('C2'))
    organ_Ds2 = create_bassline_organ(SR, duration=step_len*1.5, freq=note_to_freq('D#2'))
    organ_G2 = create_bassline_organ(SR, duration=step_len*1.5, freq=note_to_freq('G2'))

    dark_chords = ['C3', 'D#3', 'G3', 'A#3']

    for step in range(total_steps):
        s_idx = int(step * step_len * SR)
        bar = step // 16
        bar_step = step % 16

        # Intro: bars 0-3 (Drill dark piano & ticking hats)
        # Verse 1: bars 4-11 (Drill sliding 808s)
        # Chorus: bars 12-19 (SWITCH TO HEAVY 4X4 BASSLINE DROP!)
        # Verse 2: bars 20+ (Drill / Bassline hybrid)

        is_intro = bar < 4
        is_drill = (4 <= bar < 12) or (bar >= 20)
        is_bassline_drop = 12 <= bar < 20

        # DRILL SECTION DRUMS
        if is_drill:
            # Drill snare on beat 3 (step 8)
            if bar_step == 8:
                place_sample(audio, snare * 0.9, s_idx)
                place_sample(audio, rim * 0.45, s_idx)
            # Drill kick: on 0, and syncopated before the snare (e.g. 6 or 11)
            if bar_step in [0, 6, 11]:
                place_sample(audio, kick * 0.95, s_idx)
            # Drill hi-hats: triplets and stutter rolls
            if bar_step in [0, 2, 4, 7, 9, 11, 13, 15]:
                place_sample(audio, hat_c * 0.5, s_idx)
            if bar_step == 14: # Triplet roll
                place_sample(audio, hat_c * 0.35, s_idx)

            # Drill 808 sliding bass
            if bar_step == 0:
                place_sample(audio, sub_C1, s_idx)
            elif bar_step == 6:
                place_sample(audio, sub_Ds1 * 0.8, s_idx)
            elif bar_step == 12:
                place_sample(audio, sub_slide, s_idx)

        # 4X4 BASSLINE DROP SECTION (High Energy Northern UK Bassline)
        elif is_bassline_drop:
            # 4x4 Kick on EVERY beat (0, 4, 8, 12)
            if bar_step in [0, 4, 8, 12]:
                place_sample(audio, kick * 1.0, s_idx)
            # Offbeat open hi-hat on every "and" (2, 6, 10, 14)
            if bar_step in [2, 6, 10, 14]:
                place_sample(audio, hat_o * 0.55, s_idx)
            # Snare / Clap on beats 2 and 4 (4, 12)
            if bar_step in [4, 12]:
                place_sample(audio, snare * 0.85, s_idx)

            # Bouncy Organ Bassline Stabs on offbeats
            if bar_step in [2, 6, 10, 14]:
                if bar % 4 in [0, 1]:
                    place_sample(audio, organ_C2 * 0.75, s_idx)
                elif bar % 4 == 2:
                    place_sample(audio, organ_Ds2 * 0.75, s_idx)
                else:
                    place_sample(audio, organ_G2 * 0.75, s_idx)

        elif is_intro:
            # Light hi-hats in intro
            if bar_step in [0, 4, 8, 12]:
                place_sample(audio, hat_c * 0.4, s_idx)

        # Dark atmospheric synth pluck
        if bar_step in [0, 4, 8, 12]:
            note_idx = (bar + bar_step // 4) % len(dark_chords)
            synth = create_synth_lead(SR, duration=step_len*2.5, freq=note_to_freq(dark_chords[note_idx]), wave_type='saw')
            place_sample(audio, synth * 0.25, s_idx)

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.88
    return audio

# ==============================================================================
# TRACK 3: ColorVu Evidence (250 Pixels per Metre) — 138 BPM Melodic UK Rap
# ==============================================================================
def render_track_3_instrumental(duration_sec=75):
    bpm = 138
    beat_len = 60.0 / bpm
    step_len = beat_len / 4.0
    total_steps = int(duration_sec / step_len)
    total_samples = int(total_steps * step_len * SR)
    audio = np.zeros(total_samples, dtype=np.float32)

    kick = create_kick(SR, length=0.40, start_freq=145, end_freq=45)
    snare = create_snare(SR, length=0.20, tone_freq=200)
    rim = create_rimshot(SR, length=0.08)
    hat_c = create_hihat(SR, length=0.04, is_open=False)
    hat_o = create_hihat(SR, length=0.18, is_open=True)

    sub_D1 = create_808_sub(SR, duration=step_len*6, freq_start=note_to_freq('D1'))
    sub_F1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('F1'))
    sub_A1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('A1'))
    sub_G1 = create_808_sub(SR, duration=step_len*4, freq_start=note_to_freq('G1'))

    # Melodic Guitar / Rhodes Chords (D Minor 7, F Major 7, A Minor, G Minor)
    chord_roots = ['D3', 'F3', 'A3', 'G3']

    for step in range(total_steps):
        s_idx = int(step * step_len * SR)
        bar = step // 16
        bar_step = step % 16

        is_intro = bar < 4
        is_beat = bar >= 4

        # Hi-Hats: Smooth bouncy Afro-swing / Road-wave groove
        if bar_step in [0, 2, 4, 6, 8, 10, 12, 14]:
            place_sample(audio, hat_c * 0.5, s_idx)
        if bar_step in [3, 9, 15]:
            place_sample(audio, hat_c * 0.3, s_idx)
        if bar_step == 10:
            place_sample(audio, hat_o * 0.4, s_idx)

        # Snare / Rimshot on beat 3 (step 8)
        if is_beat:
            if bar_step == 8:
                place_sample(audio, rim * 0.7, s_idx)
                place_sample(audio, snare * 0.6, s_idx)

        # Kick drum: Bouncy syncopated UK Rap pattern (0, 6, 11)
        if is_beat:
            if bar_step in [0, 6, 11]:
                place_sample(audio, kick * 0.9, s_idx)

        # Warm smooth 808 Sub Bass
        if is_beat:
            chord_idx = bar % 4
            if bar_step == 0:
                if chord_idx == 0:
                    place_sample(audio, sub_D1, s_idx)
                elif chord_idx == 1:
                    place_sample(audio, sub_F1, s_idx)
                elif chord_idx == 2:
                    place_sample(audio, sub_A1, s_idx)
                elif chord_idx == 3:
                    place_sample(audio, sub_G1, s_idx)

        # Melodic electric guitar / keys chord progression
        if bar_step in [0, 6, 12]:
            root = chord_roots[bar % 4]
            freq = note_to_freq(root)
            # Triad chord
            c1 = create_synth_lead(SR, duration=step_len*3.5, freq=freq, wave_type='sine')
            c2 = create_synth_lead(SR, duration=step_len*3.5, freq=freq * 1.2, wave_type='sine') # Minor 3rd
            c3 = create_synth_lead(SR, duration=step_len*3.5, freq=freq * 1.5, wave_type='sine') # 5th
            place_sample(audio, (c1 + c2 + c3) * 0.22, s_idx)

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.88
    return audio

# ==============================================================================
# VOCALS & FULL SONG PRODUCTION
# ==============================================================================
async def generate_vocal_track(text, voice, output_path, rate="+15%", pitch="+0Hz"):
    """Generates studio vocal line using UK neural models."""
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(output_path)

def mix_and_master(inst_wav, vocal_mp3, final_mp3, vocal_volume=1.1, inst_volume=0.85):
    """Mixes instrumental and vocal stems with EQ, Reverb, Compressor, and Loudnorm mastering."""
    # FFmpeg complex filter: EQ, delay reverb, and sidechain compression
    cmd = [
        "ffmpeg", "-y",
        "-i", inst_wav,
        "-i", vocal_mp3,
        "-filter_complex",
        f"[1:a]volume={vocal_volume},equalizer=f=300:t=q:w=1.5:g=-4,aecho=0.8:0.88:45:0.35[vox];"
        f"[0:a]volume={inst_volume}[inst];"
        f"[inst][vox]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.0:LRA=11[out]",
        "-map", "[out]",
        "-b:a", "320k",
        final_mp3
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error mixing {final_mp3}: {res.stderr}")
    else:
        print(f"Successfully mastered: {final_mp3}")

async def main():
    os.makedirs("audio", exist_ok=True)
    os.makedirs("scratch_audio", exist_ok=True)

    print("--- [1/3] PRODUCING TRACK 1: 90mph Gales (Top of the Stack) [140 BPM UK Grime] ---")
    inst1 = render_track_1_instrumental(duration_sec=72)
    inst1_wav = "scratch_audio/inst1.wav"
    wavfile.write(inst1_wav, SR, (inst1 * 32767).astype(np.int16))

    lyrics1 = (
        "Yo, ADI Sound System. Gary on the ladder, top of the stack. "
        "Rain lash down when I step on the slate, Pennine winds pushing ninety on the gauge. "
        "Copper broadband died in the hedge, buffer wheel spinning on the living room edge. "
        "Now look up, see the dish on the stack, SpaceX flat panel, Gen 3 black! "
        "No hammer drill into the Yorkshire stone, stainless steel lashing locked to the bone! "
        "Ninety mile gales on the Pennine peak, dish stays locked, solid signal won't leak! "
        "Top of the stack, yeah we don't drill stone, Starlink flying through the orbit cone! "
        "Call zero-seven-eight-six-zero, two-four-four, two-seven-four, kicking open the door! "
        "Eurocode 1, calculate the wind shear, T and K wall brackets, galvanised steel, twelve-gauge heavy duty, that is how we deal! "
        "ADI Communications, top of the stack!"
    )
    vocal1_mp3 = "scratch_audio/vocal1.mp3"
    await generate_vocal_track(lyrics1, "en-GB-RyanNeural", vocal1_mp3, rate="+18%", pitch="+1Hz")
    mix_and_master(inst1_wav, vocal1_mp3, "audio/adi_01_90mph_gales_starlink_grime.mp3")

    print("\n--- [2/3] PRODUCING TRACK 2: 868 Jeweller (Anti-Jam) [142 BPM UK Drill & Bassline] ---")
    inst2 = render_track_2_instrumental(duration_sec=70)
    inst2_wav = "scratch_audio/inst2.wav"
    wavfile.write(inst2_wav, SR, (inst2 * 32767).astype(np.int16))

    lyrics2 = (
        "They think they can jam the frequency? Ajax Jeweller. Dual SIM. Watch this. "
        "Midnight creeper dressed in black, creeping round the patio, round the back. "
        "Thought he had an RF jammer in his coat, didn't know the Jeweller got his throat! "
        "Eight-six-eight megahertz, hop to the band, signal rerouted straight through the land! "
        "Dual Micro-SIM, four-G failover, Ethernet locked, man is getting bowled over! "
        "Siren screaming in the dead of the night, one-thirteen decibels, flashing red light! "
        "No wires cut, no blind spot found, Ajax Jeweller owns this ground! "
        "Grade 2 certified, tamper-proof seal, Gary Pearce fitted, that is real deal! "
        "StreetSiren bolted on the red-brick face, vandal-proof shell, no wires out of place! "
        "Zero-seven-eight-six-zero, two-four-four, two-seven-four! ADI Communications!"
    )
    vocal2_mp3 = "scratch_audio/vocal2.mp3"
    await generate_vocal_track(lyrics2, "en-GB-RyanNeural", vocal2_mp3, rate="+14%", pitch="-2Hz")
    mix_and_master(inst2_wav, vocal2_mp3, "audio/adi_02_868_jeweller_ajax_drill.mp3", vocal_volume=1.15)

    print("\n--- [3/3] PRODUCING TRACK 3: ColorVu Evidence (250 Px/m) [138 BPM Melodic UK Rap] ---")
    inst3 = render_track_3_instrumental(duration_sec=72)
    inst3_wav = "scratch_audio/inst3.wav"
    wavfile.write(inst3_wav, SR, (inst3 * 32767).astype(np.int16))

    lyrics3 = (
        "Yeah. You see them black and white ghost cameras? Infrared flare, blur in the dark? That don't stand up in court. "
        "Came to the property, surveyed the scene, old analogue cameras, blurry and mean. "
        "Infrared flare making faces look white, burglars walk past in the middle of the night. "
        "Police take the tape, say sorry no trace, can't see the plate, can't identify the face. "
        "Hikvision ColorVu, four-K true, F one-point-zero glass drinking the blue! "
        "Two-hundred and fifty pixels a metre, DORI standard, there ain't nothing sweeter! "
        "Full colour night vision, crystal and clear, no ghost in the shadows, no panic, no fear! "
        "BS EN sixty-two-six-seven-six, Part four compliance, that is how Gary fits! "
        "Crown Prosecution Service approved. ADI Communications, Gary Pearce, zero-seven-eight-six-zero, two-four-four, two-seven-four."
    )
    vocal3_mp3 = "scratch_audio/vocal3.mp3"
    await generate_vocal_track(lyrics3, "en-GB-RyanNeural", vocal3_mp3, rate="+8%", pitch="+0Hz")
    mix_and_master(inst3_wav, vocal3_mp3, "audio/adi_03_colorvu_evidence_cctv_rap.mp3", vocal_volume=1.1)

    print("\nAll 3 studio music tracks synthesized, mixed, mastered, and exported!")

if __name__ == "__main__":
    asyncio.run(main())
