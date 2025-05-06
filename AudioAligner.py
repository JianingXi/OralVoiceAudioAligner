import librosa
import numpy as np
import soundfile as sf

# === 0. Configuration: set your actual file paths ===
path1    = r'D:\Alpha\J机智\工作业务\D20250107_笨笨新华思政展播录像\说课录像\Output\笨笨录像Mp3_15.mp3'
path2    = r'D:\Alpha\J机智\工作业务\D20250107_笨笨新华思政展播录像\说课录像\Output\录音15-1.mp3'
out_path = r'D:\Alpha\J机智\工作业务\D20250107_笨笨新华思政展播录像\说课录像\Output\audio2_warp_phasevoc.wav'

# === 1. Load audio ===
y1, sr = librosa.load(path1, sr=None)  # reference (aligned to video)
y2, _  = librosa.load(path2, sr=sr)    # clear re-recording

# === 2. Compute MFCC & DTW path ===
hop = 512
mfcc1 = librosa.feature.mfcc(y=y1, sr=sr, n_mfcc=13, hop_length=hop)
mfcc2 = librosa.feature.mfcc(y=y2, sr=sr, n_mfcc=13, hop_length=hop)
_, wp  = librosa.sequence.dtw(X=mfcc2, Y=mfcc1, metric='euclidean')
wp     = np.array(wp)[::-1]

# === 3. Build continuous time mapping t_source (in seconds) ===
n1 = mfcc1.shape[1]
lists = [[] for _ in range(n1)]
for i2, j1 in wp:
    lists[j1].append(i2)
map_frames = np.array([int(np.median(l)) if l else 0 for l in lists])
t_frame1 = np.arange(n1) * hop / sr
t_map2   = map_frames * hop / sr
t_target = np.linspace(0, len(y1)/sr, num=len(y1))
t_source = np.interp(t_target, t_frame1, t_map2)

# === 4. Phase-vocoder warping ===
# Compute STFT of y2
n_fft = 2048
D2 = librosa.stft(y2, n_fft=n_fft, hop_length=hop)
# Number of output frames
n_frames_out = int(np.ceil(len(y1) / hop)) + 1

# Build frame-level mapping f_idx: for each out frame n, time = n*hop/sr -> t_source -> input frame
frame_times_out = np.arange(n_frames_out) * hop / sr
f_idx = np.interp(frame_times_out, t_target, t_source) * sr / hop
# Clamp
f_idx = np.clip(f_idx, 0, D2.shape[1] - 1)

# Interpolate STFT magnitude+phase
f_lo = np.floor(f_idx).astype(int)
f_hi = np.ceil(f_idx).astype(int)
alpha = f_idx - f_lo
# new STFT
D2_warp = (1 - alpha) * D2[:, f_lo] + alpha * D2[:, f_hi]

# === 5. Invert STFT to time-domain ===
y2_warp = librosa.istft(D2_warp, hop_length=hop, length=len(y1))

# === 6. Append any tail beyond y1 length proportionally (optional) ===
if len(y2) > len(y1):
    tail = y2[len(y1):]
    y2_warp = np.concatenate([y2_warp, tail])

# === 7. Save result ===
sf.write(out_path, y2_warp, sr)
print(f"✅ 完成：Phase vocoder 全局 warp 输出 → {out_path}")
