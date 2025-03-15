import React, { useState, useRef } from "react";

interface AudioRecorderProps {
  onAudioRecorded: (fileUrl: File) => void; // Function to send back the audio URL
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onAudioRecorded }) => {
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);
    audioChunks.current = [];

    mediaRecorder.current.ondataavailable = (event) => {
      if (event.data.size > 0) audioChunks.current.push(event.data);
    };

    mediaRecorder.current.onstop = async () => {
      const audioBlob = new Blob(audioChunks.current, { type: "audio/webm" });

      // Generate a URL
      const fileUrl = URL.createObjectURL(audioBlob);
      var file = new File([audioBlob], "name");

      console.log("Local Blob URL:", fileUrl);

      // Send the URL to parent component
      onAudioRecorded(file);
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorder.current?.stop();
    setRecording(false);
  };

  const sendAudioFile = (file: Blob) => {
    const formData = new FormData();
    formData.append('audio-file', file);
    return fetch('http://localhost:3000/audioUpload', {
      method: 'POST',
      body: formData
    });
  };

  return (
    <div>
      <button
        className={`w-24 text-white text-lg rounded-lg ml-2 p-2 ${
          recording ? "bg-red-600 hover:bg-red-800" : "bg-gray-600 hover:bg-gray-800"
        }`}
        onClick={recording ? stopRecording : startRecording}
      >
        {recording ? "REC..." : "🎙️"}
      </button>
    </div>
  );
};

export default AudioRecorder;
