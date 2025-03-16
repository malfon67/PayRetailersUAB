import React, { useState, useRef, useEffect } from "react";

interface AudioRecorderProps {
  onAudioRecorded: (fileUrl: File, recording: boolean) => void; 
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onAudioRecorded }) => {
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (recording) {
      startRecording();
    } else if (mediaRecorder.current) {
      stopRecording();
    }
  }, [recording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: "audio/webm" });
        const file = new File([audioBlob], "recording.webm");

        // Send recorded audio to parent
        onAudioRecorded(file, false); // Notify stop
      };

      mediaRecorder.current.start();
      onAudioRecorded(new File([], ""), true); // Notify start
    } catch (error) {
      console.error("Error accessing microphone:", error);
      setRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
    }
    setRecording(false);
  };

  return (
    <div className="flex flex-row items-center">
      <button
        className={`text-white text-lg rounded-lg ml-2 p-2 ${
          recording ? "bg-red-600 hover:bg-red-800" : "bg-gray-600 hover:bg-gray-800"
        }`}
        onClick={() => setRecording((prev) => !prev)}
        title="Graba una nota de voz"
      >
        {recording ? "REC..." : "🎙️"}
      </button>
    </div>
  );
};

export default AudioRecorder;
