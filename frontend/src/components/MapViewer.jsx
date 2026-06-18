import React from 'react';

const MapViewer = ({ mapUrl }) => {
  return (
    <div className="my-6 w-full max-w-5xl mx-auto">
      <h2 className="text-xl font-semibold mb-2">Religious Distribution Map</h2>
      <iframe
        src={mapUrl}
        title="Religion Map"
        className="w-full h-[500px] border"
      ></iframe>
    </div>
  );
};

export default MapViewer;