// Runs on the audio rendering thread. Converts the mic's Float32 samples to
// Int16 PCM and batches them into ~200ms chunks before handing them to the
// main thread, which forwards them to the backend over the WebSocket.
class PCMRecorderProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._buffer = [];
    this._samplesPerChunk = Math.floor(sampleRate * 0.2);
    this._collected = 0;
  }

  process(inputs) {
    const input = inputs[0];
    if (input && input[0]) {
      this._buffer.push(input[0].slice());
      this._collected += input[0].length;

      if (this._collected >= this._samplesPerChunk) {
        const merged = new Float32Array(this._collected);
        let offset = 0;
        for (const chunk of this._buffer) {
          merged.set(chunk, offset);
          offset += chunk.length;
        }

        const pcm16 = new Int16Array(merged.length);
        for (let i = 0; i < merged.length; i++) {
          const s = Math.max(-1, Math.min(1, merged[i]));
          pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
        }

        this.port.postMessage(pcm16.buffer, [pcm16.buffer]);
        this._buffer = [];
        this._collected = 0;
      }
    }
    return true;
  }
}

registerProcessor("pcm-recorder-processor", PCMRecorderProcessor);
