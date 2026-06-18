import React, { useState } from 'react';
import { uploadAndProcess } from '../api';

const FileUploader = ({ setReport }) => {
  const [files, setFiles] = useState([]);
  const [constituency, setConstituency] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!constituency || files.length === 0) return alert('Please provide all fields.');
    setLoading(true);

    const formData = new FormData();
    formData.append('constituency', constituency);
    for (let file of files) formData.append('files', file);

    try {
      const data = await uploadAndProcess(formData);
      setReport(data);
    } catch (err) {
      alert('Upload failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded bg-white shadow-md w-full max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Upload Voter PDFs</h2>
      <input
        type="text"
        placeholder="Constituency Name"
        className="border p-2 w-full mb-3"
        value={constituency}
        onChange={(e) => setConstituency(e.target.value)}
      />
      <input
        type="file"
        accept=".pdf"
        multiple
        className="mb-3"
        onChange={(e) => setFiles(Array.from(e.target.files))}
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        {loading ? 'Processing...' : 'Submit'}
      </button>
    </form>
  );
};

export default FileUploader;
